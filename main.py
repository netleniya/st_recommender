from itertools import permutations
from pathlib import Path

import pandas as pd
import streamlit as st
from recommend import recommend_books_to_readers, recommend_readers_for_book


def create_pairs(col) -> pd.DataFrame:
    """create_pairs Given a dataframe column, create a pair of items that are frequently seen together

    Args:
        col (_type_): dataframe column

    Returns:
        pd.DataFrame: pandas dataframe
    """

    return pd.DataFrame(list(permutations(col, 2)), columns=["book_a", "book_b"])

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

    user_list = df['userId'].unique().tolist()
    book_list = df['title'].unique().tolist()
    isbn_list = df['isbn13'].unique().tolist()

    st.title("Book Recommandation Web App")
    st.text(
        """Welcome to the Book Recommender. Please choose one of the following roles:
        1. Unregistered User: You have no profile in the system, and will only get non-personalized recommendations
        2. Registered User: You have an active profile, and will get recommendations based on your past reading habits
        3. Librarian: Recommend a book to a group of select readers who might be interested in it.
        """)

    role = st.radio("Choose your role:", ("Unregistered User", "Registered User", "Librarian"))

    if role == "Unregistered User":
        st.header("Welcome, Stranger!")
        bookname = st.selectbox(label="Enter Book title to get non-personalized recommendations", options=book_list)
        st.subheader("Recommendations")
        st.text(f"Top ten books frequently read with `{bookname}`")
        book_rec = return_book_pairs(df, book_title = bookname)
    elif role == "Registered User":
        user_id = _create_menu(
            "Welcome back!",
            "Please enter your User ID, and we can recommend some books",
            "The following books might be of interest",
            options=user_list
        )
        book_rec = recommend_books_to_readers(user_id=user_id)
    else:
        isbn = _create_menu(
            "Master Librarian",
            "Please enter an ISBN to recommend a book to new readers",
            "The following 5 users might be interested in that book",
            options=isbn_list
        )
        book_rec = recommend_readers_for_book(isbn=isbn)

    if startAnalysis := st.sidebar.button("Get Recommendations"):
        st.write(book_rec)


# TODO #1 Rename this here and in `main`
def _create_menu(arg0, label, options, arg2):
    st.header(arg0)
    result = st.selectbox(label=label, options=options)
    st.subheader(arg2)
    return result


if __name__ == "__main__":
    main()
