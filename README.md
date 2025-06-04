# AARP Health Article Scraper + LLM Key Theme Extractor

This project scrapes health-related articles from the AARP website and uses a local open-source LLM (via Ollama) to extract 3-5 key themes from each article.

---

## 🔧 Components

### 1. Scraper (`scraper.ipynb`)
- Uses **Selenium** to scroll and render the base health page: `https://www.aarp.org/health/`
- Filters all article and landing page URLs by checking for:
  - Valid article-like structure
  - Public (non-member-only) accessibility
- Scrapes the page content using `lxml` via `BeautifulSoup`
- Captures:
  - Title
  - Main content (from `<p>`, `<h2>`, `<ul>`, etc.)
  - Classifies whether it's a full article or a landing/catalog page
- Saves all extracted data to `scraped_articles.json`

### 2. LLM Processor (`theme_extractor.py`)

-Loads the scraped data from scraped_articles.json
-Uses the Mistral model locally via Ollama to extract 3–5 concise key themes from each article or landing page
-The Streamlit app:

	- Provides an interactive interface for reviewing each article and its extracted themes

	- Allows you to manually trigger or review LLM-based extraction
-The prompt:

	-Is custom-designed to avoid hallucination

	-Focuses only on content-grounded, short health-related themes

  	-Ignores specific names, dates, or invented info

---

## 📁 Files

- `scraper.ipynb` → Runs the AARP scraper
- `theme_extractor.py` → Feeds articles to Mistral for theme extraction
- `scraped_articles.json` → Stores the structured article data in JSON Format
- `README.txt` → This file

---

## 🧠 LLM Setup

- Download Ollama: https://ollama.com/download
- Pull model:
  ```
  ollama pull mistral
  ```
- Example use:
  ```
  ollama run mistral
  ```

You must have **at least 8GB RAM**, but for Mistral, 8GB is the minimum. You can also try lighter models like **Gemma 2B**.

---

## 🚀 How to Run

```bash
# Step 1: Run the scraper notebook
Open and run each cell in: scraper.ipynb


# Step 2: Make sure the scraped_articles.json is generated.

# Step 3: Extract themes using the LLM
streamlit run theme_extractor.py
```

---

## 🚀 Prompts Used

'''
1. Articles
You are a health-focused AI assistant.

Given the article below, identify **5 key health-related themes** strictly based on the article's actual content.

- Each theme should be a **short phrase**, not a sentence.
- **Not a generic label** (like "health tips") unless directly stated
- Do **not** include any information that is not explicitly stated in the article.
- Written clearly so that it reflects a central idea or recurring topic in the text

Article:

2. Landing Page
You are a health content summarizer.

Below is a landing page from AARP.org. It contains an introductory paragraph followed by links to other health-related articles.

Your task is to extract **3 to 5 specific health-related themes** based strictly on the **intro text** and the **titles of the linked articles**.

✅ Each theme should be a clear and meaningful phrase like “Digestive Health”, “Exercise for Seniors”, or “Hearing Loss”.

🚫 Do **not** make assumptions or generalizations (e.g., "Health Education", "Awareness").
🚫 Do **not** copy full article titles or include vague labels.
🚫 Avoid repeating similar ideas or including UI text.

Intro Text: 

---

## ✅ Output Example

```
Article: Why This Flu Season Is So Bad

Key Themes:
- High flu activity across most U.S. states
- Influenza A strain dominating this season
- Low flu vaccination rates among adults and children
- Rise in pneumonia cases following the flu
- Antibiotic-resistant pneumonias complicating treatment
```

---

## 📌 Notes

- Some articles are member-only; these are skipped.
- Landing pages are identified and logged separately.
- You can modify the prompt or model as needed.

---

Made for the AARP open-source scraping and generative analysis task.

