import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly.graph_objs import *
from flask import Flask
import numpy as np
import math
import os
server = Flask('my app')
server.secret_key = 'secret'
from flask_caching import  Cache

# windVal = [14.799627502279927, 14.14783158613675, 16.408195249829824, 14.887394725208795, 18.301188412113728, 16.484540858586271, 18.735335906462758, 18.932360700132794, 18.113506607965334, 19.225750665282366, 18.568844243108053, 17.375179186849124, 14.7213437219068, 16.766160846566773, 16.268878025195871, 18.790665048472036, 17.57411120081375, 14.221108004642183, 11.419596483892098, 14.95737412887747, 17.914625295327003, 21.128577528195223, 19.300109720799135, 19.626507946208569, 18.096337740213073, 20.207662278260976, 19.161187624729468, 15.294780714958236, 15.264099159378281, 12.119311097101111, 10.751927607373139, 12.333020479771321, 12.513647791759892, 14.65504878214154, 15.310633804289527, 16.477275480340133, 15.717530487935067, 13.594823448021323, 9.988224241734283, 10.619141997718353, 11.34711183368228, 9.1562035009182559, 9.4083229761040936, 10.063394811826321, 9.6748146968755506, 7.9508222535226878, 7.2782338792363142, 5.5059070454265999, 8.1491817694215936, 9.5875196553306168, 13.916888138759678, 13.689602400502094, 14.172075898030119, 15.528766334689934, 14.135533972556988, 15.891369507427628, 18.217520031653081, 19.286613130132181, 24.396015070762719, 26.26282339252705, 24.204473673707117, 25.214884995751952, 23.912693932523144, 23.150429518817287, 25.821828880453218, 28.167214911183056, 27.623929055578827, 29.441899511072624, 30.841762890077533, 29.21864734339486, 31.035743150282563, 33.370245981535334, 35.926418178203889, 34.412699662346739, 33.853391239767653, 34.252104961302535, 31.725953466837691, 30.463858066746322, 31.535460150136199, 31.442939656309573, 30.356675527943896, 30.564274649020795, 28.057410970568789, 28.675776241182447, 29.330635723433868, 28.58307209257223, 33.078686080352192, 33.440297219342511, 31.435959961461233, 32.16340422884447, 32.274871333426013, 32.647969096046587, 32.456785915142085, 29.944889916232093, 29.069453197139257, 29.638343088966849, 28.864565460898387, 29.256622740949794, 29.049870004784854, 25.960029743099334, 24.581302033708027, 24.393293376787696, 21.320195786961804, 20.723587761511851, 20.811427741034937, 23.173120675239833, 26.088586902547327, 25.417593452806042, 27.019057394642079, 28.166153705888842, 27.015555553784822, 27.446188799015481, 27.000375182245861, 28.996708866155476, 28.48862919850577, 27.539557622079286, 25.15176156492506, 21.405261538947119, 20.043675114134317, 19.29582789585643, 15.292415894458628, 15.031169943449783, 16.269657911955044, 18.392400839280352, 21.16033117675623, 21.774735115688891, 22.031470849781133, 22.255539660070429, 20.330750503840719, 19.144041201338045, 19.327852754512644, 20.925581545700911, 25.004065996598289, 26.732658937454037, 24.461252043415286, 23.16030037238124, 22.762132596954423, 22.114652222812683, 24.559081188677908, 25.892294400672547, 25.078370348635755, 26.823040432912236, 28.967000923772058, 31.325048994999474, 32.695501055108224, 36.394729521424743, 38.955197437654199, 43.425952267081719, 42.965083210445648, 41.631053077497207, 42.449022352087596, 38.634043238996426, 41.27749983756275, 43.201138916532621, 43.628094276378647, 44.329143581415629, 43.728246071940561, 43.72816628373252, 42.871647850892749, 42.480002440645933, 45.934396142035361, 44.21902770369762, 46.294026706806569, 50.227541130317221, 50.36908151805978, 53.033336100591576, 53.739154489891952, 51.342629538125699, 51.842810053792839, 47.417041299130481, 47.337364833598812, 49.351024437702378, 51.354796144413122, 50.194752649479938, 50.306947971618733, 48.099047915557925, 46.484581071956853, 42.312732962001036, 37.494626306488883, 38.363002507932698, 36.682732042242897, 37.265991667170319, 36.246879795310903, 36.007901136339484, 37.258946676712405, 39.670829828391653, 40.531262952576235, 39.764241864275128, 36.65873481056704, 38.514406937672554, 38.401952280349349, 36.354598671382135, 39.336663754829949, 38.535210710688617, 37.084894934491203, 38.862353112785705, 36.71913140262135, 39.526148401922043, 39.609232600599711, 40.101827837952385]
# windError = [2.59869120445124, 2.9831216395304425, 1.295782496440806, 0.6594223318721498, 2.2817917988623346, 0.4560911751498733, 0.7985580319275505, 0.5371980535150491, 1.5666454868940907, 1.4983797931013145, 0.2775411036180908, 0.9568915882294052, 1.4207765590584878, 0.5387898208897707, 0.0025165772119268848, 3.3792300761034566, 0.9419860219067329, 0.08713256679163206, 0.522397678416413, 0.2672513994183535, 0.049662485362520714, 0.9182939767759409, 2.827029805803895, 2.0083094296963324, 1.6212147677888096, 0.8866511258715065, 1.3528183657370774, 1.9778833723925597, 1.5343394352203825, 0.7583273574237321, 0.6822625257115157, 2.6203276315723736, 0.8169598428019992, 0.889936468036059, 1.450792205737326, 1.624948262619366, 0.24136050907024642, 1.5958591881880237, 1.648894730554135, 1.5765518946127481, 1.5293997071338121, 2.3763876820649408, 0.9197416554228436, 0.12954406547296027, 0.6560483558455357, 0.29889585869487223, 0.7187277338900012, 0.5926706468537564, 0.2881470244786077, 0.08282075355154431, 1.7322068229463459, 1.0376401461311944, 0.04921498083397957, 2.44748009049935, 0.4091561301486124, 1.4431048962181714, 0.1101181434661157, 2.2678610124393783, 1.2855359484188418, 3.085093393996603, 0.8146346076750477, 2.1235914832075813, 3.4171857933492715, 1.2474073229774012, 1.6528154985650134, 1.2501498711259262, 2.502840503693534, 2.4140016502126915, 3.6419121047833674, 1.1379077618474431, 1.2151345978473798, 2.7698895024959174, 3.7753734330268607, 1.9501925693051556, 4.184362447156879, 2.405339267768863, 2.5114795505191685, 2.0392013474484463, 3.8992354686669617, 2.829018873876241, 4.044817796863959, 3.2424487171710368, 2.3504199987678764, 3.0454540387238387, 1.0565138979402238, 3.046736825372882, 0.12914657557103215, 2.3830486924177334, 2.2612123253765137, 3.607616266321301, 2.5886175762034673, 4.768040316428639, 3.3607799122700723, 2.7039472709437518, 2.5499054613854364, 3.1960062351415184, 2.4107804288010537, 0.9512720200517764, 2.592744109310681, 4.456235594477913, 3.350141269062633, 1.9263689168351734, 0.775949710978785, 1.0436130309401346, 1.2778410891970169, 0.2864342173122518, 3.0364095715492425, 0.8561926359956895, 1.6532816501106826, 3.1416991023995724, 0.9746049622096091, 2.088109488042072, 1.6124192051438826, 0.70156729233973, 1.847194894083203, 0.6729286176043818, 1.7863012858156473, 0.6296936038241274, 1.2381865101045746, 0.9142470519528241, 0.8420140730872099, 0.9368095688379956, 0.8925550902868332, 2.151958446169818, 0.03280870124340707, 1.7563075939859571, 2.769090609792758, 3.3852266942878373, 1.7506841491831298, 2.485673338416538, 0.22851227370802651, 2.3276845549055105, 1.4978208489819664, 2.8838238430277086, 2.285174738693809, 2.12279543395254, 1.2001630648387267, 2.765742022635104, 2.5842400041923614, 1.8086103722229192, 2.37466579111138, 2.516760013842562, 1.0184655336443762, 0.1017534856278357, 4.013385552191055, 2.843799792008422, 2.8165188521512934, 3.6123215803733197, 3.9729715670384818, 4.130486430038443, 3.493852496029294, 5.061443999620785, 2.8837731972208083, 2.2493788687549348, 3.5895040224966435, 4.94286079990266, 4.025797274515631, 4.631967185192519, 5.238699430327409, 4.4807279125988035, 3.0150904129520604, 3.6628034855811418, 3.9445590751601873, 0.3413031056854199, 6.203188131197962, 5.6786294123896335, 4.970561906205753, 5.2643766551695075, 3.7128036912561355, 4.428414398963603, 4.393060360692144, 3.5436063789996, 4.965370419653761, 6.363740885244897, 4.9547095713382845, 7.142475124339796, 4.47213780504838, 2.7901499177635305, 3.5925036019347374, 5.585293017544233, 4.596227418144759, 2.738539229321196, 1.26981305893321, 4.767925526518761, 2.297470405579631, 2.233168504590986, 4.506430569275265, 4.254797101989071, 3.4331688529291404, 1.195951423912621, 2.110900014111669, 2.4547953119480086, 2.6117647546141947, 3.1417389209827613, 4.000094636347067, 3.2020531753582238, 2.2519647507940483, 2.215596907725428, 2.6833350390596853, 3.0689014430799406]
# wind_direction = []
# orientation = np.random.uniform(0, 360)
# count = 0
# windCount = 0
# speedCount = 0
windVal = []
windError = []
orientation = 270

def initialize():
    global windVal
    global windError
    prevVal = 20
    for i in range(0, 200):
        windVal.append(abs(np.random.normal(prevVal, 2, 1)[0]))
        windError.append(abs(np.random.normal(round(prevVal/10), 1)))
        if(round(windVal[-1]) > 45):
            prevVal = int(math.floor(windVal[-1]))
        elif(round(windVal[-1]) < 10):
            prevVal = int(math.ceil(windVal[-1]))
        else:
            prevVal = int(round(windVal[-1]))

app = dash.Dash('streaming-wind-app', server=server)

app.layout = html.Div([
    html.Div([
        html.H2("Wind Speed Dashboard",
                style={
                    'color': 'white',
                    'marginLeft': '2%',
                    'padding-top': '10px',
                    'display': 'inline-block'
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
    if (len(windVal)>202):
        print("We here")
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

    return dict(data=[trace], layout=layout)


# @app.callback(Output('wind-direction', 'figure'), [],
#               [State('wind-speed', 'figure')],
#               [Event('wind-speed-update', 'interval')])
# def gen_wind_direction(oldFigure):
#     global windVal
#     # Preset wind values either adding to old app values or we will be
#
#     windVal = []
#     if oldFigure is not None:
#         windVal = oldFigure['data'][0]['y']
#     orientation = np.random.uniform(orientation-5, orientation+5)
#     count=count+1
#     if count == 100:
#         count=0
#         orientation = np.random.uniform(orientation-50, orientation+50)
#     val = windVal[-1]
#     trace1 = Area(
#         r=[val-10],
#         t=np.full(5, orientation),
#         marker=dict(
#             color='#f8eff9'
#         )
#     )
#     trace = Area(
#         r=[val],
#         t=np.full(5, orientation),
#         marker=dict(
#             color='rgb(242, 196, 247)'
#         )
#     )
#     layout = Layout(
#         autosize=True,
#         width=300,
#         plot_bgcolor='#F2F2F2',
#         margin=Margin(
#             t=10,
#             b=10,
#             r=30,
#             l=40
#         ),
#         showlegend=False,
#         radialaxis=dict(
#             range=[0, max(max(windVal), 35)]
#         ),
#         orientation=270,
#     )
#     return dict(data=[trace, trace1], layout=layout)


@app.callback(Output('wind-histogram', 'figure'),
              [],
              [State('wind-speed', 'figure'),
               State('bin-slider', 'value'),
               State('bin-auto', 'values')],
              [Event('wind-speed-update', 'interval')])
def gen_wind_histogram(oldFigure, sliderValue, autoState):
    print(sliderValue)
    windVal = []
    if oldFigure is not None:
        windVal = oldFigure['data'][0]['y']
    if 'Auto' in autoState:
        binVal = np.histogram(windVal, bins=range(int(round(min(windVal))), int(round(max(windVal)))))
    else:
        binVal = np.histogram(windVal, bins=sliderValue)
    avgVal = float(sum(windVal))/len(windVal)
    medianVal = np.median(windVal)
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


@app.callback(Output('bin-auto', 'values'), [Input('bin-slider', 'value')],
              [State('wind-speed', 'figure')],
              [Event('bin-slider', 'change')])
def deselect_auto(sliderValue, oldFigure):
    print(oldFigure['data'][0]['y'])
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
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})



if __name__ == '__main__':
    app.run_server()
