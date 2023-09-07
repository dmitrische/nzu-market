import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def gbm_forecast(df, tscale='months', nsteps=60, nsims=100, ymax=300,
                 date0 = '1700-01-01', date1 = '2200-01-01'):

    '''
    Function returning a matplotlib figure, plotting the supplied 
    time-series data and a projection based on the assumption that
    the price dynamics follows geometric brownian motion (GBM).

    INPUTS:
    ------
    
    df - Pandas dataframe with a 'price' column and indexed by datetime.
    
    tscale - string specifying the forecasting time-step: 
             'days', 'weeks', 'months', or 'years'.
    
    nsteps - integer specifying the number of time-steps into the
             future to be forecasted.
    
    nsims - integer specifying the number of feasible trajectories 
            to be simulated using MC and then plotted.
    
    ymax - positive number setting the figure's maximum y-value.
    
    date0 - string specifying the *lower* bound of the time-window
            used to train the GBM model. 
    
    date1 - string specifying the *upper* bound of the time-window
            used to train the GBM model. 
    
    NOTE: date0 and date1 are parsed using pandas.to_datetime()

    OUTPUT:
    ------

    fig - Matplotlib figure object.
    '''

    if not isinstance(df, pd.DataFrame):        
        print('ERROR: passed df is not a dataframe')
        print('type(df)= ', type(df))
        return
    elif not isinstance(df.index, pd.DatetimeIndex):
        print('ERROR: passed df is not indexed by datetime')
        return
    elif not set(['price']).issubset(df.keys()):
        print('ERROR: passed df missing price column')
        return
    else:
        df1 = df[ (df.index >= pd.to_datetime(date0)) & (df.index <= pd.to_datetime(date1))]
        price = list(df1['price'])
        date = list(df1.index)

    # Process supplied data    
    logreturns = [np.log(price[i]/price[i-1]) for i in range(1,len(price))]
    ave = sum(logreturns)/len(logreturns)
    var = sum([(r-ave)**2 for r in logreturns])/(len(logreturns)-1)
    drift = ave - 0.5*var
    sd = np.sqrt(var)
    #print(ave,sd)

    # Calculate analytic projections
    proj_date = [date[-1]]
    proj_price = [price[-1]]
    proj_price_hi = [price[-1]]
    proj_price_lo = [price[-1]]
    proj_price_hi2 = [price[-1]]
    proj_price_lo2 = [price[-1]]
    for m in range(1,nsteps+1):
        params = {tscale:m}
        proj_date.append(date[-1]+pd.offsets.DateOffset(**params))
        d = m*drift
        v = np.sqrt(m)*sd
        v2 = 2*v
        proj_price.append(price[-1]*np.exp(d))
        proj_price_hi.append(price[-1]*np.exp(d+v))
        proj_price_lo.append(price[-1]*np.exp(d-v))
        proj_price_hi2.append(price[-1]*np.exp(d+v2))
        proj_price_lo2.append(price[-1]*np.exp(d-v2))
    
    # Run stochastic simulations
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
    for i in range(nsims):
        ax.plot(proj_date, projections[i], 'C1', alpha=0.2)
    ax.lines[-1].set_label(str(nsims)+' simulations')        
    ax.plot(proj_date, proj_price, 'C0', label='drift')
    ax.plot(proj_date, proj_price_lo, 'C0--', label='drift$~\pm~\sigma$')
    ax.plot(proj_date, proj_price_hi, 'C0--')
    ax.plot(proj_date, proj_price_lo2, 'C0:', label='drift$~\pm~2\sigma$')
    ax.plot(proj_date, proj_price_hi2, 'C0:')
    ax.plot(list(df.index), list(df['price']), 'C0-', alpha=0.3,
        label='historical data')
    ax.plot(date, price, 'C0', marker='.', linestyle='', label='training subset')

    ax.set_ylim(0, ymax)
    ax.set_xlim(df.index[0],df.index[-1]+pd.offsets.DateOffset(**{tscale:nsteps}))
    ax.set_xlabel('date')
    ax.set_ylabel('price')
    ax.set_title('Projection from data\n time-steps: '+tscale)
    plt.legend()
    
    return fig
