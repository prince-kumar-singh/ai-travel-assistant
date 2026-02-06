import streamlit as st
import json
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent

# Page config
st.set_page_config(
    page_title="AI Smart Travel Ops Assistant",
    page_icon="✈️",
    layout="wide"
)

# Title
st.title("✈️ AI Smart Travel Ops Assistant")
st.markdown("Get real-time travel safety recommendations powered by AI")

# Initialize agents (cached to avoid recreating on every run)
@st.cache_resource
def get_agents():
    return PlannerAgent(), ExecutorAgent(), VerifierAgent()

planner, executor, verifier = get_agents()

# Input section
st.markdown("### 🔍 Ask Your Travel Safety Question")
query = st.text_input(
    "Enter your query",
    placeholder="e.g., Is it safe to travel to Mumbai tomorrow?",
    label_visibility="collapsed"
)

# Process button
if st.button("🚀 Get Recommendation", type="primary"):
    if not query:
        st.warning("⚠️ Please enter a query first!")
    else:
        with st.spinner("🧠 AI is analyzing your query..."):
            # Step 1: Planning
            st.info("**Step 1/3:** 🧠 Planner Agent analyzing query...")
            plan = planner.plan(query)
            
            if "error" in plan:
                st.error(f"❌ Planning failed: {plan['error']}")
            else:
                st.success("✅ Plan generated successfully!")
                with st.expander("📋 View Generated Plan"):
                    st.json(plan)
                
                # Step 2: Execution
                st.info("**Step 2/3:** ⚙️ Executor Agent running tools...")
                tool_results = executor.execute_plan(plan)
                st.success("✅ Tools executed successfully!")
                with st.expander("🔧 View Tool Results"):
                    st.json(tool_results)
                
                # Step 3: Verification
                st.info("**Step 3/3:** ✅ Verifier Agent formatting results...")
                final_result = verifier.verify_and_respond(tool_results)
                st.success("✅ Recommendation ready!")
                
                # Display final result
                st.markdown("---")
                st.markdown("### 📊 Final Recommendation")
                
                # Pretty display of result
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("🌍 Destination", final_result.get("destination", "N/A"))
                    st.metric("📅 Date", final_result.get("date", "N/A"))
                    st.metric("🎯 Travel Score", f"{final_result.get('travel_score', 0)}/10")
                
                with col2:
                    weather = final_result.get("weather", {})
                    if weather:
                        st.metric("🌡️ Temperature", f"{weather.get('temperature', 'N/A')}°C")
                        st.info(f"☁️ {weather.get('condition', 'N/A')}")
                
                # Alerts
                alerts = final_result.get("alerts", [])
                # Ensure alerts is a list (not a string being iterated char-by-char)
                if isinstance(alerts, str):
                    alerts = [alerts] if alerts else []
                
                if alerts:
                    st.markdown("#### ⚠️ Important Alerts")
                    for alert in alerts:
                        st.warning(alert)
                
                # Recommendation
                st.markdown("#### 💡 Recommendation")
                st.success(final_result.get("recommendation", "No recommendation available"))
                
                # JSON output
                with st.expander("📄 Raw JSON Output"):
                    st.json(final_result)

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.markdown("""
    This AI-powered assistant helps you make informed travel decisions by:
    - 🌤️ Fetching real-time weather data
    - 📰 Analyzing latest news and alerts
    - 🤖 Using AI to provide safety recommendations
    """)
    
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
    - **LLM**: Groq (Llama 3.3 70B)
    - **Weather API**: OpenWeatherMap
    - **News API**: NewsData.io
    - **Framework**: Streamlit
    """)
    
    st.markdown("### 📝 Example Queries")
    st.code("Is it safe to travel to Paris next week?")
    st.code("Weather conditions in Tokyo tomorrow?")
    st.code("Travel safety to Mumbai from Delhi?")
