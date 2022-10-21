@ECHO OFF
title BootCamp Recover

if NOT exist "%TEMP%\BootCamp_Driver" (
    if NOT "%SAFEBOOT_OPTION%" == "" (
        echo Please enter normal mode to download drivers...
        timeout 2 > NUL
        exit /b 1
    )

    if NOT exist "C:\Windows\System32\brigadier.exe" (
        echo error: brigadier not found. Please install brigadier to continue.
        explorer https://github.com/timsutton/brigadier
        timeout 2 > NUL
        exit /b 1
    )

    if NOT exist "C:\Program Files\7-Zip\7z.exe" (
        echo error: 7-Zip not found. Please install 7-Zip to continue.
        explorer https://7-zip.org
        timeout 2 > NUL
        exit /b 1
    )

    if "%COMPUTER_MODEL_ID%" == "" (
        echo Please set Mac model in COMPUTER_MODEL_ID.
        echo For example COMPUTER_MODEL_ID=iMac3,1
        explorer https://support.apple.com/en-us/HT201634
        timeout 2 > NUL
        exit /b 1
    )

    mkdir %TEMP%\BootCamp_Driver
    brigadier -m %COMPUTER_MODEL_ID% -o %TEMP%\BootCamp_Driver
    if NOT %ERRORLEVEL% == 0 (
        echo Unexpected error occurred. The BootCamp driver wasn't successfully downloaded.
        pause
        exit /b 1
    )

    echo Please set boot options to safe mode "Minimal" and enter safe mode.
    msconfig
    pause
) else (
    if NOT "%SAFEBOOT_OPTION%" == "MINIMAL" (
        echo Please enter safe mode to upgrade drivers...
        timeout 2 > NUL
        exit /b 1
    )

    echo Please remove corrupted drivers completely
    echo NOTE: Please check "Delete the driver software for this device." either.
    echo.
    echo Install use "Browse my computer for drivers" and choose %TEMP%\BootCamp_Driver directory.
    echo NOTE: Please check "Include subfolders" option.
    explorer %TEMP%\BootCamp_Driver
    devmgmt.msc
    pause

    rmdir /s /q %TEMP%\BootCamp_Driver
    if NOT %ERRORLEVEL% == 0 (
        echo Unable to delete downloaded driver directory. Please delete it manually.
        explorer %TEMP%\BootCamp_Driver
        timeout 2 > NUL
    )

    echo Please uncheck safe boot options.
    msconfig
)

exit

