
import streamlit as st
from groq import Groq, APIConnectionError, AuthenticationError, RateLimitError
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Chat with Memory · Groq",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────

MODELS = {
    "Llama 3.1 8B   (fastest · free)":      "llama-3.1-8b-instant",
    "Llama 3.3 70B  (smartest · free)":     "llama-3.3-70b-versatile",
    "Llama 3 8B     (balanced · free)":     "llama3-8b-8192",
    "Gemma 2 9B     (Google model · free)": "gemma2-9b-it",
}

DEFAULT_SYSTEM = (
    "You are a helpful, knowledgeable assistant. "
    "Be concise and direct. Use markdown formatting where it helps clarity."
)

# ─────────────────────────────────────────────────────────────
# Session state — runs once per browser tab
# ─────────────────────────────────────────────────────────────

def _init():
    defaults = {
        "messages":      [],   # {"role", "content", "ts", "tokens"}
        "input_tokens":  0,
        "output_tokens": 0,
        "session_start": datetime.now().strftime("%H:%M"),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚙️ Settings")

    # API key — prefers secrets.toml, falls back to text input
    api_key: str = st.secrets.get("GROQ_API_KEY", "") or st.text_input(
        "Groq API key",
        type="password",
        placeholder="gsk_...",
        help="Free key at console.groq.com — no credit card needed.",
    )

    st.divider()

    model_label = st.selectbox("Model", list(MODELS.keys()), index=0)
    model_id    = MODELS[model_label]

    temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.7, step=0.1,
        help="Higher = more creative. Lower = more precise.",
    )
    max_tokens = st.slider(
        "Max response tokens", 256, 4096, 1024, step=256,
    )

    st.divider()

    st.markdown("**System prompt**")
    system_prompt = st.text_area(
        label="system_prompt_hidden",
        value=DEFAULT_SYSTEM,
        height=130,
        label_visibility="collapsed",
        placeholder="Describe the assistant's role or persona…",
    )

    st.divider()

    # Session stats
    st.markdown("**Session stats**")
    turns = len([m for m in st.session_state.messages if m["role"] == "user"])
    c1, c2 = st.columns(2)
    c1.metric("Turns", turns)
    c2.metric(
        "Tokens",
        st.session_state.input_tokens + st.session_state.output_tokens,
        help=f"In: {st.session_state.input_tokens} · Out: {st.session_state.output_tokens}",
    )
    st.caption(f"Started {st.session_state.session_start}")

    st.divider()

    # Export conversation
    def _export() -> str:
        lines = [f"# Chat — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]
        for m in st.session_state.messages:
            who = "**You**" if m["role"] == "user" else "**Assistant**"
            lines.append(f"{who} _{m.get('ts', '')}_\n\n{m['content']}\n")
        return "\n---\n".join(lines)

    if st.session_state.messages:
        st.download_button(
            "⬇️ Export as Markdown",
            data=_export(),
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages      = []
        st.session_state.input_tokens  = 0
        st.session_state.output_tokens = 0
        st.rerun()

# ─────────────────────────────────────────────────────────────
# Main header
# ─────────────────────────────────────────────────────────────

st.title("💬 Chat with Memory")
st.caption(
    f"Model: `{model_id}` · Temperature: `{temperature}` · "
    "Powered by Groq · Free · History preserved until cleared."
)

# ─────────────────────────────────────────────────────────────
# Render conversation history
# ─────────────────────────────────────────────────────────────

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        meta = []
        if "ts"     in msg: meta.append(msg["ts"])
        if "tokens" in msg: meta.append(f"{msg['tokens']} tokens")
        if meta: st.caption(" · ".join(meta))

# ─────────────────────────────────────────────────────────────
# Empty state
# ─────────────────────────────────────────────────────────────

if not st.session_state.messages:
    st.markdown(
        """
        <div style="text-align:center;padding:4rem 0;color:var(--text-color,#888);">
            <div style="font-size:2.5rem;margin-bottom:.75rem">💬</div>
            <div style="font-size:1.15rem;font-weight:600;margin-bottom:.4rem">
                Start a conversation
            </div>
            <div style="font-size:.9rem;opacity:.7;max-width:380px;margin:0 auto;">
                Powered by Groq — free, fast, no rate limit issues.
                14,400 requests per day on the free tier.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# API key gate
# ─────────────────────────────────────────────────────────────

if not api_key:
    st.info(
        "👈 Enter your Groq API key in the sidebar to start.  \n"
        "Get a **free** key at [console.groq.com](https://console.groq.com) — "
        "no credit card needed."
    )
    st.stop()

# ─────────────────────────────────────────────────────────────
# Chat input + Groq API call
# ─────────────────────────────────────────────────────────────

if prompt := st.chat_input("Message the assistant…"):

    # 1. Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    ts_user = datetime.now().strftime("%H:%M")
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "ts": ts_user}
    )

    # 2. Call Groq and stream the response
    with st.chat_message("assistant"):
        box       = st.empty()
        full_text = ""
        in_tok    = 0
        out_tok   = 0

        try:
            client = Groq(api_key=api_key)

            # Build messages list for Groq.
            # Groq uses the OpenAI format:
            #   system message first, then alternating user / assistant.
            api_messages = [{"role": "system", "content": system_prompt}]
            api_messages += [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            # Stream response token by token
            stream = client.chat.completions.create(
                model=model_id,
                messages=api_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )

            for chunk in stream:
                # Each chunk may carry a text delta
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    full_text += delta
                    box.markdown(full_text + "▌")

            # Estimate token count (Groq streaming doesn't return usage)
            out_tok = len(full_text.split())
            in_tok  = sum(len(m["content"].split()) for m in api_messages)

            # Render final text without cursor
            ts_asst = datetime.now().strftime("%H:%M")
            box.markdown(full_text)
            st.caption(f"{ts_asst} · {out_tok} tokens · free")

            # 3. Save and update counters
            st.session_state.messages.append(
                {
                    "role":    "assistant",
                    "content": full_text,
                    "ts":      ts_asst,
                    "tokens":  out_tok,
                }
            )
            st.session_state.input_tokens  += in_tok
            st.session_state.output_tokens += out_tok

        # ── Groq-specific error handling ──────────────────────────────
        except AuthenticationError:
            box.empty()
            st.error(
                "**Invalid API key.**  \n"
                "Check your key at [console.groq.com](https://console.groq.com)."
            )
            st.session_state.messages.pop()

        except RateLimitError:
            box.empty()
            st.warning(
                "**Rate limit hit.**  \n"
                "Free tier: 14,400 requests/day. You've used a lot today.  \n"
                "Wait a few minutes or try again tomorrow."
            )
            st.session_state.messages.pop()

        except APIConnectionError:
            box.empty()
            st.error(
                "**Connection error.**  \n"
                "Could not reach Groq servers. Check your internet connection."
            )
            st.session_state.messages.pop()

        except Exception as e:
            box.empty()
            st.error(f"**Unexpected error:** `{type(e).__name__}: {e}`")
            st.session_state.messages.pop()