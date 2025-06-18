from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup


def ice_breaker_runner(name: str) -> str:
    

    summary_template = """
        given the LinkedIn information {information} about a person from, I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm_OpenAI = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    llm_Ollama = ChatOllama(model="llama3.2")
    llm_Mistral = ChatOllama(model="mistral")

    chain = summary_prompt_template | llm_OpenAI | StrOutputParser()

    linkedIn_url = lookup(name=name)
    linkedin_data = scrape_linkedin_profile(linkedIn_url)

    res = chain.invoke(input={"information": linkedin_data})

    print(res)

if __name__ == "__main__":
    print("Ice Breaker Enter")
    ice_breaker_runner("ayobami adewole calgary alberta")

    
