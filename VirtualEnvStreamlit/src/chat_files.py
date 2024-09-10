from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field

@tool
def plot_ticker(ticker : str)->str:
    """Plot the data of a specified ticker/stock.
    
    Args : 
        ticker (str) : Name of the ticker.
    Returns:
        str : Text indicating which ticker is going to be plotted.
    """
    return f"Here is the value of the ticker : {ticker}"


