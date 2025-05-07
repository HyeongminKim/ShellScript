# 스크립트 설명
- [Cleanup.ps1](https://github.com/unstable-code/ShellScript/blob/master/Operating%20System/Windows/PowerShell/Cleanup.ps1): 다운로드 디렉토리의 exe 파일 청소 및 휴지통을 비우는 스크립트
- [HideHidden.ps1](https://github.com/unstable-code/ShellScript/blob/master/Operating%20System/Windows/PowerShell/HideHidden.ps1): Linux, macOS와 같이 dotfiles를 숨기는 스크립트
- [VerifyRecentfiles.ps1](https://github.com/unstable-code/ShellScript/blob/master/Operating%20System/Windows/PowerShell/VerifyRecentfiles.ps1): Windows 최근 사용 디렉토리를 청소하는 스크립트

### A powershell launcher for remotely loading desired scripts.

``` powershell
    iex ((New-Object System.Net.WebClient).DownloadString('<source>'))
```
