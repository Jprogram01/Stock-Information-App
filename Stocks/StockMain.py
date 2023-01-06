import requests
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
class API:
    def __init__(self, ticker, begin_date, end_date):
            self.ticker = ticker
            self.begin_date = begin_date
            self.end_date = end_date
    '''
    This API returns base information about the ticker, and also financial results but in its own dictionary
    I only care about the information found in the results dictionary.
    method grabs information from the API
    '''
    def get_information(self, ticker, begin_date, end_date):
        '''
        #Makes a request to the API, it returns a dictionary with some of the information you made the request with,
        one of the variables in that dictionary is an additonal dictionary with all the information from each day within
        time frame, so that dictionary is assiged to a variable.
        '''
        global stock_info_results
        address = (f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{begin_date}/{end_date}?adjusted=true&sort=asc&limit=50000&apiKey=zkqS6MdY0v_NEPowYD8ipKLh6cE6Hdka")
        response = requests.get(address)
        stock_info = (response.json())
        # stock_info_results = stock_info["results"]
        # count = 0
        '''
        The API gives a UTC time instead of a date, so this takes the UTC time, converts it to a date, and then 
        rewrites the UTC variable with the date instead
        '''
        # for i in stock_info_results:
        #     time = stock_info["results"][0+count]["t"]
        #     time = time/1000
        #     utc_date = time
        #     datetime_obj = datetime.utcfromtimestamp(int(utc_date))
        #     date = (datetime_obj.strftime("%m/%d/20%y"))
        #     stock_info["results"][0+count]["t"] = date
        #     count = count + 1
        # return stock_info
        try:
            stock_info_results = stock_info["results"]
        except:
                print("error!!")
        else:
            stock_info_results = stock_info["results"]
            count = 0
            '''
            The API gives a UTC time instead of a date, so this takes the UTC time, converts it to a date, and then 
            rewrites the UTC variable with the date instead
            '''
            for i in stock_info_results:
                time = stock_info["results"][0+count]["t"]
                time = time/1000
                utc_date = time
                datetime_obj = datetime.utcfromtimestamp(int(utc_date))
                date = (datetime_obj.strftime("%m/%d/20%y"))
                stock_info["results"][0+count]["t"] = date
                count = count + 1
                error = False
            return stock_info
#Class used to find both the best and worst day in terms of price over the alotted time frame,
class Day:
        def __init__(self, date, price):
            self.date = date
            self.price = price
        def bestday(self):
            print(f"The highest price for {API.ticker} was {self.price} on {self.date}")
        def worstday(self):
            print(f"The lowest price for {API.ticker} was {self.price} on {self.date}")
class Stock:
    #basic info from the API and calculation with the api
    def __init__(self, results):

        self.results = results
    def date_caculations(self,results ):
        #Variables for the information each day
        count = 0
        bestday = Day(0, 0)
        worstday = Day(0, 0)
        '''
        This for loop iterates through each day in the given parameters for the dates
        while also keeping track of the day with the highest price and day with the lowest price
        '''

        for i in stock_info_results:
            time = results["results"][0+count]["t"]
            close_price = results["results"][0+count]["c"]
            count = count + 1
            if close_price > bestday.price:
                bestday.price = close_price
                bestday.date = time

            if close_price < worstday.price or worstday.price == 0:
                worstday.price = close_price
                worstday.date = time
        return bestday.date,bestday.price, worstday.date, worstday.price
    def data_collection(self, results):
        # #Puts all the info from the results into a table, both so it can be displayed as a table and also later graphed
        results_dictionary = results["results"]
        data = pd.DataFrame.from_dict(results_dictionary)
        data.columns = ["Trading Volume", "Volume Weighted Average", "OpenPrice", "ClosePrice", "HighPrice", "LowestPrice", "Date", "Number of Trans" ]
        graph = go.Figure(data=go.Candlestick (x=data.Date,
                open=data.OpenPrice,
                high=data.HighPrice,
                low=data.LowestPrice,
                close=data.ClosePrice,
                ))
            
        # graph.write_image("images/fig1.png")
        return graph
        # graph.show()
    # def image(self, graph):
    #     graph.write_image("graph.png")
        