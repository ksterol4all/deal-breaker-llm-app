from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(search_qry: str):
    """Searches for LinkedIn or Twitter Profile Page."""

    search = TavilySearchResults()
    response = search.run(f"{search_qry}")

    return response