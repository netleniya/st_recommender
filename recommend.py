from pathlib import Path
from typing import Union

import pandas as pd

user_recs = pd.read_parquet(Path("./dataframes/recommend_books").absolute())
book_recs = pd.read_parquet(Path("./dataframes/recommend_readers").absolute())
database = pd.read_parquet(Path("./dataframes/work_df").absolute())


def recommend_books_to_readers(user_id: Union[int, float]) -> pd.DataFrame:
    df = database.merge(user_recs, on=["bookId"], how="left")
    print(f"Book recommendations for user with id {user_id}:")
    return df[df["targetId"] == user_id][["title", "isbn13", "language"]].drop_duplicates(keep='first')


def recommend_readers_for_book(isbn: Union[int, float]) -> pd.DataFrame:
    df = database[database["isbn13"] == isbn].merge(book_recs, on=["bookId"]).drop_duplicates(["targetId"])
    return df[["title", "targetId"]]
