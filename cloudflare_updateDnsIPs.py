import requests
import json
from jproperties import Properties
from concurrent.futures import ThreadPoolExecutor

class CloudflareDNSUpdater:
    def __init__(self, api_token, zone_id):
        self.api_token = api_token
        self.zone_id = zone_id
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def get_wan_ip(self):
        ip_response = requests.get("https://api.ipify.org?format=json")
        return ip_response.json()["ip"]

    def get_dns_records(self):
        response = requests.get(f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records", headers=self.headers)
        dns_records = response.json()["result"]
        return dns_records

    def update_dns_record(self, dns_record, wan_ip):
        dns_name = dns_record["name"]
        dns_type = dns_record["type"]
        dns_id = dns_record["id"]
        dns_ip = dns_record["content"]

        if dns_type == "A" and dns_ip != wan_ip:
            update_payload = {
                "type": dns_type,
                "name": dns_name,
                "content": wan_ip,
                "proxied": True
            }
            update_response = requests.put(f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{dns_id}", headers=self.headers, json=update_payload)

            if update_response.status_code == 200:
                print(f"Updated DNS record '{dns_name}' with IP '{wan_ip}'")
            else:
                print(f"Failed to update DNS record '{dns_name}' with IP '{wan_ip}'")

    def update_dns_records(self):
        wan_ip = self.get_wan_ip()
        dns_records = self.get_dns_records()

        with ThreadPoolExecutor() as executor:
            for record in dns_records:
                executor.submit(self.update_dns_record, record, wan_ip)

# Get your Cloudflare API Token and Zone ID from secrets.properties
configs = Properties()
with open('secrets.properties', 'rb') as config_file:
    configs.load(config_file)

api_token = configs.get("API_KEY").data
zone_id = configs.get("ZONE_ID").data

# Create CloudflareDNSUpdater instance
dns_updater = CloudflareDNSUpdater(api_token, zone_id)

# Update DNS records with current WAN IP
dns_updater.update_dns_records()