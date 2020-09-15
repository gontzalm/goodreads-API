import argparse
import pandas as pd
import re

DATASET_PATH = "output/books_enriched.csv"
SORT_DICT={
    "rating": "Average Rating",
    "pages": "Num Pages",
    "ratings_count": "Ratings Count",
    "title": "Title",
    "reviews_count": "Text Reviews Count"
}

def parse_argumets():
    """
    Parse arguments passed by user.
    
    Args:
        None.
    
    Returns:
        args: Parsed argments. 
    """
    parser = argparse.ArgumentParser(description="Show top rated books.")
    parser.add_argument(
        "-t",
        dest="topic",
        default=None,
        help="Filter by topic."
    )
    parser.add_argument(
        "-r",
        dest="min_rating",
        type=float,
        default=None,
        help="Filter by minimum average rating."
    )
    parser.add_argument(
        "-c",
        dest="min_count",
        type=int,
        default=None,
        help="Filter by minimum ratings count."
    )
    parser.add_argument(
        "-s",
        dest="sort",
        choices=["rating", "pages", "ratings_count", "title", "reviews_count"],
        default="title",
        help="If 1, perform aggregations."
    )
    parser.add_argument(
        "-a",
        dest="aggregate",
        action="store_true",
        help="If specified, perform aggregations."
    )
    parser.add_argument(
        "--no-a",
        dest="aggregate",
        action="store_false",
    )
    parser.add_argument(
        "-l",
        dest="list",
        type=int,
        default=10,
        help="Number of books to list."
    )
    args = parser.parse_args()
    return args


def load_books():
    """
    Load books data as a dataframe.
    
    Args:
        None.
    
    Returns:
        books (pd.DataFrame): Books dataset. 
    """
    books = pd.read_csv(DATASET_PATH, index_col="ISBN")
    return books


def filter_books(data, args):
    """
    Filter books data by parsed arguments.
    
    Args:
        data (pd.DataFrame): Books dataset.
        args (parsed args): Parsed arguments.
    
    Returns:
        books (pd.DataFrame): Books dataset. 
    """
    if args.topic:
        topic = " ".join(args.topic.split("_"))
        mask = data["Title"].str.contains(rf"{topic}", flags=re.IGNORECASE)
        data = data[mask]
    
    if args.min_rating:
        data = data[data["Average Rating"] > args.min_rating]

    if args.min_count:
        data = data[data["Ratings Count"] > args.min_count]

    return data


def sort_books(data, args):
    """
    Sort books data by parsed argument.
    
    Args:
        data (pd.DataFrame): Books dataset.
        args (parsed args): Parsed arguments.
    
    Returns:
        books (pd.DataFrame): Books dataset. 
    """
    data.sort_values(SORT_DICT[args.sort], ascending=False, inplace=True)
    return data


def aggregate_books(data):
    """
    Aggregate books data.
    
    Args:
        data (pd.DataFrame): Books dataset.
    
    Returns:
        books (pd.Series): Aggregated dataset. 
    """
    data = data.describe()
    return data