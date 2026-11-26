# Antigravity 增强配置包（Starter Kit）

一套面向 **Google Antigravity** 的开箱即用提效配置：包含全局行为规则、中文播报与极速检索插件，以及 15 个精选高频技能（文档/PPT/PDF、交互小工具、资料调研、前端设计、系统调试、视频与 Remotion 制作工作流）。

> 本仓库已完全脱敏，不含任何个人隐私、账号凭证或特定本机路径。

## 包含内容

| 模块 | 目录 | 作用 |
| :--- | :--- | :--- |
| **全局核心规则** | `config/GEMINI.md` | 强制简体中文思考与回复、KISS 极简原则、先出方案再动手、验证后再交付、精炼去废话排版 |
| **通用工具链规范** | `config/rules/local-toolchain.md` | 优先走本地 CLI 而非盲目探测、文件规范落盘、交付附带明文路径 |
| **个人档案模板** | `config/rules/user-profile.example.md` | 填写你的专业、课程或工作方向后，让 AI 永久记住你的背景 |
| **中文效率插件** | `plugins/fast-zh-workflow/` | 动手前简短播报进度、先精准文本搜索再按行段读取，拒绝哑巴模式和盲翻文件 |
| **Claude 风格美化与汉化补丁** | `theme-claudized/` | 基于 [Claudized-Antigravity](https://github.com/AlexByoung/Claudized-Antigravity) + 本地 3 轮 `user.css` 排版精调（Claude 陶土/经典明暗主题、完整简体中文界面、中文对话标题、浮动 Gemini 小窗） |
| **15 个精选技能** | `skills/` | 见下方技能清单 |

### 内置 15 个精选技能

- **效率与开发**：`micro-app-builder`（个人小工具极速开发）、`research-curator`（多源资料搜集与沉淀）、`frontend-design`（高质感前端视觉）、`systematic-debugging`（系统化排错）
- **办公与演示**：`docx`、`pdf`、`pptx`、`guizang-ppt-skill`（网页版横向翻页 PPT）
- **视频与动效**：`video-production-studio`、`video-edit-preview-workflow`、`remotion-best-practices` / `remotion-create` / `remotion-markup` / `remotion-captions` / `remotion-render`

---

## 两种安装方式（任选其一）

### 方式 1：让你的 Antigravity 全自动帮你装（最省心，推荐）

1. 克隆本仓库或解压 `.zip` 到任意文件夹。
2. 在 Antigravity 中打开该文件夹（或直接把文件夹路径发给它），发送下面这句话：

```text
请读取当前目录里的 AI_INSTALL_GUIDE.md，按里面的步骤把这套配置安装到我本机的 Antigravity 里，安装前先备份我原有配置，不要覆盖我已有的个人设置。
```

### 方式 2：Windows PowerShell 一键脚本安装

在仓库目录打开 PowerShell 运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

脚本会自动：
1. 备份你原有的 `~/.gemini/config/`（保存到 `~/.gemini/config_backup_<时间戳>`）；
2. 安装 `GEMINI.md`、`local-toolchain.md`、`fast-zh-workflow` 插件和 15 个技能；
3. 如果你尚未创建 `user-profile.md`，会自动复制一份模板供你填写（若已有则保留不覆盖）；
4. 将 `theme-claudized/` 部署到 `%USERPROFILE%\.antigravity-patch\`（含预配置 `config.json` 与排版精调 `user.css`）。

> **启用 Claude 风格美化与中文界面（需 Node.js >= 22）**：
> 进入 `%USERPROFILE%\.antigravity-patch\`，双击 `watch.bat` 即可立即生效；需要开机自启再双击 `autostart-on.bat`；随时想还原可双击 `remove.bat`。可选安装 [霞鹜文楷 LXGW WenKai](https://github.com/lxgw/LxgwWenKai) 字体获得最佳中文观感。

---

## 强烈推荐补充安装的外部插件（需单独安装）

为了保持轻量与账号安全，以下插件未打包进本仓库，建议装完本包后补装：

1. **`agy-fast`（极速批处理检索、大纲、原子多文件编辑，省 Token 且显著提速）**
   - 需先安装 Node.js >= 20，在 PowerShell 运行官方一行命令：
     ```powershell
     irm https://raw.githubusercontent.com/INK-Q/agy-fast/main/install.ps1 | iex
     ```
   - macOS / Linux：
     ```bash
     curl -fsSL https://raw.githubusercontent.com/INK-Q/agy-fast/main/install.sh | sh
     ```
2. **Antigravity 官方插件商店按需安装**：
   - `chrome-devtools-plugin`（网页调试、性能与无障碍检测）
   - `gdocs` / `gdrive` / `gmail` / `gsheets`（需在插件面板登录你自己的 Google 账号）

## 生效方法

安装完成后，在 Antigravity 侧边栏打开 **Customizations → Installed** 确认 `fast-zh-workflow`（及 `agy-fast`）处于启用状态，然后**新开一个对话**即可生效。
