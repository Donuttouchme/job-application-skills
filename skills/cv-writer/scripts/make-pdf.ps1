# make-pdf.ps1 - render an HTML file to PDF with headless Edge or Chrome.
#
#   .\make-pdf.ps1 -Html "~/job-search/applications/.../letter.html" `
#                  -Pdf  "~/job-search/applications/.../letter.pdf"
#
# Exits non-zero and explains itself on failure. Never fails silently.
#
# TWIN FILE: an identical copy lives in motivational-letter\scripts\make-pdf.ps1.
# Duplicated on purpose - coupling two skills through a cross-directory path is
# more fragile than maintaining a twin. Change both together.

param(
    [Parameter(Mandatory = $true)][string]$Html,
    [Parameter(Mandatory = $true)][string]$Pdf
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Html)) {
    Write-Error "Source HTML not found: $Html"
    exit 1
}

# Edge first (x86 path, then x64), Chrome as a fallback.
$candidates = @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$browser = $null
foreach ($c in $candidates) {
    if (Test-Path -LiteralPath $c) { $browser = $c; break }
}

if ($null -eq $browser) {
    Write-Error @"
No Edge or Chrome found, so the PDF cannot be rendered.
The HTML is complete and ready at:
  $Html
Open it in a browser and use Ctrl+P -> Save as PDF (A4, no headers/footers).
"@
    exit 2
}

$htmlFull = (Resolve-Path -LiteralPath $Html).Path
$uri = ([System.Uri]$htmlFull).AbsoluteUri

# A throwaway profile avoids clashing with a running browser instance.
$profileDir = Join-Path $env:TEMP ("letter-pdf-" + [guid]::NewGuid().ToString('N'))

# Not $args - that is an automatic variable in PowerShell.
#
# ONE QUOTED STRING, not an array. Start-Process joins an array with spaces and
# does not quote the elements, so a destination path containing a space - for
# example "C:/My Job Search/..." - reaches the browser split in two and it dies with
#   "Multiple targets are not supported in headless mode."
# Quoting each path here is the fix. Do not turn this back into an array.
$browserArgs = '--headless=new --disable-gpu --no-pdf-header-footer ' +
    ('--user-data-dir="{0}" --print-to-pdf="{1}" "{2}"' -f $profileDir, $Pdf, $uri)

if (Test-Path -LiteralPath $Pdf) { Remove-Item -LiteralPath $Pdf -Force }

# Start-Process -Wait, not the call operator: the browser detaches and the call
# operator returns before the PDF has been written.
Start-Process -FilePath $browser -ArgumentList $browserArgs -Wait -NoNewWindow | Out-Null

try { Remove-Item -LiteralPath $profileDir -Recurse -Force -ErrorAction Stop } catch {}

if (-not (Test-Path -LiteralPath $Pdf)) {
    Write-Error "$(Split-Path -Leaf $browser) ran but produced no PDF at: $Pdf"
    exit 3
}

$size = (Get-Item -LiteralPath $Pdf).Length
if ($size -lt 1024) {
    Write-Error "PDF at $Pdf is only $size bytes - the render almost certainly failed."
    exit 4
}

Write-Output "PDF written: $Pdf ($([math]::Round($size / 1KB, 1)) KB)"
