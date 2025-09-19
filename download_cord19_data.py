#!/usr/bin/env python3
"""
CORD-19 Dataset Downloader

This script helps download the CORD-19 dataset from multiple sources.
The full dataset is very large (several GB), so we provide options for:
1. Full dataset download (requires Kaggle API)
2. Sample dataset download (smaller subset)
3. Metadata-only download

Usage:
    python download_cord19_data.py --help
"""

import os
import sys
import argparse
import requests
import pandas as pd
import json
import zipfile
from pathlib import Path
import urllib.request
from tqdm import tqdm

def setup_directories():
    """Create necessary directories"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    raw_dir = data_dir / "raw"
    raw_dir.mkdir(exist_ok=True)
    
    processed_dir = data_dir / "processed"
    processed_dir.mkdir(exist_ok=True)
    
    return data_dir, raw_dir, processed_dir

def download_file_with_progress(url, filepath):
    """Download a file with progress bar"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as file, tqdm(
            desc=f"Downloading {filepath.name}",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    pbar.update(len(chunk))
        
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def download_sample_metadata():
    """Download a sample of CORD-19 metadata from GitHub"""
    print("Downloading sample CORD-19 metadata...")
    
    # This is a smaller sample dataset hosted on GitHub
    sample_urls = [
        {
            'url': 'https://raw.githubusercontent.com/allenai/cord19/master/metadata.csv',
            'filename': 'metadata_sample.csv',
            'description': 'CORD-19 Metadata Sample'
        }
    ]
    
    data_dir, raw_dir, processed_dir = setup_directories()
    
    for item in sample_urls:
        filepath = raw_dir / item['filename']
        print(f"Downloading {item['description']}...")
        
        if download_file_with_progress(item['url'], filepath):
            print(f"✅ Successfully downloaded: {filepath}")
            
            # Process the data
            try:
                df = pd.read_csv(filepath)
                print(f"📊 Dataset shape: {df.shape}")
                print(f"📊 Columns: {list(df.columns)}")
                
                # Save a processed sample
                if len(df) > 5000:
                    sample_df = df.sample(n=5000, random_state=42)
                    sample_path = processed_dir / 'cord19_sample.csv'
                    sample_df.to_csv(sample_path, index=False)
                    print(f"✅ Saved processed sample: {sample_path}")
                
                return True
            except Exception as e:
                print(f"❌ Error processing {filepath}: {e}")
                return False
        else:
            print(f"❌ Failed to download: {item['filename']}")
    
    return False

def download_with_kaggle_api():
    """Download using Kaggle API (requires setup)"""
    print("Attempting to download via Kaggle API...")
    
    try:
        # Check if kaggle is installed
        import kaggle
        
        data_dir, raw_dir, processed_dir = setup_directories()
        
        # Download the dataset
        print("Downloading CORD-19 dataset from Kaggle...")
        kaggle.api.dataset_download_files(
            'allen-institute-for-ai/CORD-19-research-challenge',
            path=str(raw_dir),
            unzip=True
        )
        
        print("✅ Kaggle download completed!")
        return True
        
    except ImportError:
        print("❌ Kaggle API not installed. Install with: pip install kaggle")
        print("💡 Then set up your API key: https://github.com/Kaggle/kaggle-api")
        return False
    except Exception as e:
        print(f"❌ Kaggle download failed: {e}")
        return False

def create_demo_dataset():
    """Create a demo dataset if real data isn't available"""
    print("Creating demo dataset...")
    
    import numpy as np
    from datetime import datetime, timedelta
    
    np.random.seed(42)
    
    # Sample data similar to CORD-19 structure
    n_samples = 2000
    
    journals = [
        'Nature', 'Science', 'The Lancet', 'New England Journal of Medicine',
        'Cell', 'PLOS ONE', 'Nature Medicine', 'Journal of Virology',
        'Virology', 'Nature Communications', 'BMJ', 'JAMA',
        'Proceedings of the National Academy of Sciences', 'Nature Microbiology',
        'Clinical Infectious Diseases', 'Emerging Infectious Diseases'
    ]
    
    covid_terms = [
        'COVID-19', 'SARS-CoV-2', 'coronavirus', 'pandemic', 'vaccine',
        'antiviral', 'treatment', 'symptoms', 'transmission', 'respiratory',
        'infection', 'immunity', 'antibody', 'outbreak', 'diagnosis',
        'therapeutic', 'prevention', 'epidemiology', 'public health', 'clinical'
    ]
    
    study_types = [
        'systematic review', 'clinical trial', 'observational study', 
        'meta-analysis', 'case series', 'cohort study', 'cross-sectional study'
    ]
    
    populations = [
        'patients', 'healthcare workers', 'elderly', 'children', 
        'adults', 'pregnant women', 'immunocompromised patients'
    ]
    
    # Generate realistic titles
    titles = []
    for _ in range(n_samples):
        term = np.random.choice(covid_terms)
        study = np.random.choice(study_types)
        pop = np.random.choice(populations)
        titles.append(f"{term} {study} in {pop}: a comprehensive analysis")
    
    # Generate realistic abstracts
    abstracts = []
    for _ in range(n_samples):
        term = np.random.choice(covid_terms).lower()
        n_participants = np.random.randint(50, 5000)
        duration = np.random.randint(1, 24)
        abstracts.append(
            f"This study investigates {term} in the context of pandemic response. "
            f"Methods included analysis of {n_participants} participants over {duration} months. "
            f"Results show significant findings related to {term} management and treatment outcomes."
        )
    
    # Create the dataset
    data = {
        'cord_uid': [f'cord-{i:06d}' for i in range(n_samples)],
        'sha': [f'sha-{np.random.randint(100000, 999999)}' for _ in range(n_samples)],
        'source_x': np.random.choice(['PMC', 'Elsevier', 'arXiv', 'bioRxiv', 'medRxiv'], n_samples),
        'title': titles,
        'doi': [f'10.1000/{np.random.randint(100000, 999999)}' for _ in range(n_samples)],
        'pmcid': [f'PMC{np.random.randint(1000000, 9999999)}' if np.random.random() > 0.3 else None for _ in range(n_samples)],
        'pubmed_id': [np.random.randint(10000000, 99999999) if np.random.random() > 0.2 else None for _ in range(n_samples)],
        'license': np.random.choice(['cc-by', 'cc-by-nc', 'cc-by-sa', 'els-covid', 'arxiv'], n_samples),
        'abstract': abstracts,
        'publish_time': pd.date_range(start='2019-12-01', end='2023-12-31', periods=n_samples),
        'authors': [f'Author{i % 100}, J.; Smith, A.; Johnson, B.' for i in range(n_samples)],
        'journal': np.random.choice(journals, n_samples),
        'mag_id': [np.random.randint(1000000000, 9999999999) if np.random.random() > 0.4 else None for _ in range(n_samples)],
        'who_covidence_id': [f'WHO-{np.random.randint(100000, 999999)}' if np.random.random() > 0.7 else None for _ in range(n_samples)],
        'arxiv_id': [f'arxiv:{np.random.randint(1000, 9999)}.{np.random.randint(1000, 9999)}' if np.random.random() > 0.8 else None for _ in range(n_samples)],
        'pdf_json_files': [f'pdf_json/{np.random.randint(1000, 9999)}.json' if np.random.random() > 0.6 else None for _ in range(n_samples)],
        'pmc_json_files': [f'pmc_json/PMC{np.random.randint(1000000, 9999999)}.json' if np.random.random() > 0.5 else None for _ in range(n_samples)],
        'url': [f'https://example.com/paper/{i}' for i in range(n_samples)],
        's2_id': [f's2-{np.random.randint(100000000, 999999999)}' for _ in range(n_samples)]
    }
    
    df = pd.DataFrame(data)
    
    # Save the demo dataset
    data_dir, raw_dir, processed_dir = setup_directories()
    demo_path = processed_dir / 'cord19_demo.csv'
    df.to_csv(demo_path, index=False)
    
    # Also save to main data directory for the app
    main_path = data_dir / 'cord19_sample.csv'
    df.to_csv(main_path, index=False)
    
    print(f"✅ Created demo dataset: {demo_path}")
    print(f"✅ Created app dataset: {main_path}")
    print(f"📊 Dataset shape: {df.shape}")
    print(f"📊 Date range: {df['publish_time'].min()} to {df['publish_time'].max()}")
    
    return True

def check_existing_data():
    """Check what data we already have"""
    data_dir = Path("data")
    
    if not data_dir.exists():
        return None
    
    files_found = []
    for file_pattern in ['*.csv', '*.json']:
        files_found.extend(data_dir.glob(file_pattern))
    
    if files_found:
        print("📁 Existing data files found:")
        for file in files_found:
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"  • {file.name}: {size_mb:.1f} MB")
        return files_found
    
    return None

def main():
    parser = argparse.ArgumentParser(description="Download CORD-19 dataset")
    parser.add_argument(
        '--method', 
        choices=['kaggle', 'sample', 'demo'], 
        default='demo',
        help='Download method: kaggle (full dataset), sample (GitHub sample), demo (generated data)'
    )
    parser.add_argument(
        '--force', 
        action='store_true',
        help='Force download even if data exists'
    )
    
    args = parser.parse_args()
    
    print("🦠 CORD-19 Dataset Downloader")
    print("=" * 50)
    
    # Check existing data
    if not args.force:
        existing = check_existing_data()
        if existing:
            response = input("Data files already exist. Continue downloading? (y/n): ")
            if response.lower() != 'y':
                print("Download cancelled.")
                return
    
    success = False
    
    if args.method == 'kaggle':
        print("🔄 Attempting Kaggle download...")
        success = download_with_kaggle_api()
        
    elif args.method == 'sample':
        print("🔄 Attempting sample download...")
        success = download_sample_metadata()
        
    elif args.method == 'demo':
        print("🔄 Creating demo dataset...")
        success = create_demo_dataset()
    
    if success:
        print("\n✅ Download completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: jupyter notebook notebooks/cord19_analysis.ipynb")
        print("2. Or run: streamlit run src/streamlit_app.py")
        print("3. Check the data/ directory for downloaded files")
    else:
        print("\n❌ Download failed. Try a different method:")
        print("  python download_cord19_data.py --method demo")
        print("  python download_cord19_data.py --method sample")
        print("  python download_cord19_data.py --method kaggle")

if __name__ == "__main__":
    main()
