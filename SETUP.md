# CORD-19 Analysis Setup Guide

This guide will help you set up and run the CORD-19 analysis project on your local machine.

## Quick Start (5 minutes)

### 1. Prerequisites Check

Make sure you have Python installed:
```bash
python --version  # Should be 3.7 or higher
pip --version     # Should be available
```

### 2. Download and Setup

```bash
# Clone the repository
git clone https://github.com/InjiniaKelvin/pythonweek8.git
cd pythonweek8

# Install dependencies
pip install -r requirements.txt

# Generate sample data (optional - app will create it automatically)
python generate_sample_data.py
```

### 3. Run the Applications

**Start Jupyter Notebook (for analysis):**
```bash
jupyter notebook notebooks/cord19_analysis.ipynb
```

**Start Streamlit App (for interactive exploration):**
```bash
streamlit run src/streamlit_app.py
```

The Streamlit app will open at: http://localhost:8501

## Detailed Setup Instructions

### Option 1: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv cord19-env

# Activate virtual environment
# On Windows:
cord19-env\Scripts\activate
# On macOS/Linux:
source cord19-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python generate_sample_data.py --size 2000

# Run the app
streamlit run src/streamlit_app.py
```

### Option 2: Using Conda

```bash
# Create conda environment
conda create -n cord19 python=3.9
conda activate cord19

# Install dependencies
pip install -r requirements.txt

# Generate sample data and run
python generate_sample_data.py
streamlit run src/streamlit_app.py
```

### Option 3: Using Docker (Advanced)

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python generate_sample_data.py

EXPOSE 8501

CMD ["streamlit", "run", "src/streamlit_app.py", "--server.headless", "true"]
```

Build and run:
```bash
docker build -t cord19-app .
docker run -p 8501:8501 cord19-app
```

## Working with Real CORD-19 Data

### Option 1: Download from Kaggle

1. Create a Kaggle account at https://www.kaggle.com
2. Go to: https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge
3. Download the dataset (you only need `metadata.csv`)
4. Place `metadata.csv` in the `data/` directory
5. Restart the Streamlit app

### Option 2: Using Kaggle API

```bash
# Install Kaggle API
pip install kaggle

# Setup API credentials (follow Kaggle API documentation)
# Download the dataset
kaggle datasets download -d allen-institute-for-ai/CORD-19-research-challenge

# Extract metadata.csv to data/ directory
unzip CORD-19-research-challenge.zip metadata.csv -d data/
```

## Troubleshooting

### Common Issues

#### 1. Module Not Found Error
```bash
# Make sure you're in the right directory
cd pythonweek8
pip install -r requirements.txt
```

#### 2. Port Already in Use
```bash
# Use a different port
streamlit run src/streamlit_app.py --server.port 8502
```

#### 3. Data File Not Found
```bash
# Generate sample data
python generate_sample_data.py
# Or ensure your metadata.csv is in the data/ directory
```

#### 4. Permission Errors (Windows)
```bash
# Run as administrator or use:
python -m pip install --user -r requirements.txt
```

#### 5. Memory Issues with Large Dataset
- Use the sample data generator instead of the full dataset
- Increase your system's virtual memory
- Use data filtering in the notebook

### Platform-Specific Notes

#### Windows Users
- Use `python` instead of `python3`
- Use `Scripts\activate` instead of `bin/activate` for virtual environments
- May need to install Microsoft C++ Build Tools for some packages

#### macOS Users
- May need to install Xcode Command Line Tools: `xcode-select --install`
- Use `python3` and `pip3` if you have multiple Python versions

#### Linux Users
- May need to install additional packages: `sudo apt-get install python3-dev`
- Ensure you have the latest pip: `pip install --upgrade pip`

## Performance Tips

### For Large Datasets
1. **Use Sampling**: The notebook includes sampling techniques for large datasets
2. **Increase Memory**: Adjust pandas settings for better memory usage
3. **Use Filters**: Apply data filters early in your analysis

### For Better App Performance
1. **Streamlit Caching**: The app uses `@st.cache_data` for performance
2. **Data Preprocessing**: Run the notebook first to generate preprocessed data
3. **Browser Settings**: Use Chrome or Firefox for best performance

## Configuration Options

### Streamlit Configuration

Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
headless = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

### Jupyter Configuration

For better notebook experience:
```bash
# Install Jupyter extensions
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user

# Enable useful extensions
jupyter nbextension enable variable_inspector/main
jupyter nbextension enable toc2/main
```

## Next Steps

### After Setup
1. **Explore the Notebook**: Start with `notebooks/cord19_analysis.ipynb`
2. **Try the Streamlit App**: Run the interactive web application
3. **Customize Analysis**: Modify the code for your specific research questions
4. **Add Your Data**: Replace sample data with your own datasets

### Learning Resources
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Plotly Documentation**: https://plotly.com/python/
- **Jupyter Documentation**: https://jupyter.org/documentation

## Getting Help

### Community Support
- **GitHub Issues**: Report bugs or request features
- **Streamlit Community**: https://discuss.streamlit.io/
- **Stack Overflow**: Tag questions with `streamlit`, `pandas`, `python`

### Documentation
- Check the main README.md for detailed project information
- Review code comments in notebooks and Python files
- Explore example outputs in the outputs/ directory

## Contributing

Want to contribute? See our contribution guidelines in README.md!

---

**🎉 You're all set!** Enjoy exploring COVID-19 research data with your new analysis toolkit.
