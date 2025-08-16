"""
Urban Pulse Analytics - Real-time City Health Monitoring System
A comprehensive data analysis platform for urban quality of life metrics
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta
import random
import time
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Urban Pulse Analytics",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .alert-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .alert-medium {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .alert-low {
        background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .insight-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-left: 5px solid #2E86AB;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class UrbanDataGenerator:
    """Generates realistic urban data for analysis"""
    
    def __init__(self):
        self.cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte"
        ]
        
        self.base_time = datetime.now() - timedelta(days=30)
    
    def generate_traffic_data(self, city: str, days: int = 30) -> pd.DataFrame:
        """Generate realistic traffic congestion data"""
        data = []
        
        for day in range(days):
            current_date = self.base_time + timedelta(days=day)
            
            # Generate hourly data for each day
            for hour in range(24):
                timestamp = current_date.replace(hour=hour, minute=0, second=0)
                
                # Traffic patterns: higher during rush hours, weekdays vs weekends
                is_weekend = timestamp.weekday() >= 5
                is_rush_hour = hour in [7, 8, 9, 17, 18, 19]
                
                base_congestion = 30
                if is_rush_hour and not is_weekend:
                    base_congestion += 40
                elif is_weekend:
                    base_congestion -= 10
                
                # Add some randomness and city-specific factors
                city_factor = hash(city) % 20 - 10
                congestion = max(0, min(100, base_congestion + city_factor + random.gauss(0, 15)))
                
                data.append({
                    'timestamp': timestamp,
                    'city': city,
                    'congestion_level': round(congestion, 1),
                    'avg_speed_mph': round(45 - (congestion * 0.3), 1),
                    'incidents': max(0, int(congestion / 20) + random.poisson(1))
                })
        
        return pd.DataFrame(data)
    
    def generate_air_quality_data(self, city: str, days: int = 30) -> pd.DataFrame:
        """Generate air quality index data"""
        data = []
        
        for day in range(days):
            current_date = self.base_time + timedelta(days=day)
            
            # Base AQI varies by city and weather patterns
            base_aqi = 50 + (hash(city) % 30)
            
            # Weather influence (simplified)
            weather_factor = random.choice([-15, -10, -5, 0, 5, 10, 20])  # Rain reduces AQI
            
            # Seasonal trends
            month = current_date.month
            seasonal_factor = 10 if month in [6, 7, 8] else -5  # Summer pollution
            
            aqi = max(0, min(300, base_aqi + weather_factor + seasonal_factor + random.gauss(0, 20)))
            
            # Categorize AQI
            if aqi <= 50:
                category = "Good"
            elif aqi <= 100:
                category = "Moderate"
            elif aqi <= 150:
                category = "Unhealthy for Sensitive"
            elif aqi <= 200:
                category = "Unhealthy"
            else:
                category = "Very Unhealthy"
            
            data.append({
                'date': current_date.date(),
                'city': city,
                'aqi': round(aqi, 1),
                'category': category,
                'pm25': round(aqi * 0.4, 1),
                'pm10': round(aqi * 0.6, 1)
            })
        
        return pd.DataFrame(data)
    
    def generate_economic_data(self, city: str, days: int = 30) -> pd.DataFrame:
        """Generate economic indicators"""
        data = []
        
        # Base economic health varies by city
        base_employment = 95 + (hash(city) % 8)
        base_housing_index = 100 + (hash(city) % 50)
        
        for day in range(days):
            current_date = self.base_time + timedelta(days=day)
            
            # Economic indicators change slowly
            employment_rate = base_employment + random.gauss(0, 0.5)
            housing_affordability = base_housing_index + random.gauss(0, 2)
            business_activity = 50 + random.gauss(0, 15)
            
            data.append({
                'date': current_date.date(),
                'city': city,
                'employment_rate': round(max(85, min(99, employment_rate)), 2),
                'housing_affordability_index': round(max(50, housing_affordability), 1),
                'business_activity_score': round(max(0, min(100, business_activity)), 1),
                'retail_footfall': random.randint(1000, 5000)
            })
        
        return pd.DataFrame(data)
    
    def generate_social_sentiment_data(self, city: str, days: int = 30) -> pd.DataFrame:
        """Generate social media sentiment data"""
        data = []
        
        sentiment_topics = [
            'transportation', 'safety', 'environment', 'economy', 
            'healthcare', 'education', 'recreation', 'governance'
        ]
        
        for day in range(days):
            current_date = self.base_time + timedelta(days=day)
            
            for topic in sentiment_topics:
                # Sentiment varies by topic and random events
                base_sentiment = 0.1 + (hash(f"{city}_{topic}") % 100) / 100 * 0.6
                daily_variation = random.gauss(0, 0.2)
                sentiment = max(-1, min(1, base_sentiment + daily_variation))
                
                # Volume of mentions
                volume = random.randint(50, 500)
                
                data.append({
                    'date': current_date.date(),
                    'city': city,
                    'topic': topic,
                    'sentiment_score': round(sentiment, 3),
                    'mention_volume': volume,
                    'positive_mentions': int(volume * max(0, sentiment)),
                    'negative_mentions': int(volume * max(0, -sentiment))
                })
        
        return pd.DataFrame(data)

class UrbanPulseAnalyzer:
    """Main analyzer for urban data"""
    
    def __init__(self):
        self.data_generator = UrbanDataGenerator()
    
    def calculate_city_health_score(self, city: str) -> Dict:
        """Calculate overall city health score"""
        
        # Generate all data types
        traffic_data = self.data_generator.generate_traffic_data(city, 7)  # Last week
        air_data = self.data_generator.generate_air_quality_data(city, 7)
        economic_data = self.data_generator.generate_economic_data(city, 7)
        sentiment_data = self.data_generator.generate_social_sentiment_data(city, 7)
        
        # Calculate component scores (0-100)
        
        # Traffic Score (lower congestion = higher score)
        avg_congestion = traffic_data['congestion_level'].mean()
        traffic_score = max(0, 100 - avg_congestion)
        
        # Air Quality Score
        avg_aqi = air_data['aqi'].mean()
        air_score = max(0, 100 - (avg_aqi / 2))  # AQI of 200 = score of 0
        
        # Economic Score
        avg_employment = economic_data['employment_rate'].mean()
        avg_business = economic_data['business_activity_score'].mean()
        economic_score = (avg_employment - 85) * 6.67 + avg_business * 0.5  # Normalize to 0-100
        
        # Social Sentiment Score
        avg_sentiment = sentiment_data['sentiment_score'].mean()
        sentiment_score = (avg_sentiment + 1) * 50  # Convert -1,1 to 0-100
        
        # Weighted overall score
        overall_score = (
            traffic_score * 0.25 +
            air_score * 0.25 +
            economic_score * 0.25 +
            sentiment_score * 0.25
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'traffic_score': round(traffic_score, 1),
            'air_quality_score': round(air_score, 1),
            'economic_score': round(max(0, min(100, economic_score)), 1),
            'sentiment_score': round(sentiment_score, 1),
            'grade': self._score_to_grade(overall_score),
            'status': self._score_to_status(overall_score)
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90: return "A+"
        elif score >= 85: return "A"
        elif score >= 80: return "A-"
        elif score >= 75: return "B+"
        elif score >= 70: return "B"
        elif score >= 65: return "B-"
        elif score >= 60: return "C+"
        elif score >= 55: return "C"
        elif score >= 50: return "C-"
        else: return "D"
    
    def _score_to_status(self, score: float) -> str:
        """Convert score to status description"""
        if score >= 80: return "Excellent"
        elif score >= 70: return "Good"
        elif score >= 60: return "Fair"
        elif score >= 50: return "Poor"
        else: return "Critical"
    
    def analyze_trends(self, city: str) -> Dict:
        """Analyze trends over time"""
        
        # Generate 30 days of data
        traffic_data = self.data_generator.generate_traffic_data(city, 30)
        air_data = self.data_generator.generate_air_quality_data(city, 30)
        economic_data = self.data_generator.generate_economic_data(city, 30)
        
        # Calculate daily averages for traffic
        daily_traffic = traffic_data.groupby(traffic_data['timestamp'].dt.date).agg({
            'congestion_level': 'mean',
            'avg_speed_mph': 'mean',
            'incidents': 'sum'
        }).reset_index()
        
        # Trend analysis
        traffic_trend = self._calculate_trend(daily_traffic['congestion_level'].values)
        air_trend = self._calculate_trend(air_data['aqi'].values)
        employment_trend = self._calculate_trend(economic_data['employment_rate'].values)
        
        return {
            'traffic_trend': traffic_trend,
            'air_quality_trend': air_trend,
            'employment_trend': employment_trend,
            'traffic_data': daily_traffic,
            'air_data': air_data,
            'economic_data': economic_data
        }
    
    def _calculate_trend(self, values: np.array) -> str:
        """Calculate if trend is improving, declining, or stable"""
        if len(values) < 2:
            return "Insufficient data"
        
        # Simple linear regression slope
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if abs(slope) < 0.1:
            return "Stable"
        elif slope > 0:
            return "Increasing"
        else:
            return "Decreasing"
    
    def generate_insights(self, city: str) -> List[str]:
        """Generate actionable insights"""
        health_score = self.calculate_city_health_score(city)
        trends = self.analyze_trends(city)
        
        insights = []
        
        # Traffic insights
        if health_score['traffic_score'] < 60:
            insights.append(f"🚦 Traffic congestion is high in {city}. Consider promoting public transportation or implementing congestion pricing.")
        
        # Air quality insights
        if health_score['air_quality_score'] < 70:
            insights.append(f"🌫️ Air quality needs improvement in {city}. Focus on reducing emissions and promoting green transportation.")
        
        # Economic insights
        if health_score['economic_score'] < 65:
            insights.append(f"💼 Economic indicators suggest room for improvement in {city}. Consider business development initiatives.")
        
        # Sentiment insights
        if health_score['sentiment_score'] < 60:
            insights.append(f"😟 Social sentiment is below average in {city}. Engage with community concerns and improve public services.")
        
        # Trend-based insights
        if trends['traffic_trend'] == "Increasing":
            insights.append(f"📈 Traffic congestion is worsening in {city}. Immediate intervention may be needed.")
        
        if trends['air_quality_trend'] == "Increasing":
            insights.append(f"📈 Air pollution is increasing in {city}. Environmental policies should be prioritized.")
        
        # Positive insights
        if health_score['overall_score'] > 80:
            insights.append(f"🌟 {city} is performing excellently! Continue current policies and share best practices.")
        
        return insights if insights else [f"✅ {city} is maintaining good urban health metrics across all categories."]

def main():
    st.markdown('<h1 class="main-header">🏙️ Urban Pulse Analytics</h1>', unsafe_allow_html=True)
    st.markdown("**Real-time City Health Monitoring & Quality of Life Analytics**")
    
    analyzer = UrbanPulseAnalyzer()
    
    # Sidebar
    st.sidebar.title("🎛️ Control Panel")
    
    # City selection
    selected_city = st.sidebar.selectbox(
        "Select City for Analysis",
        analyzer.data_generator.cities,
        index=0
    )
    
    # Analysis type
    analysis_type = st.sidebar.radio(
        "Analysis Type",
        ["City Health Dashboard", "Comparative Analysis", "Trend Analysis", "Predictive Insights"]
    )
    
    if analysis_type == "City Health Dashboard":
        st.header(f"📊 {selected_city} Health Dashboard")
        
        # Calculate health scores
        health_data = analyzer.calculate_city_health_score(selected_city)
        
        # Display main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Overall Health</h3>
                <h1>{health_data['overall_score']}</h1>
                <p>Grade: {health_data['grade']}</p>
                <p>{health_data['status']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Traffic Flow</h3>
                <h1>{health_data['traffic_score']}</h1>
                <p>Mobility Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Air Quality</h3>
                <h1>{health_data['air_quality_score']}</h1>
                <p>Environmental Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Social Sentiment</h3>
                <h1>{health_data['sentiment_score']}</h1>
                <p>Community Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Alert system
        st.subheader("🚨 Alert System")
        
        if health_data['overall_score'] < 50:
            st.markdown(f"""
            <div class="alert-high">
                <h4>🔴 HIGH PRIORITY ALERT</h4>
                <p>{selected_city} requires immediate attention. Overall health score is critically low.</p>
            </div>
            """, unsafe_allow_html=True)
        elif health_data['overall_score'] < 70:
            st.markdown(f"""
            <div class="alert-medium">
                <h4>🟡 MEDIUM PRIORITY ALERT</h4>
                <p>{selected_city} shows concerning trends. Monitor closely and consider interventions.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-low">
                <h4>🟢 ALL SYSTEMS NORMAL</h4>
                <p>{selected_city} is maintaining healthy urban metrics.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed breakdown
        st.subheader("📈 Detailed Metrics")
        
        # Create radar chart for health scores
        categories = ['Traffic', 'Air Quality', 'Economic', 'Social Sentiment']
        scores = [
            health_data['traffic_score'],
            health_data['air_quality_score'],
            health_data['economic_score'],
            health_data['sentiment_score']
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name=selected_city,
            line_color='#2E86AB'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title=f"{selected_city} Health Score Breakdown"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Insights
        st.subheader("💡 AI-Generated Insights")
        insights = analyzer.generate_insights(selected_city)
        
        for insight in insights:
            st.markdown(f"""
            <div class="insight-box">
                {insight}
            </div>
            """, unsafe_allow_html=True)
    
    elif analysis_type == "Comparative Analysis":
        st.header("🔄 Multi-City Comparison")
        
        # Select cities for comparison
        comparison_cities = st.multiselect(
            "Select cities to compare (max 5)",
            analyzer.data_generator.cities,
            default=analyzer.data_generator.cities[:3],
            max_selections=5
        )
        
        if comparison_cities:
            # Calculate scores for all selected cities
            comparison_data = []
            for city in comparison_cities:
                health_data = analyzer.calculate_city_health_score(city)
                health_data['city'] = city
                comparison_data.append(health_data)
            
            df_comparison = pd.DataFrame(comparison_data)
            
            # Overall scores comparison
            fig_bar = px.bar(
                df_comparison,
                x='city',
                y='overall_score',
                color='overall_score',
                color_continuous_scale='RdYlGn',
                title="Overall City Health Scores",
                labels={'overall_score': 'Health Score', 'city': 'City'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Detailed comparison
            metrics = ['traffic_score', 'air_quality_score', 'economic_score', 'sentiment_score']
            metric_names = ['Traffic', 'Air Quality', 'Economic', 'Social Sentiment']
            
            fig_comparison = make_subplots(
                rows=2, cols=2,
                subplot_titles=metric_names,
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "bar"}]]
            )
            
            for i, (metric, name) in enumerate(zip(metrics, metric_names)):
                row = i // 2 + 1
                col = i % 2 + 1
                
                fig_comparison.add_trace(
                    go.Bar(x=df_comparison['city'], y=df_comparison[metric], name=name),
                    row=row, col=col
                )
            
            fig_comparison.update_layout(height=600, showlegend=False, title_text="Detailed Metrics Comparison")
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Rankings table
            st.subheader("🏆 City Rankings")
            rankings = df_comparison.sort_values('overall_score', ascending=False)[['city', 'overall_score', 'grade', 'status']]
            rankings['rank'] = range(1, len(rankings) + 1)
            rankings = rankings[['rank', 'city', 'overall_score', 'grade', 'status']]
            st.dataframe(rankings, use_container_width=True)
    
    elif analysis_type == "Trend Analysis":
        st.header(f"📈 {selected_city} Trend Analysis")
        
        trends_data = analyzer.analyze_trends(selected_city)
        
        # Traffic trends
        st.subheader("🚦 Traffic Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_traffic = px.line(
                trends_data['traffic_data'],
                x='timestamp',
                y='congestion_level',
                title="Daily Average Congestion Level",
                labels={'congestion_level': 'Congestion %', 'timestamp': 'Date'}
            )
            st.plotly_chart(fig_traffic, use_container_width=True)
        
        with col2:
            fig_speed = px.line(
                trends_data['traffic_data'],
                x='timestamp',
                y='avg_speed_mph',
                title="Average Traffic Speed",
                labels={'avg_speed_mph': 'Speed (mph)', 'timestamp': 'Date'}
            )
            st.plotly_chart(fig_speed, use_container_width=True)
        
        # Air quality trends
        st.subheader("🌫️ Air Quality Trends")
        
        fig_air = px.line(
            trends_data['air_data'],
            x='date',
            y='aqi',
            color='category',
            title="Air Quality Index Over Time",
            labels={'aqi': 'AQI', 'date': 'Date'}
        )
        st.plotly_chart(fig_air, use_container_width=True)
        
        # Economic trends
        st.subheader("💼 Economic Indicators")
        
        fig_economic = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Employment Rate', 'Business Activity'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig_economic.add_trace(
            go.Scatter(x=trends_data['economic_data']['date'], 
                      y=trends_data['economic_data']['employment_rate'],
                      name='Employment Rate'),
            row=1, col=1
        )
        
        fig_economic.add_trace(
            go.Scatter(x=trends_data['economic_data']['date'], 
                      y=trends_data['economic_data']['business_activity_score'],
                      name='Business Activity'),
            row=1, col=2
        )
        
        fig_economic.update_layout(height=400, title_text="Economic Trends")
        st.plotly_chart(fig_economic, use_container_width=True)
        
        # Trend summary
        st.subheader("📊 Trend Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            trend_color = "🔴" if trends_data['traffic_trend'] == "Increasing" else "🟢" if trends_data['traffic_trend'] == "Decreasing" else "🟡"
            st.metric("Traffic Congestion", trends_data['traffic_trend'], delta=None)
        
        with col2:
            trend_color = "🔴" if trends_data['air_quality_trend'] == "Increasing" else "🟢" if trends_data['air_quality_trend'] == "Decreasing" else "🟡"
            st.metric("Air Quality (AQI)", trends_data['air_quality_trend'], delta=None)
        
        with col3:
            trend_color = "🟢" if trends_data['employment_trend'] == "Increasing" else "🔴" if trends_data['employment_trend'] == "Decreasing" else "🟡"
            st.metric("Employment Rate", trends_data['employment_trend'], delta=None)
    
    elif analysis_type == "Predictive Insights":
        st.header(f"🔮 {selected_city} Predictive Analytics")
        
        st.info("🚧 This section demonstrates predictive modeling capabilities using historical patterns.")
        
        # Generate prediction data
        current_health = analyzer.calculate_city_health_score(selected_city)
        
        # Simulate predictions for next 7 days
        prediction_dates = [datetime.now().date() + timedelta(days=i) for i in range(1, 8)]
        
        # Simple prediction model (in real scenario, would use ML models)
        base_score = current_health['overall_score']
        predictions = []
        
        for i, date in enumerate(prediction_dates):
            # Add some trend and randomness
            trend_factor = random.uniform(-2, 2)
            seasonal_factor = random.uniform(-1, 1)
            predicted_score = max(0, min(100, base_score + trend_factor + seasonal_factor))
            
            predictions.append({
                'date': date,
                'predicted_score': round(predicted_score, 1),
                'confidence': round(random.uniform(0.7, 0.95), 2)
            })
        
        df_predictions = pd.DataFrame(predictions)
        
        # Prediction chart
        fig_pred = px.line(
            df_predictions,
            x='date',
            y='predicted_score',
            title=f"{selected_city} - 7-Day Health Score Forecast",
            labels={'predicted_score': 'Predicted Health Score', 'date': 'Date'}
        )
        
        # Add confidence bands
        fig_pred.add_trace(
            go.Scatter(
                x=df_predictions['date'],
                y=df_predictions['predicted_score'] + 5,
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False
            )
        )
        
        fig_pred.add_trace(
            go.Scatter(
                x=df_predictions['date'],
                y=df_predictions['predicted_score'] - 5,
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,0,0,0)',
                name='Confidence Band',
                fillcolor='rgba(46, 134, 171, 0.2)'
            )
        )
        
        st.plotly_chart(fig_pred, use_container_width=True)
        
        # Risk assessment
        st.subheader("⚠️ Risk Assessment")
        
        avg_predicted = df_predictions['predicted_score'].mean()
        
        if avg_predicted < 60:
            st.error(f"🔴 HIGH RISK: Predicted health score may drop to {avg_predicted:.1f}. Immediate intervention recommended.")
        elif avg_predicted < 75:
            st.warning(f"🟡 MEDIUM RISK: Predicted health score of {avg_predicted:.1f}. Monitor closely.")
        else:
            st.success(f"🟢 LOW RISK: Predicted health score of {avg_predicted:.1f}. Maintain current policies.")
        
        # Recommendations
        st.subheader("🎯 Recommended Actions")
        
        recommendations = [
            "📊 Increase monitoring frequency for early warning detection",
            "🚦 Implement dynamic traffic management during peak hours",
            "🌱 Expand green infrastructure to improve air quality",
            "💬 Enhance community engagement programs",
            "📱 Deploy smart city sensors for real-time data collection"
        ]
        
        for rec in recommendations:
            st.write(f"• {rec}")
    
    # Footer
    st.markdown("---")
    st.markdown("**Urban Pulse Analytics** - Powered by Advanced Data Science & AI")
    st.markdown("*Real-time insights for smarter cities*")

if __name__ == "__main__":
    main()