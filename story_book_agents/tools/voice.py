
import os
from typing import Annotated
import azure.cognitiveservices.speech as speechsdk



def text_to_speech(text: Annotated[str, "text to speech"], filename: Annotated[str, "filename to save"]) -> Annotated[bool, "result"]:
    """
    TTS function use azure service

    Args:
        text (Annotated[str,"text to speech"]): text to speech
        filename (Annotated[str,"filename to save"]): filename to save

    Returns:
        Annotated[bool,"result"]: result

    """
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")
    speech_voice_name = os.environ.get(
        "AZURE_SPEECH_VOICE_NAME", "zh-CN-XiaoxiaoMultilingualNeural")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,
                                           region=speech_region)
    speech_config.speech_synthesis_voice_name = speech_voice_name

    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{text}]")
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

    return False
