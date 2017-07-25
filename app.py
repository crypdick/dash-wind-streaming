import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly.graph_objs import *
from scipy.stats import rayleigh
from flask import Flask
import numpy as np
import pandas as pd
import os
import sqlite3
import datetime as dt
server = Flask('my app')
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash('streaming-wind-app', server=server,
                url_base_pathname='/dash/gallery/live-wind-data/')

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
        dcc.Interval(id='wind-speed-update', interval=1000),
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
def gen_wind_speed(old_figure):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour * 3600) + (minute * 60) + (sec)

    con = sqlite3.connect("wind-data.db")
    df = pd.read_sql_query("SELECT * from Wind where rowid = " +
                           str(total_time) + ";", con)

    # To avoid using global variables, we will filter data from our database
    # and add it to the previously graphed values in the figure itself, if the
    # figure has never been graphed then we will draw data from the past 200
    # seconds and continue to stream to it.
    if old_figure is None or len(old_figure['data'][0]['y']) == 0:
        df = pd.read_sql_query("SELECT * from Wind where rowid > " +
                               str(total_time-200) + " AND rowid < " +
                               str(total_time) + ";", con)
        wind_val = df["Speed"].tolist()
        wind_error = df["SpeedError"].tolist()
    else:
        wind_val = old_figure['data'][0]['y']
        wind_error = old_figure['data'][0]['error_y']['array']

    wind_val.append(df["Speed"][0])
    wind_error.append(df["SpeedError"][0])

    if (len(wind_val) > 202):
        wind_val = wind_val[1:]
        wind_error = wind_error[1:]

    trace = Scatter(
        y=wind_val,
        line=Line(
            color='#42C4F7'
        ),
        error_y=ErrorY(
            type='data',
            array=wind_error,
            thickness=1.5,
            width=2,
            color='#B4E8FC'
        ),
        mode='lines'
    )

    layout = Layout(
        height=450,
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            showline=False,
            zeroline=False,
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(0, min(wind_val)),
                   max(45, max(wind_val)+max(wind_error))],
            showline=False,
            zeroline=False,
            nticks=max(6, round(wind_val[-3]/10))
        ),
        margin=Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return Figure(data=[trace], layout=layout)


@app.callback(Output('wind-direction', 'figure'), [],
              [State('wind-speed', 'figure')],
              [Event('wind-speed-update', 'interval')])
def gen_wind_direction(old_figure):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour * 3600) + (minute * 60) + (sec)

    con = sqlite3.connect("wind-data.db")
    wind_orientation = pd.read_sql_query("SELECT * from Wind where rowid = " +
                                         str(total_time) + ";", con)

    # Similar idea to that of the wind-speed graph, we are storing the data
    # inside the figure itself, since we are maintaining 202 elements in the
    # trace at a time while only having a range up to 200 we will get the third
    # last element from our graph as this one will be the most recent one that
    # has been displayed.
    if old_figure is not None and len(old_figure['data'][0]['y']) > 0:
        val = old_figure['data'][0]['y'][-3]
        wind_val = old_figure['data'][0]['y']

    trace = Area(
        r=np.full(5, val),
        t=np.full(5, wind_orientation['Direction']),
        marker=Marker(
            color='rgb(242, 196, 247)'
        )
    )
    trace1 = Area(
        r=np.full(5, val*0.65),
        t=np.full(5, wind_orientation['Direction']),
        marker=Marker(
            color='#F6D7F9'
        )
    )
    trace2 = Area(
        r=np.full(5, val*0.30),
        t=np.full(5, wind_orientation['Direction']),
        marker=Marker(
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
            range=[0, max(max(wind_val), 40)]
        ),
        angularaxis=dict(
            showline=False,
            tickcolor='white'
        ),
        orientation=270,
    )

    return Figure(data=[trace, trace1, trace2], layout=layout)


@app.callback(Output('wind-histogram', 'figure'),
              [],
              [State('wind-speed', 'figure'),
               State('bin-slider', 'value'),
               State('bin-auto', 'values')],
              [Event('wind-speed-update', 'interval')])
def gen_wind_histogram(old_figure, sliderValue, auto_state):
    wind_val = []
    if old_figure is not None:
        wind_val = old_figure['data'][0]['y']
    if 'Auto' in auto_state:
        bin_val = np.histogram(wind_val, bins=range(int(round(min(wind_val))),
                               int(round(max(wind_val)))))
    else:
        bin_val = np.histogram(wind_val, bins=sliderValue)
    avg_val = float(sum(wind_val))/len(wind_val)
    median_val = np.median(wind_val)

    param = rayleigh.fit(bin_val[0])
    pdf_fitted = rayleigh.pdf(bin_val[1], loc=(avg_val)*0.55,
                              scale=(bin_val[1][-1] - bin_val[1][0])/3)

    y_val = pdf_fitted * max(bin_val[0]) * 20,
    y_val_max = max(y_val[0])
    bin_val_max = max(bin_val[0])

    trace = Bar(
        x=bin_val[1],
        y=bin_val[0],
        marker=Marker(
            color='#7F7F7F'
        ),
        showlegend=False,
        hoverinfo='x+y'
    )
    trace1 = Scatter(
        x=[25],
        y=[0],
        mode='lines',
        line=Line(
            dash='dash',
            color='#2E5266'
        ),
        marker=Marker(
            opacity=0,
        ),
        visible=True,
        name='Average'
    )
    trace2 = Scatter(
        x=[25],
        y=[0],
        line=Line(
            dash='dot',
            color='#BD9391'
        ),
        mode='lines',
        marker=Marker(
            opacity=0,
        ),
        visible=True,
        name='Median'
    )
    trace3 = Scatter(
        mode='lines',
        line=Line(
            color='#42C4F7'
        ),
        y=y_val[0],
        x=bin_val[1][:len(bin_val[1])],
        name='Rayleigh Fit'
    )
    layout = Layout(
        xaxis=dict(
            title='Wind Speed (mph), Rounded to Closest Integer',
            showgrid=False,
            showline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            title='Number of Samples'
        ),
        margin=Margin(
            t=50,
            b=20,
            r=50
        ),
        autosize=True,
        bargap=0.01,
        bargroupgap=0,
        hovermode='closest',
        legend=Legend(
            x=0.175,
            y=-0.2,
            orientation='h'
        ),
        shapes=[
            dict(
                xref='x',
                yref='y',
                y1=int(max(bin_val_max, y_val_max))+0.5,
                y0=0,
                x0=avg_val,
                x1=avg_val,
                type='line',
                line=Line(
                    dash='dash',
                    color='#2E5266',
                    width=5
                )
            ),
            dict(
                xref='x',
                yref='y',
                y1=int(max(bin_val_max, y_val_max))+0.5,
                y0=0,
                x0=median_val,
                x1=median_val,
                type='line',
                line=Line(
                    dash='dot',
                    color='#BD9391',
                    width=5
                )
            )
        ]
    )
    return Figure(data=[trace, trace1, trace2, trace3], layout=layout)


@app.callback(Output('bin-auto', 'values'), [Input('bin-slider', 'value')],
              [State('wind-speed', 'figure')],
              [Event('bin-slider', 'change')])
def deselect_auto(sliderValue, old_figure):
    if (old_figure is not None and len(old_figure['data'][0]['y']) > 5):
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

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

if __name__ == '__main__':
    app.run_server()
