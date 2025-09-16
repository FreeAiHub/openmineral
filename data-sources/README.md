# 🗄️ Data Sources for ML Model Training

## Новые базы данных и источники данных для обучения моделей прогнозирования

*"Data is the new oil. Let's build the refinery for commodity intelligence."*

---

## 📊 Commodity-Specific Datasets

### **1. Metals & Minerals Database**

#### **Core Metals Dataset**
```json
{
  "dataset_name": "commodity_metals_v1",
  "description": "Comprehensive dataset for major industrial metals",
  "metals": [
    {
      "name": "Copper",
      "symbol": "CU",
      "description": "Essential for electrical conductivity and construction",
      "applications": [
        "Power generation and transmission",
        "Electric vehicles (4x more than gas cars)",
        "Wind turbines (5 tonnes per MW)",
        "Construction and infrastructure"
      ],
      "demand_drivers": [
        "EV adoption (10x growth by 2030)",
        "Renewable energy expansion",
        "Infrastructure development",
        "Digital transformation"
      ],
      "supply_characteristics": {
        "major_producers": ["Chile", "Peru", "China", "Congo"],
        "production_volume": "21M tonnes annually",
        "recycling_rate": "35%",
        "geopolitical_risks": ["Chile labor disputes", "Peru environmental regulations"]
      }
    },
    {
      "name": "Lithium",
      "symbol": "LI",
      "description": "Critical for battery technology and energy storage",
      "applications": [
        "Electric vehicle batteries",
        "Smartphone and laptop batteries",
        "Grid energy storage",
        "Portable electronics"
      ],
      "demand_drivers": [
        "EV market growth (40M vehicles by 2030)",
        "Renewable energy storage needs",
        "Consumer electronics demand",
        "Grid stabilization requirements"
      ],
      "supply_characteristics": {
        "major_producers": ["Australia", "Chile", "China", "Argentina"],
        "production_volume": "100k tonnes annually",
        "extraction_methods": ["Hard rock mining", "Brine extraction"],
        "price_volatility": "High due to supply concentration"
      }
    },
    {
      "name": "Cobalt",
      "symbol": "CO",
      "description": "Essential for battery stability and performance",
      "applications": [
        "Lithium-ion battery cathodes",
        "Superalloys for aerospace",
        "Chemical catalysts",
        "Pigments and ceramics"
      ],
      "demand_drivers": [
        "EV battery production scaling",
        "Energy storage systems growth",
        "Aerospace industry expansion",
        "Chemical industry needs"
      ],
      "supply_characteristics": {
        "major_producers": ["Congo", "Russia", "Australia", "Canada"],
        "production_volume": "140k tonnes annually",
        "byproduct_status": "80% from copper mining",
        "ethical_concerns": "Artisanal mining practices"
      }
    },
    {
      "name": "Nickel",
      "symbol": "NI",
      "description": "Key component in stainless steel and batteries",
      "applications": [
        "Stainless steel production",
        "EV battery cathodes",
        "Superalloys and turbines",
        "Electroplating and chemicals"
      ],
      "demand_drivers": [
        "Stainless steel demand growth",
        "EV battery technology shift",
        "Renewable energy infrastructure",
        "Industrial manufacturing"
      ],
      "supply_characteristics": {
        "major_producers": ["Indonesia", "Philippines", "Russia", "Australia"],
        "production_volume": "2.7M tonnes annually",
        "classifications": ["Class 1 (battery-grade)", "Class 2 (stainless steel)"],
        "environmental_impact": "High carbon footprint in Indonesia"
      }
    },
    {
      "name": "Zinc",
      "symbol": "ZN",
      "description": "Protective coating and industrial applications",
      "applications": [
        "Galvanizing steel protection",
        "Die casting for automotive",
        "Brass and bronze production",
        "Chemicals and pharmaceuticals"
      ],
      "demand_drivers": [
        "Steel production and infrastructure",
        "Automotive lightweighting",
        "Construction industry growth",
        "Green technology adoption"
      ],
      "supply_characteristics": {
        "major_producers": ["China", "Australia", "Peru", "India"],
        "production_volume": "13M tonnes annually",
        "recycling_rate": "30%",
        "byproduct_status": "Often co-produced with lead"
      }
    },
    {
      "name": "Aluminum",
      "symbol": "AL",
      "description": "Lightweight structural material",
      "applications": [
        "Transportation (aircraft, vehicles)",
        "Construction and building",
        "Packaging (cans, foil)",
        "Electrical transmission"
      ],
      "demand_drivers": [
        "Aerospace industry growth",
        "Electric vehicle lightweighting",
        "Sustainable construction",
        "Renewable energy infrastructure"
      ],
      "supply_characteristics": {
        "major_producers": ["China", "India", "Russia", "Canada"],
        "production_volume": "65M tonnes annually",
        "energy_intensity": "High electricity consumption",
        "recycling_rate": "75% (most recycled metal)"
      }
    },
    {
      "name": "Iron Ore",
      "symbol": "IO",
      "description": "Foundation of steel production",
      "applications": [
        "Steel production for construction",
        "Automotive industry",
        "Infrastructure development",
        "Manufacturing equipment"
      ],
      "demand_drivers": [
        "Infrastructure investment (Belt & Road)",
        "Urbanization in Asia",
        "Automotive production",
        "Industrial manufacturing"
      ],
      "supply_characteristics": {
        "major_producers": ["Australia", "Brazil", "China", "India"],
        "production_volume": "2.8B tonnes annually",
        "grade_variations": ["High-grade (>62% Fe)", "Low-grade (<58% Fe)"],
        "logistics_challenges": "Distance from mines to steel mills"
      }
    }
  ]
}
```

#### **Battery Metals Focus Dataset**
```json
{
  "dataset_name": "battery_metals_intelligence",
  "description": "Specialized dataset for EV and energy storage metals",
  "focus_area": "Lithium-ion battery supply chain",
  "critical_metals": [
    {
      "metal": "Lithium",
      "battery_relevance": "Anode material, electrolyte",
      "demand_projection_2030": "3M tonnes LCE",
      "current_supply_gap": "500k tonnes by 2027",
      "price_sensitivity": "High volatility due to supply concentration"
    },
    {
      "metal": "Cobalt",
      "battery_relevance": "Cathode stability, energy density",
      "ethical_concerns": " DRC artisanal mining (70% supply)",
      "substitutes": "Nickel-cobalt-manganese cathodes",
      "supply_risk": "High geopolitical risk"
    },
    {
      "metal": "Nickel",
      "battery_relevance": "High-energy cathodes (NMC, NCA)",
      "demand_shift": "Class 1 nickel for batteries vs Class 2 for steel",
      "supply_response": "Indonesia production surge",
      "environmental_impact": "High carbon emissions"
    },
    {
      "metal": "Graphite",
      "battery_relevance": "Anode material",
      "supply_dominance": "China (80% of spherical graphite)",
      "synthetic_alternatives": "Developing technology",
      "scalability_challenges": "Purification processes"
    }
  ],
  "battery_chemistry_evolution": {
    "current": "NMC 622 (Nickel Manganese Cobalt)",
    "transitioning": "NMC 811, NCA (Nickel Cobalt Aluminum)",
    "future": "Lithium Iron Phosphate (LFP), solid-state batteries",
    "impact_on_metals": {
      "nickel_demand_increase": "300% by 2030",
      "cobalt_demand_decrease": "70% reduction possible",
      "lithium_demand_surge": "500% increase projected"
    }
  }
}
```

---

## 🔍 Data Collection Sources

### **1. Primary Commodity Exchanges**

#### **London Metal Exchange (LME)**
```python
LME_DATA_SOURCES = {
    'official_api': {
        'base_url': 'https://www.lme.com/api',
        'endpoints': {
            'pricing': '/api/v1/pricing',
            'warehouse': '/api/v1/warehouse-stocks',
            'trades': '/api/v1/trades',
            'settlement': '/api/v1/settlement-prices'
        },
        'data_types': ['spot', 'futures', 'options', 'stocks'],
        'metals': ['copper', 'aluminum', 'zinc', 'lead', 'nickel', 'tin'],
        'update_frequency': 'real-time',
        'historical_depth': '30+ years'
    },
    'alternative_access': {
        'yahoo_finance': 'LME data through YF API',
        'bloomberg_terminal': 'LME data feeds',
        'refinitiv': 'LME price data',
        'tradingview': 'LME charts and indicators'
    }
}
```

#### **COMEX (CME Group)**
```python
COMEX_DATA_SOURCES = {
    'metals_traded': ['copper', 'gold', 'silver', 'platinum', 'palladium'],
    'contract_types': ['futures', 'options', 'mini-contracts'],
    'data_availability': {
        'real_time': 'Premium subscription',
        'delayed': 'Free with 15-min delay',
        'historical': '20+ years available'
    },
    'api_access': {
        'endpoint': 'https://www.cmegroup.com/api',
        'authentication': 'API key required',
        'rate_limits': '1000 requests/hour'
    }
}
```

#### **Shanghai Futures Exchange (SHFE)**
```python
SHFE_DATA_SOURCES = {
    'metals': ['copper', 'aluminum', 'zinc', 'lead', 'nickel', 'gold'],
    'trading_hours': 'Asia time zone (9:00-15:00, 21:00-01:00 CST)',
    'data_challenges': {
        'language_barrier': 'Primarily Chinese interface',
        'api_limitations': 'Limited English API access',
        'time_zone_complexity': 'Overlapping sessions'
    },
    'alternative_sources': [
        'Bloomberg SHFE data feeds',
        'Refinitiv SHFE pricing',
        'Local Chinese data providers'
    ]
}
```

### **2. Alternative Data Sources**

#### **Satellite Imagery & Mining Intelligence**
```python
SATELLITE_DATA_SOURCES = {
    'planet_labs': {
        'resolution': '3-5 meters',
        'update_frequency': 'daily',
        'coverage': 'global mining operations',
        'data_types': ['mine_activity', 'stockpile_levels', 'infrastructure_changes'],
        'cost': '$1-10 per sq km',
        'api_endpoint': 'https://api.planet.com'
    },
    'maxar': {
        'resolution': '30cm-1.5m',
        'specialty': 'high-resolution infrastructure',
        'use_cases': ['port_activity', 'railway_monitoring', 'smelter_operations'],
        'cost': '$10-50 per sq km',
        'api_endpoint': 'https://api.maxar.com'
    },
    'mining_intelligence': {
        'providers': ['SNL Metals & Mining', 'Wood Mackenzie', 'CRU Group'],
        'data_types': ['production_forecasts', 'capex_plans', 'reserve_estimates'],
        'update_frequency': 'quarterly/annual',
        'cost': '$10k-50k annually'
    }
}
```

#### **Shipping & Logistics Data**
```python
SHIPPING_DATA_SOURCES = {
    'marine_traffic': {
        'api_endpoint': 'https://api.marinetraffic.com',
        'data_types': ['vessel_positions', 'port_calls', 'cargo_info'],
        'coverage': '95% of global shipping',
        'update_frequency': 'real-time',
        'cost': '$500-5000/month'
    },
    'vessel_finder': {
        'specialty': 'historical_vessel_tracking',
        'data_types': ['route_history', 'cargo_capacity', 'ownership'],
        'cost': '$200-2000/month'
    },
    'port_intelligence': {
        'providers': ['PortCall', 'ImportGenius', 'Panama Canal data'],
        'data_types': ['berth_occupancy', 'cargo_volumes', 'waiting_times'],
        'geographic_focus': ['China ports', 'Brazil ports', 'Australia ports']
    }
}
```

#### **Economic & Fundamental Data**
```python
ECONOMIC_DATA_SOURCES = {
    'world_bank': {
        'api_endpoint': 'https://api.worldbank.org/v2',
        'data_types': ['GDP_growth', 'industrial_production', 'trade_balances'],
        'country_coverage': '200+ countries',
        'update_frequency': 'quarterly',
        'cost': 'free'
    },
    'imf': {
        'api_endpoint': 'https://www.imf.org/external/datamapper/api',
        'data_types': ['economic_forecasts', 'currency_rates', 'debt_levels'],
        'global_coverage': '190+ countries',
        'cost': 'free'
    },
    'oecd': {
        'data_types': ['leading_indicators', 'composite_indexes', 'trade_data'],
        'focus': 'developed_economies',
        'cost': 'subscription_based'
    }
}
```

---

## 🤖 ML Model Training Datasets

### **1. Time Series Forecasting Dataset**

#### **Structure for Price Prediction Models**
```python
class CommodityPriceDataset:
    def __init__(self, commodity: str, timeframe: str):
        self.commodity = commodity
        self.timeframe = timeframe  # '1D', '1H', '15min'
        self.features = self._define_features()
        self.targets = self._define_targets()

    def _define_features(self) -> List[str]:
        """Define feature set for price prediction"""
        return [
            # Price-based features
            'close_price', 'volume', 'high', 'low', 'open',
            'returns_1d', 'returns_5d', 'returns_20d',
            'volatility_5d', 'volatility_20d', 'volatility_60d',

            # Technical indicators
            'sma_5', 'sma_20', 'sma_50', 'ema_12', 'ema_26',
            'rsi_14', 'macd', 'macd_signal', 'macd_hist',
            'bb_upper', 'bb_middle', 'bb_lower', 'bb_width',
            'stoch_k', 'stoch_d', 'williams_r',

            # Volume indicators
            'volume_sma_5', 'volume_sma_20', 'obv', 'volume_ratio',

            # Market microstructure
            'spread', 'depth_imbalance', 'order_flow',

            # Alternative data
            'satellite_activity_index', 'shipping_volume_index',
            'sentiment_score', 'news_volume',

            # Economic indicators
            'usd_index', 'interest_rates', 'industrial_production',
            'trade_balance', 'currency_volatility',

            # Commodity-specific
            'inventory_levels', 'production_data', 'demand_forecasts'
        ]

    def _define_targets(self) -> List[str]:
        """Define prediction targets"""
        return [
            'price_next_1d', 'price_next_5d', 'price_next_20d',
            'return_next_1d', 'return_next_5d', 'return_next_20d',
            'volatility_next_5d', 'volatility_next_20d',
            'direction_next_1d', 'direction_next_5d', 'direction_next_20d'
        ]

    def generate_training_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Generate comprehensive training dataset"""
        # Implementation would collect data from all sources
        # and create feature matrix with targets
        pass
```

#### **Sample Training Data Structure**
```json
{
  "dataset_info": {
    "commodity": "copper",
    "timeframe": "1D",
    "date_range": "2010-01-01 to 2024-12-31",
    "total_samples": 3652,
    "feature_count": 45,
    "target_variables": 11
  },
  "sample_record": {
    "date": "2024-01-15",
    "features": {
      "close_price": 8450.50,
      "volume": 125000,
      "returns_1d": 0.0234,
      "rsi_14": 67.85,
      "macd": 45.23,
      "satellite_activity_index": 0.78,
      "shipping_volume_index": 1.12,
      "sentiment_score": 0.65,
      "usd_index": 102.45,
      "inventory_levels": 285000
    },
    "targets": {
      "price_next_1d": 8475.20,
      "return_next_1d": 0.0029,
      "direction_next_1d": 1,
      "volatility_next_5d": 0.025
    }
  }
}
```

### **2. Multi-Modal Learning Dataset**

#### **Image + Time Series Fusion**
```python
class MultiModalCommodityDataset:
    def __init__(self):
        self.image_sources = ['satellite', 'drone', 'street_view']
        self.time_series_sources = ['price_data', 'volume_data', 'economic_indicators']
        self.text_sources = ['news', 'reports', 'social_media']

    def create_fusion_dataset(self, commodity: str) -> Dict:
        """Create multi-modal dataset for advanced ML models"""

        dataset = {
            'metadata': {
                'commodity': commodity,
                'modalities': ['visual', 'temporal', 'textual'],
                'time_range': '2020-2024',
                'geographic_coverage': self._get_coverage_areas(commodity)
            },
            'visual_data': self._collect_satellite_images(commodity),
            'temporal_data': self._collect_time_series_data(commodity),
            'textual_data': self._collect_text_data(commodity),
            'fusion_labels': self._create_fusion_labels()
        }

        return dataset

    def _collect_satellite_images(self, commodity: str) -> List[Dict]:
        """Collect satellite imagery for mining sites"""
        mining_sites = self._get_mining_sites(commodity)

        satellite_data = []
        for site in mining_sites:
            images = self._download_satellite_images(site['coordinates'])
            for image in images:
                satellite_data.append({
                    'site_name': site['name'],
                    'coordinates': site['coordinates'],
                    'timestamp': image['timestamp'],
                    'image_path': image['path'],
                    'resolution': image['resolution'],
                    'cloud_cover': image['cloud_cover'],
                    'activity_labels': self._analyze_mining_activity(image)
                })

        return satellite_data

    def _collect_time_series_data(self, commodity: str) -> pd.DataFrame:
        """Collect comprehensive time series data"""
        # Implementation would aggregate from multiple sources
        pass

    def _collect_text_data(self, commodity: str) -> List[Dict]:
        """Collect news, reports, and social media data"""
        text_data = []

        # News articles
        news = self._scrape_news_sources(commodity)
        text_data.extend(news)

        # Industry reports
        reports = self._download_industry_reports(commodity)
        text_data.extend(reports)

        # Social media sentiment
        social = self._collect_social_media_data(commodity)
        text_data.extend(social)

        return text_data
```

---

## 📊 Dataset Quality Metrics

### **Data Quality Assessment Framework**
```python
class DataQualityAssessor:
    def __init__(self):
        self.quality_metrics = {
            'completeness': 0.95,    # 95% of expected data present
            'accuracy': 0.98,        # 98% data accuracy
            'timeliness': 3600,      # Max 1 hour delay
            'consistency': 0.99,     # 99% internal consistency
            'validity': 0.97         # 97% data within valid ranges
        }

    def assess_dataset_quality(self, dataset: pd.DataFrame) -> Dict:
        """Comprehensive data quality assessment"""

        assessment = {
            'completeness_score': self._check_completeness(dataset),
            'accuracy_score': self._check_accuracy(dataset),
            'timeliness_score': self._check_timeliness(dataset),
            'consistency_score': self._check_consistency(dataset),
            'validity_score': self._check_validity(dataset),
            'overall_quality': 0.0,
            'issues_found': [],
            'recommendations': []
        }

        # Calculate overall quality score
        scores = [
            assessment['completeness_score'],
            assessment['accuracy_score'],
            assessment['timeliness_score'],
            assessment['consistency_score'],
            assessment['validity_score']
        ]

        assessment['overall_quality'] = sum(scores) / len(scores)

        # Generate recommendations
