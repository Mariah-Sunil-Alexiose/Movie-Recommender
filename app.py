from flask import Flask, render_template, request
from logging import debug
import joblib
import numpy as np
import pandas as pd
import difflib

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        movie_name = request.form.get('movie')
        movies_data = pd.read_csv('movies.csv')
        similarity = joblib.load('model')
        list_of_all_titles = movies_data['title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 
        i = 0   
        movies={}   
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movies_data[movies_data.index==index]['title'].values[0]
            if (i<30):
                i+=1 
                movies[i]=title_from_index
        return render_template('prediction.html', movies=movies)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)