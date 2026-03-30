import threading
import time
import streamlit as st

# Page config
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide"
)

# Import Gradio app
from app import demo

# Launch Gradio in background
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

# UI Header
st.markdown("""
<h1 style='text-align:center;'>🩺 Diabetes Prediction System</h1>
<p style='text-align:center;'>Gradio UI embedded inside Streamlit</p>
<hr>
""", unsafe_allow_html=True)

# Embed Gradio
st.components.v1.iframe(
    src="http://localhost:7860",
    height=800
)

# Footer
st.markdown("""
<p style='text-align:center; font-size:0.8rem; color:gray;'>
⚕️ For educational purposes only. Not a substitute for medical advice.
</p>
""", unsafe_allow_html=True)