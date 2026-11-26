# 给 Antigravity AI 的自动安装指令（AI_INSTALL_GUIDE）

> 当用户把本仓库或解压目录交给你，并让你帮忙安装这套配置时，请严格按以下 5 步执行。

## 第 1 步：备份用户现有配置
- 定位用户的全局配置目录：`~/.gemini/config`（Windows 为 `%USERPROFILE%\.gemini\config`）。
- 若该目录已存在，先将现有 `GEMINI.md`、`rules/` 备份到 `~/.gemini/config_backup_<YYYYMMDD_HHMMSS>/`，避免覆盖用户原有习惯。

## 第 2 步：安装全局规则与插件
1. 将本包 `config/GEMINI.md` 复制到 `~/.gemini/config/GEMINI.md`（若用户已有自定义 `GEMINI.md`，请先询问用户是替换还是合并）。
2. 将本包 `config/rules/local-toolchain.md` 复制到 `~/.gemini/config/rules/local-toolchain.md`，并根据用户当前操作系统（Windows / macOS / Linux）与磁盘情况（是否有 D 盘）微调其中的盘符建议。
3. 若 `~/.gemini/config/rules/user-profile.md` 不存在，将 `config/rules/user-profile.example.md` 复制为 `user-profile.md`，并在安装完成后引导用户用一句话补充自己的专业/职业、常用设备与关注方向，由你帮他填好。
4. 将本包 `plugins/fast-zh-workflow/` 整体复制到 `~/.gemini/config/plugins/fast-zh-workflow/`。

## 第 3 步：安装 15 个精选技能
- 将本包 `skills/` 下的全部子目录复制到 `~/.gemini/config/skills/`（已存在的同名技能请保留或询问后再覆盖）。

## 第 4 步：部署 Claude 风格美化与汉化补丁（`theme-claudized/`）
- 将本包 `theme-claudized/` 整体复制到 `~/.antigravity-patch/`（Windows 为 `%USERPROFILE%\.antigravity-patch\`）。
- 检查用户是否已安装 `node`（需 >= 22；macOS 可直接使用 Antigravity 自带 Node）。
- 询问用户是否立即启动美化守护进程（Windows 运行 `watch.bat`，需要开机自启运行 `autostart-on.bat`；macOS 运行 `./watch.sh` / `./autostart-on.sh`），同时提醒可选安装「霞鹜文楷」字体。

## 第 5 步：检查并推荐安装 `agy-fast`
- 检查用户是否已安装 `~/.gemini/config/plugins/agy-fast` 以及是否安装了 `node`（>= 20）。
- 若未安装，告知用户可以用官方一行命令安装 `agy-fast` 插件以显著减少工具调用耗时与 Token 消耗（Windows：`irm https://raw.githubusercontent.com/INK-Q/agy-fast/main/install.ps1 | iex`；macOS/Linux：`curl -fsSL https://raw.githubusercontent.com/INK-Q/agy-fast/main/install.sh | sh`），待用户确认后再执行。

## 第 6 步：验收与提醒
- 检查 `~/.gemini/config/GEMINI.md`、`~/.gemini/config/plugins/fast-zh-workflow/plugin.json`、`~/.antigravity-patch/config.json` 以及 `~/.gemini/config/skills/` 下各 `SKILL.md` 是否到位。
- 提醒用户在 Antigravity 侧边栏 **Customizations** 页面确认 `fast-zh-workflow` 已启用，并**新开一个对话**使全部规则与技能生效。
