# User directory name
$whoami = "$env:USERNAME"

# Start cleanup Downloads directory function
Write-Host "Removing files with extension exe in download directory..." -NoNewLine
Get-ChildItem "C:\Users\$whoami\Downloads\*" -Include *.exe -Recurse | Remove-Item -Force 2>$null
if ($?) {
    Write-Host " Done. "
} else {
    Write-Host " Failed. "
}

# Start empty trash can function
Write-Host "Emptying the recycle bin of drive C..." -NoNewLine
Clear-RecycleBin -DriveLetter C -Force 2>$null
Write-Host " Done. "

# Start closing script window function
Write-Host "This window will close automatically after 5 seconds..." -NoNewLine
for($i=5; $i -ge 0; $i--) {
    if ( 1 -ne $i ) {
        Write-Host "`b`b`b`b`b`b`b`b`b`b`b`b$i seconds..." -NoNewLine
    } else {
        Write-Host "`b`b`b`b`b`b`b`b`b`b`b`b$i second... " -NoNewLine
    }
    Start-Sleep -Seconds 1
}

Write-Host "`n`nPowerShell Cleanup.ps1 has been terminated."
