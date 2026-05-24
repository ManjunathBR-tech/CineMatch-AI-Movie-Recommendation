from database import db, cursor


# =========================================
# REGISTER USER
# =========================================

def register_user(username, password):

    query = """
    INSERT INTO users(username, password)
    VALUES(%s, %s)
    """

    values = (username, password)

    try:

        cursor.execute(query, values)

        db.commit()

        return True

    except:

        return False


# =========================================
# LOGIN USER
# =========================================

def login_user(username, password):

    query = """
    SELECT * FROM users
    WHERE username=%s AND password=%s
    """

    values = (username, password)

    cursor.execute(query, values)

    user = cursor.fetchone()

    return user
# =========================================
# SAVE FAVORITE MOVIE
# =========================================

def save_favorite(user_id, movie_title):

    query = """
    INSERT INTO favorites(user_id, movie_title)
    VALUES(%s, %s)
    """

    values = (
        user_id,
        movie_title
    )

    cursor.execute(query, values)

    db.commit()


# =========================================
# GET FAVORITES
# =========================================

def get_favorites(user_id):

    query = """
    SELECT movie_title
    FROM favorites
    WHERE user_id=%s
    """

    values = (user_id,)

    cursor.execute(query, values)

    favorites = cursor.fetchall()

    return favorites