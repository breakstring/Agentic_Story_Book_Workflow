
import os
import dotenv
from autogen import UserProxyAgent
from story_book_agents.tools.pptx import create_pptx
from story_book_agents.tools.utils import get_storyboard_by_story_id,update_prompt_by_story_id_and_frame_number
from story_book_agents.tools.image import save_image_from_url
from story_book_agents.tools.video import create_video
from story_book_agents.tools.voice import text_to_speech
from story_book_agents.image_creator_agent import ImageCreatorAgent
dotenv.load_dotenv(override=True)


story_id = "8b403fab-0d8d-4c64-a72c-03b02ce1e4d6"
storyboard = get_storyboard_by_story_id(story_id=story_id)

user_proxy = UserProxyAgent("UserProxyAgent",
                            llm_config={"config_list": [{
                                "model": os.environ.get("MODEL"),
                                "api_key": os.environ.get("API_KEY"),
                                "base_url": os.environ.get("BASE_URL"),
                                "api_type": os.environ.get("API_TYPE"),
                                "api_version": os.environ.get("API_VERSION"),
                            }]},
                            human_input_mode="NEVER",
                            system_message="A human admin",
                            code_execution_config=False,
                            max_consecutive_auto_reply=0)


for frame in storyboard:
    frame_number = frame["Index"]
    story_content = frame["StoryContent"]

    image_creator = ImageCreatorAgent(
        gpt_config={"config_list": [{
            "model": os.environ.get("MODEL"),
            "api_key": os.environ.get("API_KEY"),
            "base_url": os.environ.get("BASE_URL"),
            "api_type": os.environ.get("API_TYPE"),
            "api_version": os.environ.get("API_VERSION"),
        }]},
        story_id=story_id,
        frame_number=int(frame_number),
        max_consecutive_auto_reply=0,
    )
    
    result = user_proxy.initiate_chat(
        image_creator,
        message="Hi",
    )
    img_url=result.chat_history[-1]['content'][-1]['image_url']['url']
    prompt=result.chat_history[-1]['content'][-1]['prompt']
    update_prompt_by_story_id_and_frame_number(story_id=story_id,frame_number=int(frame_number),prompt=prompt)
    save_image_from_url(story_id=story_id,frame_index=int(frame_number),image_url=img_url,is_final=True)
    voice_filename= "./output/"+story_id+"/"+frame_number+"/voice.mp3"
    text_to_speech(story_content,voice_filename)

create_pptx(story_id=story_id)
create_video(story_id=story_id)
