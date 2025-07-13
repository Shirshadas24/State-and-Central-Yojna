# from langchain_huggingface import HuggingFaceEndpoint
# from langchain.prompts import PromptTemplate
# from utils.retriever import retrieve_top_schemes
# from utils.db_logger import log_conversation
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def handle_query(query, language="Hinglish"):
#     print("🔁 Incoming Query:", query)

#     # Always fetch fresh schemes for the current query
#     schemes = retrieve_top_schemes(query, language, top_k=1, debug=True)

#     # Fallback: If no schemes matched, try something generic
#     if not schemes:
#     # 🗂 Show known schemes from JSON
#         from utils.retriever import flatten_translations, RAW_SCHEMES
#         known_schemes = flatten_translations(RAW_SCHEMES, language)
    
#         if not known_schemes and language.lower() != "hinglish":
#             known_schemes = flatten_translations(RAW_SCHEMES, "Hinglish")
    
#         scheme_names = [s.get("scheme_name", "Unnamed") for s in known_schemes]
#         schemes_list = "\n".join([f"🔹 {name}" for name in scheme_names])

#         return (
#         "Couldn't find an exact match. But here are the schemes I currently know about:\n\n" + schemes_list
#         if language.lower() == "english"
#         else "Exact match nahi mila. Yeh woh yojnaayein hain jinke baare mein main janta hoon:\n\n" + schemes_list
#     )
#         return (
#             "Sorry, I couldn't find any scheme for this query."
#             if language.lower() == "english"
#             else "Kshama kijiye, mujhe is prashn ke liye koi yojana nahi mili."
#         )

#     # Build dynamic context for the matched scheme(s)
#     context_blocks = []
#     for s in schemes:
#         if language.lower() == "english":
#             block = f"""
# 🟢 {s.get('scheme_name', 'Name not found')}
# - Benefit: {s.get('benefits', 'Information not available')}
# - Eligibility: {s.get('eligibility', 'Eligibility info not available')}
# - Application Process: {s.get('application_process', 'Process info not available')}
# - Application Link: {s.get('application_link', 'Link not available')}
# """
#         else:
#             block = f"""
# 🟢 {s.get('scheme_name', 'Naam nahi mila')}
# - Laabh: {s.get('benefits', 'Jankari uplabdh nahi hai')}
# - Yogyata: {s.get('eligibility', 'Yogyata ki jankari nahi hai')}
# - Aavedan prakriya: {s.get('application_process', 'Prakriya ki jankari nahi hai')}
# - Aavedan Link: {s.get('application_link', 'Link uplabdh nahi hai')}
# """
#         context_blocks.append(block)

#     combined_context = "\n".join(context_blocks)

#     # Language-based prompt templates
#     if language.lower() == "english":
#         prompt = PromptTemplate(
#             input_variables=["context", "query"],
#             template="""You are a government scheme advisor. Below is information about a government scheme.
# Based on the user's question, provide a simple and direct answer in English. Give a short summary for each scheme. 

# Scheme Information:
# {context}

# User's Question: {query}

# Answer:"""
#         )
#     else:
#         prompt = PromptTemplate(
#             input_variables=["context", "query"],
#             template=f"""Aap ek sarkari yojana advisor ho. Neeche kai yojnaon ki jankari di gayi hai.
# User ke prashn ke aadhar par {language} mein simple explanation dein. Har yojna ke liye short summary dein.

# Yojnaon ki Jankari:
# {{context}}

# User ka Prashna: {{query}}

# Uttar:"""
#         )

#     # 🛠️ Instantiate LLM **inside** the handler — stateless
#     llm = HuggingFaceEndpoint(
#         repo_id="mistralai/Devstral-Small-2505",
#         huggingfacehub_api_token=os.getenv("HF_TOKEN"),
#         temperature=0.5,
#         max_new_tokens=512
#     )

#     try:
#         formatted_prompt = prompt.format(context=combined_context, query=query)
#         response = llm(formatted_prompt)
#         print("🧠 DEBUG RAW RESPONSE:", response)
#     except Exception as e:
#         return f"⚠️ Error from model: {str(e)}"

#     # ✅ Extract response text
#     if isinstance(response, dict):
#         # if 'choices' in response and isinstance(response['choices'], list):
#         #     result = response['choices'][0].get('text', str(response['choices'][0]))
#         if 'generated_text' in response:
#             result = response['generated_text']
#         elif 'text' in response:
#             result = response['text']
#         else:
#             result = str(response)
#     else:
#         result = str(response)
#         # ✅ Log query and response to MongoDB
#     log_conversation(query=query, response=result.strip(), language=language)
#     return result.strip()
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from utils.retriever import retrieve_top_schemes, flatten_translations, RAW_SCHEMES
from utils.db_logger import log_conversation
import os
from dotenv import load_dotenv

load_dotenv()

def handle_query(query, language="Hinglish"):
    print("🔁 Incoming Query:", query)

    # Always fetch fresh schemes for the current query
    schemes = retrieve_top_schemes(query, language, top_k=1, debug=True)

    # Fallback: If no schemes matched, return known scheme names
    if not schemes:
        known_schemes = flatten_translations(RAW_SCHEMES, language)
        if not known_schemes and language.lower() != "hinglish":
            known_schemes = flatten_translations(RAW_SCHEMES, "Hinglish")

        scheme_names = [s.get("scheme_name", "Unnamed") for s in known_schemes]
        schemes_list = "\n".join([f"🔹 {name}" for name in scheme_names])

        response_text = (
            "Couldn't find an exact match. But here are the schemes I currently know about:\n\n" + schemes_list
            if language.lower() == "english"
            else "Exact match nahi mila. Yeh woh yojnaayein hain jinke baare mein main janta hoon:\n\n" + schemes_list
        )

        log_conversation(query=query, response=response_text, language=language)
        return response_text

    # Build context for matched scheme(s)
    context_blocks = []
    for s in schemes:
        if language.lower() == "english":
            block = f"""
🟢 {s.get('scheme_name', 'Name not found')}
- Benefit: {s.get('benefits', 'Information not available')}
- Eligibility: {s.get('eligibility', 'Eligibility info not available')}
- Application Process: {s.get('application_process', 'Process info not available')}
- Application Link: {s.get('application_link', 'Link not available')}
"""
        else:
            block = f"""
🟢 {s.get('scheme_name', 'Naam nahi mila')}
- Laabh: {s.get('benefits', 'Jankari uplabdh nahi hai')}
- Yogyata: {s.get('eligibility', 'Yogyata ki jankari nahi hai')}
- Aavedan prakriya: {s.get('application_process', 'Prakriya ki jankari nahi hai')}
- Aavedan Link: {s.get('application_link', 'Link uplabdh nahi hai')}
"""
        context_blocks.append(block)

    combined_context = "\n".join(context_blocks)

    # Prompt template
    if language.lower() == "english":
        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template="""You are a helpful government scheme advisor.
Answer the user question using the scheme information provided below.  Give a short summary for each scheme. Based on the user's question, provide a simple and direct answer in English.
Be accurate and concise.
Scheme Information:
{context}

User's Question: {query}

Answer:"""
        )
    else:
        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template=f"""Aap ek sarkari yojana advisor hain. Neeche yojnaon ki jankari di gayi hai.
User ke prashn ka uttar {language} mein dein, sirf neeche di gayi jankari ka use karke.

Yojnaon ki Jankari:
{{context}}

User ka Prashna: {{query}}

Uttar:"""
        )

    # Instantiate LLM
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Devstral-Small-2505",
        huggingfacehub_api_token=os.getenv("HF_TOKEN"),
        temperature=0.5,
        max_new_tokens=512
    )

    try:
        formatted_prompt = prompt.format(context=combined_context, query=query)
        print("📄 Prompt Sent:\n", formatted_prompt)
        response = llm.invoke(formatted_prompt)
        print("🧠 DEBUG RAW RESPONSE:", response)
    except Exception as e:
        return f"⚠️ Error from model: {str(e)}"

    # Extract model response
    if isinstance(response, dict):
        result = response.get("generated_text") or response.get("text") or str(response)
    else:
        result = str(response)

    final_response = result.strip()

    # Log conversation
    log_conversation(query=query, response=final_response, language=language)

    return final_response
