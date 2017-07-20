import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly.graph_objs import *
from flask import Flask
import numpy as np
import math
server = Flask('my app')
server.secret_key = os.environ.get('secret_key', 'secret')

wind = []
windError = []
wind_direction = []
orientation = np.random.uniform(0, 360)
count = 0
windCount = 0
speedCount = 0

app = dash.Dash('streaming-wind-app', server=server)

app.layout = html.Div([
    html.Div([
        html.H2("Wind Speed Dashboard",
                style={
                    'color': 'white',
                    'marginLeft': '2%',
                    'padding-top': '10px',
                    'display': 'inline-block',
                    'font-family': 'Product Sans'
                }
                ),
        html.Img(src="https://cdn.rawgit.com/plotly/design-assets/master/logo/dash/images/dash-logo-by-plotly-stripe-inverted.png?token=ARkbw08LOFmsmBW_ibfg9DreRuh1YDxpks5ZejfPwA%3D%3D",
                 style={
                    'height': '75px',
                    'float': 'right',
                    'position': 'relative',
                    'right': '10px'
                 },
                 ),
    ], className='Banner',
             style={
                'border-radius': '2px 2px 2px 2px',
                'background-color': '#42C4F7',
                'height': '75px',
                'margin': '0 -10px',
                'margin-bottom': '10px'
             }),
    html.Div([
        html.Div([
            html.H3("WIND SPEED (mph)",
                    style={
                        'color': '#42C4F7',
                        'border-bottom': '#D8D8D8',
                        'margin-bottom': '3px',
                        'margin-top': '3px',
                        'margin-left': '10px',
                        'font-size': '1.75rem'
                    }
                    )
        ], className='Title',
            style={
                'border-bottom': '1px solid #D8D8D8'
            }
        ),
        html.Div([
            # html.Div([], className='banner', style={'background-color': 'red', 'height': '30px'}),
            dcc.Graph(id='wind-speed'),
        ], className='twelve columns'),
        dcc.Interval(id='wind-speed-update', interval=100),
    ],
    style={
        'border': '1px solid #D8D8D8',
        'border-radius': '5px 5px 5px 5px',
        'border-bottom': '0'
    },
    className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.H3("WIND SPEED HISTOGRAM",
                        style={
                            'color': '#42C4F7',
                            'border-bottom': '#D8D8D8',
                            'margin-bottom': '3px',
                            'margin-top': '3px',
                            'margin-left': '10px',
                            'font-size': '1.75rem'
                        }
                        )
            ], className='Title',
                style={
                    'border-bottom': '1px solid #D8D8D8'
                }
            ),
            html.Div([
                dcc.Slider(
                    id='bin-slider',
                    min=0,
                    max=65,
                    step=1,
                    value=20,
                    updatemode='drag'
                    # disabled=True
                ),
            ], style={
                'width': '65%',
                'margin': '0 auto',
                'position': 'relative',
                'zIndex': '1000000',
                'top': '40px',
                'left': '25px'
            }),
            html.P('Bin Size: Auto', id='bin-size',
                    style={
                        'display': 'inline-block',
                        'font-size': 'small',
                        'font-family': 'Raleway',
                        'position': 'relative',
                        'margin': '0',
                        'float': 'right',
                        'right': '65px',
                        'top': '50px',
                        'zIndex': 10000000
                    }),
            html.Div([
                dcc.Checklist(
                    id='bin-auto',
                    options=[
                        {'label': 'Auto', 'value': 'Auto'}
                    ],
                    values=['Auto']
                ),
            ], style={
                'display': 'inline-block',
                'zIndex': '1000000',
                'position': 'relative',
                'top': '45px',
                'font-size': 'small',
                'left': '90px'
            }),
            dcc.Graph(id='wind-histogram'),
        ], style={
            'border': '1px solid #D8D8D8',
            'width': '68.4%',
            'border-radius': '5px 5px 5px 5px',
        }, className='seven columns'),
        html.Div([
            html.Div([
                html.H3("WIND DIRECTION",
                        style={
                            'color': '#42C4F7',
                            'border-bottom': '#D8D8D8',
                            'margin-bottom': '3px',
                            'margin-top': '3px',
                            'margin-left': '10px',
                            'font-size': '1.75rem'
                        }
                        )
            ], className='Title',
                style={
                    'border-bottom': '1px solid #D8D8D8'
                }
            ),
            # html.Div([
            #     html.H2("Hello")
            # ], className='banner', style={'background-color': 'red', 'height': '30px'}),
            dcc.Graph(id='wind-direction'),
        ], className='five columns',
        style={
            'border': '1px solid #D8D8D8',
            'border-radius': '5px 5px 5px 5px',
            'marginLeft': '0',
            'float': 'right',
            'width': '305px',
            # 'width': '34.6666666667%',
            'border-left': '0',
            'height': '532px'
        })
    ], className='row', style={'float': 'center', 'margin-bottom': '0'})
], style={'padding': '0px 10px 15px 10px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "1000px",
              'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})

@app.callback(Output('wind-speed', 'figure'), [], [],
              [Event('wind-speed-update', 'interval')])
def gen_wind_speed():
    global wind
    global windError
    global windCount
    windCount = windCount + 1

    if len(wind) == 0:
        prevVal = 20
    elif(round(wind[-1]) > 40):
        prevVal = int(math.floor(wind[-1]))
    elif(round(wind[-1]) < 10):
        prevVal = int(math.ceil(wind[-1]))
    else:
        prevVal = int(round(wind[-1]))

    wind.append(abs(np.random.normal(prevVal, 2, 1)[0]))
    windError.append(abs(np.random.normal(round(prevVal/10), 1)))
    if (len(wind)>200):
        wind = wind[1:]
        windError = windError[1:]

    if (len(wind)>250):
        wind = wind[:251]
        windError = windError[:251]
    trace = Scatter(
        y=wind,
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
            ticks=range(-100, 0),
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(0, min(wind)), max(45, max(wind)+max(windError))],
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

    return dict(data=[trace], layout=layout)


@app.callback(Output('wind-direction', 'figure'), [], [],
              [Event('wind-speed-update', 'interval')])
def gen_wind_direction():
    global wind
    global orientation
    global count
    orientation = np.random.uniform(orientation-5, orientation+5)
    count=count+1
    if count == 100:
        count=0
        orientation = np.random.uniform(orientation-50, orientation+50)
    val = wind[-1]
    trace1 = Area(
        r=[val-10],
        t=np.full(5, orientation),
        marker=dict(
            color='#f8eff9'
        )
    )
    trace = Area(
        r=[val],
        t=np.full(5, orientation),
        marker=dict(
            color='rgb(242, 196, 247)'
        )
    )
    layout = Layout(
        autosize=True,
        width=300,
        plot_bgcolor='#F2F2F2',
        margin=Margin(
            t=10,
            b=10,
            r=30,
            l=40
        ),
        showlegend=False,
        radialaxis=dict(
            range=[0, max(max(wind), 35)]
        ),
        orientation=270,
    )
    return dict(data=[trace, trace1], layout=layout)


@app.callback(Output('wind-histogram', 'figure'),
              [],
              [State('bin-slider', 'value'), State('bin-auto', 'values')],
              [Event('wind-speed-update', 'interval')])
def gen_wind_histogram(sliderValue, autoState):
    print(sliderValue)
    if 'Auto' in autoState:
        binVal = np.histogram(wind, bins=range(int(round(min(wind))), int(round(max(wind)))))
    else:
        binVal = np.histogram(wind, bins=sliderValue)
    avgVal = float(sum(wind[:201]))/len(wind[:201])
    medianVal = np.median(wind[:201])
    gaussian = lambda x: 3*np.exp(-(30-x)**2/20.)
    X = np.arange(len(binVal[0]))
    x = np.sum(X*binVal[0])/np.sum(binVal[0])
    width = np.sqrt(np.abs(np.sum((X-x)**2*binVal[0])/np.sum(binVal[0])))

    maxV = binVal[0].max()

    fit = lambda t : maxV*np.exp(-(t-x)**2/(2*width**2))
    yVal = fit(X)

    if(int(sliderValue) > 35):
        nticks = 35
    else:
        nticks = len(binVal[1])
    print(binVal)
    print(nticks)
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
        y=yVal,
        x=binVal[1],
        name='Gaussian Fit'
    )
    layout = Layout(
        xaxis=dict(
            title='Wind Speed (mph), Rounded to Closest Integer',
            showgrid=False,
            showline=False,
            tickvals=[round(elem, 2) for elem in binVal[1]],
            nticks=nticks,
            range=[math.ceil(min(binVal[1]))-0.5, math.floor(max(binVal[1]))+0.5]
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


@app.callback(Output('bin-auto', 'values'), [Input('bin-slider', 'value')], [],
              [Event('bin-slider', 'change')])
def deselect_auto(sliderValue):
    global wind
    if(len(wind) > 5):
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
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})



if __name__ == '__main__':
    app.run_server()
