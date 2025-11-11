### Broadway Analysis 🎭

An interactive Streamlit app and exploratory notebook for analyzing historical Broadway show performance. It visualizes monthly gross revenue trends, ranks top shows by different metrics, and includes an ARIMA-based monthly forecast for the show “Wicked.”


### Features
- **Revenue trend**: Monthly total Broadway gross plotted over time.
- **Top shows explorer**: Rank by
  - Average gross per week
  - Total revenue
  - Running weeks
- **Wicked forecast**: ARIMA-based monthly sales forecast with historical vs. predicted comparison.


### Project Structure
- `streamlit_app.py`: Streamlit UI and Plotly visualizations.
- `broadway-edav.ipynb`: EDA and time-series modeling (ARIMA; Box-Cox, stationarity tests, diagnostics).
- `data/broadway.csv`: Kaggle dataset (see “Data” below).
- `data/WickedResult.csv`: Forecast results generated from the notebook and used by the app.
- `requirements.txt`: Python dependencies.


### Data
- Source: Kaggle dataset `mexwell/broadway-shows` (`Date.Year`, `Show.Name`, `Statistics.Gross`, etc.).
- Note: The dataset used in the app ends at 2016-07, so charts reflect that timeframe.

To download the data:
- Either download from Kaggle and place `broadway.csv` in `data/`.
- Or run the notebook to programmatically fetch it via `kagglehub` and produce `WickedResult.csv`.


### Quickstart
1) Create and activate a virtual environment.
2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Ensure data files exist:
- `data/broadway.csv`
- `data/WickedResult.csv` (create by running the notebook if missing)

4) Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

5) Open the local URL printed in your terminal.


### The Notebook
- Open `broadway-edav.ipynb` in Jupyter/VS Code.
- It demonstrates:
  - Aggregation to monthly gross
  - Stationarity checks (ADF), Box-Cox transform and differencing
  - ACF/PACF inspection
  - ARIMA modeling and residual diagnostics

The Streamlit app reads `data/WickedResult.csv` to overlay predicted monthly sales for “Wicked.”

### License and Attribution
- Data © respective Kaggle contributors (`mexwell/broadway-shows`). Use per Kaggle’s terms.
- Code © 2025 Zainab Shakruwala. See repository license if provided.

### Acknowledgements
- Built with Streamlit 🎈 and Plotly.
- Time-series analysis with statsmodels and scipy.

