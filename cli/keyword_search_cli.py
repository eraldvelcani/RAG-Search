#!/usr/bin/env python3

import argparse
import json

def main() -> None:
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
   
    new_dict = {}
    
    for movie in movies_dict['movies']:
        if args.query in movie['title']:
            new_dict[movie['title']] = movie
    
    sorted_dict = sorted(new_dict.values(), key=lambda m: m['id'])[:5]
    for count, movie in enumerate(sorted_dict, start=1):
        print(f"{count}. {movie['title']}")


if __name__ == "__main__":
    main()
