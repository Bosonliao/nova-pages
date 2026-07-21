$cities = @('penghu','taitung','kinmen','yilan','yunlin','miaoli','nantou','chiayi','changhua','hsinchu','keelung','hualien','pingtung','taoyuan','tainan','taichung','taipei','newtaipei','kaohsiung')

foreach ($city in $cities) {
    $path = "C:\Users\USER\.openclaw\workspace\nova-pages\data\$city.json"
    if (Test-Path $path) {
        $data = Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json
        $nullRatings = @()
        foreach ($item in $data) {
            if ($null -eq $item.rating -or '' -eq $item.rating -or 0 -eq $item.rating) {
                $nullRatings += $item
            }
        }
        Write-Host "$city : total=$($data.Count) nullRating=$($nullRatings.Count)"
        if ($nullRatings.Count -gt 0 -and $nullRatings.Count -le 200) {
            # Show first 5 null-rating shop names
            $nullRatings | Select-Object -First 5 | ForEach-Object { Write-Host "  - $($_.name) ($($_.district))" }
        }
    }
}