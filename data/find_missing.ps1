$dir = "C:\Users\USER\.openclaw\workspace\nova-pages\data"
$files = Get-ChildItem -Path $dir -Filter "*.json" | Where-Object { $_.Name -notmatch 'drinks|osm|cities|meta|nightmarkets|search_results|geocoded' }

foreach ($f in $files) {
    try {
        $content = Get-Content $f.FullName -Raw -Encoding UTF8
        $json = $content | ConvertFrom-Json
        $missing = @()
        foreach ($item in $json) {
            if ($null -eq $item.rating -or $item.rating -eq 0) {
                $missing += $item
            }
        }
        if ($missing.Count -gt 0) {
            Write-Host "$($f.Name): $($missing.Count) missing"
            foreach ($m in $missing) {
                Write-Host "  - $($m.name) | area: $($m.area)"
            }
        }
    } catch {
        Write-Host "$($f.Name): ERROR parsing"
    }
}