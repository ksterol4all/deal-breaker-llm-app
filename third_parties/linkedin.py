import os
import requests
from dotenv import load_dotenv


load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url:str, mock:bool = False):
    """Scarpe infomration from LinkedIn profiles, 
    manually scrape the information from the LinkedIn profile
    """

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/ksterol4all/1fd4224400748ee0930ef494d32b5659/raw/1f1a98890eac6e6ffd3e74bc56f16f7a8770dd66/prasad-bankar-scrapin.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl":linkedin_profile_url
        }
        response = requests.get(url=api_endpoint, params=params, timeout=10)

    data = response.json().get("person")

    #remove redundant fields
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["recommendations", "testScores", "volunteeringExperiences"]
    }

    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/prasad-bankar-a4379b187/", mock=True)
    )