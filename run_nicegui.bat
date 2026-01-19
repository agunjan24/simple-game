@echo off
if "%1"=="--network" (
    echo Starting in network mode (accessible from other devices)
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
        for /f "tokens=1" %%b in ("%%a") do (
            echo Access from your phone at: http://%%b:8080
        )
    )
    set HOST=0.0.0.0
    python app_nicegui.py %2
) else (
    echo Starting on localhost only
    echo Use "run_nicegui --network" to access from phone
    python app_nicegui.py %1
)
