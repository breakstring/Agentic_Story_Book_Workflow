"""app.py"""
import os
import autogen
import autogen.runtime_logging
import autogen.types
import dotenv
import agentops

from autogen import UserProxyAgent
from story_book_agents import agent_manager_instance, story_draft_groupchat,storyboard_groupchat

import story_book_agents


# prepare the LLM configurations
dotenv.load_dotenv()

gpt_config_list_default = [{
    "model": os.environ.get("MODEL"),
    "api_key": os.environ.get("API_KEY"),
    "base_url": os.environ.get("BASE_URL"),
    "api_type": os.environ.get("API_TYPE"),
    "api_version": os.environ.get("API_VERSION"),
}]

dalle_config = {
    "config_list": [{
        "model": os.environ.get("DALLE_MODEL"),
        "api_key": os.environ.get("DALLE_API_KEY"),
        "base_url": os.environ.get("DALLE_BASE_URL"),
        "api_type": os.environ.get("DALLE_API_TYPE"),
        "api_version": os.environ.get("DALLE_API_VERSION"),
    }],
    "timeout": 120,
    "temperature": 0.7,
    "max_tokens": 2000

}

agentops.init(api_key=os.environ.get("AGENTOPS_API_KEY"))

story_book_agents.init_agents(gpt_config_list_default)
# create a UserProxyAgent instance
user_agent = UserProxyAgent(
    name="User",
    llm_config=False,
    human_input_mode="ALWAYS",
    code_execution_config=False,
)


def main():
    """Main function."""
    preliminary_story_requirements = "给我讲一个小狐狸的故事吧"
    chat_results = autogen.agentchat.initiate_chats([
        # Obtain preliminary requirements through the conversation with the Receptionist agent.
        {
            "sender": user_agent,
            "recipient": agent_manager_instance.default_receptionist_agent,
            "message": preliminary_story_requirements,
            "max_turns": 10,
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": """Summarize the takeaway from the conversation. Do not add any introductory phrases.
                                    If the user has explicitly specified a language for the picture book, then the language used in the summary should be consistent with the language specified by the user for the picture book; otherwise, the language used in the summary should be consistent with the main language the user used during the conversation.
                                    """
            }
        },
        # The Story Draft Group includes agents such as the Story Editor, Story Critic, Producer, and IT Assistant. They communicate through a group chat to create, review, and store the story content.
        story_draft_groupchat.set_story_draft_chat()
    ])
    story_id = chat_results[1].summary
    print("Story ID: " + story_id)
    chat_results2= autogen.agentchat.initiate_chats(
        [storyboard_groupchat.set_storyboard_chat(story_id)]
    )
    print(chat_results2[0].summary)



# entry point
if __name__ == '__main__':
    main()
    
