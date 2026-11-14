
from __future__ import annotations

import importlib.util
import sys
import uuid
from pathlib import Path

import streamlit as st

WEEK4 = Path(__file__).resolve().parent
AGENT_PATH = WEEK4 / "agent.py"

st.set_page_config(page_title="Netixsol Enquiry Assistant", page_icon="💬")
st.title("Netixsol Enquiry Assistant")
st.caption("Ask about Netixsol services or discuss a project enquiry.")

# Each browser session gets its own independently loaded agent module.
# This isolates pending previews and conversation history between tabs.
if "agent_module" not in st.session_state:
    session_key = uuid.uuid4().hex
    module_name = f"week4_agent_session_{session_key}"

    spec = importlib.util.spec_from_file_location(module_name, AGENT_PATH)
    if spec is None or spec.loader is None:
        st.error("The agent module could not be loaded.")
        st.stop()

    agent = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = agent
    spec.loader.exec_module(agent)

    # Capture sources retrieved during each turn for display below the answer.
    agent._app_sources = []
    original_search = agent.search_netixsol

    def tracked_search(query: str) -> dict:
        result = original_search(query)
        for match in result.get("matches", []):
            url = match.get("source_url", "")
            if url and url not in [item["url"] for item in agent._app_sources]:
                agent._app_sources.append({
                    "title": match.get("title", "Source"),
                    "url": url,
                })
        return result

    agent.search_netixsol = tracked_search

    # Capture the actual preview returned by the existing validation tool.
    agent._app_preview_result = None
    original_save = agent.save_enquiry

    def tracked_save(*args, **kwargs):
        result = original_save(*args, **kwargs)
        if result.get("status") == "preview_created":
            agent._app_preview_result = result
        return result

    agent.save_enquiry = tracked_save

    st.session_state.agent_module = agent
    st.session_state.messages = []

agent = st.session_state.agent_module

# Display previous messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("preview"):
            st.warning("Enquiry preview — not submitted")
            st.json(message["preview"])
            st.info(message.get("confirmation_instruction", ""))

        if message.get("sources"):
            with st.expander("Sources used"):
                for source in message["sources"]:
                    st.markdown(f"- [{source['title']}]({source['url']})")

# Handle a new message.
user_message = st.chat_input("Ask a question or describe your project...")

if user_message:
    st.session_state.messages.append({
        "role": "user",
        "content": user_message,
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    agent._app_sources = []
    agent._app_preview_result = None

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                answer = agent.run_agent_turn(user_message)

            preview_result = agent._app_preview_result or {}
            preview = preview_result.get("preview")
            instruction = preview_result.get("confirmation_instruction", "")
            sources = list(agent._app_sources)

            st.markdown(answer)

            if preview:
                st.warning("Review this enquiry carefully. It has NOT been submitted.")
                st.json(preview)
                st.info(instruction)

            if sources:
                with st.expander("Sources used"):
                    for source in sources:
                        st.markdown(f"- [{source['title']}]({source['url']})")

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "preview": preview,
                "confirmation_instruction": instruction,
                "sources": sources,
            })

        except Exception:
            friendly_message = (
                "I'm sorry, but I couldn't complete that request right now. "
                "Please try again in a moment."
            )
            st.markdown(friendly_message)
            st.session_state.messages.append({
                "role": "assistant",
                "content": friendly_message,
            })
