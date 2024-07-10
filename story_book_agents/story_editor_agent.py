"""
This agent is responsible for creating a kid's story book based on the user's input.
"""
from autogen import AssistantAgent

STORY_EDITOR_AGENT_NAME="Story_Editor"
STORY_EDITOR_AGENT_SYSTEM_MESSAGE = """
# 背景信息
你是一个儿童绘本编辑师，你的任务是为孩子们创作有趣的绘本故事。 \n

# 任务说明
你将根据用户提供给你的一些基本信息来创建一个儿童故事绘本的概要内容。

# 内容要求
- 请确保你的故事内容是有趣的，能够引起儿童的兴趣。
- 请确保你的故事内容是简单的，容易理解的。
- 请确保你的故事内容是积极向上的，能够传递正能量。
- 请确保你的故事内容是合适的，不包含任何不适合儿童的内容。

# 结构要求
- 你需要给这个故事拟定一个标题。
- 绘本故事的内容不需要你按照分页来做描述，你只需要讲述整个故事即可。对于每一页的拆分，我们会在后续的环节中由其他人进行处理。

# 输出格式
请严格按照以下<XML>格式返回你的标题和绘本故事内容，不要包含任何其他额外的内容:

<Story>
    <Title>故事标题</Title>
    <Content>故事内容</Content>
<Stroy>

"""
STORY_EDITOR_AGENT_DESCRIPTION = "This agent is responsible for creating a kid's story book based on the user's input."


class StoryEditorAgent(AssistantAgent):
    """ This agent is responsible for creating a kid's story book based on the user's input. """

    def __init__(self, gpt_config):
        super().__init__(
            name=STORY_EDITOR_AGENT_NAME,
            description=STORY_EDITOR_AGENT_DESCRIPTION,
            system_message=STORY_EDITOR_AGENT_SYSTEM_MESSAGE,
            max_consecutive_auto_reply=None,
            human_input_mode="NEVER",
            llm_config=gpt_config,
            code_execution_config=False,
            )

