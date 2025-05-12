import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.data_generator import generate_supplier_data, generate_risk_data, generate_supplier_details

# Configure page
st.set_page_config(
    page_title="Supplier Intelligence - Procurement Command Center",
    page_icon="🧾",
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
    .supplier-card {
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
    st.markdown("# 🧾 Supplier Intelligence")
    st.markdown("---")
    
    # Category selector
    categories = ["Electronics", "Raw Materials", "Packaging", "Office Supplies", 
                 "IT Services", "Logistics", "Chemicals", "Machinery"]
    selected_category = st.selectbox("Category", categories)
    
    # Options for filtering suppliers
    st.markdown("### Supplier Filters")
    
    # Tier filter
    tiers = ["All Tiers", "Tier 1", "Tier 2", "Tier 3"]
    selected_tier = st.selectbox("Tier", tiers)
    
    # Risk level filter
    risk_levels = ["All Risk Levels", "High Risk", "Medium Risk", "Low Risk"]
    selected_risk = st.selectbox("Risk Level", risk_levels)
    
    # Region filter
    regions = ["All Regions", "North America", "Europe", "Asia", "Latin America"]
    selected_region = st.selectbox("Region", regions)
    
    # Search bar for supplier name
    supplier_search = st.text_input("Search Supplier", "")
    
    # Action buttons
    st.markdown("---")
    st.markdown("### Actions")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Export Data")
    with col2:
        st.button("Run Analysis")

# Main content
st.markdown('<div class="main-header">Supplier & Risk Intelligence</div>', unsafe_allow_html=True)
st.markdown(f"#### Selected Category: {selected_category}")

# Create tabs for different supplier views
tab1, tab2, tab3 = st.tabs(["Supplier Overview", "Risk Management", "Alternative Suppliers"])

with tab1:
    # Supplier Quadrant Analysis
    st.markdown("### Supplier Strategic Positioning")
    
    # Generate supplier data
    supplier_data = generate_supplier_data(selected_category)
    
    # Create the quadrant visualization
    fig = px.scatter(
        supplier_data,
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
    
    # Add quadrant labels
    fig.add_annotation(x=2.5, y=7.5, text="Strategic Partners", showarrow=False, font=dict(size=10))
    fig.add_annotation(x=7.5, y=7.5, text="Performance Focus", showarrow=False, font=dict(size=10))
    fig.add_annotation(x=2.5, y=2.5, text="Maintain", showarrow=False, font=dict(size=10))
    fig.add_annotation(x=7.5, y=2.5, text="Risk Mitigation", showarrow=False, font=dict(size=10))
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Supplier cards with detailed information
    st.markdown("### Supplier Profiles")
    
    # Get detailed supplier data
    suppliers = generate_supplier_details()
    
    # Filter suppliers based on sidebar filters
    filtered_suppliers = suppliers
    
    # Filter by tier
    if selected_tier != "All Tiers":
        filtered_suppliers = [s for s in filtered_suppliers if s['tier'] == selected_tier]
    
    # Filter by risk
    if selected_risk != "All Risk Levels":
        if selected_risk == "High Risk":
            filtered_suppliers = [s for s in filtered_suppliers if s['overall_risk'] >= 7]
        elif selected_risk == "Medium Risk":
            filtered_suppliers = [s for s in filtered_suppliers if 4 <= s['overall_risk'] < 7]
        else:  # Low Risk
            filtered_suppliers = [s for s in filtered_suppliers if s['overall_risk'] < 4]
    
    # Filter by region
    if selected_region != "All Regions":
        filtered_suppliers = [s for s in filtered_suppliers if selected_region in s['location']]
    
    # Filter by search term
    if supplier_search:
        filtered_suppliers = [s for s in filtered_suppliers if supplier_search.lower() in s['name'].lower()]
    
    # Create a grid layout for supplier cards
    cols = st.columns(2)
    
    for i, supplier in enumerate(filtered_suppliers):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="supplier-card">
                <h4>{supplier['name']} ({supplier['tier']})</h4>
                <p><strong>Location:</strong> {supplier['location']}</p>
                <p><strong>Categories:</strong> {', '.join(supplier['categories'])}</p>
                <p><strong>Annual Spend:</strong> ${supplier['spend']:,}</p>
                <hr>
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <p><strong>Financial Risk:</strong> {supplier['financial_risk']}/10</p>
                        <p><strong>Supply Risk:</strong> {supplier['supply_risk']}/10</p>
                        <p><strong>Geo Risk:</strong> {supplier['geo_risk']}/10</p>
                    </div>
                    <div>
                        <p><strong>ESG Score:</strong> {supplier['esg_score']}/100</p>
                        <p><strong>Quality Score:</strong> {supplier['quality_score']}/100</p>
                        <p><strong>On-Time Delivery:</strong> {supplier['on_time_delivery']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add buttons for actions
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button(f"View Details", key=f"details_{i}")
            with col2:
                st.button(f"Risk Report", key=f"risk_{i}")
            with col3:
                st.button(f"Performance", key=f"perf_{i}")

with tab2:
    # Risk Heatmap
    st.markdown("### Risk Assessment Heatmap")
    
    # Generate risk data
    risk_data = generate_risk_data(selected_category)
    
    # Create heatmap
    fig = px.imshow(
        risk_data,
        labels=dict(x="Risk Category", y="Supplier", color="Risk Level"),
        x=risk_data.columns,
        y=risk_data.index,
        color_continuous_scale='RdYlGn_r'
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk metrics and overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        overall_risk = np.random.randint(40, 80)
        risk_delta = np.random.randint(-10, 10)
        st.metric("Overall Risk Score", f"{overall_risk}/100", delta=f"{risk_delta}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        high_risk_suppliers = np.random.randint(1, 5)
        st.metric("High Risk Suppliers", high_risk_suppliers, delta=f"{np.random.randint(-2, 2)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        concentration_risk = np.random.randint(30, 90)
        st.metric("Concentration Risk", f"{concentration_risk}%", delta=f"{np.random.randint(-15, 5)}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        active_mitigations = np.random.randint(2, 8)
        st.metric("Active Mitigations", active_mitigations, delta=f"{np.random.randint(0, 3)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk breakdown section
    st.markdown("### Risk Breakdown")
    
    # Generate risk metrics for different categories
    risk_categories = {
        "Financial Risk": np.random.randint(30, 90),
        "Supply Chain Risk": np.random.randint(30, 90),
        "Geopolitical Risk": np.random.randint(30, 90),
        "Regulatory Risk": np.random.randint(30, 90),
        "Climate Risk": np.random.randint(30, 90),
        "Cyber Risk": np.random.randint(30, 90)
    }
    
    # Create a bar chart
    risk_df = pd.DataFrame({
        'Category': list(risk_categories.keys()),
        'Score': list(risk_categories.values())
    })
    
    fig = px.bar(
        risk_df,
        x='Category',
        y='Score',
        color='Score',
        color_continuous_scale='RdYlGn_r',
        title="Risk by Category"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk mitigation recommendations
    st.markdown("### Risk Mitigation Recommendations")
    
    # Create sample recommendations based on highest risk areas
    highest_risk = max(risk_categories.items(), key=lambda x: x[1])
    second_highest = sorted(risk_categories.items(), key=lambda x: x[1], reverse=True)[1]
    
    mitigation_strategies = {
        "Financial Risk": [
            "Implement regular financial health monitoring",
            "Require financial guarantees or performance bonds",
            "Develop contingency plans for supplier financial distress",
            "Implement phased payment terms to reduce exposure"
        ],
        "Supply Chain Risk": [
            "Develop secondary/backup suppliers",
            "Implement buffer inventory for critical items",
            "Map n-tier supply chain for visibility",
            "Develop logistics contingency routes"
        ],
        "Geopolitical Risk": [
            "Diversify supplier base across regions",
            "Monitor geopolitical developments in supplier countries",
            "Develop regional supply alternatives",
            "Create country risk assessment process"
        ],
        "Regulatory Risk": [
            "Implement compliance monitoring and auditing",
            "Require suppliers to notify of regulatory changes",
            "Develop regulatory tracking system",
            "Include regulatory compliance in supplier evaluations"
        ],
        "Climate Risk": [
            "Assess supplier facilities for climate vulnerability",
            "Require climate adaptation plans from key suppliers",
            "Develop alternate sourcing for climate-vulnerable materials",
            "Implement carbon reduction initiatives with suppliers"
        ],
        "Cyber Risk": [
            "Implement supplier cybersecurity assessments",
            "Require cybersecurity certifications from suppliers",
            "Limit supplier system access and data sharing",
            "Develop cyber incident response plans with suppliers"
        ]
    }
    
    # Display recommendations
    st.info(f"""
    ### Priority Risk Mitigation Strategies
    
    Based on your risk assessment, the following areas require immediate attention:
    
    **{highest_risk[0]}** ({highest_risk[1]}/100) - High Priority
    {' '.join(['- ' + strategy for strategy in mitigation_strategies[highest_risk[0]][:2]])}
    
    **{second_highest[0]}** ({second_highest[1]}/100) - Medium Priority
    {' '.join(['- ' + strategy for strategy in mitigation_strategies[second_highest[0]][:2]])}
    
    Implement these strategies to reduce your risk exposure and improve supply chain resilience.
    """)

with tab3:
    # Alternative supplier analysis
    st.markdown("### AI Similarity Engine - Alternative Suppliers")
    
    # Supplier selection
    suppliers = [f"Supplier {i+1}" for i in range(10)]
    selected_supplier = st.selectbox("Select a supplier to find alternatives:", suppliers)
    
    # Parameters for alternative search
    st.markdown("### Search Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        similarity_threshold = st.slider("Minimum Similarity Score", 50, 95, 70)
        include_criteria = st.multiselect(
            "Must Include Criteria",
            ["Quality Certification", "Sustainability Rating", "Local Presence", "Size/Capacity", "Technology Capability"],
            ["Quality Certification"]
        )
    
    with col2:
        max_results = st.slider("Maximum Results", 3, 10, 5)
        exclude_regions = st.multiselect(
            "Exclude Regions",
            ["North America", "Europe", "Asia", "Latin America", "Africa", "Middle East"],
            []
        )
    
    # Search button
    if st.button("Find Alternative Suppliers", key="find_alt"):
        with st.spinner("Searching for alternative suppliers..."):
            # Simulate search time
            time.sleep(1)
            
            # Generate alternative suppliers
            alt_suppliers = []
            
            for i in range(np.random.randint(max_results-2, max_results+1)):
                similarity_score = np.random.randint(similarity_threshold, 100)
                
                # Generate random attributes based on include criteria
                attributes = {}
                for criterion in ["Quality Certification", "Sustainability Rating", "Local Presence", "Size/Capacity", "Technology Capability"]:
                    if criterion in include_criteria:
                        attributes[criterion] = "Yes"
                    else:
                        attributes[criterion] = "Yes" if np.random.random() > 0.3 else "No"
                
                # Generate regions excluding the excluded ones
                available_regions = [r for r in ["North America", "Europe", "Asia", "Latin America", "Africa", "Middle East"] if r not in exclude_regions]
                if available_regions:
                    region = np.random.choice(available_regions)
                else:
                    region = "Global"
                
                alt_suppliers.append({
                    "name": f"Alternative Supplier {i+1}",
                    "similarity": similarity_score,
                    "region": region,
                    "attributes": attributes,
                    "annual_revenue": f"${np.random.randint(10, 500)}M",
                    "employees": np.random.randint(50, 5000),
                    "established": np.random.randint(1970, 2015)
                })
            
            # Sort by similarity
            alt_suppliers.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Display alternative suppliers
            st.markdown(f"### Alternative Suppliers for {selected_supplier}")
            
            for supplier in alt_suppliers:
                # Calculate match percentage based on include criteria
                matches = sum(1 for c in include_criteria if supplier["attributes"][c] == "Yes")
                match_pct = (matches / len(include_criteria)) * 100 if include_criteria else 100
                
                color = "green" if supplier["similarity"] >= 80 else "orange" if supplier["similarity"] >= 70 else "red"
                
                st.markdown(f"""
                <div class="supplier-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4>{supplier['name']}</h4>
                        <span style="font-size: 1.2rem; color: {color}; font-weight: bold;">{supplier['similarity']}% Match</span>
                    </div>
                    <p><strong>Region:</strong> {supplier['region']}</p>
                    <p><strong>Annual Revenue:</strong> {supplier['annual_revenue']} | <strong>Employees:</strong> {supplier['employees']} | <strong>Established:</strong> {supplier['established']}</p>
                    <hr>
                    <p><strong>Matching Criteria:</strong> {match_pct:.0f}% of required criteria met</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                """, unsafe_allow_html=True)
                
                # Display attribute badges
                for attr, value in supplier["attributes"].items():
                    badge_color = "background-color: #d4edda; color: #155724;" if value == "Yes" else "background-color: #f8d7da; color: #721c24;"
                    st.markdown(f"""
                    <span style="padding: 5px 10px; border-radius: 15px; {badge_color}">{attr}: {value}</span>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button(f"View Profile", key=f"profile_{supplier['name']}")
                with col2:
                    st.button(f"Compare with Current", key=f"compare_{supplier['name']}")
                with col3:
                    st.button(f"Contact Supplier", key=f"contact_{supplier['name']}")
    
    # Supplier similarity network visualization
    st.markdown("### Supplier Network Analysis")
    
    # Create network data
    network_data = {
        "nodes": [
            {"id": "Current Supplier", "group": 1, "size": 20},
            {"id": "Alternative 1", "group": 2, "size": 15},
            {"id": "Alternative 2", "group": 2, "size": 15},
            {"id": "Alternative 3", "group": 2, "size": 12},
            {"id": "Alternative 4", "group": 2, "size": 10},
            {"id": "Tier 2 Supplier A", "group": 3, "size": 8},
            {"id": "Tier 2 Supplier B", "group": 3, "size": 7},
            {"id": "Tier 2 Supplier C", "group": 3, "size": 6},
            {"id": "Raw Material X", "group": 4, "size": 5},
            {"id": "Component Y", "group": 4, "size": 5}
        ],
        "links": [
            {"source": "Current Supplier", "target": "Tier 2 Supplier A", "value": 10},
            {"source": "Current Supplier", "target": "Tier 2 Supplier B", "value": 8},
            {"source": "Alternative 1", "target": "Tier 2 Supplier A", "value": 5},
            {"source": "Alternative 1", "target": "Tier 2 Supplier C", "value": 9},
            {"source": "Alternative 2", "target": "Tier 2 Supplier B", "value": 10},
            {"source": "Alternative 3", "target": "Tier 2 Supplier C", "value": 6},
            {"source": "Alternative 4", "target": "Tier 2 Supplier B", "value": 3},
            {"source": "Alternative 4", "target": "Tier 2 Supplier C", "value": 7},
            {"source": "Tier 2 Supplier A", "target": "Raw Material X", "value": 4},
            {"source": "Tier 2 Supplier B", "target": "Raw Material X", "value": 5},
            {"source": "Tier 2 Supplier C", "target": "Component Y", "value": 6}
        ]
    }
    
    # Display notice about network visualization
    st.info("Network visualization shows supplier relationships and dependencies. In a full implementation, this would display an interactive force-directed graph of supplier connections through the supply chain.")
    
    # Display insight about supplier network
    st.markdown(f"""
    ### Network Analysis Insights
    
    **Supply Chain Depth:** 3 tiers detected
    
    **Key Dependencies:**
    - {network_data["nodes"][5]["id"]} is a critical node connected to multiple suppliers
    - {network_data["nodes"][9]["id"]} represents a potential single point of failure
    
    **Diversification Opportunity:**
    Alternative suppliers 1 and 2 provide good diversification as they use different tier 2 suppliers
    """)
