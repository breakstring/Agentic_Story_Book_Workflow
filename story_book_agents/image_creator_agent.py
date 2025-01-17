""" This module contains the ImageCreatorAgent class. """

import os
from autogen import AssistantAgent, Agent

from .tools.image import save_image_from_url
from .image_generation_agent import ImageGenerationAgent
from .image_critic_agent import ImageCriticAgent
from .tools.utils import get_storyboard_by_story_id, get_prompt_by_story_id_and_frame_number

IMAGE_CREATOR_AGENT_NAME = "Image_Creator"
IMAGE_CREATOR_AGENT_DESCRIPTION = "This agent is responsible for generating images based on storyboard scripts for children's storybooks."


class ImageCreatorAgent(AssistantAgent):
    """ This agent is responsible for generating images based on storyboard scripts for children's storybooks. """

    def __init__(self, gpt_config, story_id: str, frame_number: int, *args, **kwargs):
        super().__init__(
            name=IMAGE_CREATOR_AGENT_NAME,
            description=IMAGE_CREATOR_AGENT_DESCRIPTION,
            llm_config=gpt_config,
            *args,
            **kwargs)

        self._story_id = story_id
        self._n_iters = int(os.environ.get("IMAGE_CRITICISM_RETRIES", 2))
        self.register_reply(
            [Agent, None], reply_func=ImageCreatorAgent._reply_user, position=0)
        self._image_generator = None
        self._image_critic = None
        self._storyboard = get_storyboard_by_story_id(self._story_id)
        self._frame_number = frame_number

    def _generate_image(self, img_prompt):
        self.send(message=img_prompt,
                  recipient=self._image_generator, request_reply=True)
        last_generation_result = self._image_generator.last_message()

        if not isinstance(last_generation_result, dict):
            raise TypeError("Expected last_message to be a dictionary")

        img_url = last_generation_result["content"][-1]["image_url"]["url"]
        if os.environ.get("IMAGE_GENERATION_TYPE") == "azure" or os.environ.get("IMAGE_GENERATION_TYPE") == "openai":
            real_prompt = last_generation_result["content"][-1]["prompt"]
        else:
            real_prompt = img_prompt
        
        print(f"Generated image: {img_url}")
        # if os environ IMAGE_SAVE_FAILURED_IMAGES is set to True, save the image
        if bool(os.environ.get("IMAGE_SAVE_FAILURED_IMAGES", "False")):
            save_image_from_url(story_id=self._story_id,frame_index=self._frame_number,image_url=img_url,is_final=False)
        return img_url, real_prompt

    def _reply_user(self, messages=None, sender=None, config=None):  # pylint: disable=unused-argument
        if all((messages is None, sender is None)):
            error_msg = f"Either {messages=} or {sender=} must be provided."
            raise AssertionError(error_msg)

        if messages is None:
            messages = self._oai_messages[sender]

        img_prompt = get_prompt_by_story_id_and_frame_number(
            self._story_id, self._frame_number)

        self._image_generator = ImageGenerationAgent(gpt_config=self.llm_config,
                                                     max_consecutive_auto_reply=0)

        img_url, real_prompt = self._generate_image(img_prompt)

        if self._n_iters > 0:
            self._image_critic = ImageCriticAgent(gpt_config=self.llm_config,
                                                  storyboard=self._storyboard,
                                                  frame_number=self._frame_number,
                                                  prompt=real_prompt,
                                                  )

            for _ in range(self._n_iters):
                self.send(message={
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": img_url},
                        }
                    ]},
                    recipient=self._image_critic,
                    request_reply=True)
                last_critic_result = self._image_critic.last_message()
                if not isinstance(last_critic_result, dict):
                    raise TypeError("Expected last_message to be a dictionary")

                if "CRITIC_DONE" in last_critic_result["content"]:
                    break

                img_prompt = last_critic_result["content"].split("PROMPT:")[1]

                img_url, real_prompt = self._generate_image(img_prompt)

        return True, {"content": [{"type": "image_url", "image_url": {"url": img_url}, "prompt": real_prompt}]}
