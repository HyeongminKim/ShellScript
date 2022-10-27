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
        if os.system(f'QRes -X {alteredX} -Y {alteredY} -R {alteredFR}') != 0:
            tkinter.messagebox.showwarning('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')

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
        if os.system(f'QRes -X {alteredX} -Y {alteredY} -R {alteredFR}') != 0:
            tkinter.messagebox.showwarning('디아블로 런처', f'{alteredX}x{alteredY} {alteredFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
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
            if os.system(f'QRes -X {originX} -Y {originY} -R {originFR}') != 0:
                tkinter.messagebox.showwarning('디아블로 런처', f'{originX}x{originY} {originFR}Hz 해상도는 이 디스플레이에서 지원하지 않습니다. 시스템 환경 설정에서 지원하는 해상도를 확인하시기 바랍니다.')
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
    except Exception as error:
        tkinter.messagebox.showerror('디아블로 런처', f'환경변수 파싱중 예외가 발생하였습니다. 올바른 표현식은 gamePath;originX;originY;originFR;alteredX;alteredY;alteredFR; 입니다. 필수 파라미터가 누락되지 않았는지 또는 ";" 문자가 올바르게 삽입되었는지 다시 한번 확인하시기 바랍니다. Exception code: {error}')
        data = None

def SetEnvironmentValue():
    global data
    tkinter.messagebox.showinfo('환경변수 편집기', '이 편집기는 본 프로그램에서만 적용되며 디아블로 런처를 종료 시 모든 변경사항이 유실됩니다. 변경사항을 영구적으로 적용하시려면 "고급 시스템 설정"을 이용해 주세요')
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
            if data is not None and not os.path.isdir(gamePath):
                tkinter.messagebox.showwarning('환경변수 편집기', f'{gamePath} 디렉토리가 존재하지 않습니다.')
                envWindow.after(1, lambda: envWindow.focus_force())
            elif data is not None and os.path.isdir(gamePath):
                if not os.path.isfile(gamePath + '/Diablo II Resurrected/Diablo II Resurrected Launcher.exe') and not os.path.isfile(gamePath + '/Diablo III/Diablo III Launcher.exe'):
                    tkinter.messagebox.showwarning('디아블로 런처', f'{gamePath} 디렉토리에는 적합한 게임이 존재하지 않습니다.')
                    envWindow.after(1, lambda: envWindow.focus_force())
                else:
                    envWindow.destroy()

    commitBtn = tkinter.Button(envWindow, text='수정', command=commit)
    commitBtn.pack()

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
notice = Label(root, text='Blizzard 정책상 게임 실행은 직접 실행하여야 하며 실행시 알림창 지시를 따르시기 바랍니다.\n해당 프로그램을 사용함으로써 발생하는 모든 불이익은 전적으로 사용자에게 있습니다.\n지원되는 디아블로 버전은 Diablo II Resurrected, Diablo III 입니다.\n그 외 버전 또는 게임은 호환이 되지 않을 수 있습니다.\n\n이 디아블로 런처에 관하여\n디아블로 게임 및 런처: (c) 2022 BLIZZARD ENTERTAINMENT, INC. ALL RIGHTS RESERVED.\n본 프로그램: Copyright (c) 2022 Hyeongmin Kim')

welcome.pack()
switchButton.pack()
emergencyButton.pack()
status.pack()
refreshBtn.pack()
info.pack()
notice.pack()

root.mainloop()

