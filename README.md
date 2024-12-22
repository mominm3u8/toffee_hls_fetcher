# 🌟 Toffee HLS Stream Fetcher

<div align="center">

![GitHub last commit](https://img.shields.io/github/last-commit/mominm3u8/toffee_hls_fetcher)
![GitHub issues](https://img.shields.io/github/issues/mominm3u8/toffee_hls_fetcher)
![GitHub](https://img.shields.io/github/license/mominm3u8/toffee_hls_fetcher)
[![Auto Update](https://github.com/mominm3u8/toffee_hls_fetcher/actions/workflows/update_channels.yml/badge.svg)](https://github.com/mominm3u8/toffee_hls_fetcher/actions/workflows/update_channels.yml)

</div>

## 📑 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Output Format](#-output-format)
- [Auto-Update System](#-auto-update-system)
- [Community](#-community)
- [Contributing](#-contributing)
- [License](#-license)

## 🔭 Overview

Toffee HLS Stream Fetcher is an automated tool that extracts and maintains an up-to-date collection of HLS streams from Toffee Live. It automatically refreshes stream data every 30 minutes and formats it for compatibility with popular media players.

### 🎯 Key Benefits
- **Always Fresh**: Stream links are automatically updated every 30 minutes
- **Player Ready**: Compatible with popular media players (NS Player, VLC, etc.)
- **Automated**: Set it and forget it - GitHub Actions handles the updates
- **Reliable**: Includes authentication and necessary headers for stable playback

## ✨ Features

- 📺 **Automated Channel Discovery**: Automatically finds all available channels
- 🔑 **Authentication Handling**: Manages cookies and authentication headers
- 📝 **Smart Formatting**: Generates player-compatible playlists
- 🔄 **Auto-Updates**: Refreshes every 30 minutes via GitHub Actions
- 🎯 **Quality Streams**: Extracts high-quality HLS stream URLs
- 📱 **Wide Compatibility**: Works with most media players

## 🚀 Quick Start

```bash
# Get the latest M3U playlist
curl -o playlist.m3u https://raw.githubusercontent.com/mominm3u8/toffee_hls_fetcher/main/toffee_channels.m3u
```

## 📥 Installation

For developers who want to run the scraper locally:

```bash
# Clone the repository
git clone https://github.com/mominm3u8/toffee_hls_fetcher.git
cd toffee_hls_fetcher

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Running Locally

```bash
python toffee_scraper.py
```

The script will:
1. Launch Chrome in headless mode
2. Extract necessary authentication
3. Discover available channels
4. Generate `toffee_channels.m3u` file

## 📄 Output Format

The generated playlist follows this JSON structure:

```json
{
  "name": "Channel Name",
  "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/channel_name/playlist.m3u8",
  "logo": "",
  "origin": "https://bldcmprod-cdn.toffeelive.com",
  "referrer": "",
  "userAgent": "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc",
  "cookie": "Edge-Cache-Cookie=...",
  "drmScheme": "",
  "drmLicense": ""
}
```

## ⚡ Auto-Update System

The repository leverages GitHub Actions for automatic updates:

- 🕒 Updates every 30 minutes
- 📝 Commits new changes only when stream data changes
- 📊 Tracks update status in Actions tab
- 🔄 Can be manually triggered if needed

## 🌐 Community

- 📱 **Telegram Channel**: Join us on [Live Cricket 24](https://t.me/live_cricket_24)
- 🐛 **Issues**: Report problems via [GitHub Issues](https://github.com/mominm3u8/toffee_hls_fetcher/issues)
- 💡 **Suggestions**: Share ideas in [Discussions](https://github.com/mominm3u8/toffee_hls_fetcher/discussions)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Please ensure you comply with Toffee Live's terms of service and your local regulations when using this tool.

---
<div align="center">
Made with ❤️ by the community
</div>