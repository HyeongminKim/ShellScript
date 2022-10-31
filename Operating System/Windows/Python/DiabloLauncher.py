#-*- coding:utf-8 -*-

import platform
import os
import sys
import signal
import subprocess

if platform.system() != 'Windows':
    print(f'{platform.system()} system does not support yet.')
    exit(1)
else:
    if platform.release() == '7' or platform.release() == '8' or platform.release() == '10' or platform.release() == '11':
        print ('support system detected. creating GUI')
    else:
        print (f'{platform.system()} {platform.release()} does not support. Please check Diablo Requirements and Specifications.')
        exit(1)

from datetime import datetime
import time

from tkinter import *
import tkinter.messagebox

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

root = Tk()
root.title('디아블로 런처')
root.geometry("520x480+100+100")
root.resizable(False, False)
root.attributes('-toolwindow', True)
launch = Tk()
launch.geometry("300x125+200+200")
launch.resizable(False, False)
launch.attributes('-toolwindow', True)
root.after(1, lambda: root.focus_force())

local = os.popen('git rev-parse HEAD')
if os.system('git pull --rebase origin master | findstr DiabloLauncher') == 0:
    remote = os.popen('git rev-parse HEAD')
    if local != remote:
        os.system('python DiabloLauncher.py &')
        exit(0)

def ShowWindow():
    launch.after(1, lambda: launch.focus_force())

def HideWindow():
    root.after(1, lambda: root.focus_force())
    for widget in launch.winfo_children():
        widget.destroy()

def AlertWindow():
    msg_box = tkinter.messagebox.askquestion('디아블로 런처', f'현재 디스플레이 해상도가 {alteredX}x{alteredY} 로 조정되어 있습니다. 게임이 실행 중인 상태에서 해상도 설정을 복구할 경우 퍼포먼스에 영향을 미칠 수 있습니다. 그래도 해상도 설정을 복구하시겠습니까?', icon='question')
    if msg_box == 'yes':
        LaunchGameAgent()
        ExitProgram()
    else:
        tkinter.messagebox.showwarning('디아블로 런처', '해상도가 조절된 상태에서는 런처를 종료할 수 없습니다. 먼저 해상도를 기본 설정으로 변경해 주시기 바랍니다.')

def ExitProgram():
    launch.destroy()
    root.destroy()
    exit(0)

def InterruptProgram(sig, frame):
    print('^C Keyboard Interrupt')
    launch.destroy()
    root.destroy()
    exit(0)

launch.protocol("WM_DELETE_WINDOW", HideWindow)
root.protocol("WM_DELETE_WINDOW", ExitProgram)
signal.signal(signal.SIGINT, InterruptProgram)

def DiabloII_Launcher():
    global diabloExecuted
    global launch
    global gameStart
    diabloExecuted = True
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
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
        root.protocol("WM_DELETE_WINDOW", ExitProgram)
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
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
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
        if os.path.isfile('C:/Windows/System32/QRes.exe'):
            gamePath, originX, originY, originFR, alteredX, alteredY, alteredFR, temp = data.split(';')
        else:
            gamePath, temp = data.split(';')

        if os.path.isfile('C:/Windows/System32/QRes.exe'):
            print(int(originX))
            print(int(originY))
            print(float(originFR))
            print(int(alteredX))
            print(int(alteredY))
            print(float(alteredFR))
    except Exception as error:
        tkinter.messagebox.showerror('디아블로 런처', f'환경변수 파싱중 예외가 발생하였습니다. 필수 파라미터가 누락되지 않았는지, 또는 잘못된 타입을 제공하지 않았는지 확인하시기 바랍니다. Exception code: {error}')
        data = None

def SetEnvironmentValue():
    global data
    tkinter.messagebox.showinfo('환경변수 편집기', '이 편집기는 본 프로그램에서만 적용되며 디아블로 런처를 종료 시 모든 변경사항이 유실됩니다. 변경사항을 영구적으로 적용하시려면 "고급 시스템 설정"을 이용해 주세요. "고급 시스템 설정"에 접근 시 관리자 권한을 요청하는 프롬프트가 나타날 수 있습니다. ')
    envWindow = Tk()
    envWindow.title('환경변수 편집기')
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
        envWindow.geometry("320x170+200+200")
    else:
        envWindow.geometry("320x50+200+200")
    envWindow.resizable(False, False)
    envWindow.attributes('-toolwindow', True)

    envGameDir = tkinter.Entry(envWindow, width=50)
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
        envOriginX = tkinter.Entry(envWindow, width=50)
        envOriginY = tkinter.Entry(envWindow, width=50)
        envOriginFR = tkinter.Entry(envWindow, width=50)
        envAlteredX = tkinter.Entry(envWindow, width=50)
        envAlteredY = tkinter.Entry(envWindow, width=50)
        envAlteredFR = tkinter.Entry(envWindow, width=50)

    envGameDir.pack()
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
        envOriginX.pack()
        envOriginY.pack()
        envOriginFR.pack()
        envAlteredX.pack()
        envAlteredY.pack()
        envAlteredFR.pack()

    if data is not None:
        envGameDir.insert(0, gamePath)
        if os.path.isfile('C:/Windows/System32/QRes.exe'):
            envOriginX.insert(0, originX)
            envOriginY.insert(0, originY)
            envOriginFR.insert(0, originFR)
            envAlteredX.insert(0, alteredX)
            envAlteredY.insert(0, alteredY)
            envAlteredFR.insert(0, alteredFR)
    else:
        envGameDir.insert(0, 'C:\Program Files (x86)')

    def commit():
        if os.path.isfile('C:/Windows/System32/QRes.exe'):
            if envGameDir.get() == '' and envOriginX.get() == '' and envOriginY.get() == '' and envOriginFR.get() == '' and envAlteredX.get() == '' and envAlteredY.get() == '' and envAlteredFR.get() == '':
                tkinter.messagebox.showwarning('환경변수 편집기', '일부 환경변수가 누락되었습니다.')
                envWindow.after(1, lambda: envWindow.focus_force())
                return
            else:
                os.environ['DiabloLauncher'] = f'{envGameDir.get().replace(";", "")};{envOriginX.get().replace(";", "")};{envOriginY.get().replace(";", "")};{envOriginFR.get().replace(";", "")};{envAlteredX.get().replace(";", "")};{envAlteredY.get().replace(";", "")};{envAlteredFR.get().replace(";", "")};'
        else:
            if envGameDir.get() == '':
                tkinter.messagebox.showwarning('환경변수 편집기', '게임 디렉토리 환경변수가 누락되었습니다.')
                envWindow.after(1, lambda: envWindow.focus_force())
                return
            else:
                os.environ['DiabloLauncher'] = f'{envGameDir.get().replace(";", "")};'

        UpdateStatusValue()
        if data is not None and not os.path.isdir(gamePath):
            tkinter.messagebox.showwarning('환경변수 편집기', f'{gamePath} 디렉토리가 존재하지 않습니다.')
            envWindow.after(1, lambda: envWindow.focus_force())
        elif data is not None and os.path.isdir(gamePath):
            if not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                tkinter.messagebox.showwarning('환경변수 편집기', f'{gamePath} 디렉토리에는 적합한 게임이 존재하지 않습니다.')
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
        msg_box = tkinter.messagebox.askquestion('디아블로 런처', '해상도를 변경하려면 QRes를 먼저 설치하여야 합니다. 지금 QRes를 다운로드 하시겠습니까?', icon='question')
        if msg_box == 'yes':
            os.system('explorer https://www.softpedia.com/get/Multimedia/Video/Other-VIDEO-Tools/QRes.shtml')

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
        status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: 아니요\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음 \n게임 디렉토리: 알 수 없음\n디렉토리 존재여부: 아니요\n디아블로 실행: 알 수 없음\n실행가능 버전: 없음\n"
        switchButton['state'] = "disabled"
    else:
        if os.path.isfile('C:/Windows/System32/QRes.exe'):
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
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II, III\n"
            elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II\n"
            elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: III\n"
            else:
                status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n"
        switchButton['state'] = "normal"


GetEnvironmentValue()
RequirementCheck()

welcome = Label(root, text='')
switchButton = Button(root, text='디아블로 실행...', command=LaunchGameAgent)
emergencyButton = Button(root, text='긴급 전원 작업 (게임 저장 후 실행 요망)', command=EmgergencyReboot)
now = datetime.now()
cnt_time = now.strftime("%H:%M:%S")
if data is None:
    status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: 아니요\n해상도 변경 지원됨: {'아니요' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음 \n게임 디렉토리: 알 수 없음\n디렉토리 존재여부: 아니요\n디아블로 실행: 알 수 없음\n실행가능 버전: 없음\n")
    switchButton['state'] = "disabled"
else:
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
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
            status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II, III\n")
        elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
            status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: II\n")
        elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
            status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n해상도 벡터: 알 수 없음\n현재 해상도: 알 수 없음\n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: III\n")
        else:
            status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니요'}\n해상도 변경 지원됨: 아니요\n해상도 벡터: 알 수 없음\n현재 해상도: \n게임 디렉토리: {f'{gamePath}' if data is not None else '알 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니요'}\n디아블로 실행: {'예' if diabloExecuted else '아니요'}\n실행가능 버전: 없음\n")
    switchButton['state'] = "normal"
refreshBtn = Button(root, text='환경변수 편집', command=SetEnvironmentValue)
info = Label(root, text='\n도움말\n디아블로를 원할히 플레이하려면 DiabloLauncher 환경 변수를 설정해 주세요.\n게임 디렉토리, 해상도를 변경하려면 DiabloLauncher 환경변수를 편집하세요.\nBootCamp 사운드가 작동하지 않을 경우 macOS로 시동하여 문제를 해결하세요.')
notice = Label(root, text=f"Blizzard 정책상 게임 실행은 직접 실행하여야 하며 실행시 알림창 지시를 따르시기 바랍니다.\n해당 프로그램을 사용함으로써 발생하는 모든 불이익은 전적으로 사용자에게 있습니다.\n지원되는 디아블로 버전은 Diablo II Resurrected, Diablo III 입니다.\n\n이 디아블로 런처에 관하여\n{subprocess.check_output('python --version', shell=True, encoding='utf-8').strip()}, {subprocess.check_output('git --version', shell=True, encoding='utf-8').strip()}, git repo-rev {subprocess.check_output('git rev-parse --short HEAD', shell=True, encoding='utf-8').strip()}\n(c) 2022 BLIZZARD ENTERTAINMENT, INC. ALL RIGHTS RESERVED.\nCopyright (c) 2022 Hyeongmin Kim")

welcome.pack()
switchButton.pack()
emergencyButton.pack()
status.pack()
refreshBtn.pack()
info.pack()
notice.pack()

root.mainloop()

