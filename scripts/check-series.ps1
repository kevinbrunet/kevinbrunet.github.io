param(
    [Parameter(Mandatory)][string]$Series,
    [Parameter(Mandatory)][ValidateRange(1, 999)][int]$ExpectedCount,
    [string]$SourceDirectory,
    [string]$PreviewUrl
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
function Read-Utf8([string]$Path) {
    $value = [IO.File]::ReadAllText($Path, $strictUtf8)
    if ($value.Contains([char]0xFFFD)) { throw "Replacement character in $Path" }
    return $value
}
function Assert-Check([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}
function Field([string]$Text, [string]$Name) {
    $match = [regex]::Match($Text, '(?m)^' + [regex]::Escape($Name) + ':\s*(.+?)\s*$')
    Assert-Check $match.Success "Missing metadata: $Name"
    return $match.Groups[1].Value.Trim('"')
}
function Output-Path([string]$Url) {
    $uri = [uri]::new([uri]'https://kevinbrunet.github.io/', $Url)
    $relative = [uri]::UnescapeDataString($uri.AbsolutePath).TrimStart('/')
    if ($relative -eq '' -or $relative.EndsWith('/')) { $relative += 'index.html' }
    return Join-Path (Join-Path $root 'public') $relative
}
function Check-Page([string]$Url) {
    $path = Output-Path $Url
    Assert-Check (Test-Path -LiteralPath $path) "Missing page: $Url"
    $html = Read-Utf8 $path
    Assert-Check (-not $html.Contains('raw HTML omitted')) "Omitted HTML: $Url"
    foreach ($match in [regex]::Matches($html, '(?:href|src)="([^"]+)"')) {
        $link = [System.Net.WebUtility]::HtmlDecode($match.Groups[1].Value)
        $uri = [uri]::new([uri]('https://kevinbrunet.github.io' + $Url), $link)
        if ($uri.Host -ne 'kevinbrunet.github.io') { continue }
        $target = Output-Path $uri.AbsolutePath
        Assert-Check (Test-Path -LiteralPath $target) "Broken local link in ${Url}: $link"
        if ($uri.Fragment -and $target.EndsWith('.html')) {
            $id = [uri]::UnescapeDataString($uri.Fragment.Substring(1))
            Assert-Check ((Read-Utf8 $target).Contains('id="' + $id + '"')) "Missing anchor in ${Url}: $link"
        }
    }
    if ($PreviewUrl) {
        $live = (Invoke-WebRequest ($PreviewUrl.TrimEnd('/') + $Url)).Content
        Assert-Check (-not $live.Contains([char]0xFFFD)) "Preview encoding error: $Url"
        foreach ($class in @('prose', 'series-next', 'index-list', 'article-cover', 'language-switcher')) {
            $pattern = '(?s)<(?:div|section|figure|span)[^>]*class="' + $class + '"[^>]*>.*?</(?:div|section|figure|span)>'
            $builtPart = [regex]::Match($html, $pattern).Value
            $livePart = [regex]::Match($live, $pattern).Value
            Assert-Check ($builtPart -eq $livePart) "Preview differs from build ($class): $Url"
        }
    }
    return $html
}

$contentDir = Join-Path $root "content/articles/$Series"
$files = @(Get-ChildItem -LiteralPath $contentDir -File -Filter '*.md' | Where-Object Name -NotLike '_index*')
$frFiles = @($files | Where-Object Name -NotLike '*.en.md' | Sort-Object Name)
$enFiles = @($files | Where-Object Name -Like '*.en.md' | Sort-Object Name)
Assert-Check ($frFiles.Count -eq $ExpectedCount -and $enFiles.Count -eq $ExpectedCount) 'Incorrect bilingual article count'
if ($SourceDirectory) {
    $sourceFiles = @(Get-ChildItem -LiteralPath $SourceDirectory -File -Filter '*.md' | Where-Object {
        $text = Read-Utf8 $_.FullName
        $text -match ('Article \d+/' + $ExpectedCount + '\b')
    } | Sort-Object Name)
    Assert-Check (($sourceFiles.Name -join '|') -eq ($frFiles.Name -join '|')) 'Source episode inventory differs'
}

$urls = @{ fr = @(); en = @() }
$seenSlugs = @{}
for ($i = 0; $i -lt $ExpectedCount; $i++) {
    $fr = Read-Utf8 $frFiles[$i].FullName
    $enPath = $frFiles[$i].FullName -replace '\.md$', '.en.md'
    Assert-Check (Test-Path -LiteralPath $enPath) 'Missing translation pair'
    $en = Read-Utf8 $enPath
    foreach ($name in @('series', 'series_order', 'date', 'draft', 'collection')) {
        Assert-Check ((Field $fr $name) -eq (Field $en $name)) "Translation metadata differs: $name"
    }
    Assert-Check ((Field $fr 'series') -eq ('["' + $Series + '"]')) 'Wrong series ID'
    Assert-Check ([int](Field $fr 'series_order') -eq ($i + 1)) 'Non-continuous episode order'
    foreach ($lang in @('fr', 'en')) {
        $text = if ($lang -eq 'fr') { $fr } else { $en }
        $slug = Field $text 'slug'
        Assert-Check (-not $seenSlugs.ContainsKey("$lang/$slug")) 'Duplicate slug'
        $seenSlugs["$lang/$slug"] = $true
        $prefix = if ($lang -eq 'en') { '/en' } else { '' }
        $urls[$lang] += "$prefix/articles/$slug/"
        $cover = Field $text 'cover'
        Assert-Check ($cover.EndsWith(".$lang.png") -and -not $cover.Contains('.base.')) 'Cover language mismatch'
        Assert-Check (Test-Path -LiteralPath (Join-Path $root ('static' + $cover))) 'Missing final cover'
        $sources = ($text -split '(?m)^## Sources\s*$', 2)[1].Trim()
        Assert-Check (-not ($sources -match '✓|✗|~|vérification|à confirmer|audit')) 'Working annotations in sources'
        foreach ($line in ($sources -split '\r?\n' | Where-Object { $_.Trim() })) {
            Assert-Check ($line -match '^- .*\[[^\]]+\]\((?:https?://|/)[^)]+\)') 'Source is not an identifiable linked reference'
        }
    }
    $frLinks = @([regex]::Matches($fr, '\]\((https?://[^)]+)\)') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $enLinks = @([regex]::Matches($en, '\]\((https?://[^)]+)\)') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    Assert-Check (($frLinks -join '|') -eq ($enLinks -join '|')) 'External references differ between languages'
    foreach ($code in [regex]::Matches($fr, '(?s)```json\r?\n(.*?)```')) {
        Assert-Check ($en.Replace("`r", '').Contains($code.Value.Replace("`r", ''))) 'JSON example changed in translation'
    }
}

foreach ($lang in @('fr', 'en')) {
    $prefix = if ($lang -eq 'en') { '/en' } else { '' }
    $seriesUrl = "$prefix/series/$Series/"
    $indexPath = Join-Path $root ("content/series/$Series/_index" + $(if ($lang -eq 'en') { '.en' }) + '.md')
    Assert-Check (Test-Path -LiteralPath $indexPath) 'Missing series landing page'
    $seriesHtml = Check-Page $seriesUrl
    $list = [regex]::Match($seriesHtml, '(?s)<section class="index-list".*?</section>').Value
    $links = @([regex]::Matches($list, '<a href="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    Assert-Check (($links -join '|') -eq ($urls[$lang] -join '|')) 'Series page episode links are incomplete or out of order'
    for ($i = 0; $i -lt $ExpectedCount; $i++) {
        Assert-Check ($list.Contains(('>{0:00}</div>' -f ($i + 1)))) 'Series numbering is incomplete'
        $html = Check-Page $urls[$lang][$i]
        $nav = [regex]::Match($html, '(?s)<section class="series-next".*?</section>').Value
        $navLinks = @([regex]::Matches($nav, '<a href="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
        Assert-Check (($navLinks -join '|') -eq ($urls[$lang] -join '|')) 'Article navigation is incomplete or uses the wrong language'
        $other = if ($lang -eq 'fr') { 'en' } else { 'fr' }
        $switcher = [regex]::Match($html, '(?s)<span class="language-switcher".*?</span>').Value
        Assert-Check ($switcher.Contains('href="' + $urls[$other][$i] + '"')) 'Wrong article translation link'
        Assert-Check ($html.Contains('class="article-citation"')) 'Missing article citation'
        if ($lang -eq 'en') {
            Assert-Check (-not ($html -match 'CLASSÉ DANS|Couverture éditoriale|Continuer la série|aria-label="Lire ')) 'French interface text on English article'
        }
    }
    $otherPrefix = if ($lang -eq 'fr') { '/en' } else { '' }
    $switcher = [regex]::Match($seriesHtml, '(?s)<span class="language-switcher".*?</span>').Value
    Assert-Check ($switcher.Contains('href="' + "$otherPrefix/series/$Series/" + '"')) 'Wrong series translation link'
}
Write-Output "PASS: $Series — $ExpectedCount French articles, $ExpectedCount English articles, both series pages, metadata, sources, local links, covers, translations and complete ordered navigation."
if ($PreviewUrl) { Write-Output 'PASS: preview content matches the build.' }
