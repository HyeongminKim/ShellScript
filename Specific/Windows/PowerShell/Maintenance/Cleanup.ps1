# User directory name
$whoami = "$env:USERNAME"

# Value for progress bar only
$deleteFailed = $false
$isMakeup = $false

# Start cleanup Downloads directory function
Write-Host "Removing files with extension exe in download directory..."
$target = Get-ChildItem -Recurse "C:\Users\$whoami\Downloads\*" -Include *.exe -Force
$progress = 0
foreach ($item in $target) {
    Remove-Item "$item" -Force 2>$null
    if ($?) {
        Get-Item "$item" 2>$null
        if ($?) {
            $output = "Access denied. unable to delete this file: $($item.name)"
            Write-Host "Access denied. unable to delete this file: $($item)" -ForegroundColor red
            $Host.PrivateData.ProgressBackgroundColor='Red'
            $deleteFailed = $true
        } else {
            $output = "Deleted file: $($item.name)"
            Write-Host "The $($item) executable has been deleted."
            $isMakeup = $true
            $Host.PrivateData.ProgressBackgroundColor='DarkCyan'
        }
    } else {
        $output = "Access denied. unable to delete this file: $($item.name)"
        Write-Host "Access denied. unable to delete this file: $($item)" -ForegroundColor red
        $Host.PrivateData.ProgressBackgroundColor='Red'
        $deleteFailed = $true
    }
    $progress++
    Write-Progress -activity "Cleanup downloads directory..." -currentOperation "$($output)" -status "Please wait until action completed... ($progress of $($target.count))" -percentComplete (($progress / $target.count) * 100)
}

# Specify message when progress bar completes
if ($deleteFailed) {
    $Host.PrivateData.ProgressBackgroundColor='Margenta'
    Write-Progress -activity "Unable to cleanup downloads directory." -status "Failed to delete target files."
} elseif ($isMakeup) {
    $Host.PrivateData.ProgressBackgroundColor='Green'
    Write-Progress -activity "Cleaned up downloads directory." -status "Successfully deleted target files."
} else {
    $Host.PrivateData.ProgressBackgroundColor='Green'
    Write-Progress -activity "Cleaned up downloads directory." -status "Requirements already satisfied."
}
Start-Sleep -milliseconds 800
Write-Progress "N/A" "N/A" -completed
$Host.PrivateData.ProgressBackgroundColor='DarkCyan'

# Start empty trash can function
Write-Host "Emptying the recycle bin of drive C..." -NoNewLine
Clear-RecycleBin -DriveLetter C -Force 2>$null
Write-Host " Done. "

