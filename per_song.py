from bs4 import BeautifulSoup as soup
import requests
import nltk
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series
import sys

class Lyrics(object):
	def grab_links(self, main_page, artist):
		"""
		This function:
		- scrapes titles of songs from the metrolyrics "Popular Songs" page using bs4 and saves to array: arr_post
	    	- the string contents of arr_post (which are song titles) are formatted to be lower case, punctuation free, and hyphenated
	    	- the revised strings are then concatenated to a URL template which links users to each "Popular Songs" complete lyrics
		:type main_page: string
		:rtype final_links: array 
		"""
		arr_post = []
		final_links = []
		page_html = soup(main_page.content, "html.parser")
		for songs in page_html.find_all(class_="title hasvidtable"):
			arr_post.append(songs.text.strip())
		arr_post = [str(item).lower().replace(" ","-").replace("'", "").replace("/","") for item in arr_post]
		
		for i in arr_post:
			final_links.append("http://www.metrolyrics.com/" + i + "-" + artist + ".html")
		print(len(final_links))
		return final_links
		
	def corpus_creation(self, final_links):
		"""
		This function:
		- reads/gets links and encodes to utf-8
		- complete lyrics of each individual title are then scraped and appended to a string: lyrics
		- all lyrics are then lower cased and stripped of punctuation in order to tidy data
	        - lyrics are saved into text file clean and ready for data analysis
		:type final_links: array
		:rtype drake_lyics.txt: .txt file
		"""
		arr = []
		for link in range(0, len(final_links)): 
			print(final_links[link])
			page = requests.get(final_links[link])
			page.encoding = 'utf-8'
			html = soup(page.content, "html.parser")
			for wrapper in html.find_all(class_="verse"):
				print(wrapper.text)
			# lyrics = ''
			# for wrapper in html.find_all(class_="verse"):
			# 	lyrics += (wrapper.text).lower()
			# lyrics = re.sub(r'[^\w\s]','',lyrics)
			#print lyrics
			#with open("drake_lyrics.txt", "a") as the_file:
			#	the_file.write(lyrics)

# metrics: [44, 55, 66, 33, 45] <- song1.txt <- "gods plan gods plan"


sol = Lyrics()
print("Please enter artist's first name.")
artist = input()
print("Please paste the URL of the artist whose song's you would like to scrape.")
print("Example: http://www.metrolyrics.com/drake-lyrics.html")
link = input() #"http://www.metrolyrics.com/drake-lyrics.html"
main_page = requests.get(str(link))
(sol.grab_links(main_page, artist.lower()))
sol.corpus_creation(sol.grab_links(main_page, artist))
