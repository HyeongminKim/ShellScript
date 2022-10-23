@ECHO OFF
title BootCamp Recover
chcp 1252 > NUL

set driverExist="false"

if "%PROCESSOR_ARCHITECTURE%" NEQ "AMD64" (
    echo The brigadier program doesn't fully support 32-bit OS yet.
    if "%SAFEBOOT_OPTION%" NEQ "MINIMAL" (
        explorer https://github.com/timsutton/brigadier/issues/2
    ) else (
        echo For more imfomation, visit https://github.com/timsutton/brigadier/issues/2
    )
    pause
    exit /b 1
)

if NOT exist "%TEMP%\BootCamp_Driver" (
    if "%SAFEBOOT_OPTION%" == "" (
        goto shouldDownloadDriver
    ) else (
        echo Unable to find BootCamp Dirver. Please enter normal mode and download BootCamp drivers...
        pause
        exit /b 1
    )
) else (
    for /F %%i in ('dir /b /a "%TEMP%\BootCamp_Driver\*"') do (
        if "%SAFEBOOT_OPTION%" == "MINIMAL" (
            goto shouldInstallDriver
        ) else (
            echo BootCamp driver already exist. Please enter safe mode to upgrade drivers...
            pause
            exit /b 1
        )
    )

    if "%SAFEBOOT_OPTION%" == "MINIMAL" (
        echo Unable to find BootCamp Dirver. Please enter normal mode and download BootCamp drivers...
        pause
        exit /b 1
    ) else (
        rmdir /s /q %TEMP%\BootCamp_Driver > NUL
        if "%ERRORLEVEL%" NEQ "0" (
            echo Unable to delete empty driver directory. Please delete it manually.
            explorer %TEMP%\BootCamp_Driver
        )
        goto shouldDownloadDriver
    )

)

:shouldDownloadDriver
if NOT exist "C:\Windows\System32\brigadier.exe" (
    echo error: Unable to locate brigadier. Please install brigadier to continue.
    explorer https://github.com/timsutton/brigadier
    pause
    exit /b 1
)

where winget > NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo error: Unable to locate winget. Please install winget to continue.
    explorer https://github.com/microsoft/winget-cli
    pause
    exit /b 1
)

if NOT exist "C:\Program Files\7-Zip\7z.exe" (
    echo error: 7-Zip not found. Please install 7-Zip to continue.
    winget install 7zip.7zip
)

if "%COMPUTER_MODEL_ID%" == "" (
    echo Please set Mac model in COMPUTER_MODEL_ID.
    echo For example COMPUTER_MODEL_ID=iMac3,1
    explorer https://support.apple.com/en-us/HT201634
    pause
    exit /b 1
)

mkdir %TEMP%\BootCamp_Driver
if "%ERRORLEVEL%" NEQ "0" (
    echo Unable to create %TEMP%\BootCamp_Driver directory. Please check the %TEMP% directory permission.
    goto fatalError
)

brigadier -m %COMPUTER_MODEL_ID% -o %TEMP%\BootCamp_Driver
if "%ERRORLEVEL%" == "0" (
    for /F %%i in ('dir /b /a "%TEMP%\BootCamp_Driver\*"') do (
        goto driverExist
    )

    echo Unable to download driver. The brigadier couldn't save drivers to %TEMP%\BootCamp_Driver directory.
    goto fatalError

    :driverExist
    echo Please set boot options to safe mode [Minimal] and enter safe mode.
    msconfig
    pause
    exit
) else (
    echo Unable to launch brigadier. The brigadier exit code is %ERRORLEVEL%.
    explorer https://github.com/timsutton/brigadier/issues
    if exist "%TEMP%\BootCamp_Driver" (
        rmdir /s /q %TEMP%\BootCamp_Driver > NUL
        if "%ERRORLEVEL%" NEQ "0" (
            echo Unable to delete empty driver directory. Please delete it manually.
            explorer %TEMP%\BootCamp_Driver
        )
    )
    pause
    exit /b 1
)

:shouldInstallDriver
echo Please remove corrupted drivers completely
echo NOTE: Please check "Delete the driver software for this device." either.
echo.
echo Install use "Browse my computer for drivers" and choose %TEMP%\BootCamp_Driver directory.
echo NOTE: Please check "Include subfolders" option.
explorer %TEMP%\BootCamp_Driver
devmgmt.msc
pause

rmdir /s /q %TEMP%\BootCamp_Driver > NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo Unable to delete downloaded driver directory. Please delete it manually.
    explorer %TEMP%\BootCamp_Driver
    pause
    exit /b 1
) else (
    echo Please uncheck safe boot options.
    msconfig
    pause
    exit
)

:fatalError
rmdir /s /q %TEMP%\BootCamp_Driver > NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo Please check the %TEMP%\BootCamp_Driver directory permission.
    echo Unable to delete downloaded driver directory. Please delete it manually.
    explorer %TEMP%\BootCamp_Driver
) else (
    echo Runtime Error: A dependency program has unexpectedly terminated.
    echo Description: The required process was terminated due to an unhandled exception.
    echo Exception Info: InvalidOperationException.
    echo StackTrace:
    echo     at brigadier.exe -m %COMPUTER_MODEL_ID% -o %TEMP%\BootCamp_Driver
    echo     at [cmd] if
    echo     at BootCampRecover.bat
    echo Attached Report
    powershell "Get-EventLog -LogName 'Application' -Newest 1 | Select-Object -Property *"
    echo.
)
pause
exit /b 1
