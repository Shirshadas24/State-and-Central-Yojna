
# from langchain_core.prompts import PromptTemplate
# from langchain_cohere import ChatCohere
# from utils.retriever import retrieve_top_schemes, flatten_translations, RAW_SCHEMES
# from utils.db_logger import log_conversation
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def handle_query(query, language="Hinglish"):
#     print("🔁 Incoming Query:", query)

   
#     schemes = retrieve_top_schemes(query, language, top_k=1, debug=True)

    
#     if not schemes:
#         known_schemes = flatten_translations(RAW_SCHEMES, language)
#         if not known_schemes and language.lower() != "hinglish":
#             known_schemes = flatten_translations(RAW_SCHEMES, "Hinglish")

#         scheme_names = [s.get("scheme_name", "Unnamed") for s in known_schemes]
#         schemes_list = "\n".join([f"🔹 {name}" for name in scheme_names])

#         response_text = (
#             "Couldn't find an exact match. But here are the schemes I currently know about:\n\n" + schemes_list
#             if language.lower() == "english"
#             else "Exact match nahi mila. Yeh woh yojnaayein hain jinke baare mein main janta hoon:\n\n" + schemes_list
#         )

#         log_conversation(query=query, response=response_text, language=language)
#         return response_text

    
#     context_blocks = []
#     for s in schemes:
#         if language.lower() == "english":
#             block = f"""
#  {s.get('scheme_name', 'Name not found')}
# - Benefit: {s.get('benefits', 'Information not available')}
# - Eligibility: {s.get('eligibility', 'Eligibility info not available')}
# - Application Process: {s.get('application_process', 'Process info not available')}
# - Application Link: {s.get('application_link', 'Link not available')}
# """
#         else:
#             block = f"""
#  {s.get('scheme_name', 'Naam nahi mila')}
# - Laabh: {s.get('benefits', 'Jankari uplabdh nahi hai')}
# - Yogyata: {s.get('eligibility', 'Yogyata ki jankari nahi hai')}
# - Aavedan prakriya: {s.get('application_process', 'Prakriya ki jankari nahi hai')}
# - Aavedan Link: {s.get('application_link', 'Link uplabdh nahi hai')}
# """
#         context_blocks.append(block)

#     combined_context = "\n".join(context_blocks)

    
#     if language.lower() == "english":
#         prompt = PromptTemplate(
#             input_variables=["context", "query"],
#             template="""You are a helpful government scheme advisor.
# Answer the user question using the scheme information provided below. Based on the user's question, provide a simple and direct answer in English.
# Be accurate and detailed. Be sure to include all relevant information which is asked.
# Scheme Information:
# {context}

# User's Question: {query}

# Answer:"""
#         )
#     else:
#         prompt = PromptTemplate(
#             input_variables=["context", "query"],
#             template=f"""Aap ek sarkari yojana advisor hain. Neeche yojnaon ki jankari di gayi hai.
# User ke prashn ka uttar {language} mein dein, sirf neeche di gayi jankari ka use karke.
# Detailed aur sahi uttar dein. Pucha gaya prashn ka uttar dena na bhoolen.
# Yojnaon ki Jankari:
# {{context}}

# User ka Prashna: {{query}}

# Uttar:"""
#         )


#     llm = ChatCohere(        
#         model="command-r")

 
#     try:
#         formatted_prompt = prompt.format(context=combined_context, query=query)
#         print("📄 Prompt Sent:\n", formatted_prompt)
#         response = llm.invoke(formatted_prompt)
#         print("DEBUG RAW RESPONSE:", response)
#     except Exception as e:
#         return f"⚠️ Error from model: {str(e)}"

# # Extract actual content
#     if hasattr(response, "content"):
#         final_response = response.content.strip()
#     elif isinstance(response, dict):
#         final_response = (
#         response.get("generated_text") or
#         response.get("text") or
#         str(response)
#     ).strip()
#     else:
#         final_response = str(response).strip()

# # Log and return
#     log_conversation(query=query, response=final_response, language=language)
#     return final_response


from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from langchain.chains import LLMChain, SequentialChain
from langchain_cohere import ChatCohere
from utils.retriever import SchemeRetriever, RAW_SCHEMES, flatten_translations
from utils.db_logger import log_conversation
from dotenv import load_dotenv
import os

load_dotenv()

retriever = SchemeRetriever(debug=True)
llm = ChatCohere(model="command-r")

# Step 1: Language Detection Chain
detect_lang_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
Detect the language (English, Hindi, Hinglish, Bengali, etc.) of the following query.
Return ONLY the language name.

Query:
{query}

Language:"""
)

lang_chain = LLMChain(llm=llm, prompt=detect_lang_prompt, output_key="language")


# Utility to format schemes per language
def format_scheme(s, language):
    if language.lower() == "english":
        return f"""
{s.get('scheme_name')}
- Benefit: {s.get('benefits')}
- Eligibility: {s.get('eligibility')}
- Application Process: {s.get('application_process')}
- Application Link: {s.get('application_link')}
"""
    else:
        return f"""
{s.get('scheme_name')}
- Laabh: {s.get('benefits')}
- Yogyata: {s.get('eligibility')}
- Aavedan prakriya: {s.get('application_process')}
- Aavedan Link: {s.get('application_link')}
"""

# Step 2: Answer Prompt Template
answer_prompt = PromptTemplate(
    input_variables=["context", "query", "language"],
    template="""
You are a helpful government scheme advisor.

Use ONLY the information provided below to answer the user's query.

The user has asked their question in {language}. So your answer MUST be written in {language} only.

Be specific and detailed.

Scheme Info:
{context}

User Query:
{query}

Your Answer:
"""
)

answer_chain = LLMChain(llm=llm, prompt=answer_prompt, output_key="final_response")


# Final function
def handle_query(query):
    print("🔁 Incoming Query:", query)

    # Step 1: Detect Language
    lang_result = lang_chain.run({"query": query})
    detected_language = lang_result.strip()
    print("🈶 Detected Language:", detected_language)

    # Step 2: Retrieve schemes
    schemes = retriever.invoke(query)

    if not schemes:
        known = flatten_translations(RAW_SCHEMES, detected_language)
        if not known and detected_language.lower() != "hinglish":
            known = flatten_translations(RAW_SCHEMES, "Hinglish")

        scheme_names = [s.get("scheme_name", "Unnamed") for s in known]
        schemes_list = "\n".join([f"🔹 {name}" for name in scheme_names])

        response_text = (
            "Couldn't find an exact match. Here are schemes I know:\n\n" + schemes_list
            if detected_language.lower() == "english"
            else "Exact match nahi mila. Yeh yojnaayein available hain:\n\n" + schemes_list
        )

        log_conversation(query, response_text, detected_language)
        return response_text

    context = "\n".join([format_scheme(s, detected_language) for s in schemes])

    result = answer_chain.run({
        "context": context,
        "query": query,
        "language": detected_language
    })

    final_response = result.strip()
    log_conversation(query, final_response, detected_language)
    return final_response
