import yfinance as yf
import pandas as pd
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

SYMBOL = "BTC-USD"

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

# Funkcja do dodawania świeżych danych do istniejących plików
def update_news(df: pd.DataFrame, symbol: str) -> None:
    output_dir = Path("data")
    csv_path = output_dir / f"{symbol}_news.csv"
    json_path = output_dir / f"{symbol}_news.json"

    if csv_path.exists():
        existing_df = pd.read_csv(csv_path, encoding="utf-8")
        combined_df = pd.concat([existing_df, df]).drop_duplicates(subset=["Tytuł", "Data"])
        combined_df.to_csv(csv_path, index=False, encoding="utf-8")
    else:
        df.to_csv(csv_path, index=False, encoding="utf-8")

    if json_path.exists():
        existing_json = pd.read_json(json_path, orient="records")
        combined_json = pd.concat([existing_json, df]).drop_duplicates(subset=["Tytuł", "Data"])
        combined_json.to_json(json_path, orient="records", force_ascii=False, indent=4)
    else:
        df.to_json(json_path, orient="records", force_ascii=False, indent=4)

    print(f"News updated in:\n- {csv_path}\n- {json_path}")

df = fetch_news(SYMBOL)


#save_news(df, SYMBOL)

update_news(df, SYMBOL)


