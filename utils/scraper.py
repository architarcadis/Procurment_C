import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
import logging
import trafilatura

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simulated_web_scrape(category):
    """
    Simulates web scraping for category intelligence.
    In a real implementation, this would use actual web scraping libraries
    to gather data from relevant sources.
    
    Args:
        category: The procurement category to scrape information for
    
    Returns:
        A list of news/intelligence items related to the category
    """
    # Simulate a delay as if we're actually scraping
    time.sleep(0.5)
    
    # Create simulated news/intelligence items
    news_sources = [
        "Industry Journal", "Market Watch", "Supply Chain Weekly", 
        "Regulatory Affairs", "Commodity Insights", "Trade Publications",
        "Company Press Release", "Financial Times", "Reuters"
    ]
    
    # Category-specific keywords
    category_keywords = {
        "Electronics": ["semiconductor", "chip shortage", "PCB", "electronic components", 
                        "display panel", "circuit board", "capacitor", "microchip"],
        
        "Raw Materials": ["steel", "aluminum", "copper", "plastic resin", "rubber", 
                          "paper pulp", "metal", "commodity", "ore", "mining"],
        
        "Packaging": ["cardboard", "plastic", "foam", "container", "box", "wrap", 
                      "packaging material", "recyclable", "sustainable packaging"],
        
        "Office Supplies": ["paper", "printer", "toner", "stationery", "office furniture", 
                           "desk", "chair", "office equipment"],
        
        "IT Services": ["cloud", "software", "hardware", "license", "IT infrastructure", 
                       "data center", "cybersecurity", "digital transformation"],
        
        "Logistics": ["freight", "shipping", "transportation", "carrier", "port congestion", 
                     "container", "delivery", "supply chain", "warehousing"],
        
        "Chemicals": ["petrochemical", "solvent", "acid", "base", "catalyst", "chemical feedstock", 
                     "polymer", "specialty chemical", "industrial chemical"],
        
        "Machinery": ["equipment", "machine parts", "industrial machinery", "manufacturing equipment", 
                     "assembly line", "robotics", "automation", "mechanical components"]
    }
    
    # If category not in our keywords, use a generic set
    if category not in category_keywords:
        keywords = ["supply", "demand", "price", "shortage", "surplus", "market", "manufacturing"]
    else:
        keywords = category_keywords[category]
    
    # News types with templates
    news_templates = [
        "{keyword} prices {direction} by {percent}% due to {reason}",
        "New {keyword} supplier enters market, promises {percent}% {improvement}",
        "Global shortage of {keyword} expected to {impact} supply chains",
        "Regulatory changes affecting {keyword} sourcing in {region}",
        "{company} announces {event} for {keyword} production",
        "Industry analyst predicts {direction} trend in {keyword} market",
        "Supply chain disruption for {keyword} due to {reason}",
        "New technology breakthrough in {keyword} manufacturing",
        "Trade tensions impact {keyword} availability from {region}",
        "{region} government announces new policy affecting {keyword} imports"
    ]
    
    # Generate random news items
    num_items = random.randint(6, 12)
    news_items = []
    
    for _ in range(num_items):
        # Pick random elements
        template = random.choice(news_templates)
        keyword = random.choice(keywords)
        source = random.choice(news_sources)
        days_ago = random.randint(1, 30)
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        impact = random.choice(["High", "Medium", "Low"])
        impact_score = random.randint(1, 10)
        direction = random.choice(["increase", "decrease", "surge", "drop", "rise", "fall"])
        percent = random.randint(5, 30)
        reason = random.choice([
            "increased demand", "supply constraints", "weather events", 
            "geopolitical tensions", "labor shortages", "transportation issues",
            "energy costs", "raw material shortages", "manufacturing delays",
            "trade restrictions", "regulatory changes"
        ])
        region = random.choice([
            "North America", "Europe", "Asia", "China", "Southeast Asia", 
            "Latin America", "Middle East", "Africa", "Global"
        ])
        company = random.choice([
            "Industry Leader Corp", "Global Supplies Inc", "PrimeMaterials Ltd", 
            "TechSupply Co", "Manufacturing Giants", "ChemWorks International",
            "LogiTech Solutions", "RawSource Partners", "PackWorks Industries"
        ])
        event = random.choice([
            "expansion", "contraction", "new facility", "plant closure", 
            "innovation", "merger", "acquisition", "strategic partnership",
            "price increase", "production cut", "capacity increase"
        ])
        improvement = random.choice([
            "cost reduction", "quality improvement", "lead time reduction", 
            "capacity increase", "efficiency gain", "sustainability improvement"
        ])
        impact = random.choice([
            "significantly impact", "disrupt", "delay", "improve", 
            "temporarily affect", "constrain", "enhance"
        ])
        
        # Format the template
        title = template.format(
            keyword=keyword,
            direction=direction,
            percent=percent,
            reason=reason,
            region=region,
            company=company,
            event=event,
            improvement=improvement,
            impact=impact
        )
        
        # Create news item
        news_item = {
            "title": title,
            "source": source,
            "date": date,
            "days_ago": days_ago,
            "impact": impact,
            "impact_score": impact_score,
            "category": category,
            "url": f"https://example.com/news/{category.lower().replace(' ', '-')}/{days_ago}"
        }
        
        news_items.append(news_item)
    
    # Sort by date (most recent first)
    news_items.sort(key=lambda x: x["days_ago"])
    
    return news_items

def get_commodity_prices(commodity):
    """
    Simulates getting commodity price data.
    In a real implementation, this would use API calls or web scraping
    to get actual commodity price data.
    
    Args:
        commodity: The commodity to get price data for
    
    Returns:
        DataFrame with historical price data
    """
    # Simulate API call delay
    time.sleep(0.3)
    
    # Generate some random but realistic price data
    np.random.seed(hash(commodity) % 1000)  # Use commodity name as seed
    
    # Generate dates for the last 2 years (monthly data)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Base price and volatility based on commodity type
    commodity_base_prices = {
        "Steel": {"base": 700, "volatility": 0.05},
        "Aluminum": {"base": 2000, "volatility": 0.07},
        "Copper": {"base": 6500, "volatility": 0.08},
        "Zinc": {"base": 2500, "volatility": 0.06},
        "Nickel": {"base": 14000, "volatility": 0.09},
        "Gold": {"base": 1800, "volatility": 0.04},
        "Silver": {"base": 25, "volatility": 0.07},
        "Crude Oil": {"base": 60, "volatility": 0.1},
        "Natural Gas": {"base": 3.5, "volatility": 0.15},
        "Cotton": {"base": 80, "volatility": 0.08},
        "Wheat": {"base": 650, "volatility": 0.12},
        "Corn": {"base": 550, "volatility": 0.1},
        "Soybeans": {"base": 1400, "volatility": 0.09},
        "Coffee": {"base": 120, "volatility": 0.14},
        "Sugar": {"base": 16, "volatility": 0.11},
        "Ethanol": {"base": 1.6, "volatility": 0.08},
        "PET Resin": {"base": 1000, "volatility": 0.06},
        "Polypropylene": {"base": 1200, "volatility": 0.05},
        "HDPE": {"base": 1100, "volatility": 0.06},
        "Paper Pulp": {"base": 850, "volatility": 0.04}
    }
    
    # If commodity not in our list, use a generic model
    if commodity not in commodity_base_prices:
        base_price = 1000
        volatility = 0.08
    else:
        base_price = commodity_base_prices[commodity]["base"]
        volatility = commodity_base_prices[commodity]["volatility"]
    
    # Generate price with trend, seasonality, and random walk
    prices = []
    
    # Random trend direction
    trend = np.random.choice([-1, 1]) * np.random.uniform(0.001, 0.004)
    
    # Random seasonality amplitude
    seasonality_amplitude = np.random.uniform(0.02, 0.1)
    
    current_price = base_price
    for i, date in enumerate(dates):
        # Trend component
        trend_component = base_price * trend * i
        
        # Seasonality component (yearly cycle)
        month = date.month
        seasonality = np.sin(2 * np.pi * month / 12) * seasonality_amplitude * base_price
        
        # Random walk component (month-to-month volatility)
        if i == 0:
            random_walk = 0
        else:
            random_walk = prices[-1] - (base_price + trend_component + seasonality)
            # Mean reversion
            random_walk = random_walk * 0.85
            
        # Add new random shock
        shock = np.random.normal(0, volatility * base_price)
        
        # Calculate price
        price = base_price + trend_component + seasonality + random_walk + shock
        prices.append(max(0.1 * base_price, price))  # Ensure price doesn't go too low
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Price': prices,
        'Currency': 'USD',
        'Unit': get_commodity_unit(commodity)
    })
    
    return df

def get_commodity_unit(commodity):
    """Helper function to get the appropriate unit for a commodity"""
    commodity_units = {
        "Steel": "per ton",
        "Aluminum": "per ton",
        "Copper": "per ton",
        "Zinc": "per ton",
        "Nickel": "per ton",
        "Gold": "per oz",
        "Silver": "per oz",
        "Crude Oil": "per barrel",
        "Natural Gas": "per MMBtu",
        "Cotton": "per lb",
        "Wheat": "per bushel",
        "Corn": "per bushel",
        "Soybeans": "per bushel",
        "Coffee": "per lb",
        "Sugar": "per lb",
        "Ethanol": "per gallon",
        "PET Resin": "per ton",
        "Polypropylene": "per ton",
        "HDPE": "per ton",
        "Paper Pulp": "per ton",
        "Jet Fuel": "per gallon",
        "Titanium": "per kg",
        "Carbon Fiber": "per kg",
        "Avionics": "per unit"
    }
    
    return commodity_units.get(commodity, "per unit")
    
def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    
    Some common website to crawl information from:
    MLB scores: https://www.mlb.com/scores/YYYY-MM-DD
    """
    try:
        # Send a request to the website
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text if text else "No content could be extracted from the URL."
    except Exception as e:
        return f"Error scraping content: {str(e)}"
        
def scrape_with_details(url: str, category: str = None):
    """
    Enhanced scraping function that returns detailed information about the scraping process
    and the structured data. This helps users understand what data is being captured and 
    how it's organized.
    
    Args:
        url: The URL to scrape
        category: Optional category to classify the content
        
    Returns:
        Dictionary containing raw data, structured data, metadata, and scraping stats
    """
    import time
    from datetime import datetime
    import hashlib
    
    start_time = time.time()
    
    try:
        # Step 1: Record metadata about the request
        metadata = {
            "url": url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category if category else "Uncategorized",
            "request_id": hashlib.md5(f"{url}{time.time()}".encode()).hexdigest()[:8]
        }
        
        # Step 2: Fetch raw content
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return {
                "success": False,
                "error": "Failed to download content",
                "metadata": metadata,
                "scraping_stats": {"duration_seconds": time.time() - start_time}
            }
            
        # Step 3: Extract text content using trafilatura
        content = trafilatura.extract(downloaded)
        
        # Step 4: Split into useful segments
        paragraphs = [p for p in content.split('\n') if p.strip()] if content else []
        
        # Step 5: Create structured dataset with metadata
        structured_data = {
            "title": paragraphs[0] if paragraphs else "No title extracted",
            "paragraphs": paragraphs,
            "word_count": len(content.split()) if content else 0,
            "paragraph_count": len(paragraphs),
            "source_url": url,
            "category": category if category else "Uncategorized",
            "date_scraped": metadata["timestamp"]
        }
        
        # Step 6: Attempt to extract dates or time references 
        import re
        date_pattern = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+\d{4}\b'
        dates_found = re.findall(date_pattern, content) if content else []
        structured_data["dates_mentioned"] = dates_found
        
        # Step 7: Attempt to extract price or financial information
        price_pattern = r'[\$£€¥]\s*\d+(?:,\d+)*(?:\.\d+)?|\d+(?:,\d+)*(?:\.\d+)?\s*(?:pounds|dollars|euros|GBP|USD|EUR)'
        prices_found = re.findall(price_pattern, content) if content else []
        structured_data["financial_references"] = prices_found
        
        # Step 8: Calculate statistics on the scraping operation
        scraping_stats = {
            "duration_seconds": time.time() - start_time,
            "content_size_bytes": len(downloaded) if downloaded else 0,
            "extracted_text_size_bytes": len(content) if content else 0,
            "extraction_ratio": len(content) / len(downloaded) if downloaded and content else 0
        }
        
        # Step 9: Compile results
        result = {
            "success": True,
            "raw_html": downloaded[:5000] + "..." if len(downloaded) > 5000 else downloaded,  # Truncate large HTML
            "raw_text": content,
            "structured_data": structured_data,
            "metadata": metadata,
            "scraping_stats": scraping_stats
        }
        
        logger.info(f"Successfully scraped {url} in {scraping_stats['duration_seconds']:.2f}s")
        return result
        
    except Exception as e:
        end_time = time.time()
        logger.error(f"Error scraping {url}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "metadata": metadata if 'metadata' in locals() else {"url": url},
            "scraping_stats": {"duration_seconds": end_time - start_time}
        }
        
def scrape_aviation_news(source_type="industry"):
    """
    Scrapes aviation industry news relevant to procurement from predefined sources
    
    Args:
        source_type: Type of source to scrape ("industry", "supplier", "regulatory")
        
    Returns:
        List of structured news items
    """
    sources = {
        "industry": [
            "https://www.airport-technology.com/news/",
            "https://simpleflying.com/category/aviation-news/",
            "https://www.flightglobal.com/news/",
        ],
        "supplier": [
            "https://www.airport-suppliers.com/press-releases/",
            "https://www.aviationpros.com/airports/",
        ],
        "regulatory": [
            "https://www.caa.co.uk/news/",
            "https://www.iata.org/en/pressroom/",
        ],
        "heathrow": [
            "https://mediacentre.heathrow.com/pressreleases/all",
        ]
    }
    
    # Select sources based on type
    urls_to_scrape = sources.get(source_type, sources["industry"])
    
    # Limit to 2 sources to avoid overwhelming the system
    urls_to_scrape = urls_to_scrape[:2]
    
    # Process each source
    results = []
    for url in urls_to_scrape:
        try:
            logger.info(f"Scraping aviation news from: {url}")
            scraped_data = scrape_with_details(url, category="Aviation News")
            
            if scraped_data["success"]:
                # Process the scraped content into structured news items
                if "structured_data" in scraped_data:
                    data = scraped_data["structured_data"]
                    
                    # Create a news item from the scraped data
                    news_item = {
                        "title": data.get("title", "Untitled"),
                        "source": url,
                        "date_scraped": data.get("date_scraped"),
                        "content_summary": " ".join(data["paragraphs"][:3]) if data.get("paragraphs") else "",
                        "financial_references": data.get("financial_references", []),
                        "dates_mentioned": data.get("dates_mentioned", []),
                        "word_count": data.get("word_count", 0),
                        "category": "Aviation News",
                        "raw_data_sample": scraped_data["raw_text"][:500] + "..." if len(scraped_data.get("raw_text", "")) > 500 else scraped_data.get("raw_text", "")
                    }
                    
                    results.append(news_item)
                    
                    logger.info(f"Successfully processed news from {url}")
                else:
                    logger.warning(f"No structured data found in scraped content from {url}")
            else:
                logger.warning(f"Failed to scrape {url}: {scraped_data.get('error', 'Unknown error')}")
        
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
    
    return results
