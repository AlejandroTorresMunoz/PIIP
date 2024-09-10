from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.schema.agent import AgentFinish

class plot_ticker_input(BaseModel):
    ticker : str = Field(..., description="Name of the ticker.")

@tool(args_schema=plot_ticker_input)
def plot_ticker(ticker : str)->str:
    """Plot the data of a specified ticker/stock.
    """
    return f"Here is the value of the ticker : {ticker}"


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


