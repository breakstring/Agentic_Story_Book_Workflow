[中文版](README.zh-cn.md)

## Agentic Story Book Workflow
A multi-agent workflow framework for creating children's picture books based on [AutoGen](https://microsoft.github.io/autogen/).


https://github.com/user-attachments/assets/323d055a-27d9-487f-b8c4-2fad2df649cc

## Agentic workflow
![MultiAgent](./images/MultiAgents.jpg)
The code involves various multi-agent collaboration methods based on AutoGen. For example:
- Initially, the User_Proxy represents the user and communicates with the Receptionist to gather user requirements.
- In the subsequent two stages, the GroupChat mechanism is used, with each GroupChat having a GroupChat Manager to coordinate the speakers in the current GroupChat.
- In the two GroupChats, the content creation roles (e.g., Story Editor, Storyboard Editor, Prompt Editor) are accompanied by an Agent responsible for reviewing the content. If the review is not approved, the GroupManager sends it back to the content creation Editor for revision.
- The final stage of generating images/videos/PPTs is currently placed in separate code (generate.py) for ease of use and potential future adjustments to the GroupChat organization. This part is temporarily handled by an Image Creator Agent, which is an independent Agent but contains two Sub-Agents internally: an Image Generation Agent responsible for AI-based image generation and another for reviewing the generated images.

## System Requirements
- **LLM**: It is recommended to use ChatGPT-4o. The current code is tested based on the ChatGPT-4o service in Azure OpenAI. In theory, it should also support OpenAI's native services with minor configuration adjustments. Although AutoGen supports multiple LLMs, practical tests with Claude 3.5 sonnet showed that it could not strictly follow the instructions in the Prompt 100% of the time, so other LLMs are not recommended.
- **Text2Image**: Supports DALL-E 3 and Flux Schnell from Replicate. Considering cost and speed, I ultimately chose the Flux Schnell API endpoint from Replicate because:
  - Using DALL-E 3 in HD mode costs $12/100 images, meaning $0.12 per image, and each image takes more than ten seconds to generate.
  - Using the Flux Schnell API service costs only $0.003 per image, with a drawing time of 1-2 seconds. From a cost and scheduling perspective, Flux Schnell seems more suitable. Even if you find the quality of the Schnell version low, using the Flux Dev version API costs only $0.03 per image (the pro version on Replicate costs $0.055, but it seems to run on CPU and is very slow, so I didn't try it). You can adjust according to your needs.
- Azure account with Speech service resources enabled.

## How to use
- Create a Python virtual environment (tested on Python 3.11) and install dependencies:
```
pip install -r requirements.txt
```
- Create a .env file, copy the contents from .env.example, and modify it with your settings. Create a story
```
python app.py
```
- Generate images/videos/PPTX: First, modify the story_id in generate.py to the story ID you want to generate (obtained from the output of app.py). Then run:
```
python generate.py
```

## Roadmap
- [ ] Improve the logic of content generation
- [ ] Add "human-in-the-loop" logic during story content creation and generation
- [ ] Background music


## FAQ
- **Does it support other languages?**
  Yes, the content creation Prompt already includes instructions to follow the user's requirements or the language used by the user.
- **What about multi-language speech?**
  Azure's TTS supports hundreds of languages. You only need to specify the desired language's voice name in AZURE_SPEECH_VOICE_NAME in the .env file (some voices support dozens of different languages).
- **The visual quality seems low**
  Two factors:
  - The test content currently displayed uses the Flux Schnell model for speed and low cost. Using the dev or pro versions will improve the visual quality. The current code does not yet support these models, but it will be added in the future.
  - The existing image review logic is not sufficient and can be improved.
  
## Others
[See some generated content demos here](DEMO-Results.md)