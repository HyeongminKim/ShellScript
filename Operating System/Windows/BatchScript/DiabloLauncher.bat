@ECHO OFF
title Diablo Bundle Launcher
chcp 65001 > NUL

set checkenv="true"
set textStyle="false"
set DAS="false"
set DAT="false"

echo | set /p=Checking Windows Terminal (1/7) ... 
timeout 1 > NUL
if NOT exist "C:\Windows\System32\wsl.exe" (
    echo.
    echo Unable to execute screen resolution program. Please install Windows Terminal.
    timeout 2 > NUL
    exit /b 1
)
echo Done.

echo | set /p=Verifying resolution program (2/7) ... 
timeout 1 > NUL
"C:\Windows\System32\wsl.exe" "resolution" "list" > NUL
if %ERRORLEVEL% == 1 (
    echo.
    echo Unable to execute screen resolution program. Please install program or check permission.
    timeout 2 > NUL
    exit /b 1
)
echo Done.

echo | set /p=Checking text styling (3/7) ... 
timeout 1 > NUL
"C:\Windows\System32\wsl.exe" "which" "figlet" > NUL
if %ERRORLEVEL% == 1 (
    echo.
    echo Warning figlet package not found. Some text style will replaced regacy text style and it doesn't show correctly.
    set checkenv="false"
) else (
    set textStyle="true"
    echo Done.
)

echo | set /p=Checking Battle.net game directory (4/7) ... 
timeout 1 > NUL
if NOT exist "%BLIZZARD_GAME_PATH%" (
    echo.
    if "%BLIZZARD_GAME_PATH%" == "" (
        echo Unable to locate Diablo installed path. Please set System Environment Variable: BLIZZARD_GAME_PATH
    ) else (
        echo Unable to locate Diablo installed path: %BLIZZARD_GAME_PATH%. 
    )
    echo Please check Diablo installed correctly or System Environment Variable.
    timeout 2 > NUL
    exit /b 1
)
echo Done.

echo | set /p=Verifying Diablo II Resurrected directory (5/7) ... 
timeout 1 > NUL
if NOT exist "%BLIZZARD_GAME_PATH%\Diablo II Resurrected" (
    echo.
    echo Unable to locate Diablo II Resurrected installed path.
    echo Please check Diablo II Resurrected installed correctly.
    set checkenv="false"
) else (
    set DAS="true"
    echo Done.
)

echo | set /p=Verifying Diablo III directory (6/7) ... 
timeout 1 > NUL
if NOT exist "%BLIZZARD_GAME_PATH%\Diablo III" (
    echo.
    echo Unable to locate Diablo III installed path. 
    echo Please check Diablo III installed correctly.
    set checkenv="false"
) else (
    set DAT="true"
    echo Done.
)

echo | set /p=Checking Diablo installed correctly (7/7) ... 
timeout 1 > NUL
if %DAS% == "false" (
    if %DAT% == "false" (
        echo Current launchable Diablo not detected. Please install Diablo first. Exiting...
        timeout 2 > NUL
        exit /b 1
    )
)
echo Done.
echo.

if %checkenv% == "false" (
    echo Some check returns warning! Please review above output.
    pause

    echo | set /p=Please wait until init progress is done.
    timeout 2 > NUL
) else (
    echo | set /p=All check passed! Please wait until init progress is done.
    timeout 2 > NUL
)
cls

if %textStyle% == "true" (
    "C:\Windows\System32\wsl.exe" "figlet" "Diablo" "Launcher"
) else (
    echo Diablo Launcher
)
echo.

echo Welcome to Diablo Bundle Launcher!
echo.

if %DAS% == "true" (
    if %DAT% == "true" (
        set /p "program=Please choose Diablo version (II, III): "
    ) else (
        set /p "program=Please choose Diablo version (II): "
    )
) else (
    if %DAT% == "true" (
        set /p "program=Please choose Diablo version (III): "
    )
)

if "%program%" == "II" (
    if %DAS% == "false" (
        goto INPUTFAILED
    )

    cls
    title Diablo II Launcher
    if %textStyle% == "true" (
        "C:\Windows\System32\wsl.exe" "figlet" "Diablo" "II" "Resurrected"
    ) else (
        echo Diablo II Resurrected
    )
    echo.
    echo Diablo II Resurrected now launching... The screen resolution will now setting the recommand value.

    echo Please launch Diablo II Resurrected click BLUE PLAY BUTTON...

    "C:\Windows\System32\wsl.exe" "resolution" "2560" "1440"

    set /p program=If you want RESETTING NORMAL SCREEN RESOLUTION and STOP THE GAME please PRESS ANY KEY...
    cd "%BLIZZARD_GAME_PATH%\Diablo II Resurrected"
    "%BLIZZARD_GAME_PATH%\Diablo II Resurrected\Diablo II Resurrected Launcher.exe"

    pause > NUL
    echo The screen resolution will now setting default value.
    "C:\Windows\System32\wsl.exe" "resolution" "5120" "2880"

    timeout 2 > NUL
    exit /b 0
) else if "%program%" == "III" (
    if %DAS% == "false" (
        goto INPUTFAILED
    )

    cls
    title Diablo III Launcher
    if %textStyle% == "true" (
        "C:\Windows\System32\wsl.exe" "figlet" "Diablo" "III"
    ) else (
        echo Diablo III
    )
    echo.
    echo Diablo III now launching... The screen resolution will now setting the recommand value.
    echo Please launch Diablo III click BLUE PLAY BUTTON...

    "C:\Windows\System32\wsl.exe" "resolution" "2560" "1440"

    set /p program=If you want RESETTING NORMAL SCREEN RESOLUTION and STOP THE GAME please PRESS ANY KEY...
    cd "%BLIZZARD_GAME_PATH%\Diablo III"
    "%BLIZZARD_GAME_PATH%\Diablo III\Diablo III Launcher.exe"

    pause > NUL
    echo The screen resolution will now setting default value.
    "C:\Windows\System32\wsl.exe" "resolution" "5120" "2880"

    timeout 2 > NUL
    exit /b 0
) else (
    goto INPUTFAILED
)

:INPUTFAILED
if "%program%" == "" (
    echo Unable to start Diablo. Please provide specific installed Diablo version. Exiting...
) else (
    echo Unable to start Diablo version: %program%. Please check installed correctly. Exiting...
)
timeout 2 > NUL
exit /b 1

