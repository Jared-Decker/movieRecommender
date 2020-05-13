#Author:        Jared Decker
#Date:          4/6/2020
#Project:       IMDB recommender

'''
All code for IMDB recommender version 1.0
'''

import os
import csv
import gzip
import re
import numpy
from collections import deque
import operator

#dataset filename
dataFile = "data.csv"

#empty lists
fields = []
rows = []
genres = set([])
actors = set([])

#scores holds the calculated compatability score for every movie that has a score > 0
scores = {}

#extract zipped data into the titles directory
print("\nExtracting Dataset...")
with open(dataFile, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    #capture field names
    fields = next(reader)

    for row in reader:
        rows.append(row)

#split genres and actors into sublists. add entries to sets.
for row in rows:
    row[2] = row[2].split(',')
    genres.update(row[2])

    row[5] = row[5].split(',')
    actors.update(row[5])

'''
-------------------Genre Search Protocols--------------------
'''
def genreSearch(genres):
    #creating an empty dictionary that will be switched on for genre selection
    switcher = {}

    #list of liked genres
    chosen_genres = []

    print("There are " + str(len(genres)) +" genres present in the top 1000 films. They are:\n")

    genres = list(genres)

    #creating a queue
    queue = deque(genres)

    #Printing genre choices and adding the available genres to the switcher.
    counter = 1
    for x in range (5):
        counter = 1
        counter = counter + (4 * (x))
        output = str(str(counter) +"."  + queue[0] + "      " + str(counter+1) + "." + 
                    queue[1]+  "     " + str(counter+2) + "." + queue[2]+ "      " + 
                    str(counter+3) + "." + queue[3]) 
        print(output)
        for i in range (4):
            case =  queue.popleft()
            switcher.update({str(counter + i): str(case)})

    #get input from user. assign weights to likes and dislikes for genres
    print("Pick 5 genres of movies that you like from greastest to least." +
            " Please enter the number that corresponds to your choice.")

    #TODO: doesnt check for disliking and liking the same genre. if time allows, fix
    for i in range (5):
        score = ((i * -1) / 2) + 3

        liked = switcher.get(input())
        chosen_genres.append((liked, score))

    print("Great! Now please enter 2 genres of movies that you dislike:")
    for i in range (2):
        disliked = switcher.get(input())
        chosen_genres.append((disliked, -2))

    for e in chosen_genres:
        if (e[1] > 0):
            print("You like: " + e[0])
        else:
            print("You dislike: " + e[0])
        
    '''
    -----------PREFERENCE MATCHING SYSTEM--------
    '''

    for x in range (999):
        for k,v in chosen_genres:
            if k in rows[x][2]:
                if rows[x][1] in scores:
                    scores[rows[x][1]] += v
                else:
                    scores.update({rows[x][1] : v})

    #sort in decending order
    sorted_scores = dict(sorted(scores.items(), key=operator.itemgetter(1), reverse=True))

    #printing top 10 suggestions
    top_ten = dict(list(sorted_scores.items())[0:10])

    print(top_ten)

    #resets the list of scores
    for x in range (999):
        for k,v in chosen_genres:
            if k in rows[x][2]:
                if rows[x][1] in scores:
                    scores[rows[x][1]] -= v
                else:
                    scores.update({rows[x][1] : v})

    print("Here are the top 10 movies recommended for you based on your choices:")
    print("The higher the associated score, the better the match. A perfect match is 7.5")
    counter = 1
    for k in top_ten:
        print(str(counter) + ". " + k + " : " + str(top_ten[k]) )
        counter += 1

'''
---------------------Actor Search Protocols----------------------
'''
def actorSearch(actors):
    #list of liked actors
    chosen_actors = []

    print("There are " + str(len(actors)) +" actors present in the top 1000 films. They are:\n")

    actors = list(actors)
 
    chosen_actors = []

    #get input from user. assign weights to likes and dislikes for actor
    print("Pick your 5 favorite actors and we will list movies in the database that have those actors.")
    for x in range (5):
        x = input()
        chosen_actors.append(x)

    print(chosen_actors)

    '''
    -----------PREFERENCE MATCHING SYSTEM--------
    '''
    actor_scores = {}
    for x in range(999):
        for actor in chosen_actors:
            if actor in rows[x][5]:
                if rows[x][1] in actor_scores:
                    actor_scores[rows[x][1]] += 1
                else:
                    actor_scores.update({rows[x][1]: 1})

   #sort in decending order
    sorted_scores = dict(sorted(actor_scores.items(), key=operator.itemgetter(1), reverse=True))

    #printing top 10 suggestions
    top_ten = dict(list(sorted_scores.items())[0:10])

    print(top_ten)

    #resets the list of scores
    for x in range(999):
        for actor in chosen_actors:
            if actor in rows[x][5]:
                if rows[x][1] in actor_scores:
                    actor_scores[rows[x][1]] -= 1
                else:
                    actor_scores.update({rows[x][1]: 1})

    print("Here are the top 10 movies recommended for you based on your choices:")
    print("The score here indicates how many of your favorite actors are in that movie.")
    counter = 1
    for k in top_ten:
        print(str(counter) + ". " + k + " : " + str(top_ten[k]) )
        counter += 1

'''
--------------GO AGAIN WHILE LOOP-------------------------
'''
goAgain = True
while(goAgain == True):

    print("Would you like to get movie recommendations based on your favorite genres or actors? Enter 1 for genres and 2 for actors")

    isValid = False
    while(isValid == False):
        i = input()
        if(i == "1"):
            genreSearch(genres)
            isValid = True
        elif(i == "2"):
            actorSearch(actors)
            isValid = True
        else:
            print("Try again. Enter 1 for genre search, and 2 for actor search.")

    print("Would you like to search again? Y for yes, N for no")
    choice = input()
    if(choice.lower() ==  "n"):
        goAgain = False