import base64
import sys
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# Ensure we can import auth.py from the main folder
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))
import auth

st.set_page_config(
    page_title="ELLI | Information Center",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- MEMORY PRESERVATION & GATEKEEPER ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

try:
    session = auth.supabase.auth.get_session()
    if session:
        st.session_state.logged_in = True
        st.session_state.user_email = session.user.email
except Exception:
    pass

if not st.session_state.logged_in:
    st.error("Please log in from the main interface to view this page.")
    st.page_link("webpage.py", label="Return to Login", icon="🔒")
    st.stop()


# --- SHARED UI LOGIC ---
components.html(
    """
    <script>
    const parentDoc = window.parent.document;
    if (!parentDoc.getElementById('elli-lottie-bg')) {
        const script = parentDoc.createElement('script');
        script.src = "https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js";
        parentDoc.head.appendChild(script);

        const container = parentDoc.createElement('div');
        container.id = 'elli-lottie-bg';
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100vw';
        container.style.height = '100vh';
        container.style.zIndex = '0';
        container.style.pointerEvents = 'none';
        container.style.opacity = '0.12';

        script.onload = () => {
            container.innerHTML = `
                <lottie-player src="https://lottie.host/80f7602e-13cb-4a11-8ec8-8cf81e3c8ca4/4xJ1t2T0B8.json" background="transparent" speed="0.6" style="width: 100%; height: 100%;" loop autoplay></lottie-player>
            `;
        };

        const stApp = parentDoc.querySelector('[data-testid="stAppViewContainer"]') || parentDoc.body;
        stApp.appendChild(container);
    }
    </script>
    """,
    height=0,
    width=0,
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
        :root { --ink:#181b1a; --panel:#202523; --mint:#1ee5aa; --gold:#ffcb05; --soft:#b9c0bc; }
        # .stApp { background:radial-gradient(circle at 25% 12%, #2a3530 0, #181b1a 32rem); color:#f5f7f5;} 
        [data-testid="stHeader"] { background:transparent; } #MainMenu, footer { visibility:hidden; }
        .block-container { max-width:1400px; padding:2rem 3.5rem 2rem; position: relative; z-index: 10; }
        
        .elli-brand { display:flex; align-items:flex-end; gap:0.8rem; margin:.2rem 0 1rem 0; }
        .elli-brand h1 { font:700 clamp(2.5rem,6vw,4rem)/.72 "Space Grotesk",sans-serif; letter-spacing:0; margin:0; color:#f2f4f2; }
        .elli-brand p { font:600 0.8rem/1.22 "Space Grotesk",sans-serif; color:#c5cbc7; margin:0 0 0.3rem 0; max-width:11rem; }
        
        .hero-section { padding:2.2rem; border:1px solid rgba(30,229,170,.2); background: rgb(28, 36, 34); box-shadow:0 0 28px rgba(30,229,170,.08); margin-bottom: 2rem; margin-top: 1rem; }
        .hero-section h2 { font:700 clamp(2.4rem,4vw,3.2rem) "Space Grotesk",sans-serif; color:#f4f7f4; margin:0; }
        .hero-subtitle { font:600 1.05rem "DM Mono",monospace; letter-spacing:.12em; text-transform:uppercase; color:var(--mint); margin:.35rem 0 .85rem; }
        .hero-copy { max-width:860px; font:400 1.02rem/1.7 "Space Grotesk",sans-serif; color:#dfe5e1; margin:0; }
        
        .feature-card { background:rgba(32,37,35,.82); border:1px solid rgba(30,229,170,.18); border-radius:1.25rem; padding:1.2rem 1.1rem; min-height:100%; margin-bottom: 1.5rem; }
        .feature-card h3 { color:#f4f7f4; font:600 1.1rem "Space Grotesk",sans-serif; margin-top:0; margin-bottom:.6rem; }
        .feature-card p { color:#dfe5e1; font:400 0.98rem/1.6 "Space Grotesk",sans-serif; margin:0; }
        
        /* Streamlit Tab Styling */
        .stTabs [data-baseweb="tab-list"] { gap: 2rem; }
        .stTabs [data-baseweb="tab"] { height: 3.5rem; white-space: pre-wrap; background-color: transparent; color: #b9c0bc; font-family: "Space Grotesk", sans-serif; font-size: 1.1rem; }
        .stTabs [aria-selected="true"] { color: var(--mint) !important; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Render Header & Navigation Menu ---
st.markdown(
    '''
    <div class="elli-brand">
        <h1>ELLI</h1>
        <p>Evolving<br>Large<br>Language<br>Intelligence</p>
    </div>
    ''', 
    unsafe_allow_html=True
)

nav_col1, nav_col2, _ = st.columns([1, 7, 6])
with nav_col1:
    st.page_link("webpage.py", label="Chat")
with nav_col2:
    st.page_link("pages/InfoPage.py", label="Info Center")

st.markdown(
    """
    <div class="hero-section">
        <p class="hero-copy">Project Overview</p>
        <h2>ELLI</h2>
        <p class="hero-subtitle">Evolving Language Learning Intelligence</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab2, tab3, tab4, tab5 = st.tabs([ "Stats for Nerds", "Creators", "Proposal", "Sources"])

# with tab1:
#     feature_cols = st.columns(3)
#     feature_items = [
#         ("Spontaneous Learning", "ELLI continuously fine-tunes itself. By reviewing historical chats and data inputs, it adapts its weights and memory spontaneously without requiring massive, separate training loops."),
#         ("Cognition & Introspection", "Operating on a dual-stage Transformer architecture, a separate, constantly-running thinking layer processes context and pushes optimized instructions directly to the output generation layer."),
#         ("Lightweight & Agile", "Built as a lean 300-million parameter model using bf16 format, ELLI can run its internal cognition loops around the clock while staying responsive and efficient."),
#     ]
#     for column, (title, body) in zip(feature_cols, feature_items):
#         with column:
#             st.markdown(f'<div class="feature-card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### ELLI’s thinking layer")
    st.info("Model WIP")

with tab3:
    st.markdown("### Team Eightfold | The Founders")
    st.markdown("""
        Team Members:

        * Kamesh Surapuraju

        * Roy Zhou

        * Edward Franco

        * Vikranth Maddali

        * Brian Suh
    """)
    readme_path = ROOT / "README2.md"
    if readme_path.exists():
        st.markdown(readme_path.read_text(encoding="utf-8"))

with tab4:
    st.markdown("### The Original Idea")
    st.markdown("The proposal of the original concept behind ELLI.")
    proposal = ROOT / "_Proposal of ELLI.pdf"
    if proposal.exists():
        pdf_data = base64.b64encode(proposal.read_bytes()).decode("utf-8")
        components.html(f'<iframe src="data:application/pdf;base64,{pdf_data}" width="100%" height="650" style="border:0;border-radius:12px;"></iframe>', height=665)
        st.download_button("Download the ELLI proposal (PDF)", proposal.read_bytes(), file_name=proposal.name, mime="application/pdf")
    else:
        st.warning(f"Proposal PDF not found at {proposal}")

with tab5:
    st.markdown("### Works Cited & Acknowledgements")
    st.markdown("The datasets, research, tools, and acknowledgements used for ELLI are listed below.")
    sources_path = ROOT / "SimplifiedSources.txt"
    if sources_path.exists():
        st.code(sources_path.read_text(encoding="utf-8"), language="bibtex")
    else:
        st.markdown("""
* **1. Datasets (via Hugging Face):** 

   
   * English Conversation:
	  
		https://huggingface.co/datasets/google/Synthetic-Persona-Chat
		
		https://huggingface.co/datasets/ParlAI/blended_skill_talk 
		
		https://huggingface.co/datasets/Organika/wizard_of_wikipedia
		
		https://huggingface.co/datasets/allenai/prosocial-dialog
		
		https://huggingface.co/datasets/allenai/soda
		
		https://huggingface.co/datasets/ianncity/GLM-5.2-Conversation

	
   * AI related:
		
		https://huggingface.co/datasets/databricks/databricks-dolly-15k
		
		https://huggingface.co/datasets/aps/super_glue
		
		https://huggingface.co/datasets/Salesforce/wikitext


   * Python:
		
		https://huggingface.co/datasets/sentence-transformers/codesearchnet
		
		https://huggingface.co/datasets/iamtarun/code_instructions_120k_alpaca
		
		https://huggingface.co/datasets/Glint-Research/Fable-5-traces
		
		https://huggingface.co/datasets/Muennighoff/mbpp
		
		https://huggingface.co/datasets/MoreThought/Fable-5-Max-Reasoning-Filtered 


   * Text generation: 
		
		https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf


   * Wiki:
		
		https://huggingface.co/datasets/allenai/sciq
		
		https://huggingface.co/datasets/allenai/openbookqa
		
		https://huggingface.co/datasets/allenai/qasc
		
		https://huggingface.co/datasets/allenai/ai2_arc
		
		https://huggingface.co/datasets/qiaojin/PubMedQA
		
		https://huggingface.co/datasets/hotpotqa/hotpot_qa
		
		https://huggingface.co/datasets/rajpurkar/squad_v2
		
		https://huggingface.co/datasets/google/boolq
		
		https://huggingface.co/datasets/ucinlp/drop
		
		https://huggingface.co/datasets/microsoft/wiki_qa
		
		https://huggingface.co/datasets/tau/commonsense_qa
		
		https://huggingface.co/datasets/ChilleD/StrategyQA/viewer/default/train?row=10
		
		https://huggingface.co/datasets/allenai/winogrande
		
		https://huggingface.co/datasets/Rowan/hellaswag
		
		https://huggingface.co/datasets/EleutherAI/race/viewer/high/test?row=0
		
		https://huggingface.co/datasets/ianncity/GLM-5.2-Science 
		
		https://huggingface.co/datasets/MuskumPillerum/General-Knowledge 


   * Math:
		
		https://huggingface.co/datasets/allenai/math_qa 
		
		https://huggingface.co/datasets/qwedsacf/competition_math
		
		https://huggingface.co/datasets/openai/gsm8k
		
		https://huggingface.co/datasets/cais/mmlu 


   * First Person:
		
		https://huggingface.co/datasets/agentlans/first-person-dialogue
		
		https://huggingface.co/datasets/openbmb/UltraFeedback


   * English literature:
		
		https://huggingface.co/datasets/ExponentialScience/DLT-Scientific-Literature
		
		http://huggingface.co/datasets/jimmyzxj/drosophila-literature-corpus
		
		https://huggingface.co/datasets/common-pile/pre_1929_books_filtered
		
		https://huggingface.co/datasets/schneewolflabs/hecke-dpo 
		
		https://huggingface.co/datasets/common-pile/project_gutenberg_filtered 


   * Humanizer : 
	
		https://huggingface.co/datasets/HuggingFaceH4/no_robots
		
		https://huggingface.co/datasets/openai/openai_humaneval

		
   * Logic : 
	  
		https://huggingface.co/datasets/PrimeIntellect/SYNTHETIC-2-SFT-verified
		
		
* **2. Websites & Research Frameworks**


	* https://streamlit.io/



* **3. AI Tools Used In This Project**


	* Eddie:
		* GitHub Copilot (for VS Code): Inline code completions and suggestions
		* Gemini: Research and learning how to build with Streamlit

	* Roy:
		* Gemini: Debugging
		* Codex: Setting up the coding environment and hardware issues
		* Claude: Aided with the building of the transformer architecture
	
        """
        )
st.sidebar.markdown(f"**Logged in as:**<br>{st.session_state.user_email}", unsafe_allow_html=True)


with st.sidebar.expander("Update Your Password", expanded=False):
    with st.form("change_password_form"):
        update_pass = st.text_input("New Password", type="password", key="update_pass_input")
        update_confirm = st.text_input("Confirm Password", type="password", key="update_confirm_input")
        update_submitted = st.form_submit_button("Update Password", key="update_submit_btn")
        
        if update_submitted:
            if update_pass != update_confirm:
                st.error("Passwords do not match.")
            elif len(update_pass) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                success, message = auth.update_password(update_pass)
                if success:
                    st.success(message)
                else:
                    st.error(message)

        if st.sidebar.button("Logout", key="logout_sidebar_btn"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            auth.supabase.auth.sign_out()
            st.rerun()

