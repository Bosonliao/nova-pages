[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$data = Get-Content 'C:\Users\USER\.openclaw\workspace\nova-pages\data\keelung.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$items = @()
if ($data.routes) { $items = $data.routes } else { $items = $data }
Write-Host "Total items: $($items.Count)"
Write-Host "--- First item structure ---"
$items[0] | ConvertTo-Json -Depth 5
Write-Host "--- Second item structure ---"
$items[1] | ConvertTo-Json -Depth 5