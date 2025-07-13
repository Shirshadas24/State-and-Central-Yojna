import re
import json
from thefuzz import fuzz

# import re
import string
# ⬇ Add at the top
KEYWORD_ALIAS = {
    "ayushman": "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
    "atal": "Atal Pension Yojana (APY)",
    "beti": "Beti Bachao, Beti Padhao (BBBP)",
    "bbbp": "Beti Bachao, Beti Padhao (BBBP)",
    "pmjay": "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
    "kisan": "Pradhan Mantri Kisan Samman Nidhi (PM-Kisan)",
    "pmjay": "Ayush Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
    "pm kisan": "Pradhan Mantri Kisan Samman Nidhi (PM-Kisan)",
    "pm awas": "Pradhan Mantri Awas Yojana (PMAY)",
    "deen": "Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)",
    "ddugky": "Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)",
    "pm awas yojana": "Pradhan Mantri Awas Yojana (PMAY)",
    "digital": "Digital India Programme",
    "digital program": "Digital India Programme",
    "digital india": "Digital India Programme",
    "jal jeevan": "Jal Jeevan Mission (JJM)",
    "jjm": "Jal Jeevan Mission (JJM)",
    "swachh bharat": "Swachh Bharat Mission (SBM)",
    "sbm": "Swachh Bharat Mission (SBM)",   
    "jal mission": "Jal Jeevan Mission (JJM)",
    "health mission": "National Health Mission (NHM)",
    "nhm": "National Health Mission (NHM)",
    "Family Welfare":"National Health Mission (NHM)",
    "Samagra Shiksha Abhiyan":"Samagra Shiksha ",
    "education":"Samagra Shiksha ",
    "education scheme":"Samagra Shiksha ",
    "nsap":"National Social Assistance Programme (NSAP)",
    "nsap scheme":"National Social Assistance Programme (NSAP)",
    "social assistance":"National Social Assistance Programme (NSAP)",
    "kisan samman":"Pradhan Mantri Kisan Samman Nidhi (PM-Kisan)",

}

def clean_query(query):
    
    query = query.lower()
    query = query.replace("yojna", "yojana")
    query = query.replace("scheme", "yojana")

    query = query.translate(str.maketrans('', '', string.punctuation))

    
    query = re.sub(
        r'\b(kya hai|what is|ka hai|ke baare mein|about|kaise apply karein?|kaise apply kare|how to apply|'
        r'application link|apply online|official website|website|link|application process|helpline number kya hai|helpline number)\b',
        '',
        query,
        flags=re.IGNORECASE
    )

   
    query = re.sub(r'\s+', ' ', query)

    return query.strip()


with open("data/schemes.json", "r", encoding="utf-8") as f:
    RAW_SCHEMES = json.load(f)


def flatten_translations(raw_data, language="Hinglish"):
    flattened = []
    for scheme in raw_data:
        for trans in scheme["translations"]:
            if trans["language"].lower() == language.lower():
                flattened.append(trans)
                break
    return flattened


def retrieve_top_schemes(query, language="Hinglish", top_k=3, threshold=20, debug=False):
    schemes = flatten_translations(RAW_SCHEMES, language)
    if not schemes and language.lower() != "hinglish":
        
        if debug:
            print(f"[FALLBACK] No schemes found for language '{language}', falling back to 'Hinglish'")
        schemes = flatten_translations(RAW_SCHEMES, "Hinglish")
    scored_schemes = []

    query_clean = clean_query(query)
    query_lower = query_clean.lower()
    for keyword, scheme_name in KEYWORD_ALIAS.items():
        if keyword in query_lower:
            for s in schemes:
                if scheme_name.lower() in s.get("scheme_name", "").lower():
                    if debug:
                        print(f"[ALIAS MATCH] {s['scheme_name']} via keyword '{keyword}'")
                    return [s]
    
    for s in schemes:
        scheme_name = s.get("scheme_name", "").lower()
        if query_lower == scheme_name or query_lower in scheme_name or scheme_name in query_lower:
            if debug:
                print(f"[EXACT MATCH] {s['scheme_name']}")
            return [s]

    
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
        
        name_score = fuzz.token_sort_ratio(query_lower, scheme_name.lower())
        if name_score > 80:
            score += 30  # Boost

        if debug:
            print(f"[DEBUG] Score: {score} | Scheme: {s.get('scheme_name')}")

        if score >= threshold:
            scored_schemes.append((score, s))

    
    scored_schemes.sort(reverse=True, key=lambda x: x[0])
    
    if not scored_schemes:
        return []

    if scored_schemes[0][0] < threshold:
        return [scored_schemes[0][1]]  
    return [s[1] for s in scored_schemes[:top_k]]

__all__ = ["retrieve_top_schemes", "flatten_translations", "RAW_SCHEMES"]
