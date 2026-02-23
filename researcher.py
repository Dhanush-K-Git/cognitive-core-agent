import os
from dotenv import load_dotenv
from tavily import TavilyClient
from state import AgentState

# 1. Load the Vault (Security first!)
load_dotenv()

# 2. Setup the Tools
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# 3. The Function (The Worker)
def researcher_node(state: AgentState):
    print("--- RESEARCHER AGENT RUNNING ---")
    
    # Get the To-Do List from the Clipboard
    plan = state["plan"]
    results = []
    
    # Loop through each step in the plan
    for step in plan:
        print(f"🔎 Searching for: {step}")
        
        try:
            # Use the "Eyes" to find the answer
            # search_depth="advanced" checks more sources
            search_result = tavily.search(query=step, search_depth="advanced", include_answer=True)
            
            # Logic: Did Tavily give us a direct answer?
            if search_result.get("answer"):
                content = search_result["answer"]
            else:
                # Fallback: If no direct answer, join the top 2 search snippets
                # This prevents "index out of range" errors
                snippets = [r["content"] for r in search_result.get("results", [])[:2]]
                content = "\n".join(snippets)
            
            # Format the data neatly to save to state
            results.append(f"Source: {step}\nContent: {content}\n---")
            
        except Exception as e:
            print(f"❌ Error searching for {step}: {e}")
            results.append(f"Error searching for {step}: {str(e)}")

    # Write the findings back to the Clipboard
    # We return a dictionary with the key "research_data" to update the state
    return {"research_data": results}

# --- TEST CODE (Only runs if you execute this file directly) ---
if __name__ == "__main__":
    # Fake a state (as if the Planner already ran)
    test_state = {
        "plan": [
            "Who is the current Prime Minister of India?",
            "What is the capital of France?"
        ]
    }
    
    # Run the researcher
    output = researcher_node(test_state)
    
    print("\n✅ RESEARCH COMPLETE:")
    for item in output["research_data"]:
        print(item)