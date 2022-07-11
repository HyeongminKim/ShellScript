# User directory name
$whoami = "$env:USERNAME"

# User root paths
$userDir = "C:\Users\$whoami"
$externalDir = "E:\Users\$whoami"

# Incompatible cache files with this script
$vscodevim = "$userDir\AppData\Roaming\Code\User\globalStorage\vscodevim.vim"
$vscode_cmd = "$vscodevim\.cmdline_history"
$vscode_search = "$vscodevim\.search_history"

# Hide dotfiles function
function Hide-Dotfiles {
    param (
        [Parameter(Mandatory)]
        [string]$targetDir
    )

    Write-Host "Hiding dotfiles in $targetDir..." -NoNewLine
    if (Test-Path -Path $targetDir) {
        Get-ChildItem "$targetDir" -recurse -force 2>$null | Where-Object {$_.name -like ".*" -and $_.attributes -match 'Hidden' -eq $false} 2>$null | Set-ItemProperty -name Attributes -value ([System.IO.FileAttributes]::Hidden) 2>$null
        Write-Host " Done!"
    } else {
        Write-Host " Skipping!"
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
