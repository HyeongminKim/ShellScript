$~LWin::
WinGetActiveTitle, currentActiveTitle
if(currentActiveTitle = "월드 오브 워크래프트") {
    SendInput {LAlt down}
} else {
    SendInput {LWin down}
}
return

$~LWin Up::
WinGetActiveTitle, currentActiveTitle
if(currentActiveTitle = "월드 오브 워크래프트") {
    SendInput {LAlt up}
} else {
    SendInput {LWin up}
}
return
