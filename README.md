# 🌟 Toffee Live Channel Scraper

Automatically scrapes and updates live channel information from Toffee Live, generating a player-compatible playlist with authentication details.

## 🚀 Features

- 📺 Automatically extracts all live channels from Toffee Live
- 🔑 Captures and includes authentication cookies
- 📝 Generates player-compatible playlist format
- 🔄 Auto-updates every 30 minutes via GitHub Actions
- 🎯 Extracts high-quality m3u8 stream URLs
- 📱 Compatible with popular media players

## 📋 Requirements

- Python 3.12+
- Chrome/Chromium Browser
- Required Python packages (see requirements.txt)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/mominm3u8/toffee_hls_fetcher.git
cd toffee_hls_fetcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running Locally

```bash
python toffee_scraper.py
```

The script will:
1. Launch a headless Chrome browser
2. Extract authentication cookies
3. Scrape all available channels
4. Generate `toffee_channels.m3u` file

### GitHub Actions Automation

The repository includes GitHub Actions workflow that:
- Runs every 30 minutes
- Updates the playlist file automatically
- Commits and pushes changes if new content is found

## 📄 Output Format

The script generates a JSON-formatted playlist file compatible with media players. Each channel entry includes:

```json
{
  "name": "Channel Name",
  "link": "https://example.com/stream.m3u8",
  "logo": "",
  "origin": "https://bldcmprod-cdn.toffeelive.com",
  "referrer": "",
  "userAgent": "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc",
  "cookie": "Edge-Cache-Cookie=...",
  "drmScheme": "",
  "drmLicense": ""
}
```

## 📱 Compatible Players

- NS Player
- VLC Media Player
- MX Player
- And other players supporting m3u8 with custom headers

## 🔄 Auto-Update Schedule

- Updates every 30 minutes
- Last update time is included in commit messages
- Can be manually triggered through GitHub Actions

## 📢 Join Our Community

- Telegram Channel: [Live Cricket 24](https://t.me/live_cricket_24)
- For updates and support

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect Toffee Live's terms of service and your local regulations when using this tool.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](../../issues).
