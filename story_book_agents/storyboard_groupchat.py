''' Storyboard group chat module'''

from typing import Union
from autogen import GroupChat, Agent, GroupChatManager

import story_book_agents
from .agent_manager import agent_manager_instance

STORYBOARD_GROUP_SELECT_SPEAKER_MESSAGE_TEMPLATE = """
You are an AI assistant acting as the administrator of a storyboard group.
Your task is to determine who should speak next in the storyboard creation process based on the current conversation context and the established workflow.

The storyboard group follows this workflow:
1. The Producer loads the story content based on the story ID.
2. The Storyboard_Editor creates the storyboard based on the story content.
3. Once the storyboard is created, the Storyboard_Critic reviews it and provides feedback.
4. If the storyboard needs revisions, the Storyboard_Editor makes the necessary changes.
5. If no further revisions are needed (indicated by "CRITIC_DONE" in the response), the Producer saves the storyboard.

Your job is to analyze the conversation context and determine which role should speak next according to this workflow.

To make your determination:
1. Examine the last speaker and their contribution in the conversation context.
2. Consider the current stage of the storyboard creation process based on the workflow.
3. Identify the appropriate next step and the corresponding role that should speak.

Remember, the storyboard group is responsible for creating a coherent and engaging storyboard based on the user's input.

Provide your response by simply stating the role of the next speaker. Do not include any additional explanation or content. Your response should be one of the following:
- Producer
- Storyboard_Editor
- Storyboard_Critic

"""


def storyboard_group_speaker_selection_func(
        last_speaker: Agent, groupchat: GroupChat
) -> Union[Agent, str, None]:
    """
    Determine the next speaker in the story draft group based on the conversation context and the established workflow.
    """
    _groupchat = groupchat
    if last_speaker == agent_manager_instance.default_it_assistant_agent and  _groupchat.messages[-1] == "Success":
        return None
    else:
        return "auto"


def init_storyboard_groupchat() -> GroupChat:
    storyboard_groupchat = GroupChat(
        agents=[
            agent_manager_instance.default_receptionist_agent,
            agent_manager_instance.default_producer_agent,
            agent_manager_instance.default_storyboard_editor_agent,
            agent_manager_instance.defualt_storyboard_critic_agent,
            agent_manager_instance.default_it_assistant_agent,
        ],
        messages=[],
        max_round=10,
        speaker_selection_method=storyboard_group_speaker_selection_func,
        select_speaker_message_template=STORYBOARD_GROUP_SELECT_SPEAKER_MESSAGE_TEMPLATE,
        select_speaker_prompt_template=None,
    )
    return storyboard_groupchat


def init_storyboard_group_manager() -> GroupChatManager:
    storyboard_group_manager = GroupChatManager(
        name="StoryboardGroup",
        groupchat=init_storyboard_groupchat(),
        llm_config=story_book_agents.gpt_config_low_temperature,
        human_input_mode="NEVER",
        code_execution_config=False,
        silent=False,
    )
    return storyboard_group_manager


def set_storyboard_chat(strory_id: str):
    storyboard_chat = {
        "sender": agent_manager_instance.default_receptionist_agent,
        "recipient": init_storyboard_group_manager(),
        "message": "The story ID is: "+strory_id + ". Please load the story content, and create the storyboard. Onece the storyboard is ready, save it.",
        #"max_turns": 1,
        "summary_method": "reflection_with_llm",
    }
    return storyboard_chat
