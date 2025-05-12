import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
from PIL import Image
import io
import base64

from utils.data_generator import (
    generate_category_health_data, 
    generate_supplier_data,
    generate_spend_data,
    generate_risk_data
)
from utils.scraper import simulated_web_scrape

# Configure page
st.set_page_config(
    page_title="Category Intelligence - Procurement Command Center",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS for professional look and feel
st.markdown("""
    <style>
    /* Main styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3B82F6;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1F2937;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Card styling */
    .metric-container {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s, box-shadow 0.2s;
        border-top: 4px solid #3B82F6;
    }
    .metric-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Insight card styling */
    .insight-card {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #3B82F6;
    }
    .insight-card.risk {
        border-left: 5px solid #EF4444;
    }
    .insight-card.opportunity {
        border-left: 5px solid #10B981;
    }
    .insight-card.alert {
        border-left: 5px solid #F59E0B;
    }
    .insight-card h4 {
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1F2937;
    }
    
    /* News item styling */
    .news-item {
        padding: 16px;
        margin-bottom: 16px;
        border-left: 5px solid #3B82F6;
        background-color: white;
        border-radius: 0 0.5rem 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .news-item.high-impact {
        border-left: 5px solid #EF4444;
    }
    .news-item.neutral {
        border-left: 5px solid #9CA3AF;
    }
    .news-item .news-title {
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 4px;
    }
    .news-item .news-date {
        font-size: 0.8rem;
        color: #6B7280;
        margin-bottom: 8px;
    }
    
    /* KPI indicator styling */
    .kpi-indicator {
        display: flex;
        align-items: center;
        margin-top: 8px;
    }
    .kpi-indicator .indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .kpi-indicator .good {
        background-color: #10B981;
    }
    .kpi-indicator .warning {
        background-color: #F59E0B;
    }
    .kpi-indicator .critical {
        background-color: #EF4444;
    }
    .kpi-indicator .text {
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Journey steps */
    .journey-container {
        display: flex;
        margin: 2rem 0;
        position: relative;
    }
    .journey-container:before {
        content: '';
        position: absolute;
        top: 20px;
        left: 0;
        right: 0;
        height: 4px;
        background: #E5E7EB;
        z-index: 1;
    }
    .journey-step {
        flex: 1;
        text-align: center;
        padding: 0 10px;
        position: relative;
        z-index: 2;
    }
    .journey-step .step-dot {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #3B82F6;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px;
        font-weight: bold;
        box-shadow: 0 0 0 4px white;
    }
    .journey-step .step-dot.active {
        background: #1E3A8A;
        transform: scale(1.2);
    }
    .journey-step .step-dot.completed {
        background: #10B981;
    }
    .journey-step .step-text {
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Buttons styling */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border-radius: 0.375rem;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
    
    /* Custom plot styling */
    .js-plotly-plot .plotly .modebar {
        margin-top: 8px !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6;
        color: white;
    }
    
    /* Action button styles */
    .action-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8px 16px;
        background-color: #3B82F6;
        color: white;
        border-radius: 4px;
        margin-right: 8px;
        font-weight: 500;
        text-decoration: none;
        transition: background-color 0.2s;
    }
    .action-button:hover {
        background-color: #2563EB;
    }
    .action-button.secondary {
        background-color: #9CA3AF;
    }
    .action-button.secondary:hover {
        background-color: #6B7280;
    }
    
    /* Dashboard summary section */
    .dashboard-summary {
        margin: 1.5rem 0;
        padding: 1rem;
        background-color: #F9FAFB;
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
    }
    
    /* Recommendation card */
    .recommendation-card {
        background-color: #EFF6FF;
        border-radius: 0.5rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
    }
    .recommendation-card.urgent {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
    }
    .recommendation-card.opportunity {
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
    }
    
    /* Select box styling */
    div[data-baseweb="select"] {
        border-radius: 0.375rem;
    }
    div[data-baseweb="select"] > div {
        background-color: white;
        border-color: #D1D5DB;
        border-radius: 0.375rem;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for engagement tracking
if 'visited_tabs' not in st.session_state:
    st.session_state.visited_tabs = set()
if 'insights_viewed' not in st.session_state:
    st.session_state.insights_viewed = 0
if 'current_story_step' not in st.session_state:
    st.session_state.current_story_step = 1
if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False
if 'category_goal_set' not in st.session_state:
    st.session_state.category_goal_set = False
if 'goals' not in st.session_state:
    st.session_state.goals = {}

# Demo data for Aviation category
aviation_suppliers = {
    "Boeing": {"spend": 32500000, "risk": "Medium", "performance": 87, "contract_end": "2025-09-30"},
    "Airbus": {"spend": 28700000, "risk": "Low", "performance": 92, "contract_end": "2026-03-15"},
    "GE Aviation": {"spend": 18900000, "risk": "Low", "performance": 89, "contract_end": "2025-12-10"},
    "Rolls-Royce": {"spend": 15600000, "risk": "Medium", "performance": 84, "contract_end": "2024-11-20"},
    "Safran": {"spend": 12300000, "risk": "Low", "performance": 90, "contract_end": "2025-06-30"},
    "Honeywell Aerospace": {"spend": 9800000, "risk": "Low", "performance": 88, "contract_end": "2024-08-15"},
    "Pratt & Whitney": {"spend": 8700000, "risk": "Medium", "performance": 85, "contract_end": "2026-01-22"},
    "Collins Aerospace": {"spend": 7500000, "risk": "Low", "performance": 91, "contract_end": "2025-05-18"},
    "Raytheon Technologies": {"spend": 6800000, "risk": "Medium", "performance": 86, "contract_end": "2024-12-05"},
    "Thales Group": {"spend": 5400000, "risk": "Medium", "performance": 83, "contract_end": "2025-10-12"}
}

# Sidebar
with st.sidebar:
    st.markdown("# 📊 Category Intelligence")
    st.markdown("---")
    
    # Category selector with Aviation featured
    categories = ["Aviation", "Electronics", "Raw Materials", "Packaging", "Office Supplies", 
                 "IT Services", "Logistics", "Chemicals", "Machinery"]
    selected_category = st.selectbox("Select Category", categories, index=0)
    
    st.markdown("---")
    
    # Time period filter
    time_period = st.select_slider(
        "Analysis Period",
        options=["Last Month", "Last Quarter", "Last 6 Months", "Last Year", "Next 6 Months"],
        value="Last Quarter"
    )
    
    # Region filter
    regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Global"]
    selected_region = st.multiselect("Region", regions, default=["Global"])
    
    # Category Intelligence Journey
    st.markdown("---")
    st.markdown("### Category Intelligence Journey")
    
    # Progress tracker - simplified to match our 3-tab structure
    progress_options = ["Overview", "Insights", "Action Plan"]
    current_step = progress_options[st.session_state.current_story_step - 1]
    
    # Display journey progress
    st.markdown(
        f"""
        <div class="journey-container">
            <div class="journey-step">
                <div class="step-dot {"completed" if st.session_state.current_story_step > 1 else "active" if st.session_state.current_story_step == 1 else ""}">1</div>
                <div class="step-text">Overview</div>
            </div>
            <div class="journey-step">
                <div class="step-dot {"completed" if st.session_state.current_story_step > 2 else "active" if st.session_state.current_story_step == 2 else ""}">2</div>
                <div class="step-text">Insights</div>
            </div>
            <div class="journey-step">
                <div class="step-dot {"active" if st.session_state.current_story_step == 3 else ""}">3</div>
                <div class="step-text">Action Plan</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(f"**Current Step:** {current_step}")
    
    # Quick actions
    st.markdown("---")
    st.markdown("### Quick Actions")
    
    if st.button("Export Intelligence Report", use_container_width=True):
        st.markdown("Generating comprehensive report...")
        st.success("✅ Report ready! Download started.")
    
    if st.button("Share Insights", use_container_width=True):
        st.info("✉️ Insights sharing options opened.")
    
    if st.button("Schedule Category Review", use_container_width=True):
        st.success("📅 Category review meeting scheduled.")

# Main Content Header
st.markdown(
    f"""
    <div class="main-header">
        {selected_category} Category Intelligence Center
    </div>
    """, 
    unsafe_allow_html=True
)

# Executive summary
exec_summary = f"""
This interactive dashboard provides a holistic view of the {selected_category} category, helping you make 
data-driven decisions about suppliers, costs, risks, and market opportunities. Navigate through the tabs 
to discover insights, analyze data patterns, develop strategies, and take action.
"""

# Key challenges/goals for Aviation
aviation_challenges = {
    "Cost Reduction": {
        "description": "Reduce overall category spend by 7-10% through strategic sourcing and demand management",
        "status": "In Progress",
        "progress": 45
    },
    "Supply Chain Risk": {
        "description": "Mitigate supplier and geopolitical risks by developing regional secondary sources",
        "status": "At Risk",
        "progress": 30
    },
    "Sustainability": {
        "description": "Achieve 20% reduction in carbon footprint from aviation operations by 2026",
        "status": "On Track",
        "progress": 60
    },
    "Innovation": {
        "description": "Drive supplier-led innovation to improve fuel efficiency by 15%",
        "status": "Need Attention",
        "progress": 25
    }
}

# Create simplified tabbed interface focusing only on key Category Intelligence aspects
overview_tab, insights_tab, action_tab = st.tabs([
    "📈 Category Overview", 
    "🔍 Key Insights", 
    "🎯 Action Plan"
])

# Control the narrative journey based on which tab the user is on
with overview_tab:
    st.session_state.visited_tabs.add("overview")
    if "overview" not in st.session_state.visited_tabs:
        st.session_state.current_story_step = 1
    
    # Executive dashboard section
    st.markdown(
        """
        <div class="dashboard-summary">
            <h3 style="margin-top:0">Executive Summary</h3>
        """
        + exec_summary +
        """
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Category Health Scorecard
    st.markdown('<div class="sub-header">Category Health Scorecard</div>', unsafe_allow_html=True)
    
    # Calculate health scores with some randomization but weighted towards specific narratives for each category
    if selected_category == "Aviation":
        health_score = 76
        risk_score = 65
        opportunity_score = 82
        efficiency_score = 78
        innovation_score = 72
    else:
        health_score = np.random.randint(65, 95)
        risk_score = np.random.randint(60, 90)
        opportunity_score = np.random.randint(70, 95)
        efficiency_score = np.random.randint(65, 90)
        innovation_score = np.random.randint(60, 85)
    
    # Set colors based on scores
    health_color = "#10B981" if health_score >= 80 else "#F59E0B" if health_score >= 70 else "#EF4444"
    risk_color = "#10B981" if risk_score >= 80 else "#F59E0B" if risk_score >= 70 else "#EF4444"
    opportunity_color = "#10B981" if opportunity_score >= 80 else "#F59E0B" if opportunity_score >= 70 else "#EF4444"
    efficiency_color = "#10B981" if efficiency_score >= 80 else "#F59E0B" if efficiency_score >= 70 else "#EF4444"
    innovation_color = "#10B981" if innovation_score >= 80 else "#F59E0B" if innovation_score >= 70 else "#EF4444"
    
    # Health score metrics in a row with improved styling
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Overall Health", f"{health_score}/100", delta=f"{np.random.randint(-3, 8)}%")
        st.markdown(
            f"""
            <div class="kpi-indicator">
                <div class="indicator {'good' if health_score >= 80 else 'warning' if health_score >= 70 else 'critical'}"></div>
                <div class="text" style="color:{health_color}">{'Strong' if health_score >= 80 else 'Moderate' if health_score >= 70 else 'Needs Attention'}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Risk Level", f"{risk_score}/100", delta=f"{np.random.randint(-8, 5)}%")
        st.markdown(
            f"""
            <div class="kpi-indicator">
                <div class="indicator {'good' if risk_score >= 80 else 'warning' if risk_score >= 70 else 'critical'}"></div>
                <div class="text" style="color:{risk_color}">{'Low' if risk_score >= 80 else 'Moderate' if risk_score >= 70 else 'High'}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Opportunity", f"{opportunity_score}/100", delta=f"{np.random.randint(0, 12)}%")
        st.markdown(
            f"""
            <div class="kpi-indicator">
                <div class="indicator {'good' if opportunity_score >= 80 else 'warning' if opportunity_score >= 70 else 'critical'}"></div>
                <div class="text" style="color:{opportunity_color}">{'Significant' if opportunity_score >= 80 else 'Moderate' if opportunity_score >= 70 else 'Limited'}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Efficiency", f"{efficiency_score}/100", delta=f"{np.random.randint(-4, 9)}%")
        st.markdown(
            f"""
            <div class="kpi-indicator">
                <div class="indicator {'good' if efficiency_score >= 80 else 'warning' if efficiency_score >= 70 else 'critical'}"></div>
                <div class="text" style="color:{efficiency_color}">{'Optimized' if efficiency_score >= 80 else 'Improving' if efficiency_score >= 70 else 'Inefficient'}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Innovation", f"{innovation_score}/100", delta=f"{np.random.randint(-2, 15)}%")
        st.markdown(
            f"""
            <div class="kpi-indicator">
                <div class="indicator {'good' if innovation_score >= 80 else 'warning' if innovation_score >= 70 else 'critical'}"></div>
                <div class="text" style="color:{innovation_color}">{'Leading' if innovation_score >= 80 else 'Advancing' if innovation_score >= 70 else 'Lagging'}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Category Goals and Progress
    st.markdown('<div class="sub-header">Category Goals & Challenges</div>', unsafe_allow_html=True)
    
    # Display category-specific goals
    if selected_category == "Aviation":
        for goal, details in aviation_challenges.items():
            status_color = "#10B981" if details["status"] == "On Track" else "#F59E0B" if details["status"] == "In Progress" or details["status"] == "Need Attention" else "#EF4444"
            
            st.markdown(
                f"""
                <div class="insight-card">
                    <h4>{goal}</h4>
                    <p>{details["description"]}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                        <div style="width: 70%; background-color: #E5E7EB; height: 10px; border-radius: 5px;">
                            <div style="width: {details["progress"]}%; background-color: {status_color}; height: 10px; border-radius: 5px;"></div>
                        </div>
                        <div style="color: {status_color}; font-weight: 600;">{details["status"]} ({details["progress"]}%)</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        # Add goal setting interface for other categories
        st.markdown("Set strategic goals for this category to track progress:")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            new_goal = st.text_input("Add a strategic goal or challenge:")
        with col2:
            if st.button("Add Goal"):
                if new_goal:
                    if selected_category not in st.session_state.goals:
                        st.session_state.goals[selected_category] = []
                    st.session_state.goals[selected_category].append(new_goal)
                    st.success(f"Goal added for {selected_category}")
        
        # Display any added goals
        if selected_category in st.session_state.goals and st.session_state.goals[selected_category]:
            for i, goal in enumerate(st.session_state.goals[selected_category]):
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <h4>Goal {i+1}</h4>
                        <p>{goal}</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                            <div style="width: 70%; background-color: #E5E7EB; height: 10px; border-radius: 5px;">
                                <div style="width: 0%; background-color: #3B82F6; height: 10px; border-radius: 5px;"></div>
                            </div>
                            <div style="color: #3B82F6; font-weight: 600;">Not Started (0%)</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No goals have been set for this category yet. Add goals to track progress.")
    
    # Key Insights - dynamic based on category
    st.markdown('<div class="sub-header">Key Category Insights</div>', unsafe_allow_html=True)
    
    # Aviation-specific insights
    if selected_category == "Aviation":
        insights = [
            {
                "type": "opportunity",
                "title": "Cost Reduction Opportunity",
                "description": "There's potential to save 12-15% ($18M annually) through consolidated purchasing of MRO supplies across regions. Current fragmentation is leading to price variance of up to 22%.",
                "impact": "High",
                "action": "Launch global MRO consolidation initiative"
            },
            {
                "type": "risk",
                "title": "Supply Chain Vulnerability",
                "description": "Single-source dependency for critical avionics components creates high supply risk. Recent supplier performance issues have impacted on-time delivery by 15%.",
                "impact": "Critical",
                "action": "Develop secondary source for top 5 critical components"
            },
            {
                "type": "alert",
                "title": "Contract Renewal Alert",
                "description": "Major contracts with Rolls-Royce and Honeywell Aerospace expire within 6 months, representing $25.4M in annual spend. Preliminary market analysis suggests favorable renegotiation conditions.",
                "impact": "Medium",
                "action": "Initiate contract renewal strategy development"
            }
        ]
    else:
        # Generate generic insights for other categories
        insights = [
            {
                "type": "opportunity",
                "title": f"{selected_category} Savings Opportunity",
                "description": f"Analysis shows potential for 8-10% cost reduction in {selected_category} through strategic sourcing and demand management.",
                "impact": "Medium",
                "action": "Develop strategic sourcing plan"
            },
            {
                "type": "risk",
                "title": "Supplier Concentration Risk",
                "description": f"Top 3 suppliers account for 68% of {selected_category} spend, creating significant dependency risk.",
                "impact": "High",
                "action": "Diversify supplier base"
            },
            {
                "type": "alert",
                "title": "Market Price Volatility",
                "description": f"{selected_category} prices have fluctuated by 15% in the last quarter, impacting budget predictability.",
                "impact": "Medium",
                "action": "Implement price hedging strategy"
            }
        ]
    
    # Display insights with action buttons
    for insight in insights:
        style_class = f"insight-card {insight['type']}"
        impact_color = "#EF4444" if insight["impact"] == "Critical" or insight["impact"] == "High" else "#F59E0B" if insight["impact"] == "Medium" else "#10B981"
        
        st.markdown(
            f"""
            <div class="{style_class}">
                <h4>{insight["title"]}</h4>
                <p>{insight["description"]}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
                    <span style="background-color: {impact_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 500;">{insight["impact"]} Impact</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(f"Take Action: {insight['action']}", key=f"action_{insight['title']}"):
                st.session_state.insights_viewed += 1
                st.session_state.show_recommendations = True
                st.success(f"Action plan for '{insight['title']}' has been initiated")
        with col2:
            pass
            
    # Market News feed for the category
    st.markdown('<div class="sub-header">Latest Market Intelligence</div>', unsafe_allow_html=True)
    
    # Aviation-specific news
    if selected_category == "Aviation":
        news_items = [
            {
                "title": "Boeing Announces Production Increase for 737 MAX",
                "date": "May 5, 2025",
                "content": "Boeing plans to increase 737 MAX production by 25% starting Q3 2025, potentially impacting component pricing and availability. This follows increased demand from major airlines.",
                "source": "Aviation Week",
                "impact": "high-impact"
            },
            {
                "title": "EU Introduces New Carbon Taxation for Aviation Industry",
                "date": "May 3, 2025",
                "content": "The European Union has approved new carbon taxation measures for the aviation industry, effective January 2026. This will increase operational costs by an estimated 5-8% for carriers.",
                "source": "FlightGlobal",
                "impact": "high-impact"
            },
            {
                "title": "Global MRO Market Expected to Grow 12% by 2027",
                "date": "April 29, 2025",
                "content": "Industry analysts project 12% growth in the global aviation MRO market over the next two years, driven by fleet expansions in Asia Pacific and Middle East regions.",
                "source": "MRO Network",
                "impact": "neutral"
            }
        ]
    else:
        news_items = simulated_web_scrape(selected_category)
    
    # Display news items
    for item in news_items:
        impact_class = item.get("impact", "neutral")
        
        st.markdown(
            f"""
            <div class="news-item {impact_class}">
                <div class="news-title">{item["title"]}</div>
                <div class="news-date">{item["date"]} | Source: {item.get("source", "Market Intelligence")}</div>
                <p>{item["content"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Navigate to next tab button
    if st.button("View Key Insights →", use_container_width=True):
        st.session_state.current_story_step = 2
        st.rerun()

# Key Insights Tab - Second step in the journey
with insights_tab:
    st.session_state.visited_tabs.add("insights")
    if "insights" in st.session_state.visited_tabs and st.session_state.current_story_step < 2:
        st.session_state.current_story_step = 2
    
    st.markdown('<div class="sub-header">Market & Spend Analysis</div>', unsafe_allow_html=True)
    
    # Introduction to this section
    st.markdown(
        """
        <div class="dashboard-summary">
            This section provides deep insights into market trends, price movements, and spend patterns. 
            Understanding these dynamics helps identify cost-saving opportunities and anticipate market shifts 
            that might impact your procurement strategy.
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Create two tabs for Market Trends and Spend Analysis
    market_tab, spend_tab = st.tabs(["Market Trends", "Spend Analysis"])
    
    with market_tab:
        st.markdown("### Market Price Trends & Forecast")
        
        # Context-specific market trends
        if selected_category == "Aviation":
            # Create a dataframe for aviation market components pricing
            end_date = pd.Timestamp('2025-05-01')
            start_date = end_date - pd.DateOffset(months=18)
            date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
            
            # Price index data (representing a composite aviation price index)
            components = {
                "Aircraft Components": {
                    "base": 100,
                    "trend": 0.5,  # 0.5% increase per month on average
                    "volatility": 2.0,
                    "color": "#3B82F6"
                },
                "Avionics": {
                    "base": 100,
                    "trend": 0.8,  # 0.8% increase per month
                    "volatility": 1.5,
                    "color": "#10B981"
                },
                "MRO Services": {
                    "base": 100,
                    "trend": 0.3,  # 0.3% increase per month
                    "volatility": 1.2,
                    "color": "#F59E0B"
                },
                "Fuel": {
                    "base": 100,
                    "trend": 1.2,  # More volatile
                    "volatility": 4.0,
                    "color": "#EF4444"
                }
            }
            
            # Generate price data
            price_data = []
            
            for component, params in components.items():
                base = params["base"]
                monthly_trend = params["trend"] / 100  # Convert percentage to decimal
                volatility = params["volatility"] / 100  # Volatility as percentage
                
                for i, date in enumerate(date_range):
                    # Add trend and random volatility
                    factor = 1 + (monthly_trend * i) + np.random.normal(0, volatility)
                    price = base * factor
                    
                    # Add seasonal patterns for some components
                    if component == "Fuel":
                        # Add seasonal pattern (higher in summer months)
                        month = date.month
                        seasonal_factor = 1.0 + 0.05 * np.sin((month - 1) * np.pi / 6)
                        price *= seasonal_factor
                    
                    price_data.append({
                        "Date": date,
                        "Component": component,
                        "Price Index": round(price, 2),
                        "Color": params["color"]
                    })
            
            df_prices = pd.DataFrame(price_data)
            
            # Create a plot with all price trends
            fig = px.line(
                df_prices, 
                x="Date", 
                y="Price Index", 
                color="Component",
                color_discrete_map={c: p["color"] for c, p in components.items()},
                title="Aviation Category Price Trends (Indexed)",
                markers=True
            )
            
            # Improve the plot styling
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Price Index (Base=100)",
                legend_title="Component",
                height=450,
                hovermode="x unified",
                plot_bgcolor="white",
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#E5E7EB',
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#E5E7EB',
                    range=[90, 130]  # Set a reasonable y-axis range
                )
            )
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Generate price forecast for the next 6 months
            st.markdown("### 6-Month Price Forecast")
            
            forecast_components = ["Aircraft Components", "Fuel"]
            forecast_periods = 6
            forecast_end = end_date + pd.DateOffset(months=forecast_periods)
            forecast_range = pd.date_range(start=end_date + pd.DateOffset(months=1), end=forecast_end, freq='MS')
            
            forecast_data = []
            
            # Get the last actual prices
            for component in forecast_components:
                last_actual = df_prices[(df_prices["Component"] == component) & (df_prices["Date"] == end_date)]["Price Index"].values[0]
                params = components[component]
                
                # Baseline forecast (trend only)
                baseline_forecast = []
                optimistic_forecast = []
                pessimistic_forecast = []
                
                for i in range(1, forecast_periods + 1):
                    # Baseline: continue current trend
                    baseline_price = last_actual * (1 + params["trend"] / 100 * i)
                    baseline_forecast.append(baseline_price)
                    
                    # Optimistic: lower trend
                    optimistic_price = last_actual * (1 + (params["trend"] - 0.2) / 100 * i)
                    optimistic_forecast.append(optimistic_price)
                    
                    # Pessimistic: higher trend
                    pessimistic_price = last_actual * (1 + (params["trend"] + 0.7) / 100 * i)
                    pessimistic_forecast.append(pessimistic_price)
                
                # Add historical data
                historical = df_prices[df_prices["Component"] == component]
                
                # Create forecast plot
                component_title = component
                fig = go.Figure()
                
                # Add historical line
                fig.add_trace(
                    go.Scatter(
                        x=historical["Date"],
                        y=historical["Price Index"],
                        name="Historical",
                        line=dict(color=params["color"], width=3),
                        mode="lines+markers"
                    )
                )
                
                # Add forecast lines
                fig.add_trace(
                    go.Scatter(
                        x=forecast_range,
                        y=baseline_forecast,
                        name="Baseline Forecast",
                        line=dict(color=params["color"], width=2, dash="solid"),
                        mode="lines"
                    )
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=forecast_range,
                        y=pessimistic_forecast,
                        name="Pessimistic",
                        line=dict(color="#EF4444", width=2, dash="dot"),
                        mode="lines"
                    )
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=forecast_range,
                        y=optimistic_forecast,
                        name="Optimistic",
                        line=dict(color="#10B981", width=2, dash="dot"),
                        mode="lines"
                    )
                )
                
                # Add forecast cone (shaded area between optimistic and pessimistic)
                fig.add_trace(
                    go.Scatter(
                        x=list(forecast_range) + list(forecast_range)[::-1],
                        y=list(pessimistic_forecast) + list(optimistic_forecast)[::-1],
                        fill='toself',
                        fillcolor='rgba(59, 130, 246, 0.1)',
                        line=dict(color='rgba(255,255,255,0)'),
                        hoverinfo="skip",
                        showlegend=False
                    )
                )
                
                # Improve plot styling
                fig.update_layout(
                    title=f"{component_title} Price Forecast",
                    xaxis_title="",
                    yaxis_title="Price Index",
                    legend_title="Scenario",
                    height=350,
                    hovermode="x unified",
                    plot_bgcolor="white",
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#E5E7EB',
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='#E5E7EB',
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                # Add a vertical line at the forecast start
                fig.add_vline(
                    x=end_date, 
                    line_width=1, 
                    line_dash="dash", 
                    line_color="gray",
                    annotation_text="Forecast Start", 
                    annotation_position="top right"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display key insights from the forecast
                if component == "Aircraft Components":
                    forecast_change = round(((baseline_forecast[-1] - last_actual) / last_actual) * 100, 1)
                    st.markdown(
                        f"""
                        <div class="insight-card">
                            <h4>Aircraft Components Market Insights</h4>
                            <p>
                                Projected {forecast_change}% price increase over the next 6 months for aircraft components.
                                The market is showing consistent upward pressure due to ongoing supply chain constraints and
                                increased demand from aircraft manufacturers.
                            </p>
                            <p>
                                <strong>Recommended Action:</strong> Consider locking in longer-term contracts now
                                before projected price increases materialize. Evaluate potential for volume-based
                                discounts to mitigate impact.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                elif component == "Fuel":
                    forecast_change = round(((baseline_forecast[-1] - last_actual) / last_actual) * 100, 1)
                    volatility = round(np.std(pessimistic_forecast) / np.mean(pessimistic_forecast) * 100, 1)
                    st.markdown(
                        f"""
                        <div class="insight-card risk">
                            <h4>Fuel Price Risk Alert</h4>
                            <p>
                                Forecast indicates {forecast_change}% increase in fuel prices with {volatility}% volatility.
                                Geopolitical tensions and seasonal demand patterns suggest potential for significant price spikes
                                in Q3 2025.
                            </p>
                            <p>
                                <strong>Recommended Action:</strong> Implement fuel hedging strategy covering 50-60% of projected 
                                consumption for next 6 months to reduce volatility impact. Consider fuel efficiency initiatives
                                to reduce overall exposure.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Market indicators and correlation analysis
            st.markdown("### Market Leading Indicators")
            
            # Create correlation matrix of factors affecting aviation pricing
            factors = [
                "Jet Fuel Price",
                "Aircraft Production Rate",
                "Air Traffic Volume",
                "Labor Cost Index",
                "Aluminum Price",
                "USD Exchange Rate",
                "GDP Growth"
            ]
            
            # Create correlation matrix with some realistic correlations
            corr_data = [
                [1.00, 0.25, 0.65, 0.40, 0.70, 0.55, 0.30],  # Jet Fuel
                [0.25, 1.00, 0.75, 0.60, 0.45, 0.15, 0.65],  # Aircraft Production
                [0.65, 0.75, 1.00, 0.35, 0.30, 0.20, 0.80],  # Air Traffic
                [0.40, 0.60, 0.35, 1.00, 0.55, 0.25, 0.40],  # Labor Cost
                [0.70, 0.45, 0.30, 0.55, 1.00, 0.60, 0.25],  # Aluminum
                [0.55, 0.15, 0.20, 0.25, 0.60, 1.00, 0.35],  # USD Exchange
                [0.30, 0.65, 0.80, 0.40, 0.25, 0.35, 1.00],  # GDP Growth
            ]
            
            corr_df = pd.DataFrame(corr_data, columns=factors, index=factors)
            
            # Create a heatmap of correlations
            fig = px.imshow(
                corr_df,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                title="Market Factor Correlation Matrix",
                aspect="auto"
            )
            
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
            
            # Market factor analysis
            st.markdown(
                """
                <div class="insight-card opportunity">
                    <h4>Market Intelligence Insight</h4>
                    <p>
                        Strong correlation (0.80) between Air Traffic Volume and GDP Growth presents an
                        opportunity. Economic indicators suggest 4.2% GDP growth in key markets, which
                        historically precedes increased air traffic volume by 3-4 months.
                    </p>
                    <p>
                        <strong>Strategic Opportunity:</strong> Proactively plan capacity expansion with suppliers
                        now to avoid potential supply constraints when demand increases. Consider timing contract
                        negotiations before air traffic volumes increase to secure more favorable terms.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        else:
            # For other categories, show generic market trend data
            st.info(f"Displaying standard market trends for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Generate generic price trend data
            end_date = pd.Timestamp('2025-05-01')
            start_date = end_date - pd.DateOffset(months=18)
            date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
            
            # Generate price data with trend and seasonality
            price_data = []
            
            base_price = 100
            trend = 0.5 / 100  # 0.5% monthly upward trend
            
            for i, date in enumerate(date_range):
                # Add trend and random noise
                price = base_price * (1 + trend * i) + np.random.normal(0, 2)
                
                # Add seasonality
                season_effect = 5 * np.sin(2 * np.pi * i / 12)
                price += season_effect
                
                price_data.append({
                    "Date": date,
                    "Price Index": price
                })
            
            df_price = pd.DataFrame(price_data)
            
            fig = px.line(
                df_price,
                x="Date",
                y="Price Index",
                title=f"{selected_category} Price Index",
                markers=True
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Generic forecast
            st.markdown("### Market Forecast")
            
            # Simple forecast (trend extrapolation)
            last_price = df_price.iloc[-1]["Price Index"]
            forecast_periods = 6
            forecast_dates = pd.date_range(
                start=end_date + pd.DateOffset(months=1),
                periods=forecast_periods,
                freq='MS'
            )
            
            # Simple forecast calculation
            forecast_prices = [last_price * (1 + trend * (i+1)) for i in range(forecast_periods)]
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame({
                "Date": forecast_dates,
                "Forecast": forecast_prices
            })
            
            # Combine historical and forecast for plotting
            historical = df_price.copy()
            historical["Type"] = "Historical"
            historical = historical.rename(columns={"Price Index": "Value"})
            
            forecast = forecast_df.copy()
            forecast["Type"] = "Forecast"
            forecast = forecast.rename(columns={"Forecast": "Value"})
            
            combined = pd.concat([
                historical[["Date", "Value", "Type"]],
                forecast[["Date", "Value", "Type"]]
            ])
            
            # Create the plot
            fig = px.line(
                combined,
                x="Date",
                y="Value",
                color="Type",
                title=f"{selected_category} Price Forecast",
                color_discrete_map={"Historical": "#3B82F6", "Forecast": "#F59E0B"}
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with spend_tab:
        st.markdown("### Category Spend Analysis")
        
        # Context-specific spend analysis
        if selected_category == "Aviation":
            # Create and display spend breakdown by subcategory
            subcategories = {
                "Aircraft Parts & Components": 42,
                "MRO Services": 25,
                "Fuel": 18,
                "Ground Support Equipment": 8,
                "Engineering Services": 7
            }
            
            # Create pie chart of subcategory spend
            fig = px.pie(
                values=list(subcategories.values()),
                names=list(subcategories.keys()),
                title="Aviation Spend by Subcategory",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                hole=0.4
            )
            
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Spend trend by month
            st.markdown("### Monthly Spend Trend")
            
            # Create monthly spend trend data
            monthly_spend = []
            baseline = 15000000  # $15M monthly baseline
            
            for i, date in enumerate(date_range):
                # Add seasonality and slight upward trend
                seasonal_factor = 1 + 0.15 * np.sin((date.month - 1) * np.pi / 6)
                trend_factor = 1 + 0.02 * (i / len(date_range))
                
                spend = baseline * seasonal_factor * trend_factor
                
                # Add some random noise
                spend *= np.random.normal(1, 0.05)
                
                monthly_spend.append({
                    "Date": date,
                    "Spend": round(spend, 0)
                })
            
            monthly_df = pd.DataFrame(monthly_spend)
            
            # Create a bar chart of monthly spend
            fig = px.bar(
                monthly_df,
                x="Date",
                y="Spend",
                title="Monthly Aviation Spend",
                color_discrete_sequence=["#3B82F6"]
            )
            
            # Add a trend line
            fig.add_trace(
                go.Scatter(
                    x=monthly_df["Date"],
                    y=monthly_df["Spend"].rolling(window=3).mean(),
                    mode="lines",
                    name="3-Month Moving Average",
                    line=dict(color="#EF4444", width=3)
                )
            )
            
            # Update layout
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Monthly Spend ($)",
                legend_title="",
                height=400,
                hovermode="x unified",
                yaxis=dict(tickformat="$,.0f")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Spend by supplier - Top 10 suppliers
            st.markdown("### Spend by Supplier")
            
            suppliers_spend = []
            total_spend = sum(s["spend"] for s in aviation_suppliers.values())
            
            for supplier, details in aviation_suppliers.items():
                suppliers_spend.append({
                    "Supplier": supplier,
                    "Spend": details["spend"],
                    "Percentage": round(details["spend"] / total_spend * 100, 1)
                })
            
            # Sort by spend descending
            suppliers_df = pd.DataFrame(suppliers_spend).sort_values("Spend", ascending=False)
            
            # Create a bar chart of supplier spend
            fig = px.bar(
                suppliers_df,
                x="Supplier",
                y="Spend",
                title="Top 10 Suppliers by Spend",
                color="Supplier",
                text="Percentage",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            # Update layout
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Annual Spend ($)",
                showlegend=False,
                height=450,
                yaxis=dict(tickformat="$,.0f")
            )
            
            # Update text position and format
            fig.update_traces(
                texttemplate="%{text}%",
                textposition="outside"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights from spend analysis
            spend_80_percent = suppliers_df["Spend"].cumsum() / total_spend
            suppliers_80_percent = (spend_80_percent <= 0.8).sum()
            
            # Calculate spend concentration (Herfindahl Index)
            herfindahl = sum((s["spend"] / total_spend)**2 for s in aviation_suppliers.values())
            concentration_level = "High" if herfindahl > 0.25 else "Moderate" if herfindahl > 0.15 else "Low"
            
            st.markdown(
                f"""
                <div class="insight-card">
                    <h4>Spend Concentration Analysis</h4>
                    <p>
                        <strong>Supplier Concentration:</strong> {suppliers_80_percent} suppliers represent 80% of total category spend.
                        <br>
                        <strong>Concentration Level:</strong> {concentration_level} (Herfindahl Index: {herfindahl:.2f})
                    </p>
                    <p>
                        <strong>Insight:</strong> The aviation category shows {concentration_level.lower()} supplier concentration, 
                        {'which presents consolidation opportunities to improve leverage and streamline supplier management.' 
                        if concentration_level == 'Low' else 
                        'indicating balanced supplier distribution while maintaining negotiation leverage.' 
                        if concentration_level == 'Moderate' else
                        'suggesting high dependency on few suppliers. Consider supplier diversification to reduce risk.'}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Spend compliance analysis
            st.markdown("### Spend Compliance & Savings Opportunities")
            
            # Create a dataframe for compliance metrics
            compliance_metrics = {
                "On-Contract Spend": 68,
                "Price Compliance": 82,
                "PO Compliance": 74,
                "Payment Term Compliance": 91
            }
            
            compliance_df = pd.DataFrame({
                "Metric": list(compliance_metrics.keys()),
                "Compliance Rate": list(compliance_metrics.values()),
                "Target": [85, 95, 90, 95]
            })
            
            # Calculate the gap to target
            compliance_df["Gap"] = compliance_df["Target"] - compliance_df["Compliance Rate"]
            compliance_df["Gap"] = compliance_df["Gap"].apply(lambda x: max(0, x))
            
            # Calculate the opportunity value
            avg_annual_spend = total_spend
            opportunity_values = []
            
            # Simple opportunity calculation logic
            for _, row in compliance_df.iterrows():
                if row["Metric"] == "On-Contract Spend":
                    # Assume 10% savings on non-compliant spend that could be brought on contract
                    value = avg_annual_spend * (row["Gap"] / 100) * 0.1
                elif row["Metric"] == "Price Compliance":
                    # Assume direct impact of price compliance gap
                    value = avg_annual_spend * (row["Gap"] / 100) * 0.12
                elif row["Metric"] == "PO Compliance":
                    # Assume 5% excess cost on non-PO spend
                    value = avg_annual_spend * (row["Gap"] / 100) * 0.05
                elif row["Metric"] == "Payment Term Compliance":
                    # Assume working capital impact
                    value = avg_annual_spend * (row["Gap"] / 100) * 0.02
                else:
                    value = 0
                
                opportunity_values.append(round(value, 0))
            
            compliance_df["Opportunity Value"] = opportunity_values
            
            # Create a bar chart showing compliance rates vs targets
            fig = go.Figure()
            
            # Add bars for actual compliance
            fig.add_trace(go.Bar(
                x=compliance_df["Metric"],
                y=compliance_df["Compliance Rate"],
                name="Current Compliance",
                marker_color="#3B82F6"
            ))
            
            # Add target lines
            fig.add_trace(go.Scatter(
                x=compliance_df["Metric"],
                y=compliance_df["Target"],
                mode="markers+lines",
                name="Target",
                marker=dict(size=10, symbol="diamond", color="#EF4444"),
                line=dict(width=2, dash="dot", color="#EF4444")
            ))
            
            # Update layout
            fig.update_layout(
                title="Compliance Metrics vs. Targets",
                xaxis_title="",
                yaxis_title="Compliance Rate (%)",
                legend_title="",
                height=400,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display opportunity values
            st.markdown("### Identified Savings Opportunities")
            
            # Format the values as currency
            compliance_df["Formatted Value"] = compliance_df["Opportunity Value"].apply(
                lambda x: f"${x:,.0f}"
            )
            
            # Sort by opportunity value
            compliance_df = compliance_df.sort_values("Opportunity Value", ascending=False)
            
            # Create a bar chart of opportunity values
            fig = px.bar(
                compliance_df,
                x="Metric",
                y="Opportunity Value",
                title="Annual Savings Opportunities",
                text="Formatted Value",
                color="Opportunity Value",
                color_continuous_scale="Viridis"
            )
            
            # Update layout
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Opportunity Value ($)",
                height=400,
                coloraxis_showscale=False,
                yaxis=dict(tickformat="$,.0f")
            )
            
            # Update text position
            fig.update_traces(
                textposition="outside"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Total opportunity
            total_opportunity = compliance_df["Opportunity Value"].sum()
            percentage_of_spend = (total_opportunity / avg_annual_spend) * 100
            
            st.markdown(
                f"""
                <div class="insight-card opportunity">
                    <h4>Compliance-Driven Savings Opportunity</h4>
                    <p>
                        <strong>Total Identified Opportunity:</strong> ${total_opportunity:,.0f} ({percentage_of_spend:.1f}% of annual spend)
                    </p>
                    <p>
                        <strong>Primary Opportunity Areas:</strong>
                        <ul>
                            <li><strong>Price Compliance:</strong> Enforce contract pricing across divisions</li>
                            <li><strong>On-Contract Spend:</strong> Redirect maverick spending to contracted suppliers</li>
                            <li><strong>PO Compliance:</strong> Improve requisition-to-PO processes</li>
                        </ul>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        else:
            # Generic spend analysis for other categories
            st.info(f"Displaying standard spend analysis for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Generate and display generic spend data
            spend_data = generate_spend_data(selected_category)
            
            # Create pie chart
            fig = px.pie(
                spend_data,
                values="Value",
                names="Subcategory",
                title=f"{selected_category} Spend by Subcategory"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Simple spend trend
            months = 12
            date_range = pd.date_range(end=pd.Timestamp('2025-05-01'), periods=months, freq='MS')
            
            spend_trend = []
            base_spend = 1000000  # $1M base monthly spend
            
            for i, date in enumerate(date_range):
                # Add some trend and randomness
                spend = base_spend * (1 + 0.02 * i / months) * np.random.normal(1, 0.1)
                spend_trend.append({
                    "Date": date,
                    "Spend": spend
                })
            
            trend_df = pd.DataFrame(spend_trend)
            
            # Create trend chart
            fig = px.line(
                trend_df,
                x="Date",
                y="Spend",
                title=f"{selected_category} Monthly Spend Trend",
                markers=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Navigate to next step button
    # Continue button not needed here anymore as we're keeping supplier analysis in the same tab
    # This content is all part of the Key Insights tab now

# Supplier Analysis Tab - Third step in the journey
# Part of Key Insights tab
with insights_tab:
    # Supply analysis section - continued from above
    
    st.markdown('<div class="sub-header">Supplier Portfolio Analysis</div>', unsafe_allow_html=True)
    
    # Introduction to supplier analysis
    st.markdown(
        """
        <div class="dashboard-summary">
            This section provides a comprehensive view of your supplier ecosystem, including performance metrics,
            risk profiles, relationship assessments, and strategic positioning. Use these insights to optimize your
            supplier portfolio and enhance collaborative relationships.
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Create supplier analysis subtabs
    supplier_overview_tab, performance_tab, risk_tab, relationship_tab = st.tabs([
        "Supplier Overview", "Performance Analysis", "Risk Assessment", "Relationship Management"
    ])
    
    with supplier_overview_tab:
        st.markdown("### Supplier Portfolio Overview")
        
        if selected_category == "Aviation":
            # Create a dataframe with supplier details
            supplier_data = []
            
            for supplier_name, details in aviation_suppliers.items():
                supplier_data.append({
                    "Supplier": supplier_name,
                    "Annual Spend": details["spend"],
                    "Risk Level": details["risk"],
                    "Performance Score": details["performance"],
                    "Contract End Date": details["contract_end"]
                })
            
            supplier_df = pd.DataFrame(supplier_data)
            
            # Sort by annual spend descending
            supplier_df = supplier_df.sort_values("Annual Spend", ascending=False)
            
            # Format the Annual Spend column
            supplier_df["Annual Spend (Formatted)"] = supplier_df["Annual Spend"].apply(
                lambda x: f"${x:,.0f}"
            )
            
            # Create a formatted dataframe for display
            display_df = supplier_df[["Supplier", "Annual Spend (Formatted)", "Risk Level", "Performance Score", "Contract End Date"]]
            display_df = display_df.rename(columns={
                "Annual Spend (Formatted)": "Annual Spend",
                "Performance Score": "Performance"
            })
            
            # Render as Streamlit dataframe with formatting
            st.dataframe(
                display_df,
                column_config={
                    "Supplier": st.column_config.TextColumn("Supplier Name"),
                    "Annual Spend": st.column_config.TextColumn("Annual Spend"),
                    "Risk Level": st.column_config.TextColumn("Risk Level"),
                    "Performance": st.column_config.ProgressColumn(
                        "Performance Score",
                        format="%d",
                        min_value=0,
                        max_value=100
                    ),
                    "Contract End Date": st.column_config.DateColumn(
                        "Contract End Date",
                        format="MMM DD, YYYY"
                    ),
                },
                use_container_width=True,
                hide_index=True
            )
            
            # Create supplier quadrant analysis
            st.markdown("### Strategic Supplier Positioning")
            
            # Add a description of the quadrant analysis
            st.markdown(
                """
                <div style='margin-bottom: 1rem;'>
                The strategic positioning matrix plots suppliers based on their performance and strategic importance (spend).
                This visualization helps identify which suppliers to invest in, maintain, develop, or phase out.
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Create data for quadrant analysis
            quadrant_data = []
            
            for supplier, details in aviation_suppliers.items():
                # Calculate strategic importance as normalized spend (0-100)
                max_spend = max(s["spend"] for s in aviation_suppliers.values())
                strategic_importance = (details["spend"] / max_spend) * 100
                
                # Use performance score directly (already 0-100)
                performance = details["performance"]
                
                # Add bubble size based on spend
                bubble_size = details["spend"] / 1000000  # Scale down for visualization
                
                # Add risk color coding
                risk_color = "#10B981" if details["risk"] == "Low" else "#F59E0B" if details["risk"] == "Medium" else "#EF4444"
                
                quadrant_data.append({
                    "Supplier": supplier,
                    "Strategic Importance": strategic_importance,
                    "Performance": performance,
                    "Spend": details["spend"],
                    "Risk": details["risk"],
                    "Size": bubble_size,
                    "Color": risk_color
                })
            
            quadrant_df = pd.DataFrame(quadrant_data)
            
            # Create a bubble chart for quadrant analysis
            fig = px.scatter(
                quadrant_df,
                x="Strategic Importance",
                y="Performance",
                size="Size",
                color="Risk",
                hover_name="Supplier",
                text="Supplier",
                size_max=40,
                color_discrete_map={
                    "Low": "#10B981",
                    "Medium": "#F59E0B",
                    "High": "#EF4444"
                }
            )
            
            # Add quadrant lines
            fig.add_hline(
                y=80,
                line_width=1,
                line_dash="dash",
                line_color="gray"
            )
            
            fig.add_vline(
                x=50,
                line_width=1,
                line_dash="dash",
                line_color="gray"
            )
            
            # Add quadrant labels
            fig.add_annotation(
                x=25, y=90,
                text="DEVELOP<br>(High Performance, Low Importance)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            fig.add_annotation(
                x=75, y=90,
                text="CORE PARTNERS<br>(High Performance, High Importance)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            fig.add_annotation(
                x=25, y=70,
                text="PHASE OUT<br>(Low Performance, Low Importance)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            fig.add_annotation(
                x=75, y=70,
                text="IMPROVE<br>(Low Performance, High Importance)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            # Improve the styling
            fig.update_layout(
                title="Strategic Supplier Positioning Matrix",
                height=600,
                plot_bgcolor="white",
                xaxis=dict(
                    title="Strategic Importance (Spend)",
                    showgrid=True,
                    gridcolor='#E5E7EB',
                    range=[0, 105]
                ),
                yaxis=dict(
                    title="Performance Score",
                    showgrid=True,
                    gridcolor='#E5E7EB',
                    range=[65, 95]
                )
            )
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Strategic recommendations based on quadrant analysis
            core_partners = quadrant_df[(quadrant_df["Strategic Importance"] >= 50) & (quadrant_df["Performance"] >= 80)]
            improve_suppliers = quadrant_df[(quadrant_df["Strategic Importance"] >= 50) & (quadrant_df["Performance"] < 80)]
            develop_suppliers = quadrant_df[(quadrant_df["Strategic Importance"] < 50) & (quadrant_df["Performance"] >= 80)]
            phase_out_suppliers = quadrant_df[(quadrant_df["Strategic Importance"] < 50) & (quadrant_df["Performance"] < 80)]
            
            st.markdown(
                f"""
                <div class="insight-card opportunity">
                    <h4>Strategic Portfolio Recommendations</h4>
                    <p>
                        <strong>Core Partners ({len(core_partners)} suppliers):</strong> {', '.join(core_partners["Supplier"].tolist())}
                        <br><em>Strategy: Long-term partnerships, innovation collaboration, strategic alignment</em>
                    </p>
                    <p>
                        <strong>Improvement Focus ({len(improve_suppliers)} suppliers):</strong> {', '.join(improve_suppliers["Supplier"].tolist())}
                        <br><em>Strategy: Performance improvement plans, increased governance, corrective action</em>
                    </p>
                    <p>
                        <strong>Development Candidates ({len(develop_suppliers)} suppliers):</strong> {', '.join(develop_suppliers["Supplier"].tolist())}
                        <br><em>Strategy: Explore additional business opportunities, category expansion</em>
                    </p>
                    <p>
                        <strong>Potential Phase-Out ({len(phase_out_suppliers)} suppliers):</strong> {', '.join(phase_out_suppliers["Supplier"].tolist())}
                        <br><em>Strategy: Evaluate alternatives, consolidation opportunities</em>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        else:
            # Generic supplier analysis for other categories
            st.info(f"Displaying standard supplier analysis for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Generate basic supplier data
            supplier_data = generate_supplier_data(selected_category)
            
            # Create a scatter plot
            fig = px.scatter(
                supplier_data,
                x="Cost",
                y="Quality",
                size="Volume",
                color="Risk",
                hover_name="Supplier",
                size_max=60,
                title=f"{selected_category} Supplier Positioning"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with performance_tab:
        st.markdown("### Supplier Performance Analysis")
        
        if selected_category == "Aviation":
            # Performance metrics to display
            st.markdown(
                """
                <div style='margin-bottom: 1rem;'>
                This dashboard tracks key performance indicators across all suppliers in the aviation category.
                Monitoring these metrics helps identify performance trends, improvement opportunities, and potential risks.
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Create performance metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                avg_quality = round(np.mean([s["performance"] for s in aviation_suppliers.values()]), 1)
                st.metric("Avg. Quality Score", f"{avg_quality}", delta=f"{round(np.random.uniform(-2, 5), 1)}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                otd = round(np.random.uniform(85, 95), 1)
                st.metric("On-Time Delivery", f"{otd}%", delta=f"{round(np.random.uniform(-3, 4), 1)}%")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                defect_rate = round(np.random.uniform(0.8, 3.5), 2)
                st.metric("Defect Rate", f"{defect_rate}%", delta=f"{-round(np.random.uniform(0.1, 0.8), 2)}%")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                cost_compliance = round(np.random.uniform(85, 98), 1)
                st.metric("Cost Compliance", f"{cost_compliance}%", delta=f"{round(np.random.uniform(-2, 6), 1)}%")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Performance trend chart
            st.markdown("### Performance Trends (Last 12 Months)")
            
            # Create time series data for performance trends
            end_date = pd.Timestamp('2025-05-01')
            start_date = end_date - pd.DateOffset(months=12)
            dates = pd.date_range(start=start_date, end=end_date, freq='MS')
            
            # Choose top suppliers for trend analysis
            top_supplier_names = list(aviation_suppliers.keys())[:5]
            
            # Create performance data
            performance_data = []
            
            for supplier in top_supplier_names:
                baseline = aviation_suppliers[supplier]["performance"]
                
                for i, date in enumerate(dates):
                    # Add slight trend and randomness
                    if supplier in ["Boeing", "Airbus"]:
                        # Slight upward trend for top suppliers
                        trend = 0.2
                    else:
                        # More variable for others
                        trend = np.random.uniform(-0.1, 0.3)
                    
                    score = min(100, max(70, baseline + trend * i + np.random.normal(0, 1.5)))
                    
                    performance_data.append({
                        "Date": date,
                        "Supplier": supplier,
                        "Performance Score": score
                    })
            
            performance_df = pd.DataFrame(performance_data)
            
            # Create line chart of performance trends
            fig = px.line(
                performance_df,
                x="Date",
                y="Performance Score",
                color="Supplier",
                markers=True,
                title="Performance Score Trends - Top 5 Suppliers"
            )
            
            # Improve styling
            fig.update_layout(
                height=450,
                hovermode="x unified",
                yaxis=dict(range=[70, 100])
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance distribution chart
            st.markdown("### Performance Distribution Analysis")
            
            # Create a dataframe with all performance metrics
            full_performance = []
            
            for supplier, details in aviation_suppliers.items():
                # Generate random but realistic metrics
                quality_score = details["performance"]
                delivery_score = max(70, min(100, quality_score + np.random.normal(0, 5)))
                responsiveness = max(70, min(100, quality_score + np.random.normal(0, 7)))
                innovation = max(50, min(100, quality_score + np.random.normal(-5, 10)))
                
                full_performance.append({
                    "Supplier": supplier,
                    "Quality": quality_score,
                    "Delivery": delivery_score,
                    "Responsiveness": responsiveness,
                    "Innovation": innovation,
                    "Average": (quality_score + delivery_score + responsiveness + innovation) / 4
                })
            
            perf_df = pd.DataFrame(full_performance)
            
            # Sort by average performance
            perf_df = perf_df.sort_values("Average", ascending=False)
            
            # Create a radar chart for top 3 and bottom 3 suppliers
            top3 = perf_df.head(3)
            bottom3 = perf_df.tail(3)
            
            # Combine for comparison
            compare_df = pd.concat([top3, bottom3])
            
            # Create radar chart
            categories = ["Quality", "Delivery", "Responsiveness", "Innovation"]
            
            fig = go.Figure()
            
            for i, row in compare_df.iterrows():
                supplier = row["Supplier"]
                values = [row[cat] for cat in categories]
                
                # Determine if top or bottom for color
                color = "#10B981" if supplier in top3["Supplier"].values else "#EF4444"
                
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],  # Close the loop
                    theta=categories + [categories[0]],  # Close the loop
                    fill='toself',
                    name=supplier,
                    line_color=color
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[50, 100]
                    ),
                    angularaxis=dict(
                        rotation=45
                    )
                ),
                title="Performance Profile: Top 3 vs Bottom 3 Suppliers",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance insights and recommendations
            top_performer = perf_df.iloc[0]["Supplier"]
            bottom_performer = perf_df.iloc[-1]["Supplier"]
            avg_score = round(perf_df["Average"].mean(), 1)
            
            # Calculate improvement potential
            below_target = perf_df[perf_df["Average"] < 85]
            potential_gain = round(sum((85 - below_target["Average"]) * (aviation_suppliers[s]["spend"] / 1000000) / 100 * 1.2) for s in below_target["Supplier"]), 1)
            
            st.markdown(
                f"""
                <div class="insight-card">
                    <h4>Performance Analysis Insights</h4>
                    <p>
                        <strong>Top Performer:</strong> {top_performer} consistently demonstrates excellence across all metrics,
                        particularly in quality and delivery reliability.
                    </p>
                    <p>
                        <strong>Improvement Focus:</strong> {bottom_performer} shows significant gaps in responsiveness
                        and innovation metrics that require attention.
                    </p>
                    <p>
                        <strong>Performance Gap Impact:</strong> Bringing all suppliers to target performance levels could 
                        yield approximately ${potential_gain}M in value through reduced quality issues, improved delivery reliability,
                        and increased operational efficiency.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        else:
            # Generic performance analysis for other categories
            st.info(f"Displaying standard performance analysis for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Create generic performance data
            suppliers = ["Supplier A", "Supplier B", "Supplier C", "Supplier D", "Supplier E"]
            metrics = ["Quality", "Delivery", "Cost", "Innovation", "Sustainability"]
            
            # Generate random performance data
            performance_data = []
            
            for supplier in suppliers:
                for metric in metrics:
                    performance_data.append({
                        "Supplier": supplier,
                        "Metric": metric,
                        "Score": np.random.randint(60, 95)
                    })
            
            # Create dataframe
            perf_df = pd.DataFrame(performance_data)
            
            # Create a heatmap
            perf_wide = perf_df.pivot(index="Supplier", columns="Metric", values="Score")
            
            fig = px.imshow(
                perf_wide,
                text_auto=True,
                color_continuous_scale="Blues",
                title=f"{selected_category} Supplier Performance Heatmap"
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with risk_tab:
        st.markdown("### Supplier Risk Assessment")
        
        if selected_category == "Aviation":
            st.markdown(
                """
                <div style='margin-bottom: 1rem;'>
                This dashboard evaluates supplier risks across multiple dimensions to identify potential vulnerabilities
                in the supply chain and develop appropriate mitigation strategies.
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Risk summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                high_risk = len([s for s, d in aviation_suppliers.items() if d["risk"] == "High"])
                med_risk = len([s for s, d in aviation_suppliers.items() if d["risk"] == "Medium"])
                st.metric("Medium/High Risk Suppliers", f"{high_risk + med_risk}/{len(aviation_suppliers)}", delta=f"{-1}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                risk_exposure = round(sum(d["spend"] for s, d in aviation_suppliers.items() if d["risk"] == "Medium" or d["risk"] == "High") / 1000000, 1)
                total_spend = round(sum(d["spend"] for d in aviation_suppliers.values()) / 1000000, 1)
                st.metric("At-Risk Spend", f"${risk_exposure}M", delta=f"{-round(np.random.uniform(0.5, 2.5), 1)}M")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                single_source = 3  # Number of single-sourced components
                st.metric("Single-Source Components", f"{single_source}", delta=f"{-1}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Risk heatmap
            st.markdown("### Risk Heatmap by Category")
            
            # Create detailed risk data
            risk_categories = ["Financial", "Operational", "Geopolitical", "Regulatory", "Environmental"]
            suppliers_list = list(aviation_suppliers.keys())[:6]  # Top 6 suppliers
            
            risk_data = []
            
            for supplier in suppliers_list:
                base_risk = 2 if aviation_suppliers[supplier]["risk"] == "Low" else 5 if aviation_suppliers[supplier]["risk"] == "Medium" else 8
                
                for category in risk_categories:
                    # Add some variation by category
                    if category == "Financial":
                        # Higher for Rolls-Royce
                        adjustment = 2 if supplier == "Rolls-Royce" else 0
                    elif category == "Geopolitical":
                        # Higher for non-US suppliers
                        adjustment = 2 if supplier in ["Airbus", "Rolls-Royce", "Safran", "Thales Group"] else 0
                    elif category == "Environmental":
                        # Higher for engine manufacturers
                        adjustment = 2 if supplier in ["GE Aviation", "Rolls-Royce", "Pratt & Whitney"] else 0
                    else:
                        adjustment = 0
                    
                    # Add some randomness
                    risk_score = min(10, max(1, base_risk + adjustment + np.random.randint(-1, 2)))
                    
                    risk_data.append({
                        "Supplier": supplier,
                        "Risk Category": category,
                        "Risk Score": risk_score
                    })
            
            risk_df = pd.DataFrame(risk_data)
            
            # Create a heatmap
            risk_wide = risk_df.pivot(index="Supplier", columns="Risk Category", values="Risk Score")
            
            fig = px.imshow(
                risk_wide,
                text_auto=True,
                color_continuous_scale="RdYlGn_r",  # Red for high risk, green for low
                title="Risk Assessment Heatmap - Top Suppliers",
                labels=dict(x="Risk Category", y="Supplier", color="Risk Score")
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk by geography
            st.markdown("### Geographic Risk Exposure")
            
            # Create supplier geographic distribution data
            geo_data = {
                "North America": 45,
                "Europe": 35,
                "Asia Pacific": 15,
                "Latin America": 5
            }
            
            # Create region risk data
            region_risk = {
                "North America": 3,
                "Europe": 4,
                "Asia Pacific": 7,
                "Latin America": 6
            }
            
            # Combine for visualization
            geo_risk_data = []
            
            for region, spend_pct in geo_data.items():
                geo_risk_data.append({
                    "Region": region,
                    "Spend Percentage": spend_pct,
                    "Risk Score": region_risk[region]
                })
            
            geo_df = pd.DataFrame(geo_risk_data)
            
            # Create a bubble chart of geographic risk
            fig = px.scatter(
                geo_df,
                x="Risk Score",
                y="Spend Percentage",
                size="Spend Percentage",
                color="Region",
                text="Region",
                size_max=60,
                title="Geographic Risk Exposure"
            )
            
            # Update layout
            fig.update_layout(
                height=500,
                xaxis=dict(
                    title="Risk Score (1-10)",
                    range=[0, 10]
                ),
                yaxis=dict(
                    title="Spend Percentage (%)",
                    range=[0, 50]
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk mitigation strategies
            st.markdown("### Risk Mitigation Strategies")
            
            # Allow selection of risk category to focus on
            risk_category = st.selectbox(
                "Select Risk Category for Mitigation Strategies",
                risk_categories
            )
            
            # Display suppliers with highest risk in selected category
            high_risk_suppliers = risk_df[risk_df["Risk Category"] == risk_category].sort_values("Risk Score", ascending=False).head(3)
            
            st.markdown(f"##### Top Risk Suppliers for {risk_category} Risk")
            
            for _, supplier in high_risk_suppliers.iterrows():
                risk_color = "#10B981" if supplier["Risk Score"] <= 3 else "#F59E0B" if supplier["Risk Score"] <= 6 else "#EF4444"
                risk_label = "Low" if supplier["Risk Score"] <= 3 else "Medium" if supplier["Risk Score"] <= 6 else "High"
                
                st.markdown(
                    f"""
                    <div style="margin-bottom: 12px; padding: 12px; border-radius: 4px; background-color: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-weight: 600;">{supplier["Supplier"]}</div>
                            <div>
                                <span>Risk Score: {supplier["Risk Score"]}</span>
                                <span style="color: {risk_color}; font-weight: bold;">Level: {risk_label}</span>
                            </div>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            # Mitigation strategies based on risk category
            st.markdown(f"##### Risk Mitigation Strategies for {risk_category}")
            
            if risk_category == "Financial":
                st.markdown("""
                - Implement quarterly financial health assessments
                - Establish financial performance thresholds
                - Consider payment term adjustments for high-risk suppliers
                - Develop contingency plans for potential supplier financial distress
                - Implement invoice factoring or supply chain finance for critical suppliers
                """)
            elif risk_category == "Geopolitical":
                st.markdown("""
                - Diversify supply base across multiple regions
                - Implement geopolitical risk monitoring system
                - Develop contingency plans for trade disruptions
                - Increase safety stock for components from high-risk regions
                - Consider nearshoring or reshoring options for critical components
                """)
            elif risk_category == "Operational":
                st.markdown("""
                - Map multi-tier supply chain for critical components
                - Implement supply chain visibility tools
                - Develop dual or multi-sourcing strategy
                - Build strategic inventory buffers
                - Create supplier collaboration program for capacity planning
                """)
            elif risk_category == "Regulatory":
                st.markdown("""
                - Implement compliance monitoring program
                - Conduct regular compliance audits
                - Provide supplier training on regulatory requirements
                - Establish clear contract language on compliance expectations
                - Monitor regulatory changes in supplier regions
                """)
            elif risk_category == "Environmental":
                st.markdown("""
                - Enhance supplier sustainability management systems
                - Implement carbon footprint measurement and reduction goals
                - Conduct environmental impact assessments
                - Develop supplier sustainability certification requirements
                - Create collaborative ESG improvement programs
                """)
                
        else:
            # Generic risk analysis for other categories
            st.info(f"Displaying standard risk analysis for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Generate and display risk heatmap
            risk_data = generate_risk_data(selected_category)
            
            fig = px.imshow(
                risk_data,
                text_auto=True,
                color_continuous_scale="RdYlGn_r",
                title=f"{selected_category} Risk Heatmap"
            )
            
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
    
    with relationship_tab:
        st.markdown("### Supplier Relationship Management")
        
        if selected_category == "Aviation":
            st.markdown(
                """
                <div style='margin-bottom: 1rem;'>
                Strategic supplier relationship management drives value beyond traditional purchasing. This dashboard
                helps assess relationship quality, identify improvement opportunities, and develop collaborative strategies.
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Create relationship assessment data
            relationship_data = []
            
            for supplier, details in aviation_suppliers.items():
                # Generate relationship metrics that somewhat correlate with performance
                base = details["performance"]
                spend = details["spend"]
                
                # Only assess top suppliers
                if spend > 10000000:
                    tier = "Strategic"
                elif spend > 5000000:
                    tier = "Key"
                else:
                    tier = "Standard"
                
                # Generate relationship metrics
                communication = min(100, max(60, base + np.random.normal(-5, 5)))
                responsiveness = min(100, max(60, base + np.random.normal(-3, 7)))
                flexibility = min(100, max(60, base + np.random.normal(-8, 8)))
                innovation = min(100, max(50, base + np.random.normal(-10, 10)))
                collaboration = min(100, max(60, base + np.random.normal(-5, 5)))
                
                relationship_score = round((communication + responsiveness + flexibility + innovation + collaboration) / 5)
                
                relationship_data.append({
                    "Supplier": supplier,
                    "Tier": tier,
                    "Communication": communication,
                    "Responsiveness": responsiveness,
                    "Flexibility": flexibility,
                    "Innovation": innovation,
                    "Collaboration": collaboration,
                    "Overall Score": relationship_score
                })
            
            rel_df = pd.DataFrame(relationship_data)
            
            # Sort by Overall Score descending
            rel_df = rel_df.sort_values("Overall Score", ascending=False)
            
            # Relationship score metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                avg_score = round(rel_df["Overall Score"].mean(), 1)
                st.metric("Avg. Relationship Score", f"{avg_score}/100", delta=f"{round(np.random.uniform(-2, 4), 1)}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                strategic_count = len(rel_df[rel_df["Tier"] == "Strategic"])
                st.metric("Strategic Suppliers", f"{strategic_count}", delta=None)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                innovation_score = round(rel_df["Innovation"].mean(), 1)
                st.metric("Innovation Index", f"{innovation_score}/100", delta=f"{round(np.random.uniform(-0.5, 6), 1)}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Relationship radar chart for strategic suppliers
            st.markdown("### Strategic Supplier Relationship Assessment")
            
            # Filter to strategic suppliers
            strategic_suppliers = rel_df[rel_df["Tier"] == "Strategic"].reset_index(drop=True)
            
            # Create radar chart
            metrics = ["Communication", "Responsiveness", "Flexibility", "Innovation", "Collaboration"]
            
            fig = go.Figure()
            
            for i, row in strategic_suppliers.iterrows():
                supplier = row["Supplier"]
                values = [row[metric] for metric in metrics]
                
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],  # Close the loop
                    theta=metrics + [metrics[0]],  # Close the loop
                    fill='toself',
                    name=supplier
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[50, 100]
                    )
                ),
                title="Relationship Dimensions - Strategic Suppliers",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Relationship improvement opportunities
            st.markdown("### Relationship Improvement Opportunities")
            
            # Calculate dimensions with biggest gaps
            avg_by_dimension = rel_df[metrics].mean().reset_index()
            avg_by_dimension.columns = ["Dimension", "Average Score"]
            avg_by_dimension = avg_by_dimension.sort_values("Average Score")
            
            # Create bar chart of dimension averages
            fig = px.bar(
                avg_by_dimension,
                x="Dimension",
                y="Average Score",
                title="Relationship Dimensions - Average Scores",
                color="Average Score",
                color_continuous_scale="Blues"
            )
            
            fig.update_layout(
                height=400,
                yaxis=dict(range=[70, 100])
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Relationship improvement recommendations
            lowest_dimension = avg_by_dimension.iloc[0]["Dimension"]
            lowest_score = round(avg_by_dimension.iloc[0]["Average Score"], 1)
            highest_dimension = avg_by_dimension.iloc[-1]["Dimension"]
            highest_score = round(avg_by_dimension.iloc[-1]["Average Score"], 1)
            
            # Find supplier with biggest gap in lowest dimension
            gap_supplier = rel_df.loc[rel_df[lowest_dimension].idxmin()]["Supplier"]
            gap_score = round(rel_df.loc[rel_df[lowest_dimension].idxmin()][lowest_dimension], 1)
            
            st.markdown(
                f"""
                <div class="insight-card opportunity">
                    <h4>Relationship Enhancement Opportunities</h4>
                    <p>
                        <strong>Primary Focus Area:</strong> {lowest_dimension} (Avg: {lowest_score})
                        <br>
                        <strong>Key Strength:</strong> {highest_dimension} (Avg: {highest_score})
                    </p>
                    <p>
                        <strong>Specific Opportunity:</strong> {gap_supplier} shows significant gap in {lowest_dimension} ({gap_score})
                        despite strong performance in other areas. Targeted relationship improvement could yield substantive benefits.
                    </p>
                    <p>
                        <strong>Recommended Actions:</strong>
                        <ul>
                            <li>Conduct executive alignment sessions focused on {lowest_dimension.lower()}</li>
                            <li>Implement quarterly business reviews with top suppliers</li>
                            <li>Develop joint innovation roadmap with strategic suppliers</li>
                            <li>Create supplier relationship scorecard system</li>
                        </ul>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        else:
            # Generic relationship management for other categories
            st.info(f"Displaying standard relationship management for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Create generic relationship assessment data
            suppliers = ["Supplier A", "Supplier B", "Supplier C", "Supplier D", "Supplier E"]
            metrics = ["Communication", "Responsiveness", "Flexibility", "Innovation", "Support"]
            
            rel_data = []
            
            for supplier in suppliers:
                for metric in metrics:
                    rel_data.append({
                        "Supplier": supplier,
                        "Metric": metric,
                        "Score": np.random.randint(70, 95)
                    })
            
            rel_df = pd.DataFrame(rel_data)
            rel_wide = rel_df.pivot(index="Supplier", columns="Metric", values="Score")
            
            # Create heatmap
            fig = px.imshow(
                rel_wide,
                text_auto=True,
                color_continuous_scale="Blues",
                title=f"{selected_category} Supplier Relationship Assessment"
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Navigate to next step button
    if st.button("View Action Plan →", use_container_width=True):
        st.session_state.current_story_step = 3
        st.rerun()

# Strategic Planning Tab - Fourth step in the journey
# Action Plan Tab - Final step in the journey
with action_tab:
    st.session_state.visited_tabs.add("action")
    if "action" in st.session_state.visited_tabs and st.session_state.current_story_step < 3:
        st.session_state.current_story_step = 3
    
    st.markdown('<div class="sub-header">Strategic Category Planning</div>', unsafe_allow_html=True)
    
    # Introduction to strategy section
    st.markdown(
        """
        <div class="dashboard-summary">
            The strategic planning section integrates all insights from market trends, spend analysis, and 
            supplier assessment to develop a cohesive, actionable category strategy. This data-driven approach 
            ensures alignment with both procurement and business objectives.
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Create subtabs for strategy components
    summary_tab, opportunity_tab, action_tab, roadmap_tab = st.tabs([
        "Strategy Summary", "Opportunity Analysis", "Action Plan", "Implementation Roadmap"
    ])
    
    with summary_tab:
        st.markdown("### Category Strategy Summary")
        
        if selected_category == "Aviation":
            # Aviation strategy summary
            st.markdown(
                """
                <div style="margin-bottom: 1.5rem; padding: 1.5rem; background-color: white; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin-top: 0; color: #1E3A8A;">Aviation Category Strategy</h4>
                    <p style="margin-bottom: 1rem;">
                        Based on comprehensive analysis of market trends, supplier performance, and spend patterns, 
                        the recommended strategy for the Aviation category focuses on strategic partnerships with key 
                        suppliers, risk mitigation through diversification, and cost reduction through enhanced 
                        contract management.
                    </p>
                    <div style="display: flex; margin-bottom: 1rem;">
                        <div style="flex: 1; padding: 0.75rem; background-color: #EFF6FF; border-radius: 0.375rem; margin-right: 0.5rem;">
                            <h5 style="margin-top: 0; color: #1E3A8A;">Strategic Focus</h5>
                            <ul style="margin-bottom: 0; padding-left: 1.25rem;">
                                <li>Develop strategic partnerships with top 3 suppliers</li>
                                <li>Reduce single-source dependency for critical components</li>
                                <li>Optimize total cost of ownership across aviation spend</li>
                                <li>Drive sustainability initiatives with key suppliers</li>
                            </ul>
                        </div>
                        <div style="flex: 1; padding: 0.75rem; background-color: #ECFDF5; border-radius: 0.375rem; margin-left: 0.5rem;">
                            <h5 style="margin-top: 0; color: #065F46;">Expected Outcomes</h5>
                            <ul style="margin-bottom: 0; padding-left: 1.25rem;">
                                <li>7-10% cost reduction over 18 months</li>
                                <li>30% reduction in supply disruptions</li>
                                <li>15% improvement in supplier innovation contributions</li>
                                <li>20% reduction in carbon footprint by 2026</li>
                            </ul>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # SWOT Analysis
            st.markdown("### SWOT Analysis: Aviation Category")
            
            # Create two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    """
                    <div style="padding: 1rem; background-color: #ECFDF5; border-radius: 0.5rem; height: 100%;">
                        <h4 style="margin-top: 0; color: #065F46;">Strengths</h4>
                        <ul>
                            <li>Strong relationships with key suppliers (Airbus, Boeing)</li>
                            <li>High-quality, reliable supply base for critical components</li>
                            <li>Established compliance and quality assurance processes</li>
                            <li>Experienced category management team</li>
                            <li>Global sourcing capabilities with regional expertise</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown(
                    """
                    <div style="padding: 1rem; background-color: #FEF2F2; border-radius: 0.5rem; margin-top: 1rem; height: 100%;">
                        <h4 style="margin-top: 0; color: #991B1B;">Threats</h4>
                        <ul>
                            <li>Increasing geopolitical tensions affecting global supply chain</li>
                            <li>Rapid inflation in key raw materials (titanium, composites)</li>
                            <li>Emerging regulatory requirements (emissions, safety standards)</li>
                            <li>Increasing competition for limited supplier capacity</li>
                            <li>Currency fluctuations impacting international procurement</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    """
                    <div style="padding: 1rem; background-color: #FEF3C7; border-radius: 0.5rem; height: 100%;">
                        <h4 style="margin-top: 0; color: #92400E;">Weaknesses</h4>
                        <ul>
                            <li>High dependency on single sources for critical components</li>
                            <li>Limited leverage with larger suppliers due to spend fragmentation</li>
                            <li>Higher than industry average lead times for specialized parts</li>
                            <li>Insufficient visibility into sub-tier supplier network</li>
                            <li>Contract compliance gaps leading to price leakage</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown(
                    """
                    <div style="padding: 1rem; background-color: #EFF6FF; border-radius: 0.5rem; margin-top: 1rem; height: 100%;">
                        <h4 style="margin-top: 0; color: #1E3A8A;">Opportunities</h4>
                        <ul>
                            <li>Consolidate fragmented MRO spend across regions</li>
                            <li>Implement advanced analytics for predictive maintenance</li>
                            <li>Develop longer-term partnerships with strategic suppliers</li>
                            <li>Joint innovation initiatives with key technology providers</li>
                            <li>Standardization of components across aircraft fleet</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Strategic positioning
            st.markdown("### Category Strategic Positioning")
            
            # Create a 2x2 matrix chart for category positioning
            positioning_data = pd.DataFrame([
                {"x": 85, "y": 70, "Category": "Aviation", "Size": 30},
                {"x": 60, "y": 40, "Category": "Office Supplies", "Size": 10},
                {"x": 75, "y": 30, "Category": "IT Services", "Size": 20},
                {"x": 30, "y": 80, "Category": "Raw Materials", "Size": 25},
                {"x": 40, "y": 55, "Category": "Logistics", "Size": 15}
            ])
            
            fig = px.scatter(
                positioning_data,
                x="x",
                y="y",
                text="Category",
                size="Size",
                color="Category",
                color_discrete_sequence=px.colors.qualitative.Bold,
                size_max=40
            )
            
            # Add quadrant lines
            fig.add_hline(
                y=50,
                line_width=1,
                line_dash="dash",
                line_color="gray"
            )
            
            fig.add_vline(
                x=50,
                line_width=1,
                line_dash="dash",
                line_color="gray"
            )
            
            # Add quadrant labels
            fig.add_annotation(
                x=25, y=75,
                text="LEVERAGE<br>(Low Value, High Impact)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            fig.add_annotation(
                x=75, y=75,
                text="STRATEGIC<br>(High Value, High Impact)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            fig.add_annotation(
                x=25, y=25,
                text="NON-CRITICAL<br>(Low Value, Low Impact)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            fig.add_annotation(
                x=75, y=25,
                text="BOTTLENECK<br>(High Value, Low Impact)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            # Update layout
            fig.update_layout(
                title="Category Positioning Matrix",
                xaxis=dict(
                    title="Business Value",
                    range=[0, 100]
                ),
                yaxis=dict(
                    title="Supply Market Impact",
                    range=[0, 100]
                ),
                height=500
            )
            
            # Update text position
            fig.update_traces(
                textposition="top center"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Strategic implications
            st.markdown(
                """
                <div class="insight-card">
                    <h4>Strategic Implications</h4>
                    <p>
                        The Aviation category is positioned in the <strong>Strategic Quadrant</strong>, indicating both high business
                        value and high supply market impact. This positioning requires a balanced approach focused on:
                    </p>
                    <ul>
                        <li><strong>Strategic Partnerships:</strong> Develop collaborative relationships with key suppliers</li>
                        <li><strong>Risk Management:</strong> Implement robust risk mitigation and contingency planning</li>
                        <li><strong>Value Beyond Savings:</strong> Focus on total value including innovation, quality, and risk reduction</li>
                        <li><strong>Executive Alignment:</strong> Ensure close alignment between procurement and business leadership</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        else:
            # Generic strategy summary for other categories
            st.info(f"Displaying standard strategy summary for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Create simple 2x2 matrix for category positioning
            st.markdown("### Category Positioning")
            
            positioning_data = pd.DataFrame([
                {"x": np.random.randint(60, 90), "y": np.random.randint(60, 90), "Category": selected_category, "Size": 30},
                {"x": np.random.randint(20, 80), "y": np.random.randint(20, 80), "Category": "Category B", "Size": 15},
                {"x": np.random.randint(20, 80), "y": np.random.randint(20, 80), "Category": "Category C", "Size": 20},
                {"x": np.random.randint(20, 80), "y": np.random.randint(20, 80), "Category": "Category D", "Size": 25}
            ])
            
            fig = px.scatter(
                positioning_data,
                x="x",
                y="y",
                text="Category",
                size="Size",
                color="Category"
            )
            
            # Add quadrant lines
            fig.add_hline(y=50, line_dash="dash", line_color="gray")
            fig.add_vline(x=50, line_dash="dash", line_color="gray")
            
            fig.update_layout(
                title="Category Positioning Matrix",
                xaxis_title="Value",
                yaxis_title="Risk",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Generic SWOT
            st.markdown("### SWOT Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Strengths")
                st.markdown("- Established supplier relationships")
                st.markdown("- Good market knowledge")
                st.markdown("- Effective category management")
                
                st.markdown("#### Weaknesses")
                st.markdown("- Limited supplier base")
                st.markdown("- Price volatility")
                st.markdown("- Contract compliance issues")
            
            with col2:
                st.markdown("#### Opportunities")
                st.markdown("- Consolidation potential")
                st.markdown("- New technology adoption")
                st.markdown("- Process standardization")
                
                st.markdown("#### Threats")
                st.markdown("- Market fluctuations")
                st.markdown("- Supply constraints")
                st.markdown("- Regulatory changes")
    
    with opportunity_tab:
        st.markdown("### Opportunity Analysis")
        
        if selected_category == "Aviation":
            # Create opportunity waterfall chart
            st.markdown(
                """
                <div style="margin-bottom: 1rem;">
                The opportunity analysis quantifies potential savings and value improvement areas across 
                the aviation category. This analysis serves as the foundation for developing targeted initiatives
                and prioritizing actions.
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Create waterfall chart data
            waterfall_data = {
                "Opportunity": [
                    "Current Spend", 
                    "Supplier Consolidation", 
                    "Specification Optimization",
                    "Contract Compliance", 
                    "Demand Management",
                    "Payment Terms",
                    "Target Spend"
                ],
                "Value": [146000000, -8760000, -5110000, -4380000, -5840000, -1460000, 120450000],
                "Type": ["total", "relative", "relative", "relative", "relative", "relative", "total"]
            }
            
            df_waterfall = pd.DataFrame(waterfall_data)
            
            # Calculate percentages for relative changes
            total_current = df_waterfall.loc[0, "Value"]
            for i in range(1, len(df_waterfall) - 1):
                df_waterfall.loc[i, "Percentage"] = abs(df_waterfall.loc[i, "Value"]) / total_current * 100
            
            # Create waterfall chart
            fig = go.Figure(go.Waterfall(
                name="Savings Waterfall",
                orientation="v",
                measure=df_waterfall["Type"],
                x=df_waterfall["Opportunity"],
                y=df_waterfall["Value"],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                decreasing={"marker": {"color": "#10B981"}},
                increasing={"marker": {"color": "#EF4444"}},
                totals={"marker": {"color": "#3B82F6"}},
                text=[f"${abs(val):,.0f}" if i > 0 and i < len(df_waterfall) - 1 else f"${abs(val):,.0f}" for i, val in enumerate(df_waterfall["Value"])],
                textposition="outside"
            ))
            
            fig.update_layout(
                title="Aviation Category Savings Opportunity Waterfall",
                showlegend=False,
                height=500,
                yaxis=dict(
                    title="Annual Spend ($)",
                    tickformat="$,.0f"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Opportunity breakdown table
            st.markdown("### Opportunity Breakdown & Implementation Complexity")
            
            # Create opportunity table
            opportunities = [
                {
                    "Opportunity": "Supplier Consolidation",
                    "Description": "Consolidate MRO suppliers from 12 to 5 strategic partners across regions",
                    "Annual Value": "$8.76M",
                    "Value Driver": "Volume leverage, reduced administrative costs",
                    "Implementation": "Medium",
                    "Timeframe": "9-12 months",
                    "Class": "opportunity"
                },
                {
                    "Opportunity": "Specification Optimization",
                    "Description": "Standardize component specifications across fleet, reducing unique parts by 25%",
                    "Annual Value": "$5.11M",
                    "Value Driver": "Reduced complexity, inventory optimization",
                    "Implementation": "High",
                    "Timeframe": "12-18 months",
                    "Class": "opportunity"
                },
                {
                    "Opportunity": "Contract Compliance",
                    "Description": "Implement robust contract management to prevent off-contract buying and price leakage",
                    "Annual Value": "$4.38M",
                    "Value Driver": "Price discipline, discount capture",
                    "Implementation": "Low",
                    "Timeframe": "3-6 months",
                    "Class": "opportunity"
                },
                {
                    "Opportunity": "Demand Management",
                    "Description": "Optimize maintenance schedules and inventory strategies to reduce overall consumption",
                    "Annual Value": "$5.84M",
                    "Value Driver": "Reduced consumption, inventory optimization",
                    "Implementation": "Medium",
                    "Timeframe": "6-9 months",
                    "Class": "opportunity"
                },
                {
                    "Opportunity": "Payment Terms",
                    "Description": "Standardize payment terms to Net 60 across suppliers (currently averaging Net 35)",
                    "Annual Value": "$1.46M",
                    "Value Driver": "Working capital improvement",
                    "Implementation": "Low",
                    "Timeframe": "3-6 months", 
                    "Class": "opportunity"
                }
            ]
            
            # Display opportunities
            for opp in opportunities:
                implementation_color = "#10B981" if opp["Implementation"] == "Low" else "#F59E0B" if opp["Implementation"] == "Medium" else "#EF4444"
                
                st.markdown(
                    f"""
                    <div class="insight-card {opp['Class']}">
                        <div style="display: flex; justify-content: space-between; align-items: top; margin-bottom: 0.5rem;">
                            <h4 style="margin: 0;">{opp['Opportunity']}</h4>
                            <div style="text-align: right;">
                                <div style="font-size: 1.25rem; font-weight: 600; color: #10B981;">{opp['Annual Value']}</div>
                                <div style="font-size: 0.8rem; color: #6B7280;">Annual Value</div>
                            </div>
                        </div>
                        <p>{opp['Description']}</p>
                        <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                            <div>
                                <strong>Value Driver:</strong> {opp['Value Driver']}
                            </div>
                            <div>
                                <strong>Implementation:</strong> <span style="color: {implementation_color};">{opp['Implementation']}</span>
                            </div>
                            <div>
                                <strong>Timeframe:</strong> {opp['Timeframe']}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Opportunity prioritization matrix
            st.markdown("### Opportunity Prioritization")
            
            # Create prioritization data
            prioritization_data = []
            
            for i, opp in enumerate(opportunities):
                # Map implementation complexity to numeric value
                complexity = 80 if opp["Implementation"] == "Low" else 50 if opp["Implementation"] == "Medium" else 20
                
                # Extract numeric value from Annual Value string
                value_str = opp["Annual Value"].replace("$", "").replace("M", "")
                value = float(value_str)
                
                # Normalize value to 0-100 scale
                max_value = 10  # Assuming max opportunity is $10M
                normalized_value = min(100, (value / max_value) * 100)
                
                prioritization_data.append({
                    "Opportunity": opp["Opportunity"],
                    "Ease of Implementation": complexity,
                    "Value": normalized_value,
                    "Annual Impact": opp["Annual Value"],
                    "Size": value * 5  # Size bubble based on value
                })
            
            df_priority = pd.DataFrame(prioritization_data)
            
            # Create bubble chart
            fig = px.scatter(
                df_priority,
                x="Value",
                y="Ease of Implementation",
                size="Size",
                color="Opportunity",
                text="Opportunity",
                hover_name="Opportunity",
                color_discrete_sequence=px.colors.qualitative.Bold,
                size_max=60,
                custom_data=["Annual Impact"]
            )
            
            # Update hover template
            fig.update_traces(
                hovertemplate="<b>%{hovertext}</b><br>Value: %{x:.1f}<br>Ease: %{y:.1f}<br>Annual Impact: %{customdata[0]}"
            )
            
            # Add quadrant lines
            fig.add_hline(
                y=50,
                line_width=1,
                line_dash="dash",
                line_color="gray"
            )
            
            fig.add_vline(
                x=50,
                line_width=1,
                line_dash="dash",
                line_color="gray"
            )
            
            # Add quadrant labels
            fig.add_annotation(
                x=25, y=75,
                text="QUICK WINS<br>(Low Value, Easy)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            fig.add_annotation(
                x=75, y=75,
                text="MAJOR PROJECTS<br>(High Value, Easy)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            fig.add_annotation(
                x=25, y=25,
                text="DEPRIORITIZE<br>(Low Value, Difficult)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            fig.add_annotation(
                x=75, y=25,
                text="STRATEGIC INITIATIVES<br>(High Value, Difficult)",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            # Update layout
            fig.update_layout(
                title="Opportunity Prioritization Matrix",
                xaxis=dict(
                    title="Value Potential",
                    range=[0, 100]
                ),
                yaxis=dict(
                    title="Ease of Implementation",
                    range=[0, 100]
                ),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Prioritization insights
            st.markdown(
                """
                <div class="insight-card opportunity">
                    <h4>Opportunity Prioritization Insights</h4>
                    <p>
                        <strong>Recommended Focus Areas:</strong>
                    </p>
                    <ol>
                        <li><strong>Contract Compliance & Payment Terms:</strong> Address these quick wins first to generate early momentum and value</li>
                        <li><strong>Supplier Consolidation & Demand Management:</strong> Initiate these major projects to capture significant value with moderate complexity</li>
                        <li><strong>Specification Optimization:</strong> Plan this strategic initiative for long-term value, while recognizing implementation challenges</li>
                    </ol>
                    <p>
                        This phased approach balances quick wins with strategic initiatives, maintaining continuous value delivery while building toward transformational change.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        else:
            # Generic opportunity analysis for other categories
            st.info(f"Displaying standard opportunity analysis for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Create simple opportunity chart
            opportunity_data = pd.DataFrame([
                {"Opportunity": "Supplier Consolidation", "Value": np.random.randint(30, 70)},
                {"Opportunity": "Specification Optimization", "Value": np.random.randint(30, 70)},
                {"Opportunity": "Contract Compliance", "Value": np.random.randint(30, 70)},
                {"Opportunity": "Demand Management", "Value": np.random.randint(30, 70)},
                {"Opportunity": "Payment Terms", "Value": np.random.randint(30, 70)}
            ])
            
            fig = px.bar(
                opportunity_data,
                x="Opportunity",
                y="Value",
                title=f"{selected_category} Opportunity Analysis",
                color="Opportunity"
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with action_tab:
        st.markdown("### Strategic Action Plan")
        
        if selected_category == "Aviation":
            # Aviation action plan
            st.markdown(
                """
                <div style="margin-bottom: 1rem;">
                The strategic action plan translates opportunities into concrete initiatives with clear ownership, 
                timelines, and success metrics. This operational roadmap ensures effective execution of the category strategy.
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Create tabs for different strategic pillars
            pillar_tabs = st.tabs([
                "Cost Optimization", "Risk Mitigation", "Supplier Relationship", "Innovation & Sustainability"
            ])
            
            with pillar_tabs[0]:
                st.markdown("#### Cost Optimization Initiatives")
                
                cost_initiatives = [
                    {
                        "Initiative": "Global MRO Supplier Consolidation",
                        "Description": "Reduce MRO suppliers from 12 to 5 strategic partners through competitive RFP and transition plan",
                        "Owner": "Mark Chen, Category Manager",
                        "Timeline": "Q3 2025 - Q1 2026",
                        "Success Metrics": "8% cost reduction, 15% reduction in supplier management overhead",
                        "Status": "Planning",
                        "Priority": "High"
                    },
                    {
                        "Initiative": "Component Standardization Program",
                        "Description": "Standardize specifications for common components across fleet to reduce unique parts by 25%",
                        "Owner": "Sarah Kim, Technical Lead",
                        "Timeline": "Q3 2025 - Q3 2026",
                        "Success Metrics": "25% reduction in unique part numbers, $5.1M annual savings",
                        "Status": "Approved",
                        "Priority": "Medium"
                    },
                    {
                        "Initiative": "Contract Compliance Automation",
                        "Description": "Implement automated compliance monitoring system with real-time alerts for off-contract spending",
                        "Owner": "David Rodriguez, Procurement Systems",
                        "Timeline": "Q3 - Q4 2025",
                        "Success Metrics": "95% PO compliance, 3% reduction in invoice price variance",
                        "Status": "In Progress",
                        "Priority": "High"
                    }
                ]
                
                # Display initiatives
                for initiative in cost_initiatives:
                    status_color = "#10B981" if initiative["Status"] == "Completed" else "#F59E0B" if initiative["Status"] == "In Progress" else "#3B82F6" if initiative["Status"] == "Approved" else "#6B7280"
                    priority_color = "#EF4444" if initiative["Priority"] == "High" else "#F59E0B" if initiative["Priority"] == "Medium" else "#6B7280"
                    
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 1rem; padding: 1rem; background-color: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <h4 style="margin: 0;">{initiative['Initiative']}</h4>
                                <div>
                                    <span style="background-color: {status_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem;">{initiative['Status']}</span>
                                    <span style="background-color: {priority_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; margin-left: 0.5rem;">{initiative['Priority']}</span>
                                </div>
                            </div>
                            <p>{initiative['Description']}</p>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.5rem;">
                                <div><strong>Owner:</strong> {initiative['Owner']}</div>
                                <div><strong>Timeline:</strong> {initiative['Timeline']}</div>
                                <div style="grid-column: span 2;"><strong>Success Metrics:</strong> {initiative['Success Metrics']}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with pillar_tabs[1]:
                st.markdown("#### Risk Mitigation Initiatives")
                
                risk_initiatives = [
                    {
                        "Initiative": "Secondary Source Development",
                        "Description": "Develop secondary sources for top 10 critical single-source components",
                        "Owner": "Elena Martinez, Supply Risk Manager",
                        "Timeline": "Q3 2025 - Q2 2026",
                        "Success Metrics": "80% of critical components with qualified alternate sources",
                        "Status": "Planning",
                        "Priority": "Critical"
                    },
                    {
                        "Initiative": "Supply Chain Mapping",
                        "Description": "Map multi-tier supply chain for critical components to identify hidden risks",
                        "Owner": "Thomas Wang, Risk Analyst",
                        "Timeline": "Q3 - Q4 2025",
                        "Success Metrics": "100% visibility to Tier 2 suppliers for critical components",
                        "Status": "Approved",
                        "Priority": "High"
                    },
                    {
                        "Initiative": "Geopolitical Risk Monitoring",
                        "Description": "Implement real-time geopolitical risk monitoring system with automated alerts",
                        "Owner": "Priya Sharma, Global Sourcing",
                        "Timeline": "Q4 2025",
                        "Success Metrics": "Zero supply disruptions due to unidentified geopolitical risks",
                        "Status": "Planning",
                        "Priority": "Medium"
                    }
                ]
                
                # Display initiatives
                for initiative in risk_initiatives:
                    status_color = "#10B981" if initiative["Status"] == "Completed" else "#F59E0B" if initiative["Status"] == "In Progress" else "#3B82F6" if initiative["Status"] == "Approved" else "#6B7280"
                    priority_color = "#7F1D1D" if initiative["Priority"] == "Critical" else "#EF4444" if initiative["Priority"] == "High" else "#F59E0B" if initiative["Priority"] == "Medium" else "#6B7280"
                    
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 1rem; padding: 1rem; background-color: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <h4 style="margin: 0;">{initiative['Initiative']}</h4>
                                <div>
                                    <span style="background-color: {status_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem;">{initiative['Status']}</span>
                                    <span style="background-color: {priority_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; margin-left: 0.5rem;">{initiative['Priority']}</span>
                                </div>
                            </div>
                            <p>{initiative['Description']}</p>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.5rem;">
                                <div><strong>Owner:</strong> {initiative['Owner']}</div>
                                <div><strong>Timeline:</strong> {initiative['Timeline']}</div>
                                <div style="grid-column: span 2;"><strong>Success Metrics:</strong> {initiative['Success Metrics']}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with pillar_tabs[2]:
                st.markdown("#### Supplier Relationship Initiatives")
                
                relationship_initiatives = [
                    {
                        "Initiative": "Strategic Supplier Summit",
                        "Description": "Conduct biannual strategic alignment summit with top 5 suppliers",
                        "Owner": "Michael Johnson, CPO",
                        "Timeline": "Q3 2025 (First Summit)",
                        "Success Metrics": "Alignment on 3-year innovation roadmap with each strategic supplier",
                        "Status": "Planning",
                        "Priority": "Medium"
                    },
                    {
                        "Initiative": "Supplier Performance Dashboard",
                        "Description": "Develop real-time supplier performance dashboard with scheduled review cadence",
                        "Owner": "Alex Chen, Analytics Lead",
                        "Timeline": "Q3 - Q4 2025",
                        "Success Metrics": "All strategic suppliers with quarterly performance reviews",
                        "Status": "In Progress",
                        "Priority": "High"
                    },
                    {
                        "Initiative": "Supplier Development Program",
                        "Description": "Launch structured improvement program for suppliers showing performance gaps",
                        "Owner": "Sophia Williams, Supplier Management",
                        "Timeline": "Q4 2025 - Q1 2026",
                        "Success Metrics": "10% average performance improvement for participating suppliers",
                        "Status": "Approved",
                        "Priority": "Medium"
                    }
                ]
                
                # Display initiatives
                for initiative in relationship_initiatives:
                    status_color = "#10B981" if initiative["Status"] == "Completed" else "#F59E0B" if initiative["Status"] == "In Progress" else "#3B82F6" if initiative["Status"] == "Approved" else "#6B7280"
                    priority_color = "#EF4444" if initiative["Priority"] == "High" else "#F59E0B" if initiative["Priority"] == "Medium" else "#6B7280"
                    
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 1rem; padding: 1rem; background-color: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <h4 style="margin: 0;">{initiative['Initiative']}</h4>
                                <div>
                                    <span style="background-color: {status_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem;">{initiative['Status']}</span>
                                    <span style="background-color: {priority_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; margin-left: 0.5rem;">{initiative['Priority']}</span>
                                </div>
                            </div>
                            <p>{initiative['Description']}</p>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.5rem;">
                                <div><strong>Owner:</strong> {initiative['Owner']}</div>
                                <div><strong>Timeline:</strong> {initiative['Timeline']}</div>
                                <div style="grid-column: span 2;"><strong>Success Metrics:</strong> {initiative['Success Metrics']}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with pillar_tabs[3]:
                st.markdown("#### Innovation & Sustainability Initiatives")
                
                innovation_initiatives = [
                    {
                        "Initiative": "Supplier Innovation Challenge",
                        "Description": "Launch innovation competition with top suppliers to address key business challenges",
                        "Owner": "Daniel Lee, Innovation Lead",
                        "Timeline": "Q4 2025",
                        "Success Metrics": "5 implemented innovations with measurable business impact",
                        "Status": "Planning",
                        "Priority": "Medium"
                    },
                    {
                        "Initiative": "Carbon Footprint Reduction",
                        "Description": "Develop joint carbon reduction roadmaps with top 10 suppliers",
                        "Owner": "Emma Garcia, Sustainability Manager",
                        "Timeline": "Q3 2025 - Q2 2026",
                        "Success Metrics": "20% reduction in category carbon footprint by 2026",
                        "Status": "Approved",
                        "Priority": "High"
                    },
                    {
                        "Initiative": "Circular Economy Pilot",
                        "Description": "Implement component reuse and recycling program with key suppliers",
                        "Owner": "Robert Thompson, Operations",
                        "Timeline": "Q1 - Q3 2026",
                        "Success Metrics": "30% increase in component reuse/recycling rate",
                        "Status": "Planning",
                        "Priority": "Medium"
                    }
                ]
                
                # Display initiatives
                for initiative in innovation_initiatives:
                    status_color = "#10B981" if initiative["Status"] == "Completed" else "#F59E0B" if initiative["Status"] == "In Progress" else "#3B82F6" if initiative["Status"] == "Approved" else "#6B7280"
                    priority_color = "#EF4444" if initiative["Priority"] == "High" else "#F59E0B" if initiative["Priority"] == "Medium" else "#6B7280"
                    
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 1rem; padding: 1rem; background-color: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <h4 style="margin: 0;">{initiative['Initiative']}</h4>
                                <div>
                                    <span style="background-color: {status_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem;">{initiative['Status']}</span>
                                    <span style="background-color: {priority_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; margin-left: 0.5rem;">{initiative['Priority']}</span>
                                </div>
                            </div>
                            <p>{initiative['Description']}</p>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.5rem;">
                                <div><strong>Owner:</strong> {initiative['Owner']}</div>
                                <div><strong>Timeline:</strong> {initiative['Timeline']}</div>
                                <div style="grid-column: span 2;"><strong>Success Metrics:</strong> {initiative['Success Metrics']}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
        else:
            # Generic action plan for other categories
            st.info(f"Displaying standard action plan for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Simple action plan
            st.markdown("#### Strategic Initiatives")
            
            initiatives = [
                "Supplier consolidation",
                "Contract renegotiation",
                "Process optimization",
                "Risk management",
                "Sustainability program"
            ]
            
            for i, initiative in enumerate(initiatives):
                st.markdown(f"{i+1}. {initiative}")
            
            # Simple timeline
            st.markdown("#### Implementation Timeline")
            
            timeline_data = pd.DataFrame([
                {"Task": "Supplier Analysis", "Start": "2025-06-01", "End": "2025-07-31", "Status": "Planning"},
                {"Task": "RFP Process", "Start": "2025-08-01", "End": "2025-10-31", "Status": "Planning"},
                {"Task": "Contract Negotiation", "Start": "2025-11-01", "End": "2025-12-31", "Status": "Planning"},
                {"Task": "Implementation", "Start": "2026-01-01", "End": "2026-03-31", "Status": "Planning"}
            ])
            
            st.dataframe(timeline_data)
    
    with roadmap_tab:
        st.markdown("### Implementation Roadmap")
        
        if selected_category == "Aviation":
            # Aviation implementation roadmap
            st.markdown(
                """
                <div style="margin-bottom: 1rem;">
                The implementation roadmap provides a timeline view of all initiatives, highlighting dependencies,
                resource requirements, and key milestones. This visual plan supports effective program management
                and stakeholder communication.
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Create a Gantt chart for implementation roadmap
            roadmap_data = []
            
            # Combine all initiatives
            all_initiatives = (
                [{"Initiative": i["Initiative"], "Timeline": i["Timeline"], "Priority": i["Priority"], "Pillar": "Cost Optimization", "Status": i["Status"]} for i in cost_initiatives] +
                [{"Initiative": i["Initiative"], "Timeline": i["Timeline"], "Priority": i["Priority"], "Pillar": "Risk Mitigation", "Status": i["Status"]} for i in risk_initiatives] +
                [{"Initiative": i["Initiative"], "Timeline": i["Timeline"], "Priority": i["Priority"], "Pillar": "Supplier Relationship", "Status": i["Status"]} for i in relationship_initiatives] +
                [{"Initiative": i["Initiative"], "Timeline": i["Timeline"], "Priority": i["Priority"], "Pillar": "Innovation & Sustainability", "Status": i["Status"]} for i in innovation_initiatives]
            )
            
            # Parse timeline into start and end dates
            for initiative in all_initiatives:
                timeline = initiative["Timeline"]
                
                # Parse the timeline string
                if "-" in timeline:
                    start_str, end_str = timeline.split("-")
                else:
                    start_str = end_str = timeline
                
                # Clean up and standardize
                start_str = start_str.strip()
                end_str = end_str.strip()
                
                # Convert to actual dates
                quarters = {
                    "Q1": "01-01",
                    "Q2": "04-01",
                    "Q3": "07-01",
                    "Q4": "10-01"
                }
                
                # Parse start date
                if "Q" in start_str:
                    q, year = start_str.split()
                    start_date = pd.Timestamp(f"{year}-{quarters[q]}")
                else:
                    # Default to start of year if only year provided
                    start_date = pd.Timestamp(f"{start_str}-01-01")
                
                # Parse end date
                if "Q" in end_str:
                    q, year = end_str.split()
                    # Set to end of quarter
                    if q == "Q1":
                        end_date = pd.Timestamp(f"{year}-03-31")
                    elif q == "Q2":
                        end_date = pd.Timestamp(f"{year}-06-30")
                    elif q == "Q3":
                        end_date = pd.Timestamp(f"{year}-09-30")
                    else:  # Q4
                        end_date = pd.Timestamp(f"{year}-12-31")
                else:
                    # Default to end of year if only year provided
                    end_date = pd.Timestamp(f"{end_str}-12-31")
                
                # Set color based on pillar
                color_map = {
                    "Cost Optimization": "#3B82F6",
                    "Risk Mitigation": "#EF4444",
                    "Supplier Relationship": "#F59E0B",
                    "Innovation & Sustainability": "#10B981"
                }
                
                # Set pattern based on status
                pattern_map = {
                    "Completed": "",
                    "In Progress": "",
                    "Approved": "\\",
                    "Planning": "x"
                }
                
                roadmap_data.append({
                    "Task": initiative["Initiative"],
                    "Pillar": initiative["Pillar"],
                    "Start": start_date,
                    "Finish": end_date,
                    "Priority": initiative["Priority"],
                    "Status": initiative["Status"],
                    "Color": color_map[initiative["Pillar"]],
                    "Pattern": pattern_map[initiative["Status"]]
                })
            
            # Create dataframe for the chart
            df_roadmap = pd.DataFrame(roadmap_data)
            
            # Sort by start date and pillar
            df_roadmap = df_roadmap.sort_values(["Start", "Pillar"])
            
            # Create Gantt chart using plotly
            fig = px.timeline(
                df_roadmap,
                x_start="Start",
                x_end="Finish",
                y="Task",
                color="Pillar",
                color_discrete_map={
                    "Cost Optimization": "#3B82F6",
                    "Risk Mitigation": "#EF4444",
                    "Supplier Relationship": "#F59E0B",
                    "Innovation & Sustainability": "#10B981"
                },
                hover_data=["Priority", "Status"]
            )
            
            # Update layout
            fig.update_layout(
                title="Aviation Category Strategy Implementation Roadmap",
                xaxis=dict(
                    title="Timeline",
                    tickformat="%b %Y"
                ),
                yaxis=dict(
                    title=""
                ),
                height=600,
                legend_title="Strategic Pillar"
            )
            
            # Reverse y-axis to show tasks from top to bottom in chronological order
            fig.update_yaxes(autorange="reversed")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Implementation summary and next steps
            st.markdown("### Implementation Summary & Next Steps")
            
            # Calculate metrics
            total_initiatives = len(df_roadmap)
            in_progress = len(df_roadmap[df_roadmap["Status"] == "In Progress"])
            planning = len(df_roadmap[df_roadmap["Status"] == "Planning"])
            approved = len(df_roadmap[df_roadmap["Status"] == "Approved"])
            completed = len(df_roadmap[df_roadmap["Status"] == "Completed"])
            
            critical_initiatives = len(df_roadmap[df_roadmap["Priority"] == "Critical"])
            high_priority = len(df_roadmap[df_roadmap["Priority"] == "High"])
            
            # Display implementation metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Total Initiatives", total_initiatives)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("In Progress", in_progress, delta=f"{in_progress}/{total_initiatives}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Critical/High Priority", f"{critical_initiatives + high_priority}", delta=f"{critical_initiatives + high_priority}/{total_initiatives}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                earliest_start = df_roadmap["Start"].min().strftime("%b %Y")
                latest_end = df_roadmap["Finish"].max().strftime("%b %Y")
                st.metric("Timeline", f"{earliest_start} - {latest_end}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Next steps
            st.markdown(
                """
                <div class="insight-card">
                    <h4>Immediate Next Steps</h4>
                    <ol>
                        <li><strong>Strategic Alignment:</strong> Review and finalize strategy with executive leadership (Due: June 15, 2025)</li>
                        <li><strong>Resource Allocation:</strong> Secure budget and resources for Q3 2025 initiatives (Due: June 30, 2025)</li>
                        <li><strong>Initiative Kickoff:</strong> Launch first wave of initiatives with detailed project plans (Due: July 15, 2025)</li>
                        <li><strong>Governance Setup:</strong> Establish program governance and regular review cadence (Due: July 31, 2025)</li>
                    </ol>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Success metrics and KPIs
            st.markdown("### Success Metrics & Key Performance Indicators")
            
            # Create KPI tracking framework
            kpis = [
                {
                    "Metric": "Cost Savings",
                    "Baseline": "$146M Annual Spend",
                    "Target": "$120.5M Annual Spend (-17.5%)",
                    "Timeline": "18 months",
                    "Tracking": "Monthly",
                    "Category": "Financial"
                },
                {
                    "Metric": "Supplier Consolidation",
                    "Baseline": "12 MRO Suppliers",
                    "Target": "5 Strategic Partners",
                    "Timeline": "12 months",
                    "Tracking": "Quarterly",
                    "Category": "Operational"
                },
                {
                    "Metric": "Secondary Source Coverage",
                    "Baseline": "40% of Critical Components",
                    "Target": "80% of Critical Components",
                    "Timeline": "12 months",
                    "Tracking": "Quarterly",
                    "Category": "Risk"
                },
                {
                    "Metric": "Innovation Contribution",
                    "Baseline": "3 Supplier Innovations Annually",
                    "Target": "10+ Implemented Innovations Annually",
                    "Timeline": "24 months",
                    "Tracking": "Quarterly",
                    "Category": "Strategic"
                },
                {
                    "Metric": "Carbon Footprint",
                    "Baseline": "Current Emissions Baseline",
                    "Target": "20% Reduction",
                    "Timeline": "24 months",
                    "Tracking": "Quarterly",
                    "Category": "Sustainability"
                }
            ]
            
            # Display KPIs in an organized table
            for kpi in kpis:
                category_color = "#3B82F6" if kpi["Category"] == "Financial" else "#F59E0B" if kpi["Category"] == "Operational" else "#EF4444" if kpi["Category"] == "Risk" else "#10B981" if kpi["Category"] == "Sustainability" else "#6B7280"
                
                st.markdown(
                    f"""
                    <div style="margin-bottom: 1rem; padding: 1rem; background-color: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <h4 style="margin: 0;">{kpi['Metric']}</h4>
                            <span style="background-color: {category_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem;">{kpi['Category']}</span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                            <div><strong>Baseline:</strong> {kpi['Baseline']}</div>
                            <div><strong>Target:</strong> {kpi['Target']}</div>
                            <div><strong>Timeline:</strong> {kpi['Timeline']}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
        else:
            # Generic implementation roadmap for other categories
            st.info(f"Displaying standard implementation roadmap for {selected_category} category. Select 'Aviation' for detailed demonstration.")
            
            # Simple roadmap
            roadmap_data = pd.DataFrame([
                {"Task": "Market Analysis", "Start": "2025-06-01", "Finish": "2025-07-31", "Category": "Analysis"},
                {"Task": "Supplier Assessment", "Start": "2025-07-01", "Finish": "2025-08-31", "Category": "Analysis"},
                {"Task": "Strategy Development", "Start": "2025-08-15", "Finish": "2025-09-30", "Category": "Planning"},
                {"Task": "Stakeholder Alignment", "Start": "2025-10-01", "Finish": "2025-10-31", "Category": "Planning"},
                {"Task": "Supplier Negotiations", "Start": "2025-11-01", "Finish": "2025-12-31", "Category": "Execution"},
                {"Task": "Implementation", "Start": "2026-01-01", "Finish": "2026-03-31", "Category": "Execution"}
            ])
            
            # Convert date strings to datetime
            roadmap_data["Start"] = pd.to_datetime(roadmap_data["Start"])
            roadmap_data["Finish"] = pd.to_datetime(roadmap_data["Finish"])
            
            # Create Gantt chart
            fig = px.timeline(
                roadmap_data,
                x_start="Start",
                x_end="Finish",
                y="Task",
                color="Category"
            )
            
            fig.update_layout(
                title=f"{selected_category} Implementation Roadmap",
                height=400
            )
            
            fig.update_yaxes(autorange="reversed")
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Call-to-action for next steps
    st.markdown(
        """
        <div class="recommendation-card">
            <h4>Recommended Next Actions</h4>
            <p>
                You've completed the strategic planning process for your category. Here are the recommended next steps:
            </p>
            <ol>
                <li>Review the key insights and opportunities identified in this analysis</li>
                <li>Share the category strategy with key stakeholders for alignment</li>
                <li>Prioritize initiatives and allocate resources for implementation</li>
                <li>Establish regular review cadence to track progress and adjust as needed</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.button("✓ Complete Category Intelligence Journey", use_container_width=True)

# Health Score Breakdown
st.markdown("### Health Score Components")
components = {
    "Supplier Performance": np.random.randint(50, 95),
    "Price Competitiveness": np.random.randint(50, 95),
    "Supply Risk": np.random.randint(50, 95),
    "Market Position": np.random.randint(50, 95),
    "Innovation": np.random.randint(50, 95),
    "Sustainability": np.random.randint(50, 95)
}

# Create a radar chart for health score components
categories = list(components.keys())
values = list(components.values())

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Category Health',
    line_color='#0066cc'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Category Health Trend
health_data = generate_category_health_data(selected_category)
fig = px.line(
    health_data, 
    x="Date", 
    y="Health Score", 
    title=f"{selected_category} Health Score Trend",
    markers=True
)
st.plotly_chart(fig, use_container_width=True)

# Category Intelligence from scraping
st.markdown("---")
st.markdown('<div class="sub-header">Latest Category Intelligence</div>', unsafe_allow_html=True)

# Get scraped news
news_items = simulated_web_scrape(selected_category)

# Create tabs for different news types
tab1, tab2, tab3 = st.tabs(["All News", "High Impact", "Price Changes"])

with tab1:
    for item in news_items:
        impact_color = "red" if item["impact"] == "High" else "orange" if item["impact"] == "Medium" else "green"
        st.markdown(
            f"""
            <div style="padding: 10px; margin-bottom: 10px; border-left: 5px solid {impact_color}; background-color: #f8f9fa;">
                <div style="font-weight: bold;">{item['title']}</div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #666; font-size: 0.8rem;">{item['source']}</span>
                    <span style="color: #666; font-size: 0.8rem;">{item['date']} ({item['days_ago']} days ago)</span>
                    <span style="color: {impact_color}; font-weight: bold; font-size: 0.8rem;">Impact: {item['impact']}</span>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

with tab2:
    high_impact_news = [item for item in news_items if item["impact"] == "High"]
    if high_impact_news:
        for item in high_impact_news:
            st.markdown(
                f"""
                <div style="padding: 10px; margin-bottom: 10px; border-left: 5px solid red; background-color: #f8f9fa;">
                    <div style="font-weight: bold;">{item['title']}</div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #666; font-size: 0.8rem;">{item['source']}</span>
                        <span style="color: #666; font-size: 0.8rem;">{item['date']} ({item['days_ago']} days ago)</span>
                        <span style="color: red; font-weight: bold; font-size: 0.8rem;">Impact: High</span>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.info("No high impact news found for this category in the selected time period.")

with tab3:
    price_news = [item for item in news_items if "price" in item["title"].lower()]
    if price_news:
        for item in price_news:
            impact_color = "red" if item["impact"] == "High" else "orange" if item["impact"] == "Medium" else "green"
            st.markdown(
                f"""
                <div style="padding: 10px; margin-bottom: 10px; border-left: 5px solid {impact_color}; background-color: #f8f9fa;">
                    <div style="font-weight: bold;">{item['title']}</div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #666; font-size: 0.8rem;">{item['source']}</span>
                        <span style="color: #666; font-size: 0.8rem;">{item['date']} ({item['days_ago']} days ago)</span>
                        <span style="color: {impact_color}; font-weight: bold; font-size: 0.8rem;">Impact: {item['impact']}</span>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.info("No price-related news found for this category in the selected time period.")

# Attractiveness vs Complexity Quadrant
st.markdown("---")
st.markdown('<div class="sub-header">Category Positioning</div>', unsafe_allow_html=True)

# Create quadrant data
attractiveness = np.random.randint(30, 80)
complexity = np.random.randint(30, 80)

# Create quadrant chart
fig = go.Figure()

# Add quadrant lines
fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, line=dict(color="Gray", width=1, dash="dash"))
fig.add_shape(type="line", x0=0, y0=50, x1=100, y1=50, line=dict(color="Gray", width=1, dash="dash"))

# Add quadrant labels
fig.add_annotation(x=25, y=75, text="Strategic<br>(High Value/Low Complexity)", showarrow=False, font=dict(size=10))
fig.add_annotation(x=75, y=75, text="Tactical<br>(High Value/High Complexity)", showarrow=False, font=dict(size=10))
fig.add_annotation(x=25, y=25, text="Non-Critical<br>(Low Value/Low Complexity)", showarrow=False, font=dict(size=10))
fig.add_annotation(x=75, y=25, text="Bottleneck<br>(Low Value/High Complexity)", showarrow=False, font=dict(size=10))

# Add category point
categories_with_spend = {
    "Electronics": np.random.randint(1000000, 5000000),
    "Raw Materials": np.random.randint(2000000, 8000000),
    "Packaging": np.random.randint(500000, 3000000),
    "Office Supplies": np.random.randint(100000, 800000),
    "IT Services": np.random.randint(1500000, 5000000),
    "Logistics": np.random.randint(1000000, 4000000),
    "Chemicals": np.random.randint(800000, 3500000),
    "Machinery": np.random.randint(2000000, 7000000)
}

# Random positions for all categories
category_positions = {}
for cat in categories:
    category_positions[cat] = {
        "attractiveness": np.random.randint(20, 80),
        "complexity": np.random.randint(20, 80)
    }

# Create data for plotting
quadrant_data = pd.DataFrame({
    "Category": categories,
    "Attractiveness": [category_positions[cat]["attractiveness"] for cat in categories],
    "Complexity": [category_positions[cat]["complexity"] for cat in categories],
    "Spend": [categories_with_spend[cat] for cat in categories]
})

# Highlight selected category
highlight = [1 if cat == selected_category else 0.3 for cat in categories]

# Plot points
fig.add_trace(go.Scatter(
    x=quadrant_data["Complexity"],
    y=quadrant_data["Attractiveness"],
    mode="markers+text",
    marker=dict(
        size=quadrant_data["Spend"] / 100000,
        color=["#0066cc" if cat == selected_category else "#999999" for cat in categories],
        opacity=highlight,
        line=dict(width=2, color="DarkSlateGrey")
    ),
    text=quadrant_data["Category"],
    textposition="top center",
    textfont=dict(
        color=["black" if cat == selected_category else "#999999" for cat in categories]
    ),
    name=""
))

# Update layout
fig.update_layout(
    title="Category Attractiveness vs. Complexity",
    xaxis=dict(
        title="Complexity",
        range=[0, 100]
    ),
    yaxis=dict(
        title="Attractiveness",
        range=[0, 100]
    ),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# Download executive briefing option
st.markdown("---")
st.markdown("### Executive Briefing")
col1, col2 = st.columns([3, 1])

with col1:
    st.write("Generate an executive briefing with the latest category intelligence, market trends, and strategic recommendations.")

with col2:
    st.download_button(
        label="Download Executive Briefing",
        data="This would be a generated executive briefing in PDF format.",
        file_name=f"{selected_category}_Executive_Briefing.pdf",
        mime="application/pdf"
    )
