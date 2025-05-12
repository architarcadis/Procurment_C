import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.data_generator import generate_price_trend_data
from utils.forecasting import simple_forecast, advanced_forecast, should_cost_model
from utils.scraper import get_commodity_prices

# Configure page
st.set_page_config(
    page_title="Price & Cost Modeling - Procurement Command Center",
    page_icon="💵",
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
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# 💵 Price & Cost Modeling")
    st.markdown("---")
    
    # Category selector
    categories = ["Electronics", "Raw Materials", "Packaging", "Office Supplies", 
                 "IT Services", "Logistics", "Chemicals", "Machinery"]
    selected_category = st.selectbox("Category", categories)
    
    # Material/item selector based on category
    if selected_category == "Electronics":
        materials = ["Semiconductors", "PCBs", "Displays", "Connectors", "Batteries"]
    elif selected_category == "Raw Materials":
        materials = ["Steel", "Aluminum", "Copper", "Zinc", "Plastic Resin"]
    elif selected_category == "Packaging":
        materials = ["Cardboard", "PET", "HDPE", "Plastic Film", "Paper"]
    elif selected_category == "Chemicals":
        materials = ["Solvents", "Polymers", "Catalysts", "Additives", "Resins"]
    elif selected_category == "Office Supplies":
        materials = ["Paper", "Toner", "Furniture", "Stationery", "Equipment"]
    elif selected_category == "Logistics":
        materials = ["Ocean Freight", "Air Freight", "Road Transport", "Warehousing", "Last Mile"]
    else:
        materials = ["Component A", "Component B", "Component C", "Raw Material X", "Service Y"]
    
    selected_material = st.selectbox("Material/Item", materials)
    
    # Time period selector
    time_periods = ["Last 6 Months", "Last Year", "Last 2 Years", "Last 3 Years"]
    time_period = st.selectbox("Time Period", time_periods)
    
    # Forecast period
    forecast_periods = [3, 6, 12, 24]
    forecast_period = st.selectbox("Forecast Periods (Months)", forecast_periods)
    
    # Forecast model
    forecast_models = ["Simple Trend", "Advanced (ML-Based)"]
    forecast_model = st.selectbox("Forecast Model", forecast_models)
    
    # Additional filters
    st.markdown("---")
    st.markdown("### Additional Filters")
    
    regions = ["Global", "North America", "Europe", "Asia", "Latin America"]
    selected_region = st.selectbox("Region", regions)
    
    currencies = ["USD", "EUR", "GBP", "JPY", "CNY"]
    selected_currency = st.selectbox("Currency", currencies)
    
    # Actions
    st.markdown("---")
    st.button("Export Data", use_container_width=True)

# Main content
st.markdown('<div class="main-header">Price & Cost Modeling</div>', unsafe_allow_html=True)
st.markdown(f"#### Selected Category: {selected_category} | Material: {selected_material}")

# Create tabs for different analyses
tab1, tab2, tab3 = st.tabs(["Price Trends & Forecasting", "Should-Cost Modeling", "Input Cost Analysis"])

with tab1:
    st.markdown("### Price Trends & Forecasting")
    
    # Get price trend data
    price_data = generate_price_trend_data(selected_category, selected_material)
    
    # Generate forecast
    if forecast_model == "Simple Trend":
        forecast_data = simple_forecast(price_data, forecast_period)
    else:
        forecast_data = advanced_forecast(price_data, forecast_period)
    
    # Plot historical + forecasted data
    fig = px.line(
        forecast_data, 
        x="Date", 
        y="Price", 
        color="Type",
        title=f"{selected_material} Price Trend & Forecast",
        color_discrete_map={"Historical": "#0066cc", "Forecast": "#ff9900"}
    )
    
    # Add confidence interval for forecasted section (just for visual effect)
    forecast_only = forecast_data[forecast_data["Type"] == "Forecast"]
    historical_end_price = forecast_data[forecast_data["Type"] == "Historical"]["Price"].iloc[-1]
    
    # Create upper and lower bounds growing with time
    upper_bound = []
    lower_bound = []
    dates = forecast_only["Date"].tolist()
    prices = forecast_only["Price"].tolist()
    
    for i, price in enumerate(prices):
        # Increase uncertainty over time
        uncertainty = 0.05 + (i * 0.01)
        upper_bound.append(price * (1 + uncertainty))
        lower_bound.append(max(0, price * (1 - uncertainty)))
    
    # Add confidence interval
    fig.add_trace(
        go.Scatter(
            x=dates + dates[::-1],
            y=upper_bound + lower_bound[::-1],
            fill='toself',
            fillcolor='rgba(255, 153, 0, 0.2)',
            line=dict(color='rgba(255, 153, 0, 0)'),
            hoverinfo="skip",
            showlegend=False
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Price analysis metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Current price vs. historical average
    current_price = price_data["Price"].iloc[-1]
    avg_price = price_data["Price"].mean()
    price_vs_avg = ((current_price / avg_price) - 1) * 100
    
    # Price volatility (standard deviation as % of mean)
    volatility = (price_data["Price"].std() / avg_price) * 100
    
    # Simple trend (last value vs. first value)
    first_price = price_data["Price"].iloc[0]
    price_trend = ((current_price / first_price) - 1) * 100
    
    # Forecast end price
    forecast_end_price = forecast_data[forecast_data["Type"] == "Forecast"]["Price"].iloc[-1]
    forecast_change = ((forecast_end_price / current_price) - 1) * 100
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Current Price", f"${current_price:.2f}", delta=f"{price_vs_avg:.1f}% vs avg")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Price Volatility", f"{volatility:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Historical Trend", f"{price_trend:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Forecast Trend", f"{forecast_change:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Price insights
    st.markdown("### Price Insights")
    
    # Determine price trend narrative
    if price_trend > 10:
        trend_narrative = "significant upward trend"
    elif price_trend > 3:
        trend_narrative = "moderate upward trend"
    elif price_trend < -10:
        trend_narrative = "significant downward trend"
    elif price_trend < -3:
        trend_narrative = "moderate downward trend"
    else:
        trend_narrative = "relatively stable prices"
    
    # Volatility narrative
    if volatility > 15:
        volatility_narrative = "high volatility"
    elif volatility > 8:
        volatility_narrative = "moderate volatility"
    else:
        volatility_narrative = "low volatility"
    
    # Forecast narrative
    if forecast_change > 10:
        forecast_narrative = "significant price increases"
    elif forecast_change > 3:
        forecast_narrative = "moderate price increases"
    elif forecast_change < -10:
        forecast_narrative = "significant price decreases"
    elif forecast_change < -3:
        forecast_narrative = "moderate price decreases"
    else:
        forecast_narrative = "stable prices"
    
    st.info(f"""
    ### Price Analysis Summary
    
    The {selected_material} market has shown **{trend_narrative}** over the analyzed period with **{volatility_narrative}** (±{volatility:.1f}%).
    
    Current price is **${current_price:.2f}** per unit, which is **{abs(price_vs_avg):.1f}% {'above' if price_vs_avg > 0 else 'below'}** the historical average.
    
    The {forecast_period}-month forecast predicts **{forecast_narrative}**, with prices expected to reach **${forecast_end_price:.2f}** ({forecast_change:.1f}% change).
    
    **Recommended Actions:**
    - {'Consider long-term contracts to lock in current prices' if forecast_change > 0 else 'Consider short-term contracts and spot purchases'}
    - {'Evaluate alternative materials or suppliers' if forecast_change > 5 else ''}
    - {'Implement price hedging strategies' if volatility > 10 else ''}
    """)

with tab2:
    st.markdown("### Should-Cost Modeling")
    
    # Create sample components for should-cost model
    if selected_material in ["Steel", "Aluminum", "Copper", "Zinc"]:
        components = {
            "raw_material": 0.6,
            "energy": 0.15,
            "labor": 0.1,
            "overhead": 0.05,
            "logistics": 0.05
        }
    elif selected_material in ["Semiconductors", "PCBs", "Displays"]:
        components = {
            "raw_material": 0.4,
            "labor": 0.2,
            "overhead": 0.15,
            "energy": 0.05,
            "additives": 0.15
        }
    elif selected_material in ["Cardboard", "PET", "HDPE", "Plastic Film", "Paper"]:
        components = {
            "raw_material": 0.5,
            "labor": 0.15,
            "energy": 0.1,
            "overhead": 0.1,
            "packaging": 0.05
        }
    else:
        components = {
            "raw_material": 0.45,
            "labor": 0.25,
            "overhead": 0.15,
            "energy": 0.1,
            "logistics": 0.05
        }
    
    # Create should-cost model
    should_cost = should_cost_model(selected_material, components)
    
    # Display should-cost breakdown
    st.markdown(f"#### Should-Cost Model for {selected_material}")
    
    # Create cost breakdown visualization
    cost_df = pd.DataFrame({
        'Component': list(should_cost['breakdown'].keys()),
        'Cost': list(should_cost['breakdown'].values())
    })
    
    # Sort by cost (descending)
    cost_df = cost_df.sort_values('Cost', ascending=False)
    
    # Create bar chart
    fig = px.bar(
        cost_df,
        x='Component',
        y='Cost',
        title=f"Cost Breakdown for {selected_material} (Total: ${should_cost['total_cost']:.2f} {should_cost['unit']})",
        color='Component',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    # Add target line
    target_cost = should_cost['total_cost'] * 0.85
    fig.add_hline(
        y=target_cost,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Target Price: ${target_cost:.2f}",
        annotation_position="top right"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost component sliders for what-if analysis
    st.markdown("### What-If Analysis")
    st.write("Adjust component costs to see impact on total cost:")
    
    # Initialize session state for component adjustments if not exists
    if "component_adjustments" not in st.session_state:
        st.session_state.component_adjustments = {comp: 0 for comp in components.keys()}
    
    # Create sliders for each component
    adjusted_costs = {}
    for component, weight in components.items():
        base_cost = should_cost['breakdown'][component]
        adjustment = st.slider(
            f"{component.title()} (Base: ${base_cost:.2f})",
            min_value=-50,
            max_value=50,
            value=st.session_state.component_adjustments[component],
            step=5,
            format="%d%%",
            key=f"slider_{component}"
        )
        
        # Update session state
        st.session_state.component_adjustments[component] = adjustment
        
        # Calculate adjusted cost
        adjusted_cost = base_cost * (1 + adjustment/100)
        adjusted_costs[component] = adjusted_cost
    
    # Calculate new total cost
    new_total_cost = sum(adjusted_costs.values())
    cost_difference = new_total_cost - should_cost['total_cost']
    percent_change = (cost_difference / should_cost['total_cost']) * 100
    
    # Display comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Original Should-Cost", f"${should_cost['total_cost']:.2f} {should_cost['unit']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            "Adjusted Should-Cost", 
            f"${new_total_cost:.2f} {should_cost['unit']}", 
            delta=f"{percent_change:.1f}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Negotiation recommendations based on should-cost
    st.markdown("### Negotiation Recommendations")
    
    # Get current market price (from first tab data)
    current_market_price = price_data["Price"].iloc[-1]
    
    # Compare should-cost to market price
    price_gap = ((current_market_price - should_cost['total_cost']) / should_cost['total_cost']) * 100
    
    if price_gap > 15:
        gap_assessment = "significantly above"
        opportunity = "high"
        tactics = [
            "Request detailed cost breakdown from suppliers",
            "Highlight component cost insights during negotiations",
            "Consider alternative sourcing options",
            "Request tiered pricing based on volume commitments"
        ]
    elif price_gap > 5:
        gap_assessment = "moderately above"
        opportunity = "moderate"
        tactics = [
            "Conduct competitive benchmarking",
            "Negotiate targeted cost reductions on key components",
            "Explore specification optimization opportunities",
            "Consider longer-term agreements with cost reduction targets"
        ]
    elif price_gap < -5:
        gap_assessment = "below"
        opportunity = "limited"
        tactics = [
            "Focus on supply assurance and quality improvements",
            "Consider longer-term agreements to lock in favorable pricing",
            "Invest in supplier relationship development",
            "Explore joint cost reduction initiatives for mutual benefit"
        ]
    else:
        gap_assessment = "reasonably aligned with"
        opportunity = "some"
        tactics = [
            "Focus on non-price value improvements",
            "Negotiate performance incentives",
            "Explore order frequency and inventory management optimization",
            "Consider joint product development initiatives"
        ]
    
    st.info(f"""
    ### Price vs. Should-Cost Analysis
    
    Current market price (${current_market_price:.2f}) is **{gap_assessment}** the should-cost model (${should_cost['total_cost']:.2f}), 
    with a gap of **{price_gap:.1f}%**.
    
    This indicates **{opportunity} opportunity** for cost negotiation.
    
    **Recommended Tactics:**
    """ + "\n".join([f"- {tactic}" for tactic in tactics]))

with tab3:
    st.markdown("### Input Cost Analysis")
    
    # Create a selector for input costs to track
    input_materials = {
        "Steel": ["Iron Ore", "Scrap Metal", "Coal", "Energy", "Alloys"],
        "Aluminum": ["Bauxite", "Energy", "Caustic Soda", "Carbon Anodes", "Alloying Elements"],
        "PCBs": ["Copper", "Fiberglass", "Chemicals", "Gold", "Energy"],
        "Displays": ["Glass", "Polarizers", "Backlights", "ICs", "Chemicals"],
        "Semiconductors": ["Silicon", "Chemicals", "Precious Metals", "Energy", "Gases"],
        "Plastic Resin": ["Ethylene", "Propylene", "Naphtha", "Natural Gas", "Additives"],
        "Cardboard": ["Paper Pulp", "Starch", "Energy", "Chemicals", "Water"]
    }
    
    # Default to some common inputs if the material isn't in our dictionary
    if selected_material not in input_materials:
        selected_inputs = ["Raw Material A", "Raw Material B", "Energy", "Labor", "Transportation"]
    else:
        selected_inputs = input_materials[selected_material]
    
    st.write("Track the key input costs that drive the price of your material:")
    
    # Allow user to select which inputs to view
    selected_inputs_to_view = st.multiselect(
        "Select Input Costs to Track",
        selected_inputs,
        default=selected_inputs[:3]
    )
    
    if selected_inputs_to_view:
        # Generate price data for each selected input
        input_price_data = {}
        for input_material in selected_inputs_to_view:
            input_price_data[input_material] = get_commodity_prices(input_material)
        
        # Create a combined plot
        fig = go.Figure()
        
        for input_material, data in input_price_data.items():
            # Normalize to percentage change from first value
            first_price = data["Price"].iloc[0]
            normalized_prices = (data["Price"] / first_price - 1) * 100
            
            fig.add_trace(go.Scatter(
                x=data["Date"],
                y=normalized_prices,
                mode='lines',
                name=f"{input_material} ({data['Unit']})"
            ))
        
        fig.update_layout(
            title="Input Cost Trends (% Change from Base Period)",
            xaxis_title="Date",
            yaxis_title="% Change",
            legend_title="Input Material"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        st.markdown("### Input Cost Correlation Analysis")
        
        # Generate correlation with the main material price
        main_price_data = price_data.copy()
        
        # Create a table to show correlations
        corr_data = []
        
        for input_material, data in input_price_data.items():
            # Align dates by resampling to monthly and merging
            input_monthly = data.resample('M', on='Date').mean()
            main_monthly = main_price_data.resample('M', on='Date').mean()
            
            # Merge datasets
            merged = pd.merge_asof(
                input_monthly.reset_index(),
                main_monthly.reset_index(),
                on='Date',
                direction='nearest'
            )
            
            # Calculate correlation if we have enough data points
            if len(merged) > 2:
                correlation = merged['Price_x'].corr(merged['Price_y'])
                
                # Calculate lag correlation (does input price lead material price?)
                merged_lag = merged.copy()
                merged_lag['Price_x_lag1'] = merged_lag['Price_x'].shift(1)
                merged_lag = merged_lag.dropna()
                
                if len(merged_lag) > 2:
                    lag_correlation = merged_lag['Price_x_lag1'].corr(merged_lag['Price_y'])
                else:
                    lag_correlation = None
                
                # Calculate price change ratio (input vs main material)
                if len(merged) > 1:
                    input_change_pct = (merged['Price_x'].iloc[-1] / merged['Price_x'].iloc[0] - 1) * 100
                    main_change_pct = (merged['Price_y'].iloc[-1] / merged['Price_y'].iloc[0] - 1) * 100
                    
                    if main_change_pct != 0:
                        passthrough_ratio = input_change_pct / main_change_pct
                    else:
                        passthrough_ratio = 0
                else:
                    passthrough_ratio = None
            else:
                correlation = None
                lag_correlation = None
                passthrough_ratio = None
            
            corr_data.append({
                'Input Material': input_material,
                'Correlation': correlation,
                'Lag Correlation': lag_correlation,
                'Pass-through Ratio': passthrough_ratio
            })
        
        # Create a DataFrame and display
        corr_df = pd.DataFrame(corr_data)
        
        # Format the dataframe
        for col in ['Correlation', 'Lag Correlation']:
            if col in corr_df.columns:
                corr_df[col] = corr_df[col].apply(lambda x: f"{x:.2f}" if x is not None else "N/A")
        
        if 'Pass-through Ratio' in corr_df.columns:
            corr_df['Pass-through Ratio'] = corr_df['Pass-through Ratio'].apply(
                lambda x: f"{x:.2f}" if x is not None else "N/A"
            )
        
        st.table(corr_df)
        
        # Input cost insights
        st.markdown("### Input Cost Insights")
        
        # Provide interpretations of the correlations
        high_corr_inputs = [
            row['Input Material'] for _, row in corr_df.iterrows() 
            if row['Correlation'] != 'N/A' and float(row['Correlation']) > 0.7
        ]
        
        moderate_corr_inputs = [
            row['Input Material'] for _, row in corr_df.iterrows() 
            if row['Correlation'] != 'N/A' and 0.4 <= float(row['Correlation']) <= 0.7
        ]
        
        if high_corr_inputs or moderate_corr_inputs:
            corr_text = "**Strong price drivers:** " + ", ".join(high_corr_inputs) if high_corr_inputs else ""
            if corr_text and moderate_corr_inputs:
                corr_text += "\n\n**Moderate price drivers:** " + ", ".join(moderate_corr_inputs)
            elif moderate_corr_inputs:
                corr_text = "**Moderate price drivers:** " + ", ".join(moderate_corr_inputs)
        else:
            corr_text = "No strong correlations identified between input costs and material price."
        
        # Provide recommendations based on correlations
        if high_corr_inputs:
            recommendations = [
                f"Index {selected_material} pricing to {', '.join(high_corr_inputs)} in supplier contracts",
                f"Monitor {high_corr_inputs[0]} market closely for early price trend indicators",
                "Consider hedging strategies for highly correlated inputs"
            ]
        else:
            recommendations = [
                "Explore other market factors that may be driving price changes",
                "Request supplier cost breakdown to better understand price drivers",
                "Consider fixed pricing rather than index-based contracts"
            ]
        
        st.info(f"""
        ### Input Cost Analysis Summary
        
        {corr_text}
        
        **Recommendations:**
        """ + "\n".join([f"- {rec}" for rec in recommendations]))
