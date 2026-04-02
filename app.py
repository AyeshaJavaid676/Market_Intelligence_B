import streamlit as st
import os
import time
import json
import zipfile
import io
from dotenv import load_dotenv
from backend.crew import market_crew
from backend.tools.semantic_cache import SemanticCache

load_dotenv()

st.set_page_config(
    page_title="AI Market Intelligence Bureau",
    page_icon="🧠",
    layout="wide"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .pipeline-step {
        text-align: center;
        padding: 15px;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 24px;
        transition: all 0.3s ease;
    }
    .step-active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 0 20px rgba(102,126,234,0.5);
        animation: pulse 1s infinite;
    }
    .step-complete {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    .step-pending {
        background: #e5e7eb;
        color: #9ca3af;
    }
    .step-arrow {
        font-size: 24px;
        color: #667eea;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .agent-card {
        text-align: center;
        padding: 15px;
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
        border-radius: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'cache_hits' not in st.session_state:
    st.session_state.cache_hits = 0
if 'cache_misses' not in st.session_state:
    st.session_state.cache_misses = 0
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {"Researcher": "pending", "Strategist": "pending", "Writer": "pending"}
if 'current_results' not in st.session_state:
    st.session_state.current_results = {'topic': None, 'research': None, 'strategy': None, 'content': None}
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# ==================== HELPER FUNCTIONS ====================
def render_pipeline():
    steps = [
        {"name": "🔍\nResearcher", "status": st.session_state.agent_status["Researcher"]},
        {"name": "🧠\nStrategist", "status": st.session_state.agent_status["Strategist"]},
        {"name": "✍️\nWriter", "status": st.session_state.agent_status["Writer"]}
    ]
    cols = st.columns([1, 0.2, 1, 0.2, 1])
    for i, step in enumerate(steps):
        col_idx = i * 2
        with cols[col_idx]:
            if step["status"] == "complete":
                cls, emoji = "step-complete", "✅"
            elif step["status"] == "active":
                cls, emoji = "step-active", "⚡"
            else:
                cls, emoji = "step-pending", "⏳"
            st.markdown(f"""
            <div style="text-align: center;">
                <div class="pipeline-step {cls}">{step["name"].split()[0]}</div>
                <p style="margin-top: 10px;">{step["name"]}</p>
                <p>{emoji} {step["status"].upper()}</p>
            </div>
            """, unsafe_allow_html=True)
        if i < len(steps) - 1:
            with cols[col_idx + 1]:
                st.markdown('<div class="step-arrow">→</div>', unsafe_allow_html=True)

def save_all_outputs(topic):
    results = {
        'topic': topic,
        'research': None,
        'strategy': None,
        'content': None
    }
    if os.path.exists("output/research.json"):
        with open("output/research.json", 'r') as f:
            results['research'] = f.read()
    if os.path.exists("output/strategy.md"):
        with open("output/strategy.md", 'r') as f:
            results['strategy'] = f.read()
    if os.path.exists("output/content.md"):
        with open("output/content.md", 'r') as f:
            results['content'] = f.read()
    st.session_state.current_results = results

def create_zip_report(topic):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in ["research.json", "strategy.md", "content.md"]:
            file_path = f"output/{file}"
            if os.path.exists(file_path):
                zip_file.write(file_path, file)
    return zip_buffer.getvalue()

# ==================== HEADER ====================
st.markdown('<div class="main-header">🧠 AI Market Intelligence Bureau</div>', unsafe_allow_html=True)
st.markdown("### Your AI Team: Researcher → Strategist → Writer")

# Agent Cards
st.markdown("### 🤖 Meet Your AI Team")
cols = st.columns(3)
agents = [
    ("🔍 Researcher", "Finds competitors & pricing"),
    ("🧠 Strategist", "Identifies market gaps"),
    ("✍️ Writer", "Creates SEO content")
]
for i, (name, desc) in enumerate(agents):
    with cols[i]:
        st.markdown(f'<div class="agent-card"><h3>{name}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ==================== PIPELINE (CREATED ONCE) ====================
pipeline_placeholder = st.empty()
with pipeline_placeholder.container():
    render_pipeline()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("📊 System Status")
    st.success("✅ All Agents Ready")
    st.info("🔍 Using Groq - 3 Agents")
    st.markdown("---")
    st.metric("Cache Hits", st.session_state.cache_hits)
    st.metric("Cache Misses", st.session_state.cache_misses)
    st.markdown("---")
    if st.session_state.current_results.get('topic'):
        st.success(f"✅ Current: {st.session_state.current_results['topic']}")
    status_placeholder = st.empty()

# ==================== MAIN INPUT ====================
topic = st.text_input("Enter topic:", placeholder="e.g., Electric scooters for adults")

# ==================== RUN BUTTON ====================
if st.button("🚀 Launch AI Team", type="primary", use_container_width=True):
    if not topic:
        st.error("Enter a topic")
    else:
        # Reset status
        st.session_state.agent_status = {"Researcher": "pending", "Strategist": "pending", "Writer": "pending"}
        st.session_state.is_running = True
        
        with pipeline_placeholder.container():
            render_pipeline()
        
        # Check cache
        cache = SemanticCache()
        cached = cache.get(topic)
        
        if cached:
            st.session_state.cache_hits += 1
            st.session_state.current_results = cached
            for a in st.session_state.agent_status:
                st.session_state.agent_status[a] = "complete"
            with pipeline_placeholder.container():
                render_pipeline()
            st.success("✅ Loaded from cache!")
            st.session_state.is_running = False
        else:
            st.session_state.cache_misses += 1
            
            # Clear old output files
            for f in ["research.json", "strategy.md", "content.md"]:
                if os.path.exists(f"output/{f}"):
                    os.remove(f"output/{f}")
            
            # STEP 1: Researcher ACTIVE (purple)
            st.session_state.agent_status["Researcher"] = "active"
            with pipeline_placeholder.container():
                render_pipeline()
            status_placeholder.info("🔍 Researcher: Searching...")
            
            # Run the crew (this runs all agents sequentially)
            try:
                result = market_crew.kickoff(inputs={"topic": topic})
                
                # After crew finishes, check files and update status one by one
                status_placeholder.info("📁 Processing outputs...")
                
                # Researcher complete
                if os.path.exists("output/research.json"):
                    st.session_state.agent_status["Researcher"] = "complete"
                    with pipeline_placeholder.container():
                        render_pipeline()
                    status_placeholder.success("✅ Researcher: Data saved")
                    time.sleep(0.5)
                
                # Strategist complete
                if os.path.exists("output/strategy.md"):
                    st.session_state.agent_status["Strategist"] = "complete"
                    with pipeline_placeholder.container():
                        render_pipeline()
                    status_placeholder.success("✅ Strategist: Analysis saved")
                    time.sleep(0.5)
                
                # Writer complete
                if os.path.exists("output/content.md"):
                    st.session_state.agent_status["Writer"] = "complete"
                    with pipeline_placeholder.container():
                        render_pipeline()
                    status_placeholder.success("✅ Writer: Content saved")
                
                # Save outputs
                save_all_outputs(topic)
                cache.set(topic, st.session_state.current_results)
                
                status_placeholder.success("✅ All complete!")
                st.success("✅ Analysis Complete!")
                
            except Exception as e:
                status_placeholder.error(f"Error: {str(e)[:200]}")
                st.error(f"Error: {e}")
            
            finally:
                st.session_state.is_running = False
                st.rerun()

# ==================== DISPLAY RESULTS ====================
if st.session_state.current_results.get('research'):
    st.markdown("---")
    st.header(f"📄 Report: {st.session_state.current_results['topic']}")
    tabs = st.tabs(["🔍 Research", "🧠 Strategy", "✍️ Content"])
    contents = [
        st.session_state.current_results.get('research'),
        st.session_state.current_results.get('strategy'),
        st.session_state.current_results.get('content')
    ]
    for i, (tab, content) in enumerate(zip(tabs, contents)):
        with tab:
            if content:
                try:
                    st.json(json.loads(content))
                except:
                    st.markdown(content)
    
    # Download ZIP option
    all_files_exist = all([os.path.exists(f"output/{f}") for f in ["research.json", "strategy.md", "content.md"]])
    if all_files_exist:
        zip_data = create_zip_report(st.session_state.current_results['topic'])
        st.download_button(
            label="📦 Download All Files (ZIP)",
            data=zip_data,
            file_name=f"{st.session_state.current_results['topic'].replace(' ', '_')}_report.zip",
            use_container_width=True
        )

st.markdown("---")
st.caption("Built with CrewAI + Groq | 3-Agent System")