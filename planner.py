import os
from dotenv import load_dotenv  # <--- IMPORT THIS AT THE TOP
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from state import AgentState

# --- FIX: LOAD THE VAULT IMMEDIATELY ---
load_dotenv() 

# 1. Setup the Brain
# Now this works because the Vault is already open!
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 2. The Prompt (The Instructions)
import datetime

# Get today's exact date
today = datetime.date.today().strftime("%B %d, %Y")

# Notice the 'f' before the quotes! This allows the {today} variable to work.
import datetime

# Get today's exact date
today = datetime.date.today().strftime("%B %d, %Y")

# Notice the 'f' before the quotes! This allows the {today} variable to work.
PLANNER_PROMPT = f"""You are a Lead Research Planner.
Today's date is {today}.
Your goal is to break down a complex user query into a list of specific search steps.

Rules:
1. Steps must be clear and concise.
2. Always append the current year to search queries if the user asks for current events.
3. Include at least 3 distinct steps.
4. Do not answer the question yourself. ONLY output the plan.
5. Output the plan as a numbered list.
"""
# 3. The Function (The Agent's Logic)
def planner_node(state: AgentState):
    print("--- PLANNER AGENT RUNNING ---")
    
    # Get the user's request from the State
    user_task = state["task"]
    
    # Send instructions + task to the Brain
    messages = [
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=user_task)
    ]
    
    # Get the response
    response = llm.invoke(messages)
    
    # Clean up the response
    plan_text = response.content
    steps = [line.strip() for line in plan_text.split("\n") if line.strip()]
    
    # Update the State
    return {"plan": steps}

# --- TEST CODE ---
if __name__ == "__main__":
    # Fake a user request
    test_state = {"task": "Find the current CEO of Microsoft and their key achievements in 2024."}
    
    # Run the planner
    result = planner_node(test_state)
    
    print("\n✅ PLAN GENERATED:")
    for step in result["plan"]:
        print(step)