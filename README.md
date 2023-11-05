# Python - Cloudflare Auto Update DNS Record IPs
Python script that updates DNS records on Cloudflare with the current WAN IP address. Below are the instructions to use this code:

1. Install Required Libraries:

   - Ensure that you have the necessary libraries installed by running the following command:
     ```python
     pip install requests jproperties
     ```

2. Obtain Cloudflare API Token and Zone ID:
   - Before running the script, you need to obtain your Cloudflare API Token and Zone ID.
   - Create a file named `secrets.properties` in the same directory as the script.
   - Open the `secrets.properties` file and add the following lines:

     ```
     API_KEY=<your_api_token>
     ZONE_ID=<your_zone_id>
     ```
   - Replace `<your_api_token>` with your Cloudflare API Token.
   - Replace `<your_zone_id>` with your Cloudflare Zone ID.

3. Understand the Methods:
   - The `get_wan_ip` method retrieves the current WAN IP using the ipify API.
   - The `get_dns_records` method retrieves the existing DNS records for the specified zone ID.
   - The `update_dns_record` method updates a single DNS record if its type is "A" and the IP is different from the current WAN IP.
   - The `update_dns_records` method gets the current WAN IP and DNS records, and then uses a `ThreadPoolExecutor` to concurrently update the DNS records using multiple threads.
   - The main code creates an instance of `CloudflareDNSUpdater` and calls the `update_dns_records` method to update the DNS records.

4. Execute the Script:
   - To execute the script manually, run the following command in your terminal:

     ```python
     python cloudflare-updateDnsIPs.py
     ```
   - The script will retrieve the WAN IP address, fetch the DNS records from Cloudflare, and update any A-type records with a different IP address.

5. Add Script to Scheduler:
   - Once you have verified the script runs without errors, you can set it to a scheduler to run automatically. I used crontab to do this.
   - To add script to crontab and to run every hour, run the following command:

      ```crontab -e
      0 * * * * python cloudflare-updateDnsIPs.py > /dev/null 2>&1
      ```

6. Review the Output:
   - The script will print the status of each DNS record update.
   - If a DNS record is successfully updated, it will print: `Updated DNS record '<dns_name>' with IP '<wan_ip>'`.
   - If a DNS record fails to update, it will print: `Failed to update DNS record '<dns_name>' with IP '<wan_ip>'`.


# PowerShell - Cloudflare Auto Update DNS Record IPs
PowerShell script that updates DNS records on Cloudflare with the current WAN IP address. Below are the instructions to use this code:

1. Obtain Cloudflare API Token and Zone ID:
   - Before running the script, you need to obtain your Cloudflare API Token and Zone ID.
   - Create a file named `secrets.properties` in the same directory as the script.
   - Open the `secrets.properties` file and add the following lines:

     ```
     API_KEY=<your_api_token>
     ZONE_ID=<your_zone_id>
     ```
   - Replace `<your_api_token>` with your Cloudflare API Token.
   - Replace `<your_zone_id>` with your Cloudflare Zone ID.

2. Understand the variables and steps:
   - The `$wanIp` method retrieves the current WAN IP using the ipify API.
   - The `$dnsRecords` method retrieves the existing DNS records for the specified zone ID.
   - The `foreach ($record in $dnsRecords)` loops through the `dnsRecords`
   - The `$response` method in conjuntion with the `if ($record.type -eq "A" -and $record.content -ne $wanIp)` condition updates a single DNS record if its type is "A" and the IP is different from the current WAN IP.

3. Execute the Script:
   - To execute the script manually, run the following command in your terminal:

     ```powershell
     .\cloudflare-updateDnsIPs.ps1
     ```
   - The script will retrieve the WAN IP address, fetch the DNS records from Cloudflare, and update any A-type records with a different IP address.

4. Add Script to Windows Scheduler:
   - Once you have verified the script runs without errors, you can set it to a scheduler to run automatically.

5. Review the Output:
   - The script will print the status of each DNS record update.
   - If a DNS record is successfully updated, it will print: `Updated DNS record $($record.name) with IP $wanIp`.
   - If a DNS record fails to update, it will print: `Failed to update DNS record $($record.name)'`.
