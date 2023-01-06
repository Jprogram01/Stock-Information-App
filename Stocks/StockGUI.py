from StockMain import *
import plotly.graph_objects as go
from tkinter import *  
import calendar
# import datetime
from datetime import *
def main():
    
    #All the global variables used throughout the project
    global root
    global send_ticker
    global send_begin_date
    global send_end_date
    global ticker_storage
    global begin_date_storage
    global end_date_storage
    global stock_info
    global ticker_string
    global begin_string
    global end_string
    global send_information_current
    global stock_results_display
    global stock_info_results
    global stock_data
    global image_display
    global image


    #Defines all the variables that'll be updated later
    send_ticker, send_begin_date, send_end_date, ticker_storage, begin_date_storage, end_date_storage = None, None,None,None,None,None
    root = Tk()
    stock_info_results = []
    stock_info = API(send_ticker, send_begin_date, send_end_date)
    stock_data = Stock(stock_info_results)
    white = PhotoImage(file = "white.png")


    #All the different tkinter widgets 
    ticker_message = Label(root, text="Enter Ticker" )
    begin_message = Label(root,text="Enter Beginning Date\n(In the format of YYYY-MM-DD)")
    end_message = Label(root,text="Enter Ending Date\n(In the format of YYYY-MM-DD)")
    button_message = Label(root, text="Display Information From\nA Set Time Frame:")
    custom_message = Label(root, text="Current Information")
    ticker_string = StringVar()
    begin_string = StringVar()
    end_string = StringVar()
    information_entry_ticker = Entry(root, textvariable= ticker_string, width=80, borderwidth=5)
    information_entry_begin = Entry(root, textvariable= begin_string, width=80, borderwidth=5)
    information_entry_end = Entry(root, textvariable=end_string, width=80, borderwidth=5)
    send_information_current = Text(root,height=3, width = 60)
    image_display = Label(image=white)
    
    

    #Inserts text into the different tkinter widgets.
    send_information_current.insert(1.0, f"Ticker:{send_ticker}\nBeginning Date:{send_begin_date}\nEnding Date:{send_end_date} ")
    information_entry_ticker.insert(0, "")
    information_entry_begin.insert(0, "")
    information_entry_end.insert(0, "")

    #Different buttons for the GUI
    ticker_Button = Button(root,text="Enter Ticker", padx = 20, pady= 20, width=15, command=lambda:get_ticker() )
    begin_Button = Button(root,text="Enter Beginning Date", padx = 20, pady= 20, width=15, command=lambda:get_begin() )
    end_Button = Button(root,text="Enter Ending Date", padx = 20, pady= 20, width=15, command=lambda:get_end() )
    send_information_Button = Button(root, text="Get Information", padx=0,pady=0, width=15, command=lambda:information_storage(send_ticker, send_begin_date, send_end_date))
    one_month_button = Button(root, text="One Month", pady=20, width=10, command=lambda:information_storage_set_time(send_ticker, 1))
    six_month_button = Button(root, text="Six Months", pady=20, width=10, command=lambda:information_storage_set_time(send_ticker, 6))
    one_year_button = Button(root, text="One Year", pady=20, width=10, command=lambda:information_storage_set_time(send_ticker, 12))
    two_year_button = Button(root, text="Two Years", pady=20, width=10, command=lambda:information_storage_set_time(send_ticker, 24))


    #Positioning for the GUI
    ticker_message.grid(row=0, column=0,padx=10,pady=10)
    information_entry_ticker.grid(row= 0, column = 1,padx=10,pady=10)
    ticker_Button.grid(row=0, column=2,columnspan=1,padx=10,pady=10)
    
    begin_message.grid(row=1, column=0,padx=10,pady=10)
    information_entry_begin.grid(row= 1, column = 1,padx=10,pady=10)
    begin_Button.grid(row=1, column=2,columnspan=1,padx=10,pady=10)

    end_message.grid(row=2, column=0,padx=10,pady=10)
    information_entry_end.grid(row= 2, column = 1,padx=10,pady=10)
    end_Button.grid(row=2, column=2,columnspan=1, padx=10,pady=10 )


    send_information_current.grid(row=3, column=1, padx=10,pady=10)
    send_information_current.config(state= "disabled")
    send_information_Button.grid(row=3,column=2,padx=10,pady=10)
    custom_message.grid(row=3, column=0)

 
    stock_results_display = Text(root,height=4,width=50)
    stock_results_display.grid(row=0, column=3, columnspan=4, padx=10,pady=10)
    stock_results_display.config(state= "disabled")
    

    image_display.grid(row=1,column=3, rowspan=3, columnspan=4, padx=10, pady=10)
    one_month_button.grid(row=4, column=3, padx=10, pady=10)
    six_month_button.grid(row=4, column=4, padx=10, pady=10)
    one_year_button.grid(row=4, column=5, padx=10, pady=10)
    two_year_button.grid(row=4, column=6, padx=10, pady=10)
    button_message.grid(row=4, column=2, padx=10, pady=10)

    #runs GUI
    root.mainloop()

#Functions to get the info out of the different textboxes into variables
def get_ticker(*args):
    ticker = ticker_string.get()
    ticker = ticker.upper()
    update_info(ticker, None, None)
def get_begin(*args):
    begin = begin_string.get()
    update_info(None,begin,None)
def get_end(*args):
    end = end_string.get()
    update_info(None,None,end)


#Function to transform the info from the different textboxes into variables that can be used to request info from an API
def update_info(ticker,begin,end):
    global send_ticker
    global send_begin_date
    global send_end_date
    global send_information_current
    if ticker != None:
        send_ticker = ticker
    if begin != None:
        send_begin_date = begin
    if end != None:
        send_end_date = end
    #Display's what info is currently stored in the different variables, so you can text different dates and tickers.
    send_information_current.config(state= "normal")
    send_information_current.delete(1.0, "end")
    send_information_current.insert(1.0, f"Ticker:{send_ticker}\nBeginning Date:{send_begin_date}\nEnding Date:{send_end_date} ")
    send_information_current.config(state= "disabled")

#Function to get variables to send to the API, and then display that information
def information_storage(ticker,begin_date,end_date):
    #converts the information from the different text boxed and stores in into variables 
    ticker_storage = ticker
    ticker_storage = ticker_storage.upper()
    begin_date_storage = begin_date
    end_date_storage = end_date

    #Uses a method from the API classes to get information from the stock API
    stock_info_results = stock_info.get_information(ticker_storage,begin_date_storage,end_date_storage)
    display_information(stock_info_results, begin_date, end_date, ticker)

def information_storage_set_time(ticker, amount):
    #Gets the ticker
    ticker_storage = ticker
    ticker_storage = ticker_storage.upper()
    #Gets the current date and converts it to a unix time
    date = datetime.utcnow()
    end_date_utc = calendar.timegm(date.utctimetuple())
    end_date_utc = float(end_date_utc)
    """
    This will take the current unix time and subtract it by whatever unix time gets you either
    one month, 6 months, one year, or two years. Then it will convert that unix time back into a date 
    which will then be sent to an API and preform all the data calculations then display the information.
    
    """
    if amount == 1:
        begin_date_utc = end_date_utc - 2588096
        datetime_obj = datetime.utcfromtimestamp(int(begin_date_utc))
        begin_date_storage = (datetime_obj.strftime("20%y-%m-%d"))
        begin_date_storage = str(begin_date_storage)
        datetime_obj = datetime.utcfromtimestamp(int(end_date_utc))
        end_date_storage = (datetime_obj.strftime("20%y-%m-%d"))
        end_date_storage=str(end_date_storage)
    if amount == 6:
        begin_date_utc = end_date_utc - 15635973
        datetime_obj = datetime.utcfromtimestamp(int(begin_date_utc))
        begin_date_storage = (datetime_obj.strftime("20%y-%m-%d"))
        begin_date_storage = str(begin_date_storage)
        datetime_obj = datetime.utcfromtimestamp(int(end_date_utc))
        end_date_storage = (datetime_obj.strftime("20%y-%m-%d"))
        end_date_storage=str(end_date_storage)
    if amount == 12:
        begin_date_utc = end_date_utc - 31532095
        datetime_obj = datetime.utcfromtimestamp(int(begin_date_utc))
        begin_date_storage = (datetime_obj.strftime("20%y-%m-%d"))
        begin_date_storage = str(begin_date_storage)
        datetime_obj = datetime.utcfromtimestamp(int(end_date_utc))
        end_date_storage = (datetime_obj.strftime("20%y-%m-%d"))
        end_date_storage=str(end_date_storage)
    if amount == 24:
        begin_date_utc = end_date_utc - 63068070
        datetime_obj = datetime.utcfromtimestamp(int(begin_date_utc))
        begin_date_storage = (datetime_obj.strftime("20%y-%m-%d"))
        begin_date_storage = str(begin_date_storage)
        datetime_obj = datetime.utcfromtimestamp(int(end_date_utc))
        end_date_storage = (datetime_obj.strftime("20%y-%m-%d"))
        end_date_storage=str(end_date_storage)
    # stock_info_results = stock_info.get_information(ticker_storage,begin_date_storage,end_date_storage)
    # display_information(stock_info_results, begin_date_storage, end_date_storage, ticker)\
    stock_info_results = stock_info.get_information(ticker_storage,begin_date_storage,end_date_storage)
    display_information(stock_info_results, begin_date_storage, end_date_storage, ticker)
    
    # try:
    #     stock_info_results = stock_info.get_information(ticker_storage,begin_date_storage,end_date_storage)
    #     display_information(stock_info_results, begin_date_storage, end_date_storage, ticker)
    # except KeyError:
    #     display_information_error()


    
    


def display_information(stock_results,begin_date, end_date, ticker):
    global image_display
    global image
    stock_info_results = stock_results
    #Uses information from the API and uses a method from the Stock class to calculate the date with the best price and date with the worst price, then display it.
    best_day_display, best_price_display, worst_day_display, worst_price_display = (stock_data.date_caculations(stock_info_results))
    stock_results_display.config(state= "normal")
    stock_results_display.delete(1.0, "end")
    stock_results_display.insert(1.0,f"The day with the best price was:{best_day_display}\nThe price for that day was: {best_price_display}\nThe day with the worst price was:{worst_day_display}\nThe price for that day was:{worst_price_display}" )
    stock_results_display.config(state= "disabled")
    #Uses information from the API and uses a method from the Stock class to put the information into a table and also graphs it
    graph = stock_data.data_collection(stock_info_results)
    graph.update_layout(
    xaxis_rangeslider_visible=False,
    margin=dict(l=0,r=0,b=0,t=0),
    )
    graph.update_xaxes(title_text=f"Dates from {begin_date} to {end_date}")
    graph.update_yaxes(title_text=f"Price of {ticker} stock")

    #Saves the graph as an image and displays it
    graph.write_image("graph.png", width=500, height=300)
    image = PhotoImage(file = "graph.png")
    image_display.configure(image=image)
def display_information_error():
    stock_results_display.insert(1.0, "Error: Please check to see if the\ninformation entered was correct" )


    
    


if __name__ == "__main__":
    main()