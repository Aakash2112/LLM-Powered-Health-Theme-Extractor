import streamlit as st
import json
import subprocess

st.set_page_config(page_title="AARP Health Article Theme Extractor", layout="wide")

# Custom styling
st.markdown("""
    <style>
        .stButton button {
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
            padding: 0.5em 1.5em;
            border-radius: 8px;
        }
        .block-container {
            padding: 2rem 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🔍 AARP Health Article Theme Explorer")

# Load articles from JSON file
@st.cache_data
def load_articles():
    with open("scraped_articles.json", "r") as f:
        return json.load(f)

articles = load_articles()

# Sidebar selection from all types (article + landing)
selectable_articles = [a for a in articles if a.get("content") or (a["type"] == "landing_page" and a.get("links"))]
selected_title = st.sidebar.selectbox(
    "Select an entry:", [f"{a['title']} ({a['type']})" for a in selectable_articles]
)
selected_article = next(a for a in selectable_articles if f"{a['title']} ({a['type']})" == selected_title)

# Display metadata
st.markdown(f"## 📰 *{selected_article['title']}*")
st.markdown(f"**URL:** [{selected_article['url']}]({selected_article['url']})")

# Display content preview
st.markdown("### 📄 Content")
if selected_article.get("content"):
    st.write(selected_article["content"][:3000] + ("..." if len(selected_article["content"]) > 3000 else ""))
else:
    st.info("ℹ️ No intro content found. This appears to be a catalog-style landing page.")

# Display links if landing page
if selected_article["type"] == "landing_page" and selected_article.get("links"):
    st.markdown("### 🔗 Linked Articles")
    for text, link in selected_article["links"][:5]:
        st.markdown(f"- [{text}]({link})")

# Ask Mistral
def ask_mistral(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")

if st.button("🧠 Extract Key Themes with Mistral"):
    with st.spinner("Analyzing with Mistral..."):

        if selected_article["type"] == "article":
            prompt = f"""
You are a health-focused AI assistant.

Given the article below, identify **5 key health-related themes** strictly based on the article's actual content.

- Each theme should be a **short phrase**, not a sentence.
- **Not a generic label** (like "health tips") unless directly stated
- Do **not** include any information that is not explicitly stated in the article.
- Written clearly so that it reflects a central idea or recurring topic in the text

Article:
\"\"\"
{selected_article["content"]}
\"\"\"

Key Themes:
- 
"""
        else:
            link_list = "\n".join([f"- {text}" for text, _ in selected_article.get("links", [])[:5]])
            intro = selected_article.get("content", "No intro text available.")

            prompt = f"""
You are a health content summarizer.

Below is a landing page from AARP.org. It contains an introductory paragraph followed by links to other health-related articles.

Your task is to extract **3 to 5 specific health-related themes** based strictly on the **intro text** and the **titles of the linked articles**.

✅ Each theme should be a clear and meaningful phrase like “Digestive Health”, “Exercise for Seniors”, or “Hearing Loss”.

🚫 Do **not** make assumptions or generalizations (e.g., "Health Education", "Awareness").
🚫 Do **not** copy full article titles or include vague labels.
🚫 Avoid repeating similar ideas or including UI text.

Intro Text:
\"\"\"
{intro}
\"\"\"

Top Linked Articles:
{link_list}

Key Themes:
-
"""

        response = ask_mistral(prompt)
        st.markdown("### 🔑 Extracted Themes")
        st.code(response.strip(), language="markdown")
