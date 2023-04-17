from itertools import permutations
from pathlib import Path
import pandas as pd
import streamlit as st


def create_pairs(col) -> pd.DataFrame:
    """create_pairs Given a dataframe column, create a pair of items that are frequently seen together

    Args:
        col (_type_): dataframe column

    Returns:
        pd.DataFrame: pandas dataframe
    """

    pairs = pd.DataFrame(list(permutations(col, 2)), columns=["book_a", "book_b"])
    return pairs


def return_book_pairs(library : pd.DataFrame, book_title : "str") -> pd.DataFrame:
    """Take a dataframe and book title as inputs, and return the top 10 books most frequently paired with the book

    Args:
        library (pd.DataFrame): dataframe containing all books
        book_title (str): title of book user is looking for

    Returns:
        pd.DataFrame: pandas dataframe
    """

    book_pairs = library.groupby("userId")["title"].apply(create_pairs).reset_index(drop=True)
    pair_counts = book_pairs.groupby(["book_a", "book_b"]).size()
    counts_df = pair_counts.to_frame(name="size").reset_index().sort_values(by="size", ascending=False)
    true_pairs = counts_df[counts_df["book_a"] != counts_df["book_b"]]

    return true_pairs[true_pairs["book_a"] == book_title].nlargest(10, "size")


def main() -> None:

    file_path = Path("./dataframes/work_df").absolute()
    print(file_path)

    df = pd.read_parquet(file_path)

    st.title("Book Recommandation Web App")
    st.text("Welcome to our web app, designed to provide personalized book recommendations.")
    st.text("Please enter the book name and upload analyzing files and then press button to start.")
    startAnalysis = st.sidebar.button("Quick Recommend")

    st.header('Enter a book name')
    bookname = st.text_input(label = "Please enter a book name you like and we can start book recommandation from there" )

    if startAnalysis:
        st.subheader("Non-Personalized Recommendations")
        st.text(f"Top ten books frequently read with `{bookname}`")
        book_rec = return_book_pairs(df, book_title = bookname)
        st.write(book_rec)


if __name__ == "__main__":
    main()
