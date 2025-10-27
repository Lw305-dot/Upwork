import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 
HEADERS = {"User-Agent": "Mozilla/5.0"}
urls=[
    
    "https://edition.cnn.com/markets"
]
response = requests.get(urls[0], headers=HEADERS)
print(response.status_code)  # Should print 200 if the request was successful
print(response.text[:500])  # Preview first 500 characters of HTML

# Inspect page structure
soup = BeautifulSoup(response.text, "html.parser")
# Print all unique HTML tags
tags = set([tag.name for tag in soup.find_all()])
print("Unique HTML tags:", tags)
# Print first 5 divs with their class names
for i, div in enumerate(soup.find_all("div", class_=True)[:5]):
    print(f"Div {i+1} class: {div.get('class')}")

# Print content of divs with class starting with 'basic-table_'
for div in soup.find_all("div", class_=lambda c: c and any(cls.startswith("basic-table_") for cls in c if isinstance(c, list))):
    print("\nFound basic-table div:")
    print(div.prettify()[:1000])  # Print first 1000 characters for preview
#"https://www.investing.com/indices/major-indices",
#"https://www.bloomberg.com/markets/stocks/world-indexes",
    # "https://www.reuters.com/markets/indices",
    # "https://www.wsj.com/market-data/stocks",
    # "https://www.cnbc.com/world/?region=world",
    # "https://www.ft.com/markets",
    # "https://groww.in/indices/global-indices"
    # "https://www.nasdaq.com/market-activity/indices",
    # "https://www.marketwatch.com/tools/marketsummary",
    # "https://www.barchart.com/stocks/indices",
    # "https://www.babypips.com/learn/forex/forex-global-equity-markets-and-you",
    #  "https://edition.cnn.com/markets",
def scrape_generic(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table")
        if not table:
            return pd.DataFrame()

        rows = []
        for row in table.find_all("tr"):
            cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if cols:
                rows.append(cols)

        if len(rows) < 2:
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.DataFrame(rows[1:], columns=rows[0])

        # Try to normalize columns
        col_map = {c.lower(): c for c in df.columns}

        # Extract common fields
        index_col = next((c for c in df.columns if "index" in c.lower() or "name" in c.lower()), None)
        price_col = next((c for c in df.columns if "last" in c.lower() or "price" in c.lower() or "close" in c.lower()), None)
        change_col = next((c for c in df.columns if "change" in c.lower() and "%" not in c.lower()), None)
        pct_col = next((c for c in df.columns if "%" in c.lower()), None)

        clean = pd.DataFrame({
            "Index": df[index_col] if index_col else None,
            "Last Price": df[price_col] if price_col else None,
            "Change": df[change_col] if change_col else None,
            "Change %": df[pct_col] if pct_col else None,
            "Source": url
        })

        return clean

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return pd.DataFrame()


def unified_pipeline():
    all_data = []
    for url in urls:
        df = scrape_generic(url)
        if not df.empty:
            all_data.append(df)
        time.sleep(2) # Be polite with a delay
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
if __name__ == "__main__":
    final_df = unified_pipeline()
    if not final_df.empty:
        print(final_df.head())
    else:
        print("No data scraped.")
