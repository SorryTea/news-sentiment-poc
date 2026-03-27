import yfinance as yf
import pandas as pd
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

SYMBOL = "BTC-USD"
SOURCE = "Yahoo Finance"


# Funkcja pomocnicza do wyciągania nazwy źródła z linków, jeśli brak jest bezpośredniej informacji o wydawcy
def get_source_name(content: dict) -> str:
    publisher = content.get("publisher", "")
    if publisher and str(publisher).strip():
        return publisher

    url = (content.get("canonicalUrl") or {}).get("url", "")
    if not url:
        return "Unknown"

    domain = urlparse(url).netloc.replace("www.", "")
    return domain


# Główna funkcja do pobierania wiadomości dla danego symbolu
def fetch_news(symbol: str) -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    news = ticker.news

    rows = []
    for item in news:
        content = item.get("content", {})
        rows.append(
            {
                "Tytuł": content.get("title", ""),
                "Źródło": get_source_name(content),
                "Data": datetime.fromtimestamp(
                    content.get("pubDate", 0)
                    if isinstance(content.get("pubDate", 0), (int, float))
                    else pd.Timestamp(content.get("pubDate", 0)).timestamp()
                ).strftime("%Y-%m-%d %H:%M"),
                "Link": (content.get("canonicalUrl") or {}).get("url", "-"),
            }
        )
    return pd.DataFrame(rows)


# Funkcja do zapisywania danych do plików CSV i JSON
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
