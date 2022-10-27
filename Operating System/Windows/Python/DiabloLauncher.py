#-*- coding:utf-8 -*-

from tkinter import *
from datetime import datetime
import tkinter.messagebox
import os

diabloExecuted = False
forceReboot = False
rebootWaitTime = 10

data = None
now = datetime.now()
cnt_time = now.strftime("%H:%M:%S")
gamePath = None
originX = None
originY = None
alteredX = None
alteredY = None

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
    diabloExecuted = True
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
        switchButton['text'] = '디스플레이 해상도 복구 (게임 종료시 사용)'
        os.system(f'QRes -X {alteredX} -Y {alteredY} -R 60')
    else:
        switchButton['text'] = '게임 종료'
    os.system(f'"{gamePath}/Diablo II Resurrected/Diablo II Resurrected Launcher.exe" &')
    refreshBtn['state'] = "disabled"
    HideWindow()
    UpdateStatusValue()

def DiabloIII_Launcher():
    global diabloExecuted
    global launch
    diabloExecuted = True
    if os.path.isfile('C:/Windows/System32/QRes.exe'):
        switchButton['text'] = '디스플레이 해상도 복구 (게임 종료시 사용)'
        os.system(f'QRes -X {alteredX} -Y {alteredY} -R 60')
    else:
        switchButton['text'] = '게임 종료'
    os.system(f'"{gamePath}/Diablo III/Diablo III Launcher.exe" &')
    refreshBtn['state'] = "disabled"
    HideWindow()
    UpdateStatusValue()

def LaunchGameAgent():
    global diabloExecuted
    global launch
    if diabloExecuted:
        diabloExecuted = False
        switchButton['text'] = '디아블로 실행...'
        if os.path.isfile('C:/Windows/System32/QRes.exe'):
            os.system(f'QRes -X {originX} -Y {originY} -R 60')
        refreshBtn['state'] = "normal"
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

def EmgergencyReboot():
    global forceReboot
    if forceReboot:
        forceReboot = False
        emergencyButton['text'] = '긴급 재시동 (게임 저장 후 실행 요망)'
        switchButton['state'] = "normal"
        refreshBtn['state'] = "normal"
        os.system(f'shutdown -a')
    else:
        forceReboot = True
        emergencyButton['text'] = '긴급 재시동 준비중... (재시동 취소)'
        if os.path.isfile('C:/Windows/System32/QRes.exe'):
            os.system(f'QRes -X {originX} -Y {originY} -R 60')
        UpdateStatusValue()
        os.system(f'shutdown -r -f -t 10 -c "Windows가 DiabloLauncher의 [긴급 재시동] 기능으로 인해 재시동 됩니다."')
        switchButton['state'] = "disabled"
        refreshBtn['state'] = "disabled"


def GetEnvironmentValue():
    global data
    global gamePath
    global originX
    global originY
    global alteredX
    global alteredY

    try:
        data = os.environ.get('DiabloLauncher')
        print(data)
        temp = None
        gamePath, originX, originY, alteredX, alteredY, temp = data.split(';')
    except:
        data = None

def SetEnvironmentValue():
    global data
    tkinter.messagebox.showinfo('환경변수 편집기', '이 편집기는 본 프로그램에서만 영향을 줍니다.')
    envWindow = Tk()
    envWindow.title('환경변수 편집기')
    envWindow.geometry("320x50+200+200")
    envWindow.resizable(False, False)
    envWindow.attributes('-toolwindow', True)

    envText = tkinter.Entry(envWindow, width=50)
    envText.pack()
    if data is not None:
        envText.insert(0, data)

    def commit():
        if envText.get() == '':
            tkinter.messagebox.showwarning('환경변수 편집기', '환경변수가 제공되지 않았습니다.')
            envWindow.after(1, lambda: envWindow.focus_force())
        else:
            os.environ['DiabloLauncher'] = envText.get()
            UpdateStatusValue()
            envWindow.destroy()

    commitBtn = tkinter.Button(envWindow, text='수정', command=commit)
    commitBtn.pack()

    envWindow.mainloop()

def RequirementCheck():
    if not os.path.isfile('C:/Windows/System32/QRes.exe'):
        tkinter.messagebox.showerror('디아블로 런처', 'QRes가 설치되지 않았습니다. 해상도를 변경하려면 QRes를 먼저 설치하여야 합니다.')
    if data is None:
        tkinter.messagebox.showwarning('디아블로 런처', '환경변수가 설정되어 있지 않습니다. "환경변수 편집" 버튼을 클릭하여 임시로 모든 기능을 사용해 보십시오.')


def UpdateStatusValue():
    GetEnvironmentValue()
    now = datetime.now()
    cnt_time = now.strftime("%H:%M:%S")
    if data is None:
        status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: 아니오\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: 사용할 수 없음\n현재 해상도: 사용할 수 없음 \n게임 디렉토리: 사용할 수 없음\n디렉토리 존재여부: 아니오\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: 없음\n"
        switchButton['state'] = "disabled"
    else:
        if os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
            status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '사용할 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '사용할 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: II, III\n"
        elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
            status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '사용할 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '사용할 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: II\n"
        elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
            status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '사용할 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '사용할 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: III\n"
        else:
            status['text'] = f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '사용할 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '사용할 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: 없음\n"
        switchButton['state'] = "normal"


GetEnvironmentValue()
RequirementCheck()

welcome = Label(root, text='')
switchButton = Button(root, text='디아블로 실행...', command=LaunchGameAgent)
emergencyButton = Button(root, text='긴급 재시동 (게임 저장 후 실행 요망)', command=EmgergencyReboot)
now = datetime.now()
cnt_time = now.strftime("%H:%M:%S")
if data is None:
    status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: 아니오\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: 사용할 수 없음\n현재 해상도: 사용할 수 없음 \n게임 디렉토리: 사용할 수 없음\n디렉토리 존재여부: 아니오\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: 없음\n")
    switchButton['state'] = "disabled"
else:
    if os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
        status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '사용할 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '사용할 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: II, III\n")
    elif os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe'):
        status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '사용할 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '사용할 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: II\n")
    elif os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
        status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '사용할 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '사용할 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: III\n")
    else:
        status = Label(root, text=f"\n정보 - {cnt_time}에 업데이트\n환경변수 설정됨: {'예' if data is not None else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('QRes -L') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data is not None else '사용할 수 없음'}\n현재 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {f'{gamePath}' if data is not None else '사용할 수 없음'}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) and data is not None else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else '아니오'}\n실행가능 버전: 없음\n")
    switchButton['state'] = "normal"
refreshBtn = Button(root, text='환경변수 편집', command=SetEnvironmentValue)
info = Label(root, text='\n도움말\n디아블로를 원할히 플레이하려면 DiabloLauncher 환경 변수를 설정해 주세요.\n게임 디렉토리, 해상도를 변경하려면 DiabloLauncher 환경변수를 편집하세요.\n긴급 재시동은 해상도를 복구한 후 시스템을 재시동합니다.')
notice = Label(root, text='Blizzard 정책상 게임 실행은 직접 실행하여야 하며 실행시 알림창 지시를 따르시기 바랍니다.\n해당 프로그램을 사용함으로써 발생하는 모든 불이익은 전적으로 사용자에게 있습니다.\n지원되는 디아블로 버전은 Diablo II Resurrected, Diablo III 입니다.\n그 외 버전 또는 게임은 호환이 되지 않을 수 있습니다.\n\n이 디아블로 런처에 관하여\n디아블로 게임 및 런처: (c) 2022 BLIZZARD ENTERTAINMENT, INC. ALL RIGHTS RESERVED.\n본 프로그램: Copyright (c) 2022 Hyeongmin Kim')

welcome.pack()
switchButton.pack()
emergencyButton.pack()
status.pack()
refreshBtn.pack()
info.pack()
notice.pack()

root.mainloop()

