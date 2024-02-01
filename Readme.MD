COP290 Assignment 1 Task 2

ANUP LAL NAYAK 2022CS51827
LUCKY AHIRWAR 2022CS52049

OBJECTIVE:

The objective of this assignment is to build a user interface consisting of the following features:
1. Plot the graph of a given stock on a defined time scale (daily, weekly etc)
2. Plot multiple stocks on the same graph to visually compare the prices.
3. Apply technical filters to get a list of stocks passing the filters ( average
price etc.)

We built a user interface similar to trading platforms like GROWW / ZERODHA.
Every logged in user can have their own PORTFOLIO.
A user can REGISTER/LOGIN and BUY/SELL stocks into/from his PORTFOLIO.

DESIGN DECISIONS:

Used Flask BluePrints to keep the code for different parts such as - Filter, NIFTY50, User Dashboard etc. to maintain code efficiently and ail scalability as it also makes it easier for other developers to understand the code.

Used appropriate self describing variable names everywhere in python so as to aid easy understanding of code.

SQLAlchemy keeps a Stocks database that is linked to the User database via a foreign key, this allows us to save the portfolio in the database for every user.

We used 
Plotly to plot the graphs.
Jugaad-data for Indian stocks.
Yfinance for some US stocks.
SQLAlchemy for saving user stocks.
Pandas dataframe to help resampling in case the viewer wants to see weekly, monthly data.


FUNCTIONALITIES:

Every logged in user can have their own PORTFOLIO.

They can add (BUY) stocks in their portfolio, remove (SELL) stocks from their portfolio, VIEW the stocks from their portfolio in a graph which has both options -
i) see daily, weekly, monthly based data.
ii) see 6 months, 1 year, 3 years etc data.

They can visually compare prices of multiple stocks by viewing multiple stocks at the same graph in a line graph. They can choose which stocks to view at one time by switching display for certain stocks on or off.

The user can view NIFTY50 stocks’ data from the Navigation bar itself.
The user can choose to filter stocks on the basis of its average price.
These stock list includes the list of US stocks.

The user can click on any stock from dashboard and see it’s data.

TRADE OFFS:

SPACE vs TIME
Giving user the option to select from all stocks in dashboard and see its graph requires our program to fetch the data of the stock everytime, this sometimes leads to slow webpade load. We made this decision of fetching and loading data everytime, instead of storing all the data with us because although storing 50 stocks data might not take much space, but we want this website to be scalable, which means it could be expanded to hundreds of stocks and storing their data would not be a good decision then. Storing data would also mean we will loose out on dynamic data control, since with our current implementation the data shown is live and updated with recent changes.



Filtering based on average
This required us to load the stocks’ data from finance everytime the user asks the list of stocks which are above a threshold average, this leads to fetching of lots of irrelevant and unused data that takes up a lot of time. We could not find a way around it since we still didnt want to store the data for those stocks somewhere.
