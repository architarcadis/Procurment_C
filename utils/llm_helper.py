import os
import json
import random
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleLLM:
    """
    A simple simulation of an LLM for procurement insights.
    In a production environment, this would be replaced with an actual LLM integration
    like GPT-4, LLaMA, etc.
    """
    
    def __init__(self):
        """Initialize the simple LLM with procurement domain knowledge"""
        # Load domain-specific knowledge
        self.knowledge_base = {
            "category_strategies": {
                "electronics": ["Consolidate suppliers", "Develop strategic partnerships", "Implement VMI programs"],
                "raw_materials": ["Implement commodity hedging", "Diversify supplier base", "Long-term contracts"],
                "packaging": ["Standardize specifications", "Sustainable sourcing", "Vendor managed inventory"],
                "office_supplies": ["Catalog management", "Demand management", "Tail spend management"],
                "it_services": ["Total cost of ownership analysis", "SLA-based contracting", "Vendor consolidation"],
                "logistics": ["Route optimization", "Carrier rationalization", "Multi-modal shipping"],
                "chemicals": ["Price indexing", "Risk management", "Specification optimization"],
                "machinery": ["TCO analysis", "Maintenance agreements", "Leasing vs. buying analysis"]
            },
            "negotiation_tactics": [
                "Volume commitments", "Multi-year agreements", "Payment term extension",
                "Consignment inventory", "Price indexing", "Rebate programs",
                "Joint cost reduction", "Gain sharing", "Market basket pricing",
                "Dual sourcing", "Competitive bidding", "Specification optimization"
            ],
            "risk_factors": [
                "Supplier financial stability", "Geographic concentration", "Single-sourcing",
                "Commodity price volatility", "Regulatory changes", "Supply chain disruptions",
                "Currency fluctuations", "Political instability", "Natural disasters",
                "Labor disputes", "Quality issues", "Intellectual property risks"
            ],
            "cost_reduction_levers": [
                "Specification optimization", "Demand management", "Make vs. buy analysis",
                "Process optimization", "Value analysis/value engineering", "Supplier consolidation",
                "Global sourcing", "Competitive bidding", "Joint process improvement",
                "Inventory optimization", "Technology enablement", "Standardization"
            ],
            "supplier_evaluation_criteria": [
                "Financial stability", "Quality", "Delivery performance",
                "Technical capability", "Innovation", "Sustainability",
                "Geographic footprint", "Capacity", "Cost competitiveness",
                "Compliance", "Risk profile", "Strategic alignment"
            ]
        }
        
        # Response templates for common procurement questions
        self.response_templates = {
            "opportunity": "Based on my analysis of the {category} category, there are several opportunities to consider:\n\n"
                          "1. {opportunity1}: This could result in approximately {savings1} in savings.\n"
                          "2. {opportunity2}: Implementation would require {effort} effort but yield {savings2} in benefits.\n"
                          "3. {opportunity3}: This strategy aligns with the organization's goal of {goal}.\n\n"
                          "I recommend prioritizing {priority} due to its {reason}.",
            
            "price_analysis": "The price trend for {material} shows {trend_direction} over the past {period}. "
                             "Key factors influencing this trend include:\n\n"
                             "• {factor1}\n"
                             "• {factor2}\n"
                             "• {factor3}\n\n"
                             "Looking ahead, market analysts expect {forecast}. "
                             "I recommend {recommendation} to mitigate price risks.",
            
            "supplier_analysis": "The supplier landscape for {category} is currently {market_state}. "
                                "Top suppliers include {supplier1}, {supplier2}, and {supplier3}.\n\n"
                                "Key considerations when evaluating suppliers in this space:\n"
                                "• {consideration1}\n"
                                "• {consideration2}\n"
                                "• {consideration3}\n\n"
                                "Based on your specific requirements, {supplier_recommendation}.",
                                
            "strategy": "An effective procurement strategy for {category} should address these key elements:\n\n"
                       "1. Sourcing approach: {sourcing_approach}\n"
                       "2. Supplier relationship: {relationship_type}\n"
                       "3. Contract structure: {contract_structure}\n"
                       "4. Risk mitigation: {risk_strategy}\n"
                       "5. Performance metrics: {metrics}\n\n"
                       "This approach aligns with market conditions showing {market_insight} and addresses the business need for {business_need}.",
                       
            "cost_breakdown": "The should-cost model for {item} breaks down as follows:\n\n"
                             "• Raw materials: {raw_material_pct}%\n"
                             "• Labor: {labor_pct}%\n"
                             "• Overhead: {overhead_pct}%\n"
                             "• Transportation: {transportation_pct}%\n"
                             "• Supplier margin: {margin_pct}%\n\n"
                             "Based on this analysis, focus negotiation efforts on {negotiation_focus} as it represents the largest opportunity for cost reduction."
        }
        
        # Common question mapping to response templates
        self.question_mapping = {
            "opportunity": ["opportunity", "saving", "potential", "improve", "optimize"],
            "price_analysis": ["price", "cost", "trend", "market", "forecast"],
            "supplier_analysis": ["supplier", "vendor", "manufacturer", "producer"],
            "strategy": ["strategy", "approach", "plan", "roadmap"],
            "cost_breakdown": ["breakdown", "component", "should-cost", "should cost", "composition"]
        }
        
        # Context memory
        self.context = {
            "last_category": None,
            "last_question": None,
            "last_response": None,
            "session_start": datetime.now()
        }
    
    def generate_response(self, query, category=None):
        """
        Generate a response to a procurement-related query
        
        Args:
            query: The user's question
            category: Optional category context
            
        Returns:
            A string response
        """
        # Simulate processing time
        time.sleep(1)
        
        # Clean and normalize query
        query = query.lower().strip()
        
        # Update context
        if category:
            self.context["last_category"] = category
        self.context["last_question"] = query
        
        # Determine query type
        query_type = self._determine_query_type(query)
        
        # Generate response based on query type
        if query_type == "opportunity":
            response = self._generate_opportunity_response(category or self.context["last_category"])
        elif query_type == "price_analysis":
            material = self._extract_material_from_query(query, category)
            response = self._generate_price_analysis_response(material)
        elif query_type == "supplier_analysis":
            response = self._generate_supplier_analysis_response(category or self.context["last_category"])
        elif query_type == "strategy":
            response = self._generate_strategy_response(category or self.context["last_category"])
        elif query_type == "cost_breakdown":
            item = self._extract_item_from_query(query, category)
            response = self._generate_cost_breakdown_response(item)
        else:
            # General response
            response = self._generate_general_response(query, category)
        
        # Update context
        self.context["last_response"] = response
        
        return response
    
    def _determine_query_type(self, query):
        """Determine the type of query based on keywords"""
        for query_type, keywords in self.question_mapping.items():
            for keyword in keywords:
                if keyword in query:
                    return query_type
        return "general"
    
    def _extract_material_from_query(self, query, category):
        """Extract material name from query or use common materials from category"""
        # List of common materials by category
        category_materials = {
            "electronics": ["semiconductors", "PCBs", "displays", "capacitors", "resistors"],
            "raw_materials": ["steel", "aluminum", "copper", "plastic resin", "rubber"],
            "packaging": ["cardboard", "plastic film", "foam", "pallets", "containers"],
            "chemicals": ["solvents", "polymers", "acids", "bases", "catalysts"],
            "office_supplies": ["paper", "toner", "ink", "stationary"],
            "logistics": ["fuel", "containers", "packaging materials"],
            "it_services": ["hardware", "software", "cloud services"],
            "machinery": ["machine parts", "equipment", "tools", "spare parts"]
        }
        
        # Normalize category
        norm_category = category.lower().replace(" ", "_") if category else None
        
        # List of common materials to check in query
        common_materials = [
            "steel", "aluminum", "copper", "plastic", "rubber", "paper", "resin",
            "semiconductors", "pcb", "display", "capacitor", "resistor",
            "cardboard", "foam", "pallet", "container", "solvent", "polymer",
            "acid", "base", "catalyst", "toner", "ink", "hardware", "software",
            "fuel", "machine part", "equipment", "tool", "spare part"
        ]
        
        # Check if any material is mentioned in query
        for material in common_materials:
            if material in query:
                return material
        
        # If no material found in query, return a random one from the category
        if norm_category in category_materials:
            return random.choice(category_materials[norm_category])
        else:
            return "materials"
    
    def _extract_item_from_query(self, query, category):
        """Extract item name from query or use common items from category"""
        # Similar to _extract_material_from_query but for items/products
        category_items = {
            "electronics": ["laptop", "server", "display", "mobile device", "network equipment"],
            "raw_materials": ["steel coil", "aluminum sheet", "copper wire", "plastic pellet", "rubber compound"],
            "packaging": ["cardboard box", "plastic wrap", "shipping container", "pallet", "foam insert"],
            "chemicals": ["industrial solvent", "polymer compound", "specialty chemical", "cleaning agent", "adhesive"],
            "office_supplies": ["printer paper", "office chair", "desk", "printer", "filing cabinet"],
            "logistics": ["freight service", "warehouse space", "distribution service", "last-mile delivery"],
            "it_services": ["software license", "cloud storage", "IT support", "cybersecurity service"],
            "machinery": ["CNC machine", "forklift", "conveyor system", "assembly equipment", "testing equipment"]
        }
        
        # Normalize category
        norm_category = category.lower().replace(" ", "_") if category else None
        
        # Common items to check in query
        common_items = [
            "laptop", "server", "display", "mobile", "network", "coil", "sheet", "wire", 
            "pellet", "compound", "box", "wrap", "container", "pallet", "insert", "solvent", 
            "polymer", "chemical", "cleaner", "adhesive", "paper", "chair", "desk", "printer", 
            "cabinet", "freight", "warehouse", "distribution", "delivery", "license", "storage", 
            "support", "security", "machine", "forklift", "conveyor", "equipment"
        ]
        
        # Check if any item is mentioned in query
        for item in common_items:
            if item in query:
                return item
        
        # If no item found in query, return a random one from the category
        if norm_category in category_items:
            return random.choice(category_items[norm_category])
        else:
            return "product"
    
    def _generate_opportunity_response(self, category):
        """Generate response about opportunities in the given category"""
        if not category:
            category = random.choice(list(self.knowledge_base["category_strategies"].keys()))
        
        norm_category = category.lower().replace(" ", "_")
        
        # Get strategies for this category or use general ones
        strategies = self.knowledge_base["category_strategies"].get(
            norm_category, 
            random.sample(list(self.knowledge_base["cost_reduction_levers"]), 3)
        )
        
        # Pick random strategies
        selected_strategies = random.sample(strategies, min(3, len(strategies)))
        
        # Generate random savings
        savings1 = f"${random.randint(100, 500)}K"
        savings2 = f"${random.randint(200, 800)}K"
        
        # Pick a goal
        goals = ["cost reduction", "risk mitigation", "sustainability", "innovation", "quality improvement"]
        
        # Fill in the template
        response = self.response_templates["opportunity"].format(
            category=category,
            opportunity1=selected_strategies[0],
            savings1=savings1,
            opportunity2=selected_strategies[1],
            effort=random.choice(["low", "medium", "high"]),
            savings2=savings2,
            opportunity3=selected_strategies[2] if len(selected_strategies) > 2 else "Strategic relationship development",
            goal=random.choice(goals),
            priority=selected_strategies[0],
            reason=random.choice(["high ROI", "low implementation complexity", "strategic importance", "quick win potential"])
        )
        
        return response
    
    def _generate_price_analysis_response(self, material):
        """Generate response about price analysis for the given material"""
        # Market factors
        factors = [
            "supply constraints due to production capacity limitations",
            "increased demand from emerging markets",
            "new regulatory requirements affecting production costs",
            "energy price fluctuations impacting manufacturing costs",
            "trade policy changes affecting import/export dynamics",
            "technological advancements reducing production costs",
            "labor cost increases in key manufacturing regions",
            "transportation and logistics challenges",
            "raw material availability issues",
            "industry consolidation changing market dynamics",
            "currency exchange rate fluctuations",
            "environmental compliance cost increases"
        ]
        
        # Trend directions
        trends = ["an upward trend", "a downward trend", "volatility", "relative stability", "a slight increase", "a gradual decrease"]
        
        # Forecast statements
        forecasts = [
            "continued price increases for the next 6-12 months",
            "prices to stabilize after recent volatility",
            "a gradual decrease as new capacity comes online",
            "ongoing volatility due to market uncertainties",
            "moderate increases tracking inflation rates",
            "divergent regional pricing trends"
        ]
        
        # Recommendations
        recommendations = [
            "locking in prices with longer-term contracts",
            "implementing price indexing in contracts",
            "developing alternative suppliers or materials",
            "increasing inventory of critical materials",
            "hedging through financial instruments",
            "staggered purchasing to average price volatility",
            "joint cost reduction initiatives with suppliers"
        ]
        
        # Fill in the template
        response = self.response_templates["price_analysis"].format(
            material=material,
            trend_direction=random.choice(trends),
            period=random.choice(["quarter", "six months", "year", "two years"]),
            factor1=random.choice(factors),
            factor2=random.choice([f for f in factors if f not in response]),
            factor3=random.choice([f for f in factors if f not in response]),
            forecast=random.choice(forecasts),
            recommendation=random.choice(recommendations)
        )
        
        return response
    
    def _generate_supplier_analysis_response(self, category):
        """Generate response about supplier analysis for the given category"""
        if not category:
            category = random.choice(list(self.knowledge_base["category_strategies"].keys()))
        
        # Market states
        market_states = [
            "highly consolidated with few major players",
            "fragmented with many regional suppliers",
            "transitioning due to industry disruption",
            "stable with established competitive dynamics",
            "experiencing rapid innovation and new entrants",
            "dominated by global suppliers with regional specialists"
        ]
        
        # Generate supplier names
        supplier_prefixes = ["Global", "Advanced", "Premium", "Strategic", "Innovative", "Reliable", "Precision", "United", "Superior", "Integrated"]
        supplier_suffixes = ["Solutions", "Industries", "Materials", "Supply Co", "Manufacturers", "Technologies", "Products", "International", "Enterprises", "Corp"]
        
        suppliers = []
        for _ in range(3):
            supplier_name = f"{random.choice(supplier_prefixes)} {random.choice(supplier_suffixes)}"
            while supplier_name in suppliers:
                supplier_name = f"{random.choice(supplier_prefixes)} {random.choice(supplier_suffixes)}"
            suppliers.append(supplier_name)
        
        # Supplier evaluation criteria from knowledge base
        criteria = random.sample(self.knowledge_base["supplier_evaluation_criteria"], 3)
        
        # Recommendations
        recommendations = [
            "I recommend evaluating Tier 1 suppliers based on total cost of ownership rather than unit price alone",
            "consider developing strategic partnerships with suppliers that offer innovation capabilities",
            "a dual-sourcing strategy would be prudent given the current market volatility",
            "focusing on suppliers with strong sustainability credentials would align with corporate objectives",
            "regional suppliers may offer advantages in flexibility and lead time despite higher unit costs",
            "suppliers with vertical integration demonstrate more stable pricing and availability"
        ]
        
        # Fill in the template
        response = self.response_templates["supplier_analysis"].format(
            category=category,
            market_state=random.choice(market_states),
            supplier1=suppliers[0],
            supplier2=suppliers[1],
            supplier3=suppliers[2],
            consideration1=criteria[0],
            consideration2=criteria[1],
            consideration3=criteria[2],
            supplier_recommendation=random.choice(recommendations)
        )
        
        return response
    
    def _generate_strategy_response(self, category):
        """Generate response about procurement strategy for the given category"""
        if not category:
            category = random.choice(list(self.knowledge_base["category_strategies"].keys()))
        
        # Sourcing approaches
        sourcing_approaches = [
            "competitive bidding with 3-5 pre-qualified suppliers",
            "strategic sole-sourcing with performance incentives",
            "regional multi-sourcing to ensure supply continuity",
            "category-based sourcing to leverage cross-category spending",
            "tiered sourcing strategy with primary and backup suppliers"
        ]
        
        # Relationship types
        relationship_types = [
            "arm's length for commodity items, strategic partnerships for critical components",
            "collaborative partnerships focused on innovation and continuous improvement",
            "performance-based relationships with regular business reviews",
            "integrated development partnerships for custom/specialty items",
            "vendor managed inventory program with key suppliers"
        ]
        
        # Contract structures
        contract_structures = [
            "2-year fixed pricing with volume-based rebates",
            "1-year with indexed pricing tied to key raw materials",
            "evergreen contract with annual price reviews and performance incentives",
            "3-year agreement with tiered pricing based on volume commitments",
            "framework agreement with mini-competitions for specific requirements"
        ]
        
        # Risk strategies
        risk_strategies = [
            "geographic diversification of supplier base",
            "inventory buffering for critical items with long lead times",
            "dual sourcing for high-value/high-risk components",
            "regular supplier financial monitoring and contingency planning",
            "contractual protections including performance bonds and risk-sharing provisions"
        ]
        
        # Performance metrics
        performance_metrics = [
            "comprehensive scorecard including quality, delivery, cost, and innovation metrics",
            "total cost of ownership measurement and tracking",
            "supplier-led continuous improvement targets with shared benefits",
            "end-to-end supply chain visibility and performance tracking",
            "sustainability and social responsibility metrics aligned with corporate goals"
        ]
        
        # Market insights
        market_insights = [
            "increasing supplier consolidation",
            "technology disruption affecting traditional supply chains",
            "volatility in input costs",
            "shifting global trade dynamics",
            "increasing focus on sustainable and ethical sourcing",
            "digitalization of procurement processes and supplier interfaces"
        ]
        
        # Business needs
        business_needs = [
            "cost reduction in a competitive market environment",
            "supply assurance for business-critical materials",
            "flexibility to respond to changing market demands",
            "innovation to maintain competitive advantage",
            "risk mitigation in an uncertain global environment",
            "regulatory compliance and corporate social responsibility goals"
        ]
        
        # Fill in the template
        response = self.response_templates["strategy"].format(
            category=category,
            sourcing_approach=random.choice(sourcing_approaches),
            relationship_type=random.choice(relationship_types),
            contract_structure=random.choice(contract_structures),
            risk_strategy=random.choice(risk_strategies),
            metrics=random.choice(performance_metrics),
            market_insight=random.choice(market_insights),
            business_need=random.choice(business_needs)
        )
        
        return response
    
    def _generate_cost_breakdown_response(self, item):
        """Generate response about cost breakdown for the given item"""
        # Generate random percentages that sum to 100%
        raw_material_pct = random.randint(25, 55)
        labor_pct = random.randint(10, 30)
        overhead_pct = random.randint(10, 25)
        transportation_pct = random.randint(5, 15)
        
        # Calculate margin to make sum 100%
        margin_pct = 100 - (raw_material_pct + labor_pct + overhead_pct + transportation_pct)
        
        # Negotiation focus options
        negotiation_focuses = [
            "raw material costs",
            "labor efficiency improvements",
            "overhead reduction",
            "logistics optimization",
            "margin compression",
            "design optimization to reduce material usage",
            "alternative materials or specifications"
        ]
        
        # Determine most logical negotiation focus based on highest percentage
        percentages = {
            "raw material costs": raw_material_pct,
            "labor efficiency improvements": labor_pct,
            "overhead reduction": overhead_pct,
            "logistics optimization": transportation_pct,
            "margin compression": margin_pct
        }
        
        # Find the component with highest percentage
        highest_component = max(percentages.items(), key=lambda x: x[1])[0]
        
        # Fill in the template
        response = self.response_templates["cost_breakdown"].format(
            item=item,
            raw_material_pct=raw_material_pct,
            labor_pct=labor_pct,
            overhead_pct=overhead_pct,
            transportation_pct=transportation_pct,
            margin_pct=margin_pct,
            negotiation_focus=highest_component
        )
        
        return response
    
    def _generate_general_response(self, query, category):
        """Generate a general response when the query doesn't fit specific templates"""
        # List of general responses
        general_responses = [
            "Based on my analysis of the {category} category, I recommend focusing on supplier consolidation, specification standardization, and demand management to optimize value.",
            
            "The {category} market is currently experiencing {market_condition}. This presents an opportunity to {strategy} which could yield significant benefits in terms of {benefit}.",
            
            "When looking at {category} procurement, it's important to consider both price and total cost of ownership. Have you evaluated the impact of {factor} on your overall costs?",
            
            "For {category}, I would suggest implementing a {timeframe} strategy that balances cost, risk, and innovation. This should include {element} as a key component.",
            
            "The most successful organizations approach {category} with a focus on {focus_area}. Would you like me to provide more specific recommendations for your situation?",
            
            "I've analyzed similar {category} challenges for other organizations. The most effective approach typically involves {approach}, especially when dealing with {circumstance}."
        ]
        
        # Market conditions
        market_conditions = [
            "significant price volatility",
            "supplier consolidation",
            "technological disruption",
            "increasing sustainability requirements",
            "shifting global supply chains",
            "capacity constraints"
        ]
        
        # Strategies
        strategies = [
            "implement value-based sourcing",
            "develop strategic supplier relationships",
            "pursue specification optimization",
            "establish a category council",
            "integrate sustainability criteria into supplier selection",
            "implement digital procurement tools"
        ]
        
        # Benefits
        benefits = [
            "cost reduction and avoidance",
            "supply chain resilience",
            "improved supplier performance",
            "innovation and continuous improvement",
            "alignment with corporate sustainability goals",
            "reduced total cost of ownership"
        ]
        
        # Factors
        factors = [
            "quality-related costs",
            "supply continuity risks",
            "lifecycle maintenance requirements",
            "end-of-life disposal costs",
            "regulatory compliance",
            "inventory carrying costs"
        ]
        
        # Timeframes
        timeframes = [
            "3-year phased",
            "agile, iterative",
            "dual-track",
            "balanced short and long-term",
            "milestone-based",
            "continuous improvement"
        ]
        
        # Elements
        elements = [
            "supplier relationship management",
            "performance-based contracting",
            "total cost modeling",
            "risk mitigation planning",
            "innovation incentives",
            "digital transformation"
        ]
        
        # Focus areas
        focus_areas = [
            "value creation beyond savings",
            "supply chain transparency",
            "cross-functional collaboration",
            "supplier-enabled innovation",
            "data-driven decision making",
            "sustainable procurement practices"
        ]
        
        # Approaches
        approaches = [
            "a category-based center of excellence",
            "strategic supplier segmentation",
            "cross-functional sourcing teams",
            "integrated business planning",
            "procurement digitalization",
            "supplier development programs"
        ]
        
        # Circumstances
        circumstances = [
            "market uncertainty",
            "complex specifications",
            "global sourcing challenges",
            "stakeholder alignment issues",
            "rapid growth scenarios",
            "technology transitions"
        ]
        
        # Select a random response template
        template = random.choice(general_responses)
        
        # If category is not provided, use a default
        if not category:
            category = random.choice(list(self.knowledge_base["category_strategies"].keys()))
        
        # Fill in the template based on its variables
        if "{market_condition}" in template:
            response = template.format(
                category=category,
                market_condition=random.choice(market_conditions),
                strategy=random.choice(strategies),
                benefit=random.choice(benefits)
            )
        elif "{factor}" in template:
            response = template.format(
                category=category,
                factor=random.choice(factors)
            )
        elif "{timeframe}" in template:
            response = template.format(
                category=category,
                timeframe=random.choice(timeframes),
                element=random.choice(elements)
            )
        elif "{focus_area}" in template:
            response = template.format(
                category=category,
                focus_area=random.choice(focus_areas)
            )
        elif "{approach}" in template:
            response = template.format(
                category=category,
                approach=random.choice(approaches),
                circumstance=random.choice(circumstances)
            )
        else:
            response = template.format(category=category)
        
        return response
