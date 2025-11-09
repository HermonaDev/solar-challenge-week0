# Solar Challenge Week 0

Cross-country solar farm analysis for Benin, Sierra Leone, and Togo for MoonLight Energy Solutions.

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/HermonaDev/solar-challenge-week0.git
cd solar-challenge-week0

# Create virtual environment
python -m venv venv

# Activate environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


## 🛠️ Technical Implementation

### Data Cleaning Pipeline
```python
from scripts.utils import SolarDataCleaner

cleaner = SolarDataCleaner()
benin_clean = cleaner.load_and_clean('data/Benin.csv', 'Benin')

## 📋 Deliverables

### Completed
- ✅ **Interim Report**: Project planning and methodology
- ✅ **Data Pipeline**: End-to-end processing scripts
- ✅ **EDA Suite**: Comprehensive analysis notebooks
- ✅ **Production Code**: Reusable utilities and tests

### In Progress   - Scheduled for Completion
- 🔄 **Final Report**: Medium-style blog post compilation
- 🔄 **Dashboard**: Streamlit deployment and screenshots- - 🔄 **Business Strategy Recommendation**
