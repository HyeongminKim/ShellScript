; Change Windows shortcut will matching macOS shortcut.

; KoreanIM
^Space::
Send {vk15sc138}
return

; Spotlight
#Space::
Send #{s}
return

#+Space::
return

; Clipboard
#c::
Send ^{c}
return

#x::
Send ^{x}
return

#v::
Send ^{v}
return

#a::
Send ^{a}
return

; Undo & Redo
#z::
Send ^{z}
return

#+z::
Send ^+{z}
return

; Save
#s::
Send ^{s}
return

; Mission Control
^#!Left::
Send ^#{Left}
return

^#!Right::
Send ^#{Right}
return

^#!Up::
Send #{Tab}
return

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

; Open System Preferences
#!,::
Send #{i}
return

; Screen Capture
#+4::
Send #+{s}
return

; Open AppStore
#!^A::
Run ms-windows-store:
return

; Window control
#w::
Send !{F4}
return

#t::
Send ^{t}
return

#f::
Send ^{f}
return

#r::
Send {F5}
return

; Overriedden run key sequence (#r) redefinition
#!r::
Run %A_Appdata%\Microsoft\Windows\Start Menu\Programs\System Tools\Run.lnk
return

#q::
WinGet, TARGET, ProcessName, A
if (TARGET == "Explorer.EXE") {
    SoundPlay %A_WinDir%\Media\Windows Foreground.wav
} else {
    Run taskkill /im %TARGET%,,Hide
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

; Launch Activity Monitor
#!ESC::
Send ^+{ESC}
return

