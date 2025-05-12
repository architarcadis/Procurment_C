import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

from utils.data_generator import (
    generate_supplier_data,
    generate_risk_data
)

# Configure page
st.set_page_config(
    page_title="Strategy Generator - Procurement Command Center",
    page_icon="🧭",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0066cc;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    .strategy-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# 🧭 Strategy Generator")
    st.markdown("---")
    
    # Category selector
    categories = ["Electronics", "Raw Materials", "Packaging", "Office Supplies", 
                  "IT Services", "Logistics", "Chemicals", "Machinery"]
    selected_category = st.selectbox("Category", categories)
    
    # Strategy time horizon
    horizons = ["Short-term (0-12 months)", "Medium-term (1-3 years)", "Long-term (3-5 years)", "All horizons"]
    selected_horizon = st.selectbox("Time Horizon", horizons)
    
    # Strategy focus
    focuses = ["Cost Reduction", "Risk Mitigation", "Innovation", "Sustainability", "All focuses"]
    selected_focus = st.selectbox("Strategic Focus", focuses)
    
    # Region focus
    regions = ["Global", "North America", "Europe", "Asia Pacific", "Latin America"]
    selected_region = st.selectbox("Region", regions)
    
    # Strategy generation button
    generate_strategy = st.button("Generate Strategy", use_container_width=True)
    
    # Export options
    st.markdown("---")
    st.markdown("### Export Options")
    export_format = st.radio("Format", ["PDF", "PowerPoint", "Excel"])
    if st.button("Export Strategy", use_container_width=True):
        st.success(f"Strategy exported as {export_format}!")

# Main content
st.markdown('<div class="main-header">Strategy Generator</div>', unsafe_allow_html=True)
st.markdown(f"#### Selected Category: {selected_category} | Horizon: {selected_horizon} | Focus: {selected_focus}")

# Create tabs for strategy components
tab1, tab2, tab3, tab4 = st.tabs(["Strategy Overview", "Market Analysis", "Playbook Builder", "Stakeholder Map"])

with tab1:
    # Strategy overview section
    st.markdown("### Category Strategy Overview")
    
    # Auto-generate SWOT analysis
    st.markdown("#### SWOT Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="strategy-card" style="border-left: 5px solid green;">
            <h5>Strengths</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        # Generate strengths based on category
        strengths = {
            "Electronics": [
                "Strong established supplier relationships",
                "Technical expertise in component specifications",
                "Effective quality control processes",
                "Scale advantage in key components"
            ],
            "Raw Materials": [
                "Long-term supplier contracts securing supply",
                "Effective hedging strategies for price volatility",
                "Diverse supplier base across regions",
                "Strong commodity expertise within procurement team"
            ],
            "Packaging": [
                "Innovative sustainable packaging initiatives",
                "Standardized specifications across product lines",
                "Strategic partnerships with key suppliers",
                "Cost-effective design capabilities"
            ]
        }
        
        # Default strengths if category not found
        category_strengths = strengths.get(selected_category, [
            "Good supplier relationships",
            "Effective category management",
            "Clear specifications and requirements",
            "Competitive pricing"
        ])
        
        for strength in category_strengths:
            st.markdown(f"<li>{strength}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategy-card" style="border-left: 5px solid red;">
            <h5>Weaknesses</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        # Generate weaknesses based on category
        weaknesses = {
            "Electronics": [
                "Single-source dependencies for critical components",
                "Limited visibility into sub-tier suppliers",
                "Long lead times affecting flexibility",
                "Price volatility exposure"
            ],
            "Raw Materials": [
                "Exposure to commodity price fluctuations",
                "Geographic concentration of key suppliers",
                "Logistics complexity and cost",
                "Limited storage capacity for buffer stock"
            ],
            "Packaging": [
                "High costs relative to industry benchmarks",
                "Inconsistent supplier performance",
                "Limited sustainability metrics and tracking",
                "Fragmented supplier base"
            ]
        }
        
        # Default weaknesses if category not found
        category_weaknesses = weaknesses.get(selected_category, [
            "Fragmented supplier base",
            "Limited market intelligence",
            "Reactive rather than strategic approach",
            "Inconsistent supplier performance measurement"
        ])
        
        for weakness in category_weaknesses:
            st.markdown(f"<li>{weakness}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="strategy-card" style="border-left: 5px solid blue;">
            <h5>Opportunities</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        # Generate opportunities based on category
        opportunities = {
            "Electronics": [
                "Emerging alternative suppliers in new regions",
                "New technologies enabling component substitution",
                "Digital supply chain integration opportunities",
                "Industry partnerships for innovation"
            ],
            "Raw Materials": [
                "Emerging sustainable material alternatives",
                "Supplier consolidation for better leverage",
                "Advanced analytics for demand forecasting",
                "Vertical integration possibilities"
            ],
            "Packaging": [
                "Circular economy initiatives",
                "New bio-based material innovations",
                "Design optimization for material reduction",
                "Supplier co-innovation programs"
            ]
        }
        
        # Default opportunities if category not found
        category_opportunities = opportunities.get(selected_category, [
            "Supplier consolidation potential",
            "Technology enablement opportunities",
            "Process standardization",
            "New supplier market entrants"
        ])
        
        for opportunity in category_opportunities:
            st.markdown(f"<li>{opportunity}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategy-card" style="border-left: 5px solid orange;">
            <h5>Threats</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        # Generate threats based on category
        threats = {
            "Electronics": [
                "Supply constraints for critical components",
                "Geopolitical tensions affecting global supply chains",
                "Rapid technological obsolescence",
                "Increasing regulatory compliance requirements"
            ],
            "Raw Materials": [
                "Volatile commodity prices",
                "Environmental regulations impacting extraction",
                "Climate change effects on raw material sources",
                "Trade disputes and tariffs"
            ],
            "Packaging": [
                "Increasing environmental regulations",
                "Rising raw material costs",
                "New competitors with innovative solutions",
                "Consumer backlash against packaging waste"
            ]
        }
        
        # Default threats if category not found
        category_threats = threats.get(selected_category, [
            "Market volatility and uncertainty",
            "Supply chain disruptions",
            "Increasing regulatory pressures",
            "Emerging competitive threats"
        ])
        
        for threat in category_threats:
            st.markdown(f"<li>{threat}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # PESTLE Analysis
    st.markdown("#### PESTLE Analysis")
    
    # Create PESTLE elements based on category
    pestle = {
        "Political": [
            "Increasing trade tensions between major economies",
            "Policy shifts favoring domestic sourcing",
            "Regional political instability affecting supply routes",
            "Government incentives for sustainable practices"
        ],
        "Economic": [
            "Inflation pressures affecting input costs",
            "Currency volatility impacting global sourcing",
            "Changing labor costs across regions",
            "Economic slowdown affecting demand forecasts"
        ],
        "Social": [
            "Growing consumer focus on ethical sourcing",
            "Changing workforce demographics in manufacturing",
            "Social media scrutiny of supply chain practices",
            "Health and safety concerns in production"
        ],
        "Technological": [
            "Automation reducing production costs",
            "Digital platforms enabling new sourcing models",
            "IoT and blockchain for supply chain transparency",
            "3D printing disrupting traditional manufacturing"
        ],
        "Legal": [
            "Stricter environmental compliance requirements",
            "Changes in international trade agreements",
            "Intellectual property protection challenges",
            "Data protection regulations affecting information sharing"
        ],
        "Environmental": [
            "Carbon reduction targets affecting production",
            "Water scarcity impacting manufacturing processes",
            "Circular economy regulations",
            "Extreme weather events disrupting supply chains"
        ]
    }
    
    # Display PESTLE in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="strategy-card">
            <h5>Political</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        for item in pestle["Political"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategy-card">
            <h5>Technological</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        for item in pestle["Technological"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="strategy-card">
            <h5>Economic</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        for item in pestle["Economic"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategy-card">
            <h5>Legal</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        for item in pestle["Legal"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="strategy-card">
            <h5>Social</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        for item in pestle["Social"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategy-card">
            <h5>Environmental</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        for item in pestle["Environmental"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Porter's Five Forces
    st.markdown("#### Porter's Five Forces Analysis")
    
    # Create radar chart for Porter's Five Forces
    categories = ['Supplier Power', 'Buyer Power', 'Competitive Rivalry', 
                  'Threat of New Entrants', 'Threat of Substitutes']
    
    # Generate values based on category
    if selected_category == "Electronics":
        values = [8, 5, 7, 4, 6]
    elif selected_category == "Raw Materials":
        values = [7, 4, 5, 3, 4]
    elif selected_category == "Packaging":
        values = [5, 6, 7, 5, 6]
    elif selected_category == "IT Services":
        values = [4, 7, 8, 6, 5]
    else:
        # Random values for other categories
        values = [np.random.randint(3, 9) for _ in range(5)]
    
    # Create the radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Industry Forces',
        line_color='#0066cc'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Strategic recommendations
    st.markdown("### Strategic Recommendations")
    
    # Generate recommendations based on category and focus
    if selected_focus == "Cost Reduction" or selected_focus == "All focuses":
        st.markdown("""
        <div class="strategy-card" style="border-left: 5px solid #0066cc;">
            <h5>Cost Reduction Strategy</h5>
            <p><strong>Objective:</strong> Reduce total category spend by 8-12% over the next 18 months while maintaining or improving quality and service levels.</p>
            <p><strong>Key Initiatives:</strong></p>
            <ol>
                <li>Consolidate supplier base from current 15 suppliers to 8-10 strategic partners</li>
                <li>Implement should-cost modeling for top 5 spend items to drive fact-based negotiations</li>
                <li>Standardize specifications across business units to leverage economies of scale</li>
                <li>Develop global volume leverage through coordinated sourcing across regions</li>
            </ol>
            <p><strong>Expected Impact:</strong> $1.2M - $1.8M annual savings</p>
        </div>
        """, unsafe_allow_html=True)
    
    if selected_focus == "Risk Mitigation" or selected_focus == "All focuses":
        st.markdown("""
        <div class="strategy-card" style="border-left: 5px solid #0066cc;">
            <h5>Risk Mitigation Strategy</h5>
            <p><strong>Objective:</strong> Reduce supply disruption risk by 40% and improve supplier financial health monitoring.</p>
            <p><strong>Key Initiatives:</strong></p>
            <ol>
                <li>Implement dual-sourcing for critical components/materials</li>
                <li>Develop n-tier supply chain mapping for key suppliers</li>
                <li>Establish regular supplier financial health monitoring</li>
                <li>Create risk-adjusted inventory policy for vulnerable materials</li>
            </ol>
            <p><strong>Expected Impact:</strong> Reduced supply disruptions, enhanced business continuity</p>
        </div>
        """, unsafe_allow_html=True)
    
    if selected_focus == "Innovation" or selected_focus == "All focuses":
        st.markdown("""
        <div class="strategy-card" style="border-left: 5px solid #0066cc;">
            <h5>Innovation Strategy</h5>
            <p><strong>Objective:</strong> Accelerate new product development cycle by 20% through supplier-enabled innovation.</p>
            <p><strong>Key Initiatives:</strong></p>
            <ol>
                <li>Establish innovation partnerships with 3-5 strategic suppliers</li>
                <li>Implement quarterly technology roadmap sharing with key suppliers</li>
                <li>Develop supplier innovation portal for idea submission and tracking</li>
                <li>Create joint innovation KPIs and recognition program</li>
            </ol>
            <p><strong>Expected Impact:</strong> Faster time-to-market, competitive differentiation</p>
        </div>
        """, unsafe_allow_html=True)
    
    if selected_focus == "Sustainability" or selected_focus == "All focuses":
        st.markdown("""
        <div class="strategy-card" style="border-left: 5px solid #0066cc;">
            <h5>Sustainability Strategy</h5>
            <p><strong>Objective:</strong> Reduce category carbon footprint by 25% and eliminate non-sustainable materials by 2025.</p>
            <p><strong>Key Initiatives:</strong></p>
            <ol>
                <li>Implement supplier sustainability scorecards with improvement targets</li>
                <li>Transition to 100% recyclable or biodegradable alternatives where feasible</li>
                <li>Optimize logistics to reduce transportation emissions</li>
                <li>Partner with suppliers on circular economy initiatives</li>
            </ol>
            <p><strong>Expected Impact:</strong> Reduced environmental impact, improved brand reputation</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    # Market Analysis section
    st.markdown("### Market Analysis")
    
    # Market overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        market_size = np.random.randint(10, 100)
        st.metric("Market Size", f"${market_size}B", delta=f"{np.random.randint(2, 8)}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        growth_rate = np.random.uniform(1.5, 7.5)
        st.metric("Growth Rate (CAGR)", f"{growth_rate:.1f}%", delta=f"{np.random.uniform(-1, 2):.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        supplier_count = np.random.randint(50, 500)
        st.metric("Global Suppliers", f"{supplier_count}", delta=f"{np.random.randint(-20, 30)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        innovation_index = np.random.randint(30, 90)
        st.metric("Innovation Index", f"{innovation_index}/100", delta=f"{np.random.randint(-10, 15)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Market trend analysis
    st.markdown("### Market Trends")
    
    # Generate market trends
    market_trends = {
        "Price Trends": np.random.choice(["Rising", "Falling", "Stable", "Volatile"]),
        "Supply-Demand Balance": np.random.choice(["Supply Surplus", "Demand Exceeding Supply", "Balanced"]),
        "Supplier Landscape": np.random.choice(["Consolidating", "Fragmenting", "Stable", "New Entrants"]),
        "Technology Impact": np.random.choice(["Disruptive", "Incremental", "Minimal"]),
        "Sustainability Focus": np.random.choice(["High", "Medium", "Low", "Increasing"])
    }
    
    # Create a dataframe for the trends
    trend_df = pd.DataFrame({
        'Trend Category': list(market_trends.keys()),
        'Current State': list(market_trends.values()),
        'Impact': [np.random.randint(1, 10) for _ in range(len(market_trends))]
    })
    
    # Create horizontal bar chart
    fig = px.bar(
        trend_df,
        y='Trend Category',
        x='Impact',
        color='Current State',
        orientation='h',
        title="Market Trend Impact Analysis",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Market forecast
    st.markdown("### Market Forecast")
    
    # Generate forecast data
    years = list(range(datetime.now().year, datetime.now().year + 6))
    
    # Base market size with some growth
    base_market_size = market_size
    growth = growth_rate / 100
    
    # Generate market sizes with some randomness
    market_sizes = [base_market_size]
    for i in range(1, len(years)):
        next_size = market_sizes[-1] * (1 + growth + np.random.uniform(-0.01, 0.02))
        market_sizes.append(next_size)
    
    # Create a dataframe
    forecast_df = pd.DataFrame({
        'Year': years,
        'Market Size ($B)': market_sizes,
        'Scenario': ['Actual' if i == 0 else 'Forecast' for i in range(len(years))]
    })
    
    # Generate optimistic and pessimistic scenarios
    optimistic_df = forecast_df.copy()
    optimistic_df['Market Size ($B)'] = [
        size * (1 + 0.02 * i) for i, size in enumerate(optimistic_df['Market Size ($B)'])
    ]
    optimistic_df['Scenario'] = 'Optimistic'
    
    pessimistic_df = forecast_df.copy()
    pessimistic_df['Market Size ($B)'] = [
        size * (1 - 0.015 * i) for i, size in enumerate(pessimistic_df['Market Size ($B)'])
    ]
    pessimistic_df['Scenario'] = 'Pessimistic'
    
    # Combine the scenarios
    combined_df = pd.concat([forecast_df, optimistic_df, pessimistic_df])
    
    # Create line chart
    fig = px.line(
        combined_df,
        x='Year',
        y='Market Size ($B)',
        color='Scenario',
        title="Market Size Forecast",
        markers=True,
        color_discrete_map={
            'Actual': '#0066cc',
            'Forecast': '#009933',
            'Optimistic': '#00cc66',
            'Pessimistic': '#ff9900'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Competitive landscape
    st.markdown("### Competitive Landscape")
    
    # Generate competitive landscape data
    competitors = [
        "Company A", "Company B", "Company C", "Company D", 
        "Company E", "Company F", "Company G", "Company H"
    ]
    
    # Market share
    market_shares = np.random.dirichlet(np.ones(len(competitors)) * 2) * 100
    
    # Create dataframe
    competitor_df = pd.DataFrame({
        'Company': competitors,
        'Market Share (%)': market_shares,
        'Growth Rate (%)': [np.random.uniform(-5, 15) for _ in range(len(competitors))],
        'Innovation Score': [np.random.randint(50, 95) for _ in range(len(competitors))]
    })
    
    # Sort by market share
    competitor_df = competitor_df.sort_values('Market Share (%)', ascending=False)
    
    # Create a bubble chart
    fig = px.scatter(
        competitor_df,
        x='Growth Rate (%)',
        y='Innovation Score',
        size='Market Share (%)',
        color='Company',
        hover_name='Company',
        size_max=60,
        title="Competitive Positioning Matrix"
    )
    
    # Add quadrant lines
    fig.add_shape(type="line", x0=5, y0=0, x1=5, y1=100, line=dict(color="Gray", width=1, dash="dash"))
    fig.add_shape(type="line", x0=-5, y0=75, x1=15, y1=75, line=dict(color="Gray", width=1, dash="dash"))
    
    # Add quadrant labels
    fig.add_annotation(x=10, y=85, text="Leaders", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=0, y=85, text="Innovators", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=10, y=65, text="Growers", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=0, y=65, text="Laggards", showarrow=False, font=dict(size=12))
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Playbook builder section
    st.markdown("### Strategic Playbook Builder")
    
    # Create negotiation levers section
    st.markdown("#### Negotiation Levers")
    
    # Different levers based on category
    negotiation_levers = {
        "Electronics": [
            {"lever": "Volume Commitment", "impact": "High", "complexity": "Low", "timeframe": "Short-term"},
            {"lever": "Payment Terms Extension", "impact": "Medium", "complexity": "Low", "timeframe": "Short-term"},
            {"lever": "Specification Optimization", "impact": "High", "complexity": "Medium", "timeframe": "Medium-term"},
            {"lever": "Joint Product Development", "impact": "High", "complexity": "High", "timeframe": "Long-term"},
            {"lever": "Consignment Inventory", "impact": "Medium", "complexity": "Medium", "timeframe": "Medium-term"}
        ],
        "Raw Materials": [
            {"lever": "Index-based Pricing", "impact": "High", "complexity": "Medium", "timeframe": "Medium-term"},
            {"lever": "Hedging Strategies", "impact": "High", "complexity": "High", "timeframe": "Medium-term"},
            {"lever": "Volume Consolidation", "impact": "High", "complexity": "Medium", "timeframe": "Short-term"},
            {"lever": "Supply Security Premium", "impact": "Medium", "complexity": "Low", "timeframe": "Short-term"},
            {"lever": "Long-term Agreements", "impact": "High", "complexity": "Medium", "timeframe": "Long-term"}
        ]
    }
    
    # Default levers if category not found
    category_levers = negotiation_levers.get(selected_category, [
        {"lever": "Volume Commitment", "impact": "High", "complexity": "Low", "timeframe": "Short-term"},
        {"lever": "Payment Terms Extension", "impact": "Medium", "complexity": "Low", "timeframe": "Short-term"},
        {"lever": "Competitive Bidding", "impact": "High", "complexity": "Medium", "timeframe": "Short-term"},
        {"lever": "Specification Optimization", "impact": "High", "complexity": "Medium", "timeframe": "Medium-term"},
        {"lever": "Supplier Consolidation", "impact": "High", "complexity": "High", "timeframe": "Medium-term"}
    ])
    
    # Create a dataframe
    levers_df = pd.DataFrame(category_levers)
    
    # Convert impact and complexity to numeric for plotting
    impact_map = {"Low": 1, "Medium": 2, "High": 3}
    complexity_map = {"Low": 1, "Medium": 2, "High": 3}
    
    levers_df["Impact_Numeric"] = levers_df["impact"].map(impact_map)
    levers_df["Complexity_Numeric"] = levers_df["complexity"].map(complexity_map)
    
    # Create a scatter plot
    fig = px.scatter(
        levers_df,
        x="Complexity_Numeric",
        y="Impact_Numeric",
        text="lever",
        color="timeframe",
        title="Negotiation Lever Prioritization Matrix",
        labels={"Complexity_Numeric": "Implementation Complexity", "Impact_Numeric": "Potential Impact"},
        color_discrete_map={
            "Short-term": "#00cc66",
            "Medium-term": "#0066cc",
            "Long-term": "#ff9900"
        }
    )
    
    # Customize the plot
    fig.update_traces(textposition="top center", marker=dict(size=15))
    
    # Update axis to show text instead of numbers
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [1, 2, 3],
            ticktext = ['Low', 'Medium', 'High']
        ),
        yaxis = dict(
            tickmode = 'array',
            tickvals = [1, 2, 3],
            ticktext = ['Low', 'Medium', 'High']
        ),
        height = 500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Category plan builder
    st.markdown("#### Category Plan Timeline")
    
    # Create a Gantt chart for the category plan
    plan_items = [
        dict(Task="Supplier Assessment", Start=datetime.now(), Finish=datetime.now() + timedelta(days=30), Phase="Analysis"),
        dict(Task="Market Analysis", Start=datetime.now(), Finish=datetime.now() + timedelta(days=45), Phase="Analysis"),
        dict(Task="Strategy Development", Start=datetime.now() + timedelta(days=30), Finish=datetime.now() + timedelta(days=75), Phase="Planning"),
        dict(Task="RFP Process", Start=datetime.now() + timedelta(days=75), Finish=datetime.now() + timedelta(days=135), Phase="Execution"),
        dict(Task="Supplier Selection", Start=datetime.now() + timedelta(days=135), Finish=datetime.now() + timedelta(days=165), Phase="Execution"),
        dict(Task="Contract Negotiation", Start=datetime.now() + timedelta(days=165), Finish=datetime.now() + timedelta(days=205), Phase="Execution"),
        dict(Task="Implementation", Start=datetime.now() + timedelta(days=205), Finish=datetime.now() + timedelta(days=265), Phase="Implementation"),
        dict(Task="Performance Tracking", Start=datetime.now() + timedelta(days=265), Finish=datetime.now() + timedelta(days=365), Phase="Monitoring")
    ]
    
    # Convert to DataFrame
    plan_df = pd.DataFrame(plan_items)
    
    # Create a Gantt chart
    fig = px.timeline(
        plan_df, 
        x_start="Start", 
        x_end="Finish", 
        y="Task",
        color="Phase",
        title="Category Strategy Implementation Timeline",
        color_discrete_map={
            "Analysis": "#0066cc",
            "Planning": "#009933",
            "Execution": "#ff9900",
            "Implementation": "#cc0000",
            "Monitoring": "#9900cc"
        }
    )
    
    fig.update_layout(
        xaxis_title="Timeline",
        yaxis_title="",
        yaxis=dict(autorange="reversed")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Strategy cards for different time horizons
    st.markdown("#### Strategic Initiatives")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="strategy-card" style="border-top: 5px solid #00cc66;">
            <h5>Short-term (0-12 months)</h5>
            <ol>
                <li><strong>Quick Wins:</strong> Immediate cost savings through tactical negotiations</li>
                <li><strong>Data Cleansing:</strong> Standardize spend categorization</li>
                <li><strong>Supplier Performance:</strong> Implement basic KPI tracking</li>
                <li><strong>Low-hanging Fruit:</strong> Address obvious specification issues</li>
            </ol>
            <p><strong>Expected Impact:</strong> 3-5% cost reduction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="strategy-card" style="border-top: 5px solid #0066cc;">
            <h5>Medium-term (1-3 years)</h5>
            <ol>
                <li><strong>Strategic Sourcing:</strong> Comprehensive RFP and supplier rationalization</li>
                <li><strong>Value Engineering:</strong> Cross-functional specification optimization</li>
                <li><strong>Risk Management:</strong> Implement multi-tier supply chain visibility</li>
                <li><strong>Digital Enablement:</strong> Implement advanced analytics</li>
            </ol>
            <p><strong>Expected Impact:</strong> 7-12% cost reduction, 40% risk reduction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="strategy-card" style="border-top: 5px solid #ff9900;">
            <h5>Long-term (3-5 years)</h5>
            <ol>
                <li><strong>Supplier Innovation:</strong> Co-development partnerships</li>
                <li><strong>Category Transformation:</strong> New business models and approaches</li>
                <li><strong>Circular Economy:</strong> Close-loop supply chain development</li>
                <li><strong>Technology Integration:</strong> Fully digital, autonomous purchasing</li>
            </ol>
            <p><strong>Expected Impact:</strong> 15-20% total cost of ownership reduction, sustainable competitive advantage</p>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    # Stakeholder mapping section
    st.markdown("### Internal Stakeholder Map")
    
    # Generate stakeholder data
    stakeholders = [
        {"name": "Operations", "influence": np.random.randint(6, 10), "interest": np.random.randint(5, 10), "type": "Primary"},
        {"name": "R&D", "influence": np.random.randint(5, 9), "interest": np.random.randint(4, 9), "type": "Primary"},
        {"name": "Finance", "influence": np.random.randint(7, 10), "interest": np.random.randint(3, 7), "type": "Primary"},
        {"name": "Quality", "influence": np.random.randint(4, 8), "interest": np.random.randint(6, 10), "type": "Primary"},
        {"name": "Legal", "influence": np.random.randint(5, 8), "interest": np.random.randint(2, 5), "type": "Secondary"},
        {"name": "Marketing", "influence": np.random.randint(3, 6), "interest": np.random.randint(2, 6), "type": "Secondary"},
        {"name": "Sustainability", "influence": np.random.randint(2, 7), "interest": np.random.randint(7, 10), "type": "Secondary"},
        {"name": "IT", "influence": np.random.randint(3, 6), "interest": np.random.randint(3, 7), "type": "Secondary"}
    ]
    
    # Create DataFrame
    stakeholder_df = pd.DataFrame(stakeholders)
    
    # Create a bubble chart for stakeholder mapping
    fig = px.scatter(
        stakeholder_df,
        x="interest",
        y="influence",
        size=[40] * len(stakeholder_df),  # Fixed size for visibility
        color="type",
        text="name",
        title="Stakeholder Influence-Interest Matrix",
        color_discrete_map={"Primary": "#0066cc", "Secondary": "#ff9900"}
    )
    
    # Add quadrant lines
    fig.add_shape(type="line", x0=5, y0=0, x1=5, y1=10, line=dict(color="Gray", width=1, dash="dash"))
    fig.add_shape(type="line", x0=0, y0=5, x1=10, y1=5, line=dict(color="Gray", width=1, dash="dash"))
    
    # Add quadrant labels
    fig.add_annotation(x=7.5, y=7.5, text="Key Players<br>(Manage Closely)", showarrow=False, font=dict(size=10))
    fig.add_annotation(x=2.5, y=7.5, text="Keep Satisfied", showarrow=False, font=dict(size=10))
    fig.add_annotation(x=7.5, y=2.5, text="Keep Informed", showarrow=False, font=dict(size=10))
    fig.add_annotation(x=2.5, y=2.5, text="Monitor", showarrow=False, font=dict(size=10))
    
    # Customize the appearance
    fig.update_traces(textposition="top center")
    
    fig.update_layout(
        xaxis_title="Interest Level",
        yaxis_title="Influence Level",
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[0, 10]),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Stakeholder engagement strategies
    st.markdown("### Stakeholder Engagement Strategy")
    
    # Generate engagement strategies based on stakeholder position
    engagement_strategies = []
    
    for index, row in stakeholder_df.iterrows():
        strategy = {}
        strategy["stakeholder"] = row["name"]
        
        # Determine engagement approach based on quadrant
        if row["influence"] >= 5 and row["interest"] >= 5:
            strategy["approach"] = "Manage Closely"
            strategy["communication"] = "Regular face-to-face meetings, involve in decision-making"
            strategy["frequency"] = "Weekly/Bi-weekly"
        elif row["influence"] >= 5 and row["interest"] < 5:
            strategy["approach"] = "Keep Satisfied"
            strategy["communication"] = "Regular updates, focus on impact to their area"
            strategy["frequency"] = "Monthly"
        elif row["influence"] < 5 and row["interest"] >= 5:
            strategy["approach"] = "Keep Informed"
            strategy["communication"] = "Detailed information, seek input on relevant topics"
            strategy["frequency"] = "Monthly/Quarterly"
        else:
            strategy["approach"] = "Monitor"
            strategy["communication"] = "General updates, minimal detailed information"
            strategy["frequency"] = "Quarterly"
        
        engagement_strategies.append(strategy)
    
    # Create DataFrame
    engagement_df = pd.DataFrame(engagement_strategies)
    
    # Display as a table
    st.table(engagement_df)
    
    # Communication plan
    st.markdown("### Communication Plan")
    
    # Create tabs for different communication types
    comm_tab1, comm_tab2, comm_tab3 = st.tabs(["Regular Updates", "Decision Points", "Escalation Path"])
    
    with comm_tab1:
        st.markdown("#### Regular Communication Cadence")
        
        regular_comms = [
            {"audience": "Category Team", "purpose": "Progress tracking", "format": "Team meeting", "frequency": "Weekly", "owner": "Category Manager"},
            {"audience": "Key Stakeholders", "purpose": "Status update", "format": "Status report", "frequency": "Bi-weekly", "owner": "Category Manager"},
            {"audience": "Leadership", "purpose": "Executive update", "format": "Dashboard", "frequency": "Monthly", "owner": "Procurement Director"},
            {"audience": "Broader Organization", "purpose": "General awareness", "format": "Newsletter", "frequency": "Quarterly", "owner": "Communications Team"}
        ]
        
        st.table(pd.DataFrame(regular_comms))
    
    with comm_tab2:
        st.markdown("#### Critical Decision Points")
        
        decision_points = [
            {"decision": "Strategy approval", "stakeholders": "Leadership, Finance", "inputs_required": "Market analysis, business case", "timeline": "Month 1"},
            {"decision": "Supplier shortlist", "stakeholders": "Operations, Quality, R&D", "inputs_required": "RFI responses, supplier assessments", "timeline": "Month 3"},
            {"decision": "Final supplier selection", "stakeholders": "Cross-functional team", "inputs_required": "RFP results, site visit reports", "timeline": "Month 5"},
            {"decision": "Contract approval", "stakeholders": "Legal, Finance, Leadership", "inputs_required": "Negotiation results, risk assessment", "timeline": "Month 7"}
        ]
        
        st.table(pd.DataFrame(decision_points))
    
    with comm_tab3:
        st.markdown("#### Escalation Path")
        
        # Create a simple flowchart using markdown
        st.markdown("""
        ```
        Category Manager
                ↓
        Procurement Director
                ↓
        VP of Supply Chain
                ↓
        Chief Financial Officer
                ↓
        CEO/Executive Committee
        ```
        """)
        
        st.markdown("""
        #### Escalation Criteria
        
        1. **Financial Impact:**
           - Exceeds budget by more than 10%
           - Savings shortfall greater than 15%
        
        2. **Timeline Impact:**
           - Critical path delayed by more than 2 weeks
           - Overall timeline extension beyond 1 month
        
        3. **Risk Triggers:**
           - Supply disruption affecting production
           - Contract terms creating significant liability
           - Compliance or regulatory concerns
        
        4. **Stakeholder Conflicts:**
           - Unresolved cross-functional disagreements
           - Strategic direction conflicts
        """)
