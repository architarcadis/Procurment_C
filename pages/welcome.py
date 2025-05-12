import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

def render_welcome_page():
    """Render the welcome page content"""
    
    # Hero section with visually appealing header
    st.markdown("""
    <div style="text-align: center; padding: 1rem; margin-bottom: 2rem;">
        <h1 style="color: #ff6b18; font-size: 2.5rem; margin-bottom: 0.5rem;">Procurement Command Center</h1>
        <p style="font-size: 1.2rem; color: #555;">Your AI-Powered Procurement Decision Hub</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for benefits by role
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="border-radius: 10px; background-color: #f8f9fa; padding: 1.5rem; height: 100%; border-left: 5px solid #ff6b18;">
            <h3 style="color: #ff6b18; margin-bottom: 1rem;">For Category Managers</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">🔍</div>
                    <div>360° view of your category</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">📊</div>
                    <div>Predictive price modeling</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">🤝</div>
                    <div>Supplier risk assessment</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">💡</div>
                    <div>AI-powered strategies</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">⏱️</div>
                    <div>Time-saving automation</div>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="border-radius: 10px; background-color: #f8f9fa; padding: 1.5rem; height: 100%; border-left: 5px solid #1e88e5;">
            <h3 style="color: #1e88e5; margin-bottom: 1rem;">For Procurement Directors</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">💼</div>
                    <div>Portfolio-level insights</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">📈</div>
                    <div>Savings opportunity tracking</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">🔄</div>
                    <div>Strategic alignment</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">🎯</div>
                    <div>Performance monitoring</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">🌐</div>
                    <div>Cross-category optimization</div>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="border-radius: 10px; background-color: #f8f9fa; padding: 1.5rem; height: 100%; border-left: 5px solid #43a047;">
            <h3 style="color: #43a047; margin-bottom: 1rem;">For Finance & Executives</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">💰</div>
                    <div>Cost visibility & control</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">📋</div>
                    <div>Executive summaries</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">⚠️</div>
                    <div>Risk mitigation</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">📱</div>
                    <div>On-demand reporting</div>
                </li>
                <li style="margin-bottom: 0.8rem; display: flex;">
                    <div style="margin-right: 10px;">🔮</div>
                    <div>Future cost projections</div>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Tool Overview Section
    st.markdown("---")
    st.markdown("## Your Procurement Journey")
    st.markdown("""
    <p style="font-size: 1.1rem;">
    The Procurement Command Center guides you through a complete procurement journey, 
    from intelligence gathering to strategic execution. Each tab represents a stage in this journey.
    </p>
    """, unsafe_allow_html=True)
    
    # Tabs overview
    st.markdown("""
    <div style="display: flex; flex-direction: column; gap: 1rem; margin-top: 1.5rem;">
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; align-items: center; border-left: 5px solid #ff6b18;">
            <div style="font-size: 2rem; margin-right: 1rem; color: #ff6b18;">📊</div>
            <div>
                <h4 style="margin: 0; color: #333;">Category Intelligence</h4>
                <p style="margin: 0; color: #666;">Comprehensive market insights, category health assessment, and key metrics tracking.</p>
            </div>
        </div>
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; align-items: center; border-left: 5px solid #1e88e5;">
            <div style="font-size: 2rem; margin-right: 1rem; color: #1e88e5;">🧠</div>
            <div>
                <h4 style="margin: 0; color: #333;">AI Co-Pilot</h4>
                <p style="margin: 0; color: #666;">Your intelligent procurement assistant - ask questions and get instant insights.</p>
            </div>
        </div>
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; align-items: center; border-left: 5px solid #7b1fa2;">
            <div style="font-size: 2rem; margin-right: 1rem; color: #7b1fa2;">📈</div>
            <div>
                <h4 style="margin: 0; color: #333;">Price Modeling</h4>
                <p style="margin: 0; color: #666;">Forecast prices, analyze trends, and create should-cost models for better negotiations.</p>
            </div>
        </div>
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; align-items: center; border-left: 5px solid #43a047;">
            <div style="font-size: 2rem; margin-right: 1rem; color: #43a047;">🏢</div>
            <div>
                <h4 style="margin: 0; color: #333;">Supplier Intelligence</h4>
                <p style="margin: 0; color: #666;">Deep supplier profiles, risk assessment, and alternative supplier recommendations.</p>
            </div>
        </div>
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; align-items: center; border-left: 5px solid #fb8c00;">
            <div style="font-size: 2rem; margin-right: 1rem; color: #fb8c00;">🧭</div>
            <div>
                <h4 style="margin: 0; color: #333;">Strategy Generator</h4>
                <p style="margin: 0; color: #666;">Create procurement strategies with SWOT analysis, playbooks, and stakeholder alignment.</p>
            </div>
        </div>
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; align-items: center; border-left: 5px solid #e53935;">
            <div style="font-size: 2rem; margin-right: 1rem; color: #e53935;">⚡</div>
            <div>
                <h4 style="margin: 0; color: #333;">Opportunity Engine</h4>
                <p style="margin: 0; color: #666;">Automatically identify savings opportunities with impact assessments and action plans.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Management section
    st.markdown("---")
    st.markdown("## Managing Your Data")
    st.markdown("""
    <p style="font-size: 1.1rem;">
    The Data Management panel in the sidebar provides powerful tools to import, connect, and enhance your procurement data:
    </p>
    """, unsafe_allow_html=True)
    
    # Data options
    data_col1, data_col2 = st.columns(2)
    
    with data_col1:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; height: 100%;">
            <h4 style="color: #ff6b18; margin-bottom: 0.8rem;">Import & Connect</h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 0.5rem;">📄 Upload CSV, Excel, or JSON files</li>
                <li style="margin-bottom: 0.5rem;">🗄️ Connect to external databases</li>
                <li style="margin-bottom: 0.5rem;">🔄 Auto-refresh from data sources</li>
                <li style="margin-bottom: 0.5rem;">🔍 Intelligent data mapping</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with data_col2:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; height: 100%;">
            <h4 style="color: #1e88e5; margin-bottom: 0.8rem;">Web Scraping & Analysis</h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 0.5rem;">🌐 Scrape supplier websites & news</li>
                <li style="margin-bottom: 0.5rem;">💱 Capture commodity price data</li>
                <li style="margin-bottom: 0.5rem;">📊 Analyze data quality</li>
                <li style="margin-bottom: 0.5rem;">🧹 Clean and transform procurement data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Getting Started guide
    st.markdown("---")
    st.markdown("## Getting Started")
    
    # Steps for getting started
    st.markdown("""
    <ol style="font-size: 1.05rem; line-height: 1.6;">
        <li><strong>Select Your Category</strong> - Choose your procurement category from the sidebar</li>
        <li><strong>Import Your Data</strong> - Use the Data Management panel to upload or connect to your data</li>
        <li><strong>Explore Intelligence</strong> - Start with the Category Intelligence tab for a complete overview</li>
        <li><strong>Generate Insights</strong> - Use the AI Co-Pilot to ask specific questions about your category</li>
        <li><strong>Develop Strategy</strong> - Move to the Strategy Generator to create data-driven procurement plans</li>
    </ol>
    """, unsafe_allow_html=True)
    
    # AI Commentary section
    st.markdown("---")
    st.markdown("## AI Insights & Assistance")
    
    st.markdown("""
    <div style="background-color: #f5f5f5; padding: 1.5rem; border-radius: 10px; margin-top: 1rem; border-left: 5px solid #ff6b18;">
        <h4 style="margin-top: 0; color: #ff6b18;">How AI Enhances Your Procurement Process</h4>
        <p>
        The Procurement Command Center leverages advanced AI to provide context-aware insights throughout your 
        procurement journey:
        </p>
        <ul>
            <li><strong>Natural Language Understanding</strong> - Ask questions in plain language through the AI Co-Pilot</li>
            <li><strong>Predictive Analytics</strong> - Forecast price trends and identify future risks</li>
            <li><strong>Pattern Recognition</strong> - Detect savings opportunities and supplier issues automatically</li>
            <li><strong>Intelligent Data Processing</strong> - Extract insights from unstructured data like contracts and news</li>
            <li><strong>Strategic Recommendations</strong> - Receive tailored procurement strategies based on your specific scenario</li>
        </ul>
        <p style="font-style: italic; margin-top: 1rem;">
        "The AI capabilities in this tool don't replace the procurement professional - they augment your expertise 
        and help you make more strategic, data-driven decisions."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Final call to action
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <p style="font-size: 1.2rem; font-weight: bold; margin-bottom: 1rem;">Ready to transform your procurement process?</p>
        <p style="font-size: 1.1rem; color: #666;">Select a category in the sidebar and begin your journey through the tabs above</p>
    </div>
    """, unsafe_allow_html=True)