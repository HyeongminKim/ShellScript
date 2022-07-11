# User directory name
$whoami = "$env:USERNAME"

# User recent items path
$recentDir = "C:\Users\$whoami\AppData\Roaming\Microsoft\Windows\Recent"

# Is broken shortcut exist?
$isBroken = $false
$deleteFailed = $false

# Start verifying recent items shortcut function
Write-Host "Verification of the existence of the original shortcut to the recent item..."

$target = Get-ChildItem -Recurse "$recentDir" -Include *.lnk -Force
$shell = New-Object -ComObject WScript.Shell
$progress = 0
foreach ($item in $target) {
    $broken = $shell.CreateShortcut($item).TargetPath
    if ($broken) {
        $check = Test-Path "$broken"
        if ($check -eq $false) {
            Remove-Item "$item" -Force 2>$null
            if ($?) {
                Get-Item "$item" 2>$null
                if ($?) {
                    $output = "Access denied. unable to delete this shortcut: $($item.name)"
                    Write-Host "Access denied. unable to delete this shortcut: $($item.name)" -ForegroundColor red
                    $Host.PrivateData.ProgressBackgroundColor='Red'
                    $deleteFailed = $true
                } else {
                    $output = "Deleted broken shortcut: $($item.name)"
                    Write-Host "$($item.name) is deleted due to a broken link."
                    $isBroken = $true
                    $Host.PrivateData.ProgressBackgroundColor='DarkCyan'
                }
            } else {
                $output = "Access denied. unable to delete this shortcut: $($item.name)"
                Write-Host "Access denied. unable to delete this shortcut: $($item.name)" -ForegroundColor red
                $Host.PrivateData.ProgressBackgroundColor='Red'
                $deleteFailed = $true
            }
        }
    } else {
        $output = "Scanned file: $($item.name)"
    }
    $progress++
    Write-Progress -activity "Verifing recent files..." -currentOperation "$($output)" -status "Please wait until action completed... ($progress of $($target.count))" -percentComplete (($progress / $target.count) * 100)
    Start-Sleep -milliseconds 256
}

# Specify message when progress bar completes
if ($deleteFailed) {
    $Host.PrivateData.ProgressBackgroundColor='Magenta'
    Write-Progress -activity "Unable to verify recent files." -status "Failed to delete target files."
} elseif ($isBroken) {
    $Host.PrivateData.ProgressBackgroundColor='Green'
    Write-Progress -activity "Verified recent files." -status "Successfully deleted target files."
} else {
    $Host.PrivateData.ProgressBackgroundColor='Green'
    Write-Progress -activity "Verified recent files." -status "Requirements already satisfied."
}
Start-Sleep -milliseconds 800
Write-Progress "N/A" "N/A" -completed
$Host.PrivateData.ProgressBackgroundColor='DarkCyan'

# Relaunch explorer.exe when broken shortcuts exist (aka. isBroken value is true)
if($isBroken -eq $true) {
    Write-Host "Restart Windows Explorer for changes to take effect"
    Write-Host "> (NOTE: Any unsaved information will be lost) ..." -NoNewLine
    cmd.exe /c taskkill /f /im explorer.exe 1>$null 2>&1
    if ($?) {
        Write-Host "Done. "
    } else {
        Write-Host "`nAnother user is logged in. Please restart computer to take effect." -ForegroundColor red
    }
    cmd.exe /c start explorer.exe
} else {
    Write-Host "Windows Explorer will not restart. Requirements already satisfied."
}

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

Write-Host "`n`nPowerShell VerifyRecentfiles.ps1 has been terminated."
