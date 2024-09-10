from langchain_core.tools import tool

@tool
def plot_ticker(ticker : str)->str:
    """Plot the data of a specified ticker/stock.
    
    Args : 
        ticker (str) : Name of the ticker.
    """
    return f"Se debería plotear el valor del ticker : {ticker}"


