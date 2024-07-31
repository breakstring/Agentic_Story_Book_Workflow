""" Image critic agent """

from typing import Dict, List, Optional, Tuple, Union
from autogen import OpenAIWrapper,Agent,AssistantAgent
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

from autogen._pydantic import model_dump

IMAGE_CRITIC_AGENT_NAME = "Image_Critic"
IMAGE_CRITIC_AGENT_SYSTEM_MESSAGE_TEMPLATE = """
You are a visual review expert for a children's storybook creation team. Your task is to review an image based on a provided storyboard script to determine if it meets the requirements for the storybook.

First, carefully read and understand the following storyboard content:
```json
{STORYBOARD}
```

The current frame number being reviewed is {FRAME_NUMBER}, and the prompt used to generate the image is:

<Prompt>
{PROMPT}
</Prompt>

Now, carefully examine the provided image.

Analyze the image based on the following criteria:

1. Overall story coherence: Does the image align with the overall story content?
2. Current frame requirements: Does the image meet the specific needs of the current frame as described in the storyboard?
3. Children's storybook visual standards: Does the image adhere to typical visual requirements for children's storybooks?
4. Logical consistency: Are there any logical errors in the image that might hinder story comprehension?
5. Visual element improvements: Are there any details that could be enhanced, such as color scheme, environment, shapes, lighting, character layout, or camera angle?

After your analysis, respond in one of two ways:

1. If you believe the image is satisfactory and doesn't require improvements, simply output:
CRITIC_DONE

2. If you think the image needs improvement, JUST provide a new prompt in the following format only:
PROMPT:[Your improved prompt here]


Ensure your improved prompt addresses the specific areas that need enhancement while maintaining the core elements of the original prompt and story requirements.
And also please note that your prompt should avoid words and expressions related to violence, pornography, politics, and similar topics as much as possible.
"""

IMAGE_CRITIC_AGENT_DESCRIPTION = "This agent is responsible for reviewing images based on storyboard scripts for children's storybooks."


class ImageCriticAgent(AssistantAgent):
    """ This agent is responsible for reviewing images based on storyboard scripts for children's storybooks. """

    def __init__(self, gpt_config, storyboard: str, frame_number: int, prompt: str,*args,**kwargs,):
        super().__init__(
            name=IMAGE_CRITIC_AGENT_NAME,
            description=IMAGE_CRITIC_AGENT_DESCRIPTION,
            system_message=IMAGE_CRITIC_AGENT_SYSTEM_MESSAGE_TEMPLATE.format(
                STORYBOARD=storyboard, FRAME_NUMBER=frame_number, PROMPT=prompt),
            max_consecutive_auto_reply=None,
            human_input_mode="NEVER",
            llm_config=gpt_config,
            code_execution_config=False,
            *args,
            **kwargs,
        )

    def generate_oai_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[OpenAIWrapper] = None,
    ) -> Tuple[bool, Union[str, Dict, None]]:
        """Generate a reply using autogen.oai."""
        client = self.client if config is None else config
        if client is None:
            return False, None
        if messages is None:
            messages = self._oai_messages[sender]

        img_url_message = {
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": messages[-1]["content"]},
                }
            ]
        }
        response = client.create(context=messages[-1].pop("context", None), messages=img_url_message)

        extracted_response = client.extract_text_or_completion_object(response)[0]
        if not isinstance(extracted_response, str):
            extracted_response = model_dump(extracted_response)
        return True, extracted_response
