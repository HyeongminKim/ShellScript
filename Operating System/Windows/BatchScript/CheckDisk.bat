@echo off

net session > nul 2>&1
if NOT %ERRORLEVEL% == 0 (
    echo This script requires administrator privileges.
    exit /B 1
)

:: Dism -Online -Cleanup-Image -CheckHealth
:: Dism -Online -Cleanup-Image -ScanHealth

Dism -Online -Cleanup-Image -RestoreHealth
sfc -scannow

chkdsk C: /F
if exist "E:" (
    chkdsk E: /F
)

