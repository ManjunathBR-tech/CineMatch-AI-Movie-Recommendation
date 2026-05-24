import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics.pairwise import cosine_similarity


# ======================================
# LOAD DATASET
# ======================================

movies = pd.read_csv("movies.csv")


# ======================================
# USE GENRES AS FEATURES
# ======================================

count = CountVectorizer(
    stop_words="english"
)

count_matrix = count.fit_transform(
    movies["genres"]
)


# ======================================
# COSINE SIMILARITY
# ======================================

similarity = cosine_similarity(
    count_matrix
)


# ======================================
# RECOMMEND FUNCTION
# ======================================

def recommend(movie_name):

    movie_name = movie_name.lower().strip()

    recommendations = []

    # SEARCH MOVIE

    matched_movies = movies[
        movies["title"].str.lower().str.contains(
            movie_name,
            na=False
        )
    ]

    # IF MOVIE NOT FOUND

    if matched_movies.empty:

        return ["Movie not found"]

    # GET FIRST MATCH

    movie_index = matched_movies.index[0]

    # GET SIMILARITY SCORES

    similarity_scores = list(
        enumerate(similarity[movie_index])
    )

    # SORT MOVIES

    sorted_movies = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # TOP 5 RECOMMENDATIONS

    for movie in sorted_movies[1:6]:

        index = movie[0]

        title = movies.iloc[index]["title"]

        recommendations.append(title)

    return recommendations