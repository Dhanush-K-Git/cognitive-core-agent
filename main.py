import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

# Import the files YOU built!
from state import AgentState
from planner import planner_node
from researcher import researcher_node
from writer import writer_node

# 1. Load the Vault
load_dotenv()

# 2. Initialize the Graph Map
# We pass our AgentState to tell the graph what the clipboard looks like
workflow = StateGraph(AgentState)

# 3. Add the Nodes (The Agents)
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)

# 4. Connect the Nodes with Edges (The Flow)
workflow.add_edge(START, "planner")          # Start point goes to the Manager
workflow.add_edge("planner", "researcher")   # Manager passes plan to Worker
workflow.add_edge("researcher", "writer")    # Worker passes notes to Editor
workflow.add_edge("writer", END)             # Editor finishes the job

# 5. Compile the Graph into a runnable application
app = workflow.compile()

# --- RUN THE APP ---
if __name__ == "__main__":
    print("🤖 Welcome to DeepResearch Agent!")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_query = input("\nAsk a complex research question: ")
        
        if user_query.lower() in ['quit', 'exit']:
            print("Shutting down...")
            break
            
        print("\n=== STARTING RESEARCH PIPELINE ===\n")
        
        # We start the graph by passing the initial state
        initial_state = {
            "task": user_query,
            "plan": [],
            "research_data": [],
            "final_report": ""
        }
        
        # Run the entire workflow end-to-end!
        result = app.invoke(initial_state)
        
        print("\n\n" + "="*60)
        print("✅ FINAL REPORT:")
        print("="*60)
        print(result["final_report"])
        print("="*60 + "\n")