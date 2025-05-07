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

