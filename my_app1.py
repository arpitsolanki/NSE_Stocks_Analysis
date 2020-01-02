
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
import dash_table
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#undervalued=pd.read_csv('undervalued.csv')
#overvalued=pd.read_csv('overvalued.csv')
stock_metrics_pe=pd.read_csv('stock_metrics_pe.csv')

undervalued=stock_metrics_pe.sort_values(by=['price_to_high'],inplace=False,ascending=False)
undervalued=undervalued.filter(['Symbol','sector','price','low52','high52','price_to_high','cv',])
undervalued['price_to_high'] = undervalued['price_to_high'].map('{:,.2f}'.format)
undervalued['cv'] = undervalued['cv'].map('{:,.2f}'.format)

stock_52_trends_l=pd.read_csv('stock_52_trends_l.csv',parse_dates=True)
stock_52_trends_l['Date'] = pd.to_datetime(stock_52_trends_l['Date'])
stock_52_trends_l.sort_values(by=['Date'], ascending=True, inplace=True)

#Returns data frame
stock_returns=stock_metrics_pe.filter(['Symbol','sector','mth_returns','qtr_returns','hly_returns','yly_returns'])
#stock_returns['yieldpct'] = stock_returns['yieldpct'].map('{:,.2f}'.format)
stock_returns['mth_returns'] = stock_returns['mth_returns'].map('{:,.2f}'.format)
stock_returns['qtr_returns'] = stock_returns['qtr_returns'].map('{:,.2f}'.format)
stock_returns['hly_returns'] = stock_returns['hly_returns'].map('{:,.2f}'.format)
stock_returns['yly_returns'] = stock_returns['yly_returns'].map('{:,.2f}'.format)
stock_returns.sort_values(by=['yly_returns'], ascending=True, inplace=True)


optlist=[]
#List of vertical symbols to populate the vertical dropdown    
seclist=stock_metrics_pe.sector.unique()
optlist_sec=[]
for i in range(len(seclist)):
    x={'label':seclist[i],'value':seclist[i]}
    optlist_sec.append(x)


app.layout = html.Div(children=[
    
    html.Div([html.H4(children='NSE STOCK ANALYSIS')],style={'padding': '5px', 'backgroundColor': '#A9A9A9',
                    "color": "black", "font-family": "Century Gothic",
                    "font-weight": "bolder"}),
    
    html.Div([dcc.Dropdown(id="selected-sector", multi=False,value="Metals",placeholder="Select Sector",
                                              options=optlist_sec)]),
    html.Div([dcc.Dropdown(id="selected-value", multi=True,placeholder="Select stocks",value="VEDL"
                                              )]),
    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=dt(2018, 12, 25),
            max_date_allowed=dt(2019, 12, 22),
            initial_visible_month=dt(2019, 1, 1),
            start_date=dt(2019,10,1),
            end_date=dt(2019, 12, 22)
    )]),
    
    html.Div([html.Div([html.H5(children='STOCK DAILY TRENDS'),dcc.Graph(id='line-graph')]
    ,className="six columns"),
    html.Div([html.H5(children='SECTOR BOX PLOTS'),dcc.Graph(id='box-plot')]
    ,className="six columns")
    ],className="row"),
        
    html.Div([
    html.Div([html.H5(children='TOP LOSERS'),
    dash_table.DataTable(
    id='undervalued_table',
    columns=[{'name': 'Company', 'id': 'Symbol'},
 #          {'name': 'sector', 'id': 'sector'},
            {'name': 'price', 'id': 'price'},
            {'name': 'low', 'id': 'low52'},
            {'name': 'high', 'id': 'high52'},
            {'name': 'price_to_high', 'id': 'price_to_high'},
            {'name': 'cv', 'id': 'cv'}
            ],
    sort_action="native",
    sort_mode="multi",
  #  data=undervalued.to_dict('records'),
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }   
    )],className="six columns"),
    
    html.Div([html.H5(children='TOP GAINERS'),
    dash_table.DataTable(
    id='overvalued_table',
    columns=[{'name': 'Company', 'id': 'Symbol'},{'name': 'price', 'id': 'price'},{'name': 'low', 'id': 'low52'},{'name': 'high', 'id': 'high52'},{'name': 'price_to_high', 'id': 'price_to_high'},{'name': 'cv', 'id': 'cv'}
            ], 
    sort_action="native",
    sort_mode="multi",
   # data=overvalued.to_dict('records'),
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'
    }
    
    )],className="six columns"),
    ],className="row"),
    
    html.Div([html.Div([html.H5(children='PRICE FLUCTUATION ANALYSIS'),dcc.Graph(id='bubble-graph')])]),
    
    html.Div([html.H5(children='RETURN ON CAPITAL'),
    dash_table.DataTable(
    id='returns_table',
    columns=[{'name': 'Company', 'id': 'Symbol'},
#           {'name': 'yield_pct', 'id': 'yieldpct'},
#            {'name': 'price', 'id': 'price'},
            {'name': 'Monthly', 'id': 'mth_returns'},
            {'name': 'Quarterly', 'id': 'qtr_returns'},
            {'name': 'Half Yearly', 'id': 'hly_returns'},
            {'name': 'Yearly', 'id': 'yly_returns'}
            ],        
   # data=overvalued.to_dict('records'),
    sort_action="native",
    sort_mode="multi",
    style_data_conditional=[
#         {
#             'if': {'row_index': 'odd'},
#             'backgroundColor': 'rgb(248, 248, 248)'
            
#         },
         {
            'if': {'column_id': str(x),
                   'filter_query': '{{{}}} < 0'.format(x)
                  },
            'color': 'red'
            
        } for x in ['mth_returns','qtr_returns','hly_returns','yly_returns']
        
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
        }
        
#         style_data={
#         'whiteSpace': 'normal',
#         'height': 'auto'
#     },
    )])
   
], style={'backgroundColor': '#F2F5FA',
                    "color": "black", "font-family": "Century Gothic",
                    "font-weight": "900"})

@app.callback(
    [Output('line-graph', 'figure'),
    Output('selected-value', 'options'),
    Output('undervalued_table', 'data'),
    Output('overvalued_table', 'data'),
    Output('returns_table', 'data')
    ],
    [Input('selected-value', 'value'),Input('selected-sector', 'value'),
    Input('date-picker-range', 'start_date'),Input('date-picker-range', 'end_date')])

def update_figure(stocklist,sector,start_date,end_date):
    
    #List of stock symbols to populate the drop down text
   # sector='Automobile'
    stock_returns_filtered=stock_returns[stock_returns.sector==sector]
    stock_returns_filtered=stock_returns_filtered.to_dict('records')
    
    filtered_stocks=stock_52_trends_l[stock_52_trends_l.sector==sector]
    undervalued_stocks=undervalued[undervalued.sector==sector]
    overvalued_stocks=undervalued_stocks.tail(5)    
    overvalued_stocks.sort_values(by=['price_to_high'], ascending=True, inplace=True)
    undervalued_stocks=undervalued_stocks.head(5)
    undervalued_stocks=undervalued_stocks.to_dict('records')
    overvalued_stocks=overvalued_stocks.to_dict('records')

    symlist=filtered_stocks.Symbol.unique()
    optlist=[]
    for i in range(len(symlist)):
        x={'label':symlist[i],'value':symlist[i]}
        optlist.append(x)
    
    
    l = []
    start_date = start_date[:10]
    start_date = dt.strptime(start_date, "%Y-%m-%d")
    end_date = end_date[:10]
    end_date = dt.strptime(end_date, '%Y-%m-%d')
    #Filter data based on date ranges selected in date range picker
    filter_df=filtered_stocks[(filtered_stocks['Date']>=start_date)&(filtered_stocks['Date']<=end_date)]
 #   filter_df=stock_52_trends_l 
    #Filter stocks selected in the multi-select dropdown
    for type in stocklist:
        temp=filter_df[filter_df['Symbol']==type]
        l.append({'x':temp['Date'], 'y':temp['price'], 'name':type, 'mode':'lines+markers'})
                 
    return [{"data": l,
            'layout': {
        #        'title': 'Stock trends',
                "xaxis": {
            #            "title": "Date"
                       # 'tickformat': '%y/%b'
                          #"autorange": false  
                },
    "yaxis": {
      "title": "Log Price",
    },
    "autosize": True,
    "hovermode": "closest",
    "showlegend": True,
    "legend":dict(x=-.1, y=1.2),
    "legend_orientation":"h",
    "margin":{"l": 0, "b": 20, "r": 0}
            }
        },
    optlist,undervalued_stocks,overvalued_stocks,stock_returns_filtered]

@app.callback(
    Output('bubble-graph', 'figure'),
    [Input('selected-sector', 'value')])
def update_bubble(sector):
#     if sector is None:
#         sector='Metals'
    filtered_stocks_bubble=stock_metrics_pe[stock_metrics_pe.sector==sector]
    lis=[]
    max_cap=filtered_stocks_bubble['marketcap'].max()
    for stock in filtered_stocks_bubble.Symbol.unique():
        temp=filtered_stocks_bubble[filtered_stocks_bubble['Symbol']==stock]
        lis.append(go.Scatter(x=temp['price_to_high'],y=temp['price_to_low'],name=stock,mode='markers',marker_size=(temp['marketcap']/max_cap)*100))

    return {"data": lis,
            "layout":go.Layout(xaxis={"title": "Price to High Ratio"},
                                yaxis={"title":"Price to Low Ratio"})
             }


@app.callback(
    Output('box-plot', 'figure'),
    [Input('selected-sector', 'value')])
def update_box(sector):
    filtered_stocks_box=stock_52_trends_l[stock_52_trends_l.sector==sector]
    l=[]
    for stock in filtered_stocks_box.Symbol.unique():
        l.append(go.Box(y=filtered_stocks_box[filtered_stocks_box["Symbol"] == stock]["price"],name=stock,marker={"size": 4}))
    return {"data": l,
            "layout": go.Layout(autosize=True,legend=dict(x=-.1, y=1.2),legend_orientation="h",
                                margin={"l": 0, "b": 0, "r": 0},xaxis={"showticklabels": False,},
                                yaxis={"title": "logprices","type": "log",},)}



if __name__ == '__main__':
    app.run_server(debug=True)
