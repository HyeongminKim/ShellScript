#NoTrayIcon
; Change Windows shortcut will matching macOS shortcut.

; Lock account & Sleep
^#q::
Run rundll32.exe user32.dll LockWorkStation
Sleep 1000
checksum := A_TimeIdle
Loop {
    if (A_TimeIdle > 4000) {
        Run rundll32.exe powrprof.dll SetSuspendState
    } else if (A_TimeIdle < checksum) {
        break
    }
}
return

; Instance path changer like Finder
#+g::
try {
    InputBox, TARGET, Go to the folder:,Please enter Windows absolute path,,,,,,,2147483,%A_MyDocuments%
    if ErrorLevel || !TARGET {
        return
    } 

    Run %TARGET%
} catch e {
    MsgBox, 16, %TARGET%, Windows cannot find '%TARGET%'. Make sure you typed the name correctly, and then try again.
}
return

F20::
  Send {Media_Play_Pause}
return

+F20::
    ShowMediaDialog()
return

ShowMediaDialog() {
    Gui, MediaGui:Destroy
    Gui, MediaGui:+AlwaysOnTop +ToolWindow +OwnDialogs
    Gui, MediaGui:Add, Text,, Media Controls
    Gui, MediaGui:Add, Button, gPlayPause w100, Play/Pause
    Gui, MediaGui:Add, Button, gNextTrack w100, Next
    Gui, MediaGui:Add, Button, gPrevTrack w100, Previous
    Gui, MediaGui:Add, Button, gCancel w100, Cancel
    Gui, MediaGui:Show,, Media Menu
}

PlayPause:
  Send {Media_Play_Pause}
  return

NextTrack:
    Send {Media_Next}
    return

PrevTrack:
    Send {Media_Prev}
    return

Cancel:
    Gui, MediaGui:Destroy
    return

