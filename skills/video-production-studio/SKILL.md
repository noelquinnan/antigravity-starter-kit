---
name: video-production-studio
description: >-
  全能视频制作与剪辑总控工作流（统一路由中心）。当用户要求制作任意类型视频——包括漫剪卡点、
  MG动效/科普解说/数据可视化、口播字幕与静音精剪、长片自动拆镜、AI配音旁白、剪映草稿或高画质压制时，
  优先加载本技能按场景联动全套工具链。
---

# 全能视频制作与剪辑总控（video-production-studio）

本技能是视频任务的**统一总控路由**，负责按任务类型把本机音视频智能脚本、Remotion 动效引擎、剪映草稿和 FFmpeg 后期串成一条完整流水线，避免遗漏任何可用工具。

---

## 1. 场景路由总表（动手前先按场景认领工具）

| 视频类型 | 核心联动链 |
| :--- | :--- |
| **漫剪 / 混剪 / 教程复刻 / 剪映草稿** | 1. 整集素材先用 `scenedetect` 自动拆镜<br>2. BGM 先用 `beat_detect.py` 提取 BPM 与强鼓点时间戳<br>3. 严格执行 `video-edit-preview-workflow`（剪映草稿 + 1080p 预览 + 内置浏览器双屏对照） |
| **MG 动效 / 科普解说 / 片头片尾 / 竖屏信息流** | 1. 脚本定稿后用 `tts_gen.py` 生成配音 MP3 + 精准 `.srt` 字幕<br>2. 按 `remotion-best-practices`（配合 `remotion-create` / `remotion-markup` / `remotion-captions` / `remotion-render`）编写 React 动画并按帧渲染 1080p/4K MP4 |
| **口播精剪 / 访谈 / 网课切片 / 烧录字幕** | 1. 用 `asr_subtitle.py`（本地 GPU `faster-whisper`）生成高精度 `.srt`<br>2. 用 `ffmpeg` 裁剪静音气口、做响度归一化与字幕烧录 |
| **图片封面 / 精灵图 / 素材预处理** | 联动 `magick`（ImageMagick 7）与 `ffmpeg` 统一分辨率、裁黑边、转透明帧/GIF |

---

## 2. 本机标准化工具脚本（全部位于本技能 `scripts/` 目录）

脚本根路径：`~/.gemini/config/skills/video-production-studio\scripts\`

1. **自动踩点（BPM + 强鼓点时间戳 JSON）**：
   ```powershell
   python "~/.gemini/config/skills/video-production-studio\scripts\beat_detect.py" "<音频或视频>" --out beats.json
   ```
2. **免费配音 + 同步字幕（Edge TTS）**：
   ```powershell
   python "~/.gemini/config/skills/video-production-studio\scripts\tts_gen.py" --text-file script.txt --voice zh-CN-XiaoxiaoNeural --out-audio voice.mp3 --out-srt voice.srt
   ```
   常用中文声线：`zh-CN-XiaoxiaoNeural`（自然女声）、`zh-CN-YunxiNeural`（自然男声）、`zh-CN-YunjianNeural`（新闻/解说男声）、`zh-CN-XiaoyiNeural`（活泼女声）。
3. **本地 GPU 语音识别出字幕（faster-whisper）**：
   ```powershell
   python "~/.gemini/config/skills/video-production-studio\scripts\asr_subtitle.py" "<视频或音频>" --model small --lang zh --out output.srt
   ```
4. **整片自动拆镜（PySceneDetect CLI）**：
   ```powershell
   scenedetect -i "<原片.mp4>" detect-adaptive list-scenes -f scenes.csv
   ```
   （需要直接切出独立片段时追加 `split-video -o scenes_dir`。）

---

## 3. 投稿级后期与压制标准（B 站 / 抖音通用）

- **音频响度归一化（防声音忽大忽小）**：
  ```powershell
  ffmpeg -i in.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:v copy -c:a aac -b:a 320k out_norm.mp4
  ```
- **高画质成片压制（兼容全平台）**：
  - 追求极致画质：`-c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -c:a aac -b:a 320k -movflags +faststart`
  - 批量高速预览（N 卡硬件加速）：`-c:v h264_nvenc -cq 19 -preset p6 -pix_fmt yuv420p`

---

## 4. 统一出厂验收闭环（交付铁律）

无论走 Remotion、FFmpeg 还是剪映草稿路线，交付成片前必须完成：
1. **画质与对齐抽帧核验**：抽取起手、高潮/动效峰值、收尾至少 3 帧检查画面清晰度、文字安全区与音画同步，无黑屏/遮挡/发灰。
2. **不覆盖原素材**：所有渲染和切片一律写入新文件。
3. **浏览器直接预览**：启动本地 HTTP 服务，在内置浏览器打开预览页或对照页供用户直接审片，不甩冷冰冰的文件路径。
