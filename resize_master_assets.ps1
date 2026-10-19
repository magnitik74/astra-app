# Astra Multi-Resolution Asset Resizer
# Generates Journal (600x600) and Small (128x128) thumbnails from 1024x1024 master files.
param (
    [string]$SourceDir = "D:\projects\monly\фигасе\СОРТИРОВАННЫЕ_АССЕТЫ\00_ИКОНКИ_И_ЛОГОТИП_АСТРА",
    [string]$TargetDir = "D:\projects\monly\АСТРА_АССЕТЫ\00_ИКОНКИ_И_ЛОГОТИП_АСТРА"
)

Add-Type -AssemblyName System.Drawing

if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

function Resize-Image {
    param (
        [System.Drawing.Bitmap]$Original,
        [int]$Width,
        [int]$Height
    )
    $destBitmap = New-Object System.Drawing.Bitmap $Width, $Height
    $graphics = [System.Drawing.Graphics]::FromImage($destBitmap)
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $graphics.DrawImage($Original, 0, 0, $Width, $Height)
    $graphics.Dispose()
    return $destBitmap
}

$files = Get-ChildItem -Path $SourceDir -Filter "*1024x1024.png"

foreach ($file in $files) {
    Write-Host "Processing: $($file.Name)..." -ForegroundColor Cyan
    $img = [System.Drawing.Bitmap]::FromFile($file.FullName)
    
    # 1. Copy Master
    $masterDest = Join-Path $TargetDir $file.Name
    Copy-Item $file.FullName $masterDest -Force
    Write-Host "  -> Master saved: $masterDest"
    
    # 2. Resize to Journal (600x600)
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name) -replace "1024x1024", "journal_600x600"
    $journalDest = Join-Path $TargetDir ($baseName + ".png")
    $journalImg = Resize-Image -Original $img -Width 600 -Height 600
    $journalImg.Save($journalDest, [System.Drawing.Imaging.ImageFormat]::Png)
    $journalImg.Dispose()
    Write-Host "  -> Journal saved: $journalDest" -ForegroundColor Green
    
    # 3. Resize to Small (128x128)
    $smallName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name) -replace "1024x1024", "small_128x128"
    $smallDest = Join-Path $TargetDir ($smallName + ".png")
    $smallImg = Resize-Image -Original $img -Width 128 -Height 128
    $smallImg.Save($smallDest, [System.Drawing.Imaging.ImageFormat]::Png)
    $smallImg.Dispose()
    Write-Host "  -> Small saved: $smallDest" -ForegroundColor Yellow
    
    $img.Dispose()
}

Write-Host "Multi-resolution generation complete!" -ForegroundColor Green
