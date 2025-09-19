import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
from collections import Counter
import json
import re
import warnings
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Suppress warnings
warnings.filterwarnings('ignore')

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the CORD-19 sample dataset"""
    try:
        # Try to load real data first
        df = pd.read_csv('data/cord19_sample.csv')
    except FileNotFoundError:
        # Create sample data if file doesn't exist
        st.warning("Sample data file not found. Creating demo dataset...")
        df = create_demo_data()
    
    # Ensure datetime conversion
    if 'publish_time' in df.columns:
        df['publish_time'] = pd.to_datetime(df['publish_time'])
        df['publication_year'] = df['publish_time'].dt.year
        df['publication_month'] = df['publish_time'].dt.month
        df['year_month'] = df['publish_time'].dt.to_period('M')
    
    return df

@st.cache_data
def load_stats():
    """Load application statistics"""
    try:
        with open('data/app_stats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'total_papers': 2000,
            'date_range': '2019-12-01 to 2023-12-31',
            'unique_journals': 16,
            'top_journal': 'Nature',
            'peak_year': 2020,
            'sources': ['PMC', 'Elsevier', 'arXiv', 'bioRxiv', 'medRxiv']
        }

def create_demo_data():
    """Create demo data for the app"""
    np.random.seed(42)
    n_samples = 1000
    
    journals = [
        'Nature', 'Science', 'The Lancet', 'New England Journal of Medicine',
        'Cell', 'PLOS ONE', 'Nature Medicine', 'Journal of Virology'
    ]
    
    covid_terms = [
        'COVID-19', 'SARS-CoV-2', 'coronavirus', 'pandemic', 'vaccine',
        'antiviral', 'treatment', 'symptoms', 'transmission'
    ]
    
    data = {
        'cord_uid': [f'cord-{i:06d}' for i in range(n_samples)],
        'title': [f'{np.random.choice(covid_terms)} study in patients' for _ in range(n_samples)],
        'journal': np.random.choice(journals, n_samples),
        'publish_time': pd.date_range(start='2019-12-01', end='2023-12-31', periods=n_samples),
        'source_x': np.random.choice(['PMC', 'Elsevier', 'arXiv'], n_samples),
        'has_full_text': np.random.choice([True, False], n_samples, p=[0.7, 0.3]),
        'title_length': np.random.normal(100, 20, n_samples),
        'abstract_word_count': np.random.normal(200, 50, n_samples)
    }
    
    df = pd.DataFrame(data)
    df['publication_year'] = df['publish_time'].dt.year
    df['publication_month'] = df['publish_time'].dt.month
    return df

def extract_words(text_series, min_length=3):
    """Extract words from text for analysis"""
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
        'a', 'an', 'as', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had'
    }
    
    all_words = []
    for text in text_series.dropna():
        words = re.findall(r'\b[a-zA-Z]+\b', str(text).lower())
        filtered_words = [w for w in words if len(w) >= min_length and w not in stop_words]
        all_words.extend(filtered_words)
    
    return all_words

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🦠 CORD-19 Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive Analysis of COVID-19 Research Papers")
    
    # Load data
    with st.spinner('Loading data...'):
        df = load_data()
        stats = load_stats()
    
    # Sidebar filters
    st.sidebar.header("🔍 Data Filters")
    
    # Year filter
    if 'publication_year' in df.columns:
        year_range = st.sidebar.slider(
            "Select Publication Year Range",
            min_value=int(df['publication_year'].min()),
            max_value=int(df['publication_year'].max()),
            value=(int(df['publication_year'].min()), int(df['publication_year'].max())),
            step=1
        )
        
        # Filter data by year
        df_filtered = df[
            (df['publication_year'] >= year_range[0]) & 
            (df['publication_year'] <= year_range[1])
        ]
    else:
        df_filtered = df
        year_range = (2019, 2023)
    
    # Source filter
    if 'source_x' in df.columns:
        selected_sources = st.sidebar.multiselect(
            "Select Data Sources",
            options=df['source_x'].unique(),
            default=df['source_x'].unique()
        )
        df_filtered = df_filtered[df_filtered['source_x'].isin(selected_sources)]
    
    # Journal filter
    if 'journal' in df.columns:
        top_journals = df['journal'].value_counts().head(10).index.tolist()
        selected_journals = st.sidebar.multiselect(
            "Select Journals (Top 10)",
            options=top_journals,
            default=top_journals[:5]
        )
        if selected_journals:
            df_filtered = df_filtered[df_filtered['journal'].isin(selected_journals)]
    
    st.sidebar.markdown(f"**Filtered Dataset**: {len(df_filtered):,} papers")
    
    # Main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "📈 Time Trends", 
        "📚 Journals", 
        "📝 Text Analysis", 
        "🗄️ Data Explorer"
    ])
    
    with tab1:
        st.header("Dataset Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Papers",
                value=f"{len(df_filtered):,}",
                delta=f"{len(df_filtered) - len(df):,}" if len(df_filtered) != len(df) else None
            )
        
        with col2:
            if 'journal' in df_filtered.columns:
                st.metric(
                    label="Unique Journals",
                    value=f"{df_filtered['journal'].nunique():,}"
                )
        
        with col3:
            if 'source_x' in df_filtered.columns:
                st.metric(
                    label="Data Sources",
                    value=f"{df_filtered['source_x'].nunique()}"
                )
        
        with col4:
            if 'publication_year' in df_filtered.columns:
                st.metric(
                    label="Year Range",
                    value=f"{df_filtered['publication_year'].min():.0f}-{df_filtered['publication_year'].max():.0f}"
                )
        
        # Source distribution
        if 'source_x' in df_filtered.columns:
            st.subheader("Distribution by Source")
            source_counts = df_filtered['source_x'].value_counts()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.pie(
                    values=source_counts.values,
                    names=source_counts.index,
                    title="Papers by Data Source"
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Source Statistics:**")
                for source, count in source_counts.items():
                    percentage = (count / len(df_filtered)) * 100
                    st.write(f"• **{source}**: {count:,} ({percentage:.1f}%)")
    
    with tab2:
        st.header("Publication Trends Over Time")
        
        if 'publication_year' in df_filtered.columns:
            # Yearly trends
            yearly_counts = df_filtered['publication_year'].value_counts().sort_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Papers by Year")
                fig = px.bar(
                    x=yearly_counts.index,
                    y=yearly_counts.values,
                    title="Annual Publication Count",
                    labels={'x': 'Year', 'y': 'Number of Papers'}
                )
                fig.update_traces(marker_color='lightblue')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Cumulative Publications")
                cumulative = yearly_counts.cumsum()
                fig = px.area(
                    x=cumulative.index,
                    y=cumulative.values,
                    title="Cumulative Publications Over Time",
                    labels={'x': 'Year', 'y': 'Cumulative Papers'}
                )
                fig.update_traces(fill='tozeroy', fillcolor='rgba(31, 119, 180, 0.3)')
                st.plotly_chart(fig, use_container_width=True)
            
            # Monthly analysis
            if 'publish_time' in df_filtered.columns:
                st.subheader("Monthly Publication Pattern")
                df_filtered['year_month'] = df_filtered['publish_time'].dt.to_period('M')
                monthly_counts = df_filtered['year_month'].value_counts().sort_index()
                monthly_counts.index = monthly_counts.index.to_timestamp()
                
                fig = px.line(
                    x=monthly_counts.index,
                    y=monthly_counts.values,
                    title="Monthly Publication Timeline",
                    labels={'x': 'Date', 'y': 'Papers Published'}
                )
                fig.update_traces(line=dict(width=2))
                st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.write("**📊 Key Insights:**")
        if 'publication_year' in df_filtered.columns:
            peak_year = yearly_counts.idxmax()
            peak_count = yearly_counts.max()
            st.write(f"• Peak publication year: **{peak_year}** with **{peak_count:,}** papers")
            st.write(f"• Total papers in selected period: **{len(df_filtered):,}**")
            st.write(f"• Average papers per year: **{len(df_filtered) / len(yearly_counts):.0f}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.header("Journal Analysis")
        
        if 'journal' in df_filtered.columns:
            journal_counts = df_filtered['journal'].value_counts()
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("Top Journals by Publication Count")
                top_journals = journal_counts.head(15)
                
                fig = px.bar(
                    y=top_journals.index,
                    x=top_journals.values,
                    orientation='h',
                    title="Top 15 Journals",
                    labels={'x': 'Number of Papers', 'y': 'Journal'}
                )
                fig.update_traces(marker_color='lightcoral')
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Journal Statistics")
                st.metric("Total Journals", f"{journal_counts.nunique():,}")
                st.metric("Top Journal", journal_counts.index[0])
                st.metric("Papers in Top Journal", f"{journal_counts.iloc[0]:,}")
                
                # Journal distribution
                single_paper_journals = sum(journal_counts == 1)
                st.write(f"**Journals with 1 paper:** {single_paper_journals:,}")
                st.write(f"**Journals with 5+ papers:** {sum(journal_counts >= 5):,}")
            
            # Journal trends over time
            if 'publication_year' in df_filtered.columns:
                st.subheader("Top Journals Over Time")
                top_5_journals = journal_counts.head(5).index
                journal_year_data = df_filtered[df_filtered['journal'].isin(top_5_journals)].groupby(['publication_year', 'journal']).size().unstack(fill_value=0)
                
                fig = px.line(
                    journal_year_data,
                    title="Publication Trends for Top 5 Journals",
                    labels={'publication_year': 'Year', 'value': 'Number of Papers'}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("Text Analysis")
        
        if 'title' in df_filtered.columns:
            # Word frequency analysis
            st.subheader("Title Word Analysis")
            
            title_words = extract_words(df_filtered['title'])
            word_freq = Counter(title_words)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Word cloud
                if len(word_freq) > 0:
                    st.subheader("Word Cloud of Titles")
                    
                    # Create word cloud
                    wordcloud_text = ' '.join(df_filtered['title'].dropna().astype(str))
                    
                    try:
                        wordcloud = WordCloud(
                            width=800,
                            height=400,
                            background_color='white',
                            max_words=100,
                            colormap='viridis'
                        ).generate(wordcloud_text)
                        
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                    except Exception as e:
                        st.write("Word cloud generation failed. Showing word frequency instead.")
            
            with col2:
                st.subheader("Top Words")
                if len(word_freq) > 0:
                    top_words = word_freq.most_common(15)
                    words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
                    
                    fig = px.bar(
                        words_df,
                        x='Frequency',
                        y='Word',
                        orientation='h',
                        title="Most Frequent Words"
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Text statistics
            if 'title_length' in df_filtered.columns:
                st.subheader("Text Characteristics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_title_length = df_filtered['title_length'].mean()
                    st.metric("Avg Title Length", f"{avg_title_length:.0f} chars")
                
                with col2:
                    if 'abstract_word_count' in df_filtered.columns:
                        avg_abstract_words = df_filtered['abstract_word_count'].mean()
                        st.metric("Avg Abstract Words", f"{avg_abstract_words:.0f}")
                
                with col3:
                    st.metric("Unique Words in Titles", f"{len(word_freq):,}")
    
    with tab5:
        st.header("Data Explorer")
        
        # Data table with search
        st.subheader("Browse Dataset")
        
        # Search functionality
        search_term = st.text_input("🔍 Search in titles:", "")
        
        display_df = df_filtered.copy()
        
        if search_term:
            mask = display_df['title'].str.contains(search_term, case=False, na=False)
            display_df = display_df[mask]
            st.write(f"Found {len(display_df):,} papers matching '{search_term}'")
        
        # Select columns to display
        available_columns = ['title', 'journal', 'publication_year', 'source_x']
        if 'publish_time' in display_df.columns:
            available_columns.append('publish_time')
        
        selected_columns = st.multiselect(
            "Select columns to display:",
            options=available_columns,
            default=['title', 'journal', 'publication_year']
        )
        
        if selected_columns:
            # Show data
            st.dataframe(
                display_df[selected_columns].head(100),
                use_container_width=True,
                height=600
            )
            
            # Download option
            csv = display_df[selected_columns].to_csv(index=False)
            st.download_button(
                label="📥 Download filtered data as CSV",
                data=csv,
                file_name=f"cord19_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Dataset summary
        st.subheader("Dataset Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Basic Statistics:**")
            st.write(f"• Total records: {len(display_df):,}")
            if 'publication_year' in display_df.columns:
                st.write(f"• Year range: {display_df['publication_year'].min():.0f} - {display_df['publication_year'].max():.0f}")
            if 'journal' in display_df.columns:
                st.write(f"• Unique journals: {display_df['journal'].nunique():,}")
        
        with col2:
            st.write("**Data Quality:**")
            for col in selected_columns:
                if col in display_df.columns:
                    missing_pct = (display_df[col].isnull().sum() / len(display_df)) * 100
                    st.write(f"• {col}: {missing_pct:.1f}% missing")

# Footer
def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h4>CORD-19 Data Explorer</h4>
        <p>Interactive analysis of COVID-19 research papers metadata</p>
        <p>Built with Streamlit • Data source: Allen Institute for AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()
