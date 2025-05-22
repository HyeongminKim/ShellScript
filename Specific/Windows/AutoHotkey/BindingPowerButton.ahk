; PowerButtonUI.ahk

#Persistent
#NoTrayIcon
SetWorkingDir %A_ScriptDir%

; 전원 버튼 이벤트는 따로 연결 필요 (예: 다른 프로그램에서 이 스크립트 실행)
; 여기선 수동으로 F12 키로 테스트
SC15E::ShowPowerDialog()

ShowPowerDialog() {
    Gui, PowerGui:Destroy
    Gui, PowerGui:+AlwaysOnTop +ToolWindow +OwnDialogs
    Gui, PowerGui:Add, Text,, Power key press.
    Gui, PowerGui:Add, Button, gShutdownSection w100, Shutdown
    Gui, PowerGui:Add, Button, gRebootSection w100, Restart
    Gui, PowerGui:Show,, Power Menu
}

ShutdownSection:
    Shutdown, 1 ; 시스템 종료
    return

RebootSection:
    Shutdown, 2 ; 다시 시작
    return

