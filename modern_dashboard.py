import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
import warnings
import time
import os

warnings.filterwarnings('ignore')

# ========================================
# PAGE CONFIGURATION
# ========================================

st.set_page_config(
    page_title="🎓 UCSB Clubs Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# SIMPLE PROFESSIONAL CSS STYLING
# ========================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Clean, modern base */
    .stApp {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main .block-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 1rem;
        border: 1px solid #e1e5e9;
    }
    
    /* Professional header */
    .main-title {
        font-family: 'Inter', sans-serif !important;
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        color: #2c3e50 !important;
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        text-align: center;
        color: #7f8c8d !important;
        margin-bottom: 2rem;
        font-weight: 400 !important;
    }
    
    /* Professional metric cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-number {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        color: white !important;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.9rem !important;
        margin: 0.5rem 0 0 0 !important;
        color: #f8f9fa !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        margin: 2rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #e1e5e9 !important;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: #667eea;
    }
    
    /* Professional cards */
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .info-card h4 {
        color: #2c3e50 !important;
        margin: 0 0 0.8rem 0 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    .info-card p {
        color: #5a6c7d !important;
        margin: 0 !important;
        line-height: 1.6 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Top clubs styling */
    .top-club-item {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
        margin: 0.8rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        border: 1px solid #f0f1f2;
    }
    
    .top-club-item:hover {
        transform: translateX(8px);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
        border-left-color: #5a67d8;
    }
    
    .club-rank {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-right: 1rem;
    }
    
    .club-name {
        font-weight: 600;
        color: #2c3e50;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }
    
    .club-details {
        color: #7f8c8d;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Status indicator */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.4rem 0.8rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        border: 1px solid #e1e5e9 !important;
        background: white !important;
        color: #2c3e50 !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        border-color: #667eea !important;
        color: #667eea !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Sidebar styling */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 1px solid #e1e5e9;
    }
    
    div[data-testid="stSidebar"] h2 {
        color: #2c3e50 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        background: transparent;
        border-radius: 8px;
        transition: all 0.3s ease;
        color: #5a6c7d;
        border: 1px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #667eea !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        border-color: #e1e5e9 !important;
    }
    
    /* Table styling */
    .stDataFrame {
        font-family: 'Inter', sans-serif !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Input styling */
    .stSelectbox label, .stTextInput label, .stSlider label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #2c3e50 !important;
    }
    
    /* Professional footer */
    .footer {
        text-align: center;
        color: #7f8c8d;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #e1e5e9;
        font-family: 'Inter', sans-serif;
        background: #f8f9fa;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# DATA LOADING FUNCTIONS
# ========================================

@st.cache_data(ttl=60)
def load_data():
    """Load data with enhanced error handling"""
    try:
        file_path = 'clubs_ucsb.xlsx'
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            df = pd.read_excel(file_path, sheet_name='clubs_ucsb')
            df = df.dropna(subset=['Club Name'])
            df['Club Name'] = df['Club Name'].astype(str)
            df['Description'] = df['Description'].fillna('No description')
            return df, "real"
        else:
            raise FileNotFoundError("Excel file not found")
    except Exception:
        return create_enhanced_sample_data(), "demo"

def create_enhanced_sample_data():
    """Create comprehensive sample data"""
    np.random.seed(int(time.time() / 30) % 2**32)
    
    activities_pool = [
        'Leadership Development', 'Community Service', 'Cultural Events', 'Academic Research',
        'Professional Networking', 'Sports & Recreation', 'Arts & Performance', 'Technology',
        'Environmental Action', 'Social Justice', 'Career Development', 'Innovation',
        'Music & Arts', 'Public Speaking', 'Volunteer Work', 'Entrepreneurship',
        'Health & Wellness', 'International Relations', 'Media & Communications', 'Education'
    ]
    
    org_types = {
        'Registered Campus Organization': 0.55,
        'Department': 0.15,
        'Associated Students': 0.08,
        'Social Fraternity/Sorority': 0.1,
        'Faculty/Staff-Only Group': 0.06,
        'Graduate Student-Only Group': 0.04,
        'Sport Club': 0.02
    }
    
    club_names = [
        "Data Science UCSB", "Environmental Coalition", "Chess Club", "Photography Society",
        "Debate Union", "Hiking Adventure Club", "Music Collective", "Theater Guild",
        "Robotics Club", "Cultural Association", "Student Government", "Greek Council",
        "Volunteer Corps", "Business Society", "Engineering United", "Film & Media Club",
        "Culinary Club", "Pre-Health Society", "Dance Company", "Gaming Alliance"
    ]
    
    sample_data = []
    for i in range(100):
        org_type = np.random.choice(list(org_types.keys()), p=list(org_types.values()))
        num_activities = max(1, min(5, int(np.random.normal(3, 1))))
        selected_activities = np.random.choice(activities_pool, size=min(num_activities, len(activities_pool)), replace=False)
        
        description = f"{org_type}\n" + "\n".join([f"- {activity}" for activity in selected_activities])
        
        # Generate realistic club name
        if i < len(club_names):
            club_name = club_names[i]
        else:
            club_name = f"{np.random.choice(club_names)} {i+1}"
        
        sample_data.append({
            'Index': i + 1,
            'Club Name': club_name,
            'Description': description
        })
    
    return pd.DataFrame(sample_data)

@st.cache_data
def process_club_data(df):
    """Process and enhance club data"""
    
    def extract_main_category(desc):
        if pd.isna(desc) or desc == 'No description':
            return 'Unknown'
        lines = str(desc).split('\n')
        return lines[0].strip() if lines else 'Unknown'
    
    def extract_activities(desc):
        if pd.isna(desc) or desc == 'No description':
            return []
        activities = re.findall(r'- ([^,\n]+)', str(desc))
        return [activity.strip() for activity in activities if activity.strip()]
    
    def categorize_organization_type(main_cat):
        """Enhanced categorization with icons"""
        if 'Registered Campus Organization' in main_cat:
            return '🎓 Student Organizations'
        elif 'Department' in main_cat:
            return '📚 Academic Departments'
        elif 'Associated Students' in main_cat:
            return '🏛️ Student Government'
        elif 'Social Fraternity/Sorority' in main_cat:
            return '🏛️ Greek Life'
        elif 'Faculty/Staff-Only Group' in main_cat:
            return '👥 Faculty/Staff Groups'
        elif 'Graduate Student-Only Group' in main_cat:
            return '🎓 Graduate Groups'
        elif 'Sport Club' in main_cat:
            return '⚽ Sports Clubs'
        else:
            return '📋 Other Organizations'
    
    # Apply data processing
    df['Main_Category'] = df['Description'].apply(extract_main_category)
    df['Activities'] = df['Description'].apply(extract_activities)
    df['Organization_Type'] = df['Main_Category'].apply(categorize_organization_type)
    df['Activity_Count'] = df['Activities'].apply(len)
    
    # Generate realistic performance metrics
    np.random.seed(42)
    
    # Performance score based on beta distribution
    df['Performance_Score'] = np.random.beta(2.5, 2, len(df)) * 100
    df['Performance_Score'] = np.clip(df['Performance_Score'], 20, 100)
    
    # Member count with realistic distribution
    df['Member_Count'] = np.random.lognormal(3.2, 0.6, len(df)).astype(int)
    df['Member_Count'] = np.clip(df['Member_Count'], 8, 180)
    
    # Budget allocation
    df['Annual_Budget'] = np.random.lognormal(8.5, 0.7, len(df)).astype(int)
    df['Annual_Budget'] = np.clip(df['Annual_Budget'], 2000, 35000)
    
    # Events and participation
    df['Events_Per_Year'] = np.random.poisson(10, len(df)) + 3
    df['Participation_Rate'] = np.random.beta(3, 1.5, len(df)) * 100
    df['Participation_Rate'] = np.clip(df['Participation_Rate'], 65, 98)
    
    # Engagement metrics
    df['Engagement_Score'] = (df['Performance_Score'] * 0.4 + 
                             df['Participation_Rate'] * 0.3 + 
                             np.random.normal(30, 10, len(df)) * 0.3)
    df['Engagement_Score'] = np.clip(df['Engagement_Score'], 40, 100)
    
    # Status based on performance
    df['Status'] = pd.cut(df['Performance_Score'], 
                         bins=[0, 60, 80, 100], 
                         labels=['Developing', 'Active', 'Highly Active'])
    
    # Calculate efficiency metrics
    df['Budget_Efficiency'] = df['Performance_Score'] / (df['Annual_Budget'] / 1000)
    df['Member_Engagement'] = df['Engagement_Score'] / df['Member_Count']
    
    return df

# ========================================
# VISUALIZATION FUNCTIONS
# ========================================

def create_performance_overview(df):
    """Create professional performance overview"""
    
    # Performance distribution
    fig_dist = px.histogram(
        df, x='Performance_Score', nbins=15,
        title="📊 Performance Score Distribution",
        color_discrete_sequence=['#667eea'],
        labels={'Performance_Score': 'Performance Score', 'count': 'Number of Clubs'}
    )
    
    fig_dist.update_layout(
        height=350,
        title_font_size=16,
        font_family="Inter",
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(gridcolor='#f0f1f2', gridwidth=1),
        yaxis=dict(gridcolor='#f0f1f2', gridwidth=1)
    )
    
    # Add average line
    avg_score = df['Performance_Score'].mean()
    fig_dist.add_vline(x=avg_score, line_dash="dash", line_color="#e74c3c",
                       annotation_text=f"Average: {avg_score:.1f}")
    
    return fig_dist

def create_organization_charts(df):
    """Create organization type analysis charts"""
    
    org_counts = df['Organization_Type'].value_counts()
    
    # Horizontal bar chart
    fig_bar = px.bar(
        x=org_counts.values,
        y=org_counts.index,
        orientation='h',
        title="🏢 Organizations by Type",
        color=org_counts.values,
        color_continuous_scale='Blues',
        text=org_counts.values
    )
    
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
    fig_bar.update_layout(
        height=400,
        showlegend=False,
        title_font_size=16,
        font_family="Inter",
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(gridcolor='#f0f1f2', gridwidth=1, title="Number of Clubs"),
        yaxis=dict(gridcolor='#f0f1f2', gridwidth=1, title="")
    )
    
    # Donut chart
    fig_donut = px.pie(
        values=org_counts.values,
        names=org_counts.index,
        title="🥧 Organization Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    
    fig_donut.update_layout(
        height=400,
        title_font_size=16,
        font_family="Inter"
    )
    
    return fig_bar, fig_donut

def create_performance_analysis(df):
    """Create performance vs metrics analysis"""
    
    # Performance vs Budget scatter
    fig_scatter = px.scatter(
        df, 
        x='Annual_Budget', 
        y='Performance_Score',
        size='Member_Count',
        color='Organization_Type',
        hover_name='Club Name',
        title="💰 Performance vs Budget Analysis",
        labels={'Annual_Budget': 'Annual Budget ($)', 'Performance_Score': 'Performance Score'},
        size_max=15
    )
    
    fig_scatter.update_layout(
        height=450,
        title_font_size=16,
        font_family="Inter",
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(gridcolor='#f0f1f2', gridwidth=1),
        yaxis=dict(gridcolor='#f0f1f2', gridwidth=1)
    )
    
    return fig_scatter

# ========================================
# MAIN DASHBOARD FUNCTION
# ========================================

def main():
    """Main professional dashboard"""
    
    # Professional Header
    st.markdown('<h1 class="main-title">🎓 UCSB Clubs Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Professional Performance Analytics for UC Santa Barbara Student Organizations</p>', 
                unsafe_allow_html=True)
    
    # Status bar
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**📊 Dashboard Status:** Last updated {current_time}")
    with col2:
        st.markdown('<span class="status-badge">🔴 Live Data</span>', unsafe_allow_html=True)
    with col3:
        st.markdown('<span class="status-badge">📈 Analytics</span>', unsafe_allow_html=True)
    
    # Control Panel
    st.markdown("### 🎛️ Dashboard Controls")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        refresh_data = st.button("🔄 Refresh Data", type="primary")
    with col2:
        auto_refresh = st.checkbox("⚡ Auto Update", value=False)
    with col3:
        show_advanced = st.checkbox("🔬 Advanced Mode", value=True)
    with col4:
        export_mode = st.checkbox("📊 Export Options", value=False)
    
    # Handle refresh
    if refresh_data:
        st.cache_data.clear()
        try:
            if hasattr(st, 'rerun'):
                st.rerun()
            else:
                st.experimental_rerun()
        except Exception:
            st.success("✅ Data refreshed successfully!")
    
    # Load and process data
    try:
        with st.spinner('📊 Loading analytics data...'):
            df, data_type = load_data()
            df = process_club_data(df)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # ========================================
    # SIDEBAR FILTERS
    # ========================================
    
    st.sidebar.markdown("## 🎛️ Analytics Filters")
    
    # Organization type filter
    org_types = ['All Organizations'] + sorted(df['Organization_Type'].unique())
    selected_org = st.sidebar.selectbox("🏢 Organization Type", org_types)
    
    # Performance filter
    st.sidebar.markdown("### 📈 Performance Filters")
    performance_range = st.sidebar.slider("Performance Score Range", 0.0, 100.0, (0.0, 100.0))
    
    # Budget filter
    budget_min = int(df['Annual_Budget'].min())
    budget_max = int(df['Annual_Budget'].max())
    budget_range = st.sidebar.slider("Annual Budget Range ($)", budget_min, budget_max, (budget_min, budget_max))
    
    # Member count filter
    member_min = int(df['Member_Count'].min())
    member_max = int(df['Member_Count'].max())
    member_range = st.sidebar.slider("Member Count Range", member_min, member_max, (member_min, member_max))
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_org != 'All Organizations':
        filtered_df = filtered_df[filtered_df['Organization_Type'] == selected_org]
    
    filtered_df = filtered_df[
        (filtered_df['Performance_Score'] >= performance_range[0]) &
        (filtered_df['Performance_Score'] <= performance_range[1]) &
        (filtered_df['Annual_Budget'] >= budget_range[0]) &
        (filtered_df['Annual_Budget'] <= budget_range[1]) &
        (filtered_df['Member_Count'] >= member_range[0]) &
        (filtered_df['Member_Count'] <= member_range[1])
    ]
    
    if filtered_df.empty:
        st.warning("⚠️ No clubs match your current filters. Please adjust your criteria.")
        return
    
    # ========================================
    # KEY METRICS DASHBOARD
    # ========================================
    
    st.markdown('<div class="section-header">📊 Executive Summary</div>', unsafe_allow_html=True)
    
    # Calculate key metrics
    total_clubs = len(filtered_df)
    avg_performance = filtered_df['Performance_Score'].mean()
    total_budget = filtered_df['Annual_Budget'].sum()
    total_members = filtered_df['Member_Count'].sum()
    avg_engagement = filtered_df['Engagement_Score'].mean()
    
    # Display metrics in grid
    metrics_html = f"""
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-icon">🎓</div>
            <div class="metric-number">{total_clubs}</div>
            <div class="metric-label">Total Clubs</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">⭐</div>
            <div class="metric-number">{avg_performance:.1f}</div>
            <div class="metric-label">Avg Performance</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-number">${total_budget:,.0f}</div>
            <div class="metric-label">Total Budget</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-number">{total_members:,}</div>
            <div class="metric-label">Total Members</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🔥</div>
            <div class="metric-number">{avg_engagement:.1f}</div>
            <div class="metric-label">Avg Engagement</div>
        </div>
    </div>
    """
    
    st.markdown(metrics_html, unsafe_allow_html=True)
    
    # ========================================
    # TOP 10 CLUBS SECTION
    # ========================================
    
    st.markdown('<div class="section-header">🏆 Top 10 Performing Clubs</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        ranking_criteria = st.selectbox(
            "**Rank by:**",
            ['Performance_Score', 'Engagement_Score', 'Member_Count', 'Annual_Budget', 'Budget_Efficiency'],
            format_func=lambda x: {
                'Performance_Score': '⭐ Performance',
                'Engagement_Score': '🔥 Engagement', 
                'Member_Count': '👥 Members',
                'Annual_Budget': '💰 Budget',
                'Budget_Efficiency': '⚡ Efficiency'
            }[x]
        )
    
    # Get top 10 clubs
    top_clubs = filtered_df.nlargest(10, ranking_criteria)
    
    with col1:
        # Display top clubs with professional styling
        for idx, (_, club) in enumerate(top_clubs.iterrows(), 1):
            # Rank emoji
            if idx == 1:
                rank_display = "🥇"
            elif idx == 2:
                rank_display = "🥈"
            elif idx == 3:
                rank_display = "🥉"
            else:
                rank_display = f"#{idx}"
            
            # Format value based on criteria
            value = club[ranking_criteria]
            if ranking_criteria == 'Annual_Budget':
                value_display = f"${value:,.0f}"
            elif ranking_criteria in ['Performance_Score', 'Engagement_Score', 'Budget_Efficiency']:
                value_display = f"{value:.1f}"
            else:
                value_display = f"{int(value)}"
            
            # Activities summary
            activities_text = ", ".join(club['Activities'][:2]) if len(club['Activities']) > 0 else "Various"
            if len(club['Activities']) > 2:
                activities_text += f" +{len(club['Activities'])-2} more"
            
            st.markdown(f"""
            <div class="top-club-item">
                <div style="display: flex; align-items: center;">
                    <span class="club-rank">{rank_display}</span>
                    <div style="flex: 1;">
                        <div class="club-name">{club['Club Name']}</div>
                        <div class="club-details">
                            {club['Organization_Type']} • {ranking_criteria.replace('_', ' ')}: {value_display}<br>
                            Members: {club['Member_Count']} • Activities: {activities_text}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================
    # ANALYTICS VISUALIZATIONS
    # ========================================
    
    st.markdown('<div class="section-header">📈 Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏢 Organizations", "💰 Performance", "📋 Data Explorer"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance distribution
            fig_dist = create_performance_overview(filtered_df)
            st.plotly_chart(fig_dist, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Key insights
            st.markdown("### 💡 Key Insights")
            
            high_performers = len(filtered_df[filtered_df['Performance_Score'] > 80])
            avg_budget_per_member = filtered_df['Annual_Budget'].sum() / filtered_df['Member_Count'].sum()
            most_efficient = filtered_df.loc[filtered_df['Budget_Efficiency'].idxmax()]
            
            st.markdown(f"""
            <div class="info-card">
                <h4>🎯 Performance Highlights</h4>
                <p>
                • <strong>{high_performers} clubs</strong> have performance scores above 80<br>
                • Average budget per member: <strong>${avg_budget_per_member:.0f}</strong><br>
                • Most efficient club: <strong>{most_efficient['Club Name']}</strong><br>
                • Total organizations analyzed: <strong>{len(filtered_df)}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Category breakdown
            category_summary = filtered_df['Organization_Type'].value_counts()
            top_category = category_summary.index[0]
            
            st.markdown(f"""
            <div class="info-card">
                <h4>📊 Category Analysis</h4>
                <p>
                • <strong>{top_category}</strong> is the largest category<br>
                • <strong>{len(category_summary)} different</strong> organization types<br>
                • Average performance: <strong>{avg_performance:.1f}/100</strong><br>
                • Total annual budget: <strong>${total_budget:,.0f}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        fig_bar, fig_donut = create_organization_charts(filtered_df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        with col2:
            st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        
        # Organization performance table
        st.markdown("### 📋 Organization Performance Summary")
        
        org_summary = filtered_df.groupby('Organization_Type').agg({
            'Club Name': 'count',
            'Performance_Score': 'mean',
            'Annual_Budget': 'sum',
            'Member_Count': 'sum',
            'Engagement_Score': 'mean'
        }).round(1)
        
        org_summary.columns = ['Clubs', 'Avg Performance', 'Total Budget', 'Total Members', 'Avg Engagement']
        org_summary['Total Budget'] = org_summary['Total Budget'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(org_summary, use_container_width=True)
    
    with tab3:
        if show_advanced:
            fig_scatter = create_performance_analysis(filtered_df)
            st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})
            
            # Performance correlation analysis
            col1, col2 = st.columns(2)
            
            with col1:
                # Budget efficiency chart
                top_efficient = filtered_df.nlargest(10, 'Budget_Efficiency')
                
                fig_efficiency = px.bar(
                    top_efficient,
                    x='Budget_Efficiency',
                    y='Club Name',
                    orientation='h',
                    title="⚡ Top 10 Most Efficient Clubs",
                    color='Budget_Efficiency',
                    color_continuous_scale='Greens'
                )
                
                fig_efficiency.update_layout(
                    height=400,
                    title_font_size=14,
                    font_family="Inter",
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                st.plotly_chart(fig_efficiency, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                # Engagement vs Performance
                fig_engagement = px.scatter(
                    filtered_df,
                    x='Performance_Score',
                    y='Engagement_Score',
                    color='Organization_Type',
                    title="🔥 Performance vs Engagement",
                    hover_name='Club Name'
                )
                
                fig_engagement.update_layout(
                    height=400,
                    title_font_size=14,
                    font_family="Inter",
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                st.plotly_chart(fig_engagement, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("💡 Enable Advanced Mode in the controls to view detailed performance analysis.")
    
    with tab4:
        st.markdown("### 🔍 Interactive Data Explorer")
        
        # Search and sort controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Search Clubs", placeholder="Enter club name...")
        
        with col2:
            sort_column = st.selectbox("📊 Sort by", 
                                     ['Performance_Score', 'Engagement_Score', 'Member_Count', 'Annual_Budget'],
                                     format_func=lambda x: x.replace('_', ' ').title())
        
        with col3:
            rows_display = st.selectbox("📄 Show rows", [10, 25, 50], index=1)
        
        # Apply search filter
        display_df = filtered_df.copy()
        if search_term:
            display_df = display_df[display_df['Club Name'].str.contains(search_term, case=False, na=False)]
        
        # Sort and limit
        display_df = display_df.sort_values(sort_column, ascending=False).head(rows_display)
        
        # Format display columns
        display_columns = ['Club Name', 'Organization_Type', 'Performance_Score', 'Member_Count', 'Annual_Budget', 'Status']
        formatted_df = display_df[display_columns].copy()
        
        formatted_df['Annual_Budget'] = formatted_df['Annual_Budget'].apply(lambda x: f"${x:,.0f}")
        formatted_df['Performance_Score'] = formatted_df['Performance_Score'].apply(lambda x: f"{x:.1f}")
        
        # Display table with enhanced styling
        st.dataframe(
            formatted_df,
            use_container_width=True,
            height=400,
            column_config={
                "Club Name": st.column_config.TextColumn("🎓 Club Name", width="large"),
                "Organization_Type": st.column_config.TextColumn("🏢 Type", width="medium"),
                "Performance_Score": st.column_config.TextColumn("⭐ Performance", width="small"),
                "Member_Count": st.column_config.NumberColumn("👥 Members", width="small"),
                "Annual_Budget": st.column_config.TextColumn("💰 Budget", width="medium"),
                "Status": st.column_config.TextColumn("📈 Status", width="small")
            }
        )
    
    # ========================================
    # EXPORT SECTION
    # ========================================
    
    if export_mode:
        st.markdown('<div class="section-header">💾 Export & Reports</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Full dataset export
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                "📊 Download Full Dataset",
                csv_data,
                f"ucsb_clubs_complete_{time.strftime('%Y%m%d_%H%M')}.csv",
                "text/csv",
                help="Download complete club dataset"
            )
        
        with col2:
            # Top performers export
            top_performers_csv = top_clubs[['Club Name', 'Organization_Type', ranking_criteria, 'Performance_Score']].to_csv(index=False)
            st.download_button(
                "🏆 Download Top Performers",
                top_performers_csv,
                f"ucsb_top_performers_{time.strftime('%Y%m%d_%H%M')}.csv",
                "text/csv",
                help="Download top performing clubs"
            )
        
        with col3:
            # Executive summary report
            executive_summary = f"""
UCSB Clubs Analytics - Executive Report
=======================================
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
-----------------
Total Organizations: {total_clubs}
Average Performance Score: {avg_performance:.1f}/100
Total Annual Budget: ${total_budget:,.0f}
Total Student Members: {total_members:,}
Average Engagement Score: {avg_engagement:.1f}/100

TOP PERFORMER
-------------
Organization: {top_clubs.iloc[0]['Club Name']}
Type: {top_clubs.iloc[0]['Organization_Type']}
{ranking_criteria.replace('_', ' ')}: {top_clubs.iloc[0][ranking_criteria]:.1f}
Performance Score: {top_clubs.iloc[0]['Performance_Score']:.1f}

CATEGORY LEADERS
----------------
"""
            for org_type in filtered_df['Organization_Type'].unique():
                type_data = filtered_df[filtered_df['Organization_Type'] == org_type]
                leader = type_data.loc[type_data['Performance_Score'].idxmax()]
                executive_summary += f"{org_type}: {leader['Club Name']} ({leader['Performance_Score']:.1f})\n"
            
            executive_summary += f"""

BUDGET ANALYSIS
---------------
Total Budget Allocation: ${total_budget:,.0f}
Average Budget per Club: ${total_budget/total_clubs:,.0f}
Budget per Member: ${total_budget/total_members:.0f}
Most Efficient: {most_efficient['Club Name']} (Efficiency: {most_efficient['Budget_Efficiency']:.2f})

RECOMMENDATIONS
---------------
• Focus investment on high-performing categories
• Investigate budget efficiency best practices
• Support emerging organizations with mentorship
• Enhance engagement in underperforming areas
• Develop performance benchmarking standards
"""
            
            st.download_button(
                "📋 Executive Summary",
                executive_summary,
                f"ucsb_executive_summary_{time.strftime('%Y%m%d_%H%M')}.txt",
                "text/plain",
                help="Download executive summary report"
            )
    
    # ========================================
    # AUTO-REFRESH & FOOTER
    # ========================================
    
    # Auto-refresh functionality
    if auto_refresh:
        st.markdown("### ⚡ Auto-Refresh Active")
        time.sleep(30)
        st.cache_data.clear()
        try:
            if hasattr(st, 'rerun'):
                st.rerun()
            else:
                st.experimental_rerun()
        except Exception:
            st.info("✅ Auto-refresh completed")
    
    # Professional footer
    st.markdown(f"""
    <div class="footer">
        <p><strong>🎓 UCSB Clubs Analytics Dashboard</strong></p>
        <p>📊 Comprehensive analysis of {total_clubs} student organizations • 
        💰 ${total_budget:,.0f} total budget • 
        👥 {total_members:,} active members</p>
        <p style="font-size: 0.9rem; opacity: 0.7; margin-top: 1rem;">
            Professional Edition • Built with Streamlit • Last updated: {time.strftime('%H:%M:%S')}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# APPLICATION ENTRY POINT
# ========================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"⚠️ Application Error: {str(e)}")
        
        # Professional error handling
        st.markdown("""
        <div class="info-card">
            <h4>🛠️ Technical Support</h4>
            <p>
            <strong>Quick Solutions:</strong><br>
            1. <strong>Browser:</strong> Refresh with Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)<br>
            2. <strong>Cache:</strong> Clear browser cache and cookies<br>
            3. <strong>Streamlit:</strong> Update with <code>pip install --upgrade streamlit</code><br>
            4. <strong>Server:</strong> Restart with Ctrl+C and run again<br>
            5. <strong>Data:</strong> Verify clubs_ucsb.xlsx file format
            </p>
        </div>
        """, unsafe_allow_html=True)

