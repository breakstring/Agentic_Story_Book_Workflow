""" This module contains the ProducerAgent class."""
from autogen import AssistantAgent


PRODUCER_AGENT_NAME = "Producer"

PRODUCER_AGENT_SYSTEM_MESSAGE = """
    你是一个儿童故事绘本制作团队的制作人，你的任务是仅仅根据提供给你的工具，协助团队成员完成绘本的制作。
    """
PRODUCER_AGENT_DESCRIPTION = "儿童故事绘本制作团队的制作人，根据提供的工具协助团队成员完成绘本的制作"

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
