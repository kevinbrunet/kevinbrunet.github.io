param(
    [Parameter(Mandatory = $true)][string]$Source,
    [Parameter(Mandatory = $true)][string]$OutputDirectory
)

Add-Type -AssemblyName System.Drawing

$width = 1584
$height = 396
$navy = [System.Drawing.ColorTranslator]::FromHtml('#121C2B')
$paper = [System.Drawing.ColorTranslator]::FromHtml('#F3EFE6')
$cobalt = [System.Drawing.ColorTranslator]::FromHtml('#2457F5')
$coral = [System.Drawing.ColorTranslator]::FromHtml('#FF5A4E')

[System.IO.Directory]::CreateDirectory($OutputDirectory) | Out-Null

function New-BannerBase {
    param([string]$InputPath)

    $sourceImage = [System.Drawing.Image]::FromFile($InputPath)
    try {
        $canvas = New-Object System.Drawing.Bitmap($width, $height)
        $canvas.SetResolution(96, 96)
        $graphics = [System.Drawing.Graphics]::FromImage($canvas)
        try {
            $graphics.Clear($navy)
            $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
            $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

            # Crop the panoramic master to LinkedIn's 4:1 ratio while retaining
            # the empty portrait zone and the human-supervision station.
            $cropHeight = [int]($sourceImage.Width / 4)
            $cropY = [int](($sourceImage.Height - $cropHeight) * 0.53)
            $sourceRect = New-Object System.Drawing.Rectangle(0, $cropY, $sourceImage.Width, $cropHeight)
            $targetRect = New-Object System.Drawing.Rectangle(0, 0, $width, $height)
            $graphics.DrawImage($sourceImage, $targetRect, $sourceRect, [System.Drawing.GraphicsUnit]::Pixel)

            # A subtle veil protects the title from the illustration without
            # flattening the architectural drawing.
            $veilBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
                (New-Object System.Drawing.Point(0, 0)),
                (New-Object System.Drawing.Point(930, 0)),
                [System.Drawing.Color]::FromArgb(235, $navy),
                [System.Drawing.Color]::FromArgb(20, $navy)
            )
            try { $graphics.FillRectangle($veilBrush, 0, 0, 930, $height) }
            finally { $veilBrush.Dispose() }
        }
        finally { $graphics.Dispose() }
        return $canvas
    }
    finally { $sourceImage.Dispose() }
}

function Add-BannerText {
    param(
        [System.Drawing.Bitmap]$Base,
        [string]$Headline,
        [string]$Subline,
        [string]$OutputPath
    )

    $result = New-Object System.Drawing.Bitmap($Base)
    $graphics = [System.Drawing.Graphics]::FromImage($result)
    try {
        $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
        $headlineFont = New-Object System.Drawing.Font('Bahnschrift SemiCondensed', 32, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
        $sublineFont = New-Object System.Drawing.Font('Bahnschrift', 17, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
        $signatureFont = New-Object System.Drawing.Font('Bahnschrift', 13, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
        $paperBrush = New-Object System.Drawing.SolidBrush($paper)
        $cobaltBrush = New-Object System.Drawing.SolidBrush($cobalt)
        $coralBrush = New-Object System.Drawing.SolidBrush($coral)
        try {
            $graphics.FillRectangle($coralBrush, 94, 75, 42, 5)
            $graphics.DrawString($Headline, $headlineFont, $paperBrush, 94, 93)
            $graphics.DrawString($Subline, $sublineFont, $cobaltBrush, 96, 145)
            $graphics.DrawString('KÉVIN BRUNET', $signatureFont, $paperBrush, 96, 184)
        }
        finally {
            $headlineFont.Dispose(); $sublineFont.Dispose(); $signatureFont.Dispose()
            $paperBrush.Dispose(); $cobaltBrush.Dispose(); $coralBrush.Dispose()
        }
        $result.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    }
    finally {
        $graphics.Dispose()
        $result.Dispose()
    }
}

$basePath = Join-Path $OutputDirectory 'architecturer-la-confiance.banner.base.png'
$frPath = Join-Path $OutputDirectory 'architecturer-la-confiance.banner.fr.png'
$enPath = Join-Path $OutputDirectory 'architecturer-la-confiance.banner.en.png'

$base = New-BannerBase -InputPath $Source
try {
    $base.Save($basePath, [System.Drawing.Imaging.ImageFormat]::Png)
    Add-BannerText -Base $base -Headline 'ARCHITECTURER LA CONFIANCE' -Subline 'SYSTÈMES CRITIQUES · SaMD · AGENTS IA' -OutputPath $frPath
    Add-BannerText -Base $base -Headline 'ARCHITECTING TRUST' -Subline 'CRITICAL SYSTEMS · SaMD · AI AGENTS' -OutputPath $enPath
}
finally { $base.Dispose() }

Write-Output $basePath
Write-Output $frPath
Write-Output $enPath
