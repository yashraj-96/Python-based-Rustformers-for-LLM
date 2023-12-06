from llm_rs.langchain import RustformersLLM
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import requests
import chainlit as cl

API_URL = "http://localhost:8083/api/chat"

#chainlit code
@cl.on_chat_start
async def start():
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to DocEdge GPT. What is your query?"
    await msg.update()

@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    Args:
        message: The user's message.

    Returns:
        None.
    """

    # Fetch the reponse from a Rust server
    response = requests.post(API_URL, json={"prompt": message.content})

    if response.status_code == 200:
        result = response.json().get("response")

        print("Response : {}".format(result))

        # Send the final answer
        msg = cl.Message(content="OK : ")
        await msg.send()
    else:
        msg = cl.Message(content="Error: Failed to generate a response.")
        await msg.send()