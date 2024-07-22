"""This module contains the AgentManager class which is used to manage all the default agent instance in the story book system"""

class AgentManager:
    """Agent Manager used to manage all the default agent instance in the story book system"""
    def __init__(self) -> None:
        self.default_receptionist_agent = None
        self.default_story_editor_agent = None
        self.default_it_assistant_agent = None
        self.default_story_critic_agent = None
        self.default_producer_agent = None
        self.default_storyboard_editor_agent = None
        self.defualt_storyboard_critic_agent = None
        self.default_text_to_image_prompt_editor_agent = None
        self.default_text_to_image_prompt_critic_agent = None

agent_manager_instance = AgentManager()
