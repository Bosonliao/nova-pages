[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$cities = @('penghu','taitung','kinmen','yilan','yunlin','miaoli','nantou','chiayi','changhua','hsinchu','keelung','hualien','pingtung','taoyuan','tainan','taichung','taipei','newtaipei','kaohsiung')

$results = @()
foreach ($city in $cities) {
    $path = "C:\Users\USER\.openclaw\workspace\nova-pages\data\$city.json"
    if (Test-Path $path) {
        $data = Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json
        $items = if ($data.routes) { $data.routes } else { $data }
        $nullRatings = @()
        foreach ($item in $items) {
            $rating = $item.rating
            if ($null -eq $rating -or '' -eq $rating -or 0 -eq $rating) {
                $nullRatings += $item
            }
        }
        if ($nullRatings.Count -gt 0) {
            $results += [PSCustomObject]@{
                City = $city
                Total = $items.Count
                NullRating = $nullRatings.Count
                Sample = ($nullRatings | Select-Object -First 3 | ForEach-Object { $_.name }) -join '; '
            }
        }
    }
}

$results | Format-Table -AutoSize
Write-Host "`n--- Details ---"
foreach ($r in $results) {
    Write-Host "`n$($r.City) ($($r.NullRating) null ratings):"
    $path = "C:\Users\USER\.openclaw\workspace\nova-pages\data\$($r.City).json"
    $data = Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json
    $items = if ($data.routes) { $data.routes } else { $data }
    $nullRatings = @()
    foreach ($item in $items) {
        $rating = $item.rating
        if ($null -eq $rating -or '' -eq $rating -or 0 -eq $rating) {
            $nullRatings += $item
        }
    }
    $nullRatings | Select-Object -First 5 | ForEach-Object {
        $name = $_.name
        $district = $_.district
        $rating = $_.rating
        $reviews = $_.reviews
        Write-Host "  name=$name | district=$district | rating=$rating | reviews=$reviews"
    }
}