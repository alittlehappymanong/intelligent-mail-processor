from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


def get_llm():

    os.environ['OPENAI_API_BASE'] = 'https://api.ohmygpt.com/v1/'
    os.environ['OPENAI_API_KEY'] = 'sk-SIMz5BFx1457F6af0d1DT3BLbkFJE43943ea051c4Ad6925D'
    # os.environ['OPENAI_API_KEY'] = 'sk-KMg0EfQ3CC0A151D99c1T3BLbKFJD46c81384d494f73be84'


    model = 'gpt-4o-mini'

    return ChatOpenAI(model=model, temperature=0.1, verbose=True)  


