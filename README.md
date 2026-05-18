## PANDUAN RUN STREAMLIT

## 1.1. Set up environment via Anaconda:
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## 1.2. Set up environment via pipenv
```
mkdir analisis_data
cd analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## 2. Run Streamlit:
```
streamlit run dashboard.py
```
