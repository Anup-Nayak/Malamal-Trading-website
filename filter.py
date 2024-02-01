from flask import Blueprint, render_template,request
import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import plotly.graph_objects as go
from jugaad_data import nse
from dateutil.relativedelta import relativedelta
from datetime import date
from plotly.offline import iplot
import yfinance as yf

filt = Blueprint("filt",__name__,static_folder= "static",template_folder="template")

yfd = ["AMZN", "MSFT", "AAPL", "GOOG", "NFLX", "TSLA", "FB", "GOOGL", "NVDA", "PYPL", "V", "INTC", "AMD", "DIS", "GS", "CSCO", "IBM", "BA", "WMT", "JPM"]

@filt.route('/',methods=['GET','POST'])
def filter():
    if request.method == 'POST':
        avg = request.form.get('avg')
        avg = float(avg)
        filtered_Stocks = filterStocks(avg)
        print(filtered_Stocks)
        return render_template('filter.html',filteredStocks = filtered_Stocks)
    else:
        return render_template('filter.html',filteredStocks = [])
    
def filterStocks(avg):
    filtered_stocks = []
    for stock in yfd:        
        a = yf.Ticker(stock)
        endDate = date.today()
        startDate = endDate - relativedelta(years = 9)
        stock_data = a.history(period='max')
        average_price = stock_data['Close'].mean()
        

        if average_price > avg:
            filtered_stocks.append(stock)
    
    return filtered_stocks