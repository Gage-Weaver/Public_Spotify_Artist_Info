import os #Import Operating System
from dotenv import load_dotenv #Import dot env functionality
import base64 #Import base64 for encoding
from requests import post, get #Import post and get
import json #Import Json for functionality
import streamlit as st #Import streamlit for web app functionality
load_dotenv() #Call load_dotenv to load user id and secret
user_id= os.getenv("Client_id") #Grab the user id from the env file
user_secret= os.getenv("Client_secret") #grab the user secret from the env file
def get_token(): #Define a function to get the token 
    auth_str=user_id+':'+user_secret #Concatenate the id and the secret to make one auth string
    auth_byte=auth_str.encode("utf-8") #Encode this string using utf8
    auth_b64=str(base64.b64encode(auth_byte), "utf-8") #Make it base64
    url="https://accounts.spotify.com/api/token" #Define the url to pass token to
    headers= { #Define headers
        "Authorization": "Basic " + auth_b64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data= {"grant_type": "client_credentials"} #Define data that is needed
    result=post(url,headers=headers, data=data) #Define result using post with the url,headers, and data
    json_res=json.loads(result.content) #Json result from result
    token=json_res["access_token"] #Grab token from json results
    return token #Return the token
def get_auth_header(token): #Define function to save work when generating the auth header
    return {"authorization": "Bearer " + token}
def search_for_artist(token, artist): #Define function to search for an artist by name and get their id which is needed to get songs
    url= "https://api.spotify.com/v1/search" #Define url for this search
    headers=get_auth_header(token) #Use the earlier function that generates header and assign to headers
    query=f"?q={artist}&type=artist&limit=1" #Assign query with limit 1 to only grab first artist that comes up
    query_url=url+query #Combine url and query 
    result=get(query_url, headers=headers) #Get the result using headers and query url
    json_result=json.loads(result.content)["artists"]["items"] #Grab the result in json form
    if len(json_result) == 0: #if no result return none
        return None
    return json_result[0] #If there is a result return it
def find_songs_by_artist(token,artist_id): #Define function to find top 10 songs by artist
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US" #Define url as f string to search with
    headers=get_auth_header(token) #Define headers using earlier function
    result=get(url, headers=headers) #Get result
    json_result=json.loads(result.content)["tracks"] #Grab json data
    return json_result #return the result
def popularity_rank(token,artist_id): #Define function to find the popularity rank of an artist
    url = f"https://api.spotify.com/v1/artists/{artist_id}" #Define url as f string to search with
    headers=get_auth_header(token) #Define headers using earlier function
    result=get(url, headers=headers) #Get result
    json_result=json.loads(result.content)["popularity"] #Grab json data
    return json_result #return the result
def genres(token,artist_id): #Define function to find the genres of an artist
    url = f"https://api.spotify.com/v1/artists/{artist_id}" #Define url as f string to search with
    headers=get_auth_header(token) #Define headers using earlier function
    result=get(url, headers=headers) #Get result
    json_result=json.loads(result.content)["genres"] #Grab json data
    return json_result #return the result
token=get_token() #Grab the token
search=True #Define search as true
artist_input= st.text_input(label="Artist", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
button = st.button(label="Search", key=None, help=None, on_click=None, args=None, kwargs=None, type="secondary", disabled=False, use_container_width=False)
if button:
    #artist_to_search=input("Input the artist you would like to Find Info For: ") #Find artist user wants to search for
    st.write(artist_input) #Print artist input
    try: #Try to print out the results, will only hit exception if no artist is found
        result=search_for_artist(token, artist_input) #Find Result of user search
        artist_id=result["id"] #Define artist_id using result function
        st.write(result['name'],"Top Ten Songs") #Print name and top 10 songs text
        st.write("Popularity Rank:",popularity_rank(token,artist_id)) #Print popularity rank
        artistgenres=genres(token,artist_id)
        genresez= ", ".join(artistgenres)
        st.write("Genres: ",genresez)#Print genres
        songs= find_songs_by_artist(token,artist_id) #Define songs using the find songs function
        for songid, song in enumerate(songs): #Loop through songs and print them out nicely
            st.write(f"{songid+1}. {song['name']}")
    except: #If no artist is found tell the user and have them try again
        st.write("Sorry, It seems we can't find that artist, check your spelling and try again")
#py -m streamlit run Top_10_Songs_by_artist.py