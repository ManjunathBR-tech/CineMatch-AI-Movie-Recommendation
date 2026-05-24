import requests
from urllib.parse import quote


API_KEY = "0154e21d87473ebd6e27a963328a04b7"


# =========================================
# GET MOVIE POSTER
# =========================================

def get_movie_poster(movie_name):

    try:

        # CLEAN MOVIE NAME

        clean_name = movie_name.split("(")[0].strip()

        # URL ENCODE

        encoded_name = quote(clean_name)

        # TMDB API URL

        url = (
            f"https://api.themoviedb.org/3/search/movie"
            f"?api_key={API_KEY}&query={encoded_name}"
        )

        response = requests.get(url)

        data = response.json()

        results = data.get("results")

        if results:

            poster_path = results[0].get(
                "poster_path"
            )

            if poster_path:

                full_url = (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

                print(full_url)

                return full_url

        return None

    except Exception as e:

        print("Poster Error:", e)

        return None