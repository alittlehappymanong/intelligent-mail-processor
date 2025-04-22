import os
from langchain_openai import ChatOpenAI
from entities import ticket_repo
from process_module import generators
from process_module import validators
from process_module import identifiers
from mailbox_module import mailbox_processor
from entities import mail_repo
# class LLMConn:
#     chat_model = None
#     def __init__(self):
#         self.chat_model = self.get_llm()
#         self.tool_bind()
#
#     pass

    # def tool_bind(self):
    #     self.chat_model.bind_tools([TicketRepo.update_ticket_assignee])
def  get_llm():

    os.environ['OPENAI_API_BASE'] = 'https://api.ohmygpt.com/v1/'
    os.environ['OPENAI_API_KEY'] = 'sk-SIMz5BFx1457F6af0d1DT3BLbkFJE43943ea051c4Ad6925D'
    # os.environ['OPENAI_API_KEY'] = 'sk-KMg0EfQ3CC0A151D99c1T3BLbKFJD46c81384d494f73be84'

    model = 'gpt-4o-mini'
    chat_model = ChatOpenAI(model=model, temperature=0.1, verbose=True)

    return chat_model

def  get_llm_with_tools():

    os.environ['OPENAI_API_BASE'] = 'https://api.ohmygpt.com/v1/'
    os.environ['OPENAI_API_KEY'] = 'sk-SIMz5BFx1457F6af0d1DT3BLbkFJE43943ea051c4Ad6925D'
    # os.environ['OPENAI_API_KEY'] = 'sk-KMg0EfQ3CC0A151D99c1T3BLbKFJD46c81384d494f73be84'

    model = 'gpt-4o-mini'
    chat_model = ChatOpenAI(model=model, temperature=0.1, verbose=True)
    chat_model.bind_tools([])

    return chat_model

from langchain.chat_models import init_chat_model
def get_chat_model():

    os.environ['OPENAI_API_BASE'] = 'https://api.ohmygpt.com/v1/'
    os.environ['OPENAI_API_KEY'] = 'sk-SIMz5BFx1457F6af0d1DT3BLbkFJE43943ea051c4Ad6925D'
    # os.environ['OPENAI_API_KEY'] = 'sk-KMg0EfQ3CC0A151D99c1T3BLbKFJD46c81384d494f73be84'
    # Construct the tool calling agent

    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    llm.bind_tools([])
    return llm

from langchain.agents import AgentExecutor, create_tool_calling_agent
def get_agent():
    os.environ['OPENAI_API_BASE'] = 'https://api.ohmygpt.com/v1/'
    os.environ['OPENAI_API_KEY'] = 'sk-SIMz5BFx1457F6af0d1DT3BLbkFJE43943ea051c4Ad6925D'
    # os.environ['OPENAI_API_KEY'] = 'sk-KMg0EfQ3CC0A151D99c1T3BLbKFJD46c81384d494f73be84'
    # Construct the tool calling agent

    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    tools = []
    # Construct the tool calling agent
    # agent = create_tool_calling_agent(llm, tools, prompt)