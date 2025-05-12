import streamlit as st
import pandas as pd
import base64
from io import StringIO
import time

def setup_sidebar():
    """Configure and display the sidebar elements"""
    
    # Add logo and title with enhanced styling
    col1, col2 = st.sidebar.columns([1, 3])
    with col1:
        try:
            # Try to load the icon image, but handle errors gracefully
            st.image("generated-icon.png", width=80)
        except Exception:
            # If image loading fails, display a text-based icon instead
            st.markdown("""
            <div style="font-size: 32px; color: #ff6b18; text-align: center; padding-top: 10px;">
                🛒
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="margin-top: 10px;">
            <h2 style="margin: 0; color: #ff6b18; font-family: 'Poppins', sans-serif;">Command Center</h2>
            <p style="margin: 0; font-size: 0.8rem; color: #666;">Procurement Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Category Selection with improved styling
    st.sidebar.markdown('<h3 style="color: #333; font-family: Poppins, sans-serif; font-size: 1.2rem;">Category Settings</h3>', unsafe_allow_html=True)
    
    # Create categories list with Aviation added
    categories = ["Electronics", "Raw Materials", "Packaging", "Chemicals", "Aviation", "IT Services", "Logistics"]
    selected_category = st.sidebar.selectbox("Select Category", categories, help="Choose the procurement category to analyze")
    
    # Region selection (multi-select)
    regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East & Africa"]
    selected_region = st.sidebar.multiselect("Select Region(s)", regions, default=["North America", "Europe"], 
                                          help="Select one or more regions to filter the data")
    
    # Time Period selection with clearer options
    time_periods = ["Last 30 Days", "Last Quarter", "Last 6 Months", "Last Year", "Custom"]
    time_period = st.sidebar.selectbox("Time Period", time_periods, 
                                    help="Select the time period for analysis or choose 'Custom' for specific dates")
    
    # If custom time period is selected, show date inputs
    if time_period == "Custom":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
    else:
        start_date = None
        end_date = None
    
    # Data Management Section
    setup_data_management()
    
    return selected_category, selected_region, time_period, start_date, end_date

def setup_data_management():
    """Configure the data management section in the sidebar"""
    
    # Create a sidebar expander for data management with enhanced styling
    st.sidebar.markdown("---")
    st.sidebar.markdown('<h3 style="color: #333; font-family: Poppins, sans-serif; font-size: 1.2rem;">Data Intelligence</h3>', unsafe_allow_html=True)
    
    # Data Management section as a radio selection instead of tabs
    with st.sidebar.expander("📊 Data Management", expanded=False):
        data_section = st.radio("Data Management Options", 
                             ["Import Data", "Database Connection", "Web Scraping", 
                              "Data Quality", "Integration", "AI Settings"])
        
        # Import Data section
        if data_section == "Import Data":
            st.write("Import data from files:")
            
            # File uploader for different file types
            uploaded_file = st.file_uploader("Upload data file", 
                                           type=["csv", "xlsx", "json", "xml"],
                                           help="Upload your procurement data files")
            
            # Show options based on file selection
            if uploaded_file is not None:
                file_type = uploaded_file.name.split('.')[-1]
                
                if file_type == 'csv':
                    # For CSV files
                    csv_delimiter = st.selectbox("CSV Delimiter", [",", ";", "\t"], 
                                           help="Select the delimiter used in your CSV file")
                    encoding = st.selectbox("File Encoding", ["utf-8", "latin-1", "iso-8859-1"], 
                                          help="Select the encoding of your file")
                
                if file_type in ['csv', 'xlsx']:
                    st.write("Preview and import settings:")
                    header_row = st.checkbox("File has header row", value=True)
                    
                    # Add mapping options
                    st.write("Map to category:")
                    mapping_type = st.radio("Data mapping", ["Auto-detect", "Manual mapping"])
                
                # Add import button
                if st.button("Import Data", use_container_width=True):
                    with st.spinner("Importing data..."):
                        time.sleep(1.5)  # Simulate processing
                        
                        # Show success message
                        st.success(f"Successfully imported data from {uploaded_file.name}")
                        
                        # Display preview
                        try:
                            if file_type == 'csv':
                                # Read CSV
                                data = pd.read_csv(StringIO(uploaded_file.getvalue().decode('utf-8')), 
                                                delimiter=csv_delimiter)
                                st.dataframe(data.head(5), use_container_width=True)
                            elif file_type == 'xlsx':
                                # Read Excel
                                data = pd.read_excel(uploaded_file)
                                st.dataframe(data.head(5), use_container_width=True)
                        except Exception as e:
                            st.error(f"Error previewing file: {str(e)}")
                            
        # Database Connection section                
        elif data_section == "Database Connection":
            st.write("Connect to external database:")
            
            # Database type selection
            db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL", "Oracle", "SQL Server", "MongoDB"])
            
            # Connection details
            st.text_input("Host", placeholder="localhost or IP address")
            st.text_input("Port", placeholder="5432")
            st.text_input("Database Name", placeholder="procurement_db")
            st.text_input("Username", placeholder="username")
            st.text_input("Password", placeholder="password", type="password")
            
            # Test and connect buttons
            col1, col2 = st.columns(2)
            with col1:
                st.button("Test Connection", use_container_width=True)
            with col2:
                if st.button("Connect", use_container_width=True):
                    with st.spinner("Connecting to database..."):
                        time.sleep(1.5)  # Simulate processing
                        st.success("Successfully connected to database")
                        
        # Web Scraping section
        elif data_section == "Web Scraping":
            st.write("Web Scraping Configuration:")
            
            # Source type
            source_type = st.radio("Scraping Source", ["Industry News", "Supplier Websites", "Commodity Prices", "Custom URLs"])
            
            if source_type == "Industry News":
                # Industry news sources
                industry_sources = st.multiselect("Select Industry Sources", 
                                                ["Supply Chain Dive", "Procurement News", "Industry Today", 
                                                "Reuters Commodities", "Bloomberg Supply Chain"])
                
                # Keywords to track
                st.text_input("Keywords to track (comma separated)", 
                            placeholder="price increase, shortage, sustainability")
                
            elif source_type == "Supplier Websites":
                # Supplier website list
                st.text_area("Supplier Websites (one URL per line)", 
                           placeholder="https://supplier1.com\nhttps://supplier2.com")
                
                # Data to extract
                st.multiselect("Data to Extract", 
                             ["Product Information", "Pricing", "News", "Contact Information", "Location Data"])
                
            elif source_type == "Commodity Prices":
                # Commodity selection
                commodities = st.multiselect("Select Commodities", 
                                          ["Steel", "Aluminum", "Copper", "Oil", "Natural Gas", 
                                           "Plastic Resin", "Paper Pulp", "Semiconductors"])
                
                # Source selection
                st.selectbox("Data Source", ["Trading Economics API", "Markets Insider", "Web Scraping"])
                
            else:  # Custom URLs
                st.text_area("Custom URLs to Scrape (one URL per line)", 
                           placeholder="https://example.com/price-list\nhttps://commodity-news.com/steel")
                
                st.text_input("CSS Selectors (comma separated)", 
                            placeholder=".price-table, .news-item, #commodity-data")
            
            # Scheduling options
            st.subheader("Scheduling")
            schedule_freq = st.select_slider("Update Frequency", 
                                           options=["Once", "Daily", "Weekly", "Monthly"])
            
            # Execute button
            if st.button("Run Web Scraping", use_container_width=True):
                with st.spinner("Scraping data from selected sources..."):
                    time.sleep(2)  # Simulate processing
                    st.success("Successfully scraped data from web sources")
                    
                    # Show sample results
                    if source_type == "Industry News":
                        st.write("Sample scraped news items:")
                        st.info("Steel Price Increase Announced by Major Suppliers - May 05, 2023")
                        st.info("Semiconductor Shortage Expected to Ease by Q3 - May 03, 2023")
                    elif source_type == "Commodity Prices":
                        st.write("Sample commodity price data:")
                        st.info("Steel: $750/ton (↑ 2.3%)")
                        st.info("Aluminum: $2,450/ton (↓ 0.5%)")
                        
        # Data Quality section
        elif data_section == "Data Quality":
            st.write("Data Quality Management:")
            
            # Data profiling
            if st.button("Run Data Profiling", use_container_width=True):
                with st.spinner("Analyzing data quality..."):
                    time.sleep(2)  # Simulate processing
                    
                    # Sample report
                    st.success("Data quality analysis complete")
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Completeness", "92%", "3.5%")
                    with col2:
                        st.metric("Accuracy", "87%", "-2.1%")
                    with col3:
                        st.metric("Timeliness", "95%", "1.2%")
            
            # Data cleansing options
            st.subheader("Data Cleansing")
            cleansing_options = st.multiselect("Select Cleansing Operations", 
                                             ["Remove Duplicates", "Fill Missing Values", 
                                              "Standardize Formats", "Currency Conversion",
                                              "Outlier Detection"])
            
            if cleansing_options:
                if st.button("Run Data Cleansing", use_container_width=True):
                    with st.spinner("Cleansing data..."):
                        time.sleep(1.5)  # Simulate processing
                        st.success("Data cleansing operations completed successfully")
        
        # Integration section
        elif data_section == "Integration":
            st.write("Data Integration Options:")
            
            # Integration types
            integration_type = st.radio("Integration Type", 
                                     ["ERP System", "Procurement Platform", "Business Intelligence", "Custom API"])
            
            if integration_type == "ERP System":
                # ERP systems
                erp_system = st.selectbox("Select ERP System", 
                                       ["SAP", "Oracle ERP", "Microsoft Dynamics", "Infor", "Other"])
                
                if erp_system == "SAP":
                    st.selectbox("SAP Module", ["SAP MM (Materials Management)", 
                                             "SAP SRM (Supplier Relationship Management)", 
                                             "SAP Ariba", "SAP S/4HANA"])
                
                # Connection frequency
                st.select_slider("Sync Frequency", 
                              options=["Real-time", "Hourly", "Daily", "Weekly"])
                
            elif integration_type == "Procurement Platform":
                # Procurement platforms
                platform = st.selectbox("Select Platform", 
                                     ["Coupa", "SAP Ariba", "Jaggaer", "Zycus", "GEP SMART", "Other"])
                
                # Data to sync
                st.multiselect("Data to Synchronize", 
                             ["Supplier Information", "Contract Data", "Purchase Orders", 
                              "Invoices", "Catalog Items", "Pricing"])
                
            elif integration_type == "Business Intelligence":
                # BI platforms
                bi_platform = st.selectbox("Select BI Platform", 
                                        ["Power BI", "Tableau", "Qlik", "Looker", "Other"])
                
                # Refresh options
                st.select_slider("Data Refresh", 
                              options=["Manual", "Daily", "Real-time"])
                
                # Export option
                st.checkbox("Enable Direct Query", value=True,
                         help="Allow BI tool to query data directly instead of importing")
                
            else:  # Custom API
                # API configuration
                st.text_input("API Endpoint URL", 
                           placeholder="https://api.example.com/data")
                
                st.selectbox("Authentication Method", 
                          ["API Key", "OAuth 2.0", "Basic Auth", "No Authentication"])
                
                st.text_area("Request Headers (JSON)", 
                          placeholder='{\n  "Content-Type": "application/json",\n  "Authorization": "Bearer $TOKEN"\n}')
            
            # Integration button
            if st.button("Configure Integration", use_container_width=True):
                with st.spinner("Setting up data integration..."):
                    time.sleep(2)  # Simulate processing
                    st.success(f"Successfully configured {integration_type} integration")
        
        # AI Settings section
        elif data_section == "AI Settings":
            st.write("AI & LLM Configuration:")
            
            # LLM choice
            llm_type = st.radio("LLM Provider", ["OpenAI", "Anthropic", "Local LLM", "Custom"])
            
            if llm_type == "OpenAI":
                # OpenAI settings
                st.markdown("#### OpenAI API Configuration")
                st.text_input("OpenAI API Key", type="password", placeholder="sk-...", 
                           help="Your OpenAI API key for GPT-4 and other models")
                
                # Model selection
                st.selectbox("Select Model", 
                          ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "text-embedding-ada-002"])
                
                # Parameters
                col1, col2 = st.columns(2)
                with col1:
                    st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1,
                           help="Higher values make output more random, lower values more deterministic")
                with col2:
                    st.slider("Top P", min_value=0.0, max_value=1.0, value=0.95, step=0.05,
                           help="Controls diversity via nucleus sampling")
                           
                st.slider("Max Tokens", min_value=100, max_value=4000, value=1000, step=100,
                       help="Maximum length of the generated text")
                
            elif llm_type == "Anthropic":
                # Anthropic settings
                st.markdown("#### Anthropic API Configuration")
                st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...", 
                           help="Your Anthropic API key for Claude models")
                
                # Model selection
                st.selectbox("Select Model", 
                          ["claude-3-5-sonnet-20241022", "claude-3-opus", "claude-3-sonnet", "claude-3-haiku"])
                
                # Parameters
                st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1,
                       help="Higher values make output more random, lower values more deterministic")
                
                st.slider("Max Tokens", min_value=100, max_value=4000, value=1000, step=100,
                       help="Maximum length of the generated text")
                
            elif llm_type == "Local LLM":
                # Local LLM settings
                st.markdown("#### Local LLM Configuration")
                st.text_input("Model Path", placeholder="/path/to/your/model",
                           help="Path to your local LLM model files")
                
                # Model type
                st.selectbox("Model Type", 
                          ["Llama", "Mistral", "Falcon", "GPT4All", "Other"])
                
                # Parameters
                st.slider("Context Length", min_value=512, max_value=8192, value=2048, step=512,
                       help="Maximum context length in tokens")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
                with col2:
                    st.checkbox("Use GPU Acceleration", value=True)
            
            else:  # Custom
                # Custom API settings
                st.markdown("#### Custom LLM API Configuration")
                st.text_input("API Endpoint", placeholder="https://api.example.com/v1/completions")
                st.text_input("API Key", type="password")
                st.text_area("Headers (JSON)", 
                          placeholder='{\n  "Content-Type": "application/json"\n}')
                st.text_area("Request Template (JSON)", 
                          placeholder='{\n  "prompt": "$PROMPT",\n  "temperature": 0.7\n}')
            
            # Memory settings
            st.markdown("#### Memory & Context Settings")
            
            # Memory type
            memory_type = st.selectbox("Conversation Memory", 
                                   ["Session Memory", "Vector Database", "No Memory"])
            
            if memory_type == "Vector Database":
                st.selectbox("Vector DB Type", 
                          ["Pinecone", "ChromaDB", "Milvus", "Local JSON"])
                
                if st.checkbox("Show Advanced Memory Settings"):
                    st.slider("Memory Window (messages)", min_value=5, max_value=50, value=10)
                    st.slider("Relevance Threshold", min_value=0.1, max_value=0.9, value=0.7, step=0.05)
            
            # Save configuration button
            if st.button("Save AI Configuration", use_container_width=True):
                with st.spinner("Configuring AI services..."):
                    time.sleep(1.5)  # Simulate processing
                    
                    # Display OpenAI warning if no API key
                    if llm_type == "OpenAI":
                        st.warning("Please ensure you've entered a valid OpenAI API key to use GPT models.")
                    
                    # Show success message    
                    st.success(f"Successfully configured {llm_type} for AI Co-Pilot and insights")

    # Add user information and settings at the bottom of sidebar
    st.sidebar.markdown("---")
    
    # User and settings
    with st.sidebar.expander("⚙️ Settings", expanded=False):
        st.write("Theme Selection")
        theme = st.selectbox("Application Theme", ["Default", "Arcadis Orange", "Dark Mode", "Light Mode", "High Contrast"])
        
        st.write("Data Refresh Settings")
        st.select_slider("Auto-refresh interval", options=["Off", "5 min", "15 min", "30 min", "1 hour"])
        
        st.write("Export Settings")
        st.multiselect("Default Export Format", ["Excel", "CSV", "PDF", "PowerPoint"], default=["Excel"])
    
    # App information
    st.sidebar.markdown("---")
    st.sidebar.caption("Procurement Command Center v1.0")
    st.sidebar.caption("© 2023 Arcadis. All rights reserved.")