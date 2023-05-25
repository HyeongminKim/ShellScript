@echo off

IF NOT "%1" == "" (
    bash.exe -c "powermgr %1 15"
    exit /b %ERRORLEVEL%
) else (
    exit /b 1
)
