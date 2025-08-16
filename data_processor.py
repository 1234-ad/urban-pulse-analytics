"""
Advanced Data Processing Module for Urban Pulse Analytics
Handles data cleaning, transformation, and statistical analysis
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

class UrbanDataProcessor:
    """Advanced data processing for urban analytics"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.min_max_scaler = MinMaxScaler()
        
    def clean_traffic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate traffic data"""
        df_clean = df.copy()
        
        # Remove outliers using IQR method
        Q1 = df_clean['congestion_level'].quantile(0.25)
        Q3 = df_clean['congestion_level'].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df_clean = df_clean[
            (df_clean['congestion_level'] >= lower_bound) & 
            (df_clean['congestion_level'] <= upper_bound)
        ]
        
        # Validate speed vs congestion relationship
        df_clean['speed_congestion_ratio'] = df_clean['avg_speed_mph'] / (df_clean['congestion_level'] + 1)
        
        # Add time-based features
        df_clean['hour'] = pd.to_datetime(df_clean['timestamp']).dt.hour
        df_clean['day_of_week'] = pd.to_datetime(df_clean['timestamp']).dt.dayofweek
        df_clean['is_weekend'] = df_clean['day_of_week'].isin([5, 6])
        df_clean['is_rush_hour'] = df_clean['hour'].isin([7, 8, 9, 17, 18, 19])
        
        return df_clean
    
    def calculate_traffic_efficiency_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate traffic efficiency metrics"""
        df_processed = df.copy()
        
        # Traffic Efficiency Index (TEI)
        # Higher speed and lower congestion = higher efficiency
        df_processed['traffic_efficiency_index'] = (
            (df_processed['avg_speed_mph'] / 45) * 0.6 +  # Normalized speed
            ((100 - df_processed['congestion_level']) / 100) * 0.4  # Inverted congestion
        ) * 100
        
        # Incident Impact Score
        df_processed['incident_impact'] = df_processed['incidents'] * df_processed['congestion_level'] / 100
        
        # Peak vs Off-Peak Performance
        peak_hours = [7, 8, 9, 17, 18, 19]
        df_processed['is_peak'] = df_processed['hour'].isin(peak_hours)
        
        return df_processed
    
    def analyze_air_quality_patterns(self, df: pd.DataFrame) -> dict:
        """Analyze air quality patterns and correlations"""
        analysis = {}
        
        # Basic statistics
        analysis['basic_stats'] = {
            'mean_aqi': df['aqi'].mean(),
            'median_aqi': df['aqi'].median(),
            'std_aqi': df['aqi'].std(),
            'min_aqi': df['aqi'].min(),
            'max_aqi': df['aqi'].max()
        }
        
        # Category distribution
        analysis['category_distribution'] = df['category'].value_counts().to_dict()
        
        # Trend analysis
        df['date'] = pd.to_datetime(df['date'])
        df_sorted = df.sort_values('date')
        
        # Calculate 7-day moving average
        df_sorted['aqi_7day_ma'] = df_sorted['aqi'].rolling(window=7, center=True).mean()
        
        # Trend direction (simple linear regression)
        x = np.arange(len(df_sorted))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, df_sorted['aqi'])
        
        analysis['trend'] = {
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'direction': 'improving' if slope < 0 else 'worsening' if slope > 0 else 'stable'
        }
        
        # Seasonal patterns (if enough data)
        if len(df_sorted) >= 30:
            df_sorted['day_of_year'] = df_sorted['date'].dt.dayofyear
            seasonal_corr = np.corrcoef(df_sorted['day_of_year'], df_sorted['aqi'])[0, 1]
            analysis['seasonal_correlation'] = seasonal_corr
        
        return analysis
    
    def calculate_economic_health_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate comprehensive economic health metrics"""
        df_processed = df.copy()
        
        # Normalize all economic indicators to 0-100 scale
        df_processed['employment_normalized'] = self.min_max_scaler.fit_transform(
            df_processed[['employment_rate']]
        ).flatten() * 100
        
        df_processed['housing_normalized'] = self.min_max_scaler.fit_transform(
            df_processed[['housing_affordability_index']]
        ).flatten() * 100
        
        df_processed['business_normalized'] = df_processed['business_activity_score']  # Already 0-100
        
        # Economic Health Index (weighted average)
        df_processed['economic_health_index'] = (
            df_processed['employment_normalized'] * 0.4 +
            df_processed['housing_normalized'] * 0.3 +
            df_processed['business_normalized'] * 0.3
        )
        
        # Economic volatility (rolling standard deviation)
        df_processed['economic_volatility'] = df_processed['economic_health_index'].rolling(
            window=7, min_periods=1
        ).std()
        
        return df_processed
    
    def analyze_sentiment_dynamics(self, df: pd.DataFrame) -> dict:
        """Analyze social sentiment patterns and dynamics"""
        analysis = {}
        
        # Overall sentiment statistics
        analysis['overall_sentiment'] = {
            'mean_sentiment': df['sentiment_score'].mean(),
            'sentiment_volatility': df['sentiment_score'].std(),
            'positive_ratio': len(df[df['sentiment_score'] > 0.1]) / len(df),
            'negative_ratio': len(df[df['sentiment_score'] < -0.1]) / len(df),
            'neutral_ratio': len(df[abs(df['sentiment_score']) <= 0.1]) / len(df)
        }
        
        # Topic-wise sentiment analysis
        topic_sentiment = df.groupby('topic').agg({
            'sentiment_score': ['mean', 'std', 'count'],
            'mention_volume': 'sum'
        }).round(3)
        
        analysis['topic_sentiment'] = topic_sentiment.to_dict()
        
        # Sentiment trends over time
        df['date'] = pd.to_datetime(df['date'])
        daily_sentiment = df.groupby('date')['sentiment_score'].mean()
        
        # Calculate sentiment momentum (rate of change)
        sentiment_momentum = daily_sentiment.diff().mean()
        analysis['sentiment_momentum'] = sentiment_momentum
        
        # Most discussed topics
        topic_volume = df.groupby('topic')['mention_volume'].sum().sort_values(ascending=False)
        analysis['top_topics'] = topic_volume.head().to_dict()
        
        # Sentiment-volume correlation
        topic_corr = df.groupby('topic').apply(
            lambda x: np.corrcoef(x['sentiment_score'], x['mention_volume'])[0, 1]
        ).fillna(0)
        analysis['sentiment_volume_correlation'] = topic_corr.to_dict()
        
        return analysis
    
    def detect_anomalies(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Detect anomalies in urban data using Isolation Forest"""
        df_processed = df.copy()
        
        # Prepare data for anomaly detection
        data_for_anomaly = df_processed[columns].fillna(df_processed[columns].mean())
        
        # Standardize the data
        data_scaled = self.scaler.fit_transform(data_for_anomaly)
        
        # Apply Isolation Forest
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_labels = iso_forest.fit_predict(data_scaled)
        
        # Add anomaly flags
        df_processed['is_anomaly'] = anomaly_labels == -1
        df_processed['anomaly_score'] = iso_forest.score_samples(data_scaled)
        
        return df_processed
    
    def perform_city_clustering(self, city_data: dict) -> dict:
        """Cluster cities based on their characteristics"""
        
        # Prepare data for clustering
        cities = list(city_data.keys())
        features = []
        
        for city in cities:
            city_features = [
                city_data[city]['traffic_score'],
                city_data[city]['air_quality_score'],
                city_data[city]['economic_score'],
                city_data[city]['sentiment_score']
            ]
            features.append(city_features)
        
        features_array = np.array(features)
        
        # Standardize features
        features_scaled = self.scaler.fit_transform(features_array)
        
        # Perform K-means clustering
        n_clusters = min(4, len(cities))  # Max 4 clusters
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(features_scaled)
        
        # Perform PCA for visualization
        pca = PCA(n_components=2)
        features_pca = pca.fit_transform(features_scaled)
        
        # Create results
        clustering_results = {
            'cities': cities,
            'cluster_labels': cluster_labels.tolist(),
            'pca_coordinates': features_pca.tolist(),
            'cluster_centers': kmeans.cluster_centers_.tolist(),
            'explained_variance_ratio': pca.explained_variance_ratio_.tolist()
        }
        
        # Interpret clusters
        cluster_interpretation = {}
        for i in range(n_clusters):
            cluster_cities = [cities[j] for j in range(len(cities)) if cluster_labels[j] == i]
            cluster_center = kmeans.cluster_centers_[i]
            
            # Interpret cluster characteristics
            characteristics = []
            if cluster_center[0] > 0.5:  # High traffic score
                characteristics.append("Good Traffic Flow")
            elif cluster_center[0] < -0.5:
                characteristics.append("Traffic Congestion Issues")
            
            if cluster_center[1] > 0.5:  # High air quality score
                characteristics.append("Clean Air")
            elif cluster_center[1] < -0.5:
                characteristics.append("Air Quality Concerns")
            
            if cluster_center[2] > 0.5:  # High economic score
                characteristics.append("Strong Economy")
            elif cluster_center[2] < -0.5:
                characteristics.append("Economic Challenges")
            
            if cluster_center[3] > 0.5:  # High sentiment score
                characteristics.append("Positive Community Sentiment")
            elif cluster_center[3] < -0.5:
                characteristics.append("Community Concerns")
            
            cluster_interpretation[f"Cluster {i+1}"] = {
                'cities': cluster_cities,
                'characteristics': characteristics if characteristics else ["Balanced Profile"]
            }
        
        clustering_results['interpretation'] = cluster_interpretation
        
        return clustering_results
    
    def calculate_correlation_matrix(self, df: pd.DataFrame, numeric_columns: list) -> pd.DataFrame:
        """Calculate correlation matrix for urban metrics"""
        
        # Select only numeric columns that exist in the dataframe
        available_columns = [col for col in numeric_columns if col in df.columns]
        
        if len(available_columns) < 2:
            return pd.DataFrame()
        
        # Calculate correlation matrix
        correlation_matrix = df[available_columns].corr()
        
        return correlation_matrix
    
    def generate_data_quality_report(self, df: pd.DataFrame) -> dict:
        """Generate comprehensive data quality report"""
        
        report = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'missing_data': {},
            'data_types': {},
            'duplicates': df.duplicated().sum(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        # Missing data analysis
        for column in df.columns:
            missing_count = df[column].isnull().sum()
            missing_percentage = (missing_count / len(df)) * 100
            report['missing_data'][column] = {
                'count': missing_count,
                'percentage': round(missing_percentage, 2)
            }
        
        # Data types
        for column in df.columns:
            report['data_types'][column] = str(df[column].dtype)
        
        # Numeric columns statistics
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            report['numeric_summary'] = df[numeric_columns].describe().to_dict()
        
        return report

class UrbanMetricsCalculator:
    """Calculate advanced urban metrics and KPIs"""
    
    @staticmethod
    def calculate_livability_index(traffic_score: float, air_score: float, 
                                 economic_score: float, sentiment_score: float,
                                 weights: dict = None) -> dict:
        """Calculate comprehensive livability index"""
        
        if weights is None:
            weights = {
                'traffic': 0.25,
                'air_quality': 0.25,
                'economic': 0.25,
                'social': 0.25
            }
        
        # Ensure weights sum to 1
        total_weight = sum(weights.values())
        if total_weight != 1.0:
            weights = {k: v/total_weight for k, v in weights.items()}
        
        livability_score = (
            traffic_score * weights['traffic'] +
            air_score * weights['air_quality'] +
            economic_score * weights['economic'] +
            sentiment_score * weights['social']
        )
        
        # Categorize livability
        if livability_score >= 85:
            category = "Excellent"
            description = "Outstanding quality of life"
        elif livability_score >= 75:
            category = "Very Good"
            description = "High quality of life"
        elif livability_score >= 65:
            category = "Good"
            description = "Good quality of life"
        elif livability_score >= 55:
            category = "Fair"
            description = "Moderate quality of life"
        elif livability_score >= 45:
            category = "Poor"
            description = "Below average quality of life"
        else:
            category = "Critical"
            description = "Significant quality of life issues"
        
        return {
            'livability_score': round(livability_score, 2),
            'category': category,
            'description': description,
            'component_scores': {
                'traffic': traffic_score,
                'air_quality': air_score,
                'economic': economic_score,
                'social': sentiment_score
            },
            'weights_used': weights
        }
    
    @staticmethod
    def calculate_sustainability_index(air_quality_score: float, traffic_efficiency: float,
                                     green_space_ratio: float = None) -> dict:
        """Calculate environmental sustainability index"""
        
        # Base calculation with available metrics
        if green_space_ratio is not None:
            sustainability_score = (
                air_quality_score * 0.4 +
                traffic_efficiency * 0.3 +
                green_space_ratio * 0.3
            )
        else:
            # Without green space data
            sustainability_score = (
                air_quality_score * 0.6 +
                traffic_efficiency * 0.4
            )
        
        # Categorize sustainability
        if sustainability_score >= 80:
            category = "Highly Sustainable"
        elif sustainability_score >= 70:
            category = "Sustainable"
        elif sustainability_score >= 60:
            category = "Moderately Sustainable"
        elif sustainability_score >= 50:
            category = "Low Sustainability"
        else:
            category = "Unsustainable"
        
        return {
            'sustainability_score': round(sustainability_score, 2),
            'category': category,
            'components': {
                'air_quality': air_quality_score,
                'traffic_efficiency': traffic_efficiency,
                'green_space': green_space_ratio
            }
        }
    
    @staticmethod
    def calculate_resilience_score(economic_volatility: float, sentiment_volatility: float,
                                 infrastructure_score: float = 75) -> dict:
        """Calculate city resilience score"""
        
        # Lower volatility = higher resilience
        economic_resilience = max(0, 100 - (economic_volatility * 10))
        social_resilience = max(0, 100 - (sentiment_volatility * 50))
        
        resilience_score = (
            economic_resilience * 0.4 +
            social_resilience * 0.3 +
            infrastructure_score * 0.3
        )
        
        if resilience_score >= 80:
            category = "Highly Resilient"
        elif resilience_score >= 70:
            category = "Resilient"
        elif resilience_score >= 60:
            category = "Moderately Resilient"
        else:
            category = "Low Resilience"
        
        return {
            'resilience_score': round(resilience_score, 2),
            'category': category,
            'components': {
                'economic_resilience': round(economic_resilience, 2),
                'social_resilience': round(social_resilience, 2),
                'infrastructure_score': infrastructure_score
            }
        }