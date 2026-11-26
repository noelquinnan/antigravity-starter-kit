# fix-shortcut.ps1 - local tweak (not in git, 小克 2026-11-26).
# Any shortcut that starts Antigravity.exe directly skips the debug port, so
# the theme can't attach. This points every Antigravity shortcut (Start Menu,
# Desktop and its sub-folders, taskbar pins) to launch-antigravity.vbs, which
# starts the theme watcher + Antigravity with --remote-debugging-port=0.
# inject.js --watch runs this automatically when a shortcut gets reset.
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$vbs = Join-Path $dir 'launch-antigravity.vbs'
$exe = Join-Path $env:LOCALAPPDATA 'Programs\Antigravity\Antigravity.exe'
$roots = @(
  (Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'),
  [Environment]::GetFolderPath('Desktop'),
  (Join-Path $env:APPDATA 'Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar')
)
$sh = New-Object -ComObject WScript.Shell
foreach ($root in $roots) {
  if (-not (Test-Path $root)) { continue }
  Get-ChildItem $root -Recurse -Filter *.lnk -ErrorAction SilentlyContinue | ForEach-Object {
    $bytes = [IO.File]::ReadAllBytes($_.FullName)
    # Drop NUL bytes so both ANSI and UTF-16 strings in the .lnk become plain text.
    $text = [Text.Encoding]::GetEncoding(28591).GetString($bytes) -replace "`0", ''
    $pointsToApp = $text -match 'antigravity\\Antigravity\.exe'
    $alreadyOk = $text -match 'launch-antigravity\.vbs'
    if ($pointsToApp -and -not $alreadyOk) {
      # WScript.Shell can't save to non-ASCII paths (e.g. "1 AI工具"), so edit a
      # temp copy with a plain name, then copy it back.
      $tmp = Join-Path $env:TEMP ('ag-lnk-' + [guid]::NewGuid().ToString('N') + '.lnk')
      Copy-Item -LiteralPath $_.FullName -Destination $tmp -Force
      $s = $sh.CreateShortcut($tmp)
      $s.TargetPath = Join-Path $env:WINDIR 'System32\wscript.exe'
      $s.Arguments = '"' + $vbs + '"'
      $s.WorkingDirectory = $dir
      $s.IconLocation = "$exe,0"
      $s.Save()
      Copy-Item -LiteralPath $tmp -Destination $_.FullName -Force
      Remove-Item -LiteralPath $tmp -Force
      Write-Output "fixed: $($_.FullName)"
    }
  }
}
