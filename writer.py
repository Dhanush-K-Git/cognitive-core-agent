import os
from dotenv import load_dotenv # <-- Import this
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from state import AgentState

# --- FIX: LOAD THE VAULT IMMEDIATELY ---
load_dotenv()

# 1. Setup the Brain
# We use temperature=0.7 here because writing needs a little creativity
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

# 2. The Prompt (The Instructions)
WRITER_PROMPT = """You are a Senior Research Analyst.
Your goal is to write a comprehensive report based ONLY on the provided research notes.

Strict Rules:
1. DO NOT hallucinate. Only include facts explicitly found in the Research Notes.
2. CONFLICT RESOLUTION: If the research notes contain conflicting information (e.g., different squad lists), prioritize the most recently published data or officially announced changes (like injury replacements). 
3. If the user's prompt is too vague to give a definitive answer, point out the ambiguity.
4. Organize the report with clear headings (##) and bullet points.
5. Cite your sources (e.g., [Source: Article Name]) if available in the notes.
"""

# 3. The Function (The Agent's Logic)
def writer_node(state: AgentState):
    print("--- WRITER AGENT RUNNING ---")
    
    # Get the User's Task and the Researcher's Notes
    user_task = state["task"]
    research_data = state["research_data"]
    
    # Combine all notes into one big string
    notes_text = "\n\n".join(research_data)
    
    # Create the message for the Brain
    messages = [
        SystemMessage(content=WRITER_PROMPT),
        HumanMessage(content=f"User Question: {user_task}\n\nResearch Notes:\n{notes_text}")
    ]
    
    # Get the final report
    response = llm.invoke(messages)
    
    # Write the report to the Clipboard
    return {"final_report": response.content}

# --- TEST CODE ---
if __name__ == "__main__":
    
    # Fake a state (as if the Researcher just finished)
    test_state = {
        "task": "Who is the Prime Minister of India?",
        "research_data": [
            "Source: Search Step 1\nContent: Narendra Modi is the current Prime Minister of India since 2014.",
            "Source: Search Step 2\nContent: He is a member of the Bharatiya Janata Party (BJP)."
        ]
    }
    
    # Run the writer
    output = writer_node(test_state)
    
    print("\n✅ FINAL REPORT GENERATED:\n")
    print(output["final_report"])