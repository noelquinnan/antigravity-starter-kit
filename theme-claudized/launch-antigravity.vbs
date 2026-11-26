' Start the theme watcher (exits by itself if one is already running),
' then open Antigravity with the local debug port the theme needs.
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
sh.Run "node """ & dir & "\inject.js"" --watch", 0, False
app = sh.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Antigravity\Antigravity.exe"
sh.Run """" & app & """ --remote-debugging-port=0", 1, False
