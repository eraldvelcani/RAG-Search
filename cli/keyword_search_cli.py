#!/usr/bin/env python3

from nltk.stem import PorterStemmer
import argparse
import json
import string

def main() -> None:
    stemmer = PorterStemmer()

    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f'Searching for: {args.query}');
        case _:
            parser.print_help()
    
    with open('data/movies.json', 'r') as f:
        movies_dict = json.load(f)
    
    with open('data/stopwords.txt', 'r') as g:
        stopwords_list = g.read().splitlines()

    new_dict = {}
    cleaned_query = (args.query).translate(str.maketrans('', '', string.punctuation)).lower()

    for movie in movies_dict['movies']:
        cleaned_movie_title = movie['title'].translate(str.maketrans('', '', string.punctuation)).lower()

        tokenized_query = list(filter(None, cleaned_query.split()))
        tokenized_title = list(filter(None, cleaned_movie_title.split()))
        
        stopwordless_query = [w for w in tokenized_query if w not in stopwords_list]
        stopwordless_title = [w for w in tokenized_title if w not in stopwords_list]

        if any(q in t for q in stopwordless_query for t in stopwordless_title):
            new_dict[movie['title']] = movie
    
    sorted_dict = sorted(new_dict.values(), key=lambda m: m['id'])
    for count, movie in enumerate(sorted_dict[:5], start=1):
        print(f"{count}. {movie['title']}")


if __name__ == "__main__":
    main()
