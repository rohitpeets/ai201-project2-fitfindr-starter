# 👕 FitFindr

FitFindr is an AI-powered thrift shopping assistant that helps users discover secondhand clothing, build outfits using their existing wardrobe, and generate social-media-ready style captions.

The agent follows a structured planning workflow that:

1. Understands what the user is looking for
2. Searches a secondhand marketplace dataset
3. Recommends outfit combinations
4. Creates a shareable "Fit Card" caption

---

## 📁 Project Structure

```text
ai201-project2-fitfindr-starter/
├── agent.py                   # Planning loop and session management
├── app.py                     # Gradio user interface
├── tools.py                   # Core agent tools
├── planning.md                # Design and planning documentation
├── README.md                  # Project documentation
├── test_app.py                # CLI testing script
├── requirements.txt           # Python dependencies
│
├── data/
│   ├── listings.json          # Mock thrift listings dataset
│   └── wardrobe_schema.json   # Wardrobe schema and example wardrobe
│
└── utils/
    └── data_loader.py         # Dataset loading utilities
```

---

## 🚀 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

You can obtain a free API key from:

https://console.groq.com

---

## 📊 Dataset Overview

### listings.json

Contains 40 mock secondhand clothing listings across multiple categories and fashion styles.

Each listing includes:

| Field       | Description               |
| ----------- | ------------------------- |
| id          | Unique listing identifier |
| title       | Listing title             |
| description | Item description          |
| category    | Clothing category         |
| style_tags  | Style labels              |
| size        | Item size                 |
| condition   | Item condition            |
| price       | Listing price             |
| colors      | Available colors          |
| brand       | Brand name                |
| platform    | Marketplace source        |

Load listings:

```python
from utils.data_loader import load_listings

listings = load_listings()
```

---

### wardrobe_schema.json

Defines the wardrobe structure used by FitFindr.

Includes:

* Wardrobe schema
* Example wardrobe
* Empty wardrobe template

Load example wardrobe:

```python
from utils.data_loader import get_example_wardrobe

wardrobe = get_example_wardrobe()
```

---

# 🧠 How FitFindr Works

FitFindr uses a sequential planning loop where each step depends on the successful completion of the previous step.

```text
User Query
    │
    ▼
Parse Query
    │
    ▼
Search Listings
    │
    ▼
Results Found?
 ┌──┴──┐
 │     │
Yes    No
 │      │
 ▼      ▼
Select  Return Error
Item
 │
 ▼
Suggest Outfit
 │
 ▼
Create Fit Card
 │
 ▼
Return Results
```

---

## Step 1: Parse User Query

The LLM extracts structured search criteria.

### Example

Input:

```text
vintage graphic tee under $30
```

Parsed Output:

```python
{
    "description": "vintage graphic tee",
    "size": None,
    "max_price": 30.0
}
```

---

## Step 2: Search Listings

The agent searches the thrift dataset using the parsed criteria.

### Filters Applied

* Maximum price
* Size matching
* Keyword relevance

### Example

```python
search_listings(
    description="vintage graphic tee",
    size=None,
    max_price=30.0
)
```

Returns:

```python
[
    listing_1,
    listing_2,
    listing_3
]
```

Sorted by relevance score.

---

## Step 3: Select Best Match

The highest-ranked result is selected.

Example:

```python
{
    "title": "Y2K Baby Tee — Butterfly Print",
    "price": 18.00,
    "platform": "Depop"
}
```

Stored as:

```python
session["selected_item"]
```

---

## Step 4: Generate Outfit Recommendation

Using the selected item and the user's wardrobe:

### If wardrobe contains items

The LLM creates specific outfit combinations using named pieces from the wardrobe.

### If wardrobe is empty

The LLM provides general styling advice.

Example:

```text
Pair the Y2K Baby Tee with baggy straight-leg jeans and chunky white sneakers for a relaxed vintage look.
```

Stored as:

```python
session["outfit_suggestion"]
```

---

## Step 5: Create Fit Card

The final step generates a short, social-media-style caption.

Example:

```text
Just scored this Y2K Baby Tee for $18 on Depop. Paired it with baggy denim and chunky sneakers for the perfect throwback vibe. Thrifted fits never miss.
```

Stored as:

```python
session["fit_card"]
```

---

# 🔄 Session State Management

FitFindr uses a shared session dictionary to pass information between tools.

```python
session = {
    "query": "",
    "wardrobe": {},
    "parsed": {},
    "search_results": [],
    "selected_item": None,
    "outfit_suggestion": None,
    "fit_card": None,
    "error": None
}
```

---

## Session Fields

| Field             | Populated By           | Used By            |
| ----------------- | ---------------------- | ------------------ |
| query             | Session Initialization | Query Parser       |
| parsed            | Query Parser           | Search Tool        |
| search_results    | Search Tool            | Item Selection     |
| selected_item     | Item Selection         | Outfit Generator   |
| wardrobe          | Session Initialization | Outfit Generator   |
| outfit_suggestion | Outfit Generator       | Fit Card Generator |
| fit_card          | Fit Card Generator     | User Interface     |
| error             | Any Step               | App Interface      |

---

# 🛠 Core Tools

## 1. search_listings()

### Purpose

Find matching thrift listings.

### Parameters

```python
search_listings(
    description: str,
    size: str | None,
    max_price: float | None
)
```

### Returns

```python
list[dict]
```

### Behavior

* Loads dataset
* Applies filters
* Scores keyword matches
* Sorts by relevance
* Returns matching listings

### Failure Mode

Returns:

```python
[]
```

when no listings are found.

---

## 2. suggest_outfit()

### Purpose

Generate styling recommendations.

### Parameters

```python
suggest_outfit(
    new_item: dict,
    wardrobe: dict
)
```

### Returns

```python
str
```

### Behavior

* Uses wardrobe items when available
* Generates personalized outfit ideas
* Falls back to general styling advice if wardrobe is empty

### Failure Mode

No exception raised.

General styling advice is returned.

---

## 3. create_fit_card()

### Purpose

Generate a shareable caption for social media.

### Parameters

```python
create_fit_card(
    outfit: str,
    new_item: dict
)
```

### Returns

```python
str
```

### Behavior

* Uses outfit recommendation
* Generates 2–4 sentence caption
* Uses higher creativity settings for variety

### Failure Mode

Returns an explanatory error message if no outfit suggestion exists.

---

# 🧪 Example Interaction

### User Query

```text
vintage graphic tee under $30
```

### Parsed Query

```python
{
    "description": "vintage graphic tee",
    "size": None,
    "max_price": 30.0
}
```

### Search Results

```python
[
    listing1,
    listing2,
    listing3
]
```

### Selected Item

```python
{
    "title": "Y2K Baby Tee — Butterfly Print",
    "price": 18.00,
    "platform": "Depop"
}
```

### Outfit Suggestion

```text
Pair the Y2K Baby Tee with baggy jeans and chunky sneakers for a casual Y2K-inspired look.
```

### Fit Card

```text
Just scored this Y2K Baby Tee for $18 on Depop. Paired it with baggy denim and sneakers for the perfect throwback fit.
```

---

# ✅ Features

* AI-powered query understanding
* Secondhand listing search
* Outfit recommendations
* Wardrobe-aware styling
* Social media caption generation
* Session-based planning architecture
* Graceful failure handling
* Gradio web interface

---

# 📌 Future Improvements

* Multi-item outfit generation
* Better ranking and recommendation algorithms
* Image-based clothing search
* Personalized style profiles
* Marketplace integrations
* Saved wardrobes and user accounts
* Trend-aware fashion recommendations

---
