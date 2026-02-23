import streamlit as st
from main import app as agent_app # Importing your LangGraph engine!

# 1. Page Configuration
st.set_page_config(page_title="Cognitive Core Agent", page_icon="🔍", layout="centered")
st.title("Cognitive Core Agent")
st.markdown("Ask a complex question, and I will autonomously plan, research, and write a comprehensive report.")

# 2. Initialize Chat Memory (Session State)
# We use session_state so the app doesn't forget the chat history when it refreshes.
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat History
# This loops through past messages and displays them on the screen.
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
            
            config = {"configurable": {"thread_id": "client_session_1"}}
            result = agent_app.invoke(initial_state, config=config)
            final_answer = result["final_report"]
            
            st.markdown(final_answer)
            
    # Save the assistant's answer to the chat history
    st.session_state.messages.append({"role": "assistant", "content": final_answer})