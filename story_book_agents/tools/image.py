'''
image related tools
'''
import os
import uuid
import replicate
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


def save_image_from_url(story_id: Annotated[str, "Story ID"], frame_index: Annotated[int, "Frame index"], image_url: Annotated[str, "Image URL"], is_final:Annotated[bool,"Is final image"]=False) -> Annotated[str, "Image filename"]:
    """
    Save image from URL

    Args:
        story_id (Annotated[str, "Story ID"]): Story ID
        frame_index (Annotated[int, "Frame index"]): Frame index
        image_url (Annotated[str, "Image URL"]): Image URL
        is_final (Annotated[bool,"Is final image"]): Is final image

    Returns:
        Annotated[str, "Image filename"]: Image filename
    """

    response = requests.get(image_url, timeout=60)
    image = Image.open(BytesIO(response.content))
    output_dir = f"output/{story_id}/{frame_index}"
    os.makedirs(output_dir, exist_ok=True)
    image_name = ""
    if is_final:
        image_name = "image.jpg"
    else:
        image_id = str(uuid.uuid4())
        image_name = f"{image_id}.jpg"
    
    image.save(f"{output_dir}/{image_name}")
    return image_name


def generate_image_by_prompt(prompt_content: Annotated[str, "Prompt Content"]) -> Annotated[tuple[str, str], "Image URL & revised prompt"]:
    """
    Generate image by prompt

    Args:
        prompt_content (Annotated[str, "Prompt Content"]): Prompt content

    Returns:
        Annotated[tuple[str,str], "Image URL & revised prompt"]
    """
    max_retries = int(os.environ.get("IMAGE_GENERATION_RETRIES", 3))
    for attempt in range(max_retries):
        try:
            image_shape = os.environ.get("IMAGE_SHAPE", "landscape").lower()
            # switch to different image generation service base the IMAGE_GENERATION_TYPE enviroment
            if os.environ.get("IMAGE_GENERATION_TYPE") == "azure" or os.environ.get("IMAGE_GENERATION_TYPE") == "openai":
                dalle_client = dalle_client_factory()                
                # set image_size base on image_shape:landscape, portrait, square
                image_size = "1792x1024"
                if image_shape == "portrait":
                    image_size = "1024x1792"
                elif image_shape == "square":
                    image_size = "1024x1024"
                else:
                    image_size = "1792x1024"

                dalle_result = dalle_client.images.generate(prompt=prompt_content,
                                                            n=1,
                                                            quality=os.environ.get("DALLE_IMAGE_QUALITY"),
                                                            size=image_size,
                                                            style=os.environ.get("DALLE_IMAGE_STYLE"),
                                                            response_format="url",
                                                            timeout=60)

                if dalle_result.data is not None:
                    image_url = dalle_result.data[0].url
                    revised_prompt = dalle_result.data[0].revised_prompt
                    return image_url, revised_prompt
                else:
                    print(f"Attempt {attempt + 1} failed: No data in response")
            elif os.environ.get("IMAGE_GENERATION_TYPE") == "replicate":
                aspect_ratio="16:9"
                if image_shape == "portrait":
                    aspect_ratio = "9:16"
                elif image_shape == "square":
                    aspect_ratio = "1:1"
                else:
                    aspect_ratio = "16:9"
                replicate_input = {
                    "prompt": prompt_content,
                    "aspect_ratio":aspect_ratio,
                    "output_quality":90
                }
                replicate_output=replicate.run(
                    "black-forest-labs/flux-schnell",
                    input=replicate_input
                )
                return str(replicate_output),prompt_content
            
            else:
                raise NotImplementedError(
                    f"IMAGE_GENERATION_TYPE:{os.environ.get('IMAGE_GENERATION_TYPE')} not implemented")
        except Exception as e:  # pylint: disable=broad-except
            print(f"Attempt {attempt + 1} failed: {e}")

    raise RuntimeError(f"Failed to generate image after {max_retries} attempts")