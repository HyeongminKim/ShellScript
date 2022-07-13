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
                    Write-Host "Access denied. unable to delete this shortcut: $($item)" -ForegroundColor red
                    $Host.PrivateData.ProgressBackgroundColor='Red'
                    $deleteFailed = $true
                } else {
                    $output = "Deleted broken shortcut: $($item.name)"
                    Write-Host "$($item) is deleted due to a broken link."
                    $isBroken = $true
                    $Host.PrivateData.ProgressBackgroundColor='DarkCyan'
                }
            } else {
                $output = "Access denied. unable to delete this shortcut: $($item.name)"
                Write-Host "Access denied. unable to delete this shortcut: $($item)" -ForegroundColor red
                $Host.PrivateData.ProgressBackgroundColor='Red'
                $deleteFailed = $true
            }
        }
    } else {
        $output = "Scanned file: $($item.name)"
    }
    $progress++
    Write-Progress -activity "Verifing recent files..." -currentOperation "$($output)" -status "Please wait until action completed... ($progress of $($target.count))" -percentComplete (($progress / $target.count) * 100)
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
if ($isBroken) {
    Write-Host "Restart Windows Explorer for changes to take effect"
    Write-Host "> (NOTE: Any unsaved information will be lost) ..." -NoNewLine
    cmd.exe /c taskkill /f /im explorer.exe 1>$null 2>&1
    if ($?) {
        Write-Host " Done. "
        cmd.exe /c start explorer.exe
    } else {
        $input = Read-Host "`nWindows Explorer doesn't seem to close properly.`n`tDid it close properly? (y/N)"
        if (($input -eq "y") -or ($input -eq "Y")) {
            Write-Host "Done. "
            cmd.exe /c start explorer.exe
        } else {
            Write-Host "Reboot the computer for the changes to take effect." -ForegroundColor red
            Write-Host "NOTE: Press the ^⇧⎋ (CTRL + SHIFT + ESC) and the Task Manager will open."
        }
    }
} else {
    Write-Host "Windows Explorer will not restart. Requirements already satisfied."
}

