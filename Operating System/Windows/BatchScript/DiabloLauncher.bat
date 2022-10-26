@ECHO OFF
title Diablo Bundle Launcher
chcp 65001 > NUL
color 07

set checkenv="true"
set textStyle="false"
set DAS="false"
set DAT="false"

echo | set /p=Checking WSL (1/8) ... 
timeout 1 > NUL
if NOT exist "C:\Windows\System32\wsl.exe" (
    echo.
    echo Unable to execute screen resolution program. Please install WSL.
    color 47
    timeout 2 > NUL
    exit /b 1
)
echo Done.

echo | set /p=Verifying resolution program (2/8) ... 
timeout 1 > NUL
"C:\Windows\System32\wsl.exe" "resolution" "list" > NUL
if %ERRORLEVEL% == 1 (
    echo.
    echo Unable to execute screen resolution program. Please install program or check permission.
    color 47
    timeout 2 > NUL
    exit /b 1
)
echo Done.

echo | set /p=Checking text styling (3/8) ... 
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

echo | set /p=Checking Battle.net game directory (4/8) ... 
timeout 1 > NUL
for /f "delims=';' tokens=1" %%a in ("%DiabloLauncher%") do (
    set getGameDir=%%a
)
if NOT exist "%getGameDir%" (
    echo.
    if "%getGameDir%" == "" (
        echo Unable to locate Diablo installed path. Please set System Environment Variable: DiabloLauncher
        echo Please set DiabloLauncher like this: GameDir;OriginX;OriginY;AlteredX;AlteredY
        echo DiabloLauncher path example: C:\Program Files\Battle.net;5120;2880;2560;1440
    ) else (
        echo Unable to locate Diablo installed path: %getGameDir%. 
    )
    echo Please check Diablo installed correctly or System Environment Variable.
    color 47
    timeout 2 > NUL
    exit /b 1
)
echo %getGameDir%.

echo | set /p=Verifying Diablo II Resurrected directory (5/8) ... 
timeout 1 > NUL
if NOT exist "%getGameDir%\Diablo II Resurrected" (
    echo.
    echo Unable to locate Diablo II Resurrected installed path.
    echo Please check Diablo II Resurrected installed correctly.
    set checkenv="false"
) else (
    set DAS="true"
    echo Done.
)

echo | set /p=Verifying Diablo III directory (6/8) ... 
timeout 1 > NUL
if NOT exist "%getGameDir%\Diablo III" (
    echo.
    echo Unable to locate Diablo III installed path. 
    echo Please check Diablo III installed correctly.
    set checkenv="false"
) else (
    set DAT="true"
    echo Done.
)

echo | set /p=Checking Diablo installed correctly (7/8) ... 
timeout 1 > NUL
if %DAS% == "false" (
    if %DAT% == "false" (
        echo Current launchable Diablo not detected. Please install Diablo first. Exiting...
        color 47
        timeout 2 > NUL
        exit /b 1
    )
)
echo Done.

echo | set /p=Checking screen resolution vector (8/8) ... 
timeout 1 > NUL
for /f "delims=';' tokens=2,3,4,5" %%a in ("%DiabloLauncher%") do (
    set ORIGIN_RES_X=%%a
    set ORIGIN_RES_Y=%%b
    set ALTERED_RES_X=%%c
    set ALTERED_RES_Y=%%d
)
if "%ORIGIN_RES_X%" == "" (
    echo.
    echo Unable to get origin screen resolution width. Please set System Environment Variable: DiabloLauncher
    echo Please set DiabloLauncher like this: GameDir;OriginX;OriginY;AlteredX;AlteredY
    echo DiabloLauncher path example: C:\Program Files\Battle.net;5120;2880;2560;1440
    color 47
    timeout 2 > NUL
    exit /b 1
) 
if "%ORIGIN_RES_Y%" == "" (
    echo.
    echo Unable to get origin screen resolution height. Please set System Environment Variable: DiabloLauncher
    echo Please set DiabloLauncher like this: GameDir;OriginX;OriginY;AlteredX;AlteredY
    echo DiabloLauncher path example: C:\Program Files\Battle.net;5120;2880;2560;1440
    color 47
    timeout 2 > NUL
    exit /b 1
)
if "%ALTERED_RES_X%" == "" (
    echo.
    echo Unable to switch screen resolution width. Please set System Environment Variable: DiabloLauncher
    echo Please set DiabloLauncher like this: GameDir;OriginX;OriginY;AlteredX;AlteredY
    echo DiabloLauncher path example: C:\Program Files\Battle.net;5120;2880;2560;1440
    color 47
    timeout 2 > NUL
    exit /b 1
) 
if "%ALTERED_RES_Y%" == "" (
    echo.
    echo Unable to switch screen resolution height. Please set System Environment Variable: DiabloLauncher
    echo Please set DiabloLauncher like this: GameDir;OriginX;OriginY;AlteredX;AlteredY
    echo DiabloLauncher path example: C:\Program Files\Battle.net;5120;2880;2560;1440
    color 47
    timeout 2 > NUL
    exit /b 1
)
echo %ORIGIN_RES_X%x%ORIGIN_RES_Y% - %ALTERED_RES_X%x%ALTERED_RES_Y%.
echo.

if %checkenv% == "false" (
    echo Some check returns warning! Please review above output.
    color 60
    pause

    echo | set /p=Please wait until init progress is done.
    timeout 2 > NUL
) else (
    echo | set /p=All check passed! Please wait until init progress is done.
    color 17
    timeout 2 > NUL
)
cls
color 07

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
    echo Battle.net now launching... The screen resolution will now setting the recommand value.

    "C:\Windows\System32\wsl.exe" "resolution" "%ALTERED_RES_X%" "%ALTERED_RES_Y%"
    echo Please launch Diablo II Resurrected click BLUE PLAY BUTTON...

    cd "%getGameDir%\Diablo II Resurrected"
    "%getGameDir%\Diablo II Resurrected\Diablo II Resurrected Launcher.exe"
    set /p program=If you want RESETTING NORMAL SCREEN RESOLUTION and STOP THE GAME please PRESS ANY KEY...

    pause > NUL
    echo The screen resolution will now setting default value.
    "C:\Windows\System32\wsl.exe" "resolution" "%ORIGIN_RES_X%" "%ORIGIN_RES_Y%"

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
    echo Battle.net now launching... The screen resolution will now setting the recommand value.

    "C:\Windows\System32\wsl.exe" "resolution" "%ALTERED_RES_X%" "%ALTERED_RES_Y%"
    echo Please launch Diablo III click BLUE PLAY BUTTON...

    cd "%getGameDir%\Diablo III"
    "%getGameDir%\Diablo III\Diablo III Launcher.exe"
    set /p program=If you want RESETTING NORMAL SCREEN RESOLUTION and STOP THE GAME please PRESS ANY KEY...

    pause > NUL
    echo The screen resolution will now setting default value.
    "C:\Windows\System32\wsl.exe" "resolution" "%ORIGIN_RES_X%" "%ORIGIN_RES_Y%"

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
color 47
timeout 2 > NUL
exit /b 1

