import requests
from bs4 import BeautifulSoup
import re

class IntelligenceScanner:
    """
    General Hendricks Intelligence Hub.
    Scrapes and extracts core wisdom from web URLs.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scan_url(self, url):
        """
        Fetches and cleans text from a URL.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts, styles, and junk
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text and clean whitespace
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Basic cleanup (remove multiple newlines)
            text = re.sub(r'\n+', '\n', text)
            
            return text
        except Exception as e:
            print(f"Intelligence Scan Failed: {e}")
            return None

if __name__ == "__main__":
    scanner = IntelligenceScanner()
    test_url = "https://www.medicalnewstoday.com/articles/321486"
    print(f"Scanning: {test_url}...")
    result = scanner.scan_url(test_url)
    print(result[:500] if result else "Scan failed.")
