# 📰 MoneyControl News Scraper and Summarizer

This project is a Python-based pipeline that scrapes news articles from [MoneyControl](https://www.moneycontrol.com), extracts content, summarizes it using Google's Gemini API, and uploads the results to a Google Spreadsheet.

---

## 📁 Project Structure

```
.
├── README.md                 # Project documentation
├── main.py                  # Main script to run the pipeline
├── processors
│   └── web_scrapper.py      # Web scraping class and logic
└── utils
    └── utils.py             # Helper functions (Gemini API, upload, parsing, etc.)
```

---

## 🚀 Features

* Scrapes news headlines and article content for specific MoneyControl categories
* Parses and converts content timestamps to UTC
* Summarizes articles using **Gemini Pro**
* Cleans and formats summaries into plain text
* Uploads raw and summarized data to **Google Sheets**

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

Requirements include:

* `requests`
* `beautifulsoup4`
* `pandas`
* `tqdm`
* `markdown2`
* `pypandoc`
* `gspread`
* `oauth2client`
* `google-generativeai`
* `python-dotenv`
* `pytz`

Also ensure `pandoc` is available; it will be auto-downloaded if missing.

---

## 🔧 Setup

1. Create a `.env` file in the project root:

   ```
   GEMINI_KEY=your_gemini_api_key
   ```

2. Save your Google service account credentials JSON file as:

   ```
   sacred-garden-240417-dd1a4c6d6b06.json
   ```

3. Enable Google Sheets and Drive APIs for your service account.

---

## 🛠️ How It Works

1. **Scrape Links**:
   From categories like `politics/`, `business/economy/`, extract article links and timestamps using HTML structure.

2. **Scrape Content**:
   Load each article and extract full article body from embedded JSON (`application/ld+json`).

3. **Summarize**:
   Use Gemini Pro to summarize each article in plain English with future outlooks.

4. **Upload to Sheets**:
   Save both raw and summarized content to a Google Spreadsheet in separate tabs.

---

## ▶️ Running the Script

```bash
python main.py
```

This will process four MoneyControl categories:

* `politics`
* `business/companies`
* `business/ipo`
* `business/economy`

Results are saved to `assets/` folder and then uploaded to Google Sheets.

---

## 🧠 Core Components

### `GetData` Class (in `web_scrapper.py`)

Handles web scraping. Capable of:

* Extracting URLs & timestamps
* Parsing JSON from article pages

### `utils.py` Functions

* `get_timestamp_and_link`: Extracts and formats timestamps
* `getnews`: Extracts article body
* `gemini_convert`: Summarizes text using Gemini
* `upload`: Pushes DataFrames to Google Sheets

---

## 📤 Output

For each category, the following files are saved under `assets/`:

* `*_link_date.xlsx`: Article URLs and timestamps
* `*_scrapped_url.xlsx`: Raw article content
* `*_converted_content.xlsx`: Summarized content

Each category also has a dedicated Google Spreadsheet with:

* Tab 1: Summary + date
* Tab 2: Merged raw and summarized data

---

## 📝 Notes

* Only news published **today** are processed
* Handles BeautifulSoup parsing and timezone conversion robustly
* Graceful fallback for API failures (e.g., harmful content)

---

## 📎 TODOs / Improvements

* Add logging instead of print statements
* Extend to other websites
* Add CLI arguments for flexibility
* Use async requests for faster scraping

---

## 👤 Author

* Built by [Abhinav Kumar]

---
