[中文版](README.zh-cn.md)

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
- Azure 账号，并开通 Speech 服务资源。

## 如何使用
- 创建 python 虚拟环境（我这里是在 Python 3.11 上进行的测试），并安装依赖包
```
pip install -r requirements.txt
```
- 创建.env 文件，并复制 .env.example 中的内容过来，修改为您的对应的设置值。
- 运行:创作故事
```
python app.py
```
- 生成图片/视频/PPTX：首先修改 generate.py 中的 story_id 为你想生成的故事 ID（从 app.py 的输出中得到）。然后运行：
```
python generate.py
```

## 路线图
- [ ]完善内容生成部分的逻辑
- [ ]在故事内容创作和内容生成的过程中增加“人在回路”的逻辑
- [ ]背景音乐

## 常见问题
- **支持其他语言么？**
  支持的，在内容创作的 Prompt 部分已经有指令要求遵循用户的要求或者用户输入时采用的语言。
- **语音的多语言呢？**
  Azure的 TTS 支持上百种语言，您只需要将.env中的AZURE_SPEECH_VOICE_NAME指定为您所需要的语言的发音人即可（有的发音人本身就支持几十种不同国家的语言）
- **视觉质量看起来不高**
  两方面的因素：
  - 一是目前我所展示的测试内容里采用的 Flux 的 Schnell 模型，为的是速度快和成本低。采用 dev 或者 pro 必然图片的视觉质量会有提高，目前代码中还未支持这两种不同的模型，未来会加入。
  - 二是现有的图片评审逻辑还不够，还有改善的余地。
  
## 其他
[部分生成的内容演示参见这里](DEMO-Results.md)