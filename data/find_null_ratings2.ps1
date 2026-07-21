[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$cities = @('penghu','taitung','kinmen','yilan','yunlin','miaoli','nantou','chiayi','changhua','hsinchu','keelung','hualien','pingtung','taoyuan','tainan','taichung','taipei','newtaipei','kaohsiung')

foreach ($city in $cities) {
    $path = "C:\Users\USER\.openclaw\workspace\nova-pages\data\$city.json"
    if (Test-Path $path) {
        $data = Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json
        
        # Check spots section
        if ($data.spots) {
            $spots = $data.spots
            $nullRatingSpots = @()
            foreach ($s in $spots) {
                if ($null -eq $s.rating -or '' -eq $s.rating -or 0 -eq $s.rating) {
                    $nullRatingSpots += $s
                }
            }
            if ($nullRatingSpots.Count -gt 0) {
                Write-Host "$city spots: total=$($spots.Count) nullRating=$($nullRatingSpots.Count)"
                $nullRatingSpots | Select-Object -First 3 | ForEach-Object {
                    Write-Host "  -> name=$($_.name) district=$($_.district) rating=$($_.rating) reviews=$($_.reviews)"
                }
            }
        }
        
        # Check food section
        if ($data.food) {
            $food = $data.food
            $nullRatingFood = @()
            foreach ($f in $food) {
                if ($null -eq $f.rating -or '' -eq $f.rating -or 0 -eq $f.rating) {
                    $nullRatingFood += $f
                }
            }
            if ($nullRatingFood.Count -gt 0) {
                Write-Host "$city food: total=$($food.Count) nullRating=$($nullRatingFood.Count)"
                $nullRatingFood | Select-Object -First 3 | ForEach-Object {
                    Write-Host "  -> name=$($f.name) district=$($f.district) rating=$($f.rating) reviews=$($f.reviews)"
                }
            }
        }
    }
}