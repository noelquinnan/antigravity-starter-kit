<#
.SYNOPSIS
  Antigravity Starter Kit 一键安装脚本（Windows PowerShell）
.DESCRIPTION
  自动备份 ~/.gemini/config 现有规则，安装脱敏后的全局规则、fast-zh-workflow 插件与 15 个精选技能。
#>

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigDir = Join-Path $env:USERPROFILE ".gemini\config"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupDir = Join-Path $env:USERPROFILE ".gemini\config_backup_$Timestamp"

Write-Host "==> 目标配置目录: $ConfigDir" -ForegroundColor Cyan

# 1. 创建目标目录并备份现有关键配置
New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ConfigDir "rules") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ConfigDir "plugins") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ConfigDir "skills") | Out-Null

$NeedBackup = (Test-Path (Join-Path $ConfigDir "GEMINI.md")) -or (Test-Path (Join-Path $ConfigDir "rules\local-toolchain.md"))
if ($NeedBackup) {
    New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
    if (Test-Path (Join-Path $ConfigDir "GEMINI.md")) {
        Copy-Item (Join-Path $ConfigDir "GEMINI.md") (Join-Path $BackupDir "GEMINI.md") -Force
    }
    if (Test-Path (Join-Path $ConfigDir "rules")) {
        Copy-Item (Join-Path $ConfigDir "rules") (Join-Path $BackupDir "rules") -Recurse -Force
    }
    Write-Host "==> 已备份原有规则至: $BackupDir" -ForegroundColor Yellow
}

# 2. 安装核心规则
Copy-Item (Join-Path $RepoRoot "config\GEMINI.md") (Join-Path $ConfigDir "GEMINI.md") -Force
Copy-Item (Join-Path $RepoRoot "config\rules\local-toolchain.md") (Join-Path $ConfigDir "rules\local-toolchain.md") -Force

$UserProfileDest = Join-Path $ConfigDir "rules\user-profile.md"
if (-not (Test-Path $UserProfileDest)) {
    Copy-Item (Join-Path $RepoRoot "config\rules\user-profile.example.md") $UserProfileDest -Force
    Write-Host "==> 已生成个人档案模板: $UserProfileDest (请按需填入你的专业/方向)" -ForegroundColor Green
} else {
    Write-Host "==> 检测到已有 user-profile.md，已保留不覆盖" -ForegroundColor DarkGray
}

# 3. 安装 fast-zh-workflow 插件
$PluginSrc = Join-Path $RepoRoot "plugins\fast-zh-workflow"
$PluginDest = Join-Path $ConfigDir "plugins\fast-zh-workflow"
if (Test-Path $PluginDest) {
    Remove-Item $PluginDest -Recurse -Force
}
Copy-Item $PluginSrc $PluginDest -Recurse -Force

# 4. 安装精选技能
$SkillsSrc = Join-Path $RepoRoot "skills"
$SkillsDest = Join-Path $ConfigDir "skills"
$SkillDirs = Get-ChildItem -Path $SkillsSrc -Directory
foreach ($sd in $SkillDirs) {
    $target = Join-Path $SkillsDest $sd.Name
    if (Test-Path $target) {
        Remove-Item $target -Recurse -Force
    }
    Copy-Item $sd.FullName $target -Recurse -Force
}

# 5. 部署 Claude 风格美化与汉化补丁（Claudized-Antigravity + 精调 user.css）
$ThemeSrc = Join-Path $RepoRoot "theme-claudized"
$ThemeDest = Join-Path $env:USERPROFILE ".antigravity-patch"
if (Test-Path $ThemeSrc) {
    if (Test-Path $ThemeDest) {
        $ThemeBak = "$ThemeDest`_backup_$Timestamp"
        Copy-Item $ThemeDest $ThemeBak -Recurse -Force
        Write-Host "==> 已备份原有皮肤补丁至: $ThemeBak" -ForegroundColor Yellow
        Remove-Item $ThemeDest -Recurse -Force
    }
    Copy-Item $ThemeSrc $ThemeDest -Recurse -Force
}

Write-Host ""
Write-Host "安装完成！已部署：" -ForegroundColor Green
Write-Host "  - 全局核心规则: GEMINI.md + local-toolchain.md"
Write-Host "  - 效率插件: fast-zh-workflow"
Write-Host "  - 精选技能: $($SkillDirs.Count) 个"
Write-Host "  - Claude 风格美化与汉化补丁: $ThemeDest"
Write-Host ""
Write-Host "下一步建议：" -ForegroundColor Cyan
Write-Host "  1. 启用 Claude 风格美化与中文界面（需 Node.js >= 22）：进入 $ThemeDest 双击 watch.bat（开机自启点 autostart-on.bat）"
Write-Host "  2. (强烈推荐) 安装 agy-fast 加速插件: irm https://raw.githubusercontent.com/INK-Q/agy-fast/main/install.ps1 | iex"
Write-Host "  3. 编辑 $UserProfileDest 填入你的专业/课程或开发方向"
Write-Host "  4. 在 Antigravity 侧边栏 Customizations 中确认插件已开启，并新开一个对话即可生效"
