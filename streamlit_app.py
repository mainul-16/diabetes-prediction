"""
streamlit_app.py  —  Streamlit wrapper to host Gradio on Streamlit Cloud
------------------------------------------------------------------------
Streamlit Cloud requires a file named `streamlit_app.py` as the entry point.
This file launches the Gradio app inside an iframe embedded in Streamlit.

How it works:
  1. Streamlit Cloud runs this file.
  2. This file starts the Gradio server in a background thread on port 7860.
  3. Streamlit embeds the Gradio UI in an iframe.
"""

import threading
import time
import streamlit as st
import gradio as gr

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide"
)

# ── Import the Gradio app object from app.py ──────────────────────────────────
from app import demo   # 'demo' is the gr.Blocks() object defined in app.py

# ── Launch Gradio in a background thread (only once) ─────────────────────────
@st.cache_resource
def launch_gradio():
    """Start Gradio server on port 7860 in a background thread."""
    def _run():
        demo.launch(
           demo.launch(server_name="127.0.0.1", server_port=7860, share=False)"""
streamlit_app.py  —  Streamlit wrapper to host Gradio on Streamlit Cloud
"""

import threading
import time
import streamlit as st

st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide"
)

from app import demo

@st.cache_resource
def launch_gradio():
    def _run():
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            quiet=True,
            prevent_thread_lock=True
        )
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    time.sleep(3)
    return "running"

launch_gradio()

st.markdown("""
    <h1 style='text-align:center; color:#1A5276;'>🩺 Diabetes Prediction System</h1>
    <p style='text-align:center; color:#555; font-size:1rem;'>
        Built with Gradio · Deployed on Streamlit Cloud · Model: Random Forest
    </p>
    <hr style='margin-bottom: 0;'>
""", unsafe_allow_html=True)

st.components.v1.iframe(
    src="http://localhost:7860",
    width=None,
    height=820,
    scrolling=True
)

st.markdown("""
    <p style='text-align:center; color:#aaa; font-size:0.8rem; margin-top:12px;'>
        ⚕️ For educational purposes only. Not a substitute for medical advice.
        | Team FCB World — Diabetes Prediction System
    </p>
""", unsafe_allow_html=True)
            quiet=True,
            prevent_thread_lock=True
        )
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    time.sleep(3)   # Give Gradio a moment to start
    return "running"

launch_gradio()

# ── Streamlit page content ────────────────────────────────────────────────────
st.markdown("""
    <h1 style='text-align:center; color:#1A5276;'>🩺 Diabetes Prediction System</h1>
    <p style='text-align:center; color:#555; font-size:1rem;'>
        Built with Gradio · Deployed on Streamlit Cloud · Model: Random Forest
    </p>
    <hr style='margin-bottom: 0;'>
""", unsafe_allow_html=True)

# Embed the Gradio app in an iframe
st.components.v1.iframe(
    src="http://localhost:7860",
    width=None,
    height=820,
    scrolling=True
)

# Footer
st.markdown("""
    <p style='text-align:center; color:#aaa; font-size:0.8rem; margin-top:12px;'>
        ⚕️ For educational purposes only. Not a substitute for medical advice.
        | Team FCB World — Diabetes Prediction System
    </p>
""", unsafe_allow_html=True)
