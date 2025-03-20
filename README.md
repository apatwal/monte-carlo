# Monte Carlo Asset Pricing Simulation
Brianna Quinn, Aditya Patwal, Bhuvan Hospet, Connor Karr, Jack Carroll

This project focuses on automating stock data retrieval, cleaning, and transformation to ensure seamless processing and analysis. An interactive dashboard will provide visual insights into historical trends, statistical summaries, and correlations. Predictive modeling to simulate future scenarios with adjustable parameters, offering an understanding of potential market movements. The final deliverable includes a presentation highlighting key insights, practical applications, and potential enhancements to refine the tool’s effectiveness.


Instructions to run this...

(Highly recommend using a virtual environment)

python3 -m venv venv

Mac/Linux users => source venv/bin/activate

Windows => venv\Scripts\activate

pip install -r backend/requirements.txt


streamlit run frontend/dashboard/app.py

When you're done, deactivate the venv:

deactivate

View this in edit

Monte-Carlo/
├── backend/                           # Backend logic and data handling
│   ├── data_collection.py             # Script to fetch stock data from Yahoo Finance
│   ├── data_cleaning.py               # Data preprocessing and cleaning logic
│   ├── monte_carlo.py                 # Monte Carlo simulation implementation
│   ├── analysis.py                    # Exploratory data analysis and statistical calculations
│
├── frontend/                          # Frontend (Streamlit dashboard)
│   ├── dashboard/
│   │   ├── app.py                     # Main Streamlit app entry point
│   │   ├── components.py              # Reusable UI components
│   │   ├── utils.py                   # Helper functions
│   │   └── settings.py                # Configuration (e.g., default tickers, API keys)
│   ├── assets/                        # Static files (e.g., images, icons)
│
├── data/                              # Data storage (for testing and development)
│   ├── raw/                           # Raw stock data
│   ├── cleaned/                       # Processed and cleaned data
