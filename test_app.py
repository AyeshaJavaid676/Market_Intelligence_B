import streamlit as st
import time
import json
import os
from dotenv import load_dotenv
from crewai_tools import TavilySearchTool

load_dotenv()

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Pipeline Test - Real Tavily Search",
    page_icon="🔍",
    layout="wide"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .pipeline-step {
        text-align: center;
        padding: 15px;
        border-radius: 50%;
        width: 100px;
        height: 100px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 28px;
        transition: all 0.3s ease;
    }
    .step-active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 0 20px rgba(102,126,234,0.5);
        transform: scale(1.05);
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
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
    .search-result {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        font-size: 13px;
    }
    .search-result a {
        color: #667eea;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {
        "Researcher": "pending",
        "Strategist": "pending",
        "Writer": "pending"
    }
if 'results' not in st.session_state:
    st.session_state.results = {
        'research': None,
        'strategy': None,
        'content': None
    }
if 'search_results' not in st.session_state:
    st.session_state.search_results = None

# ==================== TAVILY SETUP ====================
# Initialize Tavily tool
tavily_tool = TavilySearchTool(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)

# ==================== REAL FUNCTIONS WITH TAVILY ====================
def researcher_with_tavily(topic):
    """Real researcher using Tavily search"""
    st.session_state.execution_status = f"🔍 Searching Tavily for: {topic}"
    
    try:
        # Real Tavily search
        result = tavily_tool._run(query=topic)
        
        # Parse the result (it returns a JSON string)
        if isinstance(result, str):
            try:
                search_data = json.loads(result)
            except:
                search_data = {"raw": result}
        else:
            search_data = result
        
        # Extract competitor information
        competitors = []
        if "results" in search_data:
            for item in search_data["results"][:3]:
                competitors.append({
                    "name": item.get("title", "Unknown")[:50],
                    "url": item.get("url", ""),
                    "description": item.get("content", "")[:150]
                })
        
        return {
            "topic": topic,
            "competitors": competitors,
            "sources": search_data.get("results", [])[:3],
            "total_results": len(search_data.get("results", []))
        }
        
    except Exception as e:
        return {"error": str(e), "topic": topic}

def strategist_from_research(research_data):
    """Strategist analyzing research results"""
    st.session_state.execution_status = "🧠 Analyzing market gaps from research..."
    time.sleep(1.5)  # Simulate analysis time
    
    if "error" in research_data:
        return {"error": research_data["error"]}
    
    competitors = research_data.get("competitors", [])
    competitor_names = [c.get("name", "") for c in competitors if c.get("name")]
    
    return {
        "competitors_found": competitor_names,
        "market_gaps": ["Limited organic options", "High price points", "Limited flavors"],
        "opportunities": ["Affordable line", "New flavor innovation"],
        "analysis": f"Found {len(competitors)} competitors in the {research_data.get('topic', '')} market"
    }

def writer_from_strategy(strategy_data):
    """Writer creating content from strategy"""
    st.session_state.execution_status = "✍️ Creating content strategy..."
    time.sleep(1.5)
    
    if "error" in strategy_data:
        return {"error": strategy_data["error"]}
    
    competitors = strategy_data.get("competitors_found", [])
    comp_text = ", ".join(competitors[:3]) if competitors else "multiple brands"
    
    return {
        "blog_ideas": [
            f"Top {len(competitors)} Competitors in Plant-Based Snacks: {comp_text}",
            "Why Consumers Are Switching to Plant-Based Protein",
            "The Future of Healthy Snacking"
        ],
        "social_posts": [
            f"Discover the best plant-based snacks! 🌱 Check out {comp_text}",
            "Fuel your day with clean protein 💪",
            "What's your favorite protein bar? Share below!"
        ],
        "summary": f"Content strategy focused on {len(competitors)} competitors including {comp_text}"
    }

# ==================== RENDER PIPELINE ====================
def render_pipeline():
    """Render the pipeline visualization - updates the SAME pipeline"""
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
                status_class = "step-complete"
                status_emoji = "✅"
            elif step["status"] == "active":
                status_class = "step-active"
                status_emoji = "⚡"
            else:
                status_class = "step-pending"
                status_emoji = "⏳"
            
            st.markdown(f"""
            <div style="text-align: center;">
                <div class="pipeline-step {status_class}">
                    {step["name"].split()[0]}
                </div>
                <p style="margin-top: 10px; font-weight: bold;">{step["name"]}</p>
                <p style="font-size: 11px;">{status_emoji} {step["status"].upper()}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if i < len(steps) - 1:
            with cols[col_idx + 1]:
                st.markdown('<div class="step-arrow">→</div>', unsafe_allow_html=True)

# ==================== MAIN UI ====================
st.title("🔍 Pipeline Test - Real Tavily Search")
st.markdown("**The pipeline updates based on ACTUAL Tavily API search results**")
st.markdown("---")

# Pipeline placeholder (ONCE)
pipeline_placeholder = st.empty()

# Initial pipeline render
with pipeline_placeholder.container():
    render_pipeline()

# Input
topic = st.text_input("Enter topic to search:", placeholder="e.g., plant-based protein snacks", value="plant-based protein snacks")

# Status display
status_placeholder = st.empty()

# Run Button
if st.button("🚀 Launch Agents with Tavily Search", type="primary", use_container_width=True):
    # Reset status
    st.session_state.agent_status = {
        "Researcher": "pending",
        "Strategist": "pending",
        "Writer": "pending"
    }
    st.session_state.results = {'research': None, 'strategy': None, 'content': None}
    st.session_state.search_results = None
    
    # Update pipeline to pending
    with pipeline_placeholder.container():
        render_pipeline()
    
    # ========== AGENT 1: RESEARCHER (REAL TAVILY SEARCH) ==========
    st.session_state.agent_status["Researcher"] = "active"
    with pipeline_placeholder.container():
        render_pipeline()
    status_placeholder.info(f"🔍 Searching Tavily for: {topic}...")
    
    # ✅ REAL TAVILY SEARCH - waits for actual API response
    research_result = researcher_with_tavily(topic)
    
    # Update pipeline to complete
    st.session_state.agent_status["Researcher"] = "complete"
    st.session_state.results['research'] = research_result
    st.session_state.search_results = research_result
    with pipeline_placeholder.container():
        render_pipeline()
    
    if "error" in research_result:
        status_placeholder.error(f"❌ Researcher error: {research_result['error']}")
    else:
        status_placeholder.success(f"✅ Researcher completed! Found {research_result.get('total_results', 0)} results")
    
    # ========== AGENT 2: STRATEGIST ==========
    st.session_state.agent_status["Strategist"] = "active"
    with pipeline_placeholder.container():
        render_pipeline()
    status_placeholder.info("🧠 Strategist: Analyzing market gaps...")
    
    strategy_result = strategist_from_research(st.session_state.results['research'])
    
    st.session_state.agent_status["Strategist"] = "complete"
    st.session_state.results['strategy'] = strategy_result
    with pipeline_placeholder.container():
        render_pipeline()
    status_placeholder.success("✅ Strategist completed!")
    
    # ========== AGENT 3: WRITER ==========
    st.session_state.agent_status["Writer"] = "active"
    with pipeline_placeholder.container():
        render_pipeline()
    status_placeholder.info("✍️ Writer: Creating content strategy...")
    
    content_result = writer_from_strategy(st.session_state.results['strategy'])
    
    st.session_state.agent_status["Writer"] = "complete"
    st.session_state.results['content'] = content_result
    with pipeline_placeholder.container():
        render_pipeline()
    status_placeholder.success("✅ Writer completed!")
    
    # Final
    status_placeholder.success("🎉 All agents completed successfully!")
    st.balloons()

# ==================== DISPLAY REAL SEARCH RESULTS ====================
if st.session_state.search_results:
    st.markdown("---")
    st.subheader(f"🔍 Real Tavily Search Results for: {st.session_state.search_results.get('topic', '')}")
    
    if "error" in st.session_state.search_results:
        st.error(f"Search error: {st.session_state.search_results['error']}")
    else:
        competitors = st.session_state.search_results.get('competitors', [])
        
        if competitors:
            st.markdown(f"**Found {len(competitors)} competitors:**")
            for i, comp in enumerate(competitors, 1):
                with st.expander(f"{i}. {comp.get('name', 'Unknown')}"):
                    if comp.get('url'):
                        st.markdown(f"🔗 [{comp.get('url')}]({comp.get('url')})")
                    if comp.get('description'):
                        st.markdown(f"📝 {comp.get('description')}")
        else:
            st.info("No competitor data extracted. Check Tavily API key and try a different topic.")

# ==================== DISPLAY AGENT RESULTS ====================
if st.session_state.results['research'] and "error" not in st.session_state.results['research']:
    st.markdown("---")
    st.subheader("📊 Agent Outputs")
    
    tab1, tab2, tab3 = st.tabs(["🔍 Researcher", "🧠 Strategist", "✍️ Writer"])
    
    with tab1:
        st.json(st.session_state.results['research'])
    
    with tab2:
        st.json(st.session_state.results['strategy'])
    
    with tab3:
        st.json(st.session_state.results['content'])

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d;">
    <p>✅ Pipeline updates based on ACTUAL Tavily API search results</p>
    <p>🔍 Researcher → 🧠 Strategist → ✍️ Writer (status changes in place)</p>
    <p>📊 Real competitor data from Tavily search</p>
</div>
""", unsafe_allow_html=True)