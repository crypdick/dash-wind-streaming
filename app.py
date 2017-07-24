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
windOrientation = [390.5985722040842, 387.6731015591841, 389.44788616953025, 392.1191309575473, 388.1051442361065, 386.2031063183633, 388.7248327601206, 392.16664419169757, 392.36343641970427, 394.51839601742705, 395.07031244317665, 394.6979532565613, 394.8106440789709, 390.7461406266362, 387.90712887391294, 390.7638533286571, 392.12771126325686, 388.33158205555395, 389.07684635015437, 393.9740376912956, 398.18164164708054, 395.5232048430875, 398.69534214892167, 399.85535734687437, 403.08576931337734, 407.5735712289828, 405.0688995963999, 400.8406167434654, 403.10654415248655, 404.0918634136457, 402.09080168290933, 404.23115696999344, 400.5048570014988, 397.7044269742898, 400.45849230589374, 395.513378039142, 399.51702212209113, 395.51223146326, 394.07612156388774, 396.9070787090545, 401.6186370218034, 396.7488706824341, 392.6688152214263, 390.22550049826594, 390.1619764992376, 394.2390304713646, 390.50680659417355, 392.8151768858303, 390.74751900570965, 389.8628924776394, 384.9465024447294, 384.9049700810815, 389.3920196435449, 386.45089242153415, 382.089409672659, 378.2384537236944, 373.5606466164546, 373.1882327712347, 374.35910075718056, 374.15344841220247, 370.68438353542825, 366.96051989779363, 362.3934528532086, 366.6619707093404, 370.7791539622234, 369.7376220907209, 365.98454544276916, 365.56679631229326, 367.19279402924053, 370.97401231822846, 373.54661858447736, 373.88202916093326, 373.56913485257, 368.6298250886995, 364.79752550211833, 364.6480324262225, 363.85471647630203, 363.5370224818376, 368.12903576722124, 368.18681205551803, 370.20530753801836, 372.3629814032992, 372.60663959225826, 377.4177758309326, 378.63880840733344, 374.0634885798307, 372.3495341035845, 370.19414276680834, 371.1255436746014, 372.27825678720245, 367.4330805060834, 369.3455597705266, 367.4420399353105, 364.6249195780961, 361.0381629537205, 358.8924434418911, 361.68873160615107, 362.4586283430635, 363.26231981529673, 360.92168918968173, 349.4688377701178, 346.6076490695869, 349.49153337359076, 350.20738259410933, 351.07282599812316, 347.67951336350285, 346.3867102196332, 348.6180184085117, 350.54780248386436, 345.5509348128747, 346.2752707982863, 348.45825577823257, 352.6215704475676, 350.1762285953104, 346.54334566898683, 344.7177416085409, 347.856306745221, 352.21497779380917, 351.02087911736584, 353.1945745358091, 350.72063071095096, 352.50456515683607, 354.22553047289455, 355.48349048179915, 359.8782262222159, 360.64232088222053, 360.3516024038355, 363.6964657165628, 368.38569476896714, 367.2446820337421, 369.55630593732434, 367.8664486516286, 368.74710161483597, 367.02254979766167, 371.1623746668679, 375.7128050180748, 378.9724378086761, 379.47082769709255, 378.28464813396994, 374.92298504227495, 371.8148651981276, 373.4375628665786, 370.2622332887555, 374.77475341766325, 373.1191301714636, 371.5457682590492, 368.9460306587897, 366.1239053472076, 368.2258372577041, 370.3064607714513, 368.67776124394896, 372.2311632997623, 368.19728550030356, 367.2364217991554, 368.3422494642438, 368.67332958144436, 373.3763175803628, 376.1603615521258, 378.4182037642407, 382.71645661456967, 380.24724872858866, 379.6332006153542, 375.16113259325937, 372.1024347066488, 368.0771055782502, 364.1336757104126, 367.2387635226072, 370.4211591172079, 366.96033869835543, 363.07095258748245, 359.67255711191916, 358.82959898238494, 363.1087995661584, 361.9254251955187, 362.4993049292217, 358.9940527730565, 359.83296612012964, 362.3946824550109, 361.7390114771143, 366.61313268652964, 363.6630335029518, 368.6613866864327, 364.8901159144257, 362.1797730793746, 365.3947846976903, 364.95904806121086, 368.1271255929495, 363.9744661247972, 362.8800681906625, 367.80429139795535, 365.8119450594085, 369.9579975899726, 372.84278912336987, 375.99653930015904, 373.40909544453484, 370.07549772482065, 371.94818516292605, 369.3030513326501, 369.1194349628282, 367.8144933332774]
count = 0

def initialize():
    global windVal
    global windError
    windVal = []
    windError = []
    prevVal = 20
    prevOrientation = np.random.uniform(0, 360)
    for i in range(0, 200):
        windVal.append(abs(np.random.normal(prevVal, 2, 1)[0]))
        windError.append(abs(np.random.normal(round(prevVal/10), 1)))
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

    print(windOrientation[count])

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

    param = rayleigh.fit(binVal[0])
    pdf_fitted = rayleigh.pdf(binVal[1], loc=(avgVal-abs(param[1]))*0.55, scale=(binVal[1][-1] - binVal[1][0])/3)
    gaussian = lambda x: 3*np.exp(-(30-x)**2/20.)
    X = np.arange(len(binVal[0]))
    x = np.sum(X*binVal[0])/np.sum(binVal[0])
    width = np.sqrt(np.abs(np.sum((X-x)**2*binVal[0])/np.sum(binVal[0])))

    maxV = binVal[0].max()

    fit = lambda t: maxV*np.exp(-(t-x)**2/(2*width**2))
    yVal = pdf_fitted * max(binVal[0]) * 20,
    #
    # print(yVal[0])

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
        y=yVal[0],
        x=binVal[1][:len(binVal[1])],
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
                y1=int(max(max(binVal[0]), max(yVal)))+0.5,
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
                y1=int(max(max(binVal[0]), max(yVal)))+0.5,
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
