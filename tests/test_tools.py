# tests/test_tools.py
from tools import search_listings, suggest_outfit, create_fit_card

# ── search_listings (already provided) ───────────────────────────────────────

def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)

# ── suggest_outfit ────────────────────────────────────────────────────────────

def test_suggest_outfit_with_wardrobe():
    item = {"title": "Vintage Nirvana Tee", "category": "tops",
            "style_tags": ["vintage", "grunge"], "colors": ["black"], "brand": None}
    wardrobe = {"items": [{"name": "baggy Levi's", "color": "blue", "style": "casual"},
                           {"name": "white Air Force 1s", "color": "white", "style": "streetwear"}]}
    result = suggest_outfit(item, wardrobe)
    assert isinstance(result, str)
    assert len(result) > 0          # never empty

def test_suggest_outfit_empty_wardrobe():
    item = {"title": "Flowy Midi Skirt", "category": "bottoms",
            "style_tags": ["cottagecore"], "colors": ["floral"], "brand": None}
    empty_wardrobe = {"items": []}
    result = suggest_outfit(item, empty_wardrobe)
    assert isinstance(result, str)
    assert len(result) > 0          # general advice, not an exception

# ── create_fit_card ───────────────────────────────────────────────────────────

def test_fit_card_returns_caption():
    item = {"title": "Vintage Nirvana Tee", "price": 22.0, "platform": "Depop"}
    result = create_fit_card("Pair with baggy jeans and chunky sneakers.", item)
    assert isinstance(result, str)
    assert len(result) > 0

def test_fit_card_empty_outfit_returns_error_string():
    item = {"title": "Vintage Nirvana Tee", "price": 22.0, "platform": "Depop"}
    result = create_fit_card("", item)
    assert isinstance(result, str)
    assert "Missing outfit input" in result   # correct error message, no exception

def test_fit_card_whitespace_outfit_returns_error_string():
    item = {"title": "Vintage Nirvana Tee", "price": 22.0, "platform": "Depop"}
    result = create_fit_card("   ", item)
    assert isinstance(result, str)
    assert "Missing outfit input" in result