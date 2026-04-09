import streamlit as st
import os
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
import sys

# Must be first Streamlit call
st.set_page_config(
    page_title="ROYALLE SOURCE | Mission Control",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Path Setup ---
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import POSTS_DIR, BASE_DIR, POSTING_TIMES, PROFILES, save_profiles
from state_manager import StateManager
from intelligence import IntelligenceScanner
from researcher import ContentResearcher
from viral_frameworks import VIRAL_FRAMEWORKS
from main import run_production

sm = StateManager()
scanner = IntelligenceScanner()
researcher = ContentResearcher()

# ═══════════════════════════════════════════════════════════════
#  SESSION STATE INITIALIZATION (Fixes Button Lag)
# ═══════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════
#  SESSION STATE INITIALIZATION (Fixes Button Lag)
# ═══════════════════════════════════════════════════════════════
if 'action_log' not in st.session_state:
    st.session_state.action_log = []
if 'refresh_trigger' not in st.session_state:
    st.session_state.refresh_trigger = 0
if 'draft_script' not in st.session_state:
    st.session_state.draft_script = None
if 'production_queue' not in st.session_state:
    st.session_state.production_queue = []
if 'draft_meta' not in st.session_state:
    st.session_state.draft_meta = None

def trigger_action(msg):
    sm.update_step(msg, progress=10)
    st.session_state.action_log.insert(0, f"[{datetime.now().strftime('%H:%M')}] {msg}")
    st.session_state.refresh_trigger += 1

# ═══════════════════════════════════════════════════════════════
#  EXECUTIVE UI STYLING (High Contrast / Premium)
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap');

    /* === MISSION CONTROL THEME === */
    [data-testid="stAppViewContainer"] {
        background-color: #05070a;
        background-image: 
            radial-gradient(at 0% 0%, rgba(255, 215, 0, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(0, 100, 255, 0.05) 0px, transparent 50%);
        color: #ffffff;
        font-family: 'Outfit', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0a0d14;
        border-right: 1px solid rgba(255, 215, 0, 0.2);
    }

    /* === HEADER SCULPTING === */
    .brand-header {
        text-align: center;
        padding: 40px 0 20px 0;
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 215, 0, 0.1);
        margin-bottom: 30px;
    }
    .brand-header h1 {
        font-weight: 900;
        font-size: 3.2rem;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .brand-header p {
        color: #FFD700;
        letter-spacing: 5px;
        font-size: 0.8rem;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* === PREMIUM COMMAND CARDS === */
    .command-card {
        background: rgba(15, 20, 30, 0.8);
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 15px;
    }
    .command-card:hover {
        border-color: #FFD700;
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.1);
    }
    .metric-label {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 900;
        line-height: 1;
    }
    .vibrant-gold { color: #FFD700; text-shadow: 0 0 20px rgba(255, 215, 0, 0.3); }
    .vibrant-blue { color: #00A3FF; text-shadow: 0 0 20px rgba(0, 163, 255, 0.3); }
    .vibrant-green { color: #00F0FF; text-shadow: 0 0 20px rgba(0, 240, 255, 0.3); }

    /* === TACTILE BUTTONS === */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0.05)) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        color: #FFD700 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 15px !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        background: #FFD700 !important;
        color: #000000 !important;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.4) !important;
    }

    /* === STATUS INDICATORS === */
    .glow-dot {
        height: 12px; width: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        box-shadow: 0 0 15px currentColor;
    }

    /* HIDE STREAMLIT JUNK */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* === INLINE GREETING (SAFE) === */
    .inline-salute {
        text-align: center;
        padding: 20px;
        background: rgba(15, 20, 30, 0.8);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .inline-salute img {
        width: 150px;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }
    .greeting-text {
        color: #FFD700;
        font-weight: 900;
        font-size: 1.5rem;
        letter-spacing: 3px;
        margin-top: 10px;
        text-transform: uppercase;
        animation: pulse 2s infinite;
    }

    @keyframes pulse { 0% {opacity: 0.5;} 50% {opacity: 1;} 100% {opacity: 0.5;} }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def load_performance_data():
    times = pd.date_range(end=datetime.now(), periods=24, freq='h')
    data = pd.DataFrame({
        'Time': times,
        'Beauty': np.random.randint(40, 95, 24),
        'Women Health': np.random.randint(30, 88, 24)
    })
    return data

@st.cache_data(ttl=60)
def get_video_stats():
    if not os.path.exists(POSTS_DIR): return []
    videos = [f for f in os.listdir(POSTS_DIR) if f.endswith('.mp4')]
    return sorted(videos, key=lambda x: os.path.getmtime(os.path.join(POSTS_DIR, x)), reverse=True)

# ═══════════════════════════════════════════════════════════════
#  SIDEBAR (EXEC)
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("static/icon.png", width=80)
    st.markdown("### 🌐 CHANNEL MANAGER")
    
    for name, p_data in PROFILES.items():
        st.checkbox(name, value=p_data.get("active", True), key=f"prof_{name}")
        
    with st.expander("🔗 SOCIAL DESTINATIONS"):
        st.markdown("Set your target post URLs below:")
        updated_profiles = {}
        changes_made = False
        for name, p_data in PROFILES.items():
            new_url = st.text_input(f"{name} Destination URL", value=p_data.get("destination_url", ""), placeholder="https://instagram.com/...")
            updated_profiles[name] = p_data.copy()
            if new_url != p_data.get("destination_url", ""):
                updated_profiles[name]["destination_url"] = new_url
                changes_made = True
        
        if st.button("💾 Save Destinations"):
            if changes_made:
                save_profiles(updated_profiles)
                st.success("Destinations locked.")
            else:
                st.info("No changes to save.")
    
    st.markdown("---")
    st.markdown("### 🏹 UNIVERSAL COMMAND")
    target_niche = st.text_input("Enter Niche/Topic", placeholder="e.g. SaaS for Builders")
    target_goal = st.selectbox("Campaign Goal", ["sales", "engagement", "ugc", "viral"])
    target_strategy = st.selectbox("Viral Strategy", list(VIRAL_FRAMEWORKS.keys()))
    
    if st.button("🚀 RESEARCH & DRAFT"):
        if target_niche:
            trigger_action(f"Researching {target_goal} ad for {target_niche}")
            script = researcher.generate_viral_script(target_niche, target_goal, target_strategy)
            if script:
                st.session_state.draft_script = script
                st.session_state.draft_meta = {"niche": target_niche, "goal": target_goal, "strategy": target_strategy}
                st.rerun()
        else:
            st.warning("General, please specify the mission objective (Niche).")

    st.markdown("---")
    st.markdown("### 🧠 INTELLIGENCE HUB")
    target_url = st.text_input("Source URL to Scan", placeholder="https://site.com/article")
    if st.button("📡 SCAN & DRAFT"):
        if target_url:
            trigger_action(f"Scanning Intelligence: {target_url}")
            raw_text = scanner.scan_url(target_url)
            if raw_text:
                script = researcher.generate_from_url(raw_text)
                if script:
                    st.session_state.draft_script = script
                    st.session_state.draft_meta = {"niche": "Intelligence URL", "goal": "sales"}
                    st.rerun()
        else:
            st.warning("Intelligence URL required.")

    st.markdown("---")
    if st.button("🔄 REFRESH COMMAND"):
        st.rerun()

# ═══════════════════════════════════════════════════════════════
#  MISSION CONTROL HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="brand-header">
    <h1>ROYALLE SOURCE</h1>
    <p>AI CONTENT EVOLUTION SYSTEM</p>
</div>

<!-- INLINE GREETING -->
<div class="inline-salute">
    <img src="app/static/soldier_salute.png" alt="Salute">
    <div class="greeting-text">READY FOR COMMAND, GENERAL HENDRICKS</div>
</div>

<!-- AUDIO AUTOPLAY (HACK) -->
<audio autoplay>
    <source src="app/static/greeting.mp3" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  CORE METRICS & COMMAND CARDS
# ═══════════════════════════════════════════════════════════════
state = sm.load_state()

tab_mission, tab_drafts, tab_queue = st.tabs(["🚀 MISSION CONTROL", "📝 DRAFT EDITOR", "🎬 PRODUCTION QUEUE"])

with tab_mission:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        status = state.get("last_step", "STANDBY")
        st.markdown(f"""
        <div class="command-card">
            <div class="metric-label">System Mode</div>
            <div class="metric-value vibrant-gold">
                <span class="glow-dot" style="color:#FFD700; background:#FFD700;"></span>
                {status[:10].upper()}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="command-card">
            <div class="metric-label">Active Focus</div>
            <div class="metric-value vibrant-blue">UNIVERSAL</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="command-card">
            <div class="metric-label">Queue Status</div>
            <div class="metric-value vibrant-green">{len(st.session_state.production_queue)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="command-card">
            <div class="metric-label">Viral Reach</div>
            <div class="metric-value vibrant-gold">124K</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    main_left, main_right = st.columns([2, 1])

    with main_left:
        st.markdown("### 📈 VIRAL MOMENTUM FORCAST")
        df = load_performance_data()
        st.area_chart(df.set_index('Time'), color=["#FFD700", "#00A3FF"])
        
        st.markdown("### 📺 RECENT CONTENT PIPELINE")
        recent = get_video_stats()
        if recent:
            st.video(os.path.join(POSTS_DIR, recent[0]))
        else:
            st.info("No content in pipeline yet. Generate a script!")

    with main_right:
        st.markdown("### 🛡️ MISSION LOG")
        if st.session_state.action_log:
            for log in st.session_state.action_log[:8]:
                st.markdown(f"""
                <div style="background:rgba(255,215,0,0.05); border-left:2px solid #FFD700; padding:10px; margin-bottom:5px; font-size:0.85rem; color:#fff;">
                    {log}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Awaiting initial command...")

        st.markdown("<br>### 🎯 OPTIMAL WINDOWS")
        for t in POSTING_TIMES:
            st.markdown(f"""
            <div style="padding:10px; border:1px solid rgba(255,215,0,0.1); border-radius:10px; margin-bottom:5px; text-align:center; background:rgba(255,215,0,0.02);">
                <span style="color:#FFD700; font-weight:800;">{t} SAST</span> — HIGH PROBABILITY
            </div>
            """, unsafe_allow_html=True)

with tab_drafts:
    st.markdown("### 📝 SCRIPT EDITOR")
    if st.session_state.draft_script:
        draft = st.session_state.draft_script
        st.markdown(f"**Current Draft:** `{draft.get('title', 'Unknown')}`")
        
        updated_hook = st.text_area("1. THE HOOK (Scroll Stopper):", value=draft.get('hook', ''), height=80)
        updated_problem = st.text_area("2. THE PROBLEM:", value=draft.get('problem', ''), height=100)
        updated_insight = st.text_area("3. THE INSIGHT (Wisdom):", value=draft.get('insight', ''), height=100)
        updated_payoff = st.text_area("4. THE PAYOFF:", value=draft.get('payoff', ''), height=100)
        updated_cta = st.text_input("5. CALL TO ACTION:", value=draft.get('cta', ''))
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🟢 APPROVE & QUEUE", use_container_width=True):
                approved_script = {
                    "title": draft.get('title', 'Manual Edit'),
                    "hook": updated_hook,
                    "problem": updated_problem,
                    "insight": updated_insight,
                    "payoff": updated_payoff,
                    "cta": updated_cta,
                    "mood_keywords": draft.get('mood_keywords', ["cinematic"]),
                    "strategy_used": draft.get('strategy_used', 'custom')
                }
                
                # Bundle script with meta
                queue_item = {"script": approved_script, "meta": st.session_state.draft_meta}
                st.session_state.production_queue.append(queue_item)
                st.session_state.draft_script = None # Clear draft
                trigger_action("Draft Approved and Queued.")
                st.success("Added to Production Queue!")
                st.rerun()

        with c2:
            if st.button("🔴 CANCEL DRAFT", use_container_width=True):
                st.session_state.draft_script = None
                trigger_action("Draft Cancelled.")
                st.rerun()

    else:
        st.info("No active drafts. Initiate a mission from the sidebar.")

with tab_queue:
    st.markdown("### 🎬 BATCH PRODUCTION QUEUE")
    if not st.session_state.production_queue:
        st.info("The command queue is currently empty. General, standing by.")
    else:
        for i, item in enumerate(st.session_state.production_queue):
            script = item["script"]
            meta = item["meta"]
            st.markdown(f"""
            <div style="border: 1px solid rgba(255, 215, 0, 0.3); padding: 15px; border-radius: 10px; margin-bottom: 15px; background: rgba(0,0,0,0.3);">
                <h4 style="color: #FFD700; margin:0;">Target: {meta.get('niche', 'Unknown').upper()}</h4>
                <p style="color: #00A3FF; font-size: 0.8rem; margin:0; margin-bottom: 10px;">Goal: {meta.get('goal', 'N/A').upper()}</p>
                <i>"{script.get('hook', '')}"</i>
            </div>
            """, unsafe_allow_html=True)
            
        if st.button("🔥 RENDER ALL VIDEOS IN QUEUE", type="primary", use_container_width=True):
            for idx, task in enumerate(st.session_state.production_queue):
                trigger_action(f"Rendering Batch Item {idx+1}/{len(st.session_state.production_queue)}...")
                
                # Use the imported run_production
                script = task["script"]
                meta = task["meta"]
                
                try:
                    run_production(
                        niche=meta.get("niche", "general"),
                        goal=meta.get("goal", "engagement"),
                        strategy=meta.get("strategy", "custom"),
                        is_dry_run=False,
                        override_script=script
                    )
                except Exception as e:
                    st.error(f"Error rendering item {idx+1}: {e}")
                    
            st.session_state.production_queue = []
            trigger_action("Batch Deployment Complete!")
            st.success("All videos generated successfully!")
            st.rerun()


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; opacity: 0.5; font-size: 0.7rem; letter-spacing: 3px;">
    ROYALLE SOURCE EXECUTIVE • AI EVOLUTION SYSTEM v2.0
</div>
""", unsafe_allow_html=True)
