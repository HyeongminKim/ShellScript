from tkinter import *
import tkinter.messagebox
import os
import time

diabloExecuted = False
forceReboot = False
rebootWaitTime = 10

data = None
gamePath = None
originX = None
originY = None
alteredX = None
alteredY = None

root = Tk()
root.title('디아블로 런처')
root.geometry("520x450+100+100")
root.resizable(False, False)
launch = Tk()
launch.geometry("300x125+200+200")
launch.resizable(False, False)

def ShowWindow():
    launch.after(1, lambda: launch.focus_force())

def HideWindow():
    root.after(1, lambda: root.focus_force())

def ExitProgram():
    launch.destroy()
    root.destroy()
    
launch.protocol("WM_DELETE_WINDOW", HideWindow)
root.protocol("WM_DELETE_WINDOW", ExitProgram)

def DiabloII_Launcher():
    global diabloExecuted
    global launch
    diabloExecuted = True
    switchButton['text'] = '디스플레이 해상도 복구 (게임 종료시 사용)'
    os.system(f'wsl.exe resolution {alteredX} {alteredY}')
    os.system(f'"{gamePath}/Diablo II Resurrected/Diablo II Resurrected Launcher.exe"')
    tkinter.messagebox.showinfo('Diablo II Resurrected', '디아블로 II Resurrected가 실행되었습니다. 파란색 "플레이" 버튼을 클릭하여 게임을 실행해 주세요.')
    HideWindow()
    UpdateStatusValue()

def DiabloIII_Launcher():
    global diabloExecuted
    global launch
    diabloExecuted = True
    switchButton['text'] = '디스플레이 해상도 복구 (게임 종료시 사용)'
    os.system(f'wsl.exe resolution {alteredX} {alteredY}')
    os.system(f'"{gamePath}/Diablo III/Diablo III Launcher.exe"')
    tkinter.messagebox.showinfo('Diablo III', '디아블로 III이 실행되었습니다. 파란색 "플레이" 버튼을 클릭하여 게임을 실행해 주세요.')
    UpdateStatusValue()

def LaunchGameAgent():
    global diabloExecuted
    global launch
    if diabloExecuted:
        diabloExecuted = False
        switchButton['text'] = '디아블로 실행...'
        os.system(f'wsl.exe resolution {originX} {originY}')
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
            
        if not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
            diablo3['state'] = "disabled"

        ShowWindow()
        launch.mainloop()

def EmgergencyReboot():
    global forceReboot
    if forceReboot:
        forceReboot = False
        emergencyButton['text'] = '긴급 재시동 (게임 저장 후 실행 요망)'
        switchButton['state'] = "normal"
        os.system(f'shutdown -a')
    else:
        forceReboot = True
        emergencyButton['text'] = '긴급 재시동 준비중... (재시동 취소)'
        switchButton['state'] = "disabled"
        os.system(f'wsl.exe resolution {originX} {originY}')
        UpdateStatusValue()
        os.system(f'shutdown -r -f -t 10 -c "Windows가 DiabloLauncher의 [긴급 재시동] 기능으로 인해 재시동 됩니다."')


def GetEnvironmentValue():
    global data
    global gamePath
    global originX
    global originY
    global alteredX
    global alteredY

    data = os.environ.get('DiabloLauncher')
    temp = None
    gamePath, originX, originY, alteredX, alteredY, temp = data.split(';')

def UpdateStatusValue():
    GetEnvironmentValue()
    status['text'] = f"\n정보\n환경변수 설정됨: {'예' if data.index != 0 else '아니오'}\nWSL 지원됨: {'예' if os.path.isfile('C:/Windows/System32/wsl.exe') else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('wsl.exe resolution list') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data.index != 0 else '사용할 수 없음'}\n현재 디스플레이 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {gamePath}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else ' 아니오 '}\n"

GetEnvironmentValue()
welcome = Label(root, text='')
switchButton = Button(root, text='디아블로 실행...', command=LaunchGameAgent)
emergencyButton = Button(root, text='긴급 재시동 (게임 저장 후 실행 요망)', command=EmgergencyReboot)
status = Label(root, text=f"\n정보\n환경변수 설정됨: {'예' if data.index != 0 else '아니오'}\nWSL 지원됨: {'예' if os.path.isfile('C:/Windows/System32/wsl.exe') else '아니오'}\n해상도 변경 지원됨: {'아니오' if os.system('wsl.exe resolution list') != 0 else '예'}\n해상도 벡터: {f'{originX}x{originY} - {alteredX}x{alteredY}' if data.index != 0 else '사용할 수 없음'}\n현재 디스플레이 해상도: {f'{alteredX}x{alteredY}' if diabloExecuted else f'{originX}x{originY}'}\n게임 디렉토리: {gamePath}\n디렉토리 존재여부: {'예' if os.path.isdir(gamePath) else '아니오'}\n디아블로 실행: {'예' if diabloExecuted else ' 아니오 '}\n")
info = Label(root, text='도움말\n디아블로를 원할히 플레이하려면 DiabloLauncher 환경 변수를 설정해 주세요.\n게임 디렉토리, 해상도를 변경하려면 DiabloLauncher 환경변수를 편집하세요.\n긴급 재시동은 해상도를 복구한 후 시스템을 재시동합니다.')
notice = Label(root, text='Blizzard 정책상 게임 실행은 직접 실행하여야 하며 실행시 알림창 지시를 따르시기 바랍니다.\n해당 프로그램을 사용함으로써 발생하는 모든 불이익은 전적으로 사용자에게 있습니다.\n지원되는 디아블로 버전은 Diablo II Resurrected, Diablo III 입니다.\n그 외 버전 또는 게임은 호환이 되지 않을 수 있습니다.\n\n이 디아블로 런처에 관하여\n디아블로 게임 및 런처: (c) 2022 BLIZZARD ENTERTAINMENT, INC. ALL RIGHTS RESERVED.\n본 프로그램: Copyright (c) 2022 Hyeongmin Kim')

welcome.pack()
switchButton.pack()
emergencyButton.pack()
status.pack()
info.pack()
notice.pack()

root.mainloop()

