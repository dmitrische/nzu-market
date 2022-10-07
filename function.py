import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def gbm_forecast(df, tscale='months', nsteps=60, nsims=100, ymax=300):

    '''
    Function returning a matplotlib figure, plotting the supplied 
    time-series data and a projection based on the assumption that
    the price dynamics follows geometric brownian motion.
    '''
    
    date = list(df['date'])
    price = list(df['price'])

    logreturns = [np.log(price[i]/price[i-1]) for i in range(1,len(price))]

    ave = sum(logreturns)/len(logreturns)
    var = sum([(r-ave)**2 for r in logreturns])/(len(logreturns)-1)
    drift = ave - 0.5*var
    sd = np.sqrt(var)

    # Analytic projections
    proj_date = [date[-1]]
    proj_price = [price[-1]]
    proj_price_hi = [price[-1]]
    proj_price_lo = [price[-1]]
    for m in range(1,nsteps+1):
        params = {tscale:m}
        proj_date.append(date[-1]+pd.offsets.DateOffset(**params))
        d = m*drift
        v = np.sqrt(m)*sd
        proj_price.append(price[-1]*np.exp(d))
        proj_price_hi.append(price[-1]*np.exp(d+v))
        proj_price_lo.append(price[-1]*np.exp(d-v))
    
    # Stochastic simulations
    np.random.seed(seed=1)
    projections = []
    for i in range(nsims):
        projection = [price[-1]]
        for j in range(nsteps):
            rand = np.random.normal(loc=0.0, scale=sd)
            pnew = projection[-1]*np.exp(drift + rand)
            projection.append(pnew)            
        projections.append(projection)

    # Plot data and projections    
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(date, price, linestyle=':', marker='.', label='datapoints')
    for i in range(nsims):
        ax.plot(proj_date, projections[i], 'C1', alpha=0.2)
    ax.plot(proj_date, proj_price, 'C0', label='drift')
    ax.plot(proj_date, proj_price_lo, 'C0--', label='drift$~\pm~\sigma$')
    ax.plot(proj_date, proj_price_hi, 'C0--')
    ax.set_ylim(0, ymax)
    ax.set_xlim(date[0],proj_date[-1])
    ax.set_xlabel('date')
    ax.set_ylabel('price')
    ax.set_title("Projection from data")

    plt.legend()
    
    return fig
