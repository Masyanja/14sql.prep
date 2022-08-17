import sqlite3
import json

def get_value_from_db(sql):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()

        return result


def search_double_name(name1, name2):
    connection =  sqlite3.connect('netflix.db')
    cursor = connection.cursor()

    sql = f'SELECT "cast" FROM netflix where "cast" LIKE "%{name1}%" OR "cast" LIKE "{name2}"'
    result = []
    cursor.execute(sql)
    #print(cursor.fetchall())

    names_dict = {}
    for item in get_value_from_db(sql=sql):
        names = set(dict(item).get('cast').split(",")) - set([name1, name2])

    for name in names:
        names_dict[str(name).strip()] = names_dict.get(str(name).strip(), 0) + 1
    print(names_dict)
    for key, value in names_dict.items():
        if value >= 1:
            result.append(key)
    return result

def step_6(typ, year, genre):
    sql = f"""
          SELECT title, description, listed_in
          FROM netflix
          WHERE type = '{typ}'
          AND release_year = '{year}'
        AND listed_in LIKE '%{genre}%'
    """

    result = []

    for item in get_value_from_db(sql):
        result.append(dict(item))

    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    print(search_double_name('Rose McIver', 'Ben Lamb'))
    print(step_6('Movie', '2021', 'Documentaries'))