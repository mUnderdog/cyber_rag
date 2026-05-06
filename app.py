import streamlit as st
from rag_chat import get_rag_response
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PolicyCortex | Security Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR CYBERSECURITY THEME ---
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid #30363d;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Chat inputs */
    .stChatInputContainer {
        border-color: #30363d !important;
        background-color: #161b22 !important;
    }
    
    /* User Message */
    [data-testid="chatAvatarIcon-user"] {
        background-color: #238636 !important;
    }
    
    /* Assistant Message */
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #1f6feb !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #3fb950 !important;
    }
    
    /* Glowing effect for the title */
    .glow-title {
        color: #00ff00;
        text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Secondary text */
    .sub-text {
        text-align: center; 
        color: #8b949e;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00ff00 !important;'>🔒 SYS_ADMIN</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    col1.metric("Status", "ONLINE", delta="Secure")
    col2.metric("Latency", "12ms", delta="-2ms", delta_color="inverse")
    
    st.markdown("---")
    st.markdown("### Active Databases")
    st.success("✅ GDPR Regulations")
    st.success("✅ OWASP Top 10")
    st.success("✅ CIS Controls")
    
    st.markdown("---")
    st.markdown("### Capabilities")
    st.code('''
- Threat Analysis
- Policy Compliance
- Vulnerability Checking
    ''', language="markdown")
    
    st.markdown("---")
    if st.button("Clear Cache & History", type="primary"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CONTENT ---
st.markdown("<h1 class='glow-title'>CYBER_RAG // TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Secure encrypted connection established. Ready to query policy databases.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "assistant", "content": "Authentication successful. I am PolicyCortex, your AI Security Policy Assistant. How can I assist you with GDPR, OWASP, or CIS compliance today?"}
    ]

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Enter query >_"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Simulate typing/processing
        with st.spinner("Decrypting databases and retrieving context..."):
            response = get_rag_response(prompt)
            
            # Simulated typing effect for a more "terminal" feel
            full_response = ""
            for chunk in response.split(" "):
                full_response += chunk + " "
                time.sleep(0.015)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})