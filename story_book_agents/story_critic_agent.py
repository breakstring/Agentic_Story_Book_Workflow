"""
This agent's role is to review the content of children's stories created by story editors and provide critical feedback.
"""
from autogen import AssistantAgent

STORY_CRITIC_AGENT_NAME="Story_Critic"
STORY_CRITIC_AGENT_SYSTEM_MESSAGE = """
# 背景信息
你是一个儿童故事内容评审专家，你的任务是评审其他儿童故事内容创作者所撰写的儿童故事并提出修改意见。 \n

# 任务说明
你将根据用户的基本需求以及创作出来的故事内容进行审核，并提出修改意见。

# 无需修改的内容
如果你觉得现在的故事结构已经很好，不需要做任何修改，可以直接返回“CRITIC_DONE”。

# 如果你觉得故事还可以改进，那么在编写修改意见的时候，请注意通过一下几点来改进故事内容：
- 内容安全：确保故事内容是合适的，不包含任何不适合儿童的内容，如暴力、色情等。故事内容是积极向上传递正能量的。
- 内容有趣：确保故事内容是简单的，儿童容易理解的。并且是有趣的，能够引起儿童的兴趣。 
- 故事完整：确保故事内容是完整的，没有遗漏，并具有一定的教育意义。

# 建议的输出
请严格按照以下<XML>格式返回你的修改的建议要点，不要包含任何其他额外的内容，也不用返回原来的故事内容全文:
<Feedback>
修改意见
</Feedback>

"""
STORY_CRITIC_AGENT_DESCRIPTION = "This agent's role is to review the content of children's stories created by story editors and provide critical feedback."


class StoryCriticAgent(AssistantAgent):
    """ This agent's role is to review the content of children's stories created by story editors and provide critical feedback. """

    def __init__(self, gpt_config):
        super().__init__(
            name=STORY_CRITIC_AGENT_NAME,
            description=STORY_CRITIC_AGENT_DESCRIPTION,
            system_message=STORY_CRITIC_AGENT_SYSTEM_MESSAGE,
            max_consecutive_auto_reply=None,
            human_input_mode="NEVER",
            llm_config=gpt_config,
            code_execution_config=False,
            )
