import plotly
import plotly.graph_objs as go
import datetime
from pymongo import MongoClient 


# plotly.offline.plot(figure, filename = 'index_finpipe.html', auto_open = True)


    
import dash
import dash_core_components as dcc
import dash_html_components as html

import datetime as dt
import flask
import os

import time

app = dash.Dash(
    __name__, 
    assets_external_scripts='https://codepen.io/chriddyp/pen/bWLwgP.css'
)
server = app.server

app.scripts.config.serve_locally = False
#app.css.append_css({'external_url':'mycss.css'})
app.config['suppress_callback_exceptions']=True


# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
	html.Div(children = [html.H1('Welcome to Stock Charts',style={
                       'font-size': '2.65em',
                       'font-family': 'Century Gothic',
                       'color': "rgba(0, 0, 0, 0.95)",
                       'margin-top': '20%',
                       'margin-bottom': '0',
                       'text-align': 'center',
                       'background':'#eee'

                       })]),
	html.Div(style={
	'margin-left':'45%',
    'margin-top':'2%',
    'padding':20},children = [

    dcc.Link(html.Button('Get Started'), href='/page-1'),
    ])])




stock_page = html.Div([
	
    html.Div(children = [
        html.H2('Stock Chart Analysis',
                style={
                       'font-size': '2.65em',
                       'font-family': 'Century Gothic',
                       'color': "rgba(0, 0, 0, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0',
                       'text-align': 'center',
                       'background':'#eee'

                       }),
        
    ]),
    html.Div(style={
    'display': 'inline',
    'float': 'center',
    'text-align': 'center',
    'padding':20
    },children = [

    dcc.Dropdown(
    id = 'radio_buttons',
    style = {
    'width':'50%',
    'margin-left':'25%'
    },
    options=[
        {'label': 'Wipro', 'value': 'Wipro'},
        {'label': 'Finpipe', 'value': 'Finpipe'},
        {'label': 'Siemens', 'value': 'Siemens'}

    ],
    
    
    value='Wipro'
),html.Br(), dcc.Link(html.Button('Home'), href='/',style={'margin-left':'47.8%'})]),
    html.Div(style={'margin-left':'10%','margin-top':'2%'},children=[
    	dcc.Graph(
    		id = 'graphs',
    		style={
            'width':'90%',
            
            },
    		config = {'displayModeBar':False}
            

    		)],className = 'container')
])



@app.callback(
    dash.dependencies.Output('graphs','figure'),
    [dash.dependencies.Input('radio_buttons', 'value')])
def updatevalues(value):
    client = MongoClient('mongodb+srv://RipperAce85:advait123@stockdatabase-4ebzw.mongodb.net/test?retryWrites=true')
    db = client.get_database('StockCSV')
    collection = db[value]
    fields = {'Date':True,'Open':True,'Close':True,'_id':False}
    stocks = collection.find(projection = fields)

    listOpen = []
    listClose = []
    listDate = []

    for val in stocks:
    	Date = datetime.datetime.strptime(val['Date'],'%Y-%m-%d').date()
    	listDate.append(Date)
    	listOpen.append(val['Open'])
    	listClose.append(val['Close'])

    graph = go.Scatter(x = listDate, y = listOpen, mode = 'lines', name = 'Open_Price', line = dict(color = 'rgb(175, 100, 50)'))

    graph1 = go.Scatter(x = listDate, y = listClose, mode = 'lines', name = 'Close_Price', line = dict(color = 'rgb(215, 50, 50)'))

    data = [graph, graph1]
    layout = go.Layout(title = '{} chart'.format(value), xaxis = dict(rangeselector = dict(buttons = list([dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward', visible = True), 
    	dict(count = 6, label = '6M', step = 'month', stepmode = 'backward', visible = True),
    	dict(step = 'all', visible = True)])),rangeslider = dict(visible = True), type = 'date'), yaxis = dict(title = 'Stock_Price'),paper_bgcolor = '#eee')
    figure = go.Figure(data, layout)
    return figure

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return stock_page
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
