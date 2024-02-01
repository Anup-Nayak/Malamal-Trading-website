from flask import Blueprint, render_template,request
import pandas as pd
import plotly.graph_objects as go

nifty50 = Blueprint("nifty50",__name__,static_folder= "static",template_folder="template")

@nifty50.route('/',methods=['GET','POST'])
def nifty():
    df = pd.read_csv('NIFTY.csv')
    df['DATE'] = pd.to_datetime(df['DATE'])

    timeInterval = request.form.get('interval')
    
    if timeInterval == 'weekly':
        df['idx'] = df['DATE']
        df.set_index('idx',inplace=True)
        df = df.resample('W').last()
        
    elif timeInterval == 'monthly':
        df['idx'] = df['DATE']
        df.set_index('idx',inplace=True)
        df = df.resample('M').last()

    candlestick_chart = generate_candlestick_chart(df)
    return render_template('nifty.html',cc= candlestick_chart,stck="NIFTY50")

def generate_candlestick_chart(df):
    candlestick_trace = go.Candlestick(x=df['DATE'],
                                       open=df['OPEN'],
                                       high=df['HIGH'],
                                       low=df['LOW'],
                                       close=df['CLOSE'])

    layout = go.Layout(title='Price vs Time', xaxis=dict(title='Date'), yaxis=dict(title='Price'),height=800)

    figure = go.Figure(data=[candlestick_trace], layout=layout)
    figure.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(count=5,
                        label="5y",
                        step="year",
                        stepmode="backward"),

                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return figure.to_html(full_html=False)

