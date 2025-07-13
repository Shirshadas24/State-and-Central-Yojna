import re
import json
from thefuzz import fuzz

def clean_query(query):
    # Remove common trailing question phrases and info requests
    query = query.replace("yojna", "yojana")
    query = query.replace("scheme", "yojana").replace("yojna", "yojana")

    query = re.sub(
        r'\s*(kya hai|what is|ka hai|ke baare mein|about|kaise apply karein?|kaise apply kare|how to apply|application link|apply online|official website|website|link|application process|helpline number kya hai|helpline number)\??$',
        '',
        query,
        flags=re.IGNORECASE
    )
    return query.strip()

# Load all scheme data from JSON
with open("data/schemes.json", "r", encoding="utf-8") as f:
    RAW_SCHEMES = json.load(f)

# Flatten translations to get only selected language versions
def flatten_translations(raw_data, language="Hinglish"):
    flattened = []
    for scheme in raw_data:
        for trans in scheme["translations"]:
            if trans["language"].lower() == language.lower():
                flattened.append(trans)
                break
    return flattened

# Retrieve top matching schemes based on query
def retrieve_top_schemes(query, language="Hinglish", top_k=3, threshold=20, debug=False):
    schemes = flatten_translations(RAW_SCHEMES, language)
    if not schemes and language.lower() != "hinglish":
        # Fallback to Hinglish if no schemes found in requested language
        if debug:
            print(f"[FALLBACK] No schemes found for language '{language}', falling back to 'Hinglish'")
        schemes = flatten_translations(RAW_SCHEMES, "Hinglish")
    scored_schemes = []

    query_clean = clean_query(query)
    query_lower = query_clean.lower()

    # 🔍 Exact match shortcut (improved)
    for s in schemes:
        scheme_name = s.get("scheme_name", "").lower()
        if query_lower == scheme_name or query_lower in scheme_name or scheme_name in query_lower:
            if debug:
                print(f"[EXACT MATCH] {s['scheme_name']}")
            return [s]

    # 🔎 Fuzzy match across relevant fields
    for s in schemes:
        scheme_name = s.get("scheme_name", "")
        combined_text = (
            scheme_name + " " +
            s.get("eligibility", "") + " " +
            s.get("benefits", "") + " " +
            " ".join(s.get("keywords", [])) + " " +
            s.get("example_question", "")
        )
        score = fuzz.token_sort_ratio(query_lower, combined_text.lower())
        # Boost score if scheme name matches well
        name_score = fuzz.token_sort_ratio(query_lower, scheme_name.lower())
        if name_score > 80:
            score += 30  # Boost

        if debug:
            print(f"[DEBUG] Score: {score} | Scheme: {s.get('scheme_name')}")

        if score >= threshold:
            scored_schemes.append((score, s))

    # Sort by descending score
    scored_schemes.sort(reverse=True, key=lambda x: x[0])
    # ✅ NEW LOGIC: If no score is >= threshold, still return top 1 if available
    if not scored_schemes:
        return []

    if scored_schemes[0][0] < threshold:
        return [scored_schemes[0][1]]  # return best effort match
    # Return top-k relevant matches
    return [s[1] for s in scored_schemes[:top_k]]

# ✅ Export RAW_SCHEMES for use in fallback listing
__all__ = ["retrieve_top_schemes", "flatten_translations", "RAW_SCHEMES"]
