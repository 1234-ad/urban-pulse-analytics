"""
Advanced Visualization Module for Urban Pulse Analytics
Creates interactive charts and dashboards for urban data analysis
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import streamlit as st

class UrbanVisualizationEngine:
    """Advanced visualization engine for urban analytics"""
    
    def __init__(self):
        self.color_palette = [
            '#2E86AB', '#A23B72', '#F18F01', '#C73E1D', 
            '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'
        ]
        
        self.theme_config = {
            'layout': {
                'font_family': 'Arial, sans-serif',
                'font_size': 12,
                'title_font_size': 16,
                'paper_bgcolor': 'white',
                'plot_bgcolor': 'white'
            }
        }
    
    def create_city_health_radar(self, city_scores: Dict, title: str = None) -> go.Figure:
        """Create radar chart for city health metrics"""
        
        categories = ['Traffic Flow', 'Air Quality', 'Economic Health', 'Social Sentiment']
        values = [
            city_scores.get('traffic_score', 0),
            city_scores.get('air_quality_score', 0),
            city_scores.get('economic_score', 0),
            city_scores.get('sentiment_score', 0)
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=city_scores.get('city', 'City'),
            line_color=self.color_palette[0],
            fillcolor=f'rgba(46, 134, 171, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickmode='linear',
                    tick0=0,
                    dtick=20
                )
            ),
            showlegend=True,
            title=title or f"{city_scores.get('city', 'City')} Health Metrics",
            font=dict(size=12)
        )
        
        return fig
    
    def create_multi_city_comparison(self, cities_data: List[Dict]) -> go.Figure:
        """Create comprehensive multi-city comparison chart"""
        
        cities = [city['city'] for city in cities_data]
        metrics = ['traffic_score', 'air_quality_score', 'economic_score', 'sentiment_score']
        metric_names = ['Traffic', 'Air Quality', 'Economic', 'Social Sentiment']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=metric_names,
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        for i, (metric, name) in enumerate(zip(metrics, metric_names)):
            row = i // 2 + 1
            col = i % 2 + 1
            
            values = [city.get(metric, 0) for city in cities_data]
            
            fig.add_trace(
                go.Bar(
                    x=cities,
                    y=values,
                    name=name,
                    marker_color=self.color_palette[i],
                    showlegend=False
                ),
                row=row, col=col
            )
            
            # Add target line at 70 (good threshold)
            fig.add_hline(
                y=70, line_dash="dash", line_color="red", 
                opacity=0.5, row=row, col=col
            )
        
        fig.update_layout(
            height=600,
            title_text="Multi-City Performance Comparison",
            showlegend=False
        )
        
        # Update y-axes to have consistent range
        for i in range(1, 5):
            fig.update_yaxes(range=[0, 100], row=(i-1)//2 + 1, col=(i-1)%2 + 1)
        
        return fig
    
    def create_traffic_heatmap(self, traffic_data: pd.DataFrame) -> go.Figure:
        """Create traffic congestion heatmap by hour and day"""
        
        # Prepare data for heatmap
        traffic_data['hour'] = pd.to_datetime(traffic_data['timestamp']).dt.hour
        traffic_data['day_name'] = pd.to_datetime(traffic_data['timestamp']).dt.day_name()
        
        # Create pivot table
        heatmap_data = traffic_data.pivot_table(
            values='congestion_level',
            index='day_name',
            columns='hour',
            aggfunc='mean'
        )
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(day_order)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlGn_r',
            colorbar=dict(title="Congestion Level (%)"),
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Traffic Congestion Patterns by Hour and Day',
            xaxis_title='Hour of Day',
            yaxis_title='Day of Week',
            height=400
        )
        
        return fig
    
    def create_air_quality_timeline(self, air_data: pd.DataFrame) -> go.Figure:
        """Create air quality timeline with category coloring"""
        
        # Color mapping for AQI categories
        category_colors = {
            'Good': '#00E400',
            'Moderate': '#FFFF00',
            'Unhealthy for Sensitive': '#FF7E00',
            'Unhealthy': '#FF0000',
            'Very Unhealthy': '#8F3F97',
            'Hazardous': '#7E0023'
        }
        
        fig = go.Figure()
        
        # Group by city if multiple cities
        if 'city' in air_data.columns:
            for city in air_data['city'].unique():
                city_data = air_data[air_data['city'] == city]
                
                fig.add_trace(go.Scatter(
                    x=city_data['date'],
                    y=city_data['aqi'],
                    mode='lines+markers',
                    name=city,
                    line=dict(width=2),
                    marker=dict(size=6)
                ))
        else:
            fig.add_trace(go.Scatter(
                x=air_data['date'],
                y=air_data['aqi'],
                mode='lines+markers',
                name='AQI',
                line=dict(width=2, color=self.color_palette[0]),
                marker=dict(size=6)
            ))
        
        # Add AQI category reference lines
        fig.add_hline(y=50, line_dash="dash", line_color="green", 
                     annotation_text="Good", annotation_position="right")
        fig.add_hline(y=100, line_dash="dash", line_color="yellow", 
                     annotation_text="Moderate", annotation_position="right")
        fig.add_hline(y=150, line_dash="dash", line_color="orange", 
                     annotation_text="Unhealthy for Sensitive", annotation_position="right")
        
        fig.update_layout(
            title='Air Quality Index Over Time',
            xaxis_title='Date',
            yaxis_title='AQI',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_economic_indicators_dashboard(self, economic_data: pd.DataFrame) -> go.Figure:
        """Create comprehensive economic indicators dashboard"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Employment Rate Trend',
                'Housing Affordability Index',
                'Business Activity Score',
                'Economic Health Correlation'
            ],
            specs=[[{"type": "scatter"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Employment rate trend
        fig.add_trace(
            go.Scatter(
                x=economic_data['date'],
                y=economic_data['employment_rate'],
                mode='lines+markers',
                name='Employment Rate',
                line=dict(color=self.color_palette[0])
            ),
            row=1, col=1
        )
        
        # Housing affordability
        fig.add_trace(
            go.Scatter(
                x=economic_data['date'],
                y=economic_data['housing_affordability_index'],
                mode='lines+markers',
                name='Housing Affordability',
                line=dict(color=self.color_palette[1])
            ),
            row=1, col=2
        )
        
        # Business activity
        fig.add_trace(
            go.Scatter(
                x=economic_data['date'],
                y=economic_data['business_activity_score'],
                mode='lines+markers',
                name='Business Activity',
                line=dict(color=self.color_palette[2])
            ),
            row=2, col=1
        )
        
        # Correlation scatter plot
        fig.add_trace(
            go.Scatter(
                x=economic_data['employment_rate'],
                y=economic_data['business_activity_score'],
                mode='markers',
                name='Employment vs Business',
                marker=dict(
                    color=self.color_palette[3],
                    size=8,
                    opacity=0.7
                )
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            title_text="Economic Indicators Dashboard",
            showlegend=False
        )
        
        return fig
    
    def create_sentiment_analysis_chart(self, sentiment_data: pd.DataFrame) -> go.Figure:
        """Create sentiment analysis visualization"""
        
        # Aggregate sentiment by topic
        topic_sentiment = sentiment_data.groupby('topic').agg({
            'sentiment_score': 'mean',
            'mention_volume': 'sum'
        }).reset_index()
        
        # Create bubble chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=topic_sentiment['topic'],
            y=topic_sentiment['sentiment_score'],
            mode='markers',
            marker=dict(
                size=topic_sentiment['mention_volume'] / 10,  # Scale bubble size
                color=topic_sentiment['sentiment_score'],
                colorscale='RdYlGn',
                colorbar=dict(title="Sentiment Score"),
                sizemode='diameter',
                sizemin=10,
                sizemax=50,
                line=dict(width=2, color='white')
            ),
            text=topic_sentiment['topic'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Sentiment: %{y:.3f}<br>' +
                         'Volume: %{marker.size}<br>' +
                         '<extra></extra>'
        ))
        
        # Add neutral line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                     annotation_text="Neutral", annotation_position="right")
        
        fig.update_layout(
            title='Social Sentiment Analysis by Topic',
            xaxis_title='Topic',
            yaxis_title='Average Sentiment Score',
            height=400,
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_predictive_forecast_chart(self, historical_data: pd.DataFrame, 
                                       predictions: pd.DataFrame) -> go.Figure:
        """Create predictive forecast visualization"""
        
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=historical_data['date'],
            y=historical_data['value'],
            mode='lines+markers',
            name='Historical Data',
            line=dict(color=self.color_palette[0], width=2)
        ))
        
        # Predictions
        fig.add_trace(go.Scatter(
            x=predictions['date'],
            y=predictions['predicted_value'],
            mode='lines+markers',
            name='Predictions',
            line=dict(color=self.color_palette[1], width=2, dash='dash')
        ))
        
        # Confidence intervals
        if 'confidence_upper' in predictions.columns and 'confidence_lower' in predictions.columns:
            fig.add_trace(go.Scatter(
                x=predictions['date'],
                y=predictions['confidence_upper'],
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=predictions['date'],
                y=predictions['confidence_lower'],
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,0,0,0)',
                name='Confidence Interval',
                fillcolor='rgba(46, 134, 171, 0.2)'
            ))
        
        fig.update_layout(
            title='Predictive Forecast with Confidence Intervals',
            xaxis_title='Date',
            yaxis_title='Value',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_anomaly_detection_chart(self, data: pd.DataFrame, 
                                     anomaly_column: str = 'is_anomaly') -> go.Figure:
        """Create anomaly detection visualization"""
        
        fig = go.Figure()
        
        # Normal data points
        normal_data = data[~data[anomaly_column]]
        fig.add_trace(go.Scatter(
            x=normal_data.index,
            y=normal_data['value'],
            mode='markers',
            name='Normal',
            marker=dict(color=self.color_palette[0], size=6)
        ))
        
        # Anomalous data points
        anomaly_data = data[data[anomaly_column]]
        fig.add_trace(go.Scatter(
            x=anomaly_data.index,
            y=anomaly_data['value'],
            mode='markers',
            name='Anomaly',
            marker=dict(color='red', size=10, symbol='x')
        ))
        
        fig.update_layout(
            title='Anomaly Detection Results',
            xaxis_title='Time',
            yaxis_title='Value',
            height=400
        )
        
        return fig
    
    def create_correlation_heatmap(self, correlation_matrix: pd.DataFrame) -> go.Figure:
        """Create correlation heatmap for urban metrics"""
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='RdBu',
            zmid=0,
            colorbar=dict(title="Correlation Coefficient"),
            text=correlation_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Urban Metrics Correlation Matrix',
            height=500,
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_city_clustering_visualization(self, clustering_results: Dict) -> go.Figure:
        """Create city clustering visualization using PCA"""
        
        fig = go.Figure()
        
        cities = clustering_results['cities']
        pca_coords = clustering_results['pca_coordinates']
        cluster_labels = clustering_results['cluster_labels']
        
        # Create scatter plot for each cluster
        unique_clusters = list(set(cluster_labels))
        
        for cluster_id in unique_clusters:
            cluster_indices = [i for i, label in enumerate(cluster_labels) if label == cluster_id]
            cluster_cities = [cities[i] for i in cluster_indices]
            cluster_coords = [pca_coords[i] for i in cluster_indices]
            
            fig.add_trace(go.Scatter(
                x=[coord[0] for coord in cluster_coords],
                y=[coord[1] for coord in cluster_coords],
                mode='markers+text',
                name=f'Cluster {cluster_id + 1}',
                text=cluster_cities,
                textposition='top center',
                marker=dict(
                    color=self.color_palette[cluster_id % len(self.color_palette)],
                    size=12,
                    line=dict(width=2, color='white')
                )
            ))
        
        fig.update_layout(
            title='City Clustering Analysis (PCA Visualization)',
            xaxis_title=f'PC1 ({clustering_results["explained_variance_ratio"][0]:.1%} variance)',
            yaxis_title=f'PC2 ({clustering_results["explained_variance_ratio"][1]:.1%} variance)',
            height=500
        )
        
        return fig
    
    def create_kpi_dashboard(self, kpi_data: Dict) -> go.Figure:
        """Create KPI dashboard with gauge charts"""
        
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]],
            subplot_titles=['Overall Health', 'Traffic Flow', 'Air Quality', 'Economic Health']
        )
        
        # Overall Health Score
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=kpi_data.get('overall_score', 0),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Health"},
            delta={'reference': 70},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': self.color_palette[0]},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ), row=1, col=1)
        
        # Traffic Score
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=kpi_data.get('traffic_score', 0),
            title={'text': "Traffic Flow"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': self.color_palette[1]},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ]
            }
        ), row=1, col=2)
        
        # Air Quality Score
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=kpi_data.get('air_quality_score', 0),
            title={'text': "Air Quality"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': self.color_palette[2]},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ]
            }
        ), row=2, col=1)
        
        # Economic Score
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=kpi_data.get('economic_score', 0),
            title={'text': "Economic Health"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': self.color_palette[3]},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ]
            }
        ), row=2, col=2)
        
        fig.update_layout(height=600, title_text="Urban Health KPI Dashboard")
        
        return fig