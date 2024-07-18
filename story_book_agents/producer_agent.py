""" This module contains the ProducerAgent class."""
from autogen import AssistantAgent


PRODUCER_AGENT_NAME = "Producer"

PRODUCER_AGENT_SYSTEM_MESSAGE = """
    You are a producer for a children's storybook creation team. Your task is to assist team members in completing the picture book using only the tools provided to you.
    """
PRODUCER_AGENT_DESCRIPTION = "Producer, assisting team members in completing the picture book using the provided tools."

class ProducerAgent(AssistantAgent):
    """ 儿童故事绘本制作团队的制作人，协助团队成员完成绘本的制作 """

    def __init__(self, gpt_config):
        super().__init__(
            name=PRODUCER_AGENT_NAME,
            llm_config=gpt_config,
            system_message=PRODUCER_AGENT_SYSTEM_MESSAGE,
            human_input_mode="NEVER",
            code_execution_config=False,
            description=PRODUCER_AGENT_DESCRIPTION
        )
