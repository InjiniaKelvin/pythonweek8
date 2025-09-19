# CORD-19 Research Dataset Analysis

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.25+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A comprehensive analysis and interactive web application for exploring the CORD-19 research dataset, focusing on COVID-19 research papers metadata.

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Data Analysis](#-data-analysis)
- [Streamlit Application](#-streamlit-application)
- [Key Findings](#-key-findings)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Project Overview

This project provides a comprehensive analysis of the CORD-19 (COVID-19 Open Research Dataset) metadata, which contains information about COVID-19 research papers. The analysis includes:

- **Data Exploration**: Understanding the structure and characteristics of the dataset
- **Data Cleaning**: Handling missing values and preparing data for analysis
- **Trend Analysis**: Analyzing publication trends over time
- **Journal Analysis**: Identifying top publishers and publication patterns
- **Text Analysis**: Extracting insights from paper titles and abstracts
- **Interactive Visualization**: A Streamlit web application for dynamic data exploration

### Learning Objectives

By exploring this project, you will learn to:
- Practice loading and exploring real-world datasets
- Apply basic data cleaning techniques
- Create meaningful visualizations
- Build interactive web applications
- Present data insights effectively

## ✨ Features

### Data Analysis Features
- 📊 **Comprehensive Dataset Exploration**: Complete analysis of dataset structure and statistics
- 🧹 **Data Cleaning Pipeline**: Robust handling of missing values and data preparation
- 📈 **Publication Trend Analysis**: Time-series analysis of research publication patterns
- 📚 **Journal Impact Analysis**: Identification of top publishing journals and their characteristics
- 📝 **Text Analytics**: Word frequency analysis and text mining from titles and abstracts
- 🎨 **Rich Visualizations**: Multiple chart types including bar charts, line plots, pie charts, and word clouds

### Interactive Web Application
- 🌐 **Multi-tab Interface**: Organized exploration across different analysis dimensions
- 🔍 **Dynamic Filtering**: Interactive filters for years, sources, and journals
- 📊 **Real-time Visualizations**: Interactive charts using Plotly
- 💾 **Data Export**: Download filtered datasets in CSV format
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/InjiniaKelvin/pythonweek8.git
cd pythonweek8
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Dataset (Optional)
For the complete analysis, download the CORD-19 metadata:
1. Visit [Kaggle CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)
2. Download `metadata.csv`
3. Place it in the `data/` directory

**Note**: The application includes sample data generation, so you can run it without downloading the full dataset.

## 📖 Usage

### Running the Jupyter Notebook Analysis
```bash
jupyter notebook notebooks/cord19_analysis.ipynb
```

### Running the Streamlit Application
```bash
streamlit run src/streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Command Line Options
```bash
# Run Streamlit on a specific port
streamlit run src/streamlit_app.py --server.port 8502

# Run Streamlit with custom configuration
streamlit run src/streamlit_app.py --server.headless true
```

## 📁 Project Structure

```
pythonweek8/
│
├── 📁 data/                          # Data directory
│   ├── cord19_sample.csv            # Sample dataset (generated)
│   ├── app_stats.json              # Application statistics
│   └── metadata.csv                # Full CORD-19 dataset (optional)
│
├── 📁 notebooks/                     # Jupyter notebooks
│   └── cord19_analysis.ipynb       # Main analysis notebook
│
├── 📁 src/                          # Source code
│   └── streamlit_app.py            # Streamlit web application
│
├── 📁 outputs/                      # Output files and exports
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 README.md                     # This file
└── 📄 .gitignore                    # Git ignore rules
```

## 🔬 Data Analysis

### Dataset Overview
The CORD-19 dataset contains metadata for COVID-19 research papers including:
- **Paper Identifiers**: CORD UIDs, PubMed IDs, PMC IDs
- **Publication Information**: Titles, abstracts, authors, journals
- **Temporal Data**: Publication dates and timestamps
- **Source Information**: Data sources (PMC, Elsevier, arXiv, etc.)
- **Content Indicators**: Full text availability flags

### Analysis Components

#### 1. Data Loading and Exploration
- Dataset structure examination
- Data type identification
- Basic statistical summaries
- Missing value assessment

#### 2. Data Cleaning and Preparation
- Missing value handling strategies
- Data type conversions
- Feature engineering (publication years, word counts)
- Data quality validation

#### 3. Publication Trend Analysis
- Temporal publication patterns
- Year-over-year growth analysis
- Monthly publication distribution
- Cumulative publication trends

#### 4. Journal and Publisher Analysis
- Top journals by publication count
- Journal diversity metrics
- Publisher distribution analysis
- Journal-specific trends over time

#### 5. Text Analysis and Mining
- Title word frequency analysis
- Abstract content examination
- Word cloud generation
- Term co-occurrence patterns

#### 6. Source and Repository Analysis
- Data source distribution
- Full-text availability by source
- Source-specific publication patterns
- Repository comparison metrics

## 🌐 Streamlit Application

### Application Features

#### 📊 Overview Tab
- **Key Metrics Dashboard**: Total papers, journals, sources, and date ranges
- **Source Distribution**: Interactive pie charts and statistics
- **Quick Insights**: At-a-glance dataset summary

#### 📈 Time Trends Tab
- **Annual Publication Counts**: Bar charts showing yearly publication volumes
- **Cumulative Trends**: Area charts displaying research growth over time
- **Monthly Patterns**: Line charts revealing seasonal publication patterns
- **Peak Analysis**: Identification of high-activity periods

#### 📚 Journals Tab
- **Top Publishers**: Horizontal bar charts of leading journals
- **Journal Statistics**: Comprehensive metrics and rankings
- **Temporal Trends**: Publication patterns for top journals over time
- **Diversity Metrics**: Journal distribution analysis

#### 📝 Text Analysis Tab
- **Word Clouds**: Visual representation of common terms in titles
- **Frequency Analysis**: Top words in research titles
- **Text Statistics**: Average title lengths, word counts, and content metrics
- **Content Insights**: Key themes and topics identification

#### 🗄️ Data Explorer Tab
- **Interactive Data Table**: Searchable and sortable dataset browser
- **Advanced Filtering**: Multi-criteria data filtering
- **Export Functionality**: CSV download of filtered data
- **Column Selection**: Customizable data views

### Interactive Features
- **Real-time Filtering**: Dynamic data filtering with immediate visual updates
- **Cross-tab Analysis**: Insights that span multiple analytical dimensions
- **Responsive Design**: Optimal viewing on various screen sizes
- **Performance Optimization**: Efficient data handling for smooth user experience

## 📊 Key Findings

### Publication Trends
- **Research Surge**: Significant increase in COVID-19 research publications starting in 2020
- **Peak Activity**: Highest publication volumes during pandemic peak periods
- **Sustained Interest**: Continued research output through 2023

### Journal Landscape
- **Top Publishers**: Leading journals include Nature, Science, The Lancet, and NEJM
- **Journal Diversity**: Over 1,000+ unique journals publishing COVID-19 research
- **Specialization**: Mix of general medical journals and specialized virology publications

### Research Focus Areas
- **Clinical Studies**: High frequency of patient-centered research
- **Vaccine Development**: Significant emphasis on vaccine-related studies
- **Treatment Research**: Extensive therapeutic intervention studies
- **Public Health**: Strong representation of epidemiological and policy research

### Data Sources
- **Repository Distribution**: Papers sourced from PMC, Elsevier, arXiv, bioRxiv, and medRxiv
- **Full-text Availability**: Varying levels of full-text access across sources
- **Open Access**: Strong representation of open-access publications

## 🤝 Contributing

We welcome contributions to improve this project! Here's how you can help:

### Types of Contributions
- **Bug Reports**: Identify and report issues
- **Feature Requests**: Suggest new analysis features or visualizations
- **Code Contributions**: Submit pull requests with improvements
- **Documentation**: Enhance documentation and examples
- **Data Analysis**: Contribute additional analytical insights

### Contribution Process
1. **Fork the Repository**: Create your own fork of the project
2. **Create a Branch**: Make your changes in a feature branch
3. **Make Changes**: Implement your improvements
4. **Test Thoroughly**: Ensure your changes work correctly
5. **Submit Pull Request**: Create a PR with a clear description

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/pythonweek8.git
cd pythonweek8

# Create development environment
python -m venv dev-venv
source dev-venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install jupyter pytest black flake8

# Run tests
pytest tests/

# Run linting
black src/
flake8 src/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Allen Institute for AI**: For providing the CORD-19 dataset
- **Kaggle**: For hosting and distributing the dataset
- **Streamlit Team**: For the excellent web application framework
- **Python Community**: For the amazing data science libraries
- **COVID-19 Researchers**: For their invaluable contributions to science

## 📞 Support

If you encounter any issues or have questions:

1. **Check Documentation**: Review this README and code comments
2. **Search Issues**: Look through existing GitHub issues
3. **Create New Issue**: Submit detailed bug reports or feature requests
4. **Discussion Forum**: Engage with the community

## 🔄 Version History

### v1.0.0 (Current)
- ✅ Complete CORD-19 dataset analysis
- ✅ Interactive Streamlit web application
- ✅ Comprehensive data visualizations
- ✅ Text analysis and word clouds
- ✅ Export functionality
- ✅ Responsive design

### Future Enhancements
- 🔄 Advanced NLP analysis
- 🔄 Machine learning models
- 🔄 API integration
- 🔄 Real-time data updates
- 🔄 Enhanced mobile experience

---

**Built with ❤️ for the data science and research community**

For more information, visit our [GitHub repository](https://github.com/InjiniaKelvin/pythonweek8).
