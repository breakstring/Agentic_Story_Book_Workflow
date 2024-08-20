
import os
import dotenv
from autogen import UserProxyAgent
from story_book_agents.tools.pptx import create_pptx
from story_book_agents.tools.utils import get_storyboard_by_story_id, update_prompt_by_story_id_and_frame_number, get_last_story_id
from story_book_agents.tools.image import save_image_from_url
from story_book_agents.tools.video import create_video
from story_book_agents.tools.voice import text_to_speech
from story_book_agents.image_creator_agent import ImageCreatorAgent
dotenv.load_dotenv(override=True)

# get the last story id. if you have a specific story id, you can replace it with your own story id.
story_id = get_last_story_id()

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



def generate_image_by_frame_number(frame_number):
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
            message=f"This is frame {frame_number}",
        )
    img_url = result.chat_history[-1]['content'][-1]['image_url']['url']
    prompt = result.chat_history[-1]['content'][-1]['prompt']
    update_prompt_by_story_id_and_frame_number(
            story_id=story_id, frame_number=int(frame_number), prompt=prompt)
    save_image_from_url(story_id=story_id, frame_index=int(
            frame_number), image_url=img_url, is_final=True)

# generate images
def generate_images():
    for frame in storyboard:
        frame_number = frame["Index"]
        generate_image_by_frame_number(frame_number)

# generate audio
def generate_voice():
    for frame in storyboard:
        frame_number = frame["Index"]
        story_content = frame["StoryContent"]

        voice_filename = "./output/" + story_id + "/" + frame_number + "/voice.mp3"
        text_to_speech(story_content, voice_filename)


# entry point
if __name__ == '__main__':
    # generate image by frame number, you can use this function to re-generate image by frame number
    #generate_image_by_frame_number(2)
    
    # generate images, if you have images, you can comment this line
    generate_images()
    
    # generate voice, if you have voice, you can comment this line
    generate_voice()
    # just a basic blank pptx template with image and audio, you can comment this line if you donot need the pptx.
    create_pptx(story_id=story_id)
    # create video
    create_video(story_id=story_id)
    
