"""
Methods and tools to be executed by the chatbot
"""

from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.schema.agent import AgentFinish
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
import datetime
import dateparser
from typing import Optional

ACCEPTED_INTERVALS_PLOT = {"1m" : "Each minute", 
                           "2m" : "Each 2 minute", 
                           "5m" : "Each 5 minute", 
                           "15m" : "Each 15 minutes", 
                           "30m" : "Each 30 minutes", 
                           "60m" : "Each 60 minutes, or each hour", 
                           "90m" : "Each 90' minutes, or each hour and a half", 
                           "1h" : "Each hour",
                           "1d" : "Each day", 
                           "5d" : "Each 5 days", 
                           "1wk" : "Each week", 
                           "1mo" : "Each month", 
                           "3mo": "Each 3 months"}

class plot_ticker_input(BaseModel):
    ticker : str = Field(..., description="Name of the ticker.")
    start_date : Optional[str] = Field(default=None, description="Start date of the graph in format YYYY-MM-DD.")
    end_date : Optional[str] = Field(default=None, description="End date of the graph in format YYYY-MM-DD.")
    interval : str = Field(default="1d", description=f"Time granularity/intercals of the graph. The accepted values are the keys of this dictionary : {ACCEPTED_INTERVALS_PLOT}")

@tool(args_schema=plot_ticker_input)
def plot_ticker(ticker : str, 
                start_date : str = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'), 
                end_date : str = datetime.datetime.now().strftime('%Y-%m-%d'), 
                interval : str = "1d"):
    """
    Plot the data of a specified ticker/stock.
    Args : 
        -   ticker (str) : Ticker to get the financial data from
        -   period (str) : Optional input. Time horizont of the plot.
        -   start_date (str) : Optional input. Start date of the graph.
    """    

    print(f"El start_date introducido es el siguiente : {start_date}")
    print(f"El end_date introducido es el siguiente : {end_date}")
    print(f"El interval introducido es el siguiente : {interval}")


    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, interval=interval)
    
    
    if data.empty:
        # Ticker doesn't exist
        return f"There's been an error getting the values of the ticker : {ticker}"
    else:
        #TODO : Plot a graph in the streamlit page    
        fig, axs = plt.subplots()
        axs.plot(data.index, data['Close'], label="Close Price")
        axs.set_label("Date")
        axs.set_label("Price")
        axs.set_title(f"{ticker} Price History")
        axs.legend()
        # Plot the graph in Streamlit
        st.pyplot(fig)
        return f"Here is the plot of the ticker : {ticker}."


def route(result):
    """
    Method executed at the end of the chain to return a proper text answer
    """
    if len(result.content) > 0:
        return result.content
    else:
        func_to_call = result.response_metadata['message']['tool_calls'][0]['function']['name']
        input_args = result.response_metadata['message']['tool_calls'][0]['function']['arguments']
        tools = {
            "plot_ticker": plot_ticker, 
        }
        return tools[func_to_call].run(input_args)


