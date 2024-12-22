import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

class ToffeeScraper:
    def __init__(self):
        """
        Initialize the scraper
        """
        self.base_url = "https://toffeelive.com"
        self.live_url = f"{self.base_url}/en/live"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        })
        self.cookies = self._get_cookies()

    def _get_cookies(self):
        """
        Extract Edge-Cache-Cookie from the website
        """
        try:
            print("Accessing Toffee Live...")
            response = self.session.get(self.live_url)
            
            if response.status_code != 200:
                print(f"Failed to fetch page. Status code: {response.status_code}")
                return None
            
            cookie_match = re.search(r'Edge-Cache-Cookie=([^;\\]+)', response.text)
            if cookie_match:
                edge_cache_cookie = f"Edge-Cache-Cookie={cookie_match.group(1)}"
                print("\nSuccessfully extracted Edge-Cache-Cookie:")
                print(edge_cache_cookie)
                return edge_cache_cookie
            else:
                print("Error: Edge-Cache-Cookie not found in page source")
                return None
            
        except Exception as e:
            print(f"Error extracting cookies: {str(e)}")
            return None

    def scrape_channels(self):
        """
        Main function to scrape all channels
        """
        try:
            print("\nGetting channel links...")
            response = self.session.get(self.live_url)
            
            if response.status_code != 200:
                print(f"Failed to fetch page. Status code: {response.status_code}")
                return []

            # Find all m3u8 URLs
            m3u8_urls = list(
                set(
                    url for url in re.findall(r'https://[^"]+\.m3u8', response.text)
                    if "bldcmprod-cdn.toffeelive.com" in url
                )
            )
            
            channels = []
            for url in m3u8_urls:
                channel_name = url.split('/')[-2].replace('_', ' ').title()
                channel_data = {
                    'name': channel_name,
                    'page_url': self.live_url,
                    'stream_url': url,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                channels.append(channel_data)
                print(f"Found channel: {channel_name}")
            
            return channels
            
        except Exception as e:
            print(f"Error scraping channels: {str(e)}")
            return []

    def save_to_file(self, channels, filename='toffee_channels.json'):
        """
        Save the scraped channel data to a JSON file
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(channels, f, indent=4, ensure_ascii=False)
            print(f"\nChannel data saved to {filename}")
        except Exception as e:
            print(f"Error saving to file: {str(e)}")

    def save_to_m3u(self, channels, filename='toffee_channels.m3u'):
        """
        Save the scraped channel data to an M3U playlist file
        Format compatible with NS Player and similar players
        """
        try:
            channel_list = []
            
            # Add Telegram channel info
            telegram_info = {
                "name": "Join Our Telegram Channel",
                "link": "https://t.me/live_cricket_24",
                "logo": "",
                "origin": "",
                "referrer": "",
                "userAgent": "",
                "cookie": "",
                "drmScheme": "",
                "drmLicense": ""
            }
            channel_list.append(telegram_info)
            
            # Add all channels
            for channel in channels:
                channel_data = {
                    "name": channel["name"],
                    "link": channel["stream_url"],
                    "logo": "",
                    "origin": "https://bldcmprod-cdn.toffeelive.com",
                    "referrer": "",
                    "userAgent": "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc",
                    "cookie": self.cookies,
                    "drmScheme": "",
                    "drmLicense": ""
                }
                channel_list.append(channel_data)
            
            # Save as JSON format
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(channel_list, f, indent=2, ensure_ascii=False)
                
            print(f"\nPlaylist saved to {filename}")
            
        except Exception as e:
            print(f"Error saving to M3U file: {str(e)}")

def main():
    scraper = ToffeeScraper()
    print("\nStarting to scrape Toffee channels...")
    
    try:
        channels = scraper.scrape_channels()
        
        if channels:
            print(f"\nSuccessfully scraped {len(channels)} channels")
            # Save both formats
            scraper.save_to_file(channels)  # Original JSON format
            scraper.save_to_m3u(channels)   # M3U/JSON format for players
            
            # Display channel information
            print("\n=== TOFFEE CHANNELS ===")
            for channel in channels:
                print("-" * 50)
                print(f"Name: {channel['name']}")
                print(f"Stream URL: {channel['stream_url']}")
                print()
        else:
            print("No channels found or error occurred during scraping.")
    
    except KeyboardInterrupt:
        print("\nScript terminated by user.")

if __name__ == "__main__":
    main()
