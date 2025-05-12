import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.data_generator import generate_price_trend_data, generate_contract_data
from utils.scraper import simulated_web_scrape, get_commodity_prices

# Configure page
st.set_page_config(
    page_title="Opportunity Engine - Procurement Command Center",
    page_icon="⚡",
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
    .opportunity-card {
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
    st.markdown("# ⚡ Opportunity Engine")
    st.markdown("---")
    
    # Category selector
    categories = ["Electronics", "Raw Materials", "Packaging", "Office Supplies", 
                 "IT Services", "Logistics", "Chemicals", "Machinery"]
    selected_category = st.selectbox("Category", categories)
    
    # Opportunity filters
    st.markdown("### Opportunity Filters")
    
    # Opportunity type filter
    opportunity_types = ["All Types", "Cost Reduction", "Risk Mitigation", "Innovation", "Sustainability"]
    selected_opp_type = st.selectbox("Opportunity Type", opportunity_types)
    
    # Impact level filter
    impact_levels = ["All Impacts", "High Impact", "Medium Impact", "Low Impact"]
    selected_impact = st.selectbox("Impact Level", impact_levels)
    
    # Implementation effort filter
    effort_levels = ["All Effort Levels", "Low Effort", "Medium Effort", "High Effort"]
    selected_effort = st.selectbox("Implementation Effort", effort_levels)
    
    # Time period filter
    time_periods = ["Last Week", "Last Month", "Last Quarter", "Last Year"]
    selected_period = st.selectbox("Time Period", time_periods)
    
    # Refresh opportunities button
    st.markdown("---")
    if st.button("Refresh Opportunities", use_container_width=True):
        st.success("Opportunities refreshed!")

# Main content
st.markdown('<div class="main-header">Live Opportunity Engine</div>', unsafe_allow_html=True)
st.markdown(f"#### Selected Category: {selected_category}")

# Create tabs for different opportunity sources
tab1, tab2, tab3, tab4 = st.tabs(["Opportunity Dashboard", "Market Triggers", "Contract Opportunities", "Supply Glut Alerts"])

with tab1:
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
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
    opp_counts = [np.random.randint(3, 10) for _ in range(len(opp_types))]
    
    # Create pie chart
    fig = px.pie(
        names=opp_types,
        values=opp_counts,
        title="Opportunities by Type",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Opportunity impact vs. effort
        impact_levels = ["High", "Medium", "Low"]
        effort_levels = ["Low", "Medium", "High"]
        
        # Generate random counts for each combination
        data = []
        for impact in impact_levels:
            for effort in effort_levels:
                count = np.random.randint(0, 5)
                data.append({"Impact": impact, "Effort": effort, "Count": count})
        
        # Create DataFrame
        heatmap_df = pd.DataFrame(data)
        
        # Reshape for heatmap
        heatmap_df = heatmap_df.pivot(index="Impact", columns="Effort", values="Count")
        
        # Create heatmap
        fig = px.imshow(
            heatmap_df,
            labels=dict(x="Implementation Effort", y="Business Impact", color="Count"),
            x=effort_levels,
            y=impact_levels,
            color_continuous_scale="Blues",
            title="Opportunities by Impact vs. Effort"
        )
        
        # Add count annotations
        for i, impact in enumerate(impact_levels):
            for j, effort in enumerate(effort_levels):
                fig.add_annotation(
                    x=effort,
                    y=impact,
                    text=str(heatmap_df.loc[impact, effort]),
                    showarrow=False,
                    font=dict(color="white" if heatmap_df.loc[impact, effort] > 2 else "black")
                )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Top opportunities list
    st.markdown("### Top Opportunities")
    
    # Generate sample opportunities
    opportunities = []
    
    # Opportunity templates by category
    opportunity_templates = {
        "Electronics": [
            {"title": "Consolidate PCB suppliers", "type": "Cost Reduction", "impact": "High", "effort": "Medium", "savings": f"${np.random.randint(100, 500)}K", "roi": f"{np.random.randint(200, 700)}%"},
            {"title": "Implement VMI for connectors", "type": "Cost Reduction", "impact": "Medium", "effort": "Medium", "savings": f"${np.random.randint(50, 200)}K", "roi": f"{np.random.randint(150, 400)}%"},
            {"title": "Re-negotiate semiconductor contracts", "type": "Cost Reduction", "impact": "High", "effort": "Low", "savings": f"${np.random.randint(200, 800)}K", "roi": f"{np.random.randint(300, 900)}%"},
            {"title": "Develop alternate display supplier", "type": "Risk Mitigation", "impact": "High", "effort": "High", "savings": f"${np.random.randint(50, 300)}K", "roi": f"{np.random.randint(100, 300)}%"}
        ],
        "Raw Materials": [
            {"title": "Leverage steel price drop for spot buys", "type": "Cost Reduction", "impact": "High", "effort": "Low", "savings": f"${np.random.randint(200, 700)}K", "roi": f"{np.random.randint(400, 1000)}%"},
            {"title": "Implement commodity hedging", "type": "Risk Mitigation", "impact": "Medium", "effort": "High", "savings": f"${np.random.randint(100, 500)}K", "roi": f"{np.random.randint(150, 350)}%"},
            {"title": "Consolidate aluminum suppliers", "type": "Cost Reduction", "impact": "Medium", "effort": "Medium", "savings": f"${np.random.randint(150, 400)}K", "roi": f"{np.random.randint(200, 500)}%"},
            {"title": "Specification rationalization", "type": "Cost Reduction", "impact": "High", "effort": "Medium", "savings": f"${np.random.randint(300, 800)}K", "roi": f"{np.random.randint(300, 700)}%"}
        ],
        "Packaging": [
            {"title": "Optimize packaging dimensions", "type": "Cost Reduction", "impact": "Medium", "effort": "Low", "savings": f"${np.random.randint(50, 300)}K", "roi": f"{np.random.randint(300, 800)}%"},
            {"title": "Transition to sustainable materials", "type": "Sustainability", "impact": "Medium", "effort": "High", "savings": f"${np.random.randint(50, 200)}K", "roi": f"{np.random.randint(100, 300)}%"},
            {"title": "Consolidate regional suppliers", "type": "Cost Reduction", "impact": "High", "effort": "Medium", "savings": f"${np.random.randint(200, 600)}K", "roi": f"{np.random.randint(250, 600)}%"},
            {"title": "Implement SIOP process", "type": "Cost Reduction", "impact": "High", "effort": "High", "savings": f"${np.random.randint(300, 900)}K", "roi": f"{np.random.randint(200, 500)}%"}
        ]
    }
    
    # Get opportunities for selected category or use default ones
    if selected_category in opportunity_templates:
        opportunities = opportunity_templates[selected_category]
    else:
        # Generate generic opportunities
        generic_titles = [
            f"Consolidate {selected_category} suppliers",
            f"Implement VMI program for {selected_category}",
            f"Renegotiate key contracts in {selected_category}",
            f"Optimize specifications for {selected_category}"
        ]
        
        opportunity_types = ["Cost Reduction", "Risk Mitigation", "Innovation", "Sustainability"]
        impact_levels = ["High", "Medium", "Low"]
        effort_levels = ["Low", "Medium", "High"]
        
        for title in generic_titles:
            opportunities.append({
                "title": title,
                "type": np.random.choice(opportunity_types),
                "impact": np.random.choice(impact_levels),
                "effort": np.random.choice(effort_levels),
                "savings": f"${np.random.randint(50, 500)}K",
                "roi": f"{np.random.randint(150, 800)}%"
            })
    
    # Filter opportunities based on sidebar selections
    filtered_opps = opportunities
    
    if selected_opp_type != "All Types":
        filtered_opps = [o for o in filtered_opps if o["type"] == selected_opp_type]
    
    if selected_impact != "All Impacts":
        impact_level = selected_impact.split(" ")[0]
        filtered_opps = [o for o in filtered_opps if o["impact"] == impact_level]
    
    if selected_effort != "All Effort Levels":
        effort_level = selected_effort.split(" ")[0]
        filtered_opps = [o for o in filtered_opps if o["effort"] == effort_level]
    
    # Display opportunities
    if not filtered_opps:
        st.info("No opportunities match your current filter criteria. Try adjusting your filters.")
    else:
        for opp in filtered_opps:
            # Determine impact color
            impact_color = "green" if opp["impact"] == "High" else "orange" if opp["impact"] == "Medium" else "red"
            
            # Determine effort icon
            effort_icon = "🟢" if opp["effort"] == "Low" else "🟠" if opp["effort"] == "Medium" else "🔴"
            
            st.markdown(f"""
            <div class="opportunity-card" style="border-left: 5px solid {impact_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{opp['title']}</h4>
                    <span style="font-weight: bold; color: green;">{opp['savings']} potential</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <span><strong>Type:</strong> {opp['type']}</span>
                    <span><strong>Impact:</strong> <span style="color: {impact_color};">{opp['impact']}</span></span>
                    <span><strong>Effort:</strong> {effort_icon} {opp['effort']}</span>
                    <span><strong>ROI:</strong> {opp['roi']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            with col1:
                st.button(f"Analyze", key=f"analyze_{opp['title']}")
            with col2:
                st.button(f"Implement", key=f"implement_{opp['title']}")
            with col3:
                st.button(f"Dismiss", key=f"dismiss_{opp['title']}")
            with col4:
                st.write("")  # Empty column for spacing

with tab2:
    # Market triggers section
    st.markdown("### Market Trigger Analysis")
    
    # Get market news/intelligence via scraper
    market_news = simulated_web_scrape(selected_category)
    
    # Filter high-impact news
    high_impact_news = [item for item in market_news if item["impact"] == "High"]
    
    # Create metrics showing trigger counts
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        price_triggers = len([n for n in market_news if "price" in n["title"].lower()])
        st.metric("Price Change Triggers", price_triggers)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        supply_triggers = len([n for n in market_news if any(word in n["title"].lower() for word in ["supply", "shortage", "capacity"])])
        st.metric("Supply Change Triggers", supply_triggers)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        regulatory_triggers = len([n for n in market_news if any(word in n["title"].lower() for word in ["regulation", "compliance", "law", "policy"])])
        st.metric("Regulatory Triggers", regulatory_triggers)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        tech_triggers = len([n for n in market_news if any(word in n["title"].lower() for word in ["technology", "innovation", "breakthrough"])])
        st.metric("Technology Triggers", tech_triggers)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Market price trends that might trigger opportunities
    st.markdown("### Price Trend Triggers")
    
    # Get commodity prices for relevant materials
    if selected_category == "Raw Materials":
        materials = ["Steel", "Aluminum", "Copper", "Zinc"]
    elif selected_category == "Electronics":
        materials = ["Copper", "Gold", "Silver", "PET Resin"]
    elif selected_category == "Packaging":
        materials = ["Paper Pulp", "PET Resin", "HDPE", "Aluminum"]
    else:
        materials = ["Steel", "Copper", "Aluminum", "Paper Pulp"]
    
    # Create price trend visualization
    fig = go.Figure()
    
    # Plot price trends for each material (normalized to percentage change)
    for material in materials:
        price_data = get_commodity_prices(material)
        
        # Calculate percentage change from first price
        first_price = price_data["Price"].iloc[0]
        normalized_prices = (price_data["Price"] / first_price - 1) * 100
        
        fig.add_trace(go.Scatter(
            x=price_data["Date"],
            y=normalized_prices,
            mode='lines',
            name=f"{material} ({price_data['Unit']})"
        ))
    
    fig.update_layout(
        title="Price Trend Comparison (% Change)",
        xaxis_title="Date",
        yaxis_title="% Change from Base Period",
        legend_title="Material"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Identify price-related opportunities based on trends
    st.markdown("### Price-Triggered Opportunities")
    
    # Generate price-triggered opportunities
    price_opportunities = []
    
    # Find materials with significant price changes
    for material in materials:
        price_data = get_commodity_prices(material)
        first_price = price_data["Price"].iloc[0]
        last_price = price_data["Price"].iloc[-1]
        change_pct = ((last_price / first_price) - 1) * 100
        
        # If price drop, opportunity to negotiate or spot buy
        if change_pct < -10:
            price_opportunities.append({
                "title": f"Leverage {material} price drop for spot purchases",
                "trigger": f"{abs(change_pct):.1f}% price decrease in {material}",
                "action": "Immediate spot buys and contract renegotiation",
                "impact": "High" if abs(change_pct) > 20 else "Medium",
                "savings_potential": f"${np.random.randint(100, 500)}K",
                "color": "green"
            })
        # If price increase, opportunity to mitigate or find alternatives
        elif change_pct > 10:
            price_opportunities.append({
                "title": f"Mitigate {material} price increase impact",
                "trigger": f"{change_pct:.1f}% price increase in {material}",
                "action": "Evaluate alternatives or implement hedging strategy",
                "impact": "High" if change_pct > 20 else "Medium",
                "savings_potential": f"${np.random.randint(50, 300)}K",
                "color": "red"
            })
    
    if price_opportunities:
        for opp in price_opportunities:
            st.markdown(f"""
            <div class="opportunity-card" style="border-left: 5px solid {opp['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{opp['title']}</h4>
                    <span style="font-weight: bold; color: green;">{opp['savings_potential']} potential</span>
                </div>
                <p><strong>Trigger:</strong> {opp['trigger']}</p>
                <p><strong>Recommended Action:</strong> {opp['action']}</p>
                <p><strong>Impact:</strong> <span style="color: {opp['color']};">{opp['impact']}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                st.button(f"Take Action", key=f"price_action_{opp['title']}")
            with col2:
                st.button(f"Analyze Further", key=f"price_analyze_{opp['title']}")
            with col3:
                st.write("")  # Empty column for spacing
    else:
        st.info("No significant price-related opportunities detected at this time.")
    
    # Display market news that might trigger opportunities
    st.markdown("### Market News Triggers")
    
    # Display high-impact news items
    if high_impact_news:
        for item in high_impact_news:
            st.markdown(f"""
            <div class="opportunity-card" style="border-left: 5px solid red;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{item['title']}</h4>
                    <span style="color: #666; font-size: 0.8rem;">{item['source']} | {item['date']}</span>
                </div>
                <p><strong>Potential Impact:</strong> <span style="color: red;">High</span></p>
                <p><strong>Recommended Action:</strong> Evaluate implications and develop response strategy</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                st.button(f"Assess Impact", key=f"news_assess_{item['title']}")
            with col2:
                st.button(f"Create Response", key=f"news_respond_{item['title']}")
            with col3:
                st.write("")  # Empty column for spacing
    else:
        st.info("No high-impact news triggers detected for this category at this time.")

with tab3:
    # Contract opportunities section
    st.markdown("### Contract Opportunity Analysis")
    
    # Get contract data
    contract_data = generate_contract_data()
    
    # Filter contracts related to the selected category
    category_contracts = contract_data[contract_data["Category"] == selected_category]
    
    # Contract metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        expiring_soon = len(category_contracts[category_contracts["Status"] == "Expiring Soon"])
        st.metric("Expiring Soon", expiring_soon)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        expired = len(category_contracts[category_contracts["Status"] == "Expired"])
        st.metric("Expired", expired)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        total_contract_value = category_contracts["Value"].sum()
        st.metric("Total Contract Value", f"${total_contract_value/1000000:.1f}M")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        avg_contract_value = category_contracts["Value"].mean()
        st.metric("Avg. Contract Value", f"${avg_contract_value/1000:.0f}K")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Contract renewal timeline
    st.markdown("### Contract Renewal Timeline")
    
    # Create a timeline of contract expirations
    fig = px.timeline(
        category_contracts.sort_values("Days to Expiry"), 
        x_start="End Date", 
        y="Supplier",
        color="Status",
        hover_data=["Contract ID", "Value", "Days to Expiry"],
        title="Contract Expiration Timeline",
        color_discrete_map={
            "Active": "#0066cc",
            "Expiring Soon": "#ff9900",
            "Expired": "#cc0000"
        }
    )
    
    fig.update_yaxes(autorange="reversed")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Contract renewal opportunities
    st.markdown("### Contract Renewal Opportunities")
    
    # Filter for expiring or expired contracts
    renewal_opportunities = category_contracts[
        (category_contracts["Status"] == "Expiring Soon") | 
        (category_contracts["Status"] == "Expired")
    ]
    
    if not renewal_opportunities.empty:
        for _, contract in renewal_opportunities.iterrows():
            status_color = "orange" if contract["Status"] == "Expiring Soon" else "red"
            days_text = f"{contract['Days to Expiry']} days until expiry" if contract["Days to Expiry"] > 0 else f"{abs(contract['Days to Expiry'])} days overdue"
            
            # Estimate potential savings (5-15% of contract value)
            savings_pct = np.random.uniform(0.05, 0.15)
            savings = contract["Value"] * savings_pct
            
            st.markdown(f"""
            <div class="opportunity-card" style="border-left: 5px solid {status_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>Renew contract with {contract['Supplier']}</h4>
                    <span style="font-weight: bold; color: green;">${savings/1000:.0f}K potential savings</span>
                </div>
                <p><strong>Contract ID:</strong> {contract['Contract ID']} | <strong>Value:</strong> ${contract['Value']/1000:.0f}K</p>
                <p><strong>Status:</strong> <span style="color: {status_color};">{contract['Status']}</span> ({days_text})</p>
                <p><strong>Recommended Action:</strong> {
                    "Begin renewal process and evaluate market conditions" if contract["Status"] == "Expiring Soon" else 
                    "Immediate action required - conduct market analysis and prepare RFP"
                }</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            with col1:
                st.button(f"Renew", key=f"renew_{contract['Contract ID']}")
            with col2:
                st.button(f"Re-bid", key=f"rebid_{contract['Contract ID']}")
            with col3:
                st.button(f"Analyze", key=f"analyze_contract_{contract['Contract ID']}")
            with col4:
                st.write("")  # Empty column for spacing
    else:
        st.info("No contracts are currently expiring or expired for this category.")
    
    # Contract consolidation opportunities
    st.markdown("### Contract Consolidation Opportunities")
    
    # Analyze suppliers with multiple contracts
    supplier_contracts = category_contracts.groupby("Supplier").agg({
        "Contract ID": "count",
        "Value": "sum"
    }).reset_index()
    
    supplier_contracts = supplier_contracts.rename(columns={"Contract ID": "Contract Count"})
    
    # Filter suppliers with multiple contracts
    multi_contract_suppliers = supplier_contracts[supplier_contracts["Contract Count"] > 1]
    
    if not multi_contract_suppliers.empty:
        for _, supplier in multi_contract_suppliers.iterrows():
            # Estimate consolidation savings (7-12% of total contract value)
            savings_pct = np.random.uniform(0.07, 0.12)
            savings = supplier["Value"] * savings_pct
            
            st.markdown(f"""
            <div class="opportunity-card" style="border-left: 5px solid #0066cc;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>Consolidate {supplier['Contract Count']} contracts with {supplier['Supplier']}</h4>
                    <span style="font-weight: bold; color: green;">${savings/1000:.0f}K potential savings</span>
                </div>
                <p><strong>Current Spend:</strong> ${supplier['Value']/1000:.0f}K across {supplier['Contract Count']} contracts</p>
                <p><strong>Opportunity:</strong> Consolidate multiple contracts to leverage volume pricing and reduce administrative overhead</p>
                <p><strong>Recommended Action:</strong> Conduct spend analysis and prepare consolidated negotiation strategy</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                st.button(f"Consolidate", key=f"consolidate_{supplier['Supplier']}")
            with col2:
                st.button(f"Analyze Spend", key=f"analyze_spend_{supplier['Supplier']}")
            with col3:
                st.write("")  # Empty column for spacing
    else:
        st.info("No contract consolidation opportunities identified for this category.")

with tab4:
    # Supply glut alerts
    st.markdown("### Supply Glut Opportunity Alerts")
    
    # Market condition metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate random market conditions
    supply_demand_ratio = np.random.uniform(0.8, 1.2)
    inventory_levels = np.random.uniform(70, 130)
    price_pressure = np.random.uniform(-15, 15)
    lead_time_change = np.random.uniform(-20, 10)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        ratio_delta = supply_demand_ratio - 1
        st.metric("Supply/Demand Ratio", f"{supply_demand_ratio:.2f}", delta=f"{ratio_delta*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Inventory Levels", f"{inventory_levels:.1f}%", delta=f"{inventory_levels-100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Price Pressure", f"{price_pressure:.1f}%", delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Lead Time Change", f"{lead_time_change:.1f}%", delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Supply conditions chart
    st.markdown("### Supply-Demand Balance Trend")
    
    # Generate supply-demand trend data
    months = 12
    dates = pd.date_range(end=datetime.now(), periods=months, freq='M')
    
    # Generate supply and demand values with some randomness
    base_value = 100
    trend = np.random.uniform(-0.2, 0.3)
    seasonality = np.random.uniform(0.05, 0.15)
    
    supply_values = []
    demand_values = []
    
    for i, date in enumerate(dates):
        # Trend component
        trend_component = base_value * trend * i
        
        # Seasonality component
        month = date.month
        supply_seasonality = np.sin(2 * np.pi * month / 12) * seasonality * base_value
        demand_seasonality = np.cos(2 * np.pi * month / 12) * seasonality * base_value
        
        # Random noise
        supply_noise = np.random.normal(0, base_value * 0.03)
        demand_noise = np.random.normal(0, base_value * 0.02)
        
        # Calculate values
        supply = base_value + trend_component + supply_seasonality + supply_noise
        demand = base_value + trend_component + demand_seasonality + demand_noise
        
        supply_values.append(supply)
        demand_values.append(demand)
    
    # Create DataFrame
    supply_demand_df = pd.DataFrame({
        'Date': dates,
        'Supply': supply_values,
        'Demand': demand_values
    })
    
    # Calculate surplus/deficit
    supply_demand_df['Surplus'] = supply_demand_df['Supply'] - supply_demand_df['Demand']
    
    # Create a dual-axis chart
    fig = go.Figure()
    
    # Add supply and demand lines
    fig.add_trace(go.Scatter(
        x=supply_demand_df['Date'],
        y=supply_demand_df['Supply'],
        name='Supply',
        line=dict(color='#0066cc')
    ))
    
    fig.add_trace(go.Scatter(
        x=supply_demand_df['Date'],
        y=supply_demand_df['Demand'],
        name='Demand',
        line=dict(color='#ff9900')
    ))
    
    # Add surplus/deficit as bar chart on secondary axis
    fig.add_trace(go.Bar(
        x=supply_demand_df['Date'],
        y=supply_demand_df['Surplus'],
        name='Surplus/Deficit',
        marker_color=['#00cc66' if val >= 0 else '#cc0000' for val in supply_demand_df['Surplus']]
    ))
    
    fig.update_layout(
        title="Supply-Demand Balance Trend",
        xaxis_title="Date",
        yaxis_title="Index Value (Base 100)",
        barmode='relative',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Supply glut opportunities
    st.markdown("### Supply Glut Opportunities")
    
    # Check if any surplus exists
    recent_surplus = supply_demand_df['Surplus'].iloc[-1]
    
    if recent_surplus > 3:
        # Generate opportunities based on supply glut
        glut_opportunities = [
            {
                "title": f"Leverage {selected_category} supply surplus for spot purchases",
                "condition": f"Supply exceeding demand by {recent_surplus:.1f}%",
                "action": "Immediate spot buys at favorable pricing",
                "impact": "High" if recent_surplus > 10 else "Medium",
                "savings_potential": f"${np.random.randint(100, 500)}K",
                "color": "green"
            },
            {
                "title": f"Renegotiate long-term contracts based on market oversupply",
                "condition": f"Sustained oversupply in {selected_category} market",
                "action": "Approach key suppliers for contract price adjustments",
                "impact": "Medium",
                "savings_potential": f"${np.random.randint(50, 300)}K",
                "color": "green"
            }
        ]
        
        for opp in glut_opportunities:
            st.markdown(f"""
            <div class="opportunity-card" style="border-left: 5px solid {opp['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{opp['title']}</h4>
                    <span style="font-weight: bold; color: green;">{opp['savings_potential']} potential</span>
                </div>
                <p><strong>Market Condition:</strong> {opp['condition']}</p>
                <p><strong>Recommended Action:</strong> {opp['action']}</p>
                <p><strong>Impact:</strong> <span style="color: {opp['color']};">{opp['impact']}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                st.button(f"Take Action", key=f"glut_action_{opp['title']}")
            with col2:
                st.button(f"Analyze Further", key=f"glut_analyze_{opp['title']}")
            with col3:
                st.write("")  # Empty column for spacing
    elif recent_surplus < -3:
        # Generate opportunities based on supply shortage
        shortage_opportunities = [
            {
                "title": f"Secure {selected_category} supply ahead of potential shortages",
                "condition": f"Demand exceeding supply by {abs(recent_surplus):.1f}%",
                "action": "Lock in volumes with preferred suppliers",
                "impact": "High" if abs(recent_surplus) > 10 else "Medium",
                "savings_potential": "Supply assurance",
                "color": "orange"
            },
            {
                "title": f"Develop alternative sources for {selected_category}",
                "condition": f"Growing supply constraints in primary markets",
                "action": "Qualify new suppliers in different regions",
                "impact": "Medium",
                "savings_potential": "Risk mitigation",
                "color": "orange"
            }
        ]
        
        for opp in shortage_opportunities:
            st.markdown(f"""
            <div class="opportunity-card" style="border-left: 5px solid {opp['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{opp['title']}</h4>
                    <span style="font-weight: bold; color: #ff9900;">{opp['savings_potential']}</span>
                </div>
                <p><strong>Market Condition:</strong> {opp['condition']}</p>
                <p><strong>Recommended Action:</strong> {opp['action']}</p>
                <p><strong>Impact:</strong> <span style="color: {opp['color']};">{opp['impact']}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                st.button(f"Take Action", key=f"shortage_action_{opp['title']}")
            with col2:
                st.button(f"Analyze Further", key=f"shortage_analyze_{opp['title']}")
            with col3:
                st.write("")  # Empty column for spacing
    else:
        st.info("No significant supply-demand imbalance detected at this time.")
    
    # Regulatory changes section
    st.markdown("### Regulatory Change Opportunities")
    
    # Sample regulatory changes based on category
    regulatory_changes = {
        "Electronics": [
            {"title": "New REACH compliance requirements", "impact": "Medium", "deadline": "2023-12-31", "action": "Supplier certification audit"},
            {"title": "Conflict minerals reporting expansion", "impact": "Low", "deadline": "2024-05-15", "action": "Supply chain mapping update"}
        ],
        "Raw Materials": [
            {"title": "Carbon border adjustment mechanism", "impact": "High", "deadline": "2024-01-01", "action": "Supplier emissions assessment"},
            {"title": "New import tariffs on selected metals", "impact": "Medium", "deadline": "2023-10-01", "action": "Sourcing strategy revision"}
        ],
        "Packaging": [
            {"title": "Single-use plastic regulations", "impact": "High", "deadline": "2024-06-30", "action": "Alternative materials qualification"},
            {"title": "Extended producer responsibility", "impact": "Medium", "deadline": "2024-01-01", "action": "Recyclability assessment"}
        ]
    }
    
    # Get relevant regulatory changes or use empty list if none for this category
    category_regs = regulatory_changes.get(selected_category, [])
    
    if category_regs:
        for reg in category_regs:
            impact_color = "red" if reg["impact"] == "High" else "orange" if reg["impact"] == "Medium" else "green"
            
            st.markdown(f"""
            <div class="opportunity-card" style="border-left: 5px solid {impact_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{reg['title']}</h4>
                    <span>Deadline: {reg['deadline']}</span>
                </div>
                <p><strong>Impact:</strong> <span style="color: {impact_color};">{reg['impact']}</span></p>
                <p><strong>Recommended Action:</strong> {reg['action']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                st.button(f"Compliance Plan", key=f"reg_plan_{reg['title']}")
            with col2:
                st.button(f"Supplier Assessment", key=f"reg_assess_{reg['title']}")
            with col3:
                st.write("")  # Empty column for spacing
    else:
        st.info("No significant regulatory changes affecting this category at this time.")
