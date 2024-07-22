""" agents modules """

from .story_editor_agent import StoryEditorAgent
from .receptionist_agent import ReceptionistAgent
from .it_assistant_agent import ITAssistantAgent
from .story_critic_agent import StoryCriticAgent
from .producer_agent import ProducerAgent
from .storyboard_editor_agent import StoryboardEditorAgent
from .storyboard_critic_agent import StoryboardCriticAgent
from .text_to_image_prompt_editor_agent import TextToImagePromptEditorAgent
from .text_to_image_prompt_critic_agent import TextToImagePromptCriticAgent
from .tools.utils import save_story_content, load_story_content_by_id,save_storyboard_by_story_id,save_prompts_by_story_id


from .agent_manager import agent_manager_instance


gpt_config_high_temperature={
        "config_list": [],
        "temperature": 0.7,
        "cache_seed": None,
        "max_tokens": 4096
    }
gpt_config_low_temperature={
        "config_list": [],
        "temperature": 0,
        "cache_seed": None,
        "max_tokens": 4096
    }

def init_agents(default_gpt_config):
    """ init all agents """
    gpt_config_high_temperature["config_list"]=default_gpt_config
    gpt_config_low_temperature["config_list"]=default_gpt_config

    # init agents
    agent_manager_instance.default_receptionist_agent = ReceptionistAgent(
        gpt_config_high_temperature)
    agent_manager_instance.default_story_editor_agent = StoryEditorAgent(
        gpt_config_high_temperature)
    agent_manager_instance.default_it_assistant_agent = ITAssistantAgent(
        gpt_config_low_temperature)
    agent_manager_instance.default_story_critic_agent = StoryCriticAgent(
        gpt_config_low_temperature)
    agent_manager_instance.default_producer_agent = ProducerAgent(
        gpt_config_low_temperature)
    agent_manager_instance.default_storyboard_editor_agent = StoryboardEditorAgent(
        gpt_config_high_temperature)
    agent_manager_instance.defualt_storyboard_critic_agent = StoryboardCriticAgent(
        gpt_config_low_temperature)
    agent_manager_instance.default_text_to_image_prompt_editor_agent = TextToImagePromptEditorAgent(gpt_config_high_temperature)
    agent_manager_instance.default_text_to_image_prompt_critic_agent = TextToImagePromptCriticAgent(gpt_config_low_temperature)

    agent_manager_instance.default_producer_agent.register_for_llm(name="save_story_content", description="save story content")(save_story_content)
    agent_manager_instance.default_producer_agent.register_for_llm(name="load_story_content_by_id", description="load story content by id")(load_story_content_by_id)
    agent_manager_instance.default_producer_agent.register_for_llm(name="save_storyboard_by_story_id", description="save storyboard by story id")(save_storyboard_by_story_id)
    agent_manager_instance.default_producer_agent.register_for_llm(name="save_prompts_by_story_id", description="save prompts by story id")(save_prompts_by_story_id)

    agent_manager_instance.default_it_assistant_agent.register_for_execution(name="save_story_content")(save_story_content)
    agent_manager_instance.default_it_assistant_agent.register_for_execution(name="load_story_content_by_id")(load_story_content_by_id)
    agent_manager_instance.default_it_assistant_agent.register_for_execution(name="save_storyboard_by_story_id")(save_storyboard_by_story_id)
    agent_manager_instance.default_it_assistant_agent.register_for_execution(name="save_prompts_by_story_id")(save_prompts_by_story_id)

__all__ = ['init_agents', 'agent_manager_instance',"gpt_config_high_temperature","gpt_config_low_temperature"]
