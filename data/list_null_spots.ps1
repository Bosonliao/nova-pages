[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$path = "C:\Users\USER\.openclaw\workspace\nova-pages\data\taoyuan.json"
$data = Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json
$spots = $data.spots
$nullSpots = @()
foreach ($s in $spots) {
    if ($null -eq $s.rating -or '' -eq $s.rating -or 0 -eq $s.rating) {
        $nullSpots += $s
    }
}
Write-Host "Total null-rating spots: $($nullSpots.Count)"
$i = 0
foreach ($s in $nullSpots) {
    $i++
    Write-Host "$i. name=$($s.name) district=$($s.district) rating=$($s.rating) reviews=$($s.reviews)"
}