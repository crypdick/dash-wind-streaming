import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly.graph_objs import *
from scipy.stats import rayleigh
from flask import Flask
import numpy as np
import math
import os
server = Flask('my app')
server.secret_key = os.environ.get('secret_key', 'secret')


windVal = []
windError = []
windOrientation = []
count = 0


def initialize():
    global windVal
    global windError
    global windOrientation
    windVal = []
    windError = []
    windOrientation = []
    prevVal = 20
    prevOrientation = np.random.uniform(0, 360)
    for i in range(0, 200):
        windVal.append(abs(np.random.normal(prevVal, 2, 1)[0]))
        windError.append(abs(np.random.normal(round(prevVal/10), 1)))
        if(i % 100 == 0):
            windOrientation.append(np.random.uniform(prevOrientation-50,
                                                     prevOrientation+50))
        else:
            windOrientation.append(np.random.uniform(prevOrientation-5,
                                                     prevOrientation+5))
        if(round(windVal[-1]) > 45):
            prevVal = int(math.floor(windVal[-1]))
        elif(round(windVal[-1]) < 10):
            prevVal = int(math.ceil(windVal[-1]))
        else:
            prevVal = int(round(windVal[-1]))
        prevOrientation = windOrientation[-1]


app = dash.Dash('streaming-wind-app', server=server,
                url_base_pathname='/dash/gallery/live-wind-data/',
                csrf_protect=False)

app.layout = html.Div([
    html.Div([
        html.H2("Wind Speed Streaming"),
        html.Img(src="https://cdn.rawgit.com/plotly/design-assets/master/logo/dash/images/dash-logo-by-plotly-stripe-inverted.png?token=ARkbw08LOFmsmBW_ibfg9DreRuh1YDxpks5ZejfPwA%3D%3D"),
    ], className='banner'),
    html.Div([
        html.Div([
            html.H3("WIND SPEED (mph)")
        ], className='Title'),
        html.Div([
            dcc.Graph(id='wind-speed'),
        ], className='twelve columns wind-speed'),
        dcc.Interval(id='wind-speed-update', interval=100),
    ], className='row wind-speed-row'),
    html.Div([
        html.Div([
            html.Div([
                html.H3("WIND SPEED HISTOGRAM")
            ], className='Title'),
            html.Div([
                dcc.Slider(
                    id='bin-slider',
                    min=1,
                    max=60,
                    step=1,
                    value=20,
                    updatemode='drag'
                ),
            ], className='histogram-slider'),
            html.P('# of Bins: Auto', id='bin-size', className='bin-size'),
            html.Div([
                dcc.Checklist(
                    id='bin-auto',
                    options=[
                        {'label': 'Auto', 'value': 'Auto'}
                    ],
                    values=['Auto']
                ),
            ], className='bin-auto'),
            dcc.Graph(id='wind-histogram'),
        ], className='seven columns wind-histogram'),
        html.Div([
            html.Div([
                html.H3("WIND DIRECTION")
            ], className='Title'),
            dcc.Graph(id='wind-direction'),
        ], className='five columns wind-polar')
    ], className='row wind-histo-polar')
], style={'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
              'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})


@app.callback(Output('wind-speed', 'figure'), [],
              [State('wind-speed', 'figure')],
              [Event('wind-speed-update', 'interval')])
def gen_wind_speed(oldFigure):
    global windVal
    global windError
    if oldFigure is not None and len(oldFigure['data'][0]['y']) > 0:
        windVal = oldFigure['data'][0]['y']
        windError = oldFigure['data'][0]['error_y']['array']
        # windError = np
    if len(windVal) == 0:
        prevVal = 20
    elif(round(windVal[-1]) > 40):
        prevVal = int(math.floor(windVal[-1]))
    elif(round(windVal[-1]) < 10):
        prevVal = int(math.ceil(windVal[-1]))
    else:
        prevVal = int(round(windVal[-1]))

    windVal.append(abs(np.random.normal(prevVal, 2, 1)[0]))
    windError.append(abs(np.random.normal(round(prevVal/10), 1)))
    if (len(windVal) > 202):
        windVal = windVal[1:]
        windError = windError[1:]



    trace = Scatter(
        y=windVal,
        line=dict(
            color='#42C4F7'
        ),
        error_y=dict(
            type='data',
            array=windError,
            thickness=1.5,
            width=2,
            color='#B4E8FC'
        ),
        mode='lines'
    )

    layout = dict(
        height=450,
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            showline=False,
            zeroline=False,
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(0, min(windVal)), max(45, max(windVal)+max(windError))],
            showline=False,
            zeroline=False,
            nticks=max(6, round(prevVal/10))
        ),
        margin=dict(
            t=45,
            l=50,
            r=50
        )
    )

    return dict(data=[trace], layout=layout, config={"displayModeBar": False})


@app.callback(Output('wind-direction', 'figure'), [],
              [State('wind-speed', 'figure')],
              [Event('wind-speed-update', 'interval')])
def gen_wind_direction(oldFigure):
    global count
    global windOrientation

    if(count == 194):
        count = 0
    else:
        count = count + 1

    val = windVal[-3]

    trace = Area(
        r=np.full(5, val),
        t=np.full(5, windOrientation[count]),
        marker=dict(
            color='rgb(242, 196, 247)'
        )
    )
    trace1 = Area(
        r=np.full(5, val-5),
        t=np.full(5, windOrientation[count]),
        marker=dict(
            color='#F6D7F9'
        )
    )
    trace2 = Area(
        r=np.full(5, val-10),
        t=np.full(5, windOrientation[count]),
        marker=dict(
            color='#FAEBFC'
        )
    )
    layout = Layout(
        autosize=True,
        width=275,
        plot_bgcolor='#F2F2F2',
        margin=Margin(
            t=10,
            b=10,
            r=30,
            l=40
        ),
        showlegend=False,
        radialaxis=dict(
            range=[0, max(max(windVal), 40)]
        ),
        angularaxis=dict(
            showline=False,
            tickcolor='white'
        ),
        orientation=270,
    )

    return dict(data=[trace, trace1, trace2], layout=layout)


@app.callback(Output('wind-histogram', 'figure'),
              [],
              [State('wind-speed', 'figure'),
               State('bin-slider', 'value'),
               State('bin-auto', 'values')],
              [Event('wind-speed-update', 'interval')])
def gen_wind_histogram(oldFigure, sliderValue, autoState):
    windVal = []
    if oldFigure is not None:
        windVal = oldFigure['data'][0]['y']
    if 'Auto' in autoState:
        binVal = np.histogram(windVal, bins=range(int(round(min(windVal))),
                              int(round(max(windVal)))))
    else:
        binVal = np.histogram(windVal, bins=sliderValue)
    avgVal = float(sum(windVal))/len(windVal)
    medianVal = np.median(windVal)

    print(binVal[0])
    print(binVal[1])

    param = rayleigh.fit(binVal[0]) # distribution fitting
    pdf_fitted = rayleigh.pdf(binVal[1], loc=(avgVal * 0.35), scale=15)
    gaussian = lambda x: 3*np.exp(-(30-x)**2/20.)
    X = np.arange(len(binVal[0]))
    x = np.sum(X*binVal[0])/np.sum(binVal[0])
    width = np.sqrt(np.abs(np.sum((X-x)**2*binVal[0])/np.sum(binVal[0])))

    maxV = binVal[0].max()

    fit = lambda t: maxV*np.exp(-(t-x)**2/(2*width**2))
    yVal = fit(X)

    if(int(sliderValue) > 35):
        nticks = 35
    else:
        nticks = len(binVal[1])
    trace = Bar(
        x=binVal[1],
        y=binVal[0],
        marker=dict(
            color='#7F7F7F'
        ),
        showlegend=False,
        hoverinfo='y'
    )
    trace1 = Scatter(
        x=[25],
        y=[0],
        mode='lines',
        line=dict(
            dash='dash',
            color='#2E5266'
        ),
        marker=dict(
            opacity=0,
        ),
        visible=True,
        name='Average'
    )
    trace2 = Scatter(
        x=[25],
        y=[0],
        line=dict(
            dash='dot',
            color='#BD9391'
        ),
        mode='lines',
        marker=dict(
            opacity=0,
        ),
        visible=True,
        name='Median'
    )
    trace3 = Scatter(
        mode='lines',
        line=dict(
            color='#42C4F7'
        ),
        y=pdf_fitted * binVal[1] * 10,
        x=binVal[1][:len(binVal[1])],
        name='Gaussian Fit'
    )
    layout = Layout(
        xaxis=dict(
            title='Wind Speed (mph), Rounded to Closest Integer',
            showgrid=False,
            showline=False,
            tickvals=[round(elem, 2) for elem in binVal[1]],
            nticks=nticks,
            # range=[math.ceil(min(binVal[1]))-0.5,
            #       math.floor(max(binVal[1]))+0.5]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            title='Number of Samples'
            ),
        margin=dict(
            t=50,
            b=20,
            r=50
        ),
        autosize=True,
        bargap=0.01,
        bargroupgap=0,
        hovermode='closest',
        legend=dict(
            x=0.175,
            y=-0.2,
            orientation='h'
        ),
        shapes=[
            dict(
                xref='x',
                yref='y',
                y1=int(max(yVal))+0.5,
                y0=0,
                x0=avgVal,
                x1=avgVal,
                type='line',
                line=dict(
                    dash='dash',
                    color='#2E5266',
                    width=5
                )
            ),
            dict(
                xref='x',
                yref='y',
                y1=int(max(yVal))+0.5,
                y0=0,
                x0=medianVal,
                x1=medianVal,
                type='line',
                line=dict(
                    dash='dot',
                    color='#BD9391',
                    width=5
                )
            )
        ]
    )
    return dict(data=[trace, trace1, trace2, trace3], layout=layout)


@app.callback(Output('bin-auto', 'values'), [Input('bin-slider', 'value')],
              [State('wind-speed', 'figure')],
              [Event('bin-slider', 'change')])
def deselect_auto(sliderValue, oldFigure):
    if (oldFigure is not None and len(oldFigure['data'][0]['y']) > 5):
        return ['']
    else:
        return ['Auto']

@app.callback(Output('bin-size', 'children'), [Input('bin-auto', 'values')],
              [State('bin-slider', 'value')],
              [])
def deselect_auto(autoValue, sliderValue):
    if 'Auto' in autoValue:
        return '# of Bins: Auto'
    else:
        return '# of Bins: ' + str(int(sliderValue))



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dd2784a050c09181150770d06bd5f548d5a22733/dash-wind-streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})


@app.server.before_first_request
def defineInitialWind():
    initialize()


if __name__ == '__main__':
    app.run_server()
