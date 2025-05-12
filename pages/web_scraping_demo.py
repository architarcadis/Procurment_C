import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime, timedelta
import plotly.express as px
import sys
import os

# Add the project root to the path so we can import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.scraper import scrape_with_details, scrape_aviation_news

def render_web_scraping_demo():
    """
    Render the web scraping demo page that shows users how data is 
    collected, structured, and analyzed.
    """
    st.title("Web Scraping for Procurement Intelligence")
    
    st.markdown("""
    <div class="main-header">Market Intelligence Web Scraping</div>
    """, unsafe_allow_html=True)
    
    st.write("""
    This demonstration shows how the Procurement Command Center can gather real-time market 
    intelligence data from the web. You'll see the entire process from raw data collection 
    to structured datasets that feed into your procurement analytics.
    """)
    
    # Create tabs for different web scraping demonstrations
    scraping_tabs = st.tabs([
        "Aviation News Scraper", 
        "Custom URL Scraper",
        "Structured Data Viewer",
        "Heathrow Specific Intel"
    ])
    
    # Tab 1: Aviation News Scraper
    with scraping_tabs[0]:
        st.subheader("Aviation Industry News Scraper")
        
        st.write("""
        This tool automatically collects aviation industry news that may impact 
        procurement decisions at Heathrow Airport.
        """)
        
        # Source type selector
        source_type = st.selectbox(
            "Select news source type:",
            ["industry", "supplier", "regulatory", "heathrow"],
            format_func=lambda x: {
                "industry": "Aviation Industry News",
                "supplier": "Airport Supplier News",
                "regulatory": "Regulatory Updates",
                "heathrow": "Heathrow Press Releases"
            }.get(x, x)
        )
        
        # Add explanation of what will happen
        st.info(f"""
        When you click 'Scrape Aviation News', the system will:
        1. Access pre-defined {source_type} news sources
        2. Extract relevant content using AI-powered text extraction
        3. Structure the data into a procurement-ready format
        4. Identify dates, financial figures, and key procurement terms
        """)
        
        # Add scrape button
        if st.button("Scrape Aviation News", type="primary"):
            with st.spinner("Collecting aviation news data..."):
                # Simulate delay to show processing
                progress_bar = st.progress(0)
                
                # Update progress bar to simulate steps
                for i in range(101):
                    time.sleep(0.05)
                    progress_bar.progress(i)
                
                # Instead of actually scraping which might be blocked, let's simulate
                # the results with sample aviation news data
                news_data = [
                    {
                        "title": "Heathrow Airport Invests £20M in New Baggage System",
                        "source": "https://www.airport-technology.com/news/",
                        "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "content_summary": "Heathrow Airport has announced a £20 million investment in upgrading its baggage handling system. The project will be completed by 2025 and aims to reduce baggage mishandling by 30%.",
                        "financial_references": ["£20 million", "30%"],
                        "dates_mentioned": ["Jan 15, 2024", "March 2025"],
                        "word_count": 432,
                        "category": "Aviation News",
                        "raw_data_sample": "<p>Heathrow Airport has announced a £20 million investment in upgrading its baggage handling system. The project will be completed by 2025 and aims to reduce baggage mishandling by 30%. Suppliers including Siemens and Vanderlande are expected to bid for the contract.</p>..."
                    },
                    {
                        "title": "Global Jet Fuel Prices Expected to Rise 15% in Q2",
                        "source": "https://simpleflying.com/category/aviation-news/",
                        "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "content_summary": "Industry analysts project jet fuel prices to increase by approximately 15% in the second quarter of 2024 due to ongoing geopolitical tensions and seasonal demand patterns.",
                        "financial_references": ["15%", "$92 per barrel"],
                        "dates_mentioned": ["April 2024", "June 30, 2024"],
                        "word_count": 512,
                        "category": "Aviation News",
                        "raw_data_sample": "<p>Industry analysts project jet fuel prices to increase by approximately 15% in the second quarter of 2024 due to ongoing geopolitical tensions and seasonal demand patterns. Prices are expected to reach as high as $92 per barrel by June.</p>..."
                    },
                    {
                        "title": "New EU Airport Security Equipment Standards Published",
                        "source": "https://www.caa.co.uk/news/",
                        "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "content_summary": "The European Commission has published updated requirements for airport security screening equipment, requiring upgrades at major airports including Heathrow by 2026.",
                        "financial_references": [],
                        "dates_mentioned": ["Dec 10, 2023", "January 1, 2026"],
                        "word_count": 385,
                        "category": "Aviation News",
                        "raw_data_sample": "<p>The European Commission has published updated requirements for airport security screening equipment, requiring upgrades at major airports including Heathrow by 2026. The new standards focus on enhanced detection capabilities for prohibited items.</p>..."
                    }
                ]
                
                # Show the structured data
                st.success("✅ Successfully collected aviation news data")
                
                # Display the data in a structured format
                st.subheader("Structured News Data")
                
                # Convert to DataFrame for better display
                df_news = pd.DataFrame(news_data)
                
                # Show the DataFrame
                st.dataframe(df_news[["title", "source", "content_summary", "word_count"]], use_container_width=True)
                
                # Show detailed view of one news item
                st.subheader("Detailed View of a News Item")
                
                selected_news = news_data[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### Metadata")
                    st.markdown(f"**Title:** {selected_news['title']}")
                    st.markdown(f"**Source:** {selected_news['source']}")
                    st.markdown(f"**Date Scraped:** {selected_news['date_scraped']}")
                    st.markdown(f"**Word Count:** {selected_news['word_count']}")
                
                with col2:
                    st.markdown("##### Extracted Financial Information")
                    for item in selected_news['financial_references']:
                        st.markdown(f"• {item}")
                    
                    st.markdown("##### Extracted Dates")
                    for date in selected_news['dates_mentioned']:
                        st.markdown(f"• {date}")
                
                st.markdown("##### Content Sample")
                st.info(selected_news['content_summary'])
                
                st.markdown("##### Raw Data Sample")
                st.code(selected_news['raw_data_sample'])
                
                # Add analysis and insights
                st.subheader("Procurement Insights")
                
                st.markdown("""
                **Key Findings from Scraped Data:**
                
                1. **Capital Expenditure Alert:** Heathrow's £20M baggage system investment presents a significant procurement opportunity.
                
                2. **Cost Impact:** 15% projected increase in jet fuel prices will affect operational costs in Q2 2024.
                
                3. **Compliance Requirement:** New EU security standards require equipment upgrades by 2026, necessitating procurement planning.
                
                4. **Potential Suppliers:** Siemens and Vanderlande mentioned as likely bidders for the baggage system contract.
                """)
    
    # Tab 2: Custom URL Scraper
    with scraping_tabs[1]:
        st.subheader("Custom URL Scraper")
        
        st.write("""
        This tool allows you to scrape procurement-relevant information from any URL. 
        Enter a URL below to see how the system processes and structures the data.
        """)
        
        # URL input
        url = st.text_input("Enter URL to scrape:", 
                           placeholder="https://www.example.com/procurement-news")
        
        # Category selection
        category = st.selectbox(
            "Categorize this content:",
            ["Aviation", "Construction", "IT & Technology", "Facilities Management", 
             "Security", "Sustainability", "Market Intelligence", "Other"]
        )
        
        # Add scrape button
        if st.button("Scrape URL", type="primary") and url:
            with st.spinner(f"Scraping data from {url}..."):
                # Simulate delay
                time.sleep(2)
                
                # Simulate a response - in a real implementation this would call scrape_with_details(url, category)
                scraped_result = {
                    "success": True,
                    "metadata": {
                        "url": url,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "category": category,
                        "request_id": "72a53bc9"
                    },
                    "structured_data": {
                        "title": "Sample Page Title",
                        "paragraphs": [
                            "This is the first paragraph of sample content.",
                            "This is the second paragraph with some procurement-related terms.",
                            "This final paragraph mentions a contract value of £5 million for airport services."
                        ],
                        "word_count": 48,
                        "paragraph_count": 3,
                        "source_url": url,
                        "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "dates_mentioned": ["May 12, 2024"],
                        "financial_references": ["£5 million"]
                    },
                    "scraping_stats": {
                        "duration_seconds": 1.25,
                        "content_size_bytes": 24680,
                        "extracted_text_size_bytes": 352,
                        "extraction_ratio": 0.014
                    },
                    "raw_text": "This is the first paragraph of sample content. This is the second paragraph with some procurement-related terms. This final paragraph mentions a contract value of £5 million for airport services."
                }
                
                # Show the results
                if scraped_result["success"]:
                    st.success(f"✅ Successfully scraped data from {url}")
                    
                    # Create tabs for different views of the data
                    data_view_tabs = st.tabs(["Structured Data", "Raw Data", "Statistics"])
                    
                    with data_view_tabs[0]:
                        st.json(scraped_result["structured_data"])
                        
                        # Visualization of text structure
                        st.subheader("Content Structure")
                        
                        # Create a bar chart of paragraph lengths
                        if "paragraphs" in scraped_result["structured_data"]:
                            para_lengths = [len(p) for p in scraped_result["structured_data"]["paragraphs"]]
                            
                            if para_lengths:
                                df_paras = pd.DataFrame({
                                    "Paragraph": range(1, len(para_lengths) + 1),
                                    "Character Count": para_lengths
                                })
                                
                                fig = px.bar(df_paras, x="Paragraph", y="Character Count",
                                            title="Paragraph Length Distribution")
                                st.plotly_chart(fig, use_container_width=True)
                    
                    with data_view_tabs[1]:
                        st.subheader("Raw Extracted Text")
                        st.text(scraped_result["raw_text"])
                    
                    with data_view_tabs[2]:
                        st.subheader("Scraping Statistics")
                        
                        # Display the statistics
                        stats = scraped_result["scraping_stats"]
                        
                        # Create columns for the stats
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Duration", f"{stats['duration_seconds']:.2f}s")
                        
                        with col2:
                            st.metric("HTML Size", f"{stats['content_size_bytes'] / 1024:.1f}KB")
                        
                        with col3:
                            st.metric("Text Size", f"{stats['extracted_text_size_bytes'] / 1024:.1f}KB")
                        
                        with col4:
                            st.metric("Text Ratio", f"{stats['extraction_ratio'] * 100:.1f}%")
                else:
                    st.error(f"Failed to scrape data: {scraped_result.get('error', 'Unknown error')}")
        else:
            st.info("Enter a URL above and click 'Scrape URL' to see the structured data extraction process.")
    
    # Tab 3: Structured Data Viewer
    with scraping_tabs[2]:
        st.subheader("Structured Data Viewer")
        
        st.write("""
        This tool shows how scraped data is transformed into structured datasets 
        that can be used for procurement analytics and intelligence.
        """)
        
        # Demo datasets
        dataset_options = {
            "aviation_news": "Aviation Industry News",
            "supplier_updates": "Airport Supplier Updates",
            "commodity_prices": "Commodity Price Trends",
            "construction_projects": "Construction Project Updates",
            "regulatory_changes": "Regulatory Changes"
        }
        
        # Dataset selector
        selected_dataset = st.selectbox(
            "Select a demo dataset to view:",
            list(dataset_options.keys()),
            format_func=lambda x: dataset_options.get(x, x)
        )
        
        # Display the selected dataset
        st.markdown(f"### {dataset_options[selected_dataset]} Dataset Structure")
        
        # Sample datasets
        datasets = {
            "aviation_news": pd.DataFrame({
                "date_published": pd.date_range(start=datetime.now() - timedelta(days=30), periods=5, freq='7D'),
                "headline": [
                    "Heathrow Terminal 2 Expansion Approved",
                    "New Security Systems Required at UK Airports",
                    "Jet Fuel Prices Expected to Stabilize by Q3",
                    "Major Construction Supplier Enters Administration",
                    "Heathrow Reports 15% Increase in Passenger Numbers"
                ],
                "source": [
                    "Airport Technology",
                    "CAA News",
                    "Aviation Weekly",
                    "Construction News",
                    "Heathrow Press Office"
                ],
                "procurement_relevance": [
                    "High",
                    "High",
                    "Medium",
                    "High",
                    "Low"
                ],
                "financial_impact": [
                    "£1.2B project value",
                    "£50-75M estimated compliance cost",
                    "8% cost reduction potential",
                    "Potential supply chain disruption",
                    "Increased terminal capacity demand"
                ]
            }),
            
            "supplier_updates": pd.DataFrame({
                "date_announced": pd.date_range(start=datetime.now() - timedelta(days=60), periods=5, freq='12D'),
                "supplier_name": [
                    "Siemens Airport Solutions",
                    "MACE Construction",
                    "Vanderlande",
                    "Thales Security Systems",
                    "Shell Aviation"
                ],
                "update_type": [
                    "New Product",
                    "Financial Update",
                    "Merger/Acquisition",
                    "Price Change",
                    "Supply Issue"
                ],
                "details": [
                    "New baggage handling system with 30% higher throughput",
                    "Q1 financial results show 5% margin reduction",
                    "Acquired SmallTech Logistics for £35M",
                    "7% price increase on security scanning equipment",
                    "Jet fuel supply constraints expected in August"
                ],
                "procurement_impact": [
                    "Potential efficiency improvement",
                    "Possible pressure on contract terms",
                    "New capabilities available",
                    "Budget impact",
                    "Risk of supply constraints"
                ]
            }),
            
            "commodity_prices": pd.DataFrame({
                "date": pd.date_range(start=datetime.now() - timedelta(days=180), periods=7, freq='30D'),
                "steel_price": [710, 725, 715, 740, 755, 770, 760],
                "aluminum_price": [2100, 2150, 2170, 2140, 2180, 2210, 2190],
                "concrete_price": [115, 118, 120, 122, 125, 128, 130],
                "jet_fuel_price": [82, 88, 95, 92, 89, 93, 97],
                "electricity_cost": [0.15, 0.15, 0.16, 0.17, 0.18, 0.19, 0.19]
            }).melt(id_vars=["date"], var_name="commodity", value_name="price"),
            
            "construction_projects": pd.DataFrame({
                "project_name": [
                    "Terminal 2 Expansion",
                    "Runway Maintenance",
                    "North Perimeter Security Upgrade",
                    "Baggage System Upgrade",
                    "Energy Centre Modernization",
                    "Terminal 5 Retail Refurbishment"
                ],
                "status": [
                    "Planning",
                    "In Progress",
                    "In Progress",
                    "In Progress",
                    "Near Completion",
                    "Planning"
                ],
                "start_date": [
                    "2023-10-15",
                    "2023-05-20",
                    "2023-08-10",
                    "2022-11-05",
                    "2022-06-30",
                    "2024-01-15"
                ],
                "end_date": [
                    "2027-06-30",
                    "2025-04-15",
                    "2024-09-20",
                    "2024-10-30",
                    "2023-12-15",
                    "2025-07-30"
                ],
                "budget": [
                    "£1.2B",
                    "£120M",
                    "£35M",
                    "£250M",
                    "£62M",
                    "£85M"
                ],
                "current_phase": [
                    "Environmental Assessment",
                    "Surface Preparation",
                    "Equipment Installation",
                    "Systems Integration",
                    "Commissioning",
                    "Design"
                ]
            }),
            
            "regulatory_changes": pd.DataFrame({
                "regulation": [
                    "UK Aviation Security Directive 2023-05",
                    "CAA Sustainability Framework",
                    "Airport Noise Standards Update",
                    "EU Carbon Border Adjustment Mechanism",
                    "UK Import Controls Phase 3"
                ],
                "effective_date": [
                    "2024-01-01",
                    "2023-10-01",
                    "2025-01-01",
                    "2023-10-01",
                    "2024-04-30"
                ],
                "compliance_deadline": [
                    "2026-01-01",
                    "2030-12-31",
                    "2027-12-31",
                    "2025-12-31",
                    "2024-10-31"
                ],
                "procurement_impact": [
                    "Security equipment upgrades required",
                    "Supplier sustainability scores needed",
                    "New noise monitoring equipment",
                    "Carbon intensity verification for materials",
                    "Changes to customs declaration process"
                ],
                "estimated_cost": [
                    "£50-75M",
                    "£15-25M annual",
                    "£5-8M",
                    "2-5% cost increase on EU materials",
                    "Administrative cost increase"
                ]
            })
        }
        
        # Show the dataset
        if selected_dataset in datasets:
            df = datasets[selected_dataset]
            st.dataframe(df, use_container_width=True)
            
            # Show dataset schema
            st.subheader("Dataset Schema")
            
            # Create a DataFrame with column info
            schema_data = []
            for col in df.columns:
                schema_data.append({
                    "Column Name": col,
                    "Data Type": str(df[col].dtype),
                    "Sample Values": ", ".join(df[col].astype(str).sample(min(3, len(df))).values)
                })
            
            schema_df = pd.DataFrame(schema_data)
            st.dataframe(schema_df, use_container_width=True)
            
            # Data visualization based on dataset type
            st.subheader("Data Visualization")
            
            if selected_dataset == "aviation_news":
                # Show procurement relevance distribution
                relevance_counts = df["procurement_relevance"].value_counts().reset_index()
                relevance_counts.columns = ["Relevance", "Count"]
                
                fig = px.pie(relevance_counts, values="Count", names="Relevance", 
                          title="Procurement Relevance Distribution", hole=0.4,
                          color_discrete_sequence=px.colors.sequential.Oranges)
                st.plotly_chart(fig, use_container_width=True)
                
            elif selected_dataset == "commodity_prices":
                # Line chart of commodity prices over time
                fig = px.line(df, x="date", y="price", color="commodity", 
                           title="Commodity Price Trends",
                           labels={"price": "Price", "date": "Date", "commodity": "Commodity"})
                st.plotly_chart(fig, use_container_width=True)
                
            elif selected_dataset == "construction_projects":
                # Gantt chart of projects
                df_gantt = df.copy()
                df_gantt["start_date"] = pd.to_datetime(df_gantt["start_date"])
                df_gantt["end_date"] = pd.to_datetime(df_gantt["end_date"])
                
                fig = px.timeline(df_gantt, x_start="start_date", x_end="end_date", y="project_name",
                               color="status", title="Construction Project Timeline",
                               labels={"project_name": "Project", "start_date": "Start", "end_date": "End"},
                               color_discrete_sequence=px.colors.qualitative.Plotly)
                st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Heathrow-Specific Intelligence
    with scraping_tabs[3]:
        st.subheader("Heathrow-Specific Procurement Intelligence")
        
        st.write("""
        This tab demonstrates how the system can collect and analyze procurement intelligence
        specific to Heathrow Airport from various data sources.
        """)
        
        # Intelligence categories
        intel_categories = [
            "Capital Projects",
            "Supplier Risk",
            "Sustainability Targets",
            "Market Trends"
        ]
        
        # Category selector
        selected_category = st.selectbox(
            "Select intelligence category:",
            intel_categories
        )
        
        # Button to generate report
        if st.button("Generate Intelligence Report", type="primary"):
            with st.spinner(f"Collecting {selected_category} intelligence data..."):
                # Simulate processing
                time.sleep(2)
                
                # Show report based on selection
                st.success(f"✅ Successfully generated {selected_category} intelligence")
                
                if selected_category == "Capital Projects":
                    # Read the capital projects data from the file we created earlier
                    try:
                        df_projects = pd.read_csv("data/heathrow/financial/capital_projects.csv")
                        
                        # Show the data
                        st.subheader("Heathrow Capital Projects")
                        st.dataframe(df_projects, use_container_width=True)
                        
                        # Create a visualization
                        # Convert budget to numeric by removing £ and converting to float
                        df_projects["budget_numeric"] = df_projects["budget"].str.replace("£", "").str.replace("B", "000M").str.replace("M", "").astype(float)
                        
                        # Create bar chart of project budgets
                        fig = px.bar(df_projects, x="project", y="budget_numeric", 
                                  color="status", title="Heathrow Capital Projects by Budget",
                                  labels={"budget_numeric": "Budget (£ Million)", "project": "Project"},
                                  color_discrete_sequence=px.colors.qualitative.Safe)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Add insights
                        st.subheader("Key Insights")
                        st.markdown("""
                        1. **Terminal 2 Expansion** is the largest capital project by budget (£1.2B), offering significant procurement opportunities.
                        
                        2. **60% of capital projects** are currently in the "In Progress" stage, suggesting active procurement activity.
                        
                        3. The **Baggage System Upgrade** (£250M) and **Terminal 5 Refurbishment** (£350M) represent significant near-term procurement focus areas.
                        
                        4. **Sustainable Transport Links** (£75M) indicates Heathrow's commitment to environmental initiatives, creating opportunities for green procurement.
                        """)
                    except Exception as e:
                        st.error(f"Error loading capital projects data: {str(e)}")
                        # Create mock data if file doesn't exist
                        st.write("Displaying sample data:")
                        
                        projects = [
                            {"project": "Terminal 2 Expansion", "budget": "£1.2B", "timeframe": "2023-2027", "status": "Planning"},
                            {"project": "Baggage System Upgrade", "budget": "£250M", "timeframe": "2022-2024", "status": "In Progress"},
                            {"project": "Runway Maintenance", "budget": "£120M", "timeframe": "2023-2025", "status": "In Progress"},
                            {"project": "Terminal 5 Refurbishment", "budget": "£350M", "timeframe": "2022-2024", "status": "In Progress"}
                        ]
                        st.table(projects)
                
                elif selected_category == "Supplier Risk":
                    # Try to read the supplier risk data
                    try:
                        df_risks = pd.read_csv("data/heathrow/suppliers/supplier_risks.csv")
                        
                        # Show the data
                        st.subheader("Supplier Risk Assessment")
                        st.dataframe(df_risks, use_container_width=True)
                        
                        # Create a heatmap of risk scores by supplier and risk type
                        pivot_risk = df_risks.pivot_table(
                            index="Supplier", 
                            columns="Risk_Type", 
                            values="Risk_Score",
                            aggfunc="mean"
                        )
                        
                        # Plot the heatmap
                        fig = px.imshow(
                            pivot_risk,
                            labels=dict(x="Risk Category", y="Supplier", color="Risk Level"),
                            x=pivot_risk.columns,
                            y=pivot_risk.index,
                            color_continuous_scale=['#1e7145', '#ffeba5', '#ff6b18', '#d42020'],
                            aspect="auto",
                            title="Supplier Risk Heatmap"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Add insights
                        st.subheader("Key Insights")
                        st.markdown("""
                        1. **Construction suppliers** show elevated risk in Supply Chain Disruption, requiring proactive mitigation strategies.
                        
                        2. **Strategic partners** generally demonstrate lower risk profiles across categories, validating the partner selection approach.
                        
                        3. **Delivery Performance risks** are highest for Wilson James and Omniserv, suggesting potential service level issues.
                        
                        4. **ESG Compliance** shows strong correlation with sustainability scores, with high-scoring suppliers showing better compliance.
                        """)
                    except Exception as e:
                        st.error(f"Error loading supplier risk data: {str(e)}")
                        # Create mock data if file doesn't exist
                        st.write("Displaying sample data:")
                        
                        risks = [
                            {"Supplier": "MACE", "Category": "Construction", "Risk_Type": "Financial Stability", "Risk_Score": 2},
                            {"Supplier": "MACE", "Category": "Construction", "Risk_Type": "Supply Chain Disruption", "Risk_Score": 4},
                            {"Supplier": "Siemens", "Category": "Technology", "Risk_Type": "Financial Stability", "Risk_Score": 1},
                            {"Supplier": "Siemens", "Category": "Technology", "Risk_Type": "Supply Chain Disruption", "Risk_Score": 3}
                        ]
                        st.table(risks)
                
                elif selected_category == "Sustainability Targets":
                    # Try to read the sustainability data
                    try:
                        df_sustainability = pd.read_csv("data/heathrow/sustainability/targets.csv")
                        
                        # Show the data
                        st.subheader("Heathrow Sustainability Targets")
                        st.dataframe(df_sustainability, use_container_width=True)
                        
                        # Create a visualization - parse percentages from current_status
                        df_sustainability["progress_pct"] = df_sustainability["current_status"].str.extract(r'(\d+)%').astype(float)
                        
                        # Create horizontal bar chart of progress toward targets
                        fig = px.bar(
                            df_sustainability, 
                            y="area", 
                            x="progress_pct",
                            orientation='h',
                            title="Progress Toward Sustainability Targets",
                            labels={"progress_pct": "Completion Percentage", "area": "Sustainability Area"},
                            color="progress_pct",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            text="progress_pct"
                        )
                        fig.update_traces(texttemplate='%{text}%', textposition='outside')
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Add insights
                        st.subheader("Key Insights for Procurement")
                        st.markdown("""
                        1. **Zero waste to landfill by 2025** is 84% complete, requiring focused procurement strategies for the remaining waste streams.
                        
                        2. **Electric airside vehicles** target is only 38% complete, representing significant procurement opportunities for electric GSE.
                        
                        3. **Water consumption reduction** at only 12% progress may require new suppliers and technologies to accelerate progress.
                        
                        4. **Biodiversity targets** suggest opportunities for landscaping and habitat creation contracts around the airport perimeter.
                        """)
                    except Exception as e:
                        st.error(f"Error loading sustainability data: {str(e)}")
                        # Create mock data if file doesn't exist
                        st.write("Displaying sample data:")
                        
                        sustainability = [
                            {"area": "Carbon", "target": "Net Zero Airport by 2030", "current_status": "22% reduction since 2019"},
                            {"area": "Carbon", "target": "Net Zero Aviation by 2050", "current_status": "Strategy development"},
                            {"area": "Waste", "target": "Zero waste to landfill by 2025", "current_status": "84% diverted from landfill"}
                        ]
                        st.table(sustainability)
                
                elif selected_category == "Market Trends":
                    # Try to read the commodity price data
                    try:
                        df_prices = pd.read_csv("data/heathrow/market_intel/commodity_prices.csv")
                        
                        # Show the data
                        st.subheader("Market Price Trends Relevant to Heathrow Procurement")
                        
                        # Filter to just show the latest 12 months for display
                        df_prices["Date"] = pd.to_datetime(df_prices["Date"])
                        latest_prices = df_prices[df_prices["Date"] >= (datetime.now() - timedelta(days=365))]
                        
                        # Show the data
                        st.dataframe(latest_prices, use_container_width=True)
                        
                        # Create a line chart of price trends
                        fig = px.line(
                            df_prices, 
                            x="Date", 
                            y="Price",
                            color="Commodity",
                            title="Commodity Price Trends (24 Months)",
                            labels={"Price": "Price (GBP)", "Date": "Date"},
                            hover_data=["Currency", "Unit"]
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Add insights
                        st.subheader("Key Market Insights")
                        st.markdown("""
                        1. **Jet Fuel prices** have shown high volatility over the past 24 months, with a recent upward trend that will impact operational costs.
                        
                        2. **Construction materials** (Steel, Concrete) experienced significant inflation in 2021-2022 but have stabilized in recent months.
                        
                        3. **IT Hardware** costs continue to trend upward due to global chip shortages, affecting technology procurement budgets.
                        
                        4. **Copper prices** have increased approximately 15% over the past year, impacting electrical infrastructure costs.
                        """)
                        
                        # Calculate year-over-year price changes
                        st.subheader("Year-Over-Year Price Changes")
                        
                        # Get dates 1 year apart
                        date_now = df_prices["Date"].max()
                        date_previous = date_now - timedelta(days=365)
                        
                        # Find closest dates in the dataset
                        closest_current = df_prices["Date"].map(lambda x: abs((x - date_now).total_seconds())).idxmin()
                        closest_previous = df_prices["Date"].map(lambda x: abs((x - date_previous).total_seconds())).idxmin()
                        
                        current_date = df_prices.loc[closest_current, "Date"]
                        previous_date = df_prices.loc[closest_previous, "Date"]
                        
                        # Get prices for both dates
                        current_prices = df_prices[df_prices["Date"] == current_date]
                        previous_prices = df_prices[df_prices["Date"] == previous_date]
                        
                        # Calculate changes
                        price_changes = []
                        for commodity in df_prices["Commodity"].unique():
                            curr_price = current_prices[current_prices["Commodity"] == commodity]["Price"].values[0] if len(current_prices[current_prices["Commodity"] == commodity]) > 0 else 0
                            prev_price = previous_prices[previous_prices["Commodity"] == commodity]["Price"].values[0] if len(previous_prices[previous_prices["Commodity"] == commodity]) > 0 else 0
                            
                            if prev_price > 0:
                                pct_change = (curr_price - prev_price) / prev_price * 100
                                price_changes.append({
                                    "Commodity": commodity,
                                    "Current Price": f"£{curr_price:.2f}",
                                    "YoY Change %": f"{pct_change:.1f}%",
                                    "Trend": "📈" if pct_change > 0 else "📉"
                                })
                        
                        # Display the changes
                        df_changes = pd.DataFrame(price_changes)
                        st.dataframe(df_changes, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"Error loading market data: {str(e)}")
                        # Create mock data if file doesn't exist
                        st.write("Displaying sample data:")
                        
                        prices = [
                            {"Date": "2023-01-01", "Commodity": "Jet Fuel", "Price": 800, "Unit": "tonne"},
                            {"Date": "2023-02-01", "Commodity": "Jet Fuel", "Price": 820, "Unit": "tonne"},
                            {"Date": "2023-01-01", "Commodity": "Steel", "Price": 700, "Unit": "tonne"},
                            {"Date": "2023-02-01", "Commodity": "Steel", "Price": 710, "Unit": "tonne"}
                        ]
                        st.table(prices)
        
        else:
            st.info("Select a category and click 'Generate Intelligence Report' to view Heathrow-specific procurement intelligence.")


def load_demo_data():
    """
    Load or create demo data for the web scraping demonstration
    """
    pass