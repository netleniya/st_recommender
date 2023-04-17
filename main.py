import pandas as pd
import streamlit as st

from recommend import recommend_books_to_readers, recommend_readers_for_book
from itertools import permutations
from pathlib import Path


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

    role = st.radio("Choose your role", ("Registered User", "Unregistered User", "Librarian"))

    if role == "Unregistered User":
        st.header("Welcome, Stranger! ")
        bookname = st.text_input(label = "Please enter a book name you like and we can start book recommandation from there" )
        st.subheader("Non-Personalized Recommendations")
        st.text(f"Top ten books frequently read with `{bookname}`")
        book_rec = return_book_pairs(df, book_title = bookname)
    elif role == "Registered User":
        st.header("Welcome back!")
        user_id = st.number_input(label="Please enter your User ID, and we can recommend some books")
        st.subheader("The following books might be of interest")
        book_rec = recommend_books_to_readers(user_id=user_id)
    else:
        st.header("Hello, Master Librarian")
        isbn = st.number_input(label="Please enter an ISBN to recommend a book to new readers")
        st.subheader("The following 5 users might be interested in that book")
        book_rec = recommend_readers_for_book(isbn=isbn)

    startAnalysis = st.sidebar.button("Get Recommendations")

    if startAnalysis:
        st.write(book_rec)


if __name__ == "__main__":
    main()
