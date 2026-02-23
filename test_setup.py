import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tavily import TavilyClient

# 1. Load the vault (the .env file)
load_dotenv()

print("--- STARTING SANITY CHECK ---")

# --- TEST 1: THE BRAIN (GROQ) ---
try:
    print("\n1. Testing the Brain (Groq)...")
    # We use the newest Llama 3.3 model
    llm = ChatGroq(model="llama-3.3-70b-versatile") 
    response = llm.invoke("Say 'System Operational' if you can hear me.")
    print(f"✅ Brain Response: {response.content}")
except Exception as e:
    print(f"❌ Brain Failed: {e}")

# --- TEST 2: THE EYES (TAVILY) ---
try:
    print("\n2. Testing the Eyes (Tavily)...")
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    # Perform a real search
    query = "Who is the PM of India"
    results = tavily.search(query=query, search_depth="advanced", include_answer=True)    
    # DEFENSIVE CODING: Check if we actually got results!
    if results.get('results') and len(results['results']) > 0:
        # If the list is NOT empty, print the first one
        print(f"✅ Eyes Response: {results['results'][0]['content'][:100]}...")
    else:
        # If the list IS empty, just warn us (don't crash!)
        print(f"⚠️ Eyes worked (API connected), but found no results for '{query}'.")
        print(f"   (Raw output: {results})")
        
except Exception as e:
    print(f"❌ Eyes Failed: {e}")

print("\n--- CHECK COMPLETE ---")