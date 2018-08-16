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
	def grab_links(self, main_page):
		arr_post = []
		final_links = []
		page_html = soup(main_page.content, "html.parser")
		for songs in page_html.find_all(class_="title hasvidtable"):
			arr_post.append(songs.text.strip())
		arr_post = [str(item).lower().replace(" ","-").replace("'", "").replace("/","") for item in arr_post]
		
		for i in arr_post:
			final_links.append("http://www.metrolyrics.com/" + i + "-drake.html")
		return final_links

	def corpus_creation(self, final_links):
		for link in final_links:
			page = requests.get(link)
			page.encoding = 'utf-8'
			html = soup(page.content, "html.parser")
			lyrics = ''
			for wrapper in html.find_all(class_="verse"):
				lyrics += (wrapper.text).lower()
			lyrics = re.sub(r'[^\w\s]','',lyrics)
			#print lyrics
			#with open("drake_lyrics.txt", "a") as the_file:
			#	the_file.write(lyrics)
	
	def word_freq(self, file_content):	
		tokens = nltk.word_tokenize(file_content)#.encode('utf8'))
		counts = Counter(tokens)
		#s = Series(counts)
		#print counts
		
		keys = counts.keys()
		y_pos = np.arange(len(keys))
		performance = [counts[k] for k in keys]
		error = np.random.rand(len(keys))

		'''
		plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
		plt.yticks(y_pos, keys)
		plt.xlabel('Counts')
		plt.title('Lyrics')
		plt.show()
		'''

sol = Lyrics()
main_page = requests.get("http://www.metrolyrics.com/drake-lyrics.html")
file_content = open("drake_lyrics.txt").read()
sol.grab_links(main_page)
print sol.corpus_creation(sol.grab_links(main_page))
sol.word_freq(file_content)
