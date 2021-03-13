# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 16:42:52 2021

@author: Rob
utelly - api for movies, television, etc... from netflix, amazon and others
https://rapidapi.com/utelly/api/Utelly
signing up is free for the first 1000 requests then 1 penny each request

"""

import requests

url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"

querystring = {"term":"bojack","country":"uk"}

headers = {
    'x-rapidapi-key': "SIGN-UP-FOR-KEY",
    'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)