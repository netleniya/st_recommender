from itertools import permutations
import pandas as pd


def create_pairs(col) -> pd.DataFrame:
    """create_pairs Given a dataframe column, create a pair of items that are frequently seen together

    Args:
        col (_type_): dataframe column

    Returns:
        pd.DataFrame: pandas dataframe
    """
    pairs = pd.DataFrame(list(permutations(col, 2)), columns=["book_a", "book_b"])
    return pairs

def return_book_pairs(library : pd.DataFrame, book_title : "str") -> None:
    """Take a dataframe and book title as inputs, and return the top 10 books most frequently paired with the book

    Args:
        library (pd.DataFrame): dataframe containing all books
        book_title (str): title of book user is looking for
    """


    book_pairs = library.groupby("userId")["title"].apply(create_pairs).reset_index(drop=True)
    pair_counts = book_pairs.groupby(["book_a", "book_b"]).size()
    counts_df = pair_counts.to_frame(name="size").reset_index().sort_values(by="size", ascending=False)
    true_pairs = counts_df[counts_df["book_a"] != counts_df["book_b"]]

    print(true_pairs[true_pairs["book_a"] == book_title].nlargest(10, "size"))

def main() -> None:
    df = pd.read_parquet("dataframes/work_df")
    return_book_pairs(df, book_title = "Harry Potter And The Goblet Of Fire")

if __name__ == "__main__":
    main()
