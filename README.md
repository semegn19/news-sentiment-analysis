# News Sentiment Analysis for Stock Market Prediction

Analytical pipeline that quantifies financial news sentiment, computes technical indicators from historical price data, and measures the statistical relationship between sentiment and stock price movements.

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/semegn19/news-sentiment-analysis.git
cd news-sentiment-analysis
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Data Setup

Place the datasets in the following structure:
```
data/raw/
├── financial_news.csv
└── stock_prices.csv
```

## 🔄 CI/CD Pipeline

GitHub Actions automatically runs on:
- Every push and pull requests to `main` 

**Checks include**:
- Python syntax validation
- Unit tests execution


## 🛠️ Technology Stack

- **Data Processing**: pandas, numpy
- **NLP & Sentiment**: TextBlob, NLTK (VADER), scikit-learn
- **Technical Indicators**: TA-Lib, PyNance
- **Visualization**: matplotlib, seaborn, plotly
- **Testing**: pytest, pytest-cov
- **CI/CD**: GitHub Actions

