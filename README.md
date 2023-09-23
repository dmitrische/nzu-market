# nzu-market
Repository for data, analysis, and modelling pertaining to the market for New Zealand Units (NZUs) within the New Zealand Emissions Trading Scheme (NZ-ETS).

## Assets
- [./price-data-scraper/webscraper.ipynb](./price-data-scraper/webscraper.ipynb) is a Jupyter notebook for scraping historical price data on NZUs from [CarbonNews website](https://www.carbonnews.co.nz/tag.asp?tag=Jarden+NZ+Market+Report).
- [./EUdata/gatherer.ipynb](./EUdata/gatherer.ipynb) is a Jupyter notebook for gathering histoical price data on EUAs from annual Excel spreadsheet published on the [EEX website](https://www.eex.com/en/market-data/environmental-markets/eua-primary-auction-spot-download).
- [streamlit_app.py](./streamlit_app.py) provides an interactive plot of the historical data, and it is deployed on AWS: [http://13.239.6.213:8501](http://13.239.6.213:8501)
