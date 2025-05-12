import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_category_health_data(category):
    """Generate mock category health score trend data"""
    np.random.seed(hash(category) % 100)  # Consistent seed based on category
    
    # Generate dates for the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Generate health scores with some trend and noise
    base_score = np.random.randint(70, 85)
    trend = np.random.choice([-0.2, 0, 0.3])  # Downward, flat, or upward trend
    noise = np.random.normal(0, 3, size=len(dates))
    
    scores = [
        min(100, max(0, base_score + trend * i + noise[i]))
        for i in range(len(dates))
    ]
    
    return pd.DataFrame({
        'Date': dates,
        'Health Score': scores
    })

def generate_supplier_data(category):
    """Generate mock supplier data for quadrant analysis"""
    np.random.seed(hash(category) % 100)  # Consistent seed based on category
    
    # Number of suppliers varies by category
    n_suppliers = np.random.randint(8, 15)
    
    suppliers = [f"Supplier {i+1}" for i in range(n_suppliers)]
    
    # Generate risk scores (0-10, higher is worse)
    risk = np.random.uniform(1, 9, size=n_suppliers)
    
    # Generate performance scores (0-10, higher is better)
    performance = np.random.uniform(1, 9, size=n_suppliers)
    
    # Generate spend amounts
    spend = np.random.uniform(100000, 5000000, size=n_suppliers)
    
    # Assign tiers based on spend
    spend_sorted = sorted(spend, reverse=True)
    tier_cutoffs = [
        spend_sorted[min(len(spend_sorted)-1, int(n_suppliers * 0.2))],  # Top 20%
        spend_sorted[min(len(spend_sorted)-1, int(n_suppliers * 0.5))]   # Top 50%
    ]
    
    tiers = []
    for s in spend:
        if s >= tier_cutoffs[0]:
            tiers.append("Tier 1")
        elif s >= tier_cutoffs[1]:
            tiers.append("Tier 2")
        else:
            tiers.append("Tier 3")
    
    return pd.DataFrame({
        'Supplier': suppliers,
        'Risk': risk,
        'Performance': performance,
        'Spend': spend,
        'Tier': tiers
    })

def generate_spend_data(category):
    """Generate mock spend data for pie charts"""
    np.random.seed(hash(category) % 100)  # Consistent seed based on category
    
    # Generate between 5-8 suppliers
    n_suppliers = np.random.randint(5, 9)
    suppliers = [f"Supplier {i+1}" for i in range(n_suppliers)]
    
    # Generate spend following a power law distribution
    spend_raw = np.random.power(0.5, size=n_suppliers)
    spend = spend_raw / np.sum(spend_raw) * np.random.randint(5000000, 20000000)
    
    return pd.DataFrame({
        'Supplier': suppliers,
        'Spend': spend
    }).sort_values('Spend', ascending=False)

def generate_risk_data(category):
    """Generate mock risk heatmap data"""
    np.random.seed(hash(category) % 100)  # Consistent seed based on category
    
    # Risk categories
    risk_categories = [
        "Financial", "Geo-political", "Supply Chain", 
        "Regulatory", "Quality", "ESG"
    ]
    
    # Top suppliers
    n_suppliers = 8
    suppliers = [f"Supplier {i+1}" for i in range(n_suppliers)]
    
    # Generate risk matrix (0-10, higher is worse)
    risk_matrix = np.random.uniform(1, 9, size=(n_suppliers, len(risk_categories)))
    
    # Create DataFrame
    df = pd.DataFrame(risk_matrix, columns=risk_categories, index=suppliers)
    
    return df

def generate_price_trend_data(category, material):
    """Generate mock price trend data for forecasting"""
    np.random.seed(hash(f"{category}_{material}") % 100)  # Consistent seed
    
    # Generate dates for the last 24 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Base price (adjusted for aviation materials)
    if category == "Aviation":
        if material in ["Jet Fuel", "Titanium", "Carbon Fiber", "Avionics"]:
            base_price = np.random.uniform(300, 1200)  # Higher base price for aviation materials
        else:
            base_price = np.random.uniform(500, 800)
    else:
        base_price = np.random.uniform(50, 500)
    
    # Generate price with trend, seasonality, and noise
    # Different trend types, aviation tends to have more volatility
    if category == "Aviation":
        trend = np.random.choice([-0.8, 0.1, 1.2])  
        seasonality_factor = np.random.uniform(0.08, 0.25)  # More seasonal effects
        noise_factor = np.random.uniform(0.03, 0.15)  # More volatility
    else:
        trend = np.random.choice([-0.5, 0.2, 0.8])
        seasonality_factor = np.random.uniform(0.05, 0.2)
        noise_factor = np.random.uniform(0.01, 0.1)
    
    prices = []
    for i, date in enumerate(dates):
        # Trend component
        trend_component = trend * i
        
        # Seasonality component (yearly cycle)
        month = date.month
        seasonality = np.sin(2 * np.pi * month / 12) * seasonality_factor * base_price
        
        # Random noise
        noise = np.random.normal(0, noise_factor * base_price)
        
        # Calculate price
        price = base_price + trend_component + seasonality + noise
        prices.append(max(0.1, price))  # Ensure price is positive
    
    return pd.DataFrame({
        'Date': dates,
        'Price': prices
    })

def generate_supplier_details():
    """Generate detailed supplier information"""
    suppliers = []
    
    for i in range(10):
        # Basic info
        supplier = {
            'name': f"Supplier {i+1}",
            'tier': np.random.choice(["Tier 1", "Tier 2", "Tier 3"]),
            'location': np.random.choice([
                "United States", "China", "Germany", "Japan", 
                "South Korea", "France", "United Kingdom", "India"
            ]),
            'spend': np.random.randint(50000, 5000000),
            'categories': np.random.choice([
                "Raw Materials", "Electronics", "Packaging",
                "Services", "Logistics", "MRO"
            ], size=np.random.randint(1, 3)).tolist(),
            
            # Financial metrics
            'revenue': f"${np.random.randint(1, 100)}B",
            'profit_margin': f"{np.random.randint(5, 25)}%",
            'market_share': f"{np.random.randint(1, 30)}%",
            
            # Risk metrics
            'financial_risk': np.random.randint(1, 10),
            'supply_risk': np.random.randint(1, 10),
            'geo_risk': np.random.randint(1, 10),
            'overall_risk': np.random.randint(1, 10),
            
            # ESG metrics
            'esg_score': np.random.randint(30, 95),
            'carbon_footprint': f"{np.random.randint(10000, 1000000)} tons CO2e",
            
            # Performance metrics
            'quality_score': np.random.randint(60, 98),
            'on_time_delivery': f"{np.random.randint(70, 99)}%",
            'defect_rate': f"{np.random.uniform(0.1, 5):.1f}%",
            
            # Relationship metrics
            'years_of_relationship': np.random.randint(1, 20),
            'contracts': np.random.randint(1, 5)
        }
        
        suppliers.append(supplier)
    
    return suppliers

def generate_contract_data():
    """Generate mock contract data"""
    np.random.seed(42)  # Fixed seed for consistent data
    
    # Generate between 15-25 contracts
    n_contracts = np.random.randint(15, 26)
    
    categories = ["Electronics", "Raw Materials", "Packaging", "Office Supplies", 
                 "IT Services", "Logistics", "Chemicals", "Machinery"]
    
    suppliers = [f"Supplier {i+1}" for i in range(15)]
    
    # Contract start dates in the past 2 years
    now = datetime.now()
    start_dates = [now - timedelta(days=np.random.randint(30, 730)) for _ in range(n_contracts)]
    
    # Contract durations between 6 months and 3 years
    durations = [np.random.randint(180, 1095) for _ in range(n_contracts)]
    
    # Calculate end dates
    end_dates = [start + timedelta(days=duration) for start, duration in zip(start_dates, durations)]
    
    # Contract values
    values = [np.random.randint(50000, 5000000) for _ in range(n_contracts)]
    
    # Renewal status
    days_to_expiry = [(end - now).days for end in end_dates]
    status = []
    for days in days_to_expiry:
        if days < 0:
            status.append("Expired")
        elif days < 90:
            status.append("Expiring Soon")
        else:
            status.append("Active")
    
    # Create DataFrame
    return pd.DataFrame({
        'Contract ID': [f"CTR-{np.random.randint(1000, 9999)}" for _ in range(n_contracts)],
        'Supplier': np.random.choice(suppliers, size=n_contracts),
        'Category': np.random.choice(categories, size=n_contracts),
        'Start Date': [d.strftime('%Y-%m-%d') for d in start_dates],
        'End Date': [d.strftime('%Y-%m-%d') for d in end_dates],
        'Value': values,
        'Status': status,
        'Days to Expiry': days_to_expiry
    })
