import streamlit as st

# Configure the page - MUST BE THE FIRST STREAMLIT COMMAND after imports
st.set_page_config(
    page_title="Procurement Command Center",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import everything else
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import trafilatura
import requests
from utils.data_generator import (
    generate_category_health_data, 
    generate_supplier_data,
    generate_spend_data,
    generate_risk_data,
    generate_price_trend_data
)
from utils.forecasting import simple_forecast, advanced_forecast
from utils.scraper import simulated_web_scrape, get_commodity_prices
from utils.sidebar_manager import setup_sidebar
from pages.welcome import render_welcome_page
from pages.web_scraping_demo import render_web_scraping_demo

# Custom CSS to hide default Streamlit sidebar navigation links
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
.stDeployButton {display:none;}
footer {visibility: hidden;}
section[data-testid="stSidebar"] div.stSidebarNav {display: none;}
section[data-testid="stSidebar"] div:first-child button {display: none;}
section[data-testid="stSidebar"] li {display: none !important;}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.css-1544g2n {
    padding: 2rem 1rem;
}

div[data-testid="stMarkdownContainer"] h1 {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
}

div[data-testid="stMarkdownContainer"] h2, 
div[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Inter', sans-serif;
}

.card {
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.metric-card {
    text-align: center;
    background-color: white;
    border-left: 5px solid #ff6b18;
}

.stTabs {
    border-radius: 8px;
    overflow: hidden;
}

/* Override the Streamlit's default radio buttons */
div.st-bc {
    padding: 0 !important;
}

/* Improve button styling */
.stButton>button {
    border-radius: 6px;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #ff6b18;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add custom CSS with Arcadis orange theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Arcadis Orange Theme */
    :root {
        --arcadis-orange: #ff6b18;
        --arcadis-orange-light: #ff8c4d;
        --arcadis-orange-dark: #e55200;
        --arcadis-dark: #333333;
        --arcadis-gray: #f0f2f6;
        --arcadis-light: #ffffff;
        --arcadis-blue: #0077b6;
        --arcadis-green: #1e7145;
        --arcadis-red: #d42020;
    }
    
    /* Global Font Settings */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Headers */
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: var(--arcadis-orange);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #eee;
        text-shadow: 0px 1px 2px rgba(0,0,0,0.05);
    }
    
    .sub-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--arcadis-dark);
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--arcadis-orange-light);
        padding-bottom: 0.5rem;
    }
    
    h1, h2, h3, h4, h5 {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Metric containers - Tile Layout */
    .metric-container {
        background-color: var(--arcadis-light);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        border-left: 4px solid var(--arcadis-orange);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        border-left: 4px solid var(--arcadis-orange-dark);
    }
    
    /* Cards with better styling */
    .card {
        background-color: var(--arcadis-light);
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 1.2rem;
        border-top: 4px solid var(--arcadis-orange);
        transition: transform 0.2s ease-in-out;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    /* Custom button style with improved hover effects */
    .stButton>button {
        background-color: var(--arcadis-orange);
        color: white;
        border: none;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(255, 107, 24, 0.3);
    }
    
    .stButton>button:hover {
        background-color: var(--arcadis-orange-dark);
        box-shadow: 0 4px 10px rgba(255, 107, 24, 0.4);
        transform: translateY(-1px);
    }
    
    /* Custom styling for icons */
    .icon-container {
        color: var(--arcadis-orange);
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Custom tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--arcadis-orange);
        color: white;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background-color: var(--arcadis-orange);
    }
    
    /* Data tables */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
    }
    .dataframe thead {
        border-bottom: 2px solid var(--arcadis-orange);
    }
    .dataframe thead th {
        padding: 10px;
        background-color: var(--arcadis-gray);
    }
    .dataframe tbody tr:hover {
        background-color: rgba(255, 107, 24, 0.05);
    }
    
    /* Custom selectbox */
    .stSelectbox label, .stMultiselect label {
        color: var(--arcadis-dark);
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# Get sidebar selections
selected_category, selected_region, time_period, start_date, end_date = setup_sidebar()

# Create main tabs for application sections with Welcome tab
tabs = st.tabs([
    "Welcome",
    "Category Intelligence", 
    "AI Co-Pilot", 
    "Price Modeling", 
    "Supplier Intelligence", 
    "Strategy Generator",
    "Opportunity Engine",
    "Web Scraping Demo"
])

# Welcome tab
with tabs[0]:
    render_welcome_page()

# Category Intelligence tab
with tabs[1]:
    # Header
    st.markdown('<div class="main-header">Category Intelligence</div>', unsafe_allow_html=True)
    st.markdown(f"#### Selected Category: {selected_category} | Region: {', '.join(selected_region)} | Period: {time_period}")
    
    # Key metrics section
    st.markdown('<div class="sub-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate health score (0-100)
    health_score = np.random.randint(60, 95)
    health_color = "green" if health_score >= 80 else "orange" if health_score >= 70 else "red"
    
    with col1:
        st.metric("Category Health Score", f"{health_score}/100", delta=f"{np.random.randint(-5, 10)}%")
        st.markdown(f'<div style="text-align: center; color: {health_color}; font-weight: bold; margin-top: 5px;">{health_score}% HEALTHY</div>', unsafe_allow_html=True)
    
    with col2:
        st.metric("Spend to Date", f"${np.random.randint(2, 20)}M", delta=f"-{np.random.randint(2, 8)}%")
    
    with col3:
        st.metric("Active Suppliers", f"{np.random.randint(10, 100)}", delta=f"{np.random.randint(-3, 5)}")
    
    with col4:
        st.metric("Cost Savings Potential", f"${np.random.randint(1, 5)}M", delta=f"+{np.random.randint(5, 15)}%")
    
    # Layout for charts
    st.markdown("---")
    st.markdown('<div class="sub-header">Category Insights</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Category Health Trend
        health_data = generate_category_health_data(selected_category)
        fig = px.line(
            health_data, 
            x="Date", 
            y="Health Score", 
            title=f"{selected_category} Health Score Trend",
            markers=True
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk Heatmap
        st.subheader("Risk Assessment Heatmap")
        risk_data = generate_risk_data(selected_category)
        fig = px.imshow(
            risk_data,
            labels=dict(x="Risk Category", y="Supplier", color="Risk Level"),
            x=risk_data.columns,
            y=risk_data.index,
            color_continuous_scale=['#1e7145', '#ffeba5', '#ff6b18', '#d42020'],  # Green to yellow to orange to red
            aspect="auto",
            text_auto=True
        )
        fig.update_layout(
            height=400,
            coloraxis_colorbar=dict(
                title="Risk Level",
                thicknessmode="pixels", thickness=15,
                lenmode="pixels", len=300,
                yanchor="top", y=1,
                ticks="outside"
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            ),
            title_font=dict(size=16, color="#333333")
        )
        fig.update_traces(
            hovertemplate="<b>Supplier</b>: %{y}<br><b>Category</b>: %{x}<br><b>Risk Score</b>: %{z}<extra></extra>"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Spend Distribution
        st.subheader("Spend Distribution")
        spend_data = generate_spend_data(selected_category)
        fig = px.pie(
            spend_data, 
            values='Spend', 
            names='Supplier', 
            title=f"{selected_category} Spend Distribution by Supplier",
            color_discrete_sequence=px.colors.sequential.Oranges_r
        )
        fig.update_layout(
            height=300,
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=2))
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Supplier Quadrant
        st.subheader("Supplier Strategic Positioning")
        supplier_data = generate_supplier_data(selected_category)
        
        # Define colors for tiers with Arcadis orange palette
        tier_colors = {"Tier 1": "#ff6b18", "Tier 2": "#ff8c4d", "Tier 3": "#ffba8c"}
        
        fig = px.scatter(
            supplier_data,
            x="Risk",
            y="Performance",
            size="Spend",
            color="Tier",
            color_discrete_map=tier_colors,
            hover_name="Supplier",
            size_max=50,
            title="Supplier Quadrant Analysis",
            labels={"Risk": "Risk Score (Higher = More Risk)", 
                   "Performance": "Performance Score",
                   "Spend": "Annual Spend ($)"}
        )
        # Add quadrant lines
        fig.add_shape(type="line", x0=5, y0=0, x1=5, y1=10, line=dict(color="Gray", width=1, dash="dash"))
        fig.add_shape(type="line", x0=0, y0=5, x1=10, y1=5, line=dict(color="Gray", width=1, dash="dash"))
        
        # Quadrant fill colors (with transparency)
        fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, 
                     line=dict(width=0), fillcolor="rgba(0,176,80,0.1)")  # Strategic Partners - Green
        fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, 
                     line=dict(width=0), fillcolor="rgba(255,192,0,0.1)")  # Performance Focus - Yellow
        fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, 
                     line=dict(width=0), fillcolor="rgba(112,173,71,0.1)")  # Maintain - Light Green
        fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, 
                     line=dict(width=0), fillcolor="rgba(255,107,24,0.1)")  # Risk Mitigation - Orange
        
        # Add quadrant labels with better styling
        fig.add_annotation(x=2.5, y=7.5, text="<b>Strategic Partners</b>", showarrow=False, 
                          font=dict(size=12, color="#333333"), bgcolor="rgba(255,255,255,0.7)")
        fig.add_annotation(x=7.5, y=7.5, text="<b>Performance Focus</b>", showarrow=False, 
                          font=dict(size=12, color="#333333"), bgcolor="rgba(255,255,255,0.7)")
        fig.add_annotation(x=2.5, y=2.5, text="<b>Maintain</b>", showarrow=False, 
                          font=dict(size=12, color="#333333"), bgcolor="rgba(255,255,255,0.7)")
        fig.add_annotation(x=7.5, y=2.5, text="<b>Risk Mitigation</b>", showarrow=False, 
                          font=dict(size=12, color="#333333"), bgcolor="rgba(255,255,255,0.7)")
        
        fig.update_layout(
            height=400,
            title_font=dict(size=16, color="#333333"),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            ),
            margin=dict(l=30, r=30, t=50, b=50)
        )
        
        # Update axis ranges and style
        fig.update_xaxes(range=[0, 10], gridcolor='rgba(211,211,211,0.5)', zeroline=False)
        fig.update_yaxes(range=[0, 10], gridcolor='rgba(211,211,211,0.5)', zeroline=False)
        
        # Custom hover template
        hover_template = (
            "<b>%{hovertext}</b><br>" +
            "Risk: %{x:.1f}/10<br>" +
            "Performance: %{y:.1f}/10<br>" +
            "Annual Spend: $%{marker.size:,.0f}<br>" +
            "Tier: %{marker.color}"
        )
        fig.update_traces(hovertemplate=hover_template)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # News Feed and Opportunity Section
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="sub-header">Latest Category Intelligence</div>', unsafe_allow_html=True)
        
        # Generate some mock news items
        news_items = [
            {"title": f"Price increase announced for {selected_category}", "source": "Industry Journal", "date": "2 days ago", "impact": "High"},
            {"title": f"New supplier enters {selected_category} market", "source": "Market Watch", "date": "1 week ago", "impact": "Medium"},
            {"title": f"Supply chain disruption affecting {selected_category}", "source": "Supply Chain Weekly", "date": "2 weeks ago", "impact": "High"},
            {"title": f"Regulatory changes impacting {selected_category} sourcing", "source": "Regulatory Affairs", "date": "3 weeks ago", "impact": "Medium"},
        ]
        
        for item in news_items:
            impact_color = "red" if item["impact"] == "High" else "orange" if item["impact"] == "Medium" else "green"
            st.markdown(
                f"""
                <div style="padding: 10px; margin-bottom: 10px; border-left: 5px solid {impact_color}; background-color: #f8f9fa;">
                    <div style="font-weight: bold;">{item['title']}</div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #666; font-size: 0.8rem;">{item['source']}</span>
                        <span style="color: #666; font-size: 0.8rem;">{item['date']}</span>
                        <span style="color: {impact_color}; font-weight: bold; font-size: 0.8rem;">Impact: {item['impact']}</span>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    with col2:
        st.markdown('<div class="sub-header">Opportunities</div>', unsafe_allow_html=True)
        
        opportunities = [
            {"title": "Consolidate suppliers", "impact": "$250K savings", "effort": "Medium"},
            {"title": "Renegotiate contract terms", "impact": "$120K savings", "effort": "Low"},
            {"title": "Switch to alternative material", "impact": "$300K savings", "effort": "High"},
        ]
        
        for opp in opportunities:
            effort_color = "green" if opp["effort"] == "Low" else "orange" if opp["effort"] == "Medium" else "red"
            st.markdown(
                f"""
                <div style="padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f8f9fa;">
                    <div style="font-weight: bold;">{opp['title']}</div>
                    <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                        <span style="color: green; font-weight: bold;">{opp['impact']}</span>
                        <span style="color: {effort_color};">Effort: {opp['effort']}</span>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        st.button("Generate More Opportunities")

# This is the space where the former Category Intelligence tab was.
# Now we've merged Category Intelligence into the first tab (tabs[0])
            
# Price Modeling tab
with tabs[3]:
    st.markdown('<div class="main-header">Price Modeling & Forecasting</div>', unsafe_allow_html=True)
    st.markdown(f"#### Selected Category: {selected_category} | Region: {', '.join(selected_region)}")
    
    # Materials selection and price input
    st.markdown("### Price Analysis Tool")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # Material selection
        materials = []
        if selected_category == "Electronics":
            materials = ["Semiconductor Chips", "Circuit Boards", "Display Panels", "Electronic Components", "Memory Modules"]
        elif selected_category == "Raw Materials":
            materials = ["Steel", "Aluminum", "Copper", "Zinc", "Plastic Resin"]
        elif selected_category == "Packaging":
            materials = ["Cardboard", "Plastic Film", "Aluminum Foil", "Glass", "Paper"]
        elif selected_category == "Aviation":
            materials = ["Titanium", "Carbon Fiber", "Avionics", "Jet Fuel", "Aluminum Alloys"]
        elif selected_category == "Chemicals":
            materials = ["Industrial Chemicals", "Solvents", "Acids", "Polymers", "Specialty Chemicals"]
        else:
            materials = ["Material A", "Material B", "Material C", "Material D", "Material E"]
            
        selected_material = st.selectbox("Select Material", materials)
        
        # Time period selection
        forecast_period = st.slider("Forecast Period (Months)", min_value=3, max_value=24, value=12)
        
        # Show options for forecast models
        forecast_model = st.radio(
            "Forecast Model",
            ["Simple Trend", "Seasonal Model", "Advanced ML Model"]
        )
        
        # Add scenario planning options
        st.markdown("#### Scenario Planning")
        scenario = st.selectbox(
            "Market Scenario",
            ["Base Case", "High Inflation", "Supply Constraint", "Demand Surge", "Economic Downturn"]
        )
        
        # Generate forecast button
        forecast_button = st.button("Generate Price Forecast", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Historical price chart
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### Historical Price Trends")
        
        # Create placeholder for chart until user selects a material
        if not selected_material:
            st.warning("Please select a material to view price trends")
            price_data = pd.DataFrame()
        else:
            # Get historical price data for the selected material
            price_data = generate_price_trend_data(selected_category, selected_material)
            
            # Create line chart for historical prices
            fig = px.line(
                price_data,
                x="Date",
                y="Price",
                title=f"{selected_material} Price History",
                markers=True
            )
        
        fig.update_layout(
            height=300,
            hovermode="x unified",
            yaxis_title=f"Price (USD)",
            xaxis_title="",
            margin=dict(l=10, r=10, t=50, b=30),
            title_font=dict(size=16, color="#333333")
        )
        
        # Add trend line if we have data
        if selected_material and not price_data.empty and len(price_data) > 1:
            import numpy as np
            from scipy import stats
            
            x = np.array([(date - price_data['Date'].iloc[0]).days for date in price_data['Date']])
            y = price_data['Price'].values
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            trend_y = intercept + slope * x
            
            fig.add_trace(go.Scatter(
                x=price_data['Date'],
                y=trend_y,
                mode='lines',
                line=dict(color='rgba(255, 107, 24, 0.7)', width=2, dash='dot'),
                name='Trend Line'
            ))
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display forecast if button is clicked
    if forecast_button:
        st.markdown("### Price Forecast Analysis")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        with st.spinner("Generating price forecast..."):
            import time
            time.sleep(1.5)  # Simulate processing
            
            # Get historical price data for the selected material
            price_data = generate_price_trend_data(selected_category, selected_material)
            
            # Generate future dates for forecast
            last_date = price_data['Date'].iloc[-1]
            forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=30), periods=forecast_period, freq='M')
            
            # Generate forecast based on scenario
            last_price = price_data['Price'].iloc[-1]
            
            # Different scenarios affect the forecast
            if scenario == "Base Case":
                forecast_trend = 0.005  # 0.5% monthly change
                volatility = 0.02
            elif scenario == "High Inflation":
                forecast_trend = 0.015  # 1.5% monthly increase
                volatility = 0.03
            elif scenario == "Supply Constraint":
                forecast_trend = 0.02  # 2% monthly increase
                volatility = 0.04
            elif scenario == "Demand Surge":
                forecast_trend = 0.025  # 2.5% monthly increase
                volatility = 0.035
            elif scenario == "Economic Downturn":
                forecast_trend = -0.01  # 1% monthly decrease
                volatility = 0.03
            
            # Different forecast models affect the prediction
            if forecast_model == "Simple Trend":
                # Simple trend with noise
                forecast_prices = [last_price * (1 + forecast_trend * (i+1) + np.random.normal(0, volatility)) 
                                  for i in range(forecast_period)]
                confidence_high = [price * 1.1 for price in forecast_prices]
                confidence_low = [price * 0.9 for price in forecast_prices]
                
            elif forecast_model == "Seasonal Model":
                # Add seasonality to the forecast
                forecast_prices = [last_price * (1 + forecast_trend * (i+1) + 
                                              0.05 * np.sin(2 * np.pi * (i % 12) / 12) + 
                                              np.random.normal(0, volatility))
                                 for i in range(forecast_period)]
                confidence_high = [price * 1.15 for price in forecast_prices]
                confidence_low = [price * 0.85 for price in forecast_prices]
                
            else:  # Advanced ML Model
                # More complex pattern with stronger confidence intervals
                forecast_prices = [last_price * (1 + forecast_trend * (i+1) + 
                                              0.05 * np.sin(2 * np.pi * (i % 12) / 12) + 
                                              0.02 * np.sin(2 * np.pi * (i % 4) / 4) +
                                              np.random.normal(0, volatility * 0.7))
                                 for i in range(forecast_period)]
                confidence_high = [price * 1.08 for price in forecast_prices]
                confidence_low = [price * 0.92 for price in forecast_prices]
            
            # Create forecast DataFrame
            forecast_df = pd.DataFrame({
                'Date': forecast_dates,
                'Price': forecast_prices,
                'Upper Bound': confidence_high,
                'Lower Bound': confidence_low
            })
            
            # Combine historical and forecast data for visualization
            historical_df = price_data.copy()
            historical_df['Dataset'] = 'Historical'
            forecast_df['Dataset'] = 'Forecast'
            
            combined_df = pd.concat([historical_df, forecast_df], ignore_index=True)
            
            # Create the visualization
            fig = go.Figure()
            
            # Add historical data
            fig.add_trace(go.Scatter(
                x=historical_df['Date'],
                y=historical_df['Price'],
                mode='lines+markers',
                name='Historical Data',
                line=dict(color='#333333', width=2)
            ))
            
            # Add forecast data
            fig.add_trace(go.Scatter(
                x=forecast_df['Date'],
                y=forecast_df['Price'],
                mode='lines',
                name='Forecast',
                line=dict(color='#ff6b18', width=3)
            ))
            
            # Add confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_df['Date'].tolist() + forecast_df['Date'].tolist()[::-1],
                y=forecast_df['Upper Bound'].tolist() + forecast_df['Lower Bound'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(255, 107, 24, 0.2)',
                line=dict(color='rgba(255, 107, 24, 0)', width=0),
                name='Confidence Interval'
            ))
            
            # Update layout
            fig.update_layout(
                title=f"{selected_material} Price Forecast - {scenario}",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                height=500,
                hovermode="x unified",
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                ),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            # Add a vertical line separating historical from forecast
            fig.add_vline(
                x=historical_df['Date'].iloc[-1], 
                line_dash="dash", 
                line_color="gray",
                annotation_text="Forecast Start",
                annotation_position="top right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add price statistics
            col1, col2, col3 = st.columns(3)
            
            # Calculate statistics
            avg_forecast = np.mean(forecast_prices)
            peak_forecast = np.max(forecast_prices)
            min_forecast = np.min(forecast_prices)
            
            with col1:
                st.metric(
                    "Average Forecast Price", 
                    f"${avg_forecast:.2f}", 
                    f"{((avg_forecast / last_price) - 1) * 100:.1f}%"
                )
            
            with col2:
                st.metric(
                    "Peak Price", 
                    f"${peak_forecast:.2f}", 
                    f"{((peak_forecast / last_price) - 1) * 100:.1f}%"
                )
                
            with col3:
                st.metric(
                    "Minimum Price", 
                    f"${min_forecast:.2f}", 
                    f"{((min_forecast / last_price) - 1) * 100:.1f}%"
                )
                
            # Add forecast summary
            st.markdown("#### Forecast Summary")
            
            # Generate forecast insights based on scenario
            if scenario == "Base Case":
                insights = f"The base case forecast for {selected_material} shows relatively stable prices with moderate fluctuations. Prices are expected to end {forecast_trend * 100 * forecast_period:.1f}% higher than current levels over the {forecast_period}-month forecast period."
            elif scenario == "High Inflation":
                insights = f"Under high inflation conditions, {selected_material} prices are projected to increase significantly, potentially rising {forecast_trend * 100 * forecast_period:.1f}% over the {forecast_period}-month forecast period. Consider longer-term contracts to mitigate price increases."
            elif scenario == "Supply Constraint":
                insights = f"The supply constraint scenario shows sharp price increases for {selected_material}, with prices potentially rising {forecast_trend * 100 * forecast_period:.1f}% over the {forecast_period}-month period. Identifying alternative suppliers and building inventory may be advisable."
            elif scenario == "Demand Surge":
                insights = f"With increased market demand, {selected_material} prices are forecast to rise rapidly, potentially increasing {forecast_trend * 100 * forecast_period:.1f}% over the {forecast_period}-month period. Early procurement and volume commitments may help secure better pricing."
            elif scenario == "Economic Downturn":
                insights = f"In an economic downturn scenario, {selected_material} prices could decrease by {-forecast_trend * 100 * forecast_period:.1f}% over the {forecast_period}-month forecast period. This may present opportunities for favorable long-term contracts and strategic buying."
            
            st.markdown(insights)
            
            # Add procurement recommendations
            st.markdown("#### Procurement Recommendations")
            
            # Different recommendations based on forecast trend
            if avg_forecast > last_price * 1.1:  # Significant price increase
                st.markdown("""
                - **Lock in Contracts Now**: Secure longer-term contracts at current prices before increases materialize
                - **Explore Alternatives**: Investigate substitute materials or alternative suppliers
                - **Increase Stock Levels**: Consider building strategic inventory at current prices
                - **Implement Price Escalation Clauses**: For new contracts, include limits on price increases
                """)
            elif avg_forecast < last_price * 0.9:  # Significant price decrease
                st.markdown("""
                - **Delay Major Purchases**: If possible, postpone major purchases to benefit from expected price decreases
                - **Negotiate Shorter Contracts**: Prefer shorter-term agreements to capture future price decreases
                - **Include Price Review Mechanisms**: Add periodic price reviews in new contracts
                - **Manage Inventory Levels**: Minimize inventory to avoid holding higher-priced stock
                """)
            else:  # Stable prices
                st.markdown("""
                - **Maintain Balanced Approach**: Current market conditions support standard procurement strategies
                - **Focus on Supplier Performance**: With stable prices, prioritize quality and reliability in supplier selection
                - **Consider Mixed Contracts**: Implement a mix of spot purchases and medium-term contracts
                - **Monitor Market Signals**: Watch for early indicators of changing market conditions
                """)
                
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Should-cost modeling section
        st.markdown("### Should-Cost Modeling")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown("""
        The should-cost model breaks down the theoretical cost structure for the selected material 
        based on its components, manufacturing processes, and market conditions.
        """)
        
        # Generate should-cost breakdown
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Different cost components for different materials
            if selected_material in ["Steel", "Aluminum", "Copper", "Zinc"]:
                cost_components = {
                    "Raw Material": 0.65,
                    "Energy": 0.15,
                    "Labor": 0.08,
                    "Transportation": 0.05,
                    "Overhead & Profit": 0.07
                }
            elif selected_material in ["Titanium", "Carbon Fiber", "Avionics"]:
                cost_components = {
                    "Raw Material": 0.45,
                    "Processing": 0.25,
                    "Labor": 0.10,
                    "R&D": 0.08,
                    "Certification": 0.05,
                    "Overhead & Profit": 0.07
                }
            elif "Semiconductor" in selected_material or "Circuit" in selected_material:
                cost_components = {
                    "Silicon/Materials": 0.30,
                    "Fabrication": 0.35,
                    "Testing": 0.10,
                    "R&D": 0.15,
                    "Overhead & Profit": 0.10
                }
            else:
                cost_components = {
                    "Material": 0.40,
                    "Processing": 0.20,
                    "Labor": 0.15,
                    "Packaging": 0.05,
                    "Transportation": 0.05,
                    "Overhead & Profit": 0.15
                }
            
            # Create pie chart for cost breakdown
            component_names = list(cost_components.keys())
            component_values = list(cost_components.values())
            
            fig = px.pie(
                names=component_names,
                values=component_values,
                title=f"{selected_material} Cost Breakdown",
                color_discrete_sequence=px.colors.sequential.Oranges
            )
            
            fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=50, b=10)
            )
            
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Calculate should-cost based on market data and cost breakdown
            base_price = last_price
            
            st.markdown("#### Should-Cost Analysis")
            st.markdown(f"Current market price: **${base_price:.2f}**")
            
            # Show cost breakdown table
            breakdown_data = []
            for component, percentage in cost_components.items():
                cost = base_price * percentage
                breakdown_data.append({
                    "Component": component,
                    "Percentage": f"{percentage*100:.1f}%",
                    "Cost": f"${cost:.2f}"
                })
            
            breakdown_df = pd.DataFrame(breakdown_data)
            st.dataframe(breakdown_df, use_container_width=True)
            
            # Cost reduction opportunities
            st.markdown("#### Cost Reduction Opportunities")
            
            # Different opportunities for different materials/categories
            if selected_category == "Electronics":
                st.markdown("""
                - **Volume consolidation** across business units could yield 3-5% savings
                - **Design optimization** of components could reduce material usage by 5-8%
                - **Testing protocols** optimization could reduce costs by 2-3%
                - **Alternative suppliers** from emerging markets could offer 10-15% lower prices
                """)
            elif selected_category == "Aviation":
                st.markdown("""
                - **Material substitution** with qualified alternatives could save 4-6%
                - **Certification optimization** approaches could reduce costs by 2-3%
                - **Long-term agreements** with key suppliers may yield 5-8% cost avoidance
                - **Streamlined quality assurance** processes could reduce overhead by 3-4%
                """)
            else:
                st.markdown("""
                - **Supplier consolidation** could yield 3-7% volume pricing benefits
                - **Process optimization** could reduce manufacturing costs by 5-10%
                - **Transportation optimization** could save 10-15% on logistics costs
                - **Raw material sourcing** alternatives could reduce input costs by 4-8%
                """)
                
            # Show should-cost gap analysis
            estimated_should_cost = base_price * 0.85  # Typically 15% less than market
            gap_percentage = ((base_price - estimated_should_cost) / base_price) * 100
            
            st.markdown(f"##### Should-Cost Gap Analysis")
            st.markdown(f"Estimated should-cost price: **${estimated_should_cost:.2f}**")
            st.markdown(f"Current market-to-should-cost gap: **{gap_percentage:.1f}%**")
            
            # Gap visualization
            if gap_percentage > 15:
                gap_color = "#d42020"  # Red for large gap
                gap_assessment = "Significant savings opportunity"
            elif gap_percentage > 7:
                gap_color = "#ff6b18"  # Orange for medium gap
                gap_assessment = "Moderate savings opportunity"
            else:
                gap_color = "#1e7145"  # Green for small gap
                gap_assessment = "Market price close to should-cost"
                
            st.markdown(f"<span style='color:{gap_color};font-weight:bold;'>{gap_assessment}</span>", unsafe_allow_html=True)
                
        st.markdown("</div>", unsafe_allow_html=True)

# Supplier Intelligence tab
with tabs[4]:
    st.markdown('<div class="main-header">Supplier Intelligence</div>', unsafe_allow_html=True)
    st.markdown(f"#### Selected Category: {selected_category} | Region: {', '.join(selected_region)}")
    
    # Create layout with tabs for different supplier views
    supplier_tabs = st.tabs([
        "Supplier Dashboard", 
        "Supplier Comparison", 
        "Risk Assessment",
        "Performance Tracking"
    ])
    
    # Supplier Dashboard Tab
    with supplier_tabs[0]:
        st.markdown("### Supplier Overview Dashboard")
        
        # Generate supplier data
        supplier_data = generate_supplier_data(selected_category)
        supplier_list = supplier_data['Supplier'].tolist()
        
        # Select a supplier to focus on
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            selected_supplier = st.selectbox("Select Supplier", supplier_list)
            
            # Get the data for the selected supplier
            supplier_info = supplier_data[supplier_data['Supplier'] == selected_supplier].iloc[0]
            
            # Display supplier details
            st.markdown(f"#### {selected_supplier}")
            st.markdown(f"**Tier**: {supplier_info['Tier']}")
            st.markdown(f"**Annual Spend**: ${supplier_info['Spend']:,.2f}")
            
            # Calculate key metrics
            risk_score = supplier_info['Risk']
            performance_score = supplier_info['Performance']
            
            # Determine status based on scores
            if risk_score < 4 and performance_score > 7:
                status = "Strategic Partner"
                status_color = "#1e7145"  # Green
            elif risk_score > 7:
                status = "High Risk"
                status_color = "#d42020"  # Red
            elif performance_score < 4:
                status = "Underperforming"
                status_color = "#ff6b18"  # Orange
            else:
                status = "Standard"
                status_color = "#333333"  # Gray
            
            st.markdown(f"**Status**: <span style='color:{status_color};font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
            
            # Action buttons
            st.markdown("#### Actions")
            if st.button("Generate Supplier Report", use_container_width=True):
                st.session_state.show_supplier_report = True
                
            if st.button("Assess Risk", use_container_width=True):
                st.session_state.show_risk_assessment = True
                
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            # Key Performance Indicators
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Supplier KPIs")
            
            # Create metrics row
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            # Risk score metric
            with metric_col1:
                risk_delta = -round(np.random.uniform(0.2, 0.8), 1)  # Small improvement in risk
                st.metric(
                    "Risk Score", 
                    f"{risk_score:.1f}/10", 
                    f"{risk_delta:.1f}",
                    delta_color="inverse"  # Lower risk is better, so use inverse
                )
            
            # Performance score metric
            with metric_col2:
                perf_delta = round(np.random.uniform(0.1, 0.7), 1)  # Small improvement in performance
                st.metric(
                    "Performance Score", 
                    f"{performance_score:.1f}/10", 
                    f"{perf_delta:.1f}"
                )
            
            # Spend trend metric
            with metric_col3:
                spend_change = round(np.random.uniform(-5, 8), 1)  # Change in spend percentage
                st.metric(
                    "Spend Trend", 
                    f"${supplier_info['Spend']:,.0f}", 
                    f"{spend_change}%"
                )
                
            # Radar chart showing supplier performance across categories
            # Generate random scores for different performance categories
            categories = ['Quality', 'Delivery', 'Service', 'Price', 'Innovation', 'Sustainability']
            scores = []
            
            # Generate scores that align with overall performance - if good performance, scores should be higher
            base_score = performance_score * 10  # convert to 0-100 scale
            for _ in categories:
                # Create variation around the base score
                cat_score = max(0, min(100, base_score + np.random.normal(0, 10)))
                scores.append(cat_score)
            
            # Create the radar chart data
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name=selected_supplier,
                line=dict(color='#ff6b18'),
                fillcolor='rgba(255, 107, 24, 0.2)'
            ))
            
            # Add industry benchmark
            industry_scores = [65, 72, 68, 75, 60, 70]  # Benchmark scores
            
            fig.add_trace(go.Scatterpolar(
                r=industry_scores,
                theta=categories,
                fill='toself',
                name='Industry Benchmark',
                line=dict(color='#333333', dash='dash'),
                fillcolor='rgba(150, 150, 150, 0.1)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title="Performance Assessment",
                height=350,
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.1,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Performance and risk trends
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Performance Trend")
            
            # Generate performance trend data
            dates = pd.date_range(end=pd.Timestamp.now(), periods=12, freq='M')
            
            # Create performance data with some meaningful pattern
            base_perf = performance_score - 1.5  # Start a bit lower to show improvement
            performance_trend = [
                min(10, max(0, base_perf + i * 0.2 + np.random.normal(0, 0.3)))
                for i in range(len(dates))
            ]
            
            # Create the line chart
            fig = px.line(
                x=dates, 
                y=performance_trend,
                labels={"x": "Date", "y": "Performance Score"},
                markers=True
            )
            
            fig.update_layout(
                height=300,
                hovermode="x unified",
                yaxis=dict(range=[0, 10]),
                margin=dict(l=10, r=10, t=0, b=10)
            )
            
            fig.update_traces(
                line=dict(color='#ff6b18', width=2),
                marker=dict(color='#ff6b18', size=6)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Spend Analysis")
            
            # Generate spend data
            categories = ["Raw Materials", "Components", "Services", "Transportation", "Other"]
            
            # Generate spend data that sums to the total spend
            total_spend = supplier_info['Spend']
            spend_values = []
            remaining = total_spend
            
            for i in range(len(categories) - 1):
                # Allocate a portion of the remaining spend
                value = remaining * np.random.uniform(0.1, 0.4)
                spend_values.append(value)
                remaining -= value
            
            # Add the remainder to the last category
            spend_values.append(remaining)
            
            # Create the pie chart
            fig = px.pie(
                names=categories, 
                values=spend_values,
                title="Spend Breakdown",
                color_discrete_sequence=px.colors.sequential.Oranges
            )
            
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show supplier report if requested
        if "show_supplier_report" in st.session_state and st.session_state.show_supplier_report:
            st.markdown("### Supplier Performance Report")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Create tabs for different report sections
            report_tabs = st.tabs(["Overview", "Quality", "Delivery", "Compliance", "Recommendations"])
            
            with report_tabs[0]:
                st.markdown(f"#### {selected_supplier} - Executive Summary")
                
                # Executive summary
                st.markdown(f"""
                This report provides a comprehensive assessment of {selected_supplier}'s performance 
                over the past 12 months as a supplier for {selected_category}.
                
                **Key Highlights:**
                
                - Overall performance score: **{performance_score:.1f}/10** ({perf_delta:+.1f} change)
                - Risk assessment: **{risk_score:.1f}/10** ({risk_delta:+.1f} change)
                - Annual spend: **${supplier_info['Spend']:,.2f}** ({spend_change:+.1f}% change)
                - Current status: **{status}**
                """)
                
                # Key achievements and issues
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### Strengths")
                    strengths = [
                        f"Strong performance in {categories[scores.index(max(scores))]}",
                        "Consistent communication and responsiveness",
                        f"Above average scores in {len([s for s in scores if s > 70])} of {len(scores)} categories"
                    ]
                    
                    for strength in strengths:
                        st.markdown(f"- {strength}")
                
                with col2:
                    st.markdown("##### Areas for Improvement")
                    weaknesses = [
                        f"Below benchmark performance in {categories[scores.index(min(scores))]}",
                        "Inconsistent delivery schedules",
                        "Sustainability initiatives need strengthening"
                    ]
                    
                    for weakness in weaknesses:
                        st.markdown(f"- {weakness}")
            
            with report_tabs[1]:
                st.markdown("#### Quality Performance")
                
                # Generate quality metrics
                quality_metrics = {
                    "Defect Rate": f"{np.random.uniform(0.1, 2.0):.2f}%",
                    "Quality Audit Score": f"{np.random.uniform(75, 95):.1f}/100",
                    "Customer Complaints": f"{int(np.random.uniform(1, 10))}",
                    "First Pass Yield": f"{np.random.uniform(85, 98):.1f}%"
                }
                
                # Create metrics table
                metrics_df = pd.DataFrame({
                    "Metric": quality_metrics.keys(),
                    "Value": quality_metrics.values(),
                    "Benchmark": ["0.50%", "85.0/100", "5", "92.0%"],
                    "Status": ["Good", "Good", "Good", "Average"]
                })
                
                st.dataframe(metrics_df, use_container_width=True)
                
                # Quality trend chart
                st.markdown("##### Quality Trend (12 Month)")
                
                # Generate quality trend data
                dates = pd.date_range(end=pd.Timestamp.now(), periods=12, freq='M')
                quality_scores = [np.random.uniform(85, 95) for _ in range(len(dates))]
                
                # Create the line chart
                fig = px.line(
                    x=dates, 
                    y=quality_scores,
                    labels={"x": "Date", "y": "Quality Score"},
                    markers=True
                )
                
                fig.update_layout(
                    height=300,
                    hovermode="x unified",
                    yaxis=dict(range=[80, 100]),
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                fig.add_hline(
                    y=90, 
                    line_dash="dash", 
                    line_color="#ff6b18",
                    annotation_text="Target", 
                    annotation_position="bottom right"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with report_tabs[2]:
                st.markdown("#### Delivery Performance")
                
                # Generate delivery metrics
                delivery_metrics = {
                    "On-Time Delivery": f"{np.random.uniform(85, 98):.1f}%",
                    "Lead Time": f"{int(np.random.uniform(10, 30))} days",
                    "Order Fill Rate": f"{np.random.uniform(90, 99):.1f}%",
                    "Perfect Order Rate": f"{np.random.uniform(80, 95):.1f}%"
                }
                
                # Create metrics table
                metrics_df = pd.DataFrame({
                    "Metric": delivery_metrics.keys(),
                    "Value": delivery_metrics.values(),
                    "Benchmark": ["95.0%", "15 days", "98.0%", "90.0%"],
                    "Status": ["Average", "Below Average", "Good", "Good"]
                })
                
                st.dataframe(metrics_df, use_container_width=True)
                
                # Delivery performance chart - by month
                st.markdown("##### On-Time Delivery by Month")
                
                # Generate monthly delivery data
                months = pd.date_range(end=pd.Timestamp.now(), periods=12, freq='M')
                monthly_otd = [np.random.uniform(85, 98) for _ in range(len(months))]
                
                # Create the bar chart
                fig = px.bar(
                    x=[d.strftime('%b %Y') for d in months], 
                    y=monthly_otd,
                    labels={"x": "Month", "y": "On-Time Delivery (%)"},
                    color=monthly_otd,
                    color_continuous_scale='Oranges'
                )
                
                fig.update_layout(
                    height=300,
                    hovermode="x unified",
                    yaxis=dict(range=[80, 100]),
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                fig.add_hline(
                    y=95, 
                    line_dash="dash", 
                    line_color="green",
                    annotation_text="Target", 
                    annotation_position="bottom right"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with report_tabs[3]:
                st.markdown("#### Compliance & Risk")
                
                # Generate compliance data
                compliance_categories = [
                    "Regulatory Compliance", 
                    "Environmental Standards", 
                    "Labor Practices", 
                    "Data Security", 
                    "Business Ethics",
                    "Certifications"
                ]
                
                compliance_scores = [np.random.uniform(70, 95) for _ in range(len(compliance_categories))]
                compliance_statuses = ["Compliant" if score >= 80 else "Partial" if score >= 70 else "Non-Compliant" for score in compliance_scores]
                
                # Create compliance table
                compliance_df = pd.DataFrame({
                    "Category": compliance_categories,
                    "Score": [f"{score:.1f}/100" for score in compliance_scores],
                    "Status": compliance_statuses,
                    "Last Audit": [(pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(30, 365))).strftime('%Y-%m-%d') for _ in range(len(compliance_categories))]
                })
                
                st.dataframe(compliance_df, use_container_width=True)
                
                # Compliance radar chart
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=compliance_scores,
                    theta=compliance_categories,
                    fill='toself',
                    name=selected_supplier,
                    line=dict(color='#ff6b18'),
                    fillcolor='rgba(255, 107, 24, 0.2)'
                ))
                
                # Industry benchmark
                benchmark_scores = [85, 82, 88, 90, 85, 80]
                
                fig.add_trace(go.Scatterpolar(
                    r=benchmark_scores,
                    theta=compliance_categories,
                    fill='toself',
                    name='Industry Benchmark',
                    line=dict(color='#333333', dash='dash'),
                    fillcolor='rgba(150, 150, 150, 0.1)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    title="Compliance Assessment",
                    height=400,
                    margin=dict(l=10, r=10, t=40, b=10),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.1,
                        xanchor="center",
                        x=0.5
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with report_tabs[4]:
                st.markdown("#### Recommendations")
                
                # Calculate overall recommendation based on performance
                if performance_score > 7.5:
                    recommendation = "Maintain Strategic Partnership"
                    actions = [
                        "Engage in joint innovation projects",
                        "Consider multi-year contract with volume commitments",
                        "Implement quarterly business reviews",
                        "Explore additional categories or products"
                    ]
                elif performance_score > 6:
                    recommendation = "Develop Relationship"
                    actions = [
                        "Create supplier development plan",
                        "Schedule quarterly performance reviews",
                        "Consolidate spend to improve leverage",
                        "Reassess tier status"
                    ]
                elif performance_score > 4:
                    recommendation = "Monitor Closely"
                    actions = [
                        "Implement monthly performance reviews",
                        "Require corrective action plan for low-scoring areas",
                        "Identify backup suppliers",
                        "Create specific improvement targets"
                    ]
                else:
                    recommendation = "Consider Alternative Sources"
                    actions = [
                        "Identify alternative suppliers",
                        "Develop transition plan",
                        "Reduce dependency gradually",
                        "Implement risk mitigation measures"
                    ]
                
                # Show recommendation
                st.markdown(f"##### Strategic Recommendation: **{recommendation}**")
                
                # Show action plan
                st.markdown("##### Recommended Actions:")
                for action in actions:
                    st.markdown(f"- {action}")
                
                # Performance impact
                st.markdown("##### Expected Performance Impact")
                impact_data = {
                    "Current Performance": [performance_score * 10],
                    "Target (6 months)": [min(100, performance_score * 10 + 5)],
                    "Target (12 months)": [min(100, performance_score * 10 + 12)]
                }
                
                fig = go.Figure()
                
                # Add current performance
                fig.add_trace(go.Bar(
                    x=["Current Performance"],
                    y=[performance_score * 10],
                    marker_color='#333333',
                    width=0.2,
                    name="Current"
                ))
                
                # Add 6-month target
                fig.add_trace(go.Bar(
                    x=["Target (6 months)"],
                    y=[min(100, performance_score * 10 + 5)],
                    marker_color='#ff8c4d',
                    width=0.2,
                    name="6 Months"
                ))
                
                # Add 12-month target
                fig.add_trace(go.Bar(
                    x=["Target (12 months)"],
                    y=[min(100, performance_score * 10 + 12)],
                    marker_color='#ff6b18',
                    width=0.2,
                    name="12 Months"
                ))
                
                fig.update_layout(
                    title="Performance Improvement Targets",
                    yaxis=dict(title="Performance Score", range=[0, 100]),
                    height=300,
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show risk assessment if requested
        if "show_risk_assessment" in st.session_state and st.session_state.show_risk_assessment:
            st.markdown("### Supplier Risk Assessment")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Generate risk data
            risk_categories = {
                "Financial Stability": np.random.uniform(3, 8),
                "Supply Chain Disruption": np.random.uniform(3, 8),
                "Geopolitical Risk": np.random.uniform(2, 7),
                "Compliance Risk": np.random.uniform(2, 6),
                "Quality Risk": np.random.uniform(1, 5),
                "Delivery Risk": np.random.uniform(2, 6),
                "Cyber Security": np.random.uniform(3, 7),
                "ESG Risk": np.random.uniform(4, 8)
            }
            
            # Overall risk score is weighted average
            overall_risk = sum(risk_categories.values()) / len(risk_categories)
            
            # Display overall risk score
            risk_level = "High" if overall_risk > 6.5 else "Medium" if overall_risk > 4 else "Low"
            risk_color = "#d42020" if risk_level == "High" else "#ff6b18" if risk_level == "Medium" else "#1e7145"
            
            st.markdown(f"#### Overall Risk Assessment: <span style='color:{risk_color};font-weight:bold;'>{risk_level}</span>", unsafe_allow_html=True)
            st.markdown(f"Overall Risk Score: **{overall_risk:.1f}/10**")
            
            # Create horizontal bar chart for risk categories
            categories = list(risk_categories.keys())
            scores = list(risk_categories.values())
            
            # Sort by risk score descending
            sorted_indices = np.argsort(scores)[::-1]
            sorted_categories = [categories[i] for i in sorted_indices]
            sorted_scores = [scores[i] for i in sorted_indices]
            
            # Color based on risk level
            colors = ['#d42020' if s > 6.5 else '#ff6b18' if s > 4 else '#1e7145' for s in sorted_scores]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=sorted_categories,
                x=sorted_scores,
                orientation='h',
                marker_color=colors,
                text=[f"{s:.1f}" for s in sorted_scores],
                textposition='auto'
            ))
            
            fig.update_layout(
                title="Risk Assessment by Category",
                xaxis=dict(title="Risk Score", range=[0, 10]),
                height=400,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk mitigation recommendations
            st.markdown("#### Risk Mitigation Recommendations")
            
            # Identify top 3 risks
            top_risks = [categories[i] for i in sorted_indices[:3]]
            
            # Provide recommendations for each top risk
            for risk in top_risks:
                risk_score = risk_categories[risk]
                risk_level = "High" if risk_score > 6.5 else "Medium" if risk_score > 4 else "Low"
                risk_color = "#d42020" if risk_level == "High" else "#ff6b18" if risk_level == "Medium" else "#1e7145"
                
                st.markdown(f"##### {risk}: <span style='color:{risk_color};font-weight:bold;'>{risk_level}</span>", unsafe_allow_html=True)
                
                if risk == "Financial Stability":
                    st.markdown("""
                    - Conduct quarterly financial health assessments
                    - Implement payment term protections
                    - Develop contingency plans for supplier financial distress
                    - Consider requiring performance bonds for critical components
                    """)
                elif risk == "Supply Chain Disruption":
                    st.markdown("""
                    - Develop dual sourcing strategy for critical components
                    - Increase safety stock for key materials
                    - Implement supply chain visibility tools
                    - Conduct regular scenario planning exercises
                    """)
                elif risk == "Geopolitical Risk":
                    st.markdown("""
                    - Diversify supply base across multiple regions
                    - Monitor political developments in supplier countries
                    - Develop contingency plans for trade disruptions
                    - Consider forward buying critical materials
                    """)
                elif risk == "Compliance Risk":
                    st.markdown("""
                    - Implement compliance audit program
                    - Require supplier certification to relevant standards
                    - Include compliance clauses in contracts
                    - Provide supplier training on regulatory requirements
                    """)
                elif risk == "Quality Risk":
                    st.markdown("""
                    - Implement enhanced quality control measures
                    - Conduct more frequent quality audits
                    - Establish clearer quality specifications
                    - Implement incoming inspection protocols
                    """)
                elif risk == "Delivery Risk":
                    st.markdown("""
                    - Implement delivery performance monitoring system
                    - Establish clearer delivery requirements
                    - Consider buffer inventory for critical components
                    - Develop backup logistics options
                    """)
                elif risk == "Cyber Security":
                    st.markdown("""
                    - Conduct cyber security assessment
                    - Require compliance with security standards
                    - Limit data access and implement encryption
                    - Develop incident response plans
                    """)
                elif risk == "ESG Risk":
                    st.markdown("""
                    - Implement ESG monitoring program
                    - Require sustainability certifications
                    - Conduct regular ESG audits
                    - Develop improvement targets with supplier
                    """)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Supplier Comparison Tab
    with supplier_tabs[1]:
        st.markdown("### Supplier Comparison")
        
        # Generate supplier data
        supplier_data = generate_supplier_data(selected_category)
        
        # Let user select suppliers to compare
        st.markdown("Select suppliers to compare:")
        
        # Convert supplier data to more readable format
        supplier_display_data = supplier_data.copy()
        supplier_display_data['Spend'] = supplier_display_data['Spend'].apply(lambda x: f"${x:,.0f}")
        
        # Display supplier table with selection
        selected_indices = st.multiselect(
            "Choose suppliers",
            options=list(range(len(supplier_data))),
            default=list(range(min(5, len(supplier_data)))),
            format_func=lambda i: f"{supplier_data.iloc[i]['Supplier']} ({supplier_data.iloc[i]['Tier']})"
        )
        
        if selected_indices:
            # Filter data for selected suppliers
            selected_supplier_data = supplier_data.iloc[selected_indices].copy()
            
            # Create comparison visualizations
            st.markdown("#### Performance Comparison")
            
            # Radar chart comparing selected suppliers
            categories = ['Quality', 'Delivery', 'Price', 'Innovation', 'Support', 'Sustainability']
            
            fig = go.Figure()
            
            # Generate random performance scores for each supplier across categories
            for i, row in selected_supplier_data.iterrows():
                # Base the scores on the overall performance score
                base_score = row['Performance'] * 10  # Convert to 0-100 scale
                
                # Generate variations around the base score
                scores = []
                for _ in categories:
                    cat_score = max(0, min(100, base_score + np.random.normal(0, 10)))
                    scores.append(cat_score)
                
                fig.add_trace(go.Scatterpolar(
                    r=scores,
                    theta=categories,
                    fill='toself',
                    name=row['Supplier'],
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title="Supplier Performance Comparison",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Bar chart comparison
            st.markdown("#### Key Metrics Comparison")
            
            # Create metrics for comparison
            compare_col1, compare_col2 = st.columns(2)
            
            with compare_col1:
                # Compare risk scores
                fig = px.bar(
                    selected_supplier_data,
                    x='Supplier',
                    y='Risk',
                    title="Risk Score Comparison (Lower is Better)",
                    color='Risk',
                    color_continuous_scale='RdYlGn_r'  # Reversed so red is high risk
                )
                
                fig.update_layout(
                    height=350,
                    yaxis=dict(range=[0, 10])
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with compare_col2:
                # Compare performance scores
                fig = px.bar(
                    selected_supplier_data,
                    x='Supplier',
                    y='Performance',
                    title="Performance Score Comparison",
                    color='Performance',
                    color_continuous_scale='YlGn'  # Green is good performance
                )
                
                fig.update_layout(
                    height=350,
                    yaxis=dict(range=[0, 10])
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Scatter plot for quadrant analysis
            st.markdown("#### Strategic Positioning Comparison")
            
            fig = px.scatter(
                selected_supplier_data,
                x="Risk",
                y="Performance",
                size="Spend",
                color="Tier",
                hover_name="Supplier",
                size_max=50,
                title="Supplier Quadrant Analysis"
            )
            
            # Add quadrant lines
            fig.add_shape(type="line", x0=5, y0=0, x1=5, y1=10, line=dict(color="Gray", width=1, dash="dash"))
            fig.add_shape(type="line", x0=0, y0=5, x1=10, y1=5, line=dict(color="Gray", width=1, dash="dash"))
            
            # Quadrant fill colors (with transparency)
            fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, 
                         line=dict(width=0), fillcolor="rgba(0,176,80,0.1)")  # Strategic Partners - Green
            fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, 
                         line=dict(width=0), fillcolor="rgba(255,192,0,0.1)")  # Performance Focus - Yellow
            fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, 
                         line=dict(width=0), fillcolor="rgba(112,173,71,0.1)")  # Maintain - Light Green
            fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, 
                         line=dict(width=0), fillcolor="rgba(255,107,24,0.1)")  # Risk Mitigation - Orange
            
            # Add quadrant labels
            fig.add_annotation(x=2.5, y=7.5, text="Strategic Partners", showarrow=False, font=dict(size=12))
            fig.add_annotation(x=7.5, y=7.5, text="Performance Focus", showarrow=False, font=dict(size=12))
            fig.add_annotation(x=2.5, y=2.5, text="Maintain", showarrow=False, font=dict(size=12))
            fig.add_annotation(x=7.5, y=2.5, text="Risk Mitigation", showarrow=False, font=dict(size=12))
            
            fig.update_layout(
                height=600,
                xaxis=dict(title="Risk Score", range=[0, 10]),
                yaxis=dict(title="Performance Score", range=[0, 10])
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed comparison table
            st.markdown("#### Detailed Comparison")
            
            # Generate additional metrics for each supplier
            detailed_data = []
            
            for i, row in selected_supplier_data.iterrows():
                perf_score = row['Performance']
                risk_score = row['Risk']
                
                # Generate metrics that align with performance and risk scores
                on_time_delivery = max(70, min(99, 85 + (perf_score - 5) * 3 + np.random.uniform(-3, 3)))
                quality_score = max(70, min(99, 85 + (perf_score - 5) * 3 + np.random.uniform(-3, 3)))
                cost_savings = max(0, min(15, 5 + (perf_score - 5) * 2 + np.random.uniform(-2, 2)))
                contract_compliance = max(80, min(100, 90 + (perf_score - 5) * 2 + np.random.uniform(-2, 2)))
                financial_health = max(1, min(10, 10 - risk_score + np.random.uniform(-1, 1)))
                
                detailed_data.append({
                    "Supplier": row['Supplier'],
                    "Tier": row['Tier'],
                    "Annual Spend": f"${row['Spend']:,.0f}",
                    "Performance Score": f"{perf_score:.1f}/10",
                    "Risk Score": f"{risk_score:.1f}/10",
                    "On-Time Delivery": f"{on_time_delivery:.1f}%",
                    "Quality Score": f"{quality_score:.1f}/100",
                    "Cost Savings": f"{cost_savings:.1f}%",
                    "Contract Compliance": f"{contract_compliance:.1f}%",
                    "Financial Health": f"{financial_health:.1f}/10"
                })
            
            # Create DataFrame for detailed comparison
            detailed_df = pd.DataFrame(detailed_data)
            
            # Display as styled table
            st.dataframe(detailed_df, use_container_width=True)
        
        else:
            st.info("Please select at least one supplier to compare")
    
    # Risk Assessment Tab
    with supplier_tabs[2]:
        st.markdown("### Supplier Risk Assessment Dashboard")
        
        # Generate risk data
        risk_data = generate_risk_data(selected_category)
        
        # Create heatmap
        st.markdown("#### Risk Heatmap by Category and Supplier")
        
        fig = px.imshow(
            risk_data,
            labels=dict(x="Risk Category", y="Supplier", color="Risk Level"),
            x=risk_data.columns,
            y=risk_data.index,
            color_continuous_scale=['#1e7145', '#ffeba5', '#ff6b18', '#d42020'],  # Green to yellow to orange to red
            aspect="auto",
            text_auto=True
        )
        
        fig.update_layout(
            height=500,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_colorbar=dict(
                title="Risk Level",
                thicknessmode="pixels", thickness=15,
                lenmode="pixels", len=300,
                yanchor="top", y=1,
                ticks="outside"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk overview
        col1, col2 = st.columns(2)
        
        with col1:
            # Top risks by category
            st.markdown("#### Highest Risk Categories")
            
            # Calculate average risk for each category
            category_risks = risk_data.mean().reset_index()
            category_risks.columns = ['Category', 'Average Risk']
            category_risks = category_risks.sort_values('Average Risk', ascending=False)
            
            fig = px.bar(
                category_risks.head(5),
                x='Category',
                y='Average Risk',
                color='Average Risk',
                color_continuous_scale='RdYlGn_r',  # Red for high risk
                title="Top 5 Risk Categories"
            )
            
            fig.update_layout(
                height=350,
                yaxis=dict(range=[0, 10])
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Suppliers with highest risk
            st.markdown("#### Highest Risk Suppliers")
            
            # Calculate average risk for each supplier
            supplier_risks = risk_data.mean(axis=1).reset_index()
            supplier_risks.columns = ['Supplier', 'Average Risk']
            supplier_risks = supplier_risks.sort_values('Average Risk', ascending=False)
            
            fig = px.bar(
                supplier_risks.head(5),
                x='Supplier',
                y='Average Risk',
                color='Average Risk',
                color_continuous_scale='RdYlGn_r',  # Red for high risk
                title="Top 5 High Risk Suppliers"
            )
            
            fig.update_layout(
                height=350,
                yaxis=dict(range=[0, 10])
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Risk mitigation planning
        st.markdown("#### Risk Mitigation Planning")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Let user select a risk category to focus on
        risk_category = st.selectbox("Select Risk Category", risk_data.columns.tolist())
        
        if risk_category:
            # Get the suppliers with highest risk in this category
            category_supplier_risks = risk_data[risk_category].sort_values(ascending=False)
            
            # Display top 3 suppliers for this risk
            st.markdown(f"##### Top High-Risk Suppliers for {risk_category}")
            
            top_suppliers = []
            for supplier, risk in category_supplier_risks.head(3).items():
                risk_level = "High" if risk > 7 else "Medium" if risk > 4 else "Low"
                risk_color = "#d42020" if risk_level == "High" else "#ff6b18" if risk_level == "Medium" else "#1e7145"
                
                top_suppliers.append({
                    "Supplier": supplier,
                    "Risk Score": f"{risk:.1f}/10",
                    "Risk Level": risk_level,
                    "Risk Color": risk_color
                })
            
            # Display supplier risks
            for supplier in top_suppliers:
                st.markdown(
                    f"""
                    <div style="padding: 10px; margin-bottom: 10px; border-left: 5px solid {supplier['Risk Color']}; background-color: #f8f9fa;">
                        <div style="font-weight: bold;">{supplier['Supplier']}</div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Risk Score: {supplier['Risk Score']}</span>
                            <span style="color: {supplier['Risk Color']}; font-weight: bold;">Level: {supplier['Risk Level']}</span>
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
            elif risk_category == "Geo-political":
                st.markdown("""
                - Diversify supply base across multiple regions
                - Implement geopolitical risk monitoring system
                - Develop contingency plans for trade disruptions
                - Increase safety stock for components from high-risk regions
                - Consider nearshoring or reshoring options for critical components
                """)
            elif risk_category == "Supply Chain":
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
            elif risk_category == "Quality":
                st.markdown("""
                - Enhance supplier quality management systems
                - Implement statistical process control
                - Conduct regular quality audits
                - Develop supplier quality improvement programs
                - Establish supplier quality certification requirements
                """)
            elif risk_category == "ESG":
                st.markdown("""
                - Implement supplier ESG assessment program
                - Require sustainability certifications
                - Conduct carbon footprint assessments
                - Develop joint sustainability initiatives
                - Establish ESG performance metrics and targets
                """)
                
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Performance Tracking Tab
    with supplier_tabs[3]:
        st.markdown("### Supplier Performance Tracking")
        
        # Generate performance data for tracking
        dates = pd.date_range(end=pd.Timestamp.now(), periods=12, freq='M')
        
        # Top level KPI tracking
        st.markdown("#### Key Performance Indicators Over Time")
        
        # Create tabs for different KPIs
        kpi_tabs = st.tabs(["Overall Score", "Quality", "Delivery", "Cost"])
        
        with kpi_tabs[0]:
            # Generate overall performance data for multiple suppliers
            supplier_data = generate_supplier_data(selected_category)
            top_suppliers = supplier_data.sort_values('Spend', ascending=False).head(5)['Supplier'].tolist()
            
            # Create performance trend data
            performance_data = []
            
            for supplier in top_suppliers:
                # Base performance that improves slightly over time
                base_perf = np.random.uniform(5, 8)
                trend = np.random.uniform(-0.1, 0.2)  # Some improve, some decline
                
                for i, date in enumerate(dates):
                    # Add some random variation to the trend
                    perf = max(0, min(10, base_perf + trend * i + np.random.normal(0, 0.3)))
                    
                    performance_data.append({
                        'Date': date,
                        'Supplier': supplier,
                        'Performance': perf
                    })
            
            # Create DataFrame
            performance_df = pd.DataFrame(performance_data)
            
            # Create line chart
            fig = px.line(
                performance_df,
                x='Date',
                y='Performance',
                color='Supplier',
                title="Overall Performance Score Trend",
                markers=True
            )
            
            fig.update_layout(
                height=400,
                hovermode="x unified",
                yaxis=dict(title="Performance Score", range=[0, 10])
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance statistics
            st.markdown("##### Performance Statistics")
            
            # Calculate statistics by supplier
            stats = performance_df.groupby('Supplier')['Performance'].agg(['mean', 'min', 'max', 'std'])
            stats.columns = ['Average', 'Minimum', 'Maximum', 'Std Dev']
            stats = stats.sort_values('Average', ascending=False)
            stats = stats.round(2)
            
            # Add trend calculation
            trend_data = []
            for supplier in stats.index:
                supplier_perf = performance_df[performance_df['Supplier'] == supplier].sort_values('Date')
                first_half = supplier_perf['Performance'].iloc[:6].mean()
                second_half = supplier_perf['Performance'].iloc[6:].mean()
                trend = second_half - first_half
                trend_data.append(trend)
            
            stats['Trend'] = trend_data
            stats['Trend'] = stats['Trend'].round(2)
            
            # Display statistics
            st.dataframe(stats, use_container_width=True)
        
        with kpi_tabs[1]:
            # Quality metrics over time
            st.markdown("##### Quality Performance Metrics")
            
            # Create quality metrics
            metrics = ["Defect Rate (%)", "First Pass Yield (%)", "Quality Audit Score"]
            supplier = top_suppliers[0]  # Focus on one supplier for detailed metrics
            
            quality_data = []
            
            # Generate data for each metric
            for metric in metrics:
                # Set base values appropriate for each metric
                if metric == "Defect Rate (%)":
                    base = 2.0
                    trend = -0.05  # Improvement = reduction
                    variation = 0.2
                elif metric == "First Pass Yield (%)":
                    base = 90.0
                    trend = 0.3  # Improvement = increase
                    variation = 1.0
                else:  # Quality Audit Score
                    base = 85.0
                    trend = 0.4  # Improvement = increase
                    variation = 2.0
                
                for i, date in enumerate(dates):
                    # Calculate metric value with trend and variation
                    value = base + trend * i + np.random.normal(0, variation)
                    
                    # Ensure values are in appropriate ranges
                    if metric == "Defect Rate (%)":
                        value = max(0.1, value)
                    elif metric == "First Pass Yield (%)":
                        value = min(100, max(80, value))
                    else:  # Quality Audit Score
                        value = min(100, max(70, value))
                    
                    quality_data.append({
                        'Date': date,
                        'Metric': metric,
                        'Value': value
                    })
            
            # Create DataFrame
            quality_df = pd.DataFrame(quality_data)
            
            # Create separate charts for each metric
            for metric in metrics:
                metric_data = quality_df[quality_df['Metric'] == metric]
                
                fig = px.line(
                    metric_data,
                    x='Date',
                    y='Value',
                    title=f"{supplier} - {metric}",
                    markers=True
                )
                
                # Set appropriate y-axis range
                if metric == "Defect Rate (%)":
                    y_range = [0, 5]
                    target = 1.0
                    target_direction = "Max"
                    line_color = "red"
                elif metric == "First Pass Yield (%)":
                    y_range = [80, 100]
                    target = 95.0
                    target_direction = "Min"
                    line_color = "green"
                else:  # Quality Audit Score
                    y_range = [70, 100]
                    target = 90.0
                    target_direction = "Min"
                    line_color = "green"
                
                fig.update_layout(
                    height=300,
                    yaxis=dict(range=y_range),
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                
                # Add target line
                fig.add_hline(
                    y=target,
                    line_dash="dash",
                    line_color=line_color,
                    annotation_text=f"Target ({target_direction})",
                    annotation_position="bottom right"
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with kpi_tabs[2]:
            # Delivery performance
            st.markdown("##### Delivery Performance")
            
            # Create on-time delivery data
            delivery_data = []
            
            for supplier in top_suppliers:
                # Base on-time delivery percentage
                base_otd = np.random.uniform(80, 95)
                trend = np.random.uniform(-0.2, 0.5)  # Some improve, some decline
                
                for i, date in enumerate(dates):
                    # Calculate OTD with trend and variation
                    otd = min(100, max(70, base_otd + trend * i + np.random.normal(0, 2)))
                    
                    delivery_data.append({
                        'Date': date,
                        'Supplier': supplier,
                        'On-Time Delivery (%)': otd
                    })
            
            # Create DataFrame
            delivery_df = pd.DataFrame(delivery_data)
            
            # Create line chart
            fig = px.line(
                delivery_df,
                x='Date',
                y='On-Time Delivery (%)',
                color='Supplier',
                title="On-Time Delivery Performance",
                markers=True
            )
            
            fig.update_layout(
                height=400,
                hovermode="x unified",
                yaxis=dict(range=[70, 100])
            )
            
            # Add target line
            fig.add_hline(
                y=95,
                line_dash="dash",
                line_color="green",
                annotation_text="Target",
                annotation_position="bottom right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Lead time tracking
            st.markdown("##### Lead Time Performance")
            
            # Create lead time data for one supplier
            supplier = top_suppliers[0]
            lead_time_data = []
            
            # Base lead time in days
            base_lead_time = np.random.uniform(20, 30)
            trend = np.random.uniform(-0.3, 0.1)  # Hopefully improving
            
            for i, date in enumerate(dates):
                # Calculate lead time with trend and variation
                lead_time = max(10, base_lead_time + trend * i + np.random.normal(0, 1.5))
                
                lead_time_data.append({
                    'Date': date,
                    'Lead Time (Days)': lead_time
                })
            
            # Create DataFrame
            lead_time_df = pd.DataFrame(lead_time_data)
            
            # Create chart
            fig = px.line(
                lead_time_df,
                x='Date',
                y='Lead Time (Days)',
                title=f"{supplier} - Lead Time Performance",
                markers=True
            )
            
            fig.update_layout(
                height=300,
                yaxis=dict(title="Lead Time (Days)")
            )
            
            # Add target line
            fig.add_hline(
                y=15,
                line_dash="dash",
                line_color="red",
                annotation_text="Target",
                annotation_position="bottom right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with kpi_tabs[3]:
            # Cost performance
            st.markdown("##### Cost Performance")
            
            # Create price index data (100 = baseline)
            price_data = []
            
            for supplier in top_suppliers:
                # Base price index
                base_price = 100
                # Different inflation scenarios
                trend = np.random.uniform(0.2, 1.0)  # Inflation rate
                
                for i, date in enumerate(dates):
                    # Calculate price index with trend and variation
                    price_index = base_price * (1 + trend/100 * i) + np.random.normal(0, 0.5)
                    
                    price_data.append({
                        'Date': date,
                        'Supplier': supplier,
                        'Price Index': price_index
                    })
            
            # Create DataFrame
            price_df = pd.DataFrame(price_data)
            
            # Create line chart
            fig = px.line(
                price_df,
                x='Date',
                y='Price Index',
                color='Supplier',
                title="Price Index Trend (Base = 100)",
                markers=True
            )
            
            fig.update_layout(
                height=400,
                hovermode="x unified"
            )
            
            # Add baseline
            fig.add_hline(
                y=100,
                line_dash="dash",
                line_color="blue",
                annotation_text="Baseline",
                annotation_position="bottom right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost savings tracking
            st.markdown("##### Cost Savings Initiatives")
            
            # Create sample cost savings data
            savings_data = [
                {"Initiative": "Supplier Consolidation", "Target": "$250,000", "Achieved": "$210,000", "Progress": 84},
                {"Initiative": "Specification Optimization", "Target": "$180,000", "Achieved": "$125,000", "Progress": 69},
                {"Initiative": "Payment Terms Extension", "Target": "$50,000", "Achieved": "$50,000", "Progress": 100},
                {"Initiative": "Logistics Optimization", "Target": "$120,000", "Achieved": "$85,000", "Progress": 71},
                {"Initiative": "Volume Leveraging", "Target": "$300,000", "Achieved": "$175,000", "Progress": 58}
            ]
            
            # Create DataFrame
            savings_df = pd.DataFrame(savings_data)
            
            # Create horizontal bar chart for progress
            fig = px.bar(
                savings_df,
                y='Initiative',
                x='Progress',
                title="Cost Savings Progress (%)",
                orientation='h',
                color='Progress',
                color_continuous_scale='YlGn'  # Yellow to green
            )
            
            fig.update_layout(
                height=300,
                xaxis=dict(range=[0, 100])
            )
            
            # Add target line
            fig.add_vline(
                x=100,
                line_dash="dash",
                line_color="green",
                annotation_text="Target",
                annotation_position="top right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display savings details
            st.dataframe(savings_df, use_container_width=True)

# AI Co-Pilot tab
with tabs[2]:
    st.markdown('<div class="main-header">AI Procurement Co-Pilot</div>', unsafe_allow_html=True)
    st.markdown(f"#### Selected Category: {selected_category}")
    
    # Initialize session state for messages if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are an AI procurement co-pilot that provides strategic insights and recommendations on procurement categories."}
        ]
    
    # Introduction text
    st.markdown("""
    Ask me anything about your procurement category. I can help with:
    - Price trends and forecasting
    - Supplier recommendations and risk assessment
    - Cost reduction opportunities
    - Negotiation strategies
    - Market insights
    """)
    
    # Example questions
    with st.expander("Example Questions"):
        st.markdown("""
        - What's the opportunity in Steel this quarter?
        - Why is input cost up for PET resin?
        - Who are the top alternative suppliers for electronics components?
        - What's the market outlook for packaging in Europe?
        - How can I reduce costs in logistics by 10%?
        - What are the key risks in my IT services category?
        - Should I consolidate my supplier base for office supplies?
        """)
    
    # Chat interface
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.container():
                st.markdown(f"""
                <div style="padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; flex-direction: column;
                     background-color: {'#f0f2f6' if message['role'] == 'user' else '#e6f3ff'};">
                    <div><strong>{message['role'].title()}</strong></div>
                    <div style="padding-left: 1rem;">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask about your procurement category...")
    
    if user_input:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate AI response (simplified for this demo)
        ai_response = f"This is a simulated AI response about {selected_category} based on your query: '{user_input}'. In a real implementation, this would be connected to an actual LLM or AI service to provide detailed, contextual answers to procurement questions."
        
        # Add AI response to session state
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Rerun to update the UI
        st.rerun()
        
# Strategy Generator tab
with tabs[5]:
    st.markdown('<div class="main-header">Strategy Generator</div>', unsafe_allow_html=True)
    st.markdown(f"#### Selected Category: {selected_category} | Region: {', '.join(selected_region)}")
    
    # Create tabs for strategy components
    strategy_tabs = st.tabs(["Strategy Overview", "Market Analysis", "Playbook Builder", "Stakeholder Alignment"])
    
    with strategy_tabs[0]:
        st.markdown("### Current Strategy Assessment")
        
        # Current vs Target state
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Current State")
            
            # Generate current state assessment based on category
            if selected_category == "Electronics":
                current_state = """
                * Fragmented supplier base (18+ suppliers)
                * Short-term contracts (6-12 months)
                * Rising prices due to component shortages
                * Limited supplier collaboration
                * Reactive purchasing approach
                """
            elif selected_category == "Raw Materials":
                current_state = """
                * Dual sourcing strategy (2 main suppliers)
                * Annual contracts with quarterly price review
                * High price volatility and supply constraints
                * Limited visibility into sub-tier suppliers
                * Moderate supply risk exposure
                """
            elif selected_category == "Aviation":
                current_state = """
                * Single-source for critical components
                * Long-term contracts (3-5 years)
                * Quality-first approach with cost premium
                * Limited alternative suppliers qualified
                * High dependency on key suppliers
                """
            else:
                current_state = """
                * Mixed supplier strategy (6-10 suppliers)
                * Varied contract terms (6-24 months)
                * Limited category-specific expertise
                * Transaction-focused relationship
                * Minimal leverage with suppliers
                """
            
            st.markdown(current_state)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Target State")
            
            # Generate target state based on category
            if selected_category == "Electronics":
                target_state = """
                * Consolidated supplier base (5-7 strategic partners)
                * Long-term partnerships (2-3 years)
                * Early supplier involvement in design
                * Joint innovation and cost reduction
                * Price stability with volume flexibility
                """
            elif selected_category == "Raw Materials":
                target_state = """
                * Balanced portfolio (strategic partners + spot buying)
                * Index-based pricing with caps and floors
                * Improved supply chain visibility
                * Sustainability-focused supplier development
                * Alternative material qualification program
                """
            elif selected_category == "Aviation":
                target_state = """
                * Strategic dual/multi-sourcing approach
                * Performance-based contract structures
                * Supplier-led innovation program
                * Enhanced risk monitoring and mitigation
                * Balanced cost, quality and supply security
                """
            else:
                target_state = """
                * Strategic supplier consolidation
                * Value-based performance contracts
                * Category center of excellence
                * Digital procurement enablement
                * Total cost of ownership focus
                """
            
            st.markdown(target_state)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Strategy Canvas
        st.markdown("### Strategy Canvas")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # SWOT Analysis
        st.markdown("#### SWOT Analysis")
        
        swot_col1, swot_col2 = st.columns(2)
        
        with swot_col1:
            st.markdown("""
            <div class="strategy-card" style="border-left: 5px solid green;">
                <h5>Strengths</h5>
                <ul>
            """, unsafe_allow_html=True)
            
            # Generate strengths based on category
            strengths = {
                "Electronics": [
                    "Strong technical expertise in-house",
                    "Established relationships with key suppliers",
                    "Significant spend volume and leverage",
                    "Robust quality management system"
                ],
                "Raw Materials": [
                    "Established hedging capability",
                    "Diversified supplier portfolio",
                    "Strong demand forecasting process",
                    "Effective inventory management"
                ],
                "Aviation": [
                    "Long-term supplier relationships",
                    "Rigorous supplier qualification process",
                    "Strong quality control systems",
                    "Technical knowledge of components"
                ]
            }
            
            # Default strengths if category not found
            category_strengths = strengths.get(selected_category, [
                "Established procurement processes",
                "Experienced category management",
                "Stable supplier relationships",
                "Good contractual compliance"
            ])
            
            for strength in category_strengths:
                st.markdown(f"<li>{strength}</li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="strategy-card" style="border-left: 5px solid blue;">
                <h5>Opportunities</h5>
                <ul>
            """, unsafe_allow_html=True)
            
            # Generate opportunities based on category
            opportunities = {
                "Electronics": [
                    "Emerging alternative component suppliers",
                    "Digital procurement automation potential",
                    "Early supplier involvement in product design",
                    "Joint cost reduction initiatives"
                ],
                "Raw Materials": [
                    "Emerging sustainable material alternatives",
                    "Commodity price stabilization expected",
                    "Supplier consolidation for better leverage",
                    "Value-added services from key suppliers"
                ],
                "Aviation": [
                    "New suppliers entering the market",
                    "Collaborative R&D with strategic partners",
                    "Supply chain digitalization initiatives",
                    "Design optimization for material reduction"
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
        
        with swot_col2:
            st.markdown("""
            <div class="strategy-card" style="border-left: 5px solid red;">
                <h5>Weaknesses</h5>
                <ul>
            """, unsafe_allow_html=True)
            
            # Generate weaknesses based on category
            weaknesses = {
                "Electronics": [
                    "Limited visibility into sub-tier suppliers",
                    "Reactive versus strategic approach",
                    "High dependency on single sources",
                    "Limited use of advanced analytics"
                ],
                "Raw Materials": [
                    "High exposure to price volatility",
                    "Limited alternative material qualification",
                    "Reactive supplier management",
                    "Limited sustainability focus"
                ],
                "Aviation": [
                    "High dependency on key suppliers",
                    "Limited alternative supplier base",
                    "Long qualification lead times",
                    "High inventory carrying costs"
                ]
            }
            
            # Default weaknesses if category not found
            category_weaknesses = weaknesses.get(selected_category, [
                "Limited category-specific expertise",
                "Fragmented supplier base",
                "Inconsistent contract terms",
                "Limited procurement technology"
            ])
            
            for weakness in category_weaknesses:
                st.markdown(f"<li>{weakness}</li>", unsafe_allow_html=True)
            
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
                "Aviation": [
                    "Stringent regulatory requirements",
                    "Limited qualified supplier pool",
                    "Raw material shortages affecting component availability",
                    "Geopolitical tensions disrupting global supply chains"
                ]
            }
            
            # Default threats if category not found
            category_threats = threats.get(selected_category, [
                "Market consolidation reducing supplier options",
                "Cost pressures from competitors",
                "Supply chain disruptions",
                "Changing regulatory landscape"
            ])
            
            for threat in category_threats:
                st.markdown(f"<li>{threat}</li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate strategy button
        if st.button("Generate Full Strategy Document", use_container_width=True):
            st.success("Strategy document generated and ready for download")
            st.download_button(
                "Download Strategy PDF",
                data="This would be a PDF in a real implementation",
                file_name=f"{selected_category}_Strategy.pdf",
                mime="application/pdf"
            )
    
    with strategy_tabs[1]:
        st.markdown("### Market Analysis")
        
        # Market trends and insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Market Trends")
            
            # Generate market trends based on category
            if selected_category == "Electronics":
                market_trends = """
                * Semiconductor shortages expected to continue through next 2 quarters
                * Increasing demand for AI and ML components driving prices up 15-20%
                * Regionalization of supply chains accelerating
                * New entrants disrupting traditional component suppliers
                * Sustainability becoming key differentiator for suppliers
                """
            elif selected_category == "Raw Materials":
                market_trends = """
                * Commodity prices stabilizing after 18 months of volatility
                * Increased focus on sustainable and recycled materials
                * Supplier consolidation through M&A activity
                * Geopolitical tensions affecting global trade flows
                * Climate regulations impacting extraction and processing
                """
            elif selected_category == "Aviation":
                market_trends = """
                * OEM production ramp-up creating supply constraints
                * New composite materials entering qualification phase
                * Increasing regulatory focus on environmental compliance
                * Digital twins and IOT transforming MRO services
                * Supply chain resilience prioritized over pure cost savings
                """
            else:
                market_trends = """
                * Increasing supplier consolidation reducing options
                * Digital transformation accelerating across industries
                * Sustainability becoming procurement requirement
                * Supply chain regionalization and near-shoring trend
                * Service-based models replacing traditional product-only offerings
                """
            
            st.markdown(market_trends)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with strategy_tabs[2]:
        st.markdown("### Procurement Strategy Playbook Builder")
        
        # Strategy objectives section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### Strategy Objectives")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Strategic objectives based on category
            st.markdown("##### Objectives")
            
            if selected_category == "Electronics":
                objectives = [
                    "Secure supply of critical components",
                    "Reduce total cost of ownership by 12-15%",
                    "Develop strategic supplier partnerships",
                    "Increase supply chain resilience"
                ]
            elif selected_category == "Raw Materials":
                objectives = [
                    "Stabilize price volatility",
                    "Ensure security of supply",
                    "Improve sustainability metrics by 25%",
                    "Develop alternative material sources"
                ]
            elif selected_category == "Aviation":
                objectives = [
                    "Secure long-term supply agreements",
                    "Develop multi-sourcing strategy",
                    "Improve quality and compliance",
                    "Drive supplier-led innovation"
                ]
            else:
                objectives = [
                    "Optimize total cost of ownership",
                    "Develop category expertise",
                    "Increase procurement efficiency",
                    "Implement sustainability practices"
                ]
            
            for objective in objectives:
                st.markdown(f"- {objective}")
        
        with col2:
            # Key metrics based on category
            st.markdown("##### Key Performance Indicators")
            
            if selected_category == "Electronics":
                kpis = [
                    "Component lead time reduction (20%)",
                    "Cost savings vs. market (15%)",
                    "Supplier innovation contributions",
                    "Supply disruption incidents"
                ]
            elif selected_category == "Raw Materials":
                kpis = [
                    "Price variance vs. index (-10%)",
                    "Supply disruption incidents",
                    "% renewable/recycled content",
                    "Alternative material adoption rate"
                ]
            elif selected_category == "Aviation":
                kpis = [
                    "On-time delivery performance",
                    "Quality acceptance rate",
                    "Cost reduction vs. market",
                    "Innovation projects per supplier"
                ]
            else:
                kpis = [
                    "Total cost reduction (10-15%)",
                    "Supplier performance score",
                    "Process efficiency improvement",
                    "Sustainability score improvement"
                ]
            
            for kpi in kpis:
                st.markdown(f"- {kpi}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with strategy_tabs[3]:
        st.markdown("### Stakeholder Alignment")
        
        # Stakeholder analysis
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### Stakeholder Map")
        
        # Stakeholder matrix data based on category
        if selected_category == "Electronics":
            stakeholders = [
                {"Stakeholder": "Engineering", "Power": 8, "Interest": 9, "Type": "Key Player"},
                {"Stakeholder": "Operations", "Power": 7, "Interest": 8, "Type": "Key Player"},
                {"Stakeholder": "Finance", "Power": 6, "Interest": 4, "Type": "Keep Satisfied"},
                {"Stakeholder": "Quality", "Power": 5, "Interest": 7, "Type": "Keep Informed"},
                {"Stakeholder": "R&D", "Power": 8, "Interest": 6, "Type": "Key Player"},
                {"Stakeholder": "Executive Team", "Power": 9, "Interest": 5, "Type": "Keep Satisfied"}
            ]
        elif selected_category == "Raw Materials":
            stakeholders = [
                {"Stakeholder": "Production", "Power": 9, "Interest": 9, "Type": "Key Player"},
                {"Stakeholder": "Finance", "Power": 7, "Interest": 6, "Type": "Key Player"},
                {"Stakeholder": "Risk Management", "Power": 6, "Interest": 8, "Type": "Key Player"},
                {"Stakeholder": "Quality", "Power": 5, "Interest": 7, "Type": "Keep Informed"},
                {"Stakeholder": "Sustainability", "Power": 4, "Interest": 8, "Type": "Keep Informed"},
                {"Stakeholder": "Executive Team", "Power": 9, "Interest": 5, "Type": "Keep Satisfied"}
            ]
        elif selected_category == "Aviation":
            stakeholders = [
                {"Stakeholder": "Engineering", "Power": 9, "Interest": 8, "Type": "Key Player"},
                {"Stakeholder": "Quality/Compliance", "Power": 8, "Interest": 9, "Type": "Key Player"},
                {"Stakeholder": "Operations", "Power": 7, "Interest": 7, "Type": "Key Player"},
                {"Stakeholder": "Finance", "Power": 6, "Interest": 5, "Type": "Keep Satisfied"},
                {"Stakeholder": "Program Management", "Power": 8, "Interest": 8, "Type": "Key Player"},
                {"Stakeholder": "Executive Team", "Power": 9, "Interest": 6, "Type": "Keep Satisfied"}
            ]
        else:
            stakeholders = [
                {"Stakeholder": "Business Unit", "Power": 8, "Interest": 7, "Type": "Key Player"},
                {"Stakeholder": "Finance", "Power": 7, "Interest": 5, "Type": "Keep Satisfied"},
                {"Stakeholder": "Operations", "Power": 6, "Interest": 8, "Type": "Key Player"},
                {"Stakeholder": "Legal", "Power": 5, "Interest": 4, "Type": "Monitor"},
                {"Stakeholder": "Risk Management", "Power": 5, "Interest": 6, "Type": "Keep Informed"},
                {"Stakeholder": "Executive Team", "Power": 9, "Interest": 5, "Type": "Keep Satisfied"}
            ]
        
        # Create DataFrame
        import pandas as pd
        df = pd.DataFrame(stakeholders)
        
        # Display as a styled table
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Opportunity Engine tab
with tabs[6]:
    st.markdown('<div class="main-header">Opportunity Engine</div>', unsafe_allow_html=True)
    st.markdown(f"#### Selected Category: {selected_category} | Region: {', '.join(selected_region)}")
    
    # Create tabs for different opportunity views
    opportunity_tabs = st.tabs(["Opportunity Dashboard", "Market Triggers", "Contract Opportunities", "Supply Alerts"])
    
    with opportunity_tabs[0]:
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        import numpy as np
        
        with col1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            total_opportunities = np.random.randint(8, 25)
            st.metric("Total Opportunities", total_opportunities, delta=f"{np.random.randint(-3, 7)}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            potential_savings = np.random.randint(500, 3000)
            st.metric("Potential Savings", f"${potential_savings}K", delta=f"{np.random.randint(-10, 20)}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            avg_roi = np.random.randint(300, 800)
            st.metric("Average ROI", f"{avg_roi}%", delta=f"{np.random.randint(-50, 100)}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            implementation_time = np.random.randint(2, 12)
            st.metric("Avg. Implementation", f"{implementation_time} weeks", delta=f"{np.random.randint(-2, 3)} weeks")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Opportunity breakdown
        st.markdown("### Opportunity Breakdown")
        
        # Generate opportunity types and counts
        opp_types = ["Cost Reduction", "Risk Mitigation", "Innovation", "Sustainability"]
        opp_counts = np.random.randint(2, 8, size=len(opp_types))
        
        # Create pie chart
        import plotly.express as px
        
        fig = px.pie(
            names=opp_types,
            values=opp_counts,
            title="Opportunities by Type",
            color_discrete_sequence=px.colors.sequential.Oranges
        )
        
        fig.update_layout(
            height=350,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top opportunities list
        st.markdown("### Top Opportunities")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Generate opportunities based on category
        if selected_category == "Electronics":
            opportunities = [
                {
                    "title": "Component Consolidation Program",
                    "type": "Cost Reduction",
                    "impact": "High",
                    "effort": "Medium",
                    "savings": "$420K",
                    "timeline": "3-6 months"
                },
                {
                    "title": "Early Supplier Involvement Initiative",
                    "type": "Innovation",
                    "impact": "High",
                    "effort": "Medium",
                    "savings": "$350K",
                    "timeline": "6-9 months"
                },
                {
                    "title": "Alternative Supplier Qualification",
                    "type": "Risk Mitigation",
                    "impact": "Medium",
                    "effort": "High",
                    "savings": "$180K",
                    "timeline": "9-12 months"
                }
            ]
        elif selected_category == "Raw Materials":
            opportunities = [
                {
                    "title": "Index-based Pricing Transition",
                    "type": "Cost Reduction",
                    "impact": "High",
                    "effort": "Medium",
                    "savings": "$520K",
                    "timeline": "2-4 months"
                },
                {
                    "title": "Supply Chain Mapping",
                    "type": "Risk Mitigation",
                    "impact": "High",
                    "effort": "Medium",
                    "savings": "$320K",
                    "timeline": "3-5 months"
                },
                {
                    "title": "Recycled Material Qualification",
                    "type": "Sustainability",
                    "impact": "Medium",
                    "effort": "High",
                    "savings": "$220K",
                    "timeline": "6-9 months"
                }
            ]
        elif selected_category == "Aviation":
            opportunities = [
                {
                    "title": "Multi-Sourcing Critical Components",
                    "type": "Risk Mitigation",
                    "impact": "High",
                    "effort": "High",
                    "savings": "$650K",
                    "timeline": "9-12 months"
                },
                {
                    "title": "Performance-Based Contracting",
                    "type": "Cost Reduction",
                    "impact": "High",
                    "effort": "Medium",
                    "savings": "$480K",
                    "timeline": "4-6 months"
                },
                {
                    "title": "Supplier Innovation Program",
                    "type": "Innovation",
                    "impact": "Medium",
                    "effort": "Medium",
                    "savings": "$320K",
                    "timeline": "6-9 months"
                }
            ]
        else:
            opportunities = [
                {
                    "title": "Supplier Consolidation",
                    "type": "Cost Reduction",
                    "impact": "High",
                    "effort": "Medium",
                    "savings": "$380K",
                    "timeline": "3-6 months"
                },
                {
                    "title": "Specification Standardization",
                    "type": "Cost Reduction",
                    "impact": "Medium",
                    "effort": "Low",
                    "savings": "$220K",
                    "timeline": "2-3 months"
                },
                {
                    "title": "Digital Procurement Enablement",
                    "type": "Innovation",
                    "impact": "Medium",
                    "effort": "High",
                    "savings": "$290K",
                    "timeline": "6-9 months"
                }
            ]
        
        # Display opportunities
        for opp in opportunities:
            # Determine impact color
            impact_color = "green" if opp["impact"] == "High" else "orange" if opp["impact"] == "Medium" else "red"
            
            # Determine effort icon
            effort_icon = "🟢" if opp["effort"] == "Low" else "🟠" if opp["effort"] == "Medium" else "🔴"
            
            st.markdown(f"""
            <div style="padding: 15px; margin-bottom: 15px; border-left: 5px solid {impact_color}; background-color: #f8f9fa;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{opp['title']}</h4>
                    <span style="font-weight: bold; color: green;">{opp['savings']} potential</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <span><strong>Type:</strong> {opp['type']}</span>
                    <span><strong>Impact:</strong> <span style="color: {impact_color};">{opp['impact']}</span></span>
                    <span><strong>Effort:</strong> {effort_icon} {opp['effort']}</span>
                    <span><strong>Timeline:</strong> {opp['timeline']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add action buttons for each opportunity
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button(f"View Details", key=f"view_{opp['title'].replace(' ', '_')}")
            with col2:
                st.button(f"Create Project", key=f"project_{opp['title'].replace(' ', '_')}")
            with col3:
                st.button(f"Assign Owner", key=f"assign_{opp['title'].replace(' ', '_')}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with opportunity_tabs[1]:
        st.markdown("### Market Trigger Analysis")
        st.markdown("Market events that create procurement opportunities")
        
        # Market trigger alerts
        import datetime
        
        # Generate appropriate triggers based on category
        if selected_category == "Electronics":
            triggers = [
                {
                    "event": "TSMC Announces 7% Price Reduction for 5nm Process",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%b %d, %Y"),
                    "impact": "High",
                    "opportunity": "Renegotiate component pricing with suppliers using TSMC processes"
                },
                {
                    "event": "New Entrant in Display Panel Market",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=12)).strftime("%b %d, %Y"),
                    "impact": "Medium",
                    "opportunity": "Evaluate alternative supplier for display components"
                },
                {
                    "event": "Copper Price Down 8% Quarter-over-Quarter",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=18)).strftime("%b %d, %Y"),
                    "impact": "Medium",
                    "opportunity": "Review pricing of copper-intensive components"
                }
            ]
        elif selected_category == "Raw Materials":
            triggers = [
                {
                    "event": "Steel Tariffs Reduced by 12% in Major Exporting Country",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%b %d, %Y"),
                    "impact": "High",
                    "opportunity": "Reassess supplier mix to take advantage of reduced tariffs"
                },
                {
                    "event": "New Aluminum Recycling Facility Online",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%b %d, %Y"),
                    "impact": "Medium",
                    "opportunity": "Explore recycled aluminum sourcing options"
                },
                {
                    "event": "Commodity Index Forecasting 5% Reduction in Q3",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=21)).strftime("%b %d, %Y"),
                    "impact": "Medium",
                    "opportunity": "Adjust hedging strategy for upcoming quarter"
                }
            ]
        elif selected_category == "Aviation":
            triggers = [
                {
                    "event": "Major OEM Announces 15% Production Increase",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%b %d, %Y"),
                    "impact": "High",
                    "opportunity": "Secure capacity commitments before market tightens"
                },
                {
                    "event": "New Composite Material Receives Certification",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=13)).strftime("%b %d, %Y"),
                    "impact": "Medium",
                    "opportunity": "Evaluate weight/cost benefits of new material"
                },
                {
                    "event": "Aircraft Component Supplier M&A Activity",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=19)).strftime("%b %d, %Y"),
                    "impact": "Medium",
                    "opportunity": "Review supplier strategy in light of market consolidation"
                }
            ]
        else:
            triggers = [
                {
                    "event": "Industry Benchmark Shows 12% Savings from Digital Procurement",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%b %d, %Y"),
                    "impact": "High",
                    "opportunity": "Accelerate digital procurement transformation"
                },
                {
                    "event": "Key Supplier Announces Expansion",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=16)).strftime("%b %d, %Y"),
                    "impact": "Medium",
                    "opportunity": "Renegotiate agreement with volume commitments"
                },
                {
                    "event": "New Sustainability Regulation Announced",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=23)).strftime("%b %d, %Y"),
                    "impact": "Medium",
                    "opportunity": "Assess compliance and revise specifications"
                }
            ]
        
        # Display market triggers
        for trigger in triggers:
            impact_color = "red" if trigger["impact"] == "High" else "orange" if trigger["impact"] == "Medium" else "green"
            
            st.markdown(f"""
            <div style="padding: 15px; margin-bottom: 15px; border-left: 5px solid {impact_color}; background-color: #f8f9fa;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{trigger['event']}</h4>
                    <span style="color: #666;">{trigger['date']}</span>
                </div>
                <div style="margin-top: 10px;">
                    <p><strong>Impact:</strong> <span style="color: {impact_color};">{trigger['impact']}</span></p>
                    <p><strong>Opportunity:</strong> {trigger['opportunity']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with opportunity_tabs[2]:
        st.markdown("### Contract Opportunity Analysis")
        
        # Generate contract opportunities
        contracts = [
            {
                "supplier": f"{selected_category} Supplier A",
                "category": selected_category,
                "expiration": (datetime.datetime.now() + datetime.timedelta(days=45)).strftime("%b %d, %Y"),
                "annual_value": f"${np.random.randint(300, 900)}K",
                "opportunity": "Consolidation and rate negotiation",
                "days_left": 45,
                "savings_potential": f"{np.random.randint(8, 15)}%"
            },
            {
                "supplier": f"{selected_category} Supplier B",
                "category": selected_category,
                "expiration": (datetime.datetime.now() + datetime.timedelta(days=90)).strftime("%b %d, %Y"),
                "annual_value": f"${np.random.randint(200, 700)}K",
                "opportunity": "Specification optimization",
                "days_left": 90,
                "savings_potential": f"{np.random.randint(5, 12)}%"
            },
            {
                "supplier": f"{selected_category} Supplier C",
                "category": selected_category,
                "expiration": (datetime.datetime.now() + datetime.timedelta(days=120)).strftime("%b %d, %Y"),
                "annual_value": f"${np.random.randint(100, 500)}K",
                "opportunity": "Volume leveraging with Supplier A",
                "days_left": 120,
                "savings_potential": f"{np.random.randint(7, 18)}%"
            }
        ]
        
        # Display contract opportunities in a table
        contract_df = pd.DataFrame(contracts)
        st.dataframe(contract_df, use_container_width=True)
        
        # Display upcoming expirations on a timeline
        st.markdown("### Contract Expiration Timeline")
        
        # Convert days left to coordinates for timeline
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        # Create the timeline
        for i, contract in enumerate(contracts):
            fig.add_trace(go.Scatter(
                x=[contract["days_left"]],
                y=[i],
                mode="markers+text",
                marker=dict(
                    symbol="diamond",
                    size=16,
                    color="#ff6b18"
                ),
                text=[contract["supplier"]],
                textposition="middle right",
                name=contract["supplier"]
            ))
        
        # Configure the layout
        fig.update_layout(
            title="Days Until Contract Expiration",
            xaxis=dict(
                title="Days Remaining",
                range=[0, 180],
                tickvals=[0, 30, 60, 90, 120, 150, 180],
                ticktext=["0", "30", "60", "90", "120", "150", "180"]
            ),
            yaxis=dict(
                showticklabels=False
            ),
            height=250
        )
        
        # Add colored regions for urgency
        fig.add_shape(
            type="rect",
            x0=0,
            x1=30,
            y0=-1,
            y1=len(contracts),
            fillcolor="rgba(255, 0, 0, 0.1)",
            line=dict(width=0)
        )
        
        fig.add_shape(
            type="rect",
            x0=30,
            x1=90,
            y0=-1,
            y1=len(contracts),
            fillcolor="rgba(255, 165, 0, 0.1)",
            line=dict(width=0)
        )
        
        fig.add_shape(
            type="rect",
            x0=90,
            x1=180,
            y0=-1,
            y1=len(contracts),
            fillcolor="rgba(0, 128, 0, 0.1)",
            line=dict(width=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with opportunity_tabs[3]:
        st.markdown("### Supply Market Alert")
        
        # Generate supply market alerts based on category
        if selected_category == "Electronics":
            alerts = [
                {
                    "title": "Semiconductor Capacity Expansion",
                    "description": "Multiple fabs announcing 10-15% capacity increases over next 6 months",
                    "impact": "Potential price softening in Q3-Q4",
                    "recommendation": "Delay long-term commitments where possible",
                    "status": "Monitoring"
                },
                {
                    "title": "Memory Supply Glut",
                    "description": "DRAM/NAND inventories 35% above normal levels",
                    "impact": "Prices expected to drop 8-12% in next quarter",
                    "recommendation": "Negotiate spot purchases and reduced contract prices",
                    "status": "Action Required"
                }
            ]
        elif selected_category == "Raw Materials":
            alerts = [
                {
                    "title": "Aluminum Production Increases",
                    "description": "Global production up 7% vs. forecasted 3% growth",
                    "impact": "Downward price pressure expected in next 2-3 months",
                    "recommendation": "Delay contract renewals, consider spot purchases",
                    "status": "Action Required"
                },
                {
                    "title": "Steel Mill Utilization Dropping",
                    "description": "Utilization rates down to 72% from 85% last quarter",
                    "impact": "Price concessions likely available from mills",
                    "recommendation": "Renegotiate existing agreements",
                    "status": "Action Required"
                }
            ]
        elif selected_category == "Aviation":
            alerts = [
                {
                    "title": "Titanium Production Exceeding Demand",
                    "description": "7% global oversupply detected in aerospace-grade titanium",
                    "impact": "Price stabilization after 24 months of increases",
                    "recommendation": "Reconsider long-term hedging strategy",
                    "status": "Monitoring"
                },
                {
                    "title": "Carbon Fiber Capacity Expansion",
                    "description": "Two major producers increasing capacity by Q3",
                    "impact": "Potential price competition and improved lead times",
                    "recommendation": "Initiate discussions with alternative suppliers",
                    "status": "Action Required"
                }
            ]
        else:
            alerts = [
                {
                    "title": "Market Overcapacity Detected",
                    "description": "Supplier utilization rates declining across category",
                    "impact": "Favorable negotiating environment",
                    "recommendation": "Initiate RFP process for major contracts",
                    "status": "Action Required"
                },
                {
                    "title": "New Market Entrants",
                    "description": "Three new suppliers entered market in past quarter",
                    "impact": "Increased competition among suppliers",
                    "recommendation": "Assess new entrants for potential qualification",
                    "status": "Monitoring"
                }
            ]
        
        # Display supply alerts
        for alert in alerts:
            status_color = "orange" if alert["status"] == "Action Required" else "blue"
            
            st.markdown(f"""
            <div style="padding: 15px; margin-bottom: 15px; border-left: 5px solid {status_color}; background-color: #f8f9fa;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{alert['title']}</h4>
                    <span style="font-weight: bold; color: {status_color};">{alert['status']}</span>
                </div>
                <p><strong>Alert:</strong> {alert['description']}</p>
                <p><strong>Impact:</strong> {alert['impact']}</p>
                <p><strong>Recommendation:</strong> {alert['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add action buttons
            col1, col2 = st.columns(2)
            with col1:
                st.button("Accept Recommendation", key=f"accept_{alert['title'].replace(' ', '_')}")
            with col2:
                st.button("Dismiss Alert", key=f"dismiss_{alert['title'].replace(' ', '_')}")

# Web Scraping Demo tab
with tabs[7]:
    render_web_scraping_demo()
    
    # Create tabs for different data operations
    data_tabs = st.tabs(["Web Scraping", "Import Data", "Export Data", "API Integration"])
    
    with data_tabs[0]:
        st.markdown("### Web Scraping Tool")
        st.markdown("Extract data from websites to gather market intelligence and pricing information.")
        
        # Create columns for URL entry and source suggestion
        col1, col2 = st.columns([3, 2])
        
        with col1:
            scrape_url = st.text_input("Enter URL to scrape", "https://example.com")
        
        with col2:
            st.markdown("#### Need Ideas?")
            if st.button("Suggest Sources", use_container_width=True):
                # Show suggested sources based on category
                st.success("Here are recommended sources for market intelligence")
                
                # Define sources by category
                sources_by_category = {
                    "Electronics": [
                        {"name": "DigiTimes", "url": "https://www.digitimes.com/", "description": "Semiconductor and electronics industry news"},
                        {"name": "Bloomberg Tech", "url": "https://www.bloomberg.com/technology", "description": "Technology market trends and forecasts"},
                        {"name": "IHS Markit", "url": "https://ihsmarkit.com/industry/technology.html", "description": "Electronics component pricing and forecasts"}
                    ],
                    "Raw Materials": [
                        {"name": "MetalPrices.com", "url": "https://www.metalprices.com/", "description": "Metal commodity pricing data"},
                        {"name": "Mining.com", "url": "https://www.mining.com/", "description": "Mining and metals market news"},
                        {"name": "S&P Global Commodity Insights", "url": "https://www.spglobal.com/commodityinsights/", "description": "Commodity market analysis"}
                    ],
                    "Aviation": [
                        {"name": "Aviation Week", "url": "https://aviationweek.com/", "description": "Aviation industry news and market insights"},
                        {"name": "FlightGlobal", "url": "https://www.flightglobal.com/", "description": "Aerospace industry data and trends"},
                        {"name": "AviationPros", "url": "https://www.aviationpros.com/", "description": "Aviation maintenance and parts pricing"}
                    ],
                    "Chemicals": [
                        {"name": "ICIS", "url": "https://www.icis.com/", "description": "Chemical price reporting and market intelligence"},
                        {"name": "Chemical Week", "url": "https://chemweek.com/", "description": "Chemical industry news and analysis"},
                        {"name": "ChemAnalyst", "url": "https://www.chemanalyst.com/", "description": "Chemical price forecasts and procurement insights"}
                    ],
                }
                
                # Show sources for the selected category or general sources
                if selected_category in sources_by_category:
                    sources = sources_by_category[selected_category]
                else:
                    # General procurement sources for categories without specific entries
                    sources = [
                        {"name": "Institute for Supply Management", "url": "https://www.ismworld.org/", "description": "Supply management insights and reports"},
                        {"name": "Supply Chain Dive", "url": "https://www.supplychaindive.com/", "description": "Procurement and supply chain news"},
                        {"name": "Spend Matters", "url": "https://spendmatters.com/", "description": "Procurement market intelligence"}
                    ]
                
                # Display sources in expandable cards
                for i, source in enumerate(sources):
                    with st.expander(f"{source['name']}", expanded=i==0):
                        st.markdown(f"**URL**: [{source['url']}]({source['url']})")
                        st.markdown(f"**Description**: {source['description']}")
                        if st.button(f"Use this source", key=f"source_{i}", use_container_width=True):
                            scrape_url = source['url']
                            st.session_state.scrape_url = source['url']
                            st.rerun()
        
        # Action buttons
        action_col1, action_col2 = st.columns([1, 1])
        
        with action_col1:
            scrape_button = st.button("Scrape Website Content", use_container_width=True)
        
        with action_col2:
            analyze_button = st.button("Analyze Scraped Content", use_container_width=True)
        
        # Display scraped content
        if scrape_button:
            with st.spinner("Scraping website content..."):
                import time
                time.sleep(1.5)  # Simulate scraping delay
                
                try:
                    # Simulated scraping response
                    st.success("Successfully scraped website content.")
                    
                    # Add card styling to the results
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(f"### Content from {scrape_url}")
                    
                    if "digitimes" in scrape_url.lower():
                        content_type = "Electronics Market Intelligence"
                        content = "Semiconductor Supply Chain Faces New Challenges in Q2 2025\n\nThe global semiconductor industry continues to face supply constraints for key components. TSMC announced a 7% price increase for advanced nodes, while Samsung is expanding capacity by 15% to meet growing demand for AI chips. Memory prices are expected to rise by 8-12% next quarter due to increased demand from data centers."
                    elif "metal" in scrape_url.lower() or "mining" in scrape_url.lower():
                        content_type = "Raw Materials Price Report"
                        content = "Steel Market Update - May 2025\n\nHot-rolled coil prices declined 5.2% month-over-month due to reduced construction activity in North America. Aluminum spot prices remain stable with slight upward pressure from energy costs. Copper continues strong performance, rising 8.3% quarter-over-quarter driven by electrification trends and supply disruptions in Chile."
                    elif "aviation" in scrape_url.lower() or "flight" in scrape_url.lower():
                        content_type = "Aviation Industry Report"
                        content = "Aerospace Components Market Trends - Q2 2025\n\nTitanium prices have increased 12% year-to-date due to supply constraints and increased defense spending. Carbon fiber demand exceeds supply by approximately 8% for aerospace grade materials. Jet fuel prices have stabilized following a volatile Q1, with current prices 3% below January levels."
                    else:
                        content_type = "General Market Intelligence"
                        content = "Global Procurement Trends - May 2025\n\nSupply chain disruptions continue to affect lead times across multiple industries. Transportation costs have increased 7% year-over-year with ocean freight seeing the highest increases. Raw material inflation is showing signs of moderation with the exception of specialized metals and certain agricultural commodities."
                    
                    st.markdown(f"**Content Type**: {content_type}")
                    st.text_area("Extracted Content", content, height=250)
                    
                    # Add structured data extraction
                    st.markdown("### Structured Data Extraction")
                    
                    extracted_col1, extracted_col2 = st.columns(2)
                    
                    with extracted_col1:
                        # Key trends extraction
                        st.markdown("#### Key Trends")
                        trends = content.split("\n\n")[1].split(". ")
                        for trend in trends:
                            if trend:
                                st.markdown(f"- {trend}")
                    
                    with extracted_col2:
                        # Price changes extraction
                        st.markdown("#### Detected Price Changes")
                        import re
                        
                        # Find percentages with regex
                        percentages = re.findall(r'(\d+(?:\.\d+)?)%', content)
                        items = re.findall(r'([A-Z][a-z]+(?:\s[a-z]+)*)\s(?:prices|increased|declined|rising|decreased)', content)
                        
                        if percentages and items:
                            # Create a dataframe of detected price changes
                            import pandas as pd
                            price_data = []
                            for i in range(min(len(percentages), len(items))):
                                direction = "Increase" if any(word in content for word in ["increased", "rising", "up"]) else "Decrease"
                                price_data.append({"Item": items[i], "Change": f"{direction} {percentages[i]}%"})
                            
                            price_df = pd.DataFrame(price_data)
                            st.dataframe(price_df, use_container_width=True)
                        else:
                            st.info("No specific price changes detected in the text.")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Add action buttons for further analysis
                    st.markdown("### Actions")
                    action_row = st.columns(3)
                    with action_row[0]:
                        if st.button("Generate Price Report", use_container_width=True):
                            st.session_state.generate_report = True
                    
                    with action_row[1]:
                        if st.button("Extract Key Suppliers", use_container_width=True):
                            st.session_state.extract_suppliers = True
                            
                    with action_row[2]:
                        if st.button("Save to Database", use_container_width=True):
                            with st.spinner("Saving data..."):
                                time.sleep(1)
                                st.success("Data saved to procurement database")
                    
                    # Show generated report if requested
                    if "generate_report" in st.session_state and st.session_state.generate_report:
                        st.markdown("### Price Report")
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown("#### Price Trend Analysis")
                        st.markdown("The following price changes were detected in the scraped content:")
                        
                        # Create a sample visualization of extracted prices
                        import plotly.graph_objects as go
                        import numpy as np
                        
                        # Generate some sample price trend data based on the scraped content
                        if "metal" in scrape_url.lower() or "steel" in content.lower():
                            items = ["Steel", "Aluminum", "Copper"]
                            changes = [-5.2, 1.8, 8.3]
                        elif "aviation" in scrape_url.lower():
                            items = ["Titanium", "Carbon Fiber", "Jet Fuel"]
                            changes = [12.0, 8.0, -3.0]
                        else:
                            items = ["Component A", "Component B", "Component C"]
                            changes = [7.0, -2.5, 4.3]
                        
                        # Create bar chart
                        fig = go.Figure()
                        colors = ['#ff6b18' if c > 0 else '#1e7145' for c in changes]
                        
                        fig.add_trace(go.Bar(
                            x=items,
                            y=changes,
                            marker_color=colors,
                            text=[f"{c:+.1f}%" for c in changes],
                            textposition='outside'
                        ))
                        
                        fig.update_layout(
                            title="Price Changes by Component",
                            yaxis_title="Percent Change",
                            height=400,
                            margin=dict(l=40, r=40, t=40, b=40)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Show supplier extraction if requested
                    if "extract_suppliers" in st.session_state and st.session_state.extract_suppliers:
                        st.markdown("### Supplier Information")
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown("#### Detected Suppliers")
                        
                        # Extract supplier names from content
                        if "tsmc" in content.lower() or "samsung" in content.lower():
                            suppliers = [
                                {"name": "TSMC", "category": "Semiconductor", "market_share": "53%", "pricing_trend": "Increasing"},
                                {"name": "Samsung", "category": "Semiconductor", "market_share": "17%", "pricing_trend": "Increasing"}
                            ]
                        elif "aviation" in scrape_url.lower():
                            suppliers = [
                                {"name": "Boeing", "category": "Aircraft", "market_share": "45%", "pricing_trend": "Stable"},
                                {"name": "Airbus", "category": "Aircraft", "market_share": "43%", "pricing_trend": "Increasing"},
                                {"name": "Rolls-Royce", "category": "Engines", "market_share": "23%", "pricing_trend": "Increasing"}
                            ]
                        else:
                            suppliers = [
                                {"name": "Supplier A", "category": selected_category, "market_share": "34%", "pricing_trend": "Increasing"},
                                {"name": "Supplier B", "category": selected_category, "market_share": "28%", "pricing_trend": "Stable"},
                                {"name": "Supplier C", "category": selected_category, "market_share": "12%", "pricing_trend": "Decreasing"}
                            ]
                            
                        # Show supplier table
                        import pandas as pd
                        supplier_df = pd.DataFrame(suppliers)
                        st.dataframe(supplier_df, use_container_width=True)
                        
                        # Add a chart for supplier market share
                        fig = px.pie(
                            supplier_df, 
                            names='name', 
                            values=[float(s["market_share"].strip('%')) for s in suppliers],
                            title="Supplier Market Share",
                            color_discrete_sequence=px.colors.sequential.Oranges_r
                        )
                        
                        fig.update_layout(
                            height=300,
                            margin=dict(l=40, r=40, t=40, b=40)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error scraping website: {str(e)}. Please check the URL and try again.")
                
    with data_tabs[1]:
        st.markdown("### Import Data")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Upload Files")
            # File uploader for various data formats
            uploaded_file = st.file_uploader(
                "Upload procurement data file", 
                type=["csv", "xlsx", "json"], 
                help="Upload your procurement data for analysis"
            )
            
            # Mock data upload option
            st.markdown("#### Demo with Mock Data")
            st.markdown("Try the application with pre-loaded sample data")
            
            mock_data_options = [
                "Select sample dataset...",
                "Q1 2023 Spend Analysis",
                "Annual Supplier Performance",
                "Aviation Components Price Trends",
                "Global Risk Assessment",
                "Commodity Price Forecasts"
            ]
            
            mock_dataset = st.selectbox("Sample datasets", mock_data_options)
            
            if st.button("Load Sample Data", key="load_sample"):
                with st.spinner("Loading sample data..."):
                    import time
                    time.sleep(1)  # Simulate loading
                    st.success(f"Successfully loaded: {mock_dataset}")
                    st.session_state.mock_data_loaded = True
                    
            if "mock_data_loaded" in st.session_state and st.session_state.mock_data_loaded:
                st.markdown('<div style="padding: 1rem; background-color: #f8f9fa; border-left: 3px solid #ff6b18; margin-top: 1rem;">', unsafe_allow_html=True)
                st.markdown(f"**{mock_dataset}** is loaded and ready for analysis")
                st.markdown("Sample data contains:")
                st.markdown("- 24 months of historical data")
                st.markdown("- 15 suppliers with performance metrics")
                st.markdown("- 8 risk categories with assessments")
                st.markdown("- Price trends for key commodities")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Import from Systems")
            
            data_source = st.selectbox(
                "Import from connected system",
                ["Select system...", "SAP", "Oracle", "Coupa", "Ariba", "Custom API"]
            )
            
            if uploaded_file is not None:
                st.success(f"File uploaded: {uploaded_file.name}")
                
                # Preview of uploaded data
                st.markdown("#### Data Preview")
                
                preview_tab1, preview_tab2 = st.tabs(["Table Preview", "Data Summary"])
                
                with preview_tab1:
                    st.markdown("First 5 rows of data would appear here")
                    st.info("In a production environment, this would display a preview of the uploaded data.")
                
                with preview_tab2:
                    st.markdown("##### Data Summary")
                    st.markdown("- **Rows**: 1,245")
                    st.markdown("- **Columns**: 8")
                    st.markdown("- **Date Range**: Jan 2023 - Feb 2025")
                    st.markdown("- **Missing Values**: None")
                
                if st.button("Import Data", key="import_data"):
                    with st.spinner("Importing data..."):
                        import time
                        time.sleep(1.5)  # Simulate processing
                        st.success("Data successfully imported!")
                
            if data_source != "Select system...":
                st.info(f"Connect to {data_source} to import procurement data")
                
                # Connection form 
                with st.expander(f"Configure {data_source} connection"):
                    col1, col2 = st.columns(2)
                    with col1:
                        server = st.text_input("Server URL")
                        username = st.text_input("Username")
                    with col2:
                        port = st.text_input("Port")
                        password = st.text_input("Password", type="password")
                        
                    if st.button("Test Connection"):
                        with st.spinner("Testing connection..."):
                            import time
                            time.sleep(1)  # Simulate connection test
                            st.success("Connection test successful!")
                    
    with data_tabs[2]:
        st.markdown("### Export Data")
        
        # Export options
        export_format = st.selectbox(
            "Export format",
            ["CSV", "Excel", "JSON", "PDF Report", "PowerPoint"]
        )
        
        export_data = st.selectbox(
            "Select data to export",
            ["Category Analysis", "Supplier Data", "Price Trends", "Risk Assessment", "Complete Dashboard"]
        )
        
        include_charts = st.checkbox("Include visualizations", value=True)
        
        if st.button("Generate Export"):
            st.success(f"{export_data} successfully exported as {export_format}")
            st.download_button(
                label=f"Download {export_format} file",
                data="Sample export data content",
                file_name=f"{export_data.lower().replace(' ', '_')}.{export_format.lower()}",
                mime="application/octet-stream"
            )
            
    with data_tabs[3]:
        st.markdown("### API Integration")
        
        api_source = st.selectbox(
            "Select API integration",
            ["Select API...", "Market Data API", "Commodity Price API", "Supplier Database API", "Custom API"]
        )
        
        if api_source != "Select API...":
            st.text_input("API Key", type="password")
            st.text_input("API Endpoint URL", f"https://api.example.com/{api_source.lower().replace(' ', '_')}")
            
            st.markdown("### API Parameters")
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Category", value=selected_category)
                st.date_input("Start Date")
            
            with col2:
                st.text_input("Region", value=", ".join(selected_region))
                st.date_input("End Date")
                
            if st.button("Test API Connection"):
                st.success("API connection successful!")
                
            if st.button("Fetch Data from API"):
                with st.spinner("Fetching data..."):
                    import time
                    time.sleep(1)  # Simulate API call
                    st.success("Data successfully retrieved from API")
                    
                    # Show sample data
                    st.markdown("### Sample API Response")
                    st.json({
                        "status": "success",
                        "data": {
                            "category": selected_category,
                            "timestamps": ["2023-01-01", "2023-02-01", "2023-03-01"],
                            "prices": [125.7, 130.2, 128.5],
                            "volume": [1200, 1350, 1275],
                            "trend": "stable"
                        },
                        "message": "Data retrieved successfully"
                    })
