# Read the secrets.properties file
$secrets = Get-Content -Path "secrets.properties" | ConvertFrom-StringData

# Set the Cloudflare API credentials
$zoneId = $secrets.zone_id
$apiToken = $secrets.api_key

# Get the machine's WAN IP address
$wanIp = Invoke-RestMethod -Uri "https://api.ipify.org?format=json" | Select-Object -ExpandProperty ip

# Get the DNS records from Cloudflare
$dnsRecords = Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$zoneId/dns_records" -Headers @{
    "Authorization" = "Bearer $apiToken"
} | Select-Object -ExpandProperty result

# Loop through each DNS record
foreach ($record in $dnsRecords) {
    # Check if the record's IP is different from the machine's WAN IP
    if ($record.content -ne $wanIp -and $record.type -eq "A") {
        # Update the DNS record with the machine's WAN IP
        $recordData = @{
            "type" = $record.type
            "name" = $record.name
            "content" = $wanIp
            "proxied" = $True
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$zoneId/dns_records/$($record.id)" -Method PUT -Headers @{
            "Authorization" = "Bearer $apiToken"
            "Content-Type" = "application/json"
        } -Body $recordData

        $responseCode = $response.success

        if ($responseCode -eq 'True') {
            Write-Host "Updated DNS record $($record.name) with IP $wanIp"
        } else {
            Write-Host "Failed to update DNS record $($record.name)"
        }
    }
}