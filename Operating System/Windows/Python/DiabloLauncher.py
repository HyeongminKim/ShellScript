#-*- coding:utf-8 -*-

try:
    import platform

    if platform.system() != 'Windows':
        print(f'\033[31m[ERR] {platform.system()} system does not support yet.\033[m')
        exit(1)
    else:
        if platform.release() == '7' or platform.release() == '8' or platform.release() == '10' or platform.release() == '11':
            print('[INFO] support OS detected.')
        else:
            print(f'\033[31m[ERR] {platform.system()} {platform.release()} does not support. Please check Diablo Requirements and Specifications.\033[m')
            exit(1)

    import multiprocessing
    import sys

    if multiprocessing.cpu_count() >= 2 and sys.maxsize > 2**32:
        print(f'[INFO] supported {platform.processor()} CPU detected. creating GUI...')
    else:
        print(f"\033[31m[ERR] {platform.processor()} CPU does not support (core: {multiprocessing.cpu_count()}, {'x64' if sys.maxsize > 2**32 else 'x86'}).")
        print('Please check Diablo Requirements and Specifications.\033[m')
        exit(1)

    import os
    import signal
    import subprocess
    import logging

    from datetime import datetime
    import time

    from tkinter import *
    import tkinter.messagebox
    import tkinter.filedialog
except Exception as error:
    print(f'The DiabloLauncher stoped due to {error}')
    exit(1)

diabloExecuted = False

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

root = Tk()
root.withdraw()
launch = Tk()
launch.withdraw()

switchButton = None
emergencyButton = None
status = None
refreshBtn = None

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
    print('[INFO] QRes install check')
    if os.path.isfile('C:/Windows/System32/Qres.exe') or os.path.isfile(f'{userLocalApp}/Program/Common/QRes.exe)'):
        print(f"[INFO] QRes installed in {subprocess.check_output('where QRes', shell=True, encoding='utf-8').strip()}")
        resolutionProgram = True
    else:
        print('[INFO] QRes did not installed')

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
    print('^C Keyboard Interrupt')
    if diabloExecuted:
        LaunchGameAgent()
    ExitProgram()

def UpdateProgram():
    global root
    global launch
    local = os.popen('git rev-parse HEAD').read().strip()
    print('[INFO] Checking program updates...')
    if os.system('git pull --rebase origin master 2> NUL | findstr DiabloLauncher > NUL 2>&1') == 0:
        remote = os.popen('git rev-parse HEAD').read().strip()
        if local != remote:
            msg_box = tkinter.messagebox.askquestion('디아블로 런처', f'디아블로 런처가 성공적으로 업데이트 되었습니다. ({local} → {remote}) 지금 런처를 다시 시작하여 업데이트를 적용하시겠습니까?', icon='question')
            if msg_box == 'yes':
                print('[INFO] Launching new version DiabloLauncher...')
                os.popen('python DiabloLauncher.py')
                print('[INFO] Successfully updated. DiabloLauncher now exiting...')
                os.popen(f'taskkill /T /PID {os.getppid()}')
            else:
                print('[INFO] Please restart DiabloLauncher to apply any updates...')
                exit(2)
        else:
            print('[INFO] DiabloLauncher Up to date.')
            exit(0)
    elif os.system('ping -n 1 -w 1 www.google.com > NUL 2>&1') != 0:
        tkinter.messagebox.showwarning('디아블로 런처', '인터넷 연결이 오프라인인 상태에서는 디아블로 런처를 업데이트 할 수 없습니다. 나중에 다시 시도해 주세요.')
        print('\033[31m[ERR] Program update failed. Please check your internet connection.\033[m')
        exit(1)
    elif os.system('git pull --rebase origin master > NUL 2>&1') != 0:
        os.system('git status')
        tkinter.messagebox.showwarning('디아블로 런처', '레포에 알 수 없는 오류가 발생하였습니다. 자세한 사항은 로그를 참조해 주세요. ')
        print('\033[31m[ERR] Program update failed. Please see the output.\033[m')
        exit(1)
    else:
        print('[INFO] DiabloLauncher Up to date')
        exit(0)

def ConvertTime(milliseconds: float):
    elapsedTime = milliseconds

    hours = int(elapsedTime / 3600)
    elapsedTime = elapsedTime % 3600
    minutes = int(elapsedTime / 60)
    elapsedTime = elapsedTime % 60
    seconds = int(elapsedTime)

    return hours, minutes, seconds

def SaveGameRunningTime(playTime: float):
    runtimeFile = None
    try:
        if not os.path.isfile(f'{userApp}/DiabloLauncher/runtime.log'):
            if not os.path.isdir(f'{userApp}/DiabloLauncher'):
                print(f'[INFO] DiabloLauncher directory does not exist. creating directory')
                os.mkdir(f'{userApp}/DiabloLauncher')
            print(f'[INFO] runtime.log file does not exist. creating target file with write mode')
            runtimeFile = open(f'{userApp}/DiabloLauncher/runtime.log', 'w')
        else:
            print(f'[INFO] runtime.log file already exist. opening target file with append mode')
            runtimeFile = open(f'{userApp}/DiabloLauncher/runtime.log', 'a')
        print(f'[INFO] playTime: {playTime} will be write in {userApp}/DiabloLauncher/runtime.log')
        runtimeFile.write(f'{str(playTime)}\n')
    except Exception as error:
        print(f'\033[31m[ERR] Failed to save Game-play logs: {error}\033[m')
    finally:
        runtimeFile.close()

def LoadGameRunningTime():
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
                print(f'[INFO] {line}')
                data.append(line)
            for line in data:
                print(f'[INFO] {float(line)}')
                if max < float(line):
                    max = float(line)
                sum += float(line)
        else:
            raise FileNotFoundError
    except Exception as error:
        print(f'\033[31m[ERR] Failed to load Game-play logs: {error}\033[m')
    finally:
        runtimeFile.close()
        if data is not None and sum != 0:
            return len(data), max, sum, (sum / len(data))

def DiabloII_Launcher():
    global diabloExecuted
    global root
    global launch
    global gameStart
    global switchButton
    global refreshBtn
    diabloExecuted = True
    if resolutionProgram:
        if int(alteredX) < 1280 or int(alteredY) < 720:
            tkinter.messagebox.showerror('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 Diablo II Resurrected 가 지원하지 않습니다. 자세한 사항은 공식 홈페이지를 확인하시기 바랍니다. ')
            diabloExecuted = False
            root.protocol("WM_DELETE_WINDOW", ExitProgram)
            HideWindow()
            UpdateStatusValue()
            return
        if platform.release() != '10' and platform.release() != '11':
            tkinter.messagebox.showerror('디아블로 런처', f'{platform.system()} {platform.release()} 은(는) Diablo II Resurrected 가 지원하지 않습니다. 자세한 사항은 공식 홈페이지를 확인하시기 바랍니다. ')
            diabloExecuted = False
            root.protocol("WM_DELETE_WINDOW", ExitProgram)
            HideWindow()
            UpdateStatusValue()
            return
        if os.system(f'QRes -X {alteredX} -Y {alteredY} -R {alteredFR}') != 0:
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
    os.popen(f'"{gamePath}/Diablo II Resurrected/Diablo II Resurrected Launcher.exe"')
    refreshBtn['state'] = "disabled"
    gameStart = time.time()
    HideWindow()
    UpdateStatusValue()

def DiabloIII_Launcher():
    global diabloExecuted
    global root
    global launch
    global gameStart
    global switchButton
    global refreshBtn
    diabloExecuted = True
    if resolutionProgram:
        if int(alteredX) < 1024 or int(alteredY) < 768:
            tkinter.messagebox.showerror('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 Diablo III 가 지원하지 않습니다. 자세한 사항은 공식 홈페이지를 확인하시기 바랍니다. ')
            diabloExecuted = False
            root.protocol("WM_DELETE_WINDOW", ExitProgram)
            HideWindow()
            UpdateStatusValue()
            return
        if platform.release() != '7' and platform.release() != '8' and platform.release() != '10' and platform.release() != '11':
            tkinter.messagebox.showerror('디아블로 런처', f'{platform.system()} {platform.release()} 은(는) Diablo III 가 지원하지 않습니다. 자세한 사항은 공식 홈페이지를 확인하시기 바랍니다. ')
            diabloExecuted = False
            root.protocol("WM_DELETE_WINDOW", ExitProgram)
            HideWindow()
            UpdateStatusValue()
            return
        if os.system(f'QRes -X {alteredX} -Y {alteredY} -R {alteredFR}') != 0:
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
    os.popen(f'"{gamePath}/Diablo III/Diablo III Launcher.exe"')
    refreshBtn['state'] = "disabled"
    gameStart = time.time()
    HideWindow()
    UpdateStatusValue()

def LaunchGameAgent():
    global diabloExecuted
    global root
    global launch
    global switchButton
    global refreshBtn
    global gameEnd
    if diabloExecuted:
        diabloExecuted = False
        root.protocol("WM_DELETE_WINDOW", ExitProgram)
        gameEnd = time.time()
        switchButton['text'] = '디아블로 실행...'
        if resolutionProgram:
            if os.system(f'QRes -X {originX} -Y {originY} -R {originFR}') != 0:
                tkinter.messagebox.showwarning('디아블로 런처', f'{originX}x{originY} {originFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
        refreshBtn['state'] = "normal"

        SaveGameRunningTime(gameEnd - gameStart)
        loadStart = time.time()
        count, max, sum, avg = LoadGameRunningTime()
        hours, minutes, seconds = ConvertTime(gameEnd - gameStart)
        maxHours, maxMinutes, maxSeconds = ConvertTime(max)
        avgHours, avgMinutes, avgSeconds = ConvertTime(avg)
        sumHours, sumMinutes, sumSeconds = ConvertTime(sum)
        loadEnd = time.time()

        elapsedTime = loadEnd - loadStart
        if elapsedTime > loadWaitTime:
            print(f'\033[33m[WARN] The request timeout when loading game data {userApp}/DiabloLauncher/runtime.log file.\033[m')
            print(f'[INFO] Loading game data elapsed time was {elapsedTime} seconds. But, current timeout setting is {loadWaitTime} seconds.')
            print(f'[INFO] NOTE: The {userApp}/DiabloLauncher/runtime.log contents cleared.')
            if os.remove(f'{userApp}/DiabloLauncher/runtime.log') == 0:
                print(f'[INFO] The {userApp}/DiabloLauncher/runtime.log file successfully deleted.')
            else:
                print(f'\033[31m[ERR] Failed to remove {userApp}/DiabloLauncher/runtime.log file. Please delete it manually.\033[m')
        elif elapsedTime > (loadWaitTime / 2):
            print(f'\033[33m[WARN] The request job too slow when loading game data {userApp}/DiabloLauncher/runtime.log file.\033[m')
            print(f'[INFO] Loading game data elapsed time was {elapsedTime} seconds, and current timeout setting is {loadWaitTime} seconds.')
            print(f'[INFO] NOTE: {userApp}/DiabloLauncher/runtime.log contents will clear when this issues raised again.')
        else:
            print(f'[INFO] Loading game data elapsed time was {elapsedTime} seconds. ')

        print(f'[INFO] Running game time for this session: {hours}:{minutes}.{seconds}')
        print(f'[INFO] Previous game time for max session: {maxHours}:{maxMinutes}.{maxSeconds}')
        print(f'[INFO] Previous game time for avg session: {avgHours}:{avgMinutes}.{avgSeconds}')
        print(f'[INFO] Previous game time for sum session: {sumHours}:{sumMinutes}.{sumSeconds}')
        if count >= 3:
            if hours > 0:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 게임플레이 시간은 {hours}시간 {minutes}분 {seconds}초 입니다.\n통계 작성 후 {count}번의 플레이 중, 최대 {maxHours}시간 {maxMinutes}분 {maxSeconds}초 플레이 하였고, 평균 {avgHours}시간 {avgMinutes}분 {avgSeconds}초 플레이 하였습니다. 총 플레이 시간은 {sumHours}시간 {sumMinutes}분 {sumSeconds}초 입니다.')
            elif minutes >= 5:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 게임플레이 시간은 {minutes}분 {seconds}초 입니다.\n통계 작성 후 {count}번의 플레이 중, 최대 {maxHours}시간 {maxMinutes}분 {maxSeconds}초 플레이 하였고, 평균 {avgHours}시간 {avgMinutes}분 {avgSeconds}초 플레이 하였습니다. 총 플레이 시간은 {sumHours}시간 {sumMinutes}분 {sumSeconds}초 입니다. ')
        else:
            if hours > 0:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 게임플레이 시간은 {hours}시간 {minutes}분 {seconds}초 입니다.\n통계를 표시하려면 좀 더 많은 기록이 있어야 합니다.')
            elif minutes >= 5:
                tkinter.messagebox.showinfo('디아블로 런처', f'이번 게임플레이 시간은 {minutes}분 {seconds}초 입니다.\n통계를 표시하려면 좀 더 많은 기록이 있어야 합니다.')
        UpdateStatusValue()
    else:
        launch.title('디아블로 버전 선택')

        note = Label(launch, text='사용가능한 디아블로 버전만 활성화 됩니다')
        diablo2 = Button(launch, text='Diablo II Resurrected', width=20, height=5, command=DiabloII_Launcher)
        diablo3 = Button(launch, text='Diablo III', width=20, height=5, command=DiabloIII_Launcher)
        note.pack()
        diablo2.pack(side=LEFT, padx=10)
        diablo3.pack(side=RIGHT, padx=10)
        if not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
            diablo2['state'] = "disabled"
        else:
            diablo2['state'] = "normal"

        if not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
            diablo3['state'] = "disabled"
        else:
            diablo3['state'] = "normal"

        ShowWindow()
        launch.mainloop()

def RebootAgent():
    global forceReboot
    global emergencyButton
    global switchButton
    global refreshBtn
    global gameEnd
    SaveGameRunningTime(gameEnd - gameStart)
    forceReboot = True
    gameEnd = time.time()
    emergencyButton['text'] = '긴급 재시동 준비중... (재시동 취소)'
    if resolutionProgram:
        if os.system(f'QRes -X {originX} -Y {originY} -R {originFR}') != 0:
            tkinter.messagebox.showwarning('디아블로 런처', f'{originX}x{originY} {originFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
    HideWindow()
    UpdateStatusValue()
    os.system(f'shutdown -r -f -t 10 -c "Windows가 DiabloLauncher의 [긴급 재시동] 기능으로 인해 재시동 됩니다."')
    switchButton['state'] = "disabled"
    refreshBtn['state'] = "disabled"

def HaltAgent():
    global forceReboot
    global emergencyButton
    global switchButton
    global refreshBtn
    global gameEnd
    SaveGameRunningTime(gameEnd - gameStart)
    forceReboot = True
    emergencyButton['text'] = '긴급 종료 준비중... (종료 취소)'
    if resolutionProgram:
        if os.system(f'QRes -X {originX} -Y {originY} -R {originFR}') != 0:
            tkinter.messagebox.showwarning('디아블로 런처', f'{originX}x{originY} {originFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
    HideWindow()
    UpdateStatusValue()
    os.system(f'shutdown -s -f -t 10 -c "Windows가 DiabloLauncher의 [긴급 종료] 기능으로 인해 종료 됩니다."')
    switchButton['state'] = "disabled"
    refreshBtn['state'] = "disabled"


def EmgergencyReboot():
    global launch
    global forceReboot
    global emergencyButton
    global switchButton
    global refreshBtn
    if forceReboot:
        forceReboot = False
        emergencyButton['text'] = '긴급 전원 작업 (게임 저장 후 실행 요망)'
        switchButton['state'] = "normal"
        refreshBtn['state'] = "normal"
        os.system(f'shutdown -a')
    else:
        launch.title('전원')
        if resolutionProgram and diabloExecuted:
            note = Label(launch, text=f'수행할 작업 시작전 {originX}x{originY} 해상도로 복구 후 계속')
        else:
            note = Label(launch, text='수행할 작업 선택')
        reboot = Button(launch, text='재시동', width=20, height=5, command=RebootAgent)
        halt = Button(launch, text='종료', width=20, height=5, command=HaltAgent)
        note.pack()
        reboot.pack(side=LEFT, padx=10)
        halt.pack(side=RIGHT, padx=10)
        ShowWindow()
        launch.mainloop()

def GetEnvironmentValue():
    global data
    global gamePath
    if resolutionProgram:
        global originX
        global originY
        global originFR
        global alteredX
        global alteredY
        global alteredFR

    try:
        data = os.environ.get('DiabloLauncher')
        print(f'[INFO] {data}')
        temp = None
        if resolutionProgram:
            print('[INFO] QRes detected. parameter count should be 7')
            gamePath, originX, originY, originFR, alteredX, alteredY, alteredFR, temp = data.split(';')
            print('[INFO] parameter conversion succeed')
        else:
            print('[INFO] QRes not detected. parameter count should be 1')
            gamePath, temp = data.split(';')
            print('[INFO] parameter conversion succeed')

        if resolutionProgram:
            print(f'[INFO] {gamePath}')
            print(f'[INFO] {int(originX)}')
            print(f'[INFO] {int(originY)}')
            print(f'[INFO] {float(originFR)}')
            print(f'[INFO] {int(alteredX)}')
            print(f'[INFO] {int(alteredY)}')
            print(f'[INFO] {float(alteredFR)}')
    except Exception as error:
        tkinter.messagebox.showerror('디아블로 런처', f'환경변수 파싱중 예외가 발생하였습니다. 필수 파라미터가 누락되지 않았는지, 또는 잘못된 타입을 제공하지 않았는지 확인하시기 바랍니다. Exception code: {error}')
        print(f'\033[31m[ERR] Unknown data or parameter style: {data}\n\t{error}\033[m')
        data = None
        gamePath = None
        originX = None
        originY = None
        originFR = None
        alteredX = None
        alteredY = None
        alteredFR = None
    finally:
        print(f'[INFO] {data}')
        if resolutionProgram:
            print(f'[INFO] {gamePath}')
            print(f'[INFO] {originX}')
            print(f'[INFO] {originY}')
            print(f'[INFO] {originFR}')
            print(f'[INFO] {alteredX}')
            print(f'[INFO] {alteredY}')
            print(f'[INFO] {alteredFR}')
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
        print(f'[INFO] Opening directory dialog location: {gamePath if gamePath is not None else "C:/Program Files (x86)"}')
        envGameDir = tkinter.filedialog.askdirectory(parent=envWindow, initialdir=f"{gamePath if gamePath is not None else 'C:/Program Files (x86)'}", title='Battle.net 게임 디렉토리 선택')
        if envGameDir == "":
            print(f'[INFO] Selected directory dialog location: None directory path provided. resetting {temp}')
            envGameDir = temp
        else:
            print(f'[INFO] Selected directory dialog location: {envGameDir}')

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
            print(f'[INFO] {envGameDir}')
        except NameError:
            envGameDir = gamePath
            print(f'[INFO] Selected directory dialog location: None directory path provided. resetting {envGameDir}')

        if resolutionProgram:
            if envGameDir == '' or envOriginX.get() == '' or envOriginY.get() == '' or envOriginFR.get() == '' or envAlteredX.get() == '' or envAlteredY.get() == '' or envAlteredFR.get() == '':
                tkinter.messagebox.showwarning('환경변수 편집기', '일부 환경변수가 누락되었습니다.')
                print(f'\033[33m[WARN] some env can not be None.\033[m')
                envWindow.after(1, lambda: envWindow.focus_force())
                return
            else:
                os.environ['DiabloLauncher'] = f'{envGameDir.replace(";", "")};{envOriginX.get().replace(";", "")};{envOriginY.get().replace(";", "")};{envOriginFR.get().replace(";", "")};{envAlteredX.get().replace(";", "")};{envAlteredY.get().replace(";", "")};{envAlteredFR.get().replace(";", "")};'
                print(f"[INFO] gamePath = {os.environ.get('DiabloLauncher')}")
        else:
            if envGameDir == '':
                tkinter.messagebox.showwarning('환경변수 편집기', '게임 디렉토리 환경변수가 누락되었습니다.')
                print(f'\033[33m[WARN] gamePath can not be None.\033[m')
                envWindow.after(1, lambda: envWindow.focus_force())
                return
            else:
                os.environ['DiabloLauncher'] = f'{envGameDir.replace(";", "")};'
                print(f"[INFO] gamePath = {os.environ.get('DiabloLauncher')}")

        UpdateStatusValue()
        if data is not None and not os.path.isdir(gamePath):
            tkinter.messagebox.showwarning('환경변수 편집기', f'{gamePath} 디렉토리가 존재하지 않습니다.')
            print(f'\033[33m[WARN] {gamePath} no such directory.\033[m')
            envWindow.after(1, lambda: envWindow.focus_force())
        elif data is not None and os.path.isdir(gamePath):
            if not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                tkinter.messagebox.showwarning('환경변수 편집기', f'{gamePath} 디렉토리에는 적합한 게임이 존재하지 않습니다.')
                print(f'\033[33m[WARN] {gamePath} not contains game directory.\033[m')
                envWindow.after(1, lambda: envWindow.focus_force())
            else:
                envWindow.destroy()

    def openEnvSetting():
        msg_box = tkinter.messagebox.askquestion('디아블로 런처', '"고급 시스템 설정"에 접근 시 관리자 권한을 요청하는 프롬프트가 나타날 수 있으며, 업데이트된 환경변수를 반영하기 위해 프로그램을 종료해야 합니다. 계속하시겠습니까?', icon='question')
        if msg_box == 'yes':
            print('[INFO] starting advanced system env editor...')
            print('[INFO] This action will required UAC')
            os.system('sysdm.cpl ,3')
            tkinter.messagebox.showwarning('디아블로 런처', '시스템 환경변수 수정을 모두 완료한 후 다시 실행해 주세요.')
            print('[INFO] advanced system env editor launched. DiabloLauncher now exiting...')
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
        print('\033[33m[WARN] QRes not installed or not in...\033[m')
        print('\033[33m\t- C:\\Windows\\System32\033[m')
        print(f'\033[33m\t- {userLocalApp}/Program/Common/QRes.exe\033[m')
        if os.environ.get('IGN_RES_ALERT') != 'true':
            msg_box = tkinter.messagebox.askquestion('디아블로 런처', '해상도를 변경하려면 QRes를 먼저 설치하여야 합니다. 지금 QRes를 다운로드 하시겠습니까?', icon='question')
            if msg_box == 'yes':
                os.system('explorer https://www.softpedia.com/get/Multimedia/Video/Other-VIDEO-Tools/QRes.shtml')
        else:
            print('\033[33m[WARN] QRes install check dialog rejected due to "IGN_RES_ALERT" env prameter is true.\033[m')
            print('\033[33m\t Please install QRes if would you like change display resolution.\n\tURL: \033[4;34mhttps://www.softpedia.com/get/Multimedia/Video/Other-VIDEO-Tools/QRes.shtml\033[0m')

    if data is None:
        print('\033[33m[WARN] parameter not set.\033[m')
        tkinter.messagebox.showwarning('디아블로 런처', '환경변수가 설정되어 있지 않습니다. "환경변수 편집" 버튼을 클릭하여 임시로 모든 기능을 사용해 보십시오.')
    elif data is not None and not os.path.isdir(gamePath):
        print('\033[33m[WARN] directory not exist.\033[m')
        tkinter.messagebox.showwarning('디아블로 런처', f'{gamePath} 디렉토리가 존재하지 않습니다.')
    elif not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
        print('\033[33m[WARN] game directory not exist.\033[m')
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


def init():
    global root
    global launch
    global switchButton
    global emergencyButton
    global status
    global refreshBtn
    root.title(f"디아블로 런처 (rev. {subprocess.check_output('git rev-parse --short HEAD', shell=True, encoding='utf-8').strip()})")
    root.geometry("520x480+100+100")
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

    UpdateResProgram()
    GetEnvironmentValue()
    RequirementCheck()

    welcome = Label(root, text='')
    switchButton = Button(root, text='디아블로 실행...', command=LaunchGameAgent)
    emergencyButton = Button(root, text='긴급 전원 작업 (게임 저장 후 실행 요망)', command=EmgergencyReboot)
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
    refreshBtn = Button(root, text='환경변수 편집', command=SetEnvironmentValue)
    if os.path.isfile('C:/Program Files/Boot Camp/Bootcamp.exe'):
        info = Label(root, text='\n도움말\n디아블로를 원할히 플레이하려면 DiabloLauncher 환경 변수를 설정해 주세요.\n게임 디렉토리, 해상도를 변경하려면 DiabloLauncher 환경변수를 편집하세요.\nBootCamp 사운드가 작동하지 않을 경우 macOS로 시동하여 문제를 해결하세요.')
    else:
        info = Label(root, text='\n도움말\n디아블로를 원할히 플레이하려면 DiabloLauncher 환경 변수를 설정해 주세요.\n게임 디렉토리, 해상도를 변경하려면 DiabloLauncher 환경변수를 편집하세요.\n최신 드라이버 및 소프트웨어를 설치할 경우 게임 퍼포먼스가 향상됩니다.')
    notice = Label(root, text=f"Blizzard 정책상 게임 실행은 직접 실행하여야 하며 실행시 알림창 지시를 따르시기 바랍니다.\n해당 프로그램을 사용함으로써 발생하는 모든 불이익은 전적으로 사용자에게 있습니다.\n지원되는 디아블로 버전은 Diablo II Resurrected, Diablo III 입니다.\n\n이 디아블로 런처에 관하여\n{platform.system()} {platform.release()}, Python {platform.python_version()}, {subprocess.check_output('git --version', shell=True, encoding='utf-8').strip()}\n(c) 2022 BLIZZARD ENTERTAINMENT, INC. ALL RIGHTS RESERVED.\nCopyright (c) 2022 Hyeongmin Kim")

    welcome.pack()
    switchButton.pack()
    emergencyButton.pack()
    status.pack()
    refreshBtn.pack()
    info.pack()
    notice.pack()

    root.mainloop()

if __name__ == '__main__':
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)

    mainThread = multiprocessing.Process(target=init)
    updateThread = multiprocessing.Process(target=UpdateProgram)

    mainThread.start()
    updateThread.start()

    mainThread.join()
    updateThread.join()

