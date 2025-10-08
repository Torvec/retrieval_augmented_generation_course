#!/usr/bin/env python3

import argparse
import json
import string
from nltk.stem import PorterStemmer


def strip_punctuation(text):
    punctuation = string.punctuation
    table = str.maketrans("","", punctuation)
    return text.translate(table)

def handle_stopwords(text):
    processed_list = []
    with open('data/stopwords.txt', 'r') as f:
        content = f.read()
        stopwords = set(content.splitlines())
    for t in text:
        if t in stopwords:
            continue
        else:
            processed_list.append(t)
    return processed_list

def search(query, limit):
    results = []
    stemmer = PorterStemmer()
    
    with open('data/movies.json', 'r') as f:
        movies_dict = json.load(f)

    for movie in movies_dict["movies"]:

        if len(results) >= limit:
            break

        raw_title = movie["title"]
        stripped_query = strip_punctuation(query.lower()).split()
        stripped_title = strip_punctuation(raw_title.lower()).split()
        processed_query = handle_stopwords(stripped_query)
        processed_title = handle_stopwords(stripped_title)

        match_found = False
        for q_word in processed_query:
            for t_word in processed_title:
                if stemmer.stem(q_word) in stemmer.stem(t_word):
                    match_found = True
                    break
            if match_found:
                break
        
        if match_found:
            results.append(raw_title)

    return results

def print_search_results(results):
    for i in range(len(results)):
        print(f'{i+1}. {results[i]}')

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            results = search(args.query, 5)
            print(f'Searching for: {args.query}')
            print_search_results(results)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()