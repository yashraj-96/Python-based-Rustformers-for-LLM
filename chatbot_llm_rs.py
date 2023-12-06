from llm_rs.langchain import RustformersLLM
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import chainlit as cl

template="""Below is an instruction that describes a task. Write a response that appropriately completes the request.
### Instruction:
{instruction}
### Response:
Answer:"""

prompt = PromptTemplate(input_variables=["instruction"],template=template,)

llm = RustformersLLM(model_path_or_repo_id="rustformers/open-llama-ggml",model_file="open_llama_3b-f16.bin",callbacks=[StreamingStdOutCallbackHandler()])

#chain.run("Describe yourself in 100 words")

#chainlit code
@cl.on_chat_start
async def start():
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to DocEdge GPT. What is your query?"
    await msg.update()

    qa_chain = LLMChain(llm=llm, prompt=prompt)
    cl.user_session.set("chain", qa_chain)


@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    Args:
        message: The user's message.

    Returns:
        None.
    """
    chain = cl.user_session.get("chain") 
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message.content, callbacks=[cb])

    # Send the final answer
    await cl.Message(content=res).send()