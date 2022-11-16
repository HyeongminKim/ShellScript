#-*- coding:utf-8 -*-

try:
    import os
    os.system('')

    from enum import Enum
except Exception as error:
    print(f'[35m[FATL] The DiabloLauncher stoped due to {error}[0m')
    exit(1)

class color(Enum):
    RESET = '[0m'
    RED = '[31m'
    GREEN = '[32m'
    YELLOW = '[33m'
    BLUE = '[34m'
    MAGENTA = '[35m'
    GRAY = '[90m'

class errorLevel(Enum):
    INFO = 0
    WARN = 1
    ERR = 2
    FATL = 3

def logformat(level: errorLevel, text: str):
    if level == errorLevel.INFO:
        print(f'{color.GRAY.value}[INFO] {text}{color.RESET.value}')
    elif level == errorLevel.WARN:
        print(f'{color.YELLOW.value}[WARN] {text}{color.RESET.value}')
    elif level == errorLevel.ERR:
        print(f'{color.RED.value}[ERR] {text}{color.RESET.value}')
    elif level == errorLevel.FATL:
        print(f'{color.MAGENTA.value}[FATL] {text}{color.RESET.value}')
        exit(1)
    else:
        logformat(errorLevel.ERR, f'{level} is not known error level type.')

try:
    import platform

    if platform.system() != 'Windows':
        logformat(errorLevel.FATL, f'{platform.system()} system does not support yet.')
    else:
        if platform.release() == '7' or platform.release() == '8' or platform.release() == '10' or platform.release() == '11':
            logformat(errorLevel.INFO, 'support OS detected.')
        else:
            logformat(errorLevel.FATL, f'{platform.system()} {platform.release()} does not support. Please check Diablo Requirements and Specifications.')

    import multiprocessing
    import sys

    if multiprocessing.cpu_count() >= 2 and sys.maxsize > 2**32:
        logformat(errorLevel.INFO, f'supported {platform.processor()} CPU detected. creating GUI...')
    else:
        logformat(errorLevel.FATL, f"{platform.processor()} CPU does not support (core: {multiprocessing.cpu_count()}, {'x64' if sys.maxsize > 2**32 else 'x86'}).\n\tPlease check Diablo Requirements and Specifications.")

    import signal
    import subprocess
    import logging

    from datetime import datetime
    import time

    from tkinter import *
    import tkinter.messagebox
    import tkinter.filedialog
except Exception as error:
    logformat(errorLevel.FATL, f'The DiabloLauncher stoped due to {error}')

diabloExecuted = False
updateChecked = False

forceReboot = False
rebootWaitTime = 10
loadWaitTime = 10

data = None
userApp = os.environ.get('AppData')
userLocalApp = os.environ.get('LocalAppData')
now = datetime.now()
gameStart = None
gameEnd = None
cnt_time = now.strftime("%H:%M:%S")
gamePath = None
resolutionProgram = False
originX = None
originY = None
originFR = None
alteredX = None
alteredY = None
alteredFR = None
definedMod = None

root = Tk()
root.withdraw()
launch = Tk()
launch.withdraw()

switchButton = None
emergencyButton = None
status = None
statusbar = None

fileMenu = None
toolsMenu = None
aboutMenu = None
debugMenu = None

def ShowWindow():
    global launch
    launch.deiconify()
    launch.after(1, lambda: launch.focus_force())

def HideWindow():
    global root
    global launch
    root.after(1, lambda: root.focus_force())
    for widget in launch.winfo_children():
        widget.destroy()
    launch.title('무제')
    launch.withdraw()

def UpdateResProgram():
    global resolutionProgram
    logformat(errorLevel.INFO, 'QRes install check')
    if os.path.isfile('C:/Windows/System32/Qres.exe') or os.path.isfile(f'{userLocalApp}/Program/Common/QRes.exe)'):
        logformat(errorLevel.INFO, f"QRes installed in {subprocess.check_output('where QRes', shell=True, encoding='utf-8').strip()}")
        resolutionProgram = True
    else:
        logformat(errorLevel.INFO, 'QRes did not installed')

def AlertWindow():
    msg_box = tkinter.messagebox.askquestion('디아블로 런처', f'현재 디스플레이 해상도가 {alteredX}x{alteredY} 로 조정되어 있습니다. 게임이 실행 중인 상태에서 해상도 설정을 복구할 경우 퍼포먼스에 영향을 미칠 수 있습니다. 그래도 해상도 설정을 복구하시겠습니까?', icon='question')
    if msg_box == 'yes':
        LaunchGameAgent()
        ExitProgram()
    else:
        tkinter.messagebox.showwarning('디아블로 런처', '해상도가 조절된 상태에서는 런처를 종료할 수 없습니다. 먼저 해상도를 기본 설정으로 변경해 주시기 바랍니다.')

def ExitProgram():
    global root
    global launch
    launch.destroy()
    root.destroy()
    exit(0)

def InterruptProgram(sig, frame):
    global root
    global launch
    logformat(errorLevel.FATL, f'Keyboard Interrupt: {sig}')
    if diabloExecuted:
        LaunchGameAgent()
    ExitProgram()

def UpdateProgram():
    global root
    global launch
    global updateChecked
    local = os.popen('git rev-parse --short HEAD').read().strip()
    logformat(errorLevel.INFO, 'Checking program updates...')
    if os.system('git pull --rebase origin master 2> NUL | findstr DiabloLauncher > NUL 2>&1') == 0:
        remote = os.popen('git rev-parse --short HEAD').read().strip()
        if local != remote:
            tkinter.messagebox.showinfo('디아블로 런처', f'디아블로 런처가 성공적으로 업데이트 되었습니다. ({local} → {remote}) 업데이트를 반영하시려면 프로그램을 다시 시작해 주세요.')
            logformat(errorLevel.INFO, 'Successfully updated. Please restart DiabloLauncher to apply any updates...')
        else:
            if updateChecked:
                tkinter.messagebox.showinfo('디아블로 런처', '디아블로 런처가 최신 버전입니다.')
            logformat(errorLevel.INFO, 'DiabloLauncher Up to date.')
    elif os.system('ping -n 1 -w 1 www.google.com > NUL 2>&1') != 0:
        tkinter.messagebox.showwarning('디아블로 런처', '인터넷 연결이 오프라인인 상태에서는 디아블로 런처를 업데이트 할 수 없습니다. 나중에 다시 시도해 주세요.')
        logformat(errorLevel.ERR, 'Program update failed. Please check your internet connection.')
    elif os.system('git pull --rebase origin master > NUL 2>&1') != 0:
        os.system('git status')
        tkinter.messagebox.showwarning('디아블로 런처', '레포에 알 수 없는 오류가 발생하였습니다. 자세한 사항은 로그를 참조해 주세요. ')
        logformat(errorLevel.ERR, 'Program update failed. Please see the output.')
    else:
        if updateChecked:
            tkinter.messagebox.showinfo('디아블로 런처', '디아블로 런처가 최신 버전입니다.')
        logformat(errorLevel.INFO, 'DiabloLauncher Up to date.')
    updateChecked = True

def ConvertTime(milliseconds: float):
    elapsedTime = milliseconds

    hours = int(elapsedTime / 3600)
    elapsedTime = elapsedTime % 3600
    minutes = int(elapsedTime / 60)
    elapsedTime = elapsedTime % 60
    seconds = int(elapsedTime)

    logformat(errorLevel.INFO, f'The provided {milliseconds} milliseconds converted to readable time - {hours}:{minutes}.{seconds}.')
    return hours, minutes, seconds

def SaveGameRunningTime(playTime: float):
    runtimeFile = None
    try:
        if not os.path.isfile(f'{userApp}/DiabloLauncher/runtime.log'):
            if not os.path.isdir(f'{userApp}/DiabloLauncher'):
                logformat(errorLevel.INFO, 'DiabloLauncher directory does not exist. creating directory')
                os.mkdir(f'{userApp}/DiabloLauncher')
            logformat(errorLevel.INFO, 'runtime.log file does not exist. creating target file with write mode')
            runtimeFile = open(f'{userApp}/DiabloLauncher/runtime.log', 'w')
        else:
            logformat(errorLevel.INFO, 'runtime.log file already exist. opening target file with append mode')
            runtimeFile = open(f'{userApp}/DiabloLauncher/runtime.log', 'a')
        logformat(errorLevel.INFO, f'playTime: {playTime} will be write in {userApp}/DiabloLauncher/runtime.log')
        hours, minutes, seconds = ConvertTime(playTime)
        if hours == 0 and minutes < 2:
            logformat(errorLevel.INFO, f'{playTime} will be ignored. The provided {hours}:{minutes}.{seconds} playtime lower then 2 minutes.')
        else:
            runtimeFile.write(f'{str(playTime)}\n')
            logformat(errorLevel.INFO, f'Successfully wrote {playTime} in {userApp}/DiabloLauncher/runtime.log')
    except Exception as error:
        logformat(errorLevel.ERR, f'Failed to save Game-play logs: {error}')
    finally:
        if runtimeFile is not None:
            runtimeFile.close()

def LoadGameRunningTime():
    global fileMenu
    data = []
    max = 0
    sum = 0
    runtimeFile = None
    try:
        if os.path.isfile(f'{userApp}/DiabloLauncher/runtime.log'):
            runtimeFile = open(f'{userApp}/DiabloLauncher/runtime.log', 'r')
            while True:
                line = runtimeFile.readline()
                if not line: break
                logformat(errorLevel.INFO, f'{line}')
                data.append(line)
            for line in data:
                logformat(errorLevel.INFO, f'{float(line)}')
                if max < float(line):
                    max = float(line)
                sum += float(line)
            fileMenu.entryconfig(1, state='normal')
        else:
            raise FileNotFoundError
    except Exception as error:
        logformat(errorLevel.ERR, f'Failed to load Game-play logs: {error}')
        if os.path.isdir(f'{userApp}/DiabloLauncher'):
            fileMenu.entryconfig(1, state='normal')
        else:
            fileMenu.entryconfig(1, state='disabled')
    finally:
        if runtimeFile is not None:
            runtimeFile.close()
        if data is not None and sum != 0:
            return len(data), max, sum, (sum / len(data))
        elif data is not None and sum == 0:
            return len(data), max, 0, 0
        else:
            return 0, 0, 0, 0

def ClearGameRunningTime():
    if os.path.isfile(f'{userApp}/DiabloLauncher/runtime.log'):
        os.remove(f'{userApp}/DiabloLauncher/runtime.log')
        ReloadStatusBar()
    else:
        logformat(errorLevel.ERR, f'Failed to remove {userApp}/DiabloLauncher/runtime.log file. no such file or directory.')

def GameLauncher(gameName: str, supportedX: int, supportedY: int, os_min: int):
    global diabloExecuted
    global root
    global launch
    global gameStart
    global switchButton
    global toolsMenu
    diabloExecuted = True
    logformat(errorLevel.INFO, f'Launching {gameName}...')
    if resolutionProgram:
        if int(alteredX) < supportedX or int(alteredY) < supportedY:
            logformat(errorLevel.ERR, f'The {gameName} does not supported display resolution {alteredX}x{alteredY} {alteredFR}Hz')
            tkinter.messagebox.showerror('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 {gameName} 가 지원하지 않습니다. 자세한 사항은 공식 홈페이지를 확인하시기 바랍니다. ')
            diabloExecuted = False
            root.protocol("WM_DELETE_WINDOW", ExitProgram)
            HideWindow()
            UpdateStatusValue()
            return
        try:
            if int(platform.release()) >= os_min:
                logformat(errorLevel.INFO, f'The {gameName} supported current OS {platform.system()} {platform.release()}')
            else:
                raise ValueError
        except Exception:
            logformat(errorLevel.ERR, f'The {gameName} does not supported current OS {platform.system()} {platform.release()}')
            tkinter.messagebox.showerror('디아블로 런처', f'{platform.system()} {platform.release()} 은(는) {gameName} 가 지원하지 않습니다. 자세한 사항은 공식 홈페이지를 확인하시기 바랍니다. ')
            diabloExecuted = False
            root.protocol("WM_DELETE_WINDOW", ExitProgram)
            HideWindow()
            UpdateStatusValue()
            return
        if os.system(f'QRes -X {alteredX} -Y {alteredY} -R {alteredFR}') != 0:
            logformat(errorLevel.ERR, f'The current display does not supported choosed resolution {alteredX}x{alteredY} {alteredFR}Hz')
            tkinter.messagebox.showwarning('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
            diabloExecuted = False
            root.protocol("WM_DELETE_WINDOW", ExitProgram)
            HideWindow()
            UpdateStatusValue()
            return
        switchButton['text'] = '디스플레이 해상도 복구 (게임 종료시 사용)'
        root.protocol("WM_DELETE_WINDOW", AlertWindow)
    else:
        switchButton['text'] = '게임 종료'
    os.popen(f'"{gamePath}/{gameName}/{gameName} Launcher.exe"')
    toolsMenu.entryconfig(3, state='disabled')
    gameStart = time.time()
    HideWindow()
    UpdateStatusValue()

def LaunchGameAgent():
    global diabloExecuted
    global root
    global launch
    global switchButton
    global gameEnd
    global toolsMenu
    global definedMod
    if diabloExecuted:
        diabloExecuted = False
        logformat(errorLevel.INFO, 'Setting game mode is false...')
        root.protocol("WM_DELETE_WINDOW", ExitProgram)
        gameEnd = time.time()
        switchButton['text'] = '디아블로 실행...'
        toolsMenu.entryconfig(3, state='normal')
        if resolutionProgram:
            if os.system(f'QRes -X {originX} -Y {originY} -R {originFR}') != 0:
                logformat(errorLevel.ERR, f'The current display does not supported choosed resolution {alteredX}x{alteredY} {alteredFR}Hz')
                tkinter.messagebox.showwarning('디아블로 런처', f'{originX}x{originY} {originFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')

        SaveGameRunningTime(gameEnd - gameStart)
        hours, minutes, seconds = ConvertTime(gameEnd - gameStart)
        logformat(errorLevel.INFO, f'Running game time for this session: {hours}:{minutes}.{seconds}')
        if hours > 0:
            if minutes > 0 and seconds > 0:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 세션에는 {hours}시간 {minutes}분 {seconds}초 동안 플레이 했습니다.')
            elif minutes > 0 and seconds == 0:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 세션에는 {hours}시간 {minutes}분 동안 플레이 했습니다.')
            elif minutes == 0 and seconds > 0:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 세션에는 {hours}시간 {seconds}초 동안 플레이 했습니다.')
            elif minutes == 0 and seconds == 0:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 세션에는 {hours}시간 동안 플레이 했습니다. ')
        elif minutes >= 2:
            if seconds > 0:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 세션에는 {minutes}분 {seconds}초 동안 플레이 했습니다. ')
            else:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 세션에는 {minutes}분 동안 플레이 했습니다. ')
        UpdateStatusValue()
    else:
        launch.title('디아블로 버전 선택')

        note = Label(launch, text='사용가능한 디아블로 버전만 활성화 됩니다')
        diablo2 = Button(launch, text='Diablo II Resurrected\n설치되지 않음', width=20, height=5, command= lambda: GameLauncher('Diablo II Resurrected', 1280, 720, 10))
        diablo3 = Button(launch, text='Diablo III\n설치되지 않음', width=20, height=5, command= lambda: GameLauncher('Diablo III', 1024, 768, 7))
        note.pack()
        diablo2.pack(side=LEFT, padx=10)
        diablo3.pack(side=RIGHT, padx=10)
        if not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
            logformat(errorLevel.INFO, 'Diablo II Resurrected launch button disabled, because launcher is not detected.')
            diablo2['state'] = "disabled"
        else:
            logformat(errorLevel.INFO, 'Diablo II Resurrected launch button enabled.')
            diablo2['state'] = "normal"
            if os.path.isdir(gamePath + '/Diablo II Resurrected/mods'):
                logformat(errorLevel.INFO, 'Diablo II Resurrected mods directory detected.')
                GetModDetails()
                if definedMod is not None and len(definedMod) > 1:
                    logformat(errorLevel.WARN, f"Diablo II Resurrected mods are not cached. Because too many mods detected.")
                    diablo2['text'] = 'Diablo II Resurrected\n모드병합 필요'
                elif definedMod is not None and len(definedMod) == 1:
                    logformat(errorLevel.INFO, f"Converted list[str]: {definedMod} to str: {definedMod[0]}")
                    definedMod = definedMod[0]
                    if os.path.isdir(gamePath + '/Diablo II Resurrected/mods/' + definedMod + f'/{definedMod}.mpq/data') or os.path.isfile(gamePath + '/Diablo II Resurrected/mods/' + definedMod + f'/{definedMod}.mpq'):
                        diablo2['text'] = f'Diablo II Resurrected\n{definedMod} 적용됨'
                    else:
                        tkinter.messagebox.showwarning(title='디아블로 모드 관리자', message='유효하지 않은 모드 배치가 감지되었습니다. ')
                        logformat(errorLevel.WARN, f"The mod {definedMod} does not followed by path:")
                        logformat(errorLevel.WARN, f"\t- {gamePath + '/Diablo II Resurrected/mods/' + definedMod + f'{definedMod}.mpq'}")
                        logformat(errorLevel.WARN, f"\t- {gamePath + '/Diablo II Resurrected/mods/' + definedMod + f'{definedMod}.mpq/data'}")
                        diablo2['text'] = 'Diablo II Resurrected'
                else:
                    logformat(errorLevel.INFO, f"Diablo II Resurrected mods are not cached. Because mods was not installed yet.")
                    diablo2['text'] = 'Diablo II Resurrected'
            else:
                logformat(errorLevel.INFO, 'Diablo II Resurrected mods directory not found.')
                diablo2['text'] = 'Diablo II Resurrected'

        if not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
            logformat(errorLevel.INFO, 'Diablo III launch button disabled, because launcher is not detected.')
            diablo3['state'] = "disabled"
        else:
            logformat(errorLevel.INFO, 'Diablo III launch button enabled.')
            diablo3['state'] = "normal"
            if os.path.isdir(gamePath + '/Diablo III/mods'):
                logformat(errorLevel.INFO, 'Diablo III mods directory detected.')
                diablo3['text'] = 'Diablo III\n모드 지원 안됨'
            else:
                logformat(errorLevel.INFO, 'Diablo III mods directory not found.')
                diablo3['text'] = 'Diablo III'
        ShowWindow()
        launch.mainloop()

def BootAgent(poweroff: str):
    global forceReboot
    global emergencyButton
    global switchButton
    global gameEnd
    global toolsMenu
    forceReboot = True
    gameEnd = time.time()
    if diabloExecuted:
        SaveGameRunningTime(gameEnd - gameStart)
    if poweroff == 'r':
        emergencyButton['text'] = '긴급 재시동 준비중... (재시동 취소)'
        logformat(errorLevel.INFO, 'Starting Emergency reboot agent...')
    elif poweroff == 's':
        emergencyButton['text'] = '긴급 종료 준비중... (종료 취소)'
        logformat(errorLevel.INFO, 'Starting Emergency reboot agent...')
    if resolutionProgram:
        if os.system(f'QRes -X {originX} -Y {originY} -R {originFR}') != 0:
            logformat(errorLevel.ERR, f'The current display does not supported choosed resolution {alteredX}x{alteredY} {alteredFR}Hz')
            tkinter.messagebox.showwarning('디아블로 런처', f'{originX}x{originY} {originFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
    HideWindow()
    UpdateStatusValue()
    if poweroff == 'r':
        os.system(f'shutdown -r -f -t 10 -c "Windows가 DiabloLauncher의 [긴급 재시동] 기능으로 인해 재시동 됩니다."')
    elif poweroff == 's':
        os.system(f'shutdown -s -f -t 10 -c "Windows가 DiabloLauncher의 [긴급 종료] 기능으로 인해 종료 됩니다."')
    logformat(errorLevel.INFO, 'Successfully executed Windows shutdown.exe')
    switchButton['state'] = "disabled"
    toolsMenu.entryconfig(3, state='disabled')

def EmgergencyReboot():
    global launch
    global forceReboot
    global emergencyButton
    global switchButton
    global toolsMenu
    if forceReboot:
        forceReboot = False
        emergencyButton['text'] = '긴급 전원 작업 (게임 저장 후 실행 요망)'
        logformat(errorLevel.INFO, 'Aborting Emergency agent...')
        switchButton['state'] = "normal"
        toolsMenu.entryconfig(3, state='normal')
        os.system(f'shutdown -a')
        logformat(errorLevel.INFO, 'Successfully executed Windows shutdown.exe')
    else:
        launch.title('전원')
        if resolutionProgram and diabloExecuted:
            note = Label(launch, text=f'수행할 작업 시작전 {originX}x{originY} 해상도로 복구 후 계속')
        else:
            note = Label(launch, text='수행할 작업 선택')
        reboot = Button(launch, text='재시동', width=20, height=5, command= lambda: BootAgent('r'))
        halt = Button(launch, text='종료', width=20, height=5, command= lambda: BootAgent('s'))
        note.pack()
        reboot.pack(side=LEFT, padx=10)
        halt.pack(side=RIGHT, padx=10)
        ShowWindow()
        launch.mainloop()

def GetModDetails():
    global definedMod
    definedMod = os.listdir(f'{gamePath}/Diablo II Resurrected/mods')
    logformat(errorLevel.INFO, f"Detected mods: {definedMod}")

def GetEnvironmentValue():
    global data
    global gamePath
    global fileMenu
    if resolutionProgram:
        global originX
        global originY
        global originFR
        global alteredX
        global alteredY
        global alteredFR

    try:
        data = os.environ.get('DiabloLauncher')
        logformat(errorLevel.INFO, f'{data}')
        temp = None
        if resolutionProgram:
            logformat(errorLevel.INFO, 'QRes detected. parameter count should be 7')
            gamePath, originX, originY, originFR, alteredX, alteredY, alteredFR, temp = data.split(';')
            logformat(errorLevel.INFO, 'parameter conversion succeed')
            fileMenu.entryconfig(0, state='normal')
            toolsMenu.entryconfig(4, state='normal')
        else:
            logformat(errorLevel.INFO, 'QRes not detected. parameter count should be 1')
            gamePath, temp = data.split(';')
            logformat(errorLevel.INFO, 'parameter conversion succeed')
            fileMenu.entryconfig(0, state='normal')
            toolsMenu.entryconfig(4, state='normal')

        if resolutionProgram:
            logformat(errorLevel.INFO, f'{gamePath}')
            logformat(errorLevel.INFO, f'{int(originX)}')
            logformat(errorLevel.INFO, f'{int(originY)}')
            logformat(errorLevel.INFO, f'{float(originFR)}')
            logformat(errorLevel.INFO, f'{int(alteredX)}')
            logformat(errorLevel.INFO, f'{int(alteredY)}')
            logformat(errorLevel.INFO, f'{float(alteredFR)}')
    except Exception as error:
        tkinter.messagebox.showerror('디아블로 런처', f'환경변수 파싱중 예외가 발생하였습니다. 필수 파라미터가 누락되지 않았는지, 또는 잘못된 타입을 제공하지 않았는지 확인하시기 바랍니다. Exception code: {error}')
        logformat(errorLevel.ERR, f'Unknown data or parameter style: {data}\n\t{error}')
        data = None
        gamePath = None
        originX = None
        originY = None
        originFR = None
        alteredX = None
        alteredY = None
        alteredFR = None
        fileMenu.entryconfig(0, state='disabled')
        toolsMenu.entryconfig(4, state='disabled')
    finally:
        logformat(errorLevel.INFO, f'{data}')
        if resolutionProgram:
            logformat(errorLevel.INFO, f'{gamePath}')
            logformat(errorLevel.INFO, f'{originX}')
            logformat(errorLevel.INFO, f'{originY}')
            logformat(errorLevel.INFO, f'{originFR}')
            logformat(errorLevel.INFO, f'{alteredX}')
            logformat(errorLevel.INFO, f'{alteredY}')
            logformat(errorLevel.INFO, f'{alteredFR}')
        UpdateResProgram()

def SetEnvironmentValue():
    global data
    tkinter.messagebox.showinfo('환경변수 편집기', '이 편집기는 본 프로그램에서만 적용되며 디아블로 런처를 종료 시 모든 변경사항이 유실됩니다. 변경사항을 영구적으로 적용하시려면 "고급 시스템 설정"을 이용해 주세요. ')
    envWindow = Tk()
    envWindow.title('환경변수 편집기')
    if resolutionProgram:
        envWindow.geometry("265x100+200+200")
    else:
        envWindow.geometry("280x100+200+200")
    envWindow.resizable(False, False)
    envWindow.attributes('-toolwindow', True)

    def openDirectoryDialog():
        global envGameDir
        temp = gamePath
        logformat(errorLevel.INFO, f'Opening directory dialog location: {gamePath if gamePath is not None else "C:/Program Files (x86)"}')
        envGameDir = tkinter.filedialog.askdirectory(parent=envWindow, initialdir=f"{gamePath if gamePath is not None else 'C:/Program Files (x86)'}", title='Battle.net 게임 디렉토리 선택')
        if envGameDir == "":
            logformat(errorLevel.INFO, f'Selected directory dialog location: None directory path provided. resetting {temp}')
            envGameDir = temp
        else:
            logformat(errorLevel.INFO, f'Selected directory dialog location: {envGameDir}')

    envGameBtn = Button(envWindow, text=f'{"게임 디렉토리 변경..." if gamePath is not None else "게임 디렉토리 등록..."}', command=openDirectoryDialog, width=30)
    if resolutionProgram:
        originXtext = Label(envWindow, text='기본 X')
        originYtext = Label(envWindow, text=' Y')
        originFRtext = Label(envWindow, text=' FR')
        envOriginX = tkinter.Entry(envWindow, width=5)
        envOriginY = tkinter.Entry(envWindow, width=5)
        envOriginFR = tkinter.Entry(envWindow, width=4)

        alteredXtext = Label(envWindow, text='변경 X')
        alteredYtext = Label(envWindow, text=' Y')
        alteredFRtext = Label(envWindow, text=' FR')
        envAlteredX = tkinter.Entry(envWindow, width=5)
        envAlteredY = tkinter.Entry(envWindow, width=5)
        envAlteredFR = tkinter.Entry(envWindow, width=4)
    else:
        infoText = Label(envWindow, text='나머지 환경변수는 QRes가 필요하므로 제외됨')

    if resolutionProgram:
        envGameBtn.grid(row=0, column=1, columnspan=5)

        originXtext.grid(row=1, column=0)
        envOriginX.grid(row=1, column=1)
        originYtext.grid(row=1, column=2)
        envOriginY.grid(row=1, column=3)
        originFRtext.grid(row=1, column=4)
        envOriginFR.grid(row=1, column=5)

        alteredXtext.grid(row=2, column=0)
        envAlteredX.grid(row=2, column=1)
        alteredYtext.grid(row=2, column=2)
        envAlteredY.grid(row=2, column=3)
        alteredFRtext.grid(row=2, column=4)
        envAlteredFR.grid(row=2, column=5)
    else:
        envGameBtn.pack()
        infoText.pack()

    if data is not None:
        if resolutionProgram:
            envOriginX.insert(0, originX)
            envOriginY.insert(0, originY)
            envOriginFR.insert(0, originFR)
            envAlteredX.insert(0, alteredX)
            envAlteredY.insert(0, alteredY)
            envAlteredFR.insert(0, alteredFR)

    def commit():
        global envGameDir
        try:
            logformat(errorLevel.INFO, f'{envGameDir}')
        except NameError:
            envGameDir = gamePath
            logformat(errorLevel.INFO, f'Selected directory dialog location: None directory path provided. resetting {envGameDir}')

        if resolutionProgram:
            if envGameDir == '' or envOriginX.get() == '' or envOriginY.get() == '' or envOriginFR.get() == '' or envAlteredX.get() == '' or envAlteredY.get() == '' or envAlteredFR.get() == '':
                tkinter.messagebox.showwarning('환경변수 편집기', '일부 환경변수가 누락되었습니다.')
                logformat(errorLevel.WARN, 'some env can not be None.')
                envWindow.after(1, lambda: envWindow.focus_force())
                return
            else:
                os.environ['DiabloLauncher'] = f'{envGameDir.replace(";", "")};{envOriginX.get().replace(";", "")};{envOriginY.get().replace(";", "")};{envOriginFR.get().replace(";", "")};{envAlteredX.get().replace(";", "")};{envAlteredY.get().replace(";", "")};{envAlteredFR.get().replace(";", "")};'
                logformat(errorLevel.INFO, f"gamePath = {os.environ.get('DiabloLauncher')}")
        else:
            if envGameDir == '':
                tkinter.messagebox.showwarning('환경변수 편집기', '게임 디렉토리 환경변수가 누락되었습니다.')
                logformat(errorLevel.WARN, 'gamePath can not be None.')
                envWindow.after(1, lambda: envWindow.focus_force())
                return
            else:
                os.environ['DiabloLauncher'] = f'{envGameDir.replace(";", "")};'
                logformat(errorLevel.INFO, f"gamePath = {os.environ.get('DiabloLauncher')}")

        UpdateStatusValue()
        if data is not None and not os.path.isdir(gamePath):
            tkinter.messagebox.showwarning('환경변수 편집기', f'{gamePath} 디렉토리가 존재하지 않습니다.')
            logformat(errorLevel.WARN, f'{gamePath} no such directory.')
            envWindow.after(1, lambda: envWindow.focus_force())
        elif data is not None and os.path.isdir(gamePath):
            if not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                tkinter.messagebox.showwarning('환경변수 편집기', f'{gamePath} 디렉토리에는 적합한 게임이 존재하지 않습니다.')
                logformat(errorLevel.WARN, f'{gamePath} not contains game directory.')
                envWindow.after(1, lambda: envWindow.focus_force())
            else:
                envWindow.destroy()

    def openEnvSetting():
        msg_box = tkinter.messagebox.askquestion('디아블로 런처', '"고급 시스템 설정"에 접근 시 관리자 권한을 요청하는 프롬프트가 나타날 수 있으며, 업데이트된 환경변수를 반영하기 위해 프로그램을 종료해야 합니다. 계속하시겠습니까?', icon='question')
        if msg_box == 'yes':
            logformat(errorLevel.INFO, 'starting advanced system env editor... This action will required UAC')
            os.system('sysdm.cpl ,3')
            tkinter.messagebox.showwarning('디아블로 런처', '시스템 환경변수 수정을 모두 완료한 후 다시 실행해 주세요.')
            logformat(errorLevel.INFO, 'advanced system env editor launched. DiabloLauncher now exiting...')
            exit(0)
        else:
            envWindow.after(1, lambda: envWindow.focus_force())

    envSet = tkinter.Button(envWindow, text='고급 시스템 설정', command=openEnvSetting)
    commitBtn = tkinter.Button(envWindow, text='적용', command=commit)

    if resolutionProgram:
        envSet.grid(row=3, column=1, columnspan=2)
        commitBtn.grid(row=3, column=4)
    else:
        envSet.pack(side=LEFT, padx=10)
        commitBtn.pack(side=RIGHT, padx=10)

    envWindow.mainloop()

def RequirementCheck():
    if not resolutionProgram:
        logformat(errorLevel.WARN, f'QRes not installed or not in...\n\t- C:\\Windows\\System32\n\t- {userLocalApp}/Program/Common/QRes.exe')
        if os.environ.get('IGN_RES_ALERT') != 'true':
            msg_box = tkinter.messagebox.askquestion('디아블로 런처', '해상도를 변경하려면 QRes를 먼저 설치하여야 합니다. 지금 QRes를 다운로드 하시겠습니까?', icon='question')
            if msg_box == 'yes':
                os.system('explorer https://www.softpedia.com/get/Multimedia/Video/Other-VIDEO-Tools/QRes.shtml')
        else:
            logformat(errorLevel.WARN, f'QRes install check dialog rejected due to "IGN_RES_ALERT" env prameter is true.\n\tPlease install QRes if would you like change display resolution.')
            print(f"\t{color.YELLOW.value}URL:{color.BLUE.value} https://www.softpedia.com/get/Multimedia/Video/Other-VIDEO-Tools/QRes.shtml{color.RESET.value}")

    if data is None:
        logformat(errorLevel.WARN, 'parameter not set.')
        tkinter.messagebox.showwarning('디아블로 런처', '환경변수가 설정되어 있지 않습니다. "환경변수 편집" 버튼을 클릭하여 임시로 모든 기능을 사용해 보십시오.')
    elif data is not None and not os.path.isdir(gamePath):
        logformat(errorLevel.WARN, f'{gamePath} directory not exist.')
        tkinter.messagebox.showwarning('디아블로 런처', f'{gamePath} 디렉토리가 존재하지 않습니다.')
    elif not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
        logformat(errorLevel.WARN, f'game not exist in {gamePath}.')
        tkinter.messagebox.showwarning('디아블로 런처', f'{gamePath} 디렉토리에는 적합한 게임이 존재하지 않습니다.')

def UpdateStatusValue():
    global status
    global switchButton
    GetEnvironmentValue()
    now = datetime.now()
    cnt_time = now.strftime("%H:%M:%S")
    if data is None:
        status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: 아니요\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L > NUL 2>&1') != 0 else '예'}\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음 \n게임 디렉토리: 알 수 없음\n디렉토리 존재여부: 아니요\n디아블로 실행: 알 수 없음\n실행가능 버전: 없음\n"
        switchButton['state'] = "disabled"
    else:
        if resolutionProgram:
            if os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 예\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II, III\n"
            elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 예\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II\n"
            elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 예\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: III\n"
            else:
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 예\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n"
        else:
            if os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n\n\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II, III\n"
            elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n\n\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II\n"
            elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n\n\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: III\n"
            else:
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n\n\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n"
        switchButton['state'] = "normal"
        ReloadStatusBar()

def ReloadStatusBar():
    global statusbar
    global toolsMenu
    loadStart = time.time()
    count, max, sum, avg = LoadGameRunningTime()
    maxHours, maxMinutes, maxSeconds = ConvertTime(max)
    avgHours, avgMinutes, avgSeconds = ConvertTime(avg)
    sumHours, sumMinutes, sumSeconds = ConvertTime(sum)
    loadEnd = time.time()

    elapsedTime = loadEnd - loadStart
    if elapsedTime > loadWaitTime:
        logformat(errorLevel.WARN, f'The request timeout when loading game data {userApp}/DiabloLauncher/runtime.log file.')
        logformat(errorLevel.INFO, f'Loading game data elapsed time was {elapsedTime} seconds. But, current timeout setting is {loadWaitTime} seconds.')
        logformat(errorLevel.INFO, f'NOTE: The {userApp}/DiabloLauncher/runtime.log contents cleared.')
        ClearGameRunningTime()
    elif elapsedTime > (loadWaitTime / 2):
        logformat(errorLevel.WARN, f'The request job too slow when loading game data {userApp}/DiabloLauncher/runtime.log file.')
        logformat(errorLevel.INFO, f'Loading game data elapsed time was {elapsedTime} seconds, and current timeout setting is {loadWaitTime} seconds.')
        logformat(errorLevel.INFO, f'NOTE: {userApp}/DiabloLauncher/runtime.log contents will clear when this issues raised again.')
    else:
        logformat(errorLevel.INFO, f'Loading game data elapsed time was {elapsedTime} seconds.')

    logformat(errorLevel.INFO, f'Previous game time for max session: {maxHours}:{maxMinutes}.{maxSeconds}')
    logformat(errorLevel.INFO, f'Previous game time for avg session: {avgHours}:{avgMinutes}.{avgSeconds}')
    logformat(errorLevel.INFO, f'Previous game time for sum session: {sumHours}:{sumMinutes}.{sumSeconds}')

    if count >= 10 or maxHours >= 10 or avgHours >= 10 or sumHours >= 10:
        root.title(f"디아블로 런처 (rev. {subprocess.check_output('git rev-parse --short HEAD', shell=True, encoding='utf-8').strip()})")
        if sumHours >= 8766000:
            statusbar['text'] = f"세션: {count}개 | 최고: {maxHours}시간 {maxMinutes}분 {maxSeconds}초 | 평균: {avgHours}시간 {avgMinutes}분 {avgSeconds}초 | 합계: 로드할 수 없음"
        elif sumHours >= 8766:
            statusbar['text'] = f"세션: {count}개 | 최고: {maxHours}시간 {maxMinutes}분 {maxSeconds}초 | 평균: {avgHours}시간 {avgMinutes}분 {avgSeconds}초 | 합계: {int(sumHours / 8766)}년 {int(sumHours % 8766)}월"
        elif sumHours >= 731:
            statusbar['text'] = f"세션: {count}개 | 최고: {maxHours}시간 {maxMinutes}분 {maxSeconds}초 | 평균: {avgHours}시간 {avgMinutes}분 {avgSeconds}초 | 합계: {int(sumHours / 731)}월 {int(sumHours % 731)}주"
        elif sumHours >= 168:
            statusbar['text'] = f"세션: {count}개 | 최고: {maxHours}시간 {maxMinutes}분 {maxSeconds}초 | 평균: {avgHours}시간 {avgMinutes}분 {avgSeconds}초 | 합계: {int(sumHours / 168)}주 {int(sumHours % 168)}일"
        elif sumHours >= 24:
            statusbar['text'] = f"세션: {count}개 | 최고: {maxHours}시간 {maxMinutes}분 {maxSeconds}초 | 평균: {avgHours}시간 {avgMinutes}분 {avgSeconds}초 | 합계: {int(sumHours / 24)}일 {int(sumHours % 24)}시간"
        else:
            statusbar['text'] = f"세션: {count}개 | 최고: {maxHours}시간 {maxMinutes}분 {maxSeconds}초 | 평균: {avgHours}시간 {avgMinutes}분 {avgSeconds}초 | 합계: {sumHours}시간 {sumMinutes}분 {sumSeconds}초"
        statusbar['anchor'] = tkinter.CENTER
    elif count > 2:
        statusbar['text'] = f"{subprocess.check_output('git rev-parse --short HEAD', shell=True, encoding='utf-8').strip()} | 세션: {count}개 | 최고: {maxHours}시간 {maxMinutes}분 {maxSeconds}초 | 평균: {avgHours}시간 {avgMinutes}분 {avgSeconds}초 | 합계: {sumHours}시간 {sumMinutes}분 {sumSeconds}초"
        statusbar['anchor'] = tkinter.CENTER
        toolsMenu.entryconfig(8, state='normal')
    elif count > 0:
        statusbar['text'] = f"{subprocess.check_output('git rev-parse --short HEAD', shell=True, encoding='utf-8').strip()} | 세션: {count}개 | 최고: {maxHours}시간 {maxMinutes}분 {maxSeconds}초 | 평균: 데이터 부족 | 합계: {sumHours}시간 {sumMinutes}분 {sumSeconds}초"
        statusbar['anchor'] = tkinter.CENTER
        toolsMenu.entryconfig(8, state='normal')
    else:
        statusbar['text'] = f"{subprocess.check_output('git rev-parse --short HEAD', shell=True, encoding='utf-8').strip()} | 세션 통계를 로드할 수 없음"
        statusbar['anchor'] = tkinter.W
        toolsMenu.entryconfig(8, state='disabled')

def init():
    global root
    global launch
    global switchButton
    global emergencyButton
    global status
    global statusbar
    global fileMenu
    global toolsMenu
    global aboutMenu
    global debugMenu

    root.title("디아블로 런처")
    root.geometry("520x420+100+100")
    root.deiconify()
    root.resizable(False, False)
    root.attributes('-toolwindow', True)
    launch.title('무제')
    launch.geometry("300x125+200+200")
    launch.resizable(False, False)
    launch.attributes('-toolwindow', True)
    root.after(1, lambda: root.focus_force())

    launch.protocol("WM_DELETE_WINDOW", HideWindow)
    root.protocol("WM_DELETE_WINDOW", ExitProgram)
    signal.signal(signal.SIGINT, InterruptProgram)

    def ResetGameStatus():
        count, max, sum, avg = LoadGameRunningTime()
        if count > 0:
            msg_box = tkinter.messagebox.askyesno(title='디아블로 런처', message=f'통계 재설정을 수행할 경우 {count}개의 세션이 영원히 유실되며 되돌릴 수 없습니다. 만약의 경우를 대비하여 {userApp}/DiabloLauncher/runtime.log 파일을 백업하시기 바랍니다. 통계 재설정을 계속 하시겠습니까? ')
            if msg_box:
                ClearGameRunningTime()

    def ForceReload(*args):
        UpdateStatusValue()
        ReloadStatusBar()

    def ForceProgramUpdate():
        msg_box = tkinter.messagebox.askquestion('디아블로 런처', '디아블로 런처 초기 실행 이후에 업데이트를 수행할 경우 디아블로 런처가 불안정해질 수 있습니다. 계속 진행하시겠습니까?', icon='question')
        if msg_box == 'yes':
            logformat(errorLevel.WARN, f'Force program update will take effect Diablo Launcher make unstable probably.')
            UpdateProgram()

    def OpenGameStatusDir():
        userApp = os.environ.get('AppData')
        if os.path.isdir(f'{userApp}/DiabloLauncher'):
            logformat(errorLevel.INFO, f'The {userApp}/DiabloLauncher directory exist. The target directory will now open.')
            os.startfile(f'"{userApp}/DiabloLauncher"')

    def OpenGameDir():
        if gamePath is not None and os.path.isdir(gamePath):
            logformat(errorLevel.INFO, f'The {gamePath} directory exist. The target directory will now open.')
            os.startfile(f'"{gamePath}"')

    def openControlPanel():
        os.system('control.exe appwiz.cpl')

    def OpenDevSite():
        os.system('explorer https://github.com/HyeongminKim/ShellScript')

    def OpenDevIssues():
        now = datetime.now()
        cnt_time = now.strftime("%H:%M:%S")
        msg_box = tkinter.messagebox.askyesno(title='디아블로 런처', message='이슈를 제보할 경우 터미널에 출력된 전체 로그와 경고창, 프로그램 화면 등을 첨부하여 주세요. 만약 가능하다면 어떠한 이유로 문제가 발생하였으며, 문제가 재현 가능한지 등을 첨부하여 주시면 좀 더 빠른 대응이 가능합니다. 지금 이슈 제보 페이지를 방문하시겠습니까?')
        if msg_box:
            logformat(errorLevel.INFO, f"=== Generated Report at {cnt_time} ===")
            logformat(errorLevel.INFO, f"Current agent: {platform.system()} {platform.release()}, Python {platform.python_version()}, {subprocess.check_output('git --version', shell=True, encoding='utf-8').strip()}")
            logformat(errorLevel.INFO, f"env data: {'configured' if data is not None else 'None'}")
            if resolutionProgram:
                logformat(errorLevel.INFO, f"QRes version: {subprocess.check_output('QRes /S | findstr QRes', shell=True, encoding='utf-8').strip()}")
            else:
                logformat(errorLevel.INFO, f"QRes version: None")
            logformat(errorLevel.INFO, f"Resolution vector: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None and resolutionProgram else 'Unknown'}")
            logformat(errorLevel.INFO, f"GameDir path: {f'{gamePath}' if gamePath is not None else 'Unknown'}")
            if gamePath is not None:
                if os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                    logformat(errorLevel.INFO, "Installed Diablo version: II, III")
                elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
                    logformat(errorLevel.INFO, "Installed Diablo version: II")
                elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                    logformat(errorLevel.INFO, "Installed Diablo version: III")
                else:
                    logformat(errorLevel.INFO, "Installed Diablo version: None")
            else:
                logformat(errorLevel.INFO, "Installed Diablo version: N/A")

            logformat(errorLevel.INFO, f"GameDir exist: {'True' if gamePath is not None and os.path.isdir(gamePath) else 'False'}")
            logformat(errorLevel.INFO, f"Diablo Executed: {'True' if diabloExecuted else 'False'}")
            logformat(errorLevel.INFO, f"===== End Report ======")
            logformat(errorLevel.WARN, 'NOTE: Please attach the terminal output after the code-page log')
            os.system('explorer https://github.com/HyeongminKim/ShellScript/issues')

    def AboutThisApp(*args):
        about = Tk()
        about.title("이 디아블로 런처에 관하여")
        about.geometry("500x340+400+400")
        about.deiconify()
        about.resizable(False, False)
        about.attributes('-toolwindow', True)

        def openBlizzardLegalSite():
            os.system('explorer https://www.blizzard.com/en-us/legal/9c9cb70b-d1ed-4e17-998a-16c6df46be7b/copyright-notices')
        def openAppleLegalSite():
            os.system('explorer https://www.apple.com/kr/legal/intellectual-property/guidelinesfor3rdparties.html')

        if resolutionProgram:
            text = Label(about, text=f"{platform.system()} {platform.release()}, Python {platform.python_version()}, {subprocess.check_output('git --version', shell=True, encoding='utf-8').strip()}\n\n--- Copyright ---\nDiablo II Resurrected, Diablo III\n(c) 2022 BLIZZARD ENTERTAINMENT, INC. ALL RIGHTS RESERVED.\n\nDiablo Launcher\nCopyright (c) 2022 Hyeongmin Kim\n\n{subprocess.check_output('QRes /S | findstr QRes', shell=True, encoding='utf-8').strip()}\n{subprocess.check_output('QRes /S | findstr Copyright', shell=True, encoding='utf-8').strip()}\n\n이 디아블로 런처에서 언급된 특정 상표는 각 소유권자들의 자산입니다.\n디아블로(Diablo), 블리자드(Blizzard)는 Blizzard Entertainment, Inc.의 등록 상표입니다.\nBootCamp, macOS는 Apple, Inc.의 등록 상표입니다.\n\n자세한 사항은 아래 버튼을 클릭해 주세요")
        else:
            text = Label(about, text=f"{platform.system()} {platform.release()}, Python {platform.python_version()}, {subprocess.check_output('git --version', shell=True, encoding='utf-8').strip()}\n\n--- Copyright ---\nDiablo II Resurrected, Diablo III\n(c) 2022 BLIZZARD ENTERTAINMENT, INC. ALL RIGHTS RESERVED.\n\nDiablo Launcher\nCopyright (c) 2022 Hyeongmin Kim\n\n이 디아블로 런처에서 언급된 특정 상표는 각 소유권자들의 자산입니다.\n디아블로(Diablo), 블리자드(Blizzard)는 Blizzard Entertainment, Inc.의 등록 상표입니다.\nBootCamp, macOS는 Apple, Inc.의 등록 상표입니다.\n\n자세한 사항은 아래 버튼을 클릭해 주세요")
        blizzard = Button(about, text='블리자드 저작권 고지', command=openBlizzardLegalSite)
        apple = Button(about, text='애플컴퓨터 저작권 고지', command=openAppleLegalSite)
        text.pack()
        blizzard.pack(pady=4)
        apple.pack()
        about.mainloop()

    def BootCampSoundRecover():
        msg_box = tkinter.messagebox.askyesno(title='디아블로 런처', message='"사운드 장치 문제해결" 메뉴는 사운드 장치가 Cirrus Logic일 경우에만 적용됩니다. 계속하시겠습니까?')
        if msg_box == True:
            soundRecover = Tk()
            soundRecover.title("Cirrus Logic 문제 해결")
            soundRecover.geometry("480x170+300+300")
            soundRecover.deiconify()
            soundRecover.resizable(False, False)
            soundRecover.attributes('-toolwindow', True)
            notice = Label(soundRecover, text='이 도움말의 일부 과정은 macOS의 BootCamp 지원 앱에서 수행해야 합니다.')
            contents = Label(soundRecover, text='1. BootCamp 지원 앱에서 Windows 지원 소프트웨어를 USB에 저장합니다.\n2. BootCamp로 재시동합니다.\n3. msconfig를 실행에 입력하여 부팅 옵션을 안전 부팅의 최소 설치로 선택합니다.\n4. BootCamp를 안전모드로 재시동합니다. \n5. 실행에 devmgmt.msc를 입력하여 장치관리자를 띄웁니다. \n6. Cirrus Logic 디바이스와 드라이버를 제거합니다.\n7. 1번에서 다운받은 폴더 경로를 드라이버 설치경로로 선택합니다. \n8. msconfig를 실행에 입력하여 안전부팅 체크박스를 해제합니다. \n9. BootCamp를 재시동합니다. ', anchor='w', justify=LEFT)
            notice.pack()
            contents.pack()
            soundRecover.mainloop()

    def thirdpartyModController():
        global definedMod
        tkinter.messagebox.showwarning(title='디아블로 런처', message='디아블로 모드 사용시 게임 경험이 불안정해질 수 있으며, 일부 모드를 사용할 시 불이익을 받을 수 있습니다.')
        modConfig = Tk()
        modConfig.title("모드 관리자")
        modConfig.geometry("240x220+300+300")
        modConfig.deiconify()
        modConfig.resizable(False, False)
        modConfig.attributes('-toolwindow', True)

        def OpenD2RModDir():
            if not os.path.isdir(f'{gamePath}/Diablo II Resurrected/mods'):
                os.mkdir(f'{gamePath}/Diablo II Resurrected/mods')
            os.startfile(f'"{gamePath}/Diablo II Resurrected/mods"')

        def OpenD3ModDir():
            tkinter.messagebox.showwarning(title='디아블로 모드 관리자', message='Diablo III 은(는) 모드 확장을 지원하지 않습니다. ')
            modConfig.after(1, lambda: modConfig.focus_force())

        openGameModText = Label(modConfig, text='게임별 모드 디렉토리 열기')
        diablo2Mod = Button(modConfig, text='Diablo II Resurrected', command=OpenD2RModDir)
        diablo3Mod = Button(modConfig, text='Diablo III', command=OpenD3ModDir)

        note = Label(modConfig, text=f'블리자드 런처에 명령행 인수를 입력하세요\n예시: -mod exampleMod -txt\n기술적 한계로 해당 런처의 명령행 인수를\n검증할 수 없습니다.')
        licenseMod = Label(modConfig, text='모드에 대한 라이선스는\n모드 제작자에게 있습니다.')

        if not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
            diablo2Mod['text'] = 'Diablo II Resurrected\n설치 안됨'
            diablo2Mod['state'] = 'disabled'
            logformat(errorLevel.WARN, f"Diablo II Resurrected mods are not cached. Because Diablo was not installed yet.")
        else:
            diablo2Mod['state'] = 'normal'
            diablo2Mod['text'] = 'Diablo II Resurrected\n알 수 없음'
            GetModDetails()
            if definedMod is not None and len(definedMod) > 1:
                logformat(errorLevel.WARN, f"Diablo II Resurrected mods are not cached. Because too many mods detected.")
                definedMod = None
                diablo2Mod['text'] = 'Diablo II Resurrected\n병합 필요'
                licenseMod['text'] = f'여러 모드들을 통합하지 않을경우\n대부분의 모드가 동작하지 않음'
            elif definedMod is not None and len(definedMod) == 1:
                logformat(errorLevel.INFO, f"Converted list[str]: {definedMod} to str: {definedMod[0]}")
                definedMod = definedMod[0]
                if os.path.isdir(gamePath + '/Diablo II Resurrected/mods/' + definedMod + f'/{definedMod}.mpq/data') or os.path.isfile(gamePath + '/Diablo II Resurrected/mods/' + definedMod + f'/{definedMod}.mpq'):
                    diablo2Mod['text'] = f'Diablo II Resurrected\n{definedMod} 적용됨'
                    licenseMod['text'] = f'{definedMod} 모드에 대한 라이선스는\n모드 제작자에게 있습니다.'
                    note['text'] = f'블리자드 런처에 명령행 인수를 입력하세요\nex) -mod {definedMod} -txt\n기술적 한계로 해당 런처의 명령행 인수를\n검증할 수 없습니다.'
                else:
                    logformat(errorLevel.WARN, f"The mod {definedMod} does not followed by path:")
                    logformat(errorLevel.WARN, f"\t- {gamePath + '/Diablo II Resurrected/mods/' + definedMod + f'{definedMod}.mpq'}")
                    logformat(errorLevel.WARN, f"\t- {gamePath + '/Diablo II Resurrected/mods/' + definedMod + f'{definedMod}.mpq/data'}")
                    tkinter.messagebox.showwarning(title='디아블로 모드 관리자', message='유효하지 않은 모드 배치가 감지되었습니다. ')
                    definedMod = None
            else:
                definedMod = None
                logformat(errorLevel.INFO, f"Diablo II Resurrected mods are not cached. Because mods was not installed yet.")
                diablo2Mod['text'] = 'Diablo II Resurrected\n일반'
                licenseMod['text'] = f'모드 설치시\n해당 모드 라이선스는 제작자에게 있습니다.'

        if not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
            logformat(errorLevel.INFO, f"Diablo III mods are not cached. Because it was not supported yet.")
            diablo3Mod['text'] = 'Diablo III\n설치 안됨'
            diablo3Mod['state'] = 'disabled'
        else:
            logformat(errorLevel.INFO, f"Diablo III mods are not cached. Because it was not supported yet.")
            diablo3Mod['state'] = 'normal'
            diablo3Mod['text'] = 'Diablo III\n추가 정보'

        attention = Label(modConfig, text='하나의 모드 파일만 적용할 수 있습니다\n이미 제작된 통합본을 사용하거나\nmpq 관리 툴로 직접 병합해도 됩니다.')

        openGameModText.grid(row=0, column=0, columnspan=2)
        diablo2Mod.grid(row=1, column=0)
        diablo3Mod.grid(row=1, column=1)
        note.grid(row=2, column=0, columnspan=2)
        attention.grid(row=3, column=0, columnspan=2)
        licenseMod.grid(row=4, column=0, columnspan=2)

        modConfig.mainloop()

    menubar = Menu(root)
    fileMenu = Menu(menubar, tearoff=0)
    fileMenu.add_command(label='게임폴더 열기', command=OpenGameDir)
    fileMenu.add_command(label='통계폴더 열기', command=OpenGameStatusDir)
    menubar.add_cascade(label='파일', menu=fileMenu)

    toolsMenu = Menu(menubar, tearoff=0)
    toolsMenu.add_command(label='새로 고침', command=ForceReload, accelerator='F5')
    toolsMenu.add_command(label='런처 업데이트 확인...', command=ForceProgramUpdate)
    toolsMenu.add_separator()
    toolsMenu.add_command(label='환경변수 에디터...', command=SetEnvironmentValue)
    toolsMenu.add_command(label='모드 관리자', command=thirdpartyModController)

    if os.path.isfile('C:/Program Files/Boot Camp/Bootcamp.exe'):
        toolsMenu.add_command(label='소리 문제 해결...', command=BootCampSoundRecover, state='normal')
    else:
        toolsMenu.add_command(label='소리 문제 해결...', command=BootCampSoundRecover, state='disabled')

    toolsMenu.add_separator()
    toolsMenu.add_command(label='프로그램 제거 및 변경', command=openControlPanel)
    toolsMenu.add_command(label='통계 재설정...', command=ResetGameStatus)
    menubar.add_cascade(label='도구', menu=toolsMenu)

    aboutMenu = Menu(menubar, tearoff=0)
    aboutMenu.add_command(label='GitHub 방문', command=OpenDevSite)
    aboutMenu.add_command(label='이 디아블로 런처에 관하여...', command=AboutThisApp, accelerator='F1')
    menubar.add_cascade(label='정보', menu=aboutMenu)

    debugMenu = Menu(menubar, tearoff=0)
    debugMenu.add_command(label='버그 신고...', command=OpenDevIssues)
    menubar.add_cascade(label='개발자', menu=debugMenu)

    root.bind_all("<F5>", ForceReload)
    root.bind_all("<F1>", AboutThisApp)

    UpdateResProgram()
    GetEnvironmentValue()
    RequirementCheck()

    welcome = Label(root, text='')
    switchButton = Button(root, text='디아블로 실행...', command=LaunchGameAgent)
    emergencyButton = Button(root, text='긴급 전원 작업 (게임 저장 후 실행 요망)', height=2,command=EmgergencyReboot)
    now = datetime.now()
    cnt_time = now.strftime("%H:%M:%S")
    if data is None:
        status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: 아니요\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L > NUL 2>&1') != 0 else '예'}\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음 \n게임 디렉토리: 알 수 없음\n디렉토리 존재여부: 아니요\n디아블로 실행: 알 수 없음\n실행가능 버전: 없음\n")
        switchButton['state'] = "disabled"
    else:
        if resolutionProgram:
            if os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 예\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II, III\n")
            elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
                status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 예\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II\n")
            elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 예\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: III\n")
            else:
                status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 예\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n")
        else:
            if os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n\n\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II, III\n")
            elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
                status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n\n\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II\n")
            elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n\n\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: III\n")
            else:
                status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n\n\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n")
        switchButton['state'] = "normal"
    if os.path.isfile('C:/Program Files/Boot Camp/Bootcamp.exe'):
        info = Label(root, text='도움말\n디아블로를 원할히 플레이하려면 DiabloLauncher 환경 변수를 설정해 주세요.\n게임 디렉토리, 해상도를 변경하려면 DiabloLauncher 환경변수를 편집하세요.\nBootCamp 사운드 장치가 작동하지 않을 경우 소리 문제 해결 메뉴를 확인해 보세요.')
    else:
        info = Label(root, text='도움말\n디아블로를 원할히 플레이하려면 DiabloLauncher 환경 변수를 설정해 주세요.\n게임 디렉토리, 해상도를 변경하려면 DiabloLauncher 환경변수를 편집하세요.\n최신 드라이버 및 소프트웨어를 설치할 경우 게임 퍼포먼스가 향상됩니다.')
    notice = Label(root, text=f"Blizzard 정책상 게임 실행은 직접 실행하여야 하며 실행시 알림창 지시를 따르시기 바랍니다.\n해당 프로그램을 사용함으로써 발생하는 모든 불이익은 전적으로 사용자에게 있습니다.\n지원되는 디아블로 버전은 Diablo II Resurrected, Diablo III 입니다.")

    statusbar = Label(root, text=f'Initializing...', bd=1, relief=tkinter.SUNKEN)

    welcome.pack()
    switchButton.pack()
    emergencyButton.pack(pady=4)
    status.pack()
    info.pack()
    notice.pack()
    statusbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

    ReloadStatusBar()

    root.config(menu=menubar)

    root.mainloop()

if __name__ == '__main__':
    os.system('chcp 65001 > NUL')
    logformat(errorLevel.INFO, f'Active code page: UTF-8 (0xfde9)')
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)

    mainThread = multiprocessing.Process(target=init)
    updateThread = multiprocessing.Process(target=UpdateProgram)

    mainThread.start()
    updateThread.start()

    mainThread.join()
    updateThread.join()

