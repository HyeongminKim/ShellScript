#-*- coding:utf-8 -*-

from tkinter import *
from datetime import datetime
import tkinter.messagebox
import os
import subprocess
import time

diabloExecuted = False
forceReboot = False
rebootWaitTime = 10

data = None
now = datetime.now()
gameStart = None
gameEnd = None
cnt_time = now.strftime("%H:%M:%S")
gamePath = None
originX = None
originY = None
originFR = None
alteredX = None
alteredY = None
alteredFR = None

local = os.popen('git rev-parse HEAD')
if os.system('git pull --rebase origin master | findstr DiabloLauncher') == 0:
    remote = os.popen('git rev-parse HEAD')
    if local != remote:
        print(local + ' → ' + remote)
        exit(0)

root = Tk()
root.title('디아블로 런처')
root.geometry("520x480+100+100")
root.resizable(False, False)
root.attributes('-toolwindow', True)
launch = Tk()
launch.geometry("300x125+200+200")
launch.resizable(False, False)
launch.attributes('-toolwindow', True)

def ShowWindow():
    launch.after(1, lambda: launch.focus_force())

def HideWindow():
    root.after(1, lambda: root.focus_force())
    for widget in launch.winfo_children():
        widget.destroy()

def ExitProgram():
    launch.destroy()
    root.destroy()
    exit(0)
    
launch.protocol("WM_DELETE_WINDOW", HideWindow)
root.protocol("WM_DELETE_WINDOW", ExitProgram)

def DiabloII_Launcher():
    global diabloExecuted
    global launch
    global gameStart
    diabloExecuted = True
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
        if int(alteredX) < 1280 and int(alteredY) < 720:
            tkinter.messagebox.showerror('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 Diablo II Resurrected 가 지원하지 않습니다. 자세한 사항은 공식 홈페이지를 확인하시기 바랍니다. ')
            diabloExecuted = False
            return
        switchButton['text'] = '디스플레이 해상도 복구 (게임 종료시 사용)'
        if os.system(f'QRes -X {alteredX} -Y {alteredY} -R {alteredFR}') != 0:
            tkinter.messagebox.showwarning('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')

    else:
        switchButton['text'] = '게임 종료'
    os.system(f'"{gamePath}/Diablo II Resurrected/Diablo II Resurrected Launcher.exe" &')
    refreshBtn['state'] = "disabled"
    gameStart = time.time()
    HideWindow()
    UpdateStatusValue()

def DiabloIII_Launcher():
    global diabloExecuted
    global launch
    global gameStart
    diabloExecuted = True
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
        if int(alteredX) < 1024 and int(alteredY) < 768:
            tkinter.messagebox.showerror('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 Diablo III 가 지원하지 않습니다. 자세한 사항은 공식 홈페이지를 확인하시기 바랍니다. ')
            diabloExecuted = False
            return

        switchButton['text'] = '디스플레이 해상도 복구 (게임 종료시 사용)'
        if os.system(f'QRes -X {alteredX} -Y {alteredY} -R {alteredFR}') != 0:
            tkinter.messagebox.showwarning('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
    else:
        switchButton['text'] = '게임 종료'
    os.system(f'"{gamePath}/Diablo III/Diablo III Launcher.exe" &')
    refreshBtn['state'] = "disabled"
    gameStart = time.time()
    HideWindow()
    UpdateStatusValue()

def LaunchGameAgent():
    global diabloExecuted
    global launch
    global gameEnd
    if diabloExecuted:
        diabloExecuted = False
        gameEnd = time.time()
        switchButton['text'] = '디아블로 실행...'
        if os.path.isfile('C:/Windows/System32/QRes.exe'):
            if os.system(f'QRes -X {originX} -Y {originY} -R {originFR}') != 0:
                tkinter.messagebox.showwarning('디아블로 런처', f'{originX}x{originY} {originFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
        refreshBtn['state'] = "normal"

        elapsedTime = gameEnd - gameStart
        hours = int(elapsedTime / 3600)
        elapsedTime = elapsedTime % 3600
        minutes = int(elapsedTime / 60)
        elapsedTime = elapsedTime % 60
        seconds = int(elapsedTime)

        if hours > 0:
            tkinter.messagebox.showinfo('디아블로 런처', f'이번 게임플레이 시간은 {hours}시간 {minutes}분 {seconds}초 입니다.')
        elif minutes >= 5:
            tkinter.messagebox.showinfo('디아블로 런처', f'이번 게임플레이 시간은 {minutes}분 {seconds}초 입니다.')
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
    forceReboot = True
    emergencyButton['text'] = '긴급 재시동 준비중... (재시동 취소)'
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
        if os.system(f'QRes -X {originX} -Y {originY} -R {originFR}') != 0:
            tkinter.messagebox.showwarning('디아블로 런처', f'{originX}x{originY} {originFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
    HideWindow()
    UpdateStatusValue()
    os.system(f'shutdown -r -f -t 10 -c "Windows가 DiabloLauncher의 [긴급 재시동] 기능으로 인해 재시동 됩니다."')
    switchButton['state'] = "disabled"
    refreshBtn['state'] = "disabled"

def HaltAgent():
    global forceReboot
    forceReboot = True
    emergencyButton['text'] = '긴급 종료 준비중... (종료 취소)'
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
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
    if forceReboot:
        forceReboot = False
        emergencyButton['text'] = '긴급 전원 작업 (게임 저장 후 실행 요망)'
        switchButton['state'] = "normal"
        refreshBtn['state'] = "normal"
        os.system(f'shutdown -a')
    else:
        launch.title('전원')
        if diabloExecuted and os.path.isfile('C:/Windows/System32/QRes.exe'):
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
    global originX
    global originY
    global originFR
    global alteredX
    global alteredY
    global alteredFR

    try:
        data = os.environ.get('DiabloLauncher')
        print(data)
        temp = None
        gamePath, originX, originY, originFR, alteredX, alteredY, alteredFR, temp = data.split(';')
        print(int(originX))
        print(int(originY))
        print(float(originFR))
        print(int(alteredX))
        print(int(alteredY))
        print(float(alteredFR))
    except Exception as error:
        tkinter.messagebox.showerror('디아블로 런처', f'환경변수 파싱중 예외가 발생하였습니다. 필수 파라미터가 누락되지 않았는지, 잘못된 타입을 제공하지 않았는지 확인하시기 바랍니다. Exception code: {error}')
        data = None

def SetEnvironmentValue():
    global data
    tkinter.messagebox.showinfo('환경변수 편집기', '이 편집기는 본 프로그램에서만 적용되며 디아블로 런처를 종료 시 모든 변경사항이 유실됩니다. 변경사항을 영구적으로 적용하시려면 "고급 시스템 설정"을 이용해 주세요. "고급 시스템 설정"에 접근 시 관리자 권한을 요청하는 프롬프트가 나타날 수 있습니다. ')
    envWindow = Tk()
    envWindow.title('환경변수 편집기')
    envWindow.geometry("320x170+200+200")
    envWindow.resizable(False, False)
    envWindow.attributes('-toolwindow', True)

    envGameDir = tkinter.Entry(envWindow, width=50)
    envOriginX = tkinter.Entry(envWindow, width=50)
    envOriginY = tkinter.Entry(envWindow, width=50)
    envOriginFR = tkinter.Entry(envWindow, width=50)
    envAlteredX= tkinter.Entry(envWindow, width=50)
    envAlteredY = tkinter.Entry(envWindow, width=50)
    envAlteredFR = tkinter.Entry(envWindow, width=50)

    envGameDir.pack()
    envOriginX.pack()
    envOriginY.pack()
    envOriginFR.pack()
    envAlteredX.pack()
    envAlteredY.pack()
    envAlteredFR.pack()

    if data is not None:
        envGameDir.insert(0, gamePath)
        envOriginX.insert(0, originX)
        envOriginY.insert(0, originY)
        envOriginFR.insert(0, originFR)
        envAlteredX.insert(0, alteredX)
        envAlteredY.insert(0, alteredY)
        envAlteredFR.insert(0, alteredFR)
    else:
        envGameDir.insert(0, 'C:\Program Files (x86)')

    def commit():
        if envGameDir.get() != '' and envOriginX.get() == '' and envOriginY.get() == '' and envOriginFR.get() == '' and envAlteredX.get() == '' and envAlteredY.get() == '' and envAlteredFR.get() == '':
            os.environ['DiabloLauncher'] = envGameDir.get()
            UpdateStatusValue()
            if data is not None and not os.path.isdir(gamePath):
                tkinter.messagebox.showwarning('환경변수 편집기', f'{gamePath} 디렉토리가 존재하지 않습니다.')
                envWindow.after(1, lambda: envWindow.focus_force())
            elif data is not None and os.path.isdir(gamePath):
                if not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                    tkinter.messagebox.showwarning('디아블로 런처', f'{gamePath} 디렉토리에는 적합한 게임이 존재하지 않습니다.')
                    envWindow.after(1, lambda: envWindow.focus_force())
                else:
                    envWindow.destroy()
        elif envGameDir.get() == '' or envOriginX.get() == '' or envOriginY.get() == '' or envOriginFR.get() == '' or envAlteredX.get() == '' or envAlteredY.get() == '' or envAlteredFR.get() == '':
            tkinter.messagebox.showwarning('환경변수 편집기', '일부 환경변수가 누락되었습니다.')
            envWindow.after(1, lambda: envWindow.focus_force())
        else:
            if envGameDir.get().find(';') >= 0 or envOriginX.get().find(';') >= 0 or envOriginY.get().find(';') >= 0 or envOriginFR.get().find(';') >= 0 or envAlteredX.get().find(';') >= 0 or envAlteredY.get().find(';') >= 0 or envAlteredFR.get().find(';') >= 0:
                tkinter.messagebox.showwarning('환경변수 편집기', '개행문자 ";" 가 포함되었으며 해당 문자는 모두 무시됩니다. 이 문제로 인하여 예기치 않은 디렉토리가 지정될 수 있습니다. 해당 문자는 레거시 에디터 편집방식으로 현재 버전에는 적용할 수 없습니다. 레거시 에디터를 사용하시려면 첫번째 텍스트 필드를 제외한 모든 텍스트 필드는 공란이어야 합니다.')
                os.environ['DiabloLauncher'] = f'{envGameDir.get().replace(";", "")};{envOriginX.get().replace(";", "")};{envOriginY.get().replace(";", "")};{envOriginFR.get().replace(";", "")};{envAlteredX.get().replace(";", "")};{envAlteredY.get().replace(";", "")};{envAlteredFR.get().replace(";", "")};'

            UpdateStatusValue()
            if data is not None and not os.path.isdir(gamePath):
                tkinter.messagebox.showwarning('환경변수 편집기', f'{gamePath} 디렉토리가 존재하지 않습니다.')
                envWindow.after(1, lambda: envWindow.focus_force())
            elif data is not None and os.path.isdir(gamePath):
                if not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                    tkinter.messagebox.showwarning('디아블로 런처', f'{gamePath} 디렉토리에는 적합한 게임이 존재하지 않습니다.')
                    envWindow.after(1, lambda: envWindow.focus_force())
                else:
                    envWindow.destroy()

    def openEnvSetting():
        tkinter.messagebox.showwarning('디아블로 런처', '업데이트된 환경변수를 반영하기 위해 프로그램을 종료합니다. 환경변수 편집을 모두 완료한 후 다시 실행해 주세요.')
        os.system('sysdm.cpl ,3')
        exit(0)

    envSet = tkinter.Button(envWindow, text='고급 시스템 설정', command=openEnvSetting)
    envSet.pack(side=LEFT, padx=10)

    commitBtn = tkinter.Button(envWindow, text='적용', command=commit)
    commitBtn.pack()
    commitBtn.pack(side=RIGHT, padx=10)

    envWindow.mainloop()

def RequirementCheck():
    if not os.path.isfile('C:/Windows/System32/QRes.exe'):
        tkinter.messagebox.showerror('디아블로 런처', 'QRes가 설치되지 않았습니다. 해상도를 변경하려면 QRes를 먼저 설치하여야 합니다.')
    if data is None:
        tkinter.messagebox.showwarning('디아블로 런처', '환경변수가 설정되어 있지 않습니다. "환경변수 편집" 버튼을 클릭하여 임시로 모든 기능을 사용해 보십시오.')
    elif data is not None and not os.path.isdir(gamePath):
        tkinter.messagebox.showwarning('디아블로 런처', f'{gamePath} 디렉토리가 존재하지 않습니다.')
    elif not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
        tkinter.messagebox.showwarning('디아블로 런처', f'{gamePath} 디렉토리에는 적합한 게임이 존재하지 않습니다.')

def UpdateStatusValue():
    GetEnvironmentValue()
    now = datetime.now()
    cnt_time = now.strftime("%H:%M:%S")
    if data is None:
        status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: 아니요\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음 \n게임 디렉토리: 알 수 없음\n디렉토리 존재여부: 아니요\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n"
        switchButton['state'] = "disabled"
    else:
        if os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
            status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II, III\n"
        elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
            status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II\n"
        elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
            status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: III\n"
        else:
            status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n"
        switchButton['state'] = "normal"


GetEnvironmentValue()
RequirementCheck()

welcome = Label(root, text='')
switchButton = Button(root, text='디아블로 실행...', command=LaunchGameAgent)
emergencyButton = Button(root, text='긴급 전원 작업 (게임 저장 후 실행 요망)', command=EmgergencyReboot)
now = datetime.now()
cnt_time = now.strftime("%H:%M:%S")
if data is None:
    status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: 아니요\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음 \n게임 디렉토리: 알 수 없음\n디렉토리 존재여부: 아니요\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n")
    switchButton['state'] = "disabled"
else:
    if os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
        status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II, III\n")
    elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
        status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II\n")
    elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
        status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: III\n")
    else:
        status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '알 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY} {alteredFR}Hz' if diabloExecuted else f'{originX}x{originY} {originFR}Hz'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n")
    switchButton['state'] = "normal"
refreshBtn = Button(root, text='환경변수 편집', command=SetEnvironmentValue)
info = Label(root, text='\n도움말\n디아블로를 원할히 플레이하려면 DiabloLauncher 환경 변수를 설정해 주세요.\n게임 디렉토리, 해상도를 변경하려면 DiabloLauncher 환경변수를 편집하세요.\nBootCamp 사운드가 작동하지 않을 경우 macOS로 시동하여 문제를 해결하세요.')
notice = Label(root, text=f"Blizzard 정책상 게임 실행은 직접 실행하여야 하며 실행시 알림창 지시를 따르시기 바랍니다.\n해당 프로그램을 사용함으로써 발생하는 모든 불이익은 전적으로 사용자에게 있습니다.\n지원되는 디아블로 버전은 Diablo II Resurrected, Diablo III 입니다.\n그 외 버전 또는 게임은 호환이 되지 않을 수 있습니다.\n\n이 디아블로 런처({subprocess.check_output('git rev-parse --short HEAD', shell=True, encoding='utf-8').strip()}) 에 관하여\n(c) 2022 BLIZZARD ENTERTAINMENT, INC. ALL RIGHTS RESERVED.\nCopyright (c) 2022 Hyeongmin Kim")

welcome.pack()
switchButton.pack()
emergencyButton.pack()
status.pack()
refreshBtn.pack()
info.pack()
notice.pack()

root.mainloop()

