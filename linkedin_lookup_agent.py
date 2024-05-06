
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub
from tools import get_profile_url_tavily

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo-0125', 
        temperature=0)
    
    template = """given the full name {name_of_person} I want you to get me a link to thier linkedin profile page.
        Your answer should contain only a URL"""
        
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the LinkedIn Page URL"
        )
    ]    
    
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    
    linked_profile_url = result["output"]
    return linked_profile_url
    
    
    
    
    
if __name__ == "__main__":
    linkedin_url = lookup(name="Jeffery Inman Booz")    
    # return "https://gist.githubusercontent.com/jinman36/2e6195537e362197ade2f6804dbf3184/raw/3606249159b0d79903afa882949367e8c817349d/ji_test.json"