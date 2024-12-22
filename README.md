# Toffee HLS Stream Fetcher

A Python script that fetches live cricket stream links from Toffee Live and formats them into an M3U playlist.

## Features

- Extracts m3u8 stream URLs directly from Toffee Live
- Generates both JSON and M3U playlist formats
- Automatically updates every 30 minutes via GitHub Actions
- Includes Edge-Cache-Cookie for stream access
- Compatible with NS Player and similar media players

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/toffee_hls_fetcher.git
cd toffee_hls_fetcher
```

2. Install dependencies:
```bash
pip install requests beautifulsoup4
```

## Usage

Run the script:
```bash
python toffee_scraper.py
```

This will:
1. Fetch available stream links from Toffee Live
2. Extract the Edge-Cache-Cookie
3. Generate two files:
   - `toffee_channels.json`: Raw channel data
   - `toffee_channels.m3u`: M3U playlist in JSON format

## Output Format

The M3U playlist is formatted as JSON with the following structure:
```json
{
  "name": "Channel Name",
  "link": "https://example.com/stream.m3u8",
  "logo": "",
  "origin": "https://bldcmprod-cdn.toffeelive.com",
  "referrer": "",
  "userAgent": "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc",
  "cookie": "Edge-Cache-Cookie=xxx",
  "drmScheme": "",
  "drmLicense": ""
}
```

## GitHub Actions

The repository includes a GitHub Actions workflow that:
- Runs every 30 minutes
- Updates the channel list automatically
- Commits and pushes changes if new channels are found

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.