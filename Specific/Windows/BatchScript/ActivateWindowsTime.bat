@echo off
:: state: 1 STOPPED
:: state: 2 START_PENDING
:: state: 3 STOP_PENDING
:: state: 4 RUNNING

bcdedit > NUL
if %ERRORLEVEL% == 1 (
    echo access denied. Are you root?
    exit /b 1
)

sc query w32time | findstr RUNNING > NUL
if %ERRORLEVEL% == 1 (
    sc start w32time
    timeout /t 3 /nobreak > NUL
    sc query w32time | findstr RUNNING > NUL
    if %ERRORLEVEL% == 1 (
        echo unable to start w32time. Aborting
        exit /b 127
    )
)

w32tm /resync
if %ERRORLEVEL% == 1 (
    echo unable to sync network time. Check w32time service.
    exit /b 2
)
