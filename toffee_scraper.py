import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class ToffeeScraper:
    def __init__(self):
        """
        Initialize the scraper with automated cookie extraction
        """
        self.base_url = "https://toffeelive.com"
        self.live_url = f"{self.base_url}/en/live"
        self.driver = self._setup_driver()
        self.cookies = self._get_cookies()
        self.session = requests.Session()
        if self.cookies:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Cookie': self.cookies
            })

    def _setup_driver(self):
        """
        Set up Chrome driver with necessary options
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--enable-javascript')
        
        # Enable performance logging
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL', 'browser': 'ALL'})
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def _get_cookies(self):
        """
        Extract Edge-Cache-Cookie from the website
        """
        try:
            print("Accessing Toffee Live...")
            self.driver.get(self.live_url)
            time.sleep(5)  # Wait for cookies to be set
            
            # Get page source and look for Edge-Cache-Cookie
            page_source = self.driver.page_source
            cookie_match = re.search(r'Edge-Cache-Cookie=([^;\\]+)', page_source)
            
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

    def get_channel_links(self):
        """
        Get all channel links from the main page
        """
        try:
            print("\nGetting channel links...")
            self.driver.get(self.live_url)
            time.sleep(5)  # Wait for page to load
            
            # Find all channel links
            links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/watch/"]')
            channel_links = []
            
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if href and '/watch/' in href:
                        channel_name = link.text.strip()
                        if not channel_name:
                            # Try to find name in child elements
                            channel_name = link.find_element(By.CSS_SELECTOR, '*').text.strip()
                        channel_links.append({
                            'name': channel_name or 'Unknown Channel',
                            'url': href
                        })
                        print(f"Found channel: {channel_name} - {href}")
                except Exception as e:
                    continue
            
            return channel_links
            
        except Exception as e:
            print(f"Error getting channel links: {str(e)}")
            return []

    def extract_m3u8_url(self, channel_url, retries=3):
        """
        Extract m3u8 URL from a specific channel
        """
        for attempt in range(retries):
            try:
                print(f"\nAccessing channel: {channel_url}")
                self.driver.get(channel_url)
                time.sleep(10)  # Wait for stream to start loading
                
                # Get network logs
                logs = self.driver.get_log('performance')
                
                for entry in logs:
                    try:
                        log = json.loads(entry['message'])['message']
                        if 'Network.responseReceived' in log['method']:
                            url = log.get('params', {}).get('response', {}).get('url', '')
                            if '.m3u8' in url:
                                print(f"Found stream URL: {url}")
                                return url
                    except:
                        continue
                
                # Also check browser console logs
                browser_logs = self.driver.get_log('browser')
                for log in browser_logs:
                    if '.m3u8' in log['message']:
                        urls = re.findall(r'https?://[^\s<>"]+?\.m3u8', log['message'])
                        if urls:
                            print(f"Found stream URL: {urls[0]}")
                            return urls[0]
                
                if attempt < retries - 1:
                    print(f"No stream URL found, retrying... ({attempt + 1}/{retries})")
                    time.sleep(5)
                
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(5)
                    continue
                
        print("Failed to extract stream URL after all attempts")
        return None

    def extract_channel_name_from_url(self, url):
        """
        Extract channel name from m3u8 URL
        Example: https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_1_hd/playlist.m3u8
        Returns: sony_sports_1_hd
        """
        try:
            # Extract the part between /live/ and /playlist.m3u8
            match = re.search(r'/live/([^/]+)/playlist\.m3u8', url)
            if match:
                channel_name = match.group(1)
                # Convert underscores to spaces and capitalize words
                channel_name = channel_name.replace('_', ' ').title()
                return channel_name
            return "Unknown Channel"
        except Exception:
            return "Unknown Channel"

    def scrape_channels(self):
        """
        Main function to scrape all channels
        """
        channels = []
        channel_links = self.get_channel_links()
        
        print(f"\nFound {len(channel_links)} channels to process")
        
        for channel in channel_links:
            stream_url = self.extract_m3u8_url(channel['url'])
            if stream_url:
                # Extract channel name from m3u8 URL
                channel_name = self.extract_channel_name_from_url(stream_url)
                channel_data = {
                    'name': channel_name,
                    'page_url': channel['url'],
                    'stream_url': stream_url,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                channels.append(channel_data)
        
        return channels

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
                    "logo": "",  # You might want to extract this from the page
                    "origin": "https://bldcmprod-cdn.toffeelive.com",
                    "referrer": "",
                    "userAgent": "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc",
                    "cookie": self.cookies,  # Using the Edge-Cache-Cookie
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

    def cleanup(self):
        """
        Clean up resources
        """
        if self.driver:
            self.driver.quit()

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
                print(f"Page URL: {channel['page_url']}")
                print(f"Stream URL: {channel['stream_url']}")
                print()
        else:
            print("No channels found or error occurred during scraping.")
    
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
