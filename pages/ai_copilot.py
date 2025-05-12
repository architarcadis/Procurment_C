import streamlit as st
import time
import pandas as pd
import numpy as np
from utils.llm_helper import SimpleLLM

# Configure page
st.set_page_config(
    page_title="AI Co-Pilot - Procurement Command Center",
    page_icon="🧠",
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
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #f0f2f6;
    }
    .chat-message.assistant {
        background-color: #e6f3ff;
    }
    .chat-message .content {
        display: flex;
        padding-left: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# 🧠 AI Co-Pilot")
    st.markdown("---")
    
    # Category selector
    categories = ["Electronics", "Raw Materials", "Packaging", "Office Supplies", 
                 "IT Services", "Logistics", "Chemicals", "Machinery"]
    selected_category = st.selectbox("Select Category", categories)
    
    st.markdown("---")
    st.markdown("### Conversation History")
    
    # Display conversation history
    if "messages" in st.session_state:
        for i, msg in enumerate(st.session_state.messages):
            if i > 0:  # Skip the system message
                st.markdown(f"**{msg['role'].title()}**: {msg['content'][:50]}...")
    
    # Clear conversation button
    if st.button("Clear Conversation"):
        if "messages" in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "You are an AI procurement co-pilot that provides strategic insights and recommendations on procurement categories."}
            ]
        st.success("Conversation cleared!")

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI procurement co-pilot that provides strategic insights and recommendations on procurement categories."}
    ]

# Initialize LLM helper
llm = SimpleLLM()

# Main content
st.markdown('<div class="main-header">AI Procurement Co-Pilot</div>', unsafe_allow_html=True)
st.markdown(f"#### Selected Category: {selected_category}")

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

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.container():
            st.markdown(f"""
            <div class="chat-message {message['role']}">
                <div><strong>{message['role'].title()}</strong></div>
                <div class="content">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Ask about your procurement category...")

if prompt:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.container():
        st.markdown(f"""
        <div class="chat-message user">
            <div><strong>User</strong></div>
            <div class="content">
                {prompt}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate response with loading indicator
    with st.status("Thinking...", expanded=True) as status:
        st.write("Analyzing procurement data...")
        time.sleep(0.5)
        st.write("Reviewing market trends...")
        time.sleep(0.5)
        st.write("Generating insights...")
        time.sleep(0.5)
        
        # Generate response using the LLM helper
        response = llm.generate_response(prompt, selected_category)
        
        status.update(label="Response ready!", state="complete", expanded=False)
    
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response
    with st.container():
        st.markdown(f"""
        <div class="chat-message assistant">
            <div><strong>AI Co-Pilot</strong></div>
            <div class="content">
                {response}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Additional features section
st.markdown("---")
st.markdown("### Advanced Features")

# Create tabs for different features
tab1, tab2, tab3 = st.tabs(["Category Deep Dive", "Negotiation Coach", "Document Analysis"])

with tab1:
    st.markdown("#### Category Deep Dive")
    st.write("Get comprehensive analysis of your selected category including price trends, supplier landscape, and strategic recommendations.")
    
    if st.button("Generate Category Deep Dive"):
        with st.spinner("Generating comprehensive category analysis..."):
            time.sleep(2)
            
            # This would be replaced with actual content generation in a production app
            response = llm.generate_response(f"Provide a comprehensive analysis of the {selected_category} category including market trends, supplier landscape, and strategic recommendations", selected_category)
            
            st.markdown(f"""
            <div class="chat-message assistant">
                <div><strong>Category Analysis</strong></div>
                <div class="content">
                    {response}
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("#### Negotiation Coach")
    st.write("Get tailored negotiation advice for your specific supplier engagement.")
    
    supplier_name = st.text_input("Supplier Name")
    negotiation_goal = st.selectbox(
        "Negotiation Goal",
        ["Price Reduction", "Contract Extension", "Service Level Improvement", "Payment Terms Extension", "Volume Commitment"]
    )
    
    if st.button("Get Negotiation Advice") and supplier_name:
        with st.spinner("Generating negotiation strategies..."):
            time.sleep(2)
            
            # This would be replaced with actual content generation in a production app
            response = llm.generate_response(f"Provide negotiation strategies for {negotiation_goal} with supplier {supplier_name} in the {selected_category} category", selected_category)
            
            st.markdown(f"""
            <div class="chat-message assistant">
                <div><strong>Negotiation Strategy</strong></div>
                <div class="content">
                    {response}
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("#### Document Analysis")
    st.write("Upload procurement documents for AI analysis.")
    
    uploaded_file = st.file_uploader("Upload contract or RFP document", type=["pdf", "docx", "txt"])
    
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        
        if st.button("Analyze Document"):
            with st.spinner("Analyzing document..."):
                time.sleep(2)
                
                # This would be replaced with actual document analysis in a production app
                st.markdown("""
                ### Document Analysis Results
                
                **Document Type:** Contract
                
                **Key Terms:**
                - Contract Value: $1.2M
                - Term: 24 months
                - Renewal: Automatic 12-month renewal
                - Termination Notice: 90 days
                
                **Risks Identified:**
                - No price protection clause
                - Limited supplier liability ($500K cap)
                - Exclusive supplier arrangement
                
                **Opportunities:**
                - Negotiate volume-based discounts
                - Add performance metrics and SLAs
                - Include benchmarking clause
                """)
