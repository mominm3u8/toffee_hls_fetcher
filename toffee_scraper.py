import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
import random

class ToffeeScraper:
    def __init__(self):
        """
        Initialize the scraper
        """
        self.base_url = "https://toffeelive.com"
        self.live_url = f"{self.base_url}/en/live"
        self.session = self._create_session()
        self.cookies = None
        
        # Try to get cookies multiple times
        for i in range(3):
            print(f"\nAttempt {i+1} to get cookies...")
            self.cookies = self._get_cookies()
            if self.cookies:
                break
            time.sleep(5)  # Wait between attempts

    def _create_session(self):
        """
        Create a session with proper headers
        """
        session = requests.Session()
        
        # List of common user agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
        ]
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        session.headers.update(headers)
        return session

    def _get_cookies(self):
        """
        Extract Edge-Cache-Cookie from the website
        """
        try:
            print("Accessing Toffee Live...")
            
            # First get the main page to get any session cookies
            response = self.session.get(self.base_url)
            time.sleep(2)  # Wait a bit
            
            # Now get the live page
            response = self.session.get(self.live_url)
            print("\nResponse Status:", response.status_code)
            print("Response Headers:", dict(response.headers))
            print("\nPage Content Preview:", response.text[:1000])
            
            if response.status_code != 200:
                print(f"Failed to fetch page. Status code: {response.status_code}")
                return None
            
            # Try different patterns to find the cookie
            patterns = [
                r'Edge-Cache-Cookie=([^;\\"\s]+)',
                r'"Edge-Cache-Cookie":"([^"]+)"',
                r'Edge-Cache-Cookie:\s*([^\s;]+)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response.text)
                if matches:
                    edge_cache_cookie = f"Edge-Cache-Cookie={matches[0]}"
                    print("\nSuccessfully extracted Edge-Cache-Cookie:")
                    print(edge_cache_cookie)
                    return edge_cache_cookie
            
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
            
            # Refresh the session
            self.session = self._create_session()
            
            # Get the live page
            response = self.session.get(self.live_url)
            print("\nScraping Response Status:", response.status_code)
            
            if response.status_code != 200:
                print(f"Failed to fetch page. Status code: {response.status_code}")
                return []

            # Find all m3u8 URLs using multiple patterns
            m3u8_patterns = [
                r'https://[^"]+\.m3u8',
                r'https://[\w\-\.]+/[\w\-\./]+\.m3u8',
                r'"url":"(https://[^"]+\.m3u8)"'
            ]
            
            m3u8_urls = set()
            for pattern in m3u8_patterns:
                urls = re.findall(pattern, response.text)
                m3u8_urls.update([url for url in urls if "bldcmprod-cdn.toffeelive.com" in url])
            
            print(f"\nFound {len(m3u8_urls)} m3u8 URLs")
            
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
