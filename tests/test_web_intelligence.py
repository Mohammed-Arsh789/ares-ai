from tools.web_intelligence import WebIntelligence


def main():

    web = WebIntelligence()

    result = web.search(
        "Python programming language",
        max_results=3,
    )

    if hasattr(result, "success"):

        if not result.success:

            print(
                "WEB SEARCH FAILED:"
            )

            print(
                result.error
            )

            return

    print(
        "QUERY:"
    )

    print(
        result["query"]
    )

    print()

    print(
        "RESULTS:"
    )

    for item in result["results"]:

        print(
            f"{item['score']:.2f} | "
            f"{item['title']} | "
            f"{item['url']}"
        )

    print()

    print(
        "SOURCES:"
    )

    for source in result["sources"]:

        print(
            source
        )


if __name__ == "__main__":
    main()