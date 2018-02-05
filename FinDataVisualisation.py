import math
import numpy as np
import pandas as pd
from scipy import stats

from datetime import datetime
from datetime import time as dt_tm
from datetime import date as dt_date

import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()

from IPython.display import HTML

import plotly
plotly.tools.set_credentials_file(username='MuruRaj10', api_key='uwkz1C6Viau2KK4XN8BH')

import plotly.plotly as py
import plotly.tools as plotly_tools
from plotly.graph_objs import *

df = pd.DataFrame.from_csv('googl.csv',index_col=False)
df2 = pd.DataFrame.from_csv('YAHOO-INDEX_GSPC.csv',index_col=False)

df = df.drop(['Open','Low','High'], axis=1)
df2 = df2.drop(['Open','Low','High','Adjusted Close'], axis=1)

df.columns = ['Date', 'Close', 'Volume']
df2.columns = ['Date', 'Close', 'Volume']
df['Date'] =  pd.to_datetime(df['Date'])
df2['Date'] = pd.to_datetime(df2['Date'])

df_date_index = df.set_index(['Date']) #For finding nearest dates later
last_index = len(df)-1

ABC_Price = [Scatter(
          x=df['Date'],
          y=df['Close'], name='ABC INC')]

layout_ABC_P = Layout(
    title='ABC Inc Daily Closing Prices',
    xaxis=dict(
        title='Date',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Prices/USD',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

fig_ABC_P = Figure(data=ABC_Price, layout=layout_ABC_P)
url_1 =py.plot(fig_ABC_P, filename='ABC Daily Stock prices', auto_open=False)

ABC_Vol = [Bar(
    x=df['Date'],
    y=df['Volume'],
    name='ABC daily volume',
    marker=dict(
        color='rgb(49,130,189)'
    )
)]        
layout_ABC_V = Layout(
    xaxis=dict(
        tickangle=-45,
        title='Date',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Volume',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    barmode='group'
)

fig_ABC_Vol = Figure(data=ABC_Vol, layout=layout_ABC_V)
url_2 =py.plot(fig_ABC_Vol, filename='ABC daily volume', auto_open = False)

One_year_return_ABC = 100.0*(df['Close'][0]/df['Close'][last_index] - 1 )
One_year_return_SP = 100.0*(df2['Close'][0]/df2['Close'][last_index] - 1)

current_month = df['Date'][0].month
current_year = df['Date'][0].year
month_start_index =df_date_index.index.get_loc(dt_date(current_year,current_month,1),method='nearest')
year_start_index =df_date_index.index.get_loc(dt_date(current_year,1,1),method='nearest')

MTD = 100.0*(df['Close'][0]/df['Close'][month_start_index] - 1 )
YTD = 100.0*(df['Close'][0]/df['Close'][year_start_index] - 1 )

def daily_log_return(prices):
    return np.log(prices['Close'][:-1].values / prices['Close'][1:])
Daily_log_returns_ABC = daily_log_return(df)
Daily_log_returns_SP = daily_log_return(df2)
Daily_log_returns_ABC_Std = np.std(Daily_log_returns_ABC)
Daily_log_returns_SP_Std = np.std(Daily_log_returns_SP)

def daily_return(prices):
    return prices['Close'][:-1].values / prices['Close'][1:]
Daily_return_ABC = daily_return(df)
Daily_return_SP = daily_return(df2)
Daily_returns_ABC_Std = np.std(Daily_return_ABC)
Daily_returns_SP_Std = np.std(Daily_return_SP)
n=len(Daily_return_ABC)
TE = np.sqrt(np.sum((Daily_return_ABC - Daily_return_SP)**2)/(n-1))

Y = np.array(Daily_log_returns_ABC)
X = np.array(Daily_log_returns_SP)
slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
line = slope*X+intercept

trace1 = Scatter(
                  x=X, 
                  y=Y, 
                  mode='markers',
                  marker=Marker(size = 3,color='rgb(255, 127, 14)'),
                  name='Log returns'
                  )

trace2 = Scatter(
                  x=X, 
                  y=line, 
                  mode='lines',
                  marker=Marker(color='rgb(31, 119, 180)'),
                  name='Fit'
                  )

layout_reg = Layout(
                title='ABC Inc against S&P 500',
                plot_bgcolor='rgb(229, 229, 229)',
                  xaxis=XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                  yaxis=YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)')
                )

data_reg = [trace1, trace2]
fig_reg = Figure(data=data_reg, layout=layout_reg)

url_3 =py.plot(fig_reg, filename='ABC Inc against S&P 500', auto_open = False)

One_year_Perf = {'ABC' : [One_year_return_ABC, Daily_returns_ABC_Std], 
                 'S&P' : [One_year_return_SP, Daily_returns_SP_Std]}
One_year_Perf=pd.DataFrame(One_year_Perf, index=['Annual Return(%)', 'Standard Deviation'])

Perf2 = {'MTD(%)' : [MTD], 'YTD(%)' : [YTD]}
Perf2 = pd.DataFrame(Perf2)

wrt_benchmark = {'Tracking Error(%)' : [TE*100], 'Beta' : [slope]}
wrt_benchmark = pd.DataFrame(wrt_benchmark)

summary_table_1 = str(One_year_Perf.to_html()).replace(
    '<table border="1" class="dataframe">','<table class="table table-striped">')
summary_table_2 = str(Perf2.to_html(index=False)).replace(
    '<table border="1" class="dataframe">','<table class="table table-striped">')
summary_table_3 = str(wrt_benchmark.to_html(index=False)).replace(
    '<table border="1" class="dataframe">','<table class="table table-striped">')
    
html_string = '''
<html>
    <head>
        <title>ABC Inc. Porfolio</title>
        <meta charset="utf-8" />
        <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{background:whitesmoke; margin: 25px; overflow:scroll;} h3{background: rgb(187, 225, 255);}
        .center {margin: auto;width: 60%;padding: 10px;}
        </style>
    </head>
    <body>
        <h4>Portfolio: Alphabet INC.(GOOGL)</h4>
        <h4>Benchmark: S&P 500 (INX)</h4>
        <h4>Date: 2017-03-07</h4>
        
        <div class="row container-fluid"> 
            <div class="col-xs-6">
                <div class="table-responsive">
                    <table>
                        <thead style="background: rgb(187, 225, 255);">
                            <tr>
                              <th class="col-xs-3">Performance summary</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                              <td class="col-xs-3">''' + summary_table_1 + ''' </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="col-xs-6">
                <div class="table-responsive">
                    <table class="table table-striped">
                      <thead style="background: rgb(187, 225, 255);">
                        <tr>
                          <th class="col-xs-3">Performance to date</th>
                          <th class="col-xs-3">Performance relative to benchmark</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td class="col-xs-3">''' + summary_table_2 + ''' </td>
                          <td class="col-xs-3">''' + summary_table_3 + '''</td>
                        </tr>
                      </tbody>
                    </table>
                </div>
            </div> 
        </div>
        <hr>

        <div class="row container-fluid";> 
            <div class="col-xs-6">
                <div class="table-responsive">
                    <table>
                        <thead style="background: rgb(187, 225, 255);">
                            <tr>
                              <th class="col-xs-6">ABC Inc. (GOOGL) stock from 9 Mar 2016 to 7 Mar 2017</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="col-xs-6"> 
                                  <iframe width="800" height="600"; frameborder="0" \
                                    seamless="seamless" scrolling="no" \
                                    src="''' + url_1 + '''.embed?width=800&height=550""></iframe> </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="col-xs-6">
                <div class="table-responsive">
                    <table>
                        <thead style="background: rgb(187, 225, 255);">
                            <tr>
                              <th class="col-xs-6">ABC Inc (GOOGL) stock volume</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="col-xs-6"> 
                                  <iframe width="800" height="600"; frameborder="0" \
                                    seamless="seamless" scrolling="no" \
                                    src="''' + url_2 + '''.embed?width=800&height=550""></iframe> </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div> 
        </div>
        <hr>
        <div class="center">
        <h3>Alphabet Inc. (GOOGL) against S&P 500 (INX) log returns </h3>
        <iframe width="800" height="600"; frameborder="0" seamless="seamless" scrolling="no" \
        src="''' + url_3 + '''.embed?width=800&height=550""></iframe>        
        </div>
    </body>
</html>'''

f = open('AlphabetInc-Portfolio.html','w')
f.write(html_string)
f.close()