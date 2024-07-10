"""app.py"""
import os

from typing import Union

import autogen
import autogen.types
import dotenv

from autogen import UserProxyAgent, GroupChatManager, GroupChat, Agent
from story_book_agents import StoryEditorAgent, ITAssistantAgent, ReceptionistAgent, StoryCriticAgent, ProducerAgent
from story_book_agents.tools.utils import save_story_content


# prepare the LLM configurations
dotenv.load_dotenv()
gpt_config_list_default = [{
    "model": os.environ.get("MODEL"),
    "api_key": os.environ.get("API_KEY"),
    "base_url": os.environ.get("BASE_URL"),
    "api_type": os.environ.get("API_TYPE"),
    "api_version": os.environ.get("API_VERSION"),
}]
gpt_config_high_temperature = {
    "config_list": gpt_config_list_default,
    "temperature": 0.7,
    "cache_seed": None
}
gpt_config_low_temperature = {
    "config_list": gpt_config_list_default,
    "temperature": 0,
    "cache_seed": None
}


user_agent = UserProxyAgent(
    name="User",
    llm_config=False,
    human_input_mode="ALWAYS",
    code_execution_config=False,
)

producer_agent = ProducerAgent(gpt_config_low_temperature)
reception_agent = ReceptionistAgent(gpt_config_high_temperature)
story_editor_agent = StoryEditorAgent(gpt_config_high_temperature)
it_assistant_agent = ITAssistantAgent(gpt_config_low_temperature)
story_critic_agent = StoryCriticAgent(gpt_config_high_temperature)

# story_editor_agent.register_for_llm(name="generate_story_id", description="生成故事ID")(generate_story_id)
producer_agent.register_for_llm(
    name="save_story_content", description="保存故事内容")(save_story_content)


it_assistant_agent.register_for_execution(
    name="save_story_content")(save_story_content)
# it_assistant_agent.register_for_execution(name="generate_story_id")(generate_story_id)


def story_draft_group_speaker_selection_func(
        last_speaker: Agent, groupchat: GroupChat
) -> Union[Agent, str, None]:
    """
    故事草稿组的发言选择函数
    """
    _groupchat = groupchat
    if last_speaker == it_assistant_agent:
        return None
    else:
        return "auto"


# setup a chat group with the receptionist agent, story editor agent, and IT assistant agent
story_draft_group = GroupChat(
    agents=[
        producer_agent,
        story_editor_agent,
        it_assistant_agent,
        story_critic_agent,
    ],
    messages=[],
    max_round=10,
    speaker_selection_method=story_draft_group_speaker_selection_func,
    select_speaker_message_template="""
    你是一个故事草稿组的管理员，你们正在为一个儿童故事绘本创作文字内容，你需要根据当前对话的上下文内容，选择下一个发言的人。

    故事草稿组的工作流程如下：
    1. 首先，请 'Story_Editor' 来编写故事内容。
    2. 当故事内容编写完毕后，请 'Story_Critic' 来审阅故事内容并给出修改意见。
    3. 如果故事内容需要修改，则请 'Story_Editor' 再来修改故事内容。
    4. 如果故事内容无需修改（即返回内容中包含 "CRITIC_DONE" ），那么就请 'Producer' 来保存故事内容并输出 "STORY_SAVED"结束对话。
    
    请直接返回下一个发言的角色，除此之外不要返回任何内容。
    """,
    select_speaker_prompt_template=None,
)

story_draft_group_manager = GroupChatManager(
    name="StoryDraftGroup",
    groupchat=story_draft_group,
    llm_config=gpt_config_low_temperature,
    human_input_mode="NEVER",
    code_execution_config=False,
    silent=False,
    is_termination_msg=lambda msg: "STORY_SAVED" in msg["content"].lower(),
)


reception_chat = {
    "sender": user_agent,
    "recipient": reception_agent,
    "message": "我想要一个儿童绘本故事",
    "max_turns": 10,
    "summary_method": "reflection_with_llm",
    "summary_args": {
        "summary_prompt": """Summarize the takeaway from the conversation. Do not add any introductory phrases.
        总结的结果需要的语言需要和用户期望得到的绘本的语言保持一致。
        """
    }
}

story_draft_chat = {
    "sender": reception_agent,
    "recipient": story_draft_group_manager,
    "message": "用户需求整理完毕，请创作故事内容并保存故事内容。",
    "max_turns": 1,
    "summary_method": "reflection_with_llm",
    "summary_args": {
        "summary_prompt": """
        请从上方的对话中总结出故事ID，直接输出故事ID即可，不要输出任何其他内容。
        """
    }
}

# entry point
if __name__ == '__main__':
    # Start logging
    LOGGING_SESSION_ID = autogen.runtime_logging.start(
        config={"dbname": "./output/logs.db"})
    print("Logging session ID: " + str(LOGGING_SESSION_ID))

    chat_results = autogen.agentchat.initiate_chats([
        reception_chat,
        story_draft_chat
    ])
    print(chat_results[0].summary)
    print(chat_results[1].summary)

    autogen.runtime_logging.stop()
