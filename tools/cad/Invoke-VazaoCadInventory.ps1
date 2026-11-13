[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot "..\..\reports\cad-inventory"),
    [switch]$SkipKnownPathScan
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-RegistryInstalledApplications {
    $roots = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )
    $items = @()
    foreach ($root in $roots) {
        $base = $root -replace '\\\*$', ''
        if (Test-Path -LiteralPath $base) {
            $items += Get-ItemProperty -Path $root -ErrorAction SilentlyContinue |
                Where-Object { $_.DisplayName } |
                ForEach-Object {
                    [pscustomobject]@{
                        Name = [string]$_.DisplayName
                        Version = [string]$_.DisplayVersion
                        Publisher = [string]$_.Publisher
                        InstallLocation = [string]$_.InstallLocation
                        DisplayIcon = [string]$_.DisplayIcon
                        RegistrySource = $root
                    }
                }
        }
    }
    return @($items | Sort-Object Name, Version -Unique)
}

function Get-ExecutableEvidence {
    param([string[]]$Names)
    $results = @()
    foreach ($name in $Names) {
        foreach ($command in @(Get-Command $name -All -ErrorAction SilentlyContinue)) {
            $results += [pscustomobject]@{
                Command = $name
                Path = [string]$command.Source
                Type = [string]$command.CommandType
            }
        }
    }
    return $results
}

function Get-KnownPathEvidence {
    $programFilesX86 = (Get-Item -LiteralPath "Env:ProgramFiles(x86)" -ErrorAction SilentlyContinue).Value
    $roots = @(
        $env:ProgramFiles, $programFilesX86,
        "$env:LOCALAPPDATA\Programs"
    ) | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -Unique
    $patterns = @(
        "FreeCAD.exe", "FreeCADCmd.exe", "FreeCADGUI.exe", "acad.exe",
        "Inventor.exe", "SLDWORKS.exe", "QCAD.exe", "librecad.exe",
        "bricscad.exe", "DraftSight.exe", "FusionLauncher.exe",
        "Fusion360.exe", "kicad.exe", "pcbnew.exe"
    )
    $found = @()
    foreach ($root in $roots) {
        foreach ($pattern in $patterns) {
            try {
                $found += Get-ChildItem -LiteralPath $root -Filter $pattern -File -Recurse -ErrorAction SilentlyContinue |
                    Select-Object -First 20 -ExpandProperty FullName
            } catch { }
        }
    }
    return @($found | Sort-Object -Unique)
}

function Get-CadClassification {
    param([object[]]$Applications, [object[]]$Executables, [string[]]$Paths)
    $allText = @(
        $Applications | ForEach-Object { "$($_.Name) $($_.Publisher) $($_.InstallLocation) $($_.DisplayIcon)" }
        $Executables | ForEach-Object { "$($_.Command) $($_.Path)" }
        $Paths
    ) -join [Environment]::NewLine
    $families = @(
        @{ Name = "FreeCAD"; Pattern = "(?i)FreeCAD" },
        @{ Name = "Autodesk AutoCAD"; Pattern = "(?i)AutoCAD|acad\.exe" },
        @{ Name = "Autodesk Inventor"; Pattern = "(?i)Inventor" },
        @{ Name = "Autodesk Fusion"; Pattern = "(?i)Fusion 360|Autodesk Fusion|FusionLauncher" },
        @{ Name = "SOLIDWORKS"; Pattern = "(?i)SOLIDWORKS|SLDWORKS" },
        @{ Name = "BricsCAD"; Pattern = "(?i)BricsCAD" },
        @{ Name = "DraftSight"; Pattern = "(?i)DraftSight" },
        @{ Name = "QCAD"; Pattern = "(?i)QCAD" },
        @{ Name = "LibreCAD"; Pattern = "(?i)LibreCAD" },
        @{ Name = "KiCad (ECAD, not mechanical CAD)"; Pattern = "(?i)KiCad|pcbnew\.exe" }
    )
    foreach ($family in $families) {
        [pscustomobject]@{
            ProductFamily = $family.Name
            EvidenceFound = [bool]($allText -match $family.Pattern)
            Note = if ($family.Name -like "KiCad*") { "ECAD evidence only; not mechanical CAD." } else { "Presence evidence is not proof of a working installation." }
        }
    }
}

$timestamp = Get-Date
$os = Get-CimInstance Win32_OperatingSystem
$computer = Get-CimInstance Win32_ComputerSystem
$apps = @(Get-RegistryInstalledApplications)
$executables = @(Get-ExecutableEvidence -Names @(
    "FreeCAD", "FreeCADCmd", "FreeCADGUI", "acad", "Inventor",
    "SLDWORKS", "QCAD", "librecad", "bricscad", "DraftSight",
    "FusionLauncher", "kicad", "pcbnew"
))
$paths = @()
if (-not $SkipKnownPathScan) { $paths = @(Get-KnownPathEvidence) }
$classifications = @(Get-CadClassification -Applications $apps -Executables $executables -Paths $paths)

$report = [ordered]@{
    ReportType = "VAZAO_EVSE_CAD_WORKSTATION_INVENTORY"
    GeneratedAtLocal = $timestamp.ToString("o")
    Computer = [ordered]@{
        Name = $computer.Name
        Manufacturer = $computer.Manufacturer
        Model = $computer.Model
        Domain = $computer.Domain
    }
    OperatingSystem = [ordered]@{
        Caption = $os.Caption
        Version = $os.Version
        BuildNumber = $os.BuildNumber
        Architecture = $os.OSArchitecture
    }
    PowerShell = [ordered]@{
        Version = $PSVersionTable.PSVersion.ToString()
        Edition = $PSVersionTable.PSEdition
    }
    CadFamilyEvidence = $classifications
    ExecutableEvidence = $executables
    KnownExecutablePaths = $paths
    InstalledApplications = $apps
    Limitations = @(
        "Read-only inventory; no software installed, removed, launched or modified.",
        "Registry entries and executable paths are presence evidence only.",
        "No native CAD save/reopen, STEP/DXF import/export, geometry or parametric test was run.",
        "Portable installs, custom paths, Store apps and browser CAD services may not be fully detected.",
        "KiCad is ECAD and is not classified as a mechanical CAD authoring tool."
    )
}
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$stamp = $timestamp.ToString("yyyyMMdd-HHmmss")
$jsonPath = Join-Path $OutputDirectory "VAZAO-CAD-INVENTORY-$stamp.json"
$mdPath = Join-Path $OutputDirectory "VAZAO-CAD-INVENTORY-$stamp.md"
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$lines = @(
    "# VAZÃO EVSE — CAD workstation inventory", "",
    "- Generated: $($timestamp.ToString("yyyy-MM-dd HH:mm:ss zzz"))",
    "- Computer: $($computer.Name)",
    "- OS: $($os.Caption) $($os.Version) ($($os.OSArchitecture))",
    "- PowerShell: $($PSVersionTable.PSVersion)", "",
    "## CAD family evidence", "",
    "| Family | Evidence found | Note |", "|---|---:|---|"
)
foreach ($item in $classifications) {
    $lines += "| $($item.ProductFamily) | $($item.EvidenceFound) | $($item.Note) |"
}
$lines += @("", "## Executable paths", "")
if ($paths.Count -eq 0 -and $executables.Count -eq 0) { $lines += "No known CAD executable path or command was detected." }
foreach ($item in $executables) { $lines += "- Command '$($item.Command)': '$($item.Path)'" }
foreach ($item in $paths) { $lines += "- '$item'" }
$lines += @("", "## Installed application records", "")
foreach ($app in $apps) {
    if ($app.Name -match "(?i)CAD|FreeCAD|Autodesk|Inventor|SolidWorks|BricsCAD|DraftSight|QCAD|LibreCAD|KiCad") {
        $lines += "- **$($app.Name)** — version '$($app.Version)'; publisher: $($app.Publisher); location: '$($app.InstallLocation)'"
    }
}
$lines += @("", "## Limitations", "")
foreach ($limitation in $report.Limitations) { $lines += "- $limitation" }
$lines -join [Environment]::NewLine | Set-Content -LiteralPath $mdPath -Encoding UTF8

[pscustomobject]@{
    Status = "COMPLETED"
    JsonReport = (Resolve-Path -LiteralPath $jsonPath).Path
    MarkdownReport = (Resolve-Path -LiteralPath $mdPath).Path
    InstalledApplicationRecords = $apps.Count
    ExecutableEvidenceCount = $executables.Count
    KnownExecutablePathCount = $paths.Count
    Note = "Inventory only. No CAD application was launched and no format test was performed."
} | Format-List
