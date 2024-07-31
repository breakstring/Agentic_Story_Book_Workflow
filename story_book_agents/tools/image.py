'''
image related tools
'''
import os
import uuid
from typing import Annotated, Union
from io import BytesIO

from openai import OpenAI, AzureOpenAI

import requests
from PIL import Image
from .utils import get_prompt_by_story_id_and_frame_number, get_prompts_by_story_id


def dalle_client_factory() -> Union[OpenAI, AzureOpenAI]:
    """
    Dalle client factory
    """
    if os.environ.get("IMAGE_GENERATION_TYPE") == "azure":  # Azure DallE
        return AzureOpenAI(api_key=os.environ.get("DALLE_API_KEY"),
                           azure_deployment=os.environ.get("DALLE_MODEL"),
                           api_version=os.environ.get("DALLE_API_VERSION"),
                           azure_endpoint=os.environ.get("DALLE_BASE_URL"))
    else:
        return OpenAI(api_key=os.environ.get("DALLE_API_KEY"))


def save_image_from_url(story_id: Annotated[str, "Story ID"], frame_index: Annotated[int, "Frame index"], image_url: Annotated[str, "Image URL"]) -> Annotated[str, "Image ID"]:
    """
    Save image from URL

    Args:
        story_id (Annotated[str, "Story ID"]): Story ID
        frame_index (Annotated[int, "Frame index"]): Frame index
        image_url (Annotated[str, "Image URL"]): Image URL

    Returns:
        Annotated[str, "Image ID"]: Image ID
    """

    response = requests.get(image_url, timeout=60)
    image = Image.open(BytesIO(response.content))
    image_id = str(uuid.uuid4())
    output_dir = f"output/{story_id}/{frame_index}"
    os.makedirs(output_dir, exist_ok=True)
    image.save(f"{output_dir}/{image_id}.png")
    return image_id


def generate_image_by_prompt(prompt_content: Annotated[str, "Prompt Content"]) -> Annotated[tuple[str, str], "Image URL & revised prompt"]:
    """
    Generate image by prompt

    Args:
        prompt_content (Annotated[str, "Prompt Content"]): Prompt content

    Returns:
        Annotated[tuple[str,str], "Image URL & revised prompt"]
    """
    # switch to different image generation service base the IMAGE_GENERATION_TYPE enviroment
    if os.environ.get("IMAGE_GENERATION_TYPE") == "azure" or os.environ.get("IMAGE_GENERATION_TYPE") == "openai":

        max_retries = os.environ.get("IMAGE_GENERATION_RETRIES", 3)
        for attempt in range(max_retries):
            try:
                dalle_client = dalle_client_factory()
                dalle_result = dalle_client.images.generate(prompt=prompt_content,
                                                            n=1,
                                                            quality=os.environ.get("DALLE_IMAGE_QUALITY"),
                                                            size=os.environ.get("IMAGE_SIZE"),
                                                            style=os.environ.get("DALLE_IMAGE_STYLE"),
                                                            response_format="url",
                                                            timeout=60)

                if dalle_result.data is not None:
                    image_url = dalle_result.data[0].url
                    revised_prompt = dalle_result.data[0].revised_prompt
                    return image_url, revised_prompt
                else:
                    print(f"Attempt {attempt + 1} failed: No data in response")
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")

        raise RuntimeError(f"Failed to generate image after {max_retries} attempts")

    else:
        raise NotImplementedError(
            f"IMAGE_GENERATION_TYPE:{os.environ.get('IMAGE_GENERATION_TYPE')} not implemented")


def generate_image_by_id(story_id: Annotated[str, "Story ID"], frame_index: Annotated[int, "Frame index"]) -> Annotated[str, "Image ID"]:
    """
    Generate image by story ID and frame ID

    Args:
        story_id (Annotated[str, "Story ID"]): Story ID
        frame_index (Annotated[int, "Frame index"]): Frame index

    Returns:
        Annotated[str, "Image ID"]: Image ID
    """
    # get default prompt by story id and frame id
    prompt_content = get_prompt_by_story_id_and_frame_number(
        story_id, frame_index)
    # generate image by prompts
    img_url, revised_prompt = generate_image_by_prompt(prompt_content)
    print(revised_prompt)
    # save image to local
    img_id = save_image_from_url(story_id, frame_index, img_url)
    # save image id & revised prompt to local

    return img_id


def generate_image_by_storyid(story_id: Annotated[str, "Story ID"]):
    """
    Generate image by story ID

    Args:
        story_id (Annotated [str, "Story ID"]): Story ID

    Returns:
    """
    print(f"Generating images for story id: {story_id}")
    prompts = get_prompts_by_story_id(story_id)
    for item in prompts:
        index = item['Index']
        prompt = item['Prompt']
        print(f"Generating image for frame index: {index}")
        img_url, revised_prompt = generate_image_by_prompt(prompt)
        img_id = save_image_from_url(story_id, index, img_url)
        print(f"Image ID: {img_id}")
        print(f"Revised Prompt: {revised_prompt}")
