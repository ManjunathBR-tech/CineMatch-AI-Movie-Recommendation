import matplotlib.pyplot as plt
from collections import Counter
import ttkbootstrap as tb
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

from recommender import recommend
from poster import get_movie_poster

from login import (
    register_user,
    login_user,
    save_favorite,
    get_favorites
)

# =========================================
# MAIN WINDOW
# =========================================

app = tb.Window(themename="cyborg")

app.title("🎬 CineMatch")

app.geometry("1500x850")

app.configure(bg="black")

current_user = None


# =========================================
# CLEAR WINDOW
# =========================================

def clear_window():

    for widget in app.winfo_children():

        widget.destroy()


# =========================================
# SEARCH MOVIE
# =========================================

def search_movie():

    movie_name = movie_entry.get()

    if movie_name == "":

        messagebox.showerror(
            "Error",
            "Please enter a movie name"
        )

        return

    # CLEAR OLD RECOMMENDATIONS

    recommendation_list.delete(0, END)

    # GET RECOMMENDATIONS

    movies = recommend(movie_name)

    for movie in movies:

        recommendation_list.insert(
            END,
            movie
        )

    # =====================================
    # SHOW POSTER
    # =====================================

    poster_url = get_movie_poster(movie_name)

    if poster_url:

        try:

            headers = {
              "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(
            poster_url,
            headers=headers,
            timeout=10
              )



            img_data = response.content

            img = Image.open(
                BytesIO(img_data)
            )

            img = img.convert("RGB")

            img = img.resize(
                (300, 450)
            )

            photo = ImageTk.PhotoImage(img)

            poster_label.config(
                image=photo,
                text=""
            )

            poster_label.image = photo

        except Exception as e:

            print("Poster Error:", e)

            poster_label.config(
                image="",
                text="Poster Not Found",
                fg="white",
                bg="black",
                font=("Segoe UI", 16)
            )

    else:

        poster_label.config(
            image="",
            text="Poster Not Found",
            fg="white",
            bg="black",
            font=("Segoe UI", 16)
        )


# =========================================
# ADD TO FAVORITES
# =========================================

def add_to_favorites():

    movie_name = movie_entry.get()

    if movie_name == "":

        messagebox.showerror(
            "Error",
            "Enter movie name"
        )

        return

    save_favorite(
        current_user,
        movie_name
    )

    messagebox.showinfo(
        "Success",
        "❤️ Movie Saved to Favorites"
    )


# =========================================
# SHOW FAVORITES
# =========================================

def show_favorites():

    favorites = get_favorites(
        current_user
    )

    recommendation_list.delete(0, END)

    for movie in favorites:

        recommendation_list.insert(
            END,
            movie[0]
        )

# =========================================
# ANALYTICS DASHBOARD
# =========================================

def show_analytics():

    # CLEAR OLD LIST

    recommendation_list.delete(0, END)

    # LOAD MOVIES DATA

    import pandas as pd

    movies = pd.read_csv("movies.csv")

    # GET ALL GENRES

    genres = []

    for genre in movies["genres"]:

        genre_list = genre.split("|")

        genres.extend(genre_list)

    # COUNT GENRES

    genre_count = Counter(genres)

    # TOP 10 GENRES

    top_genres = genre_count.most_common(10)

    genre_names = [
        item[0]
        for item in top_genres
    ]

    genre_values = [
        item[1]
        for item in top_genres
    ]

    # SHOW IN LISTBOX

    recommendation_list.insert(
        END,
        "🎬 TOP MOVIE GENRES"
    )

    recommendation_list.insert(
        END,
        "===================="
    )

    for genre, count in top_genres:

        recommendation_list.insert(
            END,
            f"{genre} : {count}"
        )

    # PLOT GRAPH

    plt.figure(figsize=(10, 6))

    plt.bar(
        genre_names,
        genre_values
    )

    plt.title(
        "Top Movie Genres"
    )

    plt.xlabel(
        "Genres"
    )

    plt.ylabel(
        "Count"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()
# =========================================
# MAIN APP UI
# =========================================

def open_main_app():

    clear_window()

    # SIDEBAR

    sidebar = Frame(
        app,
        bg="#111111",
        width=250
    )

    sidebar.pack(
        side=LEFT,
        fill=Y
    )

    sidebar.pack_propagate(False)

    # LOGO

    logo = Label(
        sidebar,
        text="🎬 CineMatch",
        font=("Segoe UI", 24, "bold"),
        fg="#bb86fc",
        bg="#111111"
    )

    logo.pack(pady=30)

    # MENU

    menu = Label(
        sidebar,
        text="🍿 MENU",
        font=("Segoe UI", 16, "bold"),
        fg="white",
        bg="#111111"
    )

    menu.pack(pady=20)

    # DASHBOARD BUTTON

    dashboard_btn = tb.Button(
        sidebar,
        text="🏠 Dashboard",
        bootstyle="secondary-outline",
        width=20
    )

    dashboard_btn.pack(pady=10)

    # MOVIES BUTTON

    movies_btn = tb.Button(
        sidebar,
        text="🎥 Movies",
        bootstyle="secondary-outline",
        width=20
    )

    movies_btn.pack(pady=10)

    # FAVORITES BUTTON

    favorites_btn = tb.Button(
        sidebar,
        text="❤️ Favorites",
        bootstyle="secondary-outline",
        width=20,
        command=show_favorites
    )

    favorites_btn.pack(pady=10)

    # ANALYTICS BUTTON

    analytics_btn = tb.Button(
        sidebar,
        text="📊 Analytics",
        bootstyle="secondary-outline",
        width=20,
        command=show_analytics
    )

    analytics_btn.pack(pady=10)

    # LOGOUT BUTTON

    logout_btn = tb.Button(
        sidebar,
        text="🚪 Logout",
        bootstyle="danger-outline",
        width=20,
        command=show_login_page
    )

    logout_btn.pack(pady=30)

    # CONTENT

    content = Frame(
        app,
        bg="black"
    )

    content.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )

    # TITLE

    title = Label(
        content,
        text="🌌 AI Movie Recommendation Engine",
        font=("Segoe UI", 32, "bold"),
        fg="#bb86fc",
        bg="black"
    )

    title.pack(pady=20)

    # SEARCH BOX

    global movie_entry

    movie_entry = tb.Entry(
        content,
        width=50,
        font=("Segoe UI", 14)
    )

    movie_entry.pack(pady=15)

    # SEARCH BUTTON

    search_btn = tb.Button(
        content,
        text="🔍 Recommend Movies",
        bootstyle="info-outline",
        width=25,
        command=search_movie
    )

    search_btn.pack(pady=10)

    # SAVE FAVORITE BUTTON

    favorite_btn = tb.Button(
        content,
        text="❤️ Save Favorite",
        bootstyle="danger-outline",
        width=25,
        command=add_to_favorites
    )

    favorite_btn.pack(pady=10)

    # MAIN FRAME

    main_frame = Frame(
        content,
        bg="black"
    )

    main_frame.pack(pady=20)

    # LEFT FRAME

    left_frame = Frame(
        main_frame,
        bg="black"
    )

    left_frame.grid(
        row=0,
        column=0,
        padx=30
    )

    # RECOMMEND LABEL

    recommend_label = Label(
        left_frame,
        text="🎯 Recommended Movies",
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg="black"
    )

    recommend_label.pack(pady=15)

    # RECOMMEND LIST

    global recommendation_list

    recommendation_list = Listbox(
        left_frame,
        width=50,
        height=18,
        bg="#1a1a1a",
        fg="white",
        font=("Segoe UI", 13),
        selectbackground="#bb86fc",
        selectforeground="black"
    )

    recommendation_list.pack()

    # RIGHT FRAME

    right_frame = Frame(
        main_frame,
        bg="black"
    )

    right_frame.grid(
        row=0,
        column=1,
        padx=30
    )

    # POSTER TITLE

    poster_title = Label(
        right_frame,
        text="🎬 Movie Poster",
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg="black"
    )

    poster_title.pack(pady=15)

    # POSTER LABEL

    global poster_label

    poster_label = Label(
        right_frame,
        bg="black"
    )

    poster_label.pack()

    # FOOTER

    footer = Label(
        content,
        text="🚀 Powered by AI + TMDB API",
        font=("Segoe UI", 12),
        fg="#00ff99",
        bg="black"
    )

    footer.pack(pady=15)


# =========================================
# LOGIN PAGE
# =========================================

def show_login_page():

    clear_window()

    login_frame = Frame(
        app,
        bg="#111111",
        width=500,
        height=500
    )

    login_frame.place(
        relx=0.5,
        rely=0.5,
        anchor=CENTER
    )

    # TITLE

    title = Label(
        login_frame,
        text="🎬 CineMatch Login",
        font=("Segoe UI", 28, "bold"),
        fg="#bb86fc",
        bg="#111111"
    )

    title.pack(pady=30)

    # USERNAME

    username_label = Label(
        login_frame,
        text="Username",
        font=("Segoe UI", 14),
        fg="white",
        bg="#111111"
    )

    username_label.pack(pady=10)

    username_entry = tb.Entry(
        login_frame,
        width=35,
        font=("Segoe UI", 12)
    )

    username_entry.pack(pady=10)

    # PASSWORD

    password_label = Label(
        login_frame,
        text="Password",
        font=("Segoe UI", 14),
        fg="white",
        bg="#111111"
    )

    password_label.pack(pady=10)

    password_entry = tb.Entry(
        login_frame,
        width=35,
        show="*",
        font=("Segoe UI", 12)
    )

    password_entry.pack(pady=10)

    # LOGIN FUNCTION

    def login():

        global current_user

        username = username_entry.get()

        password = password_entry.get()

        user = login_user(
            username,
            password
        )

        if user:

            current_user = user[0]

            messagebox.showinfo(
                "Success",
                "🎉 Login Successful"
            )

            open_main_app()

        else:

            messagebox.showerror(
                "Error",
                "❌ Invalid Credentials"
            )

    # REGISTER FUNCTION

    def register():

        username = username_entry.get()

        password = password_entry.get()

        success = register_user(
            username,
            password
        )

        if success:

            messagebox.showinfo(
                "Success",
                "✅ Registration Successful"
            )

        else:

            messagebox.showerror(
                "Error",
                "Username already exists"
            )

    # LOGIN BUTTON

    login_btn = tb.Button(
        login_frame,
        text="🔐 Login",
        bootstyle="success-outline",
        width=25,
        command=login
    )

    login_btn.pack(pady=20)

    # REGISTER BUTTON

    register_btn = tb.Button(
        login_frame,
        text="📝 Register",
        bootstyle="info-outline",
        width=25,
        command=register
    )

    register_btn.pack(pady=10)


# =========================================
# START APP
# =========================================

show_login_page()

app.mainloop()