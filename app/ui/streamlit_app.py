# streamlit_app.py
import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineAI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state init ────────────────────────────────────────────────────────
# Conversation Memory
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # list of dicts: {role, content, action}

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
 
/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0e0e0e;
    color: #f0ece4;
}
 
/* Hide streamlit branding */
#MainMenu, footer, header {visibility: hidden;}
 
/* Title */
.cine-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: #f0ece4;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.cine-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #888;
    font-weight: 300;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
 
/* Chat container */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    padding: 1rem 0;
    max-height: 60vh;
    overflow-y: auto;
}
 
/* User message bubble */
.msg-user {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 16px 16px 4px 16px;
    padding: 0.9rem 1.2rem;
    max-width: 75%;
    align-self: flex-end;
    margin-left: auto;
    font-size: 0.95rem;
    color: #f0ece4;
}
 
/* Assistant recommend bubble */
.msg-recommend {
    background: #111;
    border: 1px solid #c8a96e33;
    border-left: 3px solid #c8a96e;
    border-radius: 4px 16px 16px 16px;
    padding: 1rem 1.2rem;
    max-width: 80%;
    font-size: 0.9rem;
    color: #d0ccc4;
}
 
/* Assistant explain bubble */
.msg-explain {
    background: #111;
    border: 1px solid #6e9ec833;
    border-left: 3px solid #6e9ec8;
    border-radius: 4px 16px 16px 16px;
    padding: 1rem 1.2rem;
    max-width: 80%;
    font-size: 0.9rem;
    color: #d0ccc4;
    font-style: italic;
    line-height: 1.6;
}
 
/* Movie list inside bubble */
.movie-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.3rem 0;
    border-bottom: 1px solid #222;
    font-size: 0.88rem;
}
.movie-item:last-child { border-bottom: none; }
.movie-num {
    color: #c8a96e;
    font-family: 'DM Serif Display', serif;
    font-size: 1rem;
    min-width: 1.2rem;
}
 
/* Message label */
.msg-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #555;
    margin-bottom: 0.4rem;
    font-weight: 500;
}
 
/* Thread badge */
.thread-badge {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    color: #666;
    font-family: monospace;
    display: inline-block;
    margin-bottom: 1rem;
}
 
/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0a0a0a;
    border-right: 1px solid #1e1e1e;
}
 
/* Input */
.stTextInput > div > div > input {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 12px !important;
    color: #f0ece4 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c8a96e !important;
    box-shadow: 0 0 0 1px #c8a96e44 !important;
}
 
/* Button */
.stButton > button {
    background: #c8a96e !important;
    color: #0e0e0e !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #d4b87a !important;
    transform: translateY(-1px) !important;
}
 
/* Divider */
hr { border-color: #1e1e1e !important; }
 
/* Warning */
.stWarning {
    background: #1a1a1a !important;
    border-color: #c8a96e44 !important;
}
 
/* Slider */
.stSlider > div { color: #888 !important; }
 
/* Multiselect */
.stMultiSelect > div { 
    background: #1a1a1a !important;
    border-color: #2a2a2a !important;
}
 
/* Expander */
.streamlit-expanderHeader {
    background: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 8px !important;
    color: #888 !important;
}
 
/* New conversation button */
.stButton.new-conv > button {
    background: transparent !important;
    color: #555 !important;
    border: 1px solid #2a2a2a !important;
    font-size: 0.8rem !important;
}
.stButton.new-conv > button:hover {
    border-color: #444 !important;
    color: #888 !important;
    transform: none !important;
}
</style>
""", unsafe_allow_html=True
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Movie Recommender 🎬")
    st.markdown('<p class="cine-title">CineAI</p>', unsafe_allow_html=True)
    st.markdown('<p class="cine-subtitle">Conversational film discovery</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Filters
    st.markdown("**Preferences**")

    top_k = st.slider("Results", 1, 20, 5)

    genres = st.multiselect(
        "Filter by genres",
        ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History",
        "Horror", "Music", "Mystery", "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"],
        placeholder="Any genre"
    )


    # Select the user mode
    user_mode = st.segmented_control(
        "Mode",
        ["smart", "quality", "taste"],
        default="smart"
    )

    # Year filter
    with st.expander("Year range"):

        year_mode = st.radio("Year mode", ["All time", "Custom"], label_visibility="collapsed") 
        if year_mode == "All time":
            year_from, year_to = 1900, 2026

        else:
            years = list(range(2026, 1899, -1))
            col1, col2 = st.columns(2)

            with col1:
                year_from = st.selectbox("From", years, index=len(years)-1)

            with col2:
                year_to = st.selectbox("To", years, index=0)

    st.markdown("---")


    if st.session_state.thread_id:
            st.markdown(
                f'<div class="thread-badge">🔗 {st.session_state.thread_id[:20]}...</div>',
                unsafe_allow_html=True
            )
            continue_conv = st.checkbox("Continue this conversation", value=True)
    
            if st.button("New conversation", key="new_conv"):
                st.session_state.thread_id = None
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.markdown('<p style="color:#555; font-size:0.8rem;">No active conversation</p>', unsafe_allow_html=True)
        continue_conv = False

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("---")

# Chat history display
if st.session_state.chat_history:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="msg-user">{msg["content"]}</div>',
                unsafe_allow_html=True
            )
        elif msg["role"] == "assistant":
            action = msg.get("action", "recommend")

            if action == "explain":
                st.markdown(
                    f'<div class="msg-explain">'
                    f'<div class="msg-label">💡 Explanation</div>'
                    f'{msg["content"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )
            elif action == "recommend" and isinstance(msg.get("movies"), list):
                movies_html = "".join([
                    f'<div class="movie-item"><span class="movie-num">{i}.</span>{m}</div>'
                    for i, m in enumerate(msg["movies"], 1)
                ])
                st.markdown(
                    f'<div class="msg-recommend">'
                    f'<div class="msg-label">🎬 Recommendations</div>'
                    f'{movies_html}'
                    f'</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="msg-recommend">'
                    f'<div class="msg-label">ℹ️ Message</div>'
                    f'{msg["content"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )
            st.markdown("---")
else:
    st.markdown(
        '<p style="color:#333; font-size:0.9rem; text-align:center; padding:3rem 0;">'
        'Start a conversation — ask for a movie recommendation or explain a title.'
        '</p>',
        unsafe_allow_html=True
    )

# ── Input area ────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5,1])

with col_input:
    user_input = st.text_input(
        "Message",
        placeholder = "Recommend me something emotional... / Why did you recommend Her?",
        label_visibility = "collapsed",
        key = "user_input"
    )

with col_btn:
    send = st.button("Send →")

# ── Handle send ───────────────────────────────────────────────────────────────
if send:
    if not user_input.strip():
        st.warning("Type something first.")
    else:
        thread_id = st.session_state.thread_id if continue_conv else None

        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    #http://localhost:8000/agent
                    "http://api:8000/agent",
                    json={
                        "query": user_input,
                        "top_k": top_k,
                        "filters": {
                            "genres": genres,
                            "year_from": year_from,
                            "year_to": year_to
                        },
                        "user_mode": user_mode,
                        "thread_id": thread_id
                    },
                    timeout=300
                )
                response.raise_for_status()
                data = response.json()
                print("\nDATA FROM API: ", data)

            except requests.exceptions.Timeout:
                st.error("Request time out. The models may stil be loading.")
            except Exception as e:
                st.error(f"Error connecting to the API: {e}")
                st.stop()

        # Save the thread_id
        st.session_state.thread_id = data.get("thread_id")

        action = data.get("action")
        movies = data.get("movies", [])
        explanation = data.get("explanation")
        message = data.get("message")
        print("\nEXPLANATION: ", explanation)

        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # Add assistant response to chat history
        if action == "explain" and explanation:
            st.session_state.chat_history.append({
                "role": "assistant",
                "action": "explain",
                "content": explanation,
            })

        elif movies:
            st.session_state.chat_history.append({
                "role": "assistant",
                "action": "recommend",
                "movies": movies,
                "content": ", ".join(movies)
            })

        elif message:
            st.session_state.chat_history.append({
                "role": "assistant",
                "action": "clarify",
                "content": message
            })
        
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "action": "other",
                "content": "No results found."
            })
 
        st.rerun()



