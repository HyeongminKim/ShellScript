# User directory name
$whoami = "$env:USERNAME"

# User root paths
$userDir = "C:\Users\$whoami"
$externalDir = "E:\Users\$whoami"

# Incompatible cache files with this script
$vscodevim = "$userDir\AppData\Roaming\Code\User\globalStorage\vscodevim.vim"
$vscode_cmd = "$vscodevim\.cmdline_history"
$vscode_search = "$vscodevim\.search_history"

$isMakeup = $false
$accessFailed = $false

# Hide dotfiles function
function Hide-Dotfiles {
    param (
        [Parameter(Mandatory)]
        [string]$targetDir
    )

    if (Test-Path -Path $targetDir) {
        Write-Host "Hiding dotfiles in $targetDir..."
        $folder = Get-ChildItem -Recurse "$targetDir" -Include .* -Force 2>$null
        $progress = 0
        foreach ($item in $folder) {
            $target = Get-Item $item -Force
            if ($target.attributes.GetType().Hidden) {
                Set-ItemProperty -Path $target -name Attributes -value ([System.IO.FileAttributes]::Hidden) -Force 2>$null
                if ($?) {
                    $output = "Hid dotfiles: $($item.name)"
                    Write-Host "$($item.name) is hid due to dotfiles."
                    $isMakeup = $true
                    $Host.PrivateData.ProgressBackgroundColor='DarkCyan'
                } else {
                    $output = "Access denied. unable to modify this file: $($item.name)"
                    Write-Host "Access denied. unable to modify attributes this file: $($item.name)" -ForegroundColor red
                    $Host.PrivateData.ProgressBackgroundColor='Red'
                    $accessFailed = $true
                }
            } else {
                $output = "Scanned file: $($item.name)"
            }
            $progress++
            Write-Progress -activity "Hiding dotfiles..." -currentOperation "$($output)" -status "Please wait until action completed... ($progress of $($folder.count))" -percentComplete (($progress / $folder.count) * 100)
        }

        if ($accessFailed) {
            $Host.PrivateData.ProgressBackgroundColor='Magenta'
            Write-Progress -activity "Unable to hide dotfiles." -status "Failed to hide target files."
        } elseif ($isMakeup) {
            $Host.PrivateData.ProgressBackgroundColor='Green'
            Write-Progress -activity "Hid dotfiles." -status "Successfully deleted target files."
        } else {
            $Host.PrivateData.ProgressBackgroundColor='Green'
            Write-Progress -activity "Hid dotfiles." -status "Requirements already satisfied."
        }
        Start-Sleep -milliseconds 800
        Write-Progress "N/A" "N/A" -completed
        $Host.PrivateData.ProgressBackgroundColor='DarkCyan'
    } else {
        Write-Host "Hiding dotfiles in $targetDir... Skipping!"
    }
}

# Remove incompatible cache files with this script
Write-Host "Removing vscodevim cache files incompatible with this script..." -NoNewLine
if ((Test-Path -Path $vscodevim) -and ((Test-Path -Path $vscode_cmd) -or (Test-Path -Path $vscode_search))) {
    Remove-Item "$vscode_cmd" 2>$null
    Remove-Item "$vscode_search" 2>$null
    Write-Host " Done!"
} else {
    Write-Host " Skipping!"
}

# Hide dotfiles in target dir path
Hide-Dotfiles $userDir
Hide-Dotfiles $externalDir

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

Write-Host "`n`nPowerShell HideHidden.ps1 has been terminated."
