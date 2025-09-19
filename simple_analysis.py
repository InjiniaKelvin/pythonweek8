#!/usr/bin/env python3
"""
Simple CORD-19 Data Viewer

A basic command-line interface to explore the CORD-19 dataset
when Streamlit is not available.
"""

import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from pathlib import Path

def load_data():
    """Load the CORD-19 dataset"""
    data_path = Path("data/cord19_sample.csv")
    
    if not data_path.exists():
        print("❌ Data file not found. Run: python3 download_cord19_data.py --method demo")
        return None
    
    try:
        df = pd.read_csv(data_path)
        df['publish_time'] = pd.to_datetime(df['publish_time'])
        df['publication_year'] = df['publish_time'].dt.year
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def show_basic_stats(df):
    """Display basic statistics about the dataset"""
    print("\n" + "="*60)
    print("📊 CORD-19 DATASET OVERVIEW")
    print("="*60)
    
    print(f"Total papers: {len(df):,}")
    print(f"Date range: {df['publish_time'].min().strftime('%Y-%m-%d')} to {df['publish_time'].max().strftime('%Y-%m-%d')}")
    print(f"Unique journals: {df['journal'].nunique():,}")
    print(f"Data sources: {', '.join(df['source_x'].unique())}")
    
    print("\n📈 PUBLICATION BY YEAR:")
    year_counts = df['publication_year'].value_counts().sort_index()
    for year, count in year_counts.items():
        print(f"  {int(year)}: {count:,} papers")
    
    print("\n📚 TOP 10 JOURNALS:")
    top_journals = df['journal'].value_counts().head(10)
    for i, (journal, count) in enumerate(top_journals.items(), 1):
        print(f"  {i:2d}. {journal}: {count:,} papers")
    
    print("\n🗄️ SOURCE DISTRIBUTION:")
    source_counts = df['source_x'].value_counts()
    for source, count in source_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {source}: {count:,} papers ({percentage:.1f}%)")

def analyze_titles(df):
    """Analyze paper titles"""
    print("\n" + "="*60)
    print("📝 TITLE ANALYSIS")
    print("="*60)
    
    # Basic text statistics
    df['title_length'] = df['title'].str.len()
    df['title_words'] = df['title'].str.split().str.len()
    
    print(f"Average title length: {df['title_length'].mean():.1f} characters")
    print(f"Average words per title: {df['title_words'].mean():.1f} words")
    
    # Find common terms
    all_words = []
    stop_words = {'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
    
    for title in df['title'].dropna():
        words = [word.lower().strip('.,!?:;') for word in title.split()]
        words = [word for word in words if len(word) >= 3 and word not in stop_words]
        all_words.extend(words)
    
    from collections import Counter
    word_freq = Counter(all_words)
    
    print("\n🔤 MOST FREQUENT WORDS IN TITLES:")
    for i, (word, count) in enumerate(word_freq.most_common(15), 1):
        print(f"  {i:2d}. {word}: {count:,} occurrences")

def create_visualizations(df):
    """Create basic visualizations"""
    print("\n" + "="*60)
    print("📊 CREATING VISUALIZATIONS")
    print("="*60)
    
    try:
        # Create output directory
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        # Publications by year
        year_counts = df['publication_year'].value_counts().sort_index()
        
        plt.figure(figsize=(12, 6))
        plt.bar(year_counts.index, year_counts.values, color='skyblue', edgecolor='navy')
        plt.title('COVID-19 Research Papers by Publication Year', fontsize=14, fontweight='bold')
        plt.xlabel('Year')
        plt.ylabel('Number of Papers')
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for year, count in year_counts.items():
            plt.text(year, count + max(year_counts) * 0.01, str(count), 
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_dir / 'publications_by_year.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved: outputs/publications_by_year.png")
        
        # Top journals
        top_journals = df['journal'].value_counts().head(10)
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(top_journals)), top_journals.values, color='lightcoral')
        plt.yticks(range(len(top_journals)), [j[:40] + '...' if len(j) > 40 else j for j in top_journals.index])
        plt.xlabel('Number of Papers')
        plt.title('Top 10 Journals Publishing COVID-19 Research', fontsize=14, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(top_journals.values):
            plt.text(v + max(top_journals.values) * 0.01, i, str(v), 
                    va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_dir / 'top_journals.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved: outputs/top_journals.png")
        
        # Source distribution
        source_counts = df['source_x'].value_counts()
        
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(source_counts)))
        wedges, texts, autotexts = plt.pie(source_counts.values, labels=source_counts.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Distribution of Papers by Data Source', fontsize=14, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(output_dir / 'source_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved: outputs/source_distribution.png")
        
        print(f"\n📁 All visualizations saved to: {output_dir.absolute()}")
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        print("💡 Make sure matplotlib is installed: sudo apt install python3-matplotlib")

def export_sample_data(df):
    """Export sample data for further analysis"""
    print("\n" + "="*60)
    print("📤 EXPORTING SAMPLE DATA")
    print("="*60)
    
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Export recent papers (last 2 years)
    recent_papers = df[df['publication_year'] >= df['publication_year'].max() - 1]
    recent_path = output_dir / 'recent_papers.csv'
    recent_papers.to_csv(recent_path, index=False)
    print(f"✅ Exported {len(recent_papers):,} recent papers to: {recent_path}")
    
    # Export top journal papers
    top_journal = df['journal'].value_counts().index[0]
    top_journal_papers = df[df['journal'] == top_journal]
    journal_path = output_dir / f'top_journal_papers.csv'
    top_journal_papers.to_csv(journal_path, index=False)
    print(f"✅ Exported {len(top_journal_papers):,} papers from {top_journal} to: {journal_path}")
    
    # Create summary statistics
    summary = {
        'total_papers': len(df),
        'date_range': {
            'start': df['publish_time'].min().isoformat(),
            'end': df['publish_time'].max().isoformat()
        },
        'unique_journals': df['journal'].nunique(),
        'top_journal': {
            'name': df['journal'].value_counts().index[0],
            'papers': int(df['journal'].value_counts().iloc[0])
        },
        'sources': df['source_x'].value_counts().to_dict(),
        'yearly_distribution': df['publication_year'].value_counts().sort_index().to_dict()
    }
    
    summary_path = output_dir / 'dataset_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"✅ Exported summary statistics to: {summary_path}")

def interactive_menu(df):
    """Simple interactive menu"""
    while True:
        print("\n" + "="*60)
        print("🦠 CORD-19 DATA EXPLORER - INTERACTIVE MENU")
        print("="*60)
        print("1. Show basic statistics")
        print("2. Analyze paper titles")
        print("3. Create visualizations")
        print("4. Export sample data")
        print("5. Search papers by keyword")
        print("6. Show specific journal papers")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            show_basic_stats(df)
        elif choice == '2':
            analyze_titles(df)
        elif choice == '3':
            create_visualizations(df)
        elif choice == '4':
            export_sample_data(df)
        elif choice == '5':
            keyword = input("Enter keyword to search in titles: ").strip()
            if keyword:
                matches = df[df['title'].str.contains(keyword, case=False, na=False)]
                print(f"\n🔍 Found {len(matches):,} papers containing '{keyword}':")
                for i, (_, row) in enumerate(matches.head(10).iterrows(), 1):
                    print(f"  {i}. {row['title'][:80]}... ({row['journal']}, {int(row['publication_year'])})")
                if len(matches) > 10:
                    print(f"  ... and {len(matches) - 10:,} more papers")
        elif choice == '6':
            print("\nTop 10 journals:")
            top_journals = df['journal'].value_counts().head(10)
            for i, (journal, count) in enumerate(top_journals.items(), 1):
                print(f"  {i}. {journal} ({count:,} papers)")
            
            try:
                journal_choice = int(input("\nEnter journal number (1-10): ")) - 1
                if 0 <= journal_choice < len(top_journals):
                    selected_journal = top_journals.index[journal_choice]
                    journal_papers = df[df['journal'] == selected_journal]
                    print(f"\n📚 Papers from {selected_journal}:")
                    for i, (_, row) in enumerate(journal_papers.head(10).iterrows(), 1):
                        print(f"  {i}. {row['title'][:80]}... ({int(row['publication_year'])})")
                    if len(journal_papers) > 10:
                        print(f"  ... and {len(journal_papers) - 10:,} more papers")
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input!")
        elif choice == '7':
            print("👋 Thanks for exploring the CORD-19 dataset!")
            break
        else:
            print("Invalid choice! Please enter a number from 1-7.")

def main():
    """Main function"""
    print("🦠 CORD-19 Data Explorer")
    print("Loading dataset...")
    
    df = load_data()
    if df is None:
        return
    
    print(f"✅ Loaded {len(df):,} papers successfully!")
    
    # Auto-generate basic analysis
    show_basic_stats(df)
    analyze_titles(df)
    create_visualizations(df)
    export_sample_data(df)
    
    # Interactive menu
    print("\n" + "="*60)
    print("🔍 INTERACTIVE EXPLORATION")
    print("="*60)
    
    response = input("Would you like to explore the data interactively? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        interactive_menu(df)
    else:
        print("\n📋 Analysis complete! Check the 'outputs/' directory for:")
        print("  • Visualization charts (PNG files)")
        print("  • Exported data samples (CSV files)")
        print("  • Summary statistics (JSON file)")
        print("\n💡 Run 'python3 simple_analysis.py' again anytime to explore the data!")

if __name__ == "__main__":
    main()
