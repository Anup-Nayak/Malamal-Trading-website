from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import plotly.graph_objects as go
from jugaad_data import nse
from dateutil.relativedelta import relativedelta
from datetime import date
from plotly.offline import iplot

NIFTY50 = [
    "ADANIENT",
    "ADANIPORTS",
    "APOLLOHOSP",
    "ASIAN PAINTS",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BAJFINANCE",
    "BAJAJFINSV",
    "BPCL",
    "BHARTIARTL",
    "BRITANNIA",
    "CIPLA",
    "COALINDIA"
    "DIVISLAB",
    "DRREDDY",
    "EICHERMOT",
    "GRASIM",
    "HCLTECH",
    "HDFCBANK",
    "HERONOTOCO",
    "HDFCLIFE",
    "HINDALCO",
    "HINDUNILVR"
    "ICICIBANK",
    "ITC",
    "INDUSINDBK"
    "INFY",
    "JSW STEEL",
    "KOTAKBANK",
    "LTIM"
    "LT",
    "MARUTI",
    "NTPC",
    "NESTLEIND"
    "ONGC",
    "POWERGRID",
    "RELIANCE",
    "SBIN",
    "SUNPHARMA",
    "TCS",
    "TATACONUM",
    "TATAGOLD",
    "TATAMOTORS",
    "TATASTEEL", 
    "TECHM",
    "TITAN",
    "UPL",
    "ULTRACEMCO",
    "WIPRO"]


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    stocks = db.relationship('Stock', backref='user', lazy=True)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Initialize Database within Application Context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('register'))
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('index'))

# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' in session:
#         return render_template('welcome.html', username=session['username'])
#     else:
#         return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/buy',methods = ['POST','GET'])
def buy():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    else:
        
        userid = session['user_id']
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if request.method == 'POST':
            stkName = request.form['stockName']
            stkSym = request.form['stockSym']

            
            if stkSym in NIFTY50:
                new_stock = Stock(symbol= stkSym,name = stkName,user = user)
                db.session.add(new_stock)
                db.session.commit()
            else:
                flash('Enter correct stock.')
                return redirect(url_for('dashboard'))
        return render_template('buy.html',username=username,data=Stock.query.filter_by(user_id=userid).all())
    
@app.route('/sell',methods = ['POST','GET'])
def sell():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    else:
        userid = session['user_id']
        username = session['username']
        if request.method == 'POST':
            stkName = request.form['stockName']
            stkSym = request.form['stockSym']

            if stkSym in NIFTY50:
                user = User.query.filter_by(username=username).first()
                stock = Stock.query.filter_by(user=user, symbol=stkSym).delete()
                db.session.commit()
            else:
                flash('Enter correct stock.')
                return redirect(url_for('dashboard'))
        return render_template('sell.html',username=username,data=Stock.query.filter_by(user_id=userid).all())


@app.route('/view', methods = ['POST','GET'])
def view():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    else:
        if request.method == 'GET' :
            userid = session['user_id']
            username = session['username']
            myStockData = Stock.query.filter_by(user_id=userid).all()
            myStocks = []
            for stocks in myStockData:
                myStocks.append(stocks.symbol)
            endDate = date.today()
            startDate = endDate - relativedelta(years = 9)
            dfs=[]

            for stockSym in myStocks:          
                df = nse.stock_df(stockSym,startDate,endDate)
                dfs.append(df)

            candlestick_chart = gc(dfs,myStocks)
            
            return render_template('stock.html',cc = candlestick_chart)
        else:
            return redirect(url_for('dashboard'))

 
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        if request.method == 'POST':
            val = request.form.get('operationType')
            if(val == 'view'):
                return redirect(url_for('view'))
            elif(val == 'buy'):
                return redirect(url_for('buy'))
            else:
                return redirect(url_for('sell'))
        userid = session['user_id']
        username = session['username']
        return render_template('newDash.html',username=username,nifty50= NIFTY50, stocks=Stock.query.filter_by(user_id=userid).all())

    else:
        flash('Please LOGIN!')
        return redirect(url_for('index'))
    
@app.route('/stock/<stkName>',methods=['GET','POST'])
def stock(stkName):

    if 'user_id' in session:
        username = session['username']
        timeInterval = request.form.get('interval')
        endDate = date.today()
        startDate = endDate - relativedelta(years = 9)
        df = nse.stock_df(stkName,startDate,endDate)
        df = df.set_index('DATE')

        if timeInterval == 'weekly':
            # df['DATE'] = pd.to_datetime(df['DATE'])
            # df = df.set_index('DATE')
            df = df.resample('W')
            
        elif timeInterval == 'monthly':
            # df['DATE'] = pd.to_datetime(df['DATE'])
            # df = df.set_index('DATE')
            df = df.resample('M')
        
        # df = df.reset_index()
        print(df)
        candlestick_chart = generate_candlestick_chart(df)
        return render_template('stock.html',cc= candlestick_chart,stock=stkName)

    else:
        flash('Please LOGIN!')
        return redirect(url_for('index'))

def generate_candlestick_chart(df):
    candlestick_trace = go.Candlestick(x=df.index,
                                       open=df['OPEN'],
                                       high=df['HIGH'],
                                       low=df['LOW'],
                                       close=df['CLOSE'])

    layout = go.Layout(title='Price vs Time', xaxis=dict(title='Date'), yaxis=dict(title='Price'),height=800)

    figure = go.Figure(data=[candlestick_trace], layout=layout)
    return figure.to_html(full_html=False)


@app.route('/stocks',methods=['GET','POST'])
def stocks():
    stockSyms = ["SBIN","HDFC"]
    dfs = []
    if 'user_id' in session:
        username = session['username']
        if request.method == 'GET':
            endDate = date.today()
            startDate = endDate - relativedelta(years = 9)
            for stockSym in stockSyms:          
                df = nse.stock_df(stockSym,startDate,endDate)
                dfs.append(df)


            candlestick_chart = gc(dfs,stockSyms)
            
            return render_template('stock.html',cc= candlestick_chart)

        else:
            return redirect(url_for('index')) 
    else:
        flash('Please LOGIN!')
        return redirect(url_for('index'))

def gc(dfs,stockSyms):
    i = 0
    candlestick_traces = []
    for df in dfs:
        candlestick_trace = go.Candlestick(x=df['DATE'],
                                        open=df['OPEN'],
                                        high=df['HIGH'],
                                        low=df['LOW'],
                                        close=df['CLOSE'],name=stockSyms[i])
        candlestick_traces.append(candlestick_trace)
        i = i+1
    layout = go.Layout(title='Candlestick Chart', xaxis=dict(title='Date'), yaxis=dict(title='Price'),height=800)

    figure = go.Figure(data=candlestick_traces, layout=layout)
    return figure.to_html(full_html=False)

@app.route('/NIFTY50')
def nifty():
    df = pd.read_csv('NIFTY.csv')
    candlestick_chart = generate_candlestick_chart(df)
    return render_template('stock.html',cc= candlestick_chart,stock="NIFTY50")


if __name__ == '__main__':
    app.run(debug=True)
