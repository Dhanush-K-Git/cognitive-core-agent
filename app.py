import streamlit as st
from main import app as agent_app # Importing your LangGraph engine!

# 1. Page Configuration
st.set_page_config(page_title="Cognitive Core Agent", page_icon="🔍", layout="centered")
st.title("Cognitive Core Agent")
st.markdown("Ask a complex question, and I will autonomously plan, research, and write a comprehensive report.")

# 2. Memory Manager Sidebar
with st.sidebar:
    st.header("📂 Session Manager")
    st.write("Type a session name to load past research.")
    session_id = st.text_input("Session ID:", value="default_session")

# Lock in the config for LangGraph
config = {"configurable": {"thread_id": session_id}}

# 3. Sync Streamlit Memory with SQLite (THE UPGRADE)
if "current_session" not in st.session_state or st.session_state.current_session != session_id:
    st.session_state.current_session = session_id
    st.session_state.messages = []
    
    try:
        # 🚀 Fetch the ENTIRE history of this session from the SQLite Checkpointer
        # get_state_history returns newest to oldest, so we reverse it to draw top-to-bottom
        state_history = list(agent_app.get_state_history(config))
        state_history.reverse()
        
        seen_reports = set() # To prevent drawing duplicate bubbles
        
        for state in state_history:
            vals = state.values
            # We only want to draw states where the agent actually finished its report
            if "final_report" in vals and vals["final_report"] and vals["final_report"] not in seen_reports:
                
                # Extract the clean prompt (removes the "Previous Chat History" injection)
                raw_task = vals.get("task", "")
                if "User's New Request:" in raw_task:
                    clean_prompt = raw_task.split("User's New Request:")[-1].strip()
                else:
                    clean_prompt = raw_task.strip()
                    
                # Add the chat bubbles back to Streamlit's visual memory!
                st.session_state.messages.append({"role": "user", "content": clean_prompt})
                st.session_state.messages.append({"role": "assistant", "content": vals["final_report"]})
                
                seen_reports.add(vals["final_report"])
    except Exception as e:
        # If it's a brand new session and errors out, just ignore and start fresh
        pass

# 4. Display Chat History on the Screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. The Chat Input Box
# This creates the text box at the bottom of the screen.
if prompt := st.chat_input("What would you like me to research?"):
    
    # Immediately show the user's question on the screen
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

   # 5. Run the Agent Engine!
    with st.chat_message("assistant"):
        with st.spinner("Analyzing, planning, and researching (this may take a minute)..."):
            
            # --- NEW: Context Injection ---
            # Grab the last 4 messages from the screen to give the agent context
            history = ""
            for msg in st.session_state.messages[-4:]:
                history += f"{msg['role'].capitalize()}: {msg['content']}\n\n"
                
            enriched_prompt = f"Previous Chat History:\n{history}\nUser's New Request: {prompt}"
            
            # Feed the ENRICHED prompt into the state
            initial_state = {
                "task": enriched_prompt,
                "plan": [],
                "research_data": [],
                "final_report": ""
            }
            
            result = agent_app.invoke(initial_state, config=config)
            final_answer = result["final_report"]
            
            st.markdown(final_answer)
            
    # Save the assistant's answer to the chat history
    st.session_state.messages.append({"role": "assistant", "content": final_answer})