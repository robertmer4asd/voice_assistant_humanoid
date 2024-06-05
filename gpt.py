import wikipedia

def search_wikipedia(query):
    try:
        # Search Wikipedia for the query
        search_results = wikipedia.search(query, results=1)

        if search_results:
            # Fetch the summary of the first search result
            page_summary = wikipedia.summary(search_results[0], sentences=2)
            return page_summary
        else:
            return "Sorry, I couldn't find any relevant information."

    except wikipedia.exceptions.DisambiguationError as e:
        # If there are multiple options for the search query
        first_option = e.options[0]
        page_summary = wikipedia.summary(first_option, sentences=2)
        return page_summary

    except wikipedia.exceptions.PageError:
        # If the search query does not match any Wikipedia page
        return "Sorry, I couldn't find any relevant information."

# Example usage
query = "What is the capital of France?"
answer = search_wikipedia(query)
print("Answer:", answer)
