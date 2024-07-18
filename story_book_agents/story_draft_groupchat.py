""" Story Draft Group Chat  """

from typing import Union
from autogen.agentchat import Agent, GroupChat, GroupChatManager

import story_book_agents
from .agent_manager import agent_manager_instance


STORY_DRAFT_GROUP_SELECT_SPEAKER_MESSAGE_TEMPLATE = """
You are an AI assistant acting as the administrator of a story draft group. Your task is to determine who should speak next in the story creation process based on the current conversation context and the established workflow.

The story draft group follows this workflow:
1. The Story_Editor writes the story content.
2. Once the story content is written, the Story_Critic reviews it and provides feedback.
3. If the story needs revisions, the Story_Editor makes the necessary changes.
4. If no further revisions are needed (indicated by "CRITIC_DONE" in the response), the Producer saves the story content.

Your job is to analyze the conversation context and determine which role should speak next according to this workflow.

To make your determination:
1. Examine the last speaker and their contribution in the conversation context.
2. Consider the current stage of the story creation process based on the workflow.
3. Identify the appropriate next step and the corresponding role that should speak.

Provide your response by simply stating the role of the next speaker. Do not include any additional explanation or content. Your response should be one of the following:
- Story_Editor
- Story_Critic
- Producer
"""

def story_draft_group_speaker_selection_func(
        last_speaker: Agent, groupchat: GroupChat
) -> Union[Agent, str, None]:
    """
    Determine the next speaker in the story draft group based on the conversation context and the established workflow.
    """
    _groupchat = groupchat
    if last_speaker == agent_manager_instance.default_it_assistant_agent:
        return None
    else:
        return "auto"

def init_story_draft_groupchat()->GroupChat:
    story_draft_groupchat = GroupChat(
        agents=[
            agent_manager_instance.default_producer_agent,
            agent_manager_instance.default_story_editor_agent,
            agent_manager_instance.default_story_critic_agent,
            agent_manager_instance.default_it_assistant_agent,
        ],
        messages=[],
        max_round=10,
        speaker_selection_method=story_draft_group_speaker_selection_func,
        select_speaker_message_template=STORY_DRAFT_GROUP_SELECT_SPEAKER_MESSAGE_TEMPLATE,
        select_speaker_prompt_template=None,
    )
    return story_draft_groupchat

def init_story_draft_group_manager()->GroupChatManager:
    story_draft_group_manager = GroupChatManager(
        name="StoryDraftGroup",
        groupchat=init_story_draft_groupchat(),
        llm_config=story_book_agents.gpt_config_low_temperature,
        human_input_mode="NEVER",
        code_execution_config=False,
        silent=False,
    )
    return story_draft_group_manager

def set_story_draft_chat():
    story_draft_chat = {
        "sender": agent_manager_instance.default_receptionist_agent,
        "recipient": init_story_draft_group_manager(),
        "message": "User requirements have been compiled. Please create the story content and save it.",
        "max_turns": 1,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": """
            Please summarize the story ID from the above conversation and output the story ID directly. Do not output any other content.
            """
        }
    }
    return story_draft_chat
