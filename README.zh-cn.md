[English](README.md)

## Agentic Story Book Workflow
基于 [AutoGen](https://microsoft.github.io/autogen/) 的一个儿童绘本制作多智能体工作流框架。

https://github.com/user-attachments/assets/323d055a-27d9-487f-b8c4-2fad2df649cc

## Agentic workflow
![MultiAgent](./images/MultiAgents.jpg)
在代码中涉及到多种基于 AutoGen 的不同的多智能体协作方式。例如：
- 在一开始，由 User_Proxy 代表用户和 Receptionist 来进行交流，从而采集用户的需求。
- 在后继的两个环节中，均采用了 GroupChat 的机制，每个 GroupChat 中又分别设置了一个 GroupChat Manager 用来协调当前的 GroupChat 中的发言人角色。
- 在两个 GroupChat 中，内容的创作角色（例如 Story Editor,Storboard Editor, Prompt Editor）均伴随着有一个进行该环节的评审的Agent。当他们的评审没有通过的话，由 GroupManger 发回内容创作 Editor 进行重新修改。
- 最后的生成图片/视频/PPT 的环节，目前我将其放到了独立的代码中(generate.py)，一是便于我目前的使用，二是后继对于 GroupChat 的组织可能还会有所调整。所以这部分暂时由一个 Image Creator Agent 来负责，和前面所不同的是这是一个独立的 Agent，但是它自己内部又包含了两个 Sub-Agents，一个 Image Generation Agent 负责进行文生图的 AI 的调用。另外一个负责对于生成的图片的审查。

## 系统需求
- **LLM**: 建议使用 ChatGPT-4o,目前代码基于 Azure OpenAI 服务中的 ChatGPT-4o 进行测试，理论上对于 OpenAI 的原生服务也应该可以支持，最多需要对于 Config 做微调。尽管 AutoGen 支持多种 LLM，但是经过实际测试使用 Claude 3.5 sonnet 时也无法100%严格的遵循 Prompt 中的指令，所以不建议使用其他 LLM。
- **Text2Image**: 支持 DALL-E 3 以及 Replicate 中的 Flux schnell。但是从成本和速度上考虑的话我最终选用了 Replicate 中的 Flux Schnell API 端点。因为
  - 在使用 Landscpae 或者 Portrait 模式的图片，HD 模式下DALL-E 3 的价格是 12$/100 张图，意味着每张图 0.12$，而且每张图要十多秒以上才能绘制完毕并得到结果。
  - 但是采用 Flux Schnell 的 API 服务每张图的成本只有 0.003$，绘图时间一般在 1 ～2 秒。从成本和时间调度来说 Flux Schnell 似乎更加合适，哪怕你觉得 Schnell 版本的质量不高，要使用 Flux Dev 版本的 API 成本也只有 0.03$而已（Replicate 上的 pro 版本成本为 0.055$，但是由于似乎它在 CPU 上，绘图速度很慢我就没有尝试），您也可以根据自己的需求来调整。
- **Azure 账号**，并开通 Speech 服务资源。

## 如何使用
- 创建 python 虚拟环境（我这里是在 Python 3.11 上进行的测试），并安装依赖包
```
pip install -r requirements.txt
```
- 创建.env 文件，并复制 .env.example 中的内容过来，修改为您的对应的设置值。执行下面的脚本来创作故事：
```
python app.py
```
- 生成图片/视频/PPTX：首先修改 generate.py 中的 story_id 为你想生成的故事 ID（从 app.py 的输出中得到）。然后运行：
```
python generate.py
```

## .env 环境变量
|变量名|描述 |默认值|
|:-----|:----|:-----:|
|AGENTOPS_API_KEY| [AgentOps](https://app.agentops.ai/) API Key| |
|MODEL|Azure 上的模型部署名或者 OpenAI 上的模型名 | |
|API_VERSION|API Version|'2024-06-01'|
|API_TYPE|'azure' 或者 'openai'|azure|
|API_KEY|API Key| |
|BASE_URL|API base url,  Azure 应该形如 'https://{region_name}.openai.azure.com/'||
|IMAGE_GENERATION_TYPE|'azure', 'openai' 或者 'replicate'||
|IMAGE_SHAPE|'landscape', 'portrait' 或者 'square'|landscape|
|DALLE_MODEL|Azure 上的模型部署名或者 OpenAI 上的模型名 | |
|DALLE_API_VERSION|API Version|'2024-06-01'|
|DALLE_API_KEY|API Key| |
|DALLE_BASE_URL|API base url, Azure 上应该形如 'https://{region_name}.openai.azure.com/'||
|DALLE_IMAGE_QUALITY|'hd' 或者 'standard'|'hd'|
|DALLE_IMAGE_STYLE|'vivid' 或者 'natural'|'vivid'|
|REPLICATE_API_TOKEN|[repilicate](https://replicate.com/) api key| |
|IMAGE_GENERATION_RETRIES|生成每张图片时的重试次数|3|
|IMAGE_CRITICISM_RETRIES|每张图片的最大审核次数|2|
|IMAGE_SAVE_FAILURED_IMAGES|是否保存生成后未采用的图片:True or False|False|
|AZURE_SPEECH_KEY|Azure 语音的 API Key||
|AZURE_SPEECH_REGION|Azure 服务语音部署区域||
|AZURE_SPEECH_VOICE_NAME|Azure 语音发音人|'zh-CN-XiaoxiaoMultilingualNeural'|


## 路线图
- [ ]增加更多 FLUX 模型版本和渠道
- [ ]完善内容生成部分的逻辑
- [ ]在故事内容创作和内容生成的过程中增加“人在回路”的逻辑
- [ ]背景音乐

## 常见问题
- **我看到你的 Demo 的故事内容是中文，它支持其他语言么？**
  支持的，在内容创作的 Prompt 部分已经有指令要求遵循用户的要求或者用户输入时采用的语言。
- **语音的多语言呢？**
  Azure的 TTS 支持上百种语言，您只需要将.env中的AZURE_SPEECH_VOICE_NAME指定为您所需要的语言的发音人即可（有的发音人本身就支持几十种不同国家的语言）
- **那为啥你的 Prompt 都用英文写的？**
  毋容置疑，英文的 Prompt 的效果要比中文好一点。一个很有用的小技巧，在 Anthropic 的 Portal 里有一个帮你生成提示词的工具，你可以在那边输入你初步想法然后他帮你生成提示词，你只需要做少量的修改就可以用到你的程序里面。
- **视觉质量看起来不高**
  这里有两方面的因素：
  - 一是目前我所展示的测试内容里采用的 Flux 的 Schnell 模型，为的是速度快和成本低。采用 dev 或者 pro 必然图片的视觉质量会有提高，目前代码中还未支持这两种不同的模型，未来会加入。
  - 二是现有的图片评审逻辑还不够，还有改善的余地。
  
## 其他
[部分生成的内容演示参见这里](DEMO-Results.md)