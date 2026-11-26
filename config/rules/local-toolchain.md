# 本机工具链与执行习惯（通用模板）

- **动手前说明**：调用工具前用一句话简短说明目的，不重复上文。
- **优先走本地 CLI / 接口，避免无谓探测与 GUI 点击**：
  - 搜索文本与文件：优先使用 `rg`（ripgrep）；Windows 若安装了 Everything CLI 可用 `es`。
  - 音视频与图片：`ffmpeg` / `ffprobe` / `yt-dlp`、`magick`（ImageMagick）、`scenedetect`；涉及视频制作/剪辑/动效/字幕/配音，优先加载总控技能 `video-production-studio`。
  - 文档与数据：`pandoc`、`duckdb`、`sqlite3`、`jq`。
  - 开发与版本控制：`python`、`node`、`pnpm`、`git`、`gh`。
- **文件落盘与交付定位**：
  - 新建项目优先放在非系统盘的工作区目录（如存在 `D:\` 盘，优先使用 `D:\AI_Projects\<项目名>` 与 `D:\Temp`，减少占用 `C:\` 盘空间）。
  - 交付图片、动图、视频、文档或打包产物等最终成品时，除可点击链接外，在回复末尾附上一行纯文本目录路径，方便用户快速复制或在文件管理器中打开。
