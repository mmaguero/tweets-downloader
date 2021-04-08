# tweets-downloader
Download tweets by API or SNScrape

Install:

`
python3 -m venv myVenv
source myVenv/bin/activate
pip install -r requirements.txt
`

Use:

- `python3 scrape_tweets.py 1 False > outsns_track1.txt` for SNScrape
- `python3 scrape_tweets.py 2 True > outsns_track2.txt` for API
