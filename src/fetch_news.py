import yfinance as yf
import pandas as pd
from datetime import datetime
from pathlib import Path

SYMBOL = "BTC-USD"
SOURCE = "Yahoo Finance"


#
def fetch_news(symbol: str) -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    news = ticker.news

    rows = []
    for item in news:
        content = item.get("content", {})
        rows.append(
            {
                "Tytuł": content.get("title", ""),
                "Źródło": content.get("publisher", ""),
                "Data": datetime.fromtimestamp(
                    content.get("pubDate", 0)
                    if isinstance(content.get("pubDate", 0), (int, float))
                    else pd.Timestamp(content.get("pubDate", 0)).timestamp()
                ).strftime("%Y-%m-%d %H:%M"),
                "Link": (content.get("canonicalUrl") or {}).get("url", "-"),
            }
        )
    return pd.DataFrame(rows)


# pd.set_option("display.max_colwidth", 60)
# pd.set_option("display.max_rows",     None)
# pd.set_option("display.width",        None)

# print(f"\nNews for: {SYMBOL}\n")
# print(df.to_string(index=False))
# print(f"\nTotal articles: {len(df)}")


def save_news(df: pd.DataFrame, symbol: str) -> None:
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    csv_path = output_dir / f"{symbol}_news.csv"
    json_path = output_dir / f"{symbol}_news.json"

    df.to_csv(csv_path, index=False, encoding="utf-8")
    df.to_json(json_path, orient="records", force_ascii=False, indent=4)

    print(f"News saved to:\n- {csv_path}\n- {json_path}")


df = fetch_news(SYMBOL)
save_news(df, SYMBOL)
