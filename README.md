# PoC News Sentiment

Prosty Proof of Concept do analizy sentymentu newsów o BTC-USD.

Projekt składa się z dwóch części:

- `src/fetch_news.py` – pobiera newsy z Yahoo Finance i zapisuje je do plików
- `notebooks/poc_news_sentiment.ipynb` – analizuje sentyment newsów i wyznacza prosty sygnał

## Struktura projektu

- `src/` – skrypt do pobierania danych
- `data/` – zapisane newsy w `csv` i `json`
- `notebooks/` – notebook z analizą sentymentu
- `requirements.txt` – wymagane biblioteki

## Jak to działa

### 1. Pobieranie danych

Skrypt `fetch_news.py`:

- pobiera newsy dla zadanego symbolu, tutaj `BTC-USD`
- wyciąga tytuł, źródło, datę i link
- zapisuje dane do folderu `data`
- przy kolejnym uruchomieniu aktualizuje pliki i usuwa duplikaty

### 2. Analiza sentymentu

W notebooku:

- ładowane są zapisane newsy
- analizowany jest sentyment nagłówków
- liczony jest `importance_score`
- na końcu wyznaczany jest prosty sygnał, np. `KUP`, `SPRZEDAJ`, `OBSERWUJ`

## Importance score

Końcowy wynik wiadomości uwzględnia:

- sentyment nagłówka
- wiarygodność źródła
- aktualność informacji

Wagi i progi są na razie dobrane dość intuicyjnie, więc ten projekt traktuję bardziej jako PoC niż gotowe narzędzie.

## Uruchomienie

Najpierw instalacja bibliotek:

```bash
pip install -r requirements.txt
```

Potem uruchomienie skryptu:

python src/fetch_news.py

Na końcu można odpalić notebook i przejść przez analizę:

jupyter notebook
