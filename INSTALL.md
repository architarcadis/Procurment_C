# Procurement Command Center - Installation Guide

## Installation Steps

### Step 1: Extract the ZIP File
Extract the ZIP file to a directory of your choice.

### Step 2: Set Up Python Environment

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

Install the required packages:

```bash
pip install streamlit pandas numpy plotly scikit-learn requests beautifulsoup4 trafilatura anthropic openai pillow
```

### Step 4: Create Streamlit Config (Optional)

For better configuration, create a `.streamlit` directory with a config file:

```bash
mkdir -p .streamlit
```

Create `.streamlit/config.toml` with the following content:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

### Step 5: Run the Application

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501 (or the port you configured).

## API Keys (Optional)

For AI-powered features, you may need to set up API keys for:
- OpenAI (for GPT-4 integration)
- Anthropic (for Claude integration)

These can be configured as environment variables:
```bash
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
```

## Project Structure

- `app.py`: Main application entry point
- `pages/`: Contains all the dashboard modules
  - `category_intelligence.py`: The Category Intelligence module
  - Other module pages (supplier_intelligence.py, price_modeling.py, etc.)
- `utils/`: Utility functions and helpers
- `data/`: Sample data files for demonstrations

## Features

- Category Intelligence: Visual analytics of category performance
- Supplier Intelligence: In-depth supplier analysis and risk assessment
- Opportunity Engine: Identification of cost-saving opportunities
- Price Modeling: Price trend analysis and forecasting
- Strategy Generator: AI-powered procurement strategy recommendations
- AI Copilot: Interactive AI assistant for procurement queries