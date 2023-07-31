@echo off

IF NOT "%1" == "" (
    IF %1 == "sleep" (
        bash.exe -c "echo -en '\n\n' | powermgr %1"
    ) ELSE (
        bash.exe -c "powermgr %1 15"
    )
    exit /b %ERRORLEVEL%
) ELSE (
    exit /b 1
)
