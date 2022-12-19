import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
from tkinter import *

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


cv = CountVectorizer()
# <----Transformin "Combined Features" sesries of data frame into a count matrix so that we compare all the movie's with each other
count_matrix = cv.fit_transform(movie["combined_features"])

# Using Cosine Similarity Algo to find similarity b/w all the movies. The value close to one indicate more similarity
cosine_sim = cosine_similarity(count_matrix) 


def Restart(moive_list_gui):
    moive_list_gui.destroy()
    Start()


def Exit(start):
    start.destroy()

def title_from_index(index):
    return movie[movie.index == index]["title"].values[0]

def displayListofMovies(start,list_of_similar_movies):
    start.destroy()
    movie_list_gui=Tk()
    movie_list_gui.title("Movie Recommender")
    movie_list_gui.geometry("800x600")
    bgimg= PhotoImage(file = "mrbg.png")
    Label(movie_list_gui,image=bgimg).place(x=0,y=0)
    listbox=Listbox(movie_list_gui, height = 25,
                  width = 40,fg="black")
    Label(movie_list_gui,text="this islist page").pack()
    i=0
    for rec_movie in list_of_similar_movies:
            if(i!=0):
                # Label(movie_list_gui,text=i).pack()
                # Label(movie_list_gui,text=title_from_index(rec_movie[0])).pack()
                listbox.insert(i,title_from_index(rec_movie[0]))
            i=i+1
            if i>20:
                break
    listbox.pack()
    Button(movie_list_gui,text="Go Back",command=lambda:Restart(movie_list_gui)).pack()


def send_sim_movies(movie_index):
    similar_movies =  list(enumerate(cosine_sim[movie_index]))
    # <----Sorting the list in descending order---->
    similar_movies_sorted = sorted(similar_movies,key=lambda x:x[1],reverse=True)
    return similar_movies_sorted


def index_from_title(title):
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
    print(titlesim)
    # print(movie[movie.title == titlesim]["index"].values[0])
    return movie[movie.title == titlesim]["index"].values[0]




def submitMovieName(start,movie_name_var):
    user_movie_name=movie_name_var.get()
    movie_index = index_from_title(user_movie_name)
    list_of_similar_movies=send_sim_movies(movie_index)
    displayListofMovies(start,list_of_similar_movies)




def Start():
    start=Tk()
    start.title("Moiver Recommender")
    start.geometry("800x600")
    # start.config(background = "#1cb5bd",)
    bgimg= PhotoImage(file = "mrbg.png")
    Label(start,image=bgimg).place(x=0,y=0)
    Label(start,text="Enter a movie Name",fg="black").pack(pady=80)
    movie_name_var=StringVar()
    Entry(start,textvariable=movie_name_var,fg="black").pack()
    Button(start,text="Get list of Movies",command=lambda:submitMovieName(start,movie_name_var),fg="black").pack(pady=10)
    Button(start,text="Exit",command=lambda:Exit(start)).pack(pady=10)
    start.mainloop()



Start() # Starting the code





