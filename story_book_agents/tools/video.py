import os
import random
from typing import Annotated
from moviepy.editor import ImageClip,AudioFileClip,concatenate_videoclips,CompositeVideoClip


def apply_effect(clip, effect, duration, **kwargs):
    original_size = clip.size
    w, h = original_size
    move_distance = kwargs.get('move_distance', 0.15)
    scale_factor = 1 + move_distance

    if effect == "zoom_in":
        return clip.resize(lambda t: 1 + 0.15*t/duration)
    elif effect == "zoom_out":
        return clip.resize(lambda t: 1 + 0.15*(1-t/duration))
    elif effect.startswith("move"):
        enlarged_clip = clip.resize(scale_factor)
        w_new, h_new = enlarged_clip.size

        if effect == "move_left":
            start_pos = (0, 'center')
            end_pos = (-(w_new - w), 'center')
        elif effect == "move_right":
            start_pos = (-(w_new - w), 'center')
            end_pos = (0, 'center')
        elif effect == "move_up":
            start_pos = ('center', 0)
            end_pos = ('center', -(h_new - h))
        elif effect == "move_down":
            start_pos = ('center', -(h_new - h))
            end_pos = ('center', 0)
        else:
            raise ValueError(f"Unknown move effect: {effect}")

        def move_position(t):
            progress = t / duration
            x1, y1 = start_pos
            x2, y2 = end_pos
            if x1 == 'center':
                x = 'center'
            else:
                x = x1 + (x2 - x1) * progress
            if y1 == 'center':
                y = 'center'
            else:
                y = y1 + (y2 - y1) * progress
            return (x, y)

        moving_clip = enlarged_clip.set_position(move_position)
        return CompositeVideoClip([moving_clip], size=original_size).set_duration(duration)
    elif effect == "none":
        return clip
    else:
        raise ValueError(f"Unknown effect: {effect}")


effects_config = [
    {"effect": "none"},
    {"effect": "move_left"},
    {"effect": "random"},
    {"effect": "zoom_in"},
    # Add more configurations for additional shots...
]

def create_video(story_id: Annotated[str,'story id'] ):
    """
    Create video by story id

    Args:
    story_id (Annotated[str,'story id']): story id

    """
    output_directory= "./output/"+story_id
    # 获取所有子目录
    subdirs = sorted([d for d in os.listdir(output_directory) if os.path.isdir(os.path.join(output_directory, d))], key=int)
    available_effects = ["zoom_in", "zoom_out", "move_left", "move_right", "move_up", "move_down",  "none"]

    clips = []
    original_size = None
    for subdir in subdirs:
        subdir_path = os.path.join(output_directory, subdir)
        image_path = os.path.join(subdir_path, 'image.jpg')
        audio_path = os.path.join(subdir_path, 'voice.mp3')
        
        # 创建图像clip
        image_clip = ImageClip(image_path)
        if original_size is None:
            original_size = image_clip.size

        # 获取音频时长
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration
        
        chosen_effect =random.choice(available_effects)
        print(f"Applying effect: {chosen_effect} to clip in {subdir}")

        image_clip = apply_effect(image_clip, chosen_effect, audio_duration)
        # 设置图像clip时长（比音频长0.5秒）
        image_clip = image_clip.set_duration(audio_duration + 0.5)
        if image_clip.size != original_size:
            image_clip = image_clip.resize(original_size)        
        # 添加音频
        video_clip = image_clip.set_audio(audio)
        
        # 添加过渡效果（淡入淡出）
        video_clip = video_clip.crossfadein(0.5).crossfadeout(0.5)
        
        clips.append(video_clip)
    
    # 合并所有clips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # 输出最终视频
    final_clip.write_videofile(os.path.join(output_directory,'output.mp4') , fps=24)
    
    # 输出最终音频
    final_clip.audio.write_audiofile(os.path.join(output_directory,'output.mp3'),fps=44100)

