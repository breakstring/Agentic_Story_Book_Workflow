"""
utils tools for story_book_agents
"""

import datetime
from typing import Annotated
import uuid
import xml.etree.ElementTree as ET

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


class MyJSONStorage(JSONStorage):
    """
    Custom JSON storage class that sets ensure_ascii=False and indent=4.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kwargs['ensure_ascii'] = False
        self.kwargs['indent'] = 4


def save_story_content(story_title: Annotated[str, "Story Title"], story_content: Annotated[str, "Story Content"]) -> Annotated[str, " 保存的故事的ID"]:
    """
    Save story content

    参数：
    story_title (Annotated[str, "Story Title"]): Story title
    story_draft (Annotated[str, "Story Content"]): Story content

    返回值：
    Annotated[str, "Story ID"]: Story ID

    """
    story_id = str(uuid.uuid4())
    db = TinyDB('output/stories.json',
                storage=CachingMiddleware(MyJSONStorage))

    # story_table = db.table('stories')
    story = {'story_id': story_id,
             'story_title': story_title,
             'story_content': story_content,
             'created_at': datetime.datetime.now().timestamp()}
    db.insert(story)
    # story_table.insert(story)
    db.close()
    return story_id


def load_story_content_by_id(story_id: Annotated[str, "Story ID"]) -> Annotated[str, "Story Content"]:
    """
    Load story content by ID

    参数：
    story_id (Annotated[str, "Story ID"])：Story ID

    返回值：
    Annotated[str, "Story Content"]: Story content

    """
    db = TinyDB('output/stories.json',
                storage=CachingMiddleware(MyJSONStorage))
    stories = Query()
    story = db.search(stories.story_id == story_id)[0]
    db.close()
    return story['story_content']


def save_storyboard_by_story_id(story_id: Annotated[str, "Story ID"], storyboard_content: Annotated[str, "Storyboard Content"]) -> Annotated[str, "Result"]:
    """
    Save storyboard by story ID

    参数：
    story_id (Annotated[str, "Story ID"]): Story ID
    storyboard_content (Annotated[str, "Storyboard Content"]): Storyboard content

    返回值：
    Annotated[str, "Result"]: Result

    """
    root = ET.fromstring(storyboard_content)
    storyboard_items = [{child.tag: child.text for child in item}
                        for item in root.findall('StoryboardItem')]

    db = TinyDB('output/storyboards.json',
                storage=CachingMiddleware(MyJSONStorage))
    storyboard = {'story_id': story_id,
                  'storyboard_content': storyboard_items,
                  'created_at': datetime.datetime.now().timestamp()}
    db.insert(storyboard)
    db.close()
    return "STORYBOARD_SAVED"

def save_prompts_by_story_id(story_id:Annotated[str, "Story ID"], prompts_content:Annotated[str, "Prompts Content"])->Annotated[str, "Result"]:
    """
    Save prompts by story ID

    参数：
    story_id (Annotated[str, "Story ID"]): Story ID
    prompts_content (Annotated[str, "Prompts Content"]): Prompts content

    返回值：
    Annotated[str, "Result"]: Result

    """
    root = ET.fromstring(prompts_content)
    prompts_items = [{child.tag: child.text for child in item}
                        for item in root.findall('StoryboardItem')]

    db = TinyDB('output/prompts.json',
                storage=CachingMiddleware(MyJSONStorage))
    prompts = {'story_id': story_id,
                  'prompts_content': prompts_items,
                  'created_at': datetime.datetime.now().timestamp()}
    db.insert(prompts)
    db.close()
    return "PROMPTS_SAVED"
