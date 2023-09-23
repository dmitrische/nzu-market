# nzu-market
Repository for data, analysis, and modelling pertaining to the market for New Zealand Units (NZUs) within the New Zealand Emissions Trading Scheme (NZ-ETS).

An interactive plot of the historical data and model forecasts is implemented in [streamlit_app.py](./streamlit_app.py), and the app is deployed on AWS: [http://13.239.6.213:8501](http://13.239.6.213:8501).

When implementing and deploying the app, I followed these two examples:
https://github.com/upendrak/streamlit-aws-tutorial
https://www.superkaka.se/posts/part2_deploy_streamlit.html

To collect the underlying data, I created two Jupyter notebooks: 
- [./price-data-scrape/webscraper.ipynb](./price-data-scrape/webscraper.ipynb) for scraping historical price data on NZUs from [CarbonNews website](https://www.carbonnews.co.nz/tag.asp?tag=Jarden+NZ+Market+Report).
- [./EUdata/gatherer.ipynb](./EUdata/gatherer.ipynb) for extracting histoical prices of EUAs from Excel spreadsheets published on the [EEX website](https://www.eex.com/en/market-data/environmental-markets/eua-primary-auction-spot-download).
