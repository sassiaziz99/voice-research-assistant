import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

TEST_QUERY = "who won the world cup 2026?"


def search(query: str):
    response = client.search(
        query = query, 
        search_depth = "basic",
        max_results = 5,
        include_answer = True,
    )
    return response


if __name__ == "__main__":
    result = search(TEST_QUERY)
    
    print("Tavily quick answer: ")
    print(result.get("answer"))
    print("\nTop sources:")
    
    for item in result["results"]:
        print(f"- {item['title']} ({item['url']})")
        print(f" {item['content'][:150]}...")
        
        
        