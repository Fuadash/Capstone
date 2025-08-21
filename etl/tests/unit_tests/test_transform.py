import pandas as pd
import pytest
from src.transform.transform import (
    transform,
    clean_nulls,
    enrich_reviews,
    enrich_platforms,
    enrich_tags,
    get_sentiment,
)


# Test mock/fixture made by chatgpt
@pytest.fixture
def sample_df():
    sample_df = pd.DataFrame(
        {
            "AppID": [1, 2, None],
            "Name": ["Game A", "Game B", "Game C"],
            "Release date": ["2020-01-01", "2019-05-05", "2021-07-07"],
            "Peak CCU": [1000, 200, None],
            "Required age": [0, 18, 10],
            "Price": [9.99, 150.0, 0.0],
            "Supported languages": ["['English']", "[]", "['English','French']"],
            "Full audio languages": ["['English']", "['English']", None],
            "Windows": [True, True, False],
            "Mac": [False, True, False],
            "Linux": [False, False, True],
            "Metacritic score": [80, 70, None],
            "Positive": [100, 10, 0],
            "Negative": [20, 5, 0],
            "Recommendations": [50, 2, 0],
            "Tags": [None, "Action, Indie", None],
        }
    )
    extra_cols = [
        "Discount",
        "DLC count",
        "Header image",
        "Achievements",
        "Average playtime forever",
        "Average playtime two weeks",
        "Median playtime forever",
        "Median playtime two weeks",
        "Screenshots",
        "Movies",
        "Score rank",
        "User score",
        "Estimated owners",
        "About the game",
        "Reviews",
        "Website",
        "Support url",
        "Support email",
        "Metacritic url",
        "Publishers",
    ]
    for col in extra_cols:
        sample_df[col] = None
    return sample_df


def test_clean_nulls(sample_df):
    result = clean_nulls(sample_df, ["AppID", "Name"])
    assert result["AppID"].isna().sum() == 0
    assert result["Name"].isna().sum() == 0
    assert "Game C" not in result["Name"].values


def test_enrich_reviews(sample_df):
    df = enrich_reviews(sample_df.copy())
    assert "Positive %" in df.columns
    assert "Sentiment" in df.columns
    # Check positive percentage calculation
    assert df.loc[0, "Positive %"] == round((100 / (100 + 20)) * 100)
    # Check sentiment categories
    assert df.loc[0, "Sentiment"] in [
        "Positive",
        "Very Positive",
        "Overwhelmingly Positive",
        "Mixed",
        "Negative",
        "Mostly Negative",
        "Very Negative",
        "Overwhelmingly Negative",
        "No Reviews",
    ]


def test_get_sentiment_logic():
    row = {"Positive %": 96, "Total": 1000}
    assert get_sentiment(row) == "Overwhelmingly Positive"

    row = {"Positive %": 50, "Total": 100}
    assert get_sentiment(row) == "Mixed"

    row = {"Positive %": pd.NA, "Total": 0}
    assert get_sentiment(row) == "No Reviews"


def test_enrich_platforms(sample_df):
    df = enrich_platforms(sample_df.copy())
    assert "Available platforms" in df.columns
    assert df.loc[0, "Available platforms"] == "Windows"
    assert "Mac" in df.loc[1, "Available platforms"]


def test_enrich_tags(sample_df):
    df = enrich_tags(sample_df.copy())
    assert "Tags" in df.columns
    assert df.loc[0, "Tags"] == "No user-submitted tags available"
    assert df.loc[1, "Tags"] == "Action, Indie"


def test_transform_pipeline(tmp_path, sample_df):
    # This is fascinating technology, built-in fixture that creates a temp path
    output_csv = tmp_path / "processed.csv"
    result_df = transform(sample_df.copy(), output_csv=str(output_csv))

    # check file is created
    assert output_csv.exists()

    # check filtering worked: row with Price=150 removed
    assert (result_df["Price"] > 100).sum() == 0

    # check age restricted field exists
    assert "Age restricted" in result_df.columns
    assert set(result_df["Age restricted"].unique()) <= {True, False} # <= is subset operator

    # check final enrichments exist
    assert "Sentiment" in result_df.columns
    assert "Available platforms" in result_df.columns
    assert "Tags" in result_df.columns
