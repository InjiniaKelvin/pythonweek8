"""
Sample Data Generator for CORD-19 Analysis
==========================================

This script generates sample data that mimics the structure of the CORD-19 dataset
for demonstration and testing purposes.

Usage:
    python generate_sample_data.py [--size SIZE] [--output OUTPUT]

Arguments:
    --size: Number of sample records to generate (default: 2000)
    --output: Output file path (default: data/cord19_sample.csv)
"""

import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime, timedelta
import json

def generate_cord19_sample(n_samples=2000, random_seed=42):
    """
    Generate sample CORD-19 data with realistic structure and content.
    
    Args:
        n_samples (int): Number of sample records to generate
        random_seed (int): Random seed for reproducibility
    
    Returns:
        pd.DataFrame: Generated sample dataset
    """
    np.random.seed(random_seed)
    
    # Sample journals (real COVID-19 research journals)
    journals = [
        'Nature', 'Science', 'The Lancet', 'New England Journal of Medicine',
        'Cell', 'PLOS ONE', 'Nature Medicine', 'Journal of Virology',
        'Virology', 'Nature Communications', 'BMJ', 'JAMA',
        'Proceedings of the National Academy of Sciences', 'Nature Microbiology',
        'Clinical Infectious Diseases', 'Emerging Infectious Diseases',
        'The Lancet Infectious Diseases', 'Journal of Medical Virology',
        'Antiviral Research', 'Vaccine', 'International Journal of Infectious Diseases'
    ]
    
    # COVID-related terms for generating realistic titles
    covid_terms = [
        'COVID-19', 'SARS-CoV-2', 'coronavirus', 'pandemic', 'vaccine',
        'antiviral', 'treatment', 'symptoms', 'transmission', 'respiratory',
        'infection', 'immunity', 'antibody', 'outbreak', 'diagnosis',
        'therapeutic', 'prevention', 'epidemiology', 'public health', 'clinical'
    ]
    
    # Study types and populations
    study_types = [
        'systematic review', 'clinical trial', 'observational study', 
        'meta-analysis', 'case series', 'cohort study', 'cross-sectional study',
        'randomized controlled trial', 'case-control study', 'retrospective analysis'
    ]
    
    populations = [
        'patients', 'population', 'healthcare workers', 'elderly', 'children',
        'adults', 'pregnant women', 'immunocompromised patients', 'hospitalized patients',
        'outpatients', 'intensive care patients', 'community'
    ]
    
    # Data sources
    sources = ['PMC', 'Elsevier', 'arXiv', 'bioRxiv', 'medRxiv']
    
    # Generate base data
    data = {
        'cord_uid': [f'cord-{i:06d}' for i in range(n_samples)],
        'sha': [f'sha{np.random.randint(100000, 999999)}' for _ in range(n_samples)],
        'source_x': np.random.choice(sources, n_samples),
        'title': [],
        'doi': [f'10.{np.random.randint(1000, 9999)}/{np.random.randint(100000, 999999)}' 
                if np.random.random() > 0.1 else None for _ in range(n_samples)],
        'pmcid': [f'PMC{np.random.randint(1000000, 9999999)}' 
                 if np.random.random() > 0.3 else None for _ in range(n_samples)],
        'pubmed_id': [np.random.randint(10000000, 99999999) 
                     if np.random.random() > 0.2 else None for _ in range(n_samples)],
        'license': np.random.choice(['cc-by', 'cc-by-nc', 'cc-by-sa', 'els-covid', 'arxiv', 'no-cc'], 
                                   n_samples, p=[0.25, 0.20, 0.15, 0.15, 0.15, 0.10]),
        'abstract': [],
        'publish_time': pd.date_range(start='2019-12-01', end='2024-01-31', periods=n_samples),
        'authors': [],
        'journal': np.random.choice(journals, n_samples),
        'mag_id': [np.random.randint(1000000000, 9999999999) 
                  if np.random.random() > 0.4 else None for _ in range(n_samples)],
        'who_covidence_id': [f'WHO-{np.random.randint(10000, 99999)}' 
                           if np.random.random() > 0.8 else None for _ in range(n_samples)],
        'arxiv_id': [f'{np.random.randint(2000, 2024)}.{np.random.randint(10000, 99999)}' 
                    if np.random.random() > 0.9 else None for _ in range(n_samples)],
        'has_pdf_parse': np.random.choice([True, False], n_samples, p=[0.6, 0.4]),
        'has_pmc_xml_parse': np.random.choice([True, False], n_samples, p=[0.4, 0.6]),
        'full_text_file': np.random.choice(['pdf_json', 'pmc_json', None], 
                                          n_samples, p=[0.3, 0.3, 0.4]),
        'url': [f'https://example.com/paper/{i}' if np.random.random() > 0.3 else None 
               for i in range(n_samples)]
    }
    
    # Generate realistic titles
    for _ in range(n_samples):
        main_term = np.random.choice(covid_terms)
        study_type = np.random.choice(study_types)
        population = np.random.choice(populations)
        
        title_templates = [
            f"{main_term} {np.random.choice(['treatment', 'vaccine', 'diagnosis', 'prevention'])} in {population}: {study_type}",
            f"Impact of {main_term} on {population}: {study_type}",
            f"{study_type.title()} of {main_term} {np.random.choice(['symptoms', 'transmission', 'outcomes'])} in {population}",
            f"{main_term} {np.random.choice(['infection', 'disease', 'syndrome'])}: {study_type} among {population}",
            f"Effectiveness of {np.random.choice(['vaccines', 'treatments', 'interventions'])} against {main_term} in {population}"
        ]
        
        title = np.random.choice(title_templates)
        data['title'].append(title)
    
    # Generate realistic abstracts
    for i in range(n_samples):
        abstract_templates = [
            f"Background: This study investigates {np.random.choice(covid_terms).lower()} in the context of pandemic response. "
            f"Methods: We analyzed data from {np.random.randint(50, 5000)} participants over {np.random.randint(1, 24)} months. "
            f"Results: Our findings show significant associations with {np.random.choice(['mortality', 'morbidity', 'transmission', 'immunity'])}. "
            f"Conclusions: These results have important implications for {np.random.choice(['public health', 'clinical practice', 'policy making'])}.",
            
            f"Objective: To evaluate the {np.random.choice(['efficacy', 'safety', 'effectiveness'])} of "
            f"{np.random.choice(['vaccines', 'treatments', 'interventions'])} in {np.random.choice(populations)}. "
            f"Design: {np.random.choice(study_types).title()} conducted between "
            f"{np.random.randint(2020, 2023)} and {np.random.randint(2021, 2024)}. "
            f"Setting: {np.random.choice(['Hospital', 'Community', 'Multi-center', 'Primary care'])} setting. "
            f"Participants: {np.random.randint(100, 10000)} individuals. "
            f"Main outcome measures: {np.random.choice(['Hospitalization', 'Mortality', 'Infection rates', 'Symptom severity'])}.",
            
            "Abstract not available"
        ]
        
        if np.random.random() > 0.1:  # 90% have abstracts
            abstract = np.random.choice(abstract_templates[:-1])
        else:
            abstract = abstract_templates[-1]
        
        data['abstract'].append(abstract)
    
    # Generate author lists
    author_names = [
        'Smith J', 'Johnson A', 'Williams B', 'Brown C', 'Jones D', 'Garcia E',
        'Miller F', 'Davis G', 'Rodriguez H', 'Martinez I', 'Hernandez J', 'Lopez K',
        'Zhang L', 'Wang M', 'Liu N', 'Chen O', 'Yang P', 'Wu Q', 'Kumar R', 'Patel S'
    ]
    
    for _ in range(n_samples):
        num_authors = np.random.choice([1, 2, 3, 4, 5, 6], p=[0.1, 0.2, 0.3, 0.2, 0.1, 0.1])
        authors = np.random.choice(author_names, num_authors, replace=False)
        author_string = '; '.join(authors)
        data['authors'].append(author_string)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add derived features
    df['publication_year'] = df['publish_time'].dt.year
    df['publication_month'] = df['publish_time'].dt.month
    df['publication_month_name'] = df['publish_time'].dt.month_name()
    df['title_length'] = df['title'].str.len()
    df['abstract_word_count'] = df['abstract'].str.split().str.len()
    df['has_full_text'] = (df['has_pdf_parse'] | df['has_pmc_xml_parse'])
    
    return df

def generate_app_stats(df):
    """
    Generate application statistics for the sample dataset.
    
    Args:
        df (pd.DataFrame): Sample dataset
    
    Returns:
        dict: Statistics dictionary
    """
    stats = {
        'total_papers': len(df),
        'date_range': f"{df['publish_time'].min().strftime('%Y-%m-%d')} to {df['publish_time'].max().strftime('%Y-%m-%d')}",
        'unique_journals': df['journal'].nunique(),
        'top_journal': df['journal'].value_counts().index[0],
        'peak_year': int(df['publication_year'].value_counts().index[0]),
        'sources': list(df['source_x'].unique()),
        'generated_at': datetime.now().isoformat(),
        'sample_data': True
    }
    return stats

def main():
    """Main function to generate sample data."""
    parser = argparse.ArgumentParser(description='Generate sample CORD-19 data')
    parser.add_argument('--size', type=int, default=2000, 
                       help='Number of sample records to generate (default: 2000)')
    parser.add_argument('--output', type=str, default='data/cord19_sample.csv',
                       help='Output file path (default: data/cord19_sample.csv)')
    parser.add_argument('--stats', type=str, default='data/app_stats.json',
                       help='Statistics file path (default: data/app_stats.json)')
    
    args = parser.parse_args()
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    print(f"Generating {args.size:,} sample CORD-19 records...")
    
    # Generate sample data
    df = generate_cord19_sample(args.size)
    
    # Save dataset
    df.to_csv(args.output, index=False)
    print(f"Sample dataset saved to: {args.output}")
    print(f"Dataset shape: {df.shape}")
    
    # Generate and save statistics
    stats = generate_app_stats(df)
    with open(args.stats, 'w') as f:
        json.dump(stats, f, indent=2, default=str)
    print(f"Statistics saved to: {args.stats}")
    
    # Display summary
    print("\n=== SAMPLE DATA SUMMARY ===")
    print(f"Total records: {len(df):,}")
    print(f"Date range: {stats['date_range']}")
    print(f"Unique journals: {stats['unique_journals']}")
    print(f"Data sources: {', '.join(stats['sources'])}")
    print(f"Top journal: {stats['top_journal']}")
    print(f"Peak year: {stats['peak_year']}")
    
    # Show sample records
    print("\n=== SAMPLE RECORDS ===")
    print(df[['title', 'journal', 'publication_year', 'source_x']].head())
    
    print(f"\n✅ Sample data generation complete!")
    print(f"You can now run the Streamlit app: streamlit run src/streamlit_app.py")

if __name__ == "__main__":
    main()
