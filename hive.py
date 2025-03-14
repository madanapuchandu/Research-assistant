import arxiv
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def build_query(keyword: str) -> str:
    """
    Constructs an arXiv search query with improved accuracy.

    Args:
        keyword (str): User-provided keyword.

    Returns:
        str: A formatted query string for arXiv search.
    """
    keyword = keyword.strip().lower()
    
    # Search in title, abstract, and categories
    query = f"ti:\"{keyword}\" OR abs:\"{keyword}\" OR cat:\"{keyword}\""
    return query

def search_arxiv(query: str, max_results: int = 10) -> List[arxiv.Result]:
    """
    Searches arXiv for papers matching the given refined query.

    Args:
        query (str): The structured search query.
        max_results (int): Maximum number of results to retrieve.

    Returns:
        List[arxiv.Result]: A list of arXiv search results.
    """
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance  # Prioritize relevance
        )
        results = list(search.results())
        
        if not results:
            logging.info("No relevant results found for the query: %s", query)
        
        return results
    except Exception as e:
        logging.error("Error occurred while searching arXiv: %s", str(e))
        return []

def display_results(results: List[arxiv.Result]) -> None:
    """
    Displays the search results in a structured format.

    Args:
        results (List[arxiv.Result]): List of arXiv search results.
    """
    if not results:
        print("\nNo relevant results found.")
        return

    for result in results:
        print("\n" + "=" * 80)
        print(f"Title: {result.title}")
        print(f"Authors: {', '.join(author.name for author in result.authors)}")
        print(f"Published: {result.published.strftime('%Y-%m-%d')}")
        print(f"Category: {', '.join(result.categories)}")
        print(f"URL: {result.entry_id}")
    print("=" * 80)

def main() -> None:
    """Main function to run the arXiv search."""
    keyword = input("Enter a keyword for arXiv search: ").strip()
    if not keyword:
        logging.warning("No keyword entered. Exiting.")
        return

    query = build_query(keyword)
    results = search_arxiv(query)
    display_results(results)

if __name__ == "__main__":
    main()
