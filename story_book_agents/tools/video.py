import os
from typing import Annotated
from moviepy.editor import ImageClip,AudioFileClip,concatenate_videoclips


def create_video(story_id: Annotated[str,'story id'] ):
    """
    Create video by story id

    Args:
    story_id (Annotated[str,'story id']): story id

    """
    output_directory= "./output/"+story_id
    # 获取所有子目录
    subdirs = sorted([d for d in os.listdir(output_directory) if os.path.isdir(os.path.join(output_directory, d))], key=int)
    
    clips = []
    for subdir in subdirs:
        subdir_path = os.path.join(output_directory, subdir)
        image_path = os.path.join(subdir_path, 'image.png')
        audio_path = os.path.join(subdir_path, 'voice.mp3')
        
        # 创建图像clip
        image_clip = ImageClip(image_path)
        
        # 获取音频时长
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration
        
        # 设置图像clip时长（比音频长0.5秒）
        image_clip = image_clip.set_duration(audio_duration + 0.5)
        
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

