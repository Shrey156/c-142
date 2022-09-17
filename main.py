from flask import Flask, jsonify
import pandas as pd
from demographic import output
from content import get_recommendation

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

# extracting important information from dataframe
movies=movies_data[['original_title','poster_link','release_date','runtime','weighted_rating']]

# variables to store data
liked=[]
disliked=[]
not_watched=[]

# method to fetch data from database
def assign_value():
  m_data={
    'original_title':movies.iloc[0,0],
    'poster_link':movies.iloc[0,1],
    'release_date':movies.iloc[0,2] or 'N/A',
    'runtime':movies.iloc[0,3],
    'weighted_rating':movies.iloc[0,4]/2
  }
  return m_data

# /movies api
@app.route("/movies")
def get_movie():
  movie=assign_value()
  return  jsonify({
    'data':movie,
    'status':'success'
  })

# /like api
@app.route("/like")
def like_movie():
  global movies
  movie=assign_value()
  liked.append(movie)
  movies.drop([0],inplace=True)
  movies=movies.reset_index(drop=True)
  return  jsonify({
    'status':'success'
  })

# /dislike api
@app.route("/dislike")
def dislike_movie():
  global movies
  movie=assign_value()
  disliked.append(movie)
  movies.drop([0],inplace=True)
  movies=movies.reset_index(drop=True)
  return  jsonify({
    'status':'success'
  })

# /did_not_watch api
@app.route("/didnotwatch")
def did_not_watch():
  global movies
  movie=assign_value()
  not_watched.append(movie)
  movies.drop([0],inplace=True)
  movies=movies.reset_index(drop=True)
  return  jsonify({
    'status':'success'
  })

@app.route('/liked')
def like():
  global liked
  return jsonify({
    'data':liked,
    'status':'success'
  })

@app.route('/popular')
def popular1():
  movie_data=[]
  for index ,row in output.iterrows:
    data={
      'original_title' : row['original_title'],
       'poster_link' : row['poster_link'], 
       'runtime': row['runtime'], 
       'release_date' : row['release_date'] or 'N/A', 
       'weighted_rating': row['weighted_rating']/2
    }
    movie_data.append(data)
  return jsonify({
    'data':movie_data,
    'status':'success'
  })

@app.route('/recommend')
def recommend1():
  global liked
  column_names=['original_title' , 'poster_link' , 'runtime', 'release_date' , 'weighted_rating']
  all=pd.DataFrame(columns=column_names)
  for row in liked:
    output=get_recommendation(row['original_title'])
    all=all.append(output)
  all.drop_duplicates(subset=['original_title'],inplace=True)
  movie_data=[]
  for index ,row in all.iterrows:
    data={
      'original_title' : row['original_title'],
       'poster_link' : row['poster_link'], 
       'runtime': row['runtime'], 
       'release_date' : row['release_date'] or 'N/A', 
       'weighted_rating': row['weighted_rating']/2
    }
    movie_data.append(data)
  return jsonify({
    'data':movie_data,
    'status':'success'
  })


if __name__ == "__main__":
  app.run()