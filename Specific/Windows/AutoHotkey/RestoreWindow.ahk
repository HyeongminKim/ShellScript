#NoTrayIcon
; 전역 배열과 추적용 맵
global minimizedWindows := Object()
global minimizedCount := 0
global seen := Object()

SetTimer, TrackMinimizedWindows, 500
return

; Alt + - 로 가장 최근 최소화된 창 복원
!-::
if (minimizedCount > 0) {
    hwnd := minimizedWindows[minimizedCount]
    minimizedWindows.Delete(minimizedCount)
    minimizedCount--

    if WinExist("ahk_id " hwnd) {
        WinRestore, ahk_id %hwnd%
        WinActivate, ahk_id %hwnd%
    }
}
return

; 최소화된 창 추적
TrackMinimizedWindows:
    WinGet, id, List,,, Program Manager
    Loop, %id%
    {
        hwnd := id%A_Index%
        WinGet, state, MinMax, ahk_id %hwnd%
        WinGetTitle, title, ahk_id %hwnd%

        if (state = -1 and title != "" and !seen.HasKey(hwnd)) {
            minimizedCount++
            minimizedWindows[minimizedCount] := hwnd
            seen[hwnd] := true
        }

        if (state != -1 and seen.HasKey(hwnd)) {
            seen.Delete(hwnd)
            index := FindIndex(minimizedWindows, hwnd, minimizedCount)
            if (index) {
                ; 앞으로 땡기기
                Loop % minimizedCount - index {
                    i := index + A_Index - 1
                    minimizedWindows[i] := minimizedWindows[i + 1]
                }
                minimizedWindows.Delete(minimizedCount)
                minimizedCount--
            }
        }
    }
return

; 리스트에서 hwnd 인덱스 찾기
FindIndex(list, value, count) {
    Loop, %count%
        if (list[A_Index] == value)
            return A_Index
    return 0
}

