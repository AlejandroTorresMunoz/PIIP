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

class plot_ticker_input(BaseModel):
    ticker : str = Field(..., description="Name of the ticker.")
    start_date : str = Field(default=None, description="Start date of the graph.")
    end_date : str = Field(default=None, description="End date of the graph.")
    interval : str = Field(default="1d", description="Time granularity of the graph.")

@tool(args_schema=plot_ticker_input)
def plot_ticker(ticker : str, start_date : str = "1d", end_date : str = "1d", interval : str = "1d"):
    """
    Plot the data of a specified ticker/stock.
    Args : 
        -   ticker (str) : Ticker to get the financial data from
        -   period (str) : Optional input. Time horizont of the plot.
        -   start_date (str) : Optional input. Start date of the graph.
    """
    
    if start_date is None or start_date.strip()=="":
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    else:
        start_date = dateparser.parse(start_date)
        start_date = start_date.strftime('%Y-%m-%d')
    if end_date is None or start_date.strip()=="":
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        end_date = dateparser.parse(end_date)
        end_date = end_date.strftime('%Y-%m-%d')
    print("Los valores que ha interpretado la función de LLM son los siguientes : ")
    print(ticker)
    print(start_date)
    print(end_date)
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, interval=interval)
    
    if data.empty:
        # Ticker doesn't exist
        return f"The ticker {ticker} doesn't exist."
    else:
        #TODO : Plot a graph in the streamlit page    
        print("Mostrando gráfica")
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


