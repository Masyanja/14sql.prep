import sqlite3
from flask import Flask, request, render_template
# connection = sqlite3.connect('netflix.db')

# cursor = connection.cursor()
# query = """
#         SELECT title, country, release_year, description
#         FROM netflix
#         WHERE title = '1994'
# """
#
# cursor.execute(query)
#
# for row in cursor.fetchall():
#     print(row)

app = Flask(__name__)

@app.route("/movie/<title_for_search>")
def movie_by_title(title_for_search):
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    query = f"""
            SELECT title, country, release_year, description
            FROM netflix
            WHERE title = {title_for_search}
    """
    cursor.execute(query)
    return render_template('output_movies.html', data=cursor.fetchall())

@app.route("/movie/<yearfrom>/to/<yearto>")
def movie_by_year_range(yearfrom, yearto):
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE {yearfrom} <= release_year AND {yearto} >= release_year
            AND type = 'Movie'
            LIMIT 10
    """
    cursor.execute(query)
    return render_template('year-range.html', data=cursor.fetchall())

@app.route("/rating/children")
def movie_for_children():
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating = 'G'
    """
    cursor.execute(query)
    return render_template('rating.html', data=cursor.fetchall())


@app.route("/rating/family")
def movie_for_family():
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating in ('G', 'PG', 'PG-13')
    """
    cursor.execute(query)
    return render_template('rating.html', data=cursor.fetchall())

@app.route("/rating/adult")
def movie_for_adult():
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating in ('R', 'NC-17')
    """
    cursor.execute(query)
    return render_template('rating.html', data=cursor.fetchall())

@app.route("/genre/<genre>")
def movie_by_genre(genre):
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10
    """
    cursor.execute(query)
    return render_template('genre.html', data=cursor.fetchall())


app.run()