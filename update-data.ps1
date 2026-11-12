# 更新衛星軌道資料（需連網）。在此資料夾按右鍵「用 PowerShell 執行」即可。
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
$tle = (Invoke-WebRequest -Uri $url -UseBasicParsing -UserAgent 'Mozilla/5.0').Content -replace "`r", ''
if ($tle -notmatch "(?m)^1 \d{5}") { throw 'CelesTrak 回傳的內容不是 TLE 資料，未更新。' }
$stamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$js = "window.TLE_FETCHED=`"$stamp`";`nwindow.TLE_DATA=" + ($tle | ConvertTo-Json) + ';'
[IO.File]::WriteAllText((Join-Path $here 'data\tle.js'), $js, (New-Object System.Text.UTF8Encoding($false)))
$n = ([regex]::Matches($tle, "(?m)^1 ")).Count
Write-Host "已更新 $n 顆衛星的軌道資料 ($stamp)"
