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

