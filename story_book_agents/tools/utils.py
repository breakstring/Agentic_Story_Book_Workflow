''' utils tools for story_book_agents '''

import datetime
from typing import Annotated
import uuid
from tinydb import TinyDB
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
    保存故事内容

    参数：
    story_title (Annotated[str, "Story Title"]): 故事标题
    story_draft (Annotated[str, "Story Content"]): 故事内容

    返回值：
    Annotated[str, "Story ID"]: 故事的唯一标识符

    """
    story_id = str(uuid.uuid4())
    db = TinyDB('output/stories.json',
                storage=CachingMiddleware(MyJSONStorage))

    story_table = db.table('stories')
    story = {'story_id': story_id,
             'story_title': story_title,
             'story_content': story_content,
             'created_at': datetime.datetime.now().timestamp()}
    story_table.insert(story)
    db.close()
    return story_id
