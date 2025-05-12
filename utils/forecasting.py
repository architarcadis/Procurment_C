import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta

def simple_forecast(historical_data, periods=6):
    """
    Simple forecasting using linear regression
    
    Args:
        historical_data: DataFrame with 'Date' and 'Price' columns
        periods: Number of periods to forecast
    
    Returns:
        DataFrame with forecasted values
    """
    # Prepare data
    df = historical_data.copy()
    
    # Convert dates to numeric feature (days since first date)
    first_date = df['Date'].min()
    df['days_feature'] = (df['Date'] - first_date).dt.days
    
    # Train linear regression model
    model = LinearRegression()
    X = df[['days_feature']]
    y = df['Price']
    model.fit(X, y)
    
    # Generate future dates for prediction
    last_date = df['Date'].max()
    future_dates = pd.date_range(
        start=last_date + timedelta(days=30), 
        periods=periods, 
        freq='M'
    )
    
    # Prepare prediction data
    future_df = pd.DataFrame({
        'Date': future_dates,
        'days_feature': [(d - first_date).days for d in future_dates]
    })
    
    # Make predictions
    future_df['Price'] = model.predict(future_df[['days_feature']])
    future_df['Type'] = 'Forecast'
    
    # Mark historical data
    df['Type'] = 'Historical'
    
    # Combine historical and forecasted data
    result = pd.concat([df[['Date', 'Price', 'Type']], future_df[['Date', 'Price', 'Type']]])
    
    return result

def advanced_forecast(historical_data, periods=6):
    """
    More advanced forecasting using RandomForest with additional features
    
    Args:
        historical_data: DataFrame with 'Date' and 'Price' columns
        periods: Number of periods to forecast
    
    Returns:
        DataFrame with forecasted values
    """
    # Prepare data
    df = historical_data.copy()
    
    # Extract date features
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['day_of_year'] = df['Date'].dt.dayofyear
    df['days_feature'] = (df['Date'] - df['Date'].min()).dt.days
    
    # Add lag features (price from previous periods)
    df['price_lag1'] = df['Price'].shift(1)
    df['price_lag2'] = df['Price'].shift(2)
    df['price_lag3'] = df['Price'].shift(3)
    
    # Add rolling means
    df['rolling_mean_3'] = df['Price'].rolling(window=3).mean()
    df['rolling_mean_6'] = df['Price'].rolling(window=6).mean()
    
    # Drop rows with NaN values (first few rows with lag features)
    df = df.dropna()
    
    # Select features for training
    features = ['days_feature', 'month', 'day_of_year', 
                'price_lag1', 'price_lag2', 'price_lag3',
                'rolling_mean_3', 'rolling_mean_6']
    
    # Train random forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    X = df[features]
    y = df['Price']
    model.fit(X, y)
    
    # Prepare future data for prediction
    last_date = df['Date'].max()
    future_dates = pd.date_range(
        start=last_date + timedelta(days=30), 
        periods=periods, 
        freq='M'
    )
    
    future_df = pd.DataFrame({'Date': future_dates})
    future_df['year'] = future_df['Date'].dt.year
    future_df['month'] = future_df['Date'].dt.month
    future_df['day_of_year'] = future_df['Date'].dt.dayofyear
    future_df['days_feature'] = (future_df['Date'] - df['Date'].min()).dt.days
    
    # For each period in the future, predict and update lag features
    all_data = df.copy()
    
    for i in range(len(future_df)):
        # Get the current row to predict
        current_row = future_df.iloc[[i]].copy()
        
        # Get the most recent actual or predicted values for lag features
        current_row['price_lag1'] = all_data['Price'].iloc[-1]
        current_row['price_lag2'] = all_data['Price'].iloc[-2]
        current_row['price_lag3'] = all_data['Price'].iloc[-3]
        
        # Get rolling means
        current_row['rolling_mean_3'] = all_data['Price'].iloc[-3:].mean()
        current_row['rolling_mean_6'] = all_data['Price'].iloc[-6:].mean()
        
        # Make prediction
        prediction = model.predict(current_row[features])[0]
        current_row['Price'] = prediction
        
        # Add to all data for next prediction
        all_data = pd.concat([all_data, current_row])
    
    # Combine with historical data
    future_df = all_data.iloc[-periods:][['Date', 'Price']]
    future_df['Type'] = 'Forecast'
    
    # Mark historical data
    historical_df = historical_data.copy()
    historical_df['Type'] = 'Historical'
    
    # Combine historical and forecasted data
    result = pd.concat([historical_df[['Date', 'Price', 'Type']], future_df[['Date', 'Price', 'Type']]])
    
    return result

def should_cost_model(material_name, components):
    """
    Generate a simple should-cost model based on components
    
    Args:
        material_name: Name of the material
        components: Dictionary of components and their weights
    
    Returns:
        Dictionary with cost breakdown
    """
    # Base costs for some common components ($/kg)
    base_costs = {
        'labor': np.random.uniform(20, 50),
        'overhead': np.random.uniform(10, 30),
        'raw_material': np.random.uniform(5, 30),
        'packaging': np.random.uniform(1, 10),
        'logistics': np.random.uniform(2, 15),
        'energy': np.random.uniform(2, 10),
        'additives': np.random.uniform(8, 25),
    }
    
    # Cost breakdown
    cost_breakdown = {}
    total_cost = 0
    
    for component, weight in components.items():
        if component in base_costs:
            cost = base_costs[component] * weight
        else:
            cost = np.random.uniform(5, 30) * weight
        
        cost_breakdown[component] = cost
        total_cost += cost
    
    # Add markup
    markup_pct = np.random.uniform(0.1, 0.3)
    markup = total_cost * markup_pct
    cost_breakdown['markup'] = markup
    total_cost += markup
    
    return {
        'material': material_name,
        'breakdown': cost_breakdown,
        'total_cost': total_cost,
        'unit': 'per kg'
    }
