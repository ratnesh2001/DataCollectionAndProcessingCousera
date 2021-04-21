import requests_with_caching
import json

def get_movies_from_tastedive(movie_name):
    kvp = {'q': movie_name, 'type': 'movies', 'limit': 5}
    resp = requests_with_caching.get("https://tastedive.com/api/similar", params = kvp)
    result = resp.json()
    return result

def extract_movie_titles(dict):
    movie_list = []
    for i in dict['Similar']['Results']:
        movie_list.append(i['Name'])
    return movie_list

def get_related_titles(movie_list):
    final_list = []
    for i in movie_list:
        temp_list = extract_movie_titles(get_movies_from_tastedive(i))
        final_list = final_list + temp_list
        final_list = list( dict.fromkeys(final_list) )
    return final_list

def get_movie_data(title):
    kvp = {'t': title, 'r': 'json'}
    data = requests_with_caching.get("http://www.omdbapi.com/", params = kvp)
    return data.json()

def get_movie_rating(data):
    for i in data['Ratings']:
        if i['Source'] == 'Rotten Tomatoes':
            return int(i['Value'][:-1])
    return 0

def get_sorted_recommendations(movie_list):
    related_movies = get_related_titles(movie_list)
    related_movies = sorted(related_movies, key = lambda movieName: (get_movie_rating(get_movie_data(movieName)), movieName), reverse=True)
    return related_movies
get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

