""" Image generation agent """

from typing import Dict, List, Optional, Tuple, Union
from autogen import ConversableAgent, Agent
from .tools.image import generate_image_by_prompt

IMAGE_GENERATION_AGENT_NAME = "Image_Generator"


class ImageGenerationAgent(ConversableAgent):
    """ This agent is responsible for generating images based on storyboard scripts for children's storybooks. """

    def __init__(self, gpt_config, *args, **kwargs):
        super().__init__(
            name=IMAGE_GENERATION_AGENT_NAME,
            llm_config=gpt_config,
            *args,
            **kwargs)

        self.register_reply(
            [Agent, None], ImageGenerationAgent._generate_dalle_reply, position=0)

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        # override and always "silent" the send out message;
        # otherwise, the print log would be super long!
        super().send(message, recipient, request_reply, silent=True)

    def _generate_dalle_reply(self, messages: Optional[List[Dict]], sender: "Agent", config) -> Tuple[bool, Union[str, Dict, None]]: # pylint: disable=unused-argument

        if messages is None:
            messages = self._oai_messages[sender]

        prompt = messages[-1]["content"]
        img_url, revised_prompt = generate_image_by_prompt(prompt)

        # Return the OpenAI message format
        return True, {"content": [{"type": "image_url", "image_url": {"url": img_url}, "prompt": revised_prompt}]}
