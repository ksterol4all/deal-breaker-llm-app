import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor)
from langchain import hub
from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name:str) -> str:
    llm_OpenAI = ChatOpenAI(temperature=0, model_name="gpt-4o")

    template = """Given the full name "{name_of_person}", find the most relevant LinkedIn profile for this person.
                Your response must contain only a single valid LinkedIn profile URL, and no other text.
                Do not provide multiple options or commentary."""

    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

    tools_for_agent = [
        Tool(name="Crawl Google for linkedin profile page", func=get_profile_url_tavily, description="useful for when you need to get linkedin Page URL")
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm_OpenAI, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)

    response = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})

    profile_url = response["output"]

    return profile_url


if __name__ == "__main__":
    linkedIn_url = lookup(name="Ayobami Adewole")
    print(linkedIn_url)