# 🔍 Cognitive Core Agent: Autonomous Deep Research Agent

An enterprise-grade, multi-agent research system built with LangGraph and Streamlit. This application autonomously breaks down complex queries, executes live internet searches, and synthesizes accurate, citation-backed reports while maintaining long-term conversational memory.

## 🚀 Key Features

* **Multi-Agent Orchestration (LangGraph):** Utilizes a cyclical graph architecture dividing tasks between a Planner (query breakdown), Researcher (live web scraping), and Writer (synthesis and conflict resolution).
* **Persistent Stateful Memory:** Implements an SQLite checkpointer and real-time context injection to maintain long-term memory across complex, multi-turn conversational threads.
* **Anti-Hallucination Guardrails:** Engineered with strict prompt constraints requiring explicit source citations and mandatory conflict resolution for contradictory web data.
* **Live Market Intelligence:** Bypasses standard LLM knowledge cutoffs by integrating live search tools to retrieve up-to-the-minute data, pricing, and news.
* **Interactive Web UI:** Fully accessible via a responsive Streamlit dashboard.

## 🛠️ Tech Stack

* **Backend:** Python, LangGraph, LangChain
* **Frontend:** Streamlit
* **Database/Memory:** SQLite (`langgraph-checkpoint-sqlite`)
* **LLM Provider:** Groq (Llama-3) / OpenAI *(Adjust based on what you used)*

## 🧠 Architecture Flow

1.  **User Input:** The user submits a complex analytical question via the Streamlit UI.
2.  **Context Injection:** The system appends previous chat history to the prompt for pronoun resolution and context maintenance.
3.  **Planner Agent:** Deconstructs the enriched prompt into 3-5 executable search steps.
4.  **Researcher Agent:** Executes searches using live web tools and compiles raw markdown notes.
5.  **Writer Agent:** Analyzes the raw data, applies anti-hallucination rules, and generates a formatted, final markdown report.

## 👤 Author
**Dhanush Kumar**
*AI & Machine Learning Engineer*
[Link to your LinkedIn]