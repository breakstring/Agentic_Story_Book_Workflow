''' IT assistant agent'''

from autogen import AssistantAgent


IT_ASSISTANT_AGENT_NAME="Team_Assistant"
IT_ASSISTANT_AGENT_SYSTEM_MESSAGE="""
你是团队中的IT助理，你的任务是辅助团队成员完成任务。
主要工作是：
- 生成故事的ID
- 保存故事内容

"""
IT_ASSISTANT_AGENT_DESCRIPTION = "生成故事的ID，保存故事内容。"

class ITAssistantAgent(AssistantAgent):
    ''' IT assistant agent'''
    def __init__(self,gpt_config):
        super().__init__(
            name=IT_ASSISTANT_AGENT_NAME,
            system_message=IT_ASSISTANT_AGENT_SYSTEM_MESSAGE,
            description=IT_ASSISTANT_AGENT_DESCRIPTION,
            llm_config=gpt_config,
            code_execution_config=False,
            human_input_mode="NEVER",
        )
