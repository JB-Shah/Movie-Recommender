  
# importing Requuired Libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import tkinter as tk
root = tk.Tk()
root.title('Movie Recommender')
root.geometry("600x400")

# <--Function to get input of the movie name enterd by the User--->
def submitMovieName():
    name=movie_name_var.get()
    return name
# <----GUI using Tkinter--->
heading=tk.Label(root,text="Enter A  Movie Name",font=('Times New Roman',20,'bold'))
movie_name_var=tk.StringVar()
user_movie_entry= tk.Entry(root,textvariable = movie_name_var, font=('Times New Roman',10,'normal'))
sub_btn=tk.Button(root,text = 'Submit', command = submitMovieName)

# <---Styling--->
heading.grid(row=0,column=0)
user_movie_entry.grid(row=1,column=0)
sub_btn.grid(row=1,column=1)

root.mainloop()

def title_from_index(index):
    return movie[movie.index == index]["title"].values[0]

def index_from_title(title):
    # <-----Correcting Errors in File--->
    indexes=['index']
    for index in indexes:
      movie[index]=movie[index].fillna(-1)
    movie["index"]=movie["index"].astype('int64')

    # <----Making List of all titles of movie---->
    title_list = movie['title'].tolist()
    # <---Correcting Errors in File ---->
    for t in range(len(title_list)):
      if type(title_list[t])=='float':
        title_list[t]=" "
    # <----DiffLib--->
    common = difflib.get_close_matches(title, title_list,1)
    titlesim = common[0]
    return movie[movie.title == titlesim]["index"].values[0]

# <----Reading the CSV File--->
movie = pd.read_csv(r"./4000 Movies Data Final.csv")
# <----Filling 'NA' with an empty string----->
# Correcting Errors in The File
movie['title']=movie['title'].fillna('')
# Combining Various Attributes
features = ['keywords','cast','genres','director']
for feature in features:
    # <----Filling 'NA' with an empty string----->
  # Correcting Errors in The File
    movie[feature] = movie[feature].fillna('')




def combine_features(row):
    try:
        return row['keywords'] +" "+row['cast']+" "+row['genres']+" "+row['director']
    except:
        print ("Error:", row)

movie["combined_features"] = movie.apply(combine_features,axis=1)

# <----Invoking the CountVectoriser Function--->
cv = CountVectorizer()
# <----Transformin "Combined Features" sesries of data frame into a count matrix so that we compare all the movie's with each other
count_matrix = cv.fit_transform(movie["combined_features"])

# Using Cosine Similarity Algo to find similarity b/w all the movies. The value close to one indicate more similarity
cosine_sim = cosine_similarity(count_matrix) 



user_movie=submitMovieName()
movie_index = index_from_title(user_movie)


# <---Creatng List of Similar Movies---->
similar_movies =  list(enumerate(cosine_sim[movie_index]))
# <----Sorting the list in descending order---->
similar_movies_sorted = sorted(similar_movies,key=lambda x:x[1],reverse=True)
# <---Printing the movies which the user might be interested in---->
i=0
print("\nOther movies you might be interested in:-\n")
for rec_movie in similar_movies_sorted:
        if(i!=0):
            print (i,") ",title_from_index(rec_movie[0]),sep="")
        i=i+1
        if i>20:
            break
