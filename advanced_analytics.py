import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from collections import Counter
import numpy as np

def create_network_analysis(activity_df):
    """Create network analysis of clubs with similar activities"""
    if activity_df.empty:
        return None
    
    # Create club-activity matrix
    club_activities = activity_df.groupby('Club_Name')['Activity'].apply(list).to_dict()
    
    # Find clubs with similar activities
    similar_clubs = []
    clubs = list(club_activities.keys())
    
    for i, club1 in enumerate(clubs):
        for club2 in clubs[i+1:]:
            activities1 = set(club_activities[club1])
            activities2 = set(club_activities[club2])
            common = activities1.intersection(activities2)
            
            if len(common) >= 2:  # At least 2 common activities
                similar_clubs.append({
                    'Club1': club1,
                    'Club2': club2,
                    'Common_Activities': len(common),
                    'Activities': ', '.join(list(common)[:3])
                })
    
    return pd.DataFrame(similar_clubs).sort_values('Common_Activities', ascending=False)

def create_activity_correlation_matrix(activity_df):
    """Create correlation matrix of activities"""
    if activity_df.empty:
        return None
    
    # Create pivot table
    activity_pivot = activity_df.pivot_table(
        index='Club_Name', 
        columns='Activity', 
        aggfunc='size', 
        fill_value=0
    )
    
    # Calculate correlation
    correlation_matrix = activity_pivot.corr()
    
    # Create heatmap
    fig = px.imshow(
        correlation_matrix,
        title="🔥 Activity Correlation Heatmap",
        labels={'color': 'Correlation'},
        aspect='auto'
    )
    
    fig.update_layout(
        height=600,
        title_font_size=18
    )
    
    return fig

def show_advanced_analytics():
    """Show advanced analytics page"""
    st.title("🔬 Advanced Club Analytics")
    
    # This would connect to your main data processing
    st.write("Advanced analytics features coming soon!")
    
    # You can add more sophisticated analyses here
    st.markdown("""
    ### Available Advanced Features:
    - **Network Analysis**: Find clubs with similar activities
    - **Trend Analysis**: Activity popularity over time
    - **Clustering**: Group similar organizations
    - **Predictive Modeling**: Suggest new activities for clubs
    """)
