

from twython import Twython
import string, json, pprint
import urllib
from datetime import datetime
from datetime import date
from time import *
import string, os, sys, subprocess, time
import psycopg2
import folium
import csv

##codes to access twitter API. 
APP_KEY = "Jiuz6QX9VFjbb1BohHkk957Ue"
APP_SECRET = "0t6OZ5O7wpyGgHj3hNoHKoDvdKYEFnH1vNklSLO1o0BwNFujNX"
OAUTH_TOKEN = "50629314-JCIOsV29c3m5ny6g7bwWUpOLx0a7lCQ5xsWeRL4SF"
OAUTH_TOKEN_SECRET = "N8j17Y6MScjcmJBPInU1MZ90r2E4rBmJ0vFRMfetX0Qni"

##initiating Twython object 
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

if os.path.exists('CampusART.csv'):
    os.remove('CampusART.csv')

output_file = 'CampusART.csv'

CampusLat = 51.9856010
CampusLon = 5.6661316

CampusART_map = folium.Map(location=[CampusLat, CampusLon],
                   zoom_start=17)
folium.TileLayer('openstreetmap').add_to(CampusART_map)
folium.TileLayer('stamenwatercolor').add_to(CampusART_map)
folium.TileLayer('stamenterrain').add_to(CampusART_map)
folium.TileLayer('stamentoner').add_to(CampusART_map)
folium.TileLayer('cartodbpositron').add_to(CampusART_map)
folium.TileLayer('cartodbdark_matter').add_to(CampusART_map)
folium.LayerControl().add_to(CampusART_map)

search_results = twitter.search(q='#livegeo AND #WDM', count=50,
                                geocode='51.9856010,5.6661316,2km')

for tweet in search_results["statuses"]:
    tweet_name =  tweet['user']['screen_name']
    followers_count =  tweet['user']['followers_count']
    tweet_text = tweet['text']
    tweet_text = tweet_text.replace(',', ' -')
    dt = tweet['created_at']
    tweet_datetime = datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')
    coordinates = tweet['coordinates']
    if coordinates != None:
        tweet_lat = coordinates['coordinates'][0] 
        tweet_lon = coordinates['coordinates'][1]   
        string_to_write = str(tweet_datetime)+","+str(tweet_name)+","+str(tweet_lat)+","+str(tweet_lon)+","+str(tweet_text)
        target = open(output_file, 'a')
        target.write(string_to_write) 
        target.write('\n') 
        target.close()


with open('CampusART.csv') as csvfile:
     alltweets = csv.reader(csvfile, delimiter=',')
     for tweet in alltweets:
        pop_date = tweet[0]
        pop_user = tweet[1]
        pop_lon = tweet[2]
        pop_lat = tweet[3]
        pop_tweet= tweet[4][:-14]
        html="""<h3> Art  piece</h3> <h5>{pop_tweet}</h5>
        By: <a href="http://www.twitter.com/{pop_user}" target="_blank"> @{pop_user} </a>
        <br> Latitude: {pop_lat}
        <br> Longitude: {pop_lon}
        <br> Tweeted at: {pop_date}""".format(pop_tweet=pop_tweet,
                                      pop_user=pop_user,
                                      pop_lon=pop_lon,
                                      pop_lat=pop_lat,
                                      pop_date = pop_date)
        iframe = folium.element.IFrame(html=html, width = 250, height = 150)
        popup = folium.Popup(iframe)
        folium.Marker(location=[pop_lat, pop_lon],
                      popup=popup,
                      icon=folium.Icon(icon='comment')).add_to(CampusART_map)
        CampusART_map.save('CampusART_map.html')



