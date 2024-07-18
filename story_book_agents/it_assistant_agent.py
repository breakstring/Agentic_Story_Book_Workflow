''' IT assistant agent'''

from autogen import AssistantAgent


IT_ASSISTANT_AGENT_NAME="IT_Assistant"
IT_ASSISTANT_AGENT_SYSTEM_MESSAGE="""
You are the IT assistant in the team. Your task is to assist team members in completing their tasks.
Your main responsibilities are:
- Generate a story ID for the story content.
- Save the story content.

"""
IT_ASSISTANT_AGENT_DESCRIPTION = "IT assistant, generate the story id and save stroy content."

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
