from textblob import TextBlob
import urllib.request
from urllib.request import urlopen
import json
import re

class Crawler:
    def __init__(self):
        self.subreddit = ""
        self.post_type = ""
        self.duration = ""
        self.url = ""
        self.subreddit_json = ""
        self.post_info = {}
        
    def get_json(self, subreddit, post_type="top", duration="day"):
        """
        subreddit = which subreddit to crawl (r/cryptocurrency, r/bitcoin, r/ethereum...)
        post_type = Hot, New, Top, etc...
        duration = Hour, Day, Week, etc...
        """
        self.subreddit = ""
        self.post_type = ""
        self.duration = ""
        self.url = "https://www.reddit.com/r/{}/{}.json?t={}".format(subreddit, post_type, duration)
        
        with urllib.request.urlopen(self.url) as url:
            subreddit_json = json.loads(url.read().decode())["data"]
        return subreddit_json

    def iterate_json(self, subreddit_json, tags):
        """
        Iterates through the subreddit json and extracts the desired 
        tags and their corresponsing information.

        After extracting the desired information from a single post it performs
        an analysis on the title of the post to determine the sentiment of the post.
        """
        post_number = 0        
        for element in subreddit_json["children"]:
            for tag in tags:
                if tag != "":
                    post_tag = tag
                    tag_element = element["data"][tag]          
                    self.post_info[post_tag] = tag_element           
            post_number += 1
            self.analyze_post(self.post_info, post_number)
            self.post_info.clear()

    def analyze_post(self, post_info, post_number):
        """
        Prints out the post information after analyzing the sentimental
        value of the title.
        """
        print("Post Number: {}".format(post_number))
        post_sentiment = ""
        sentiment_value = 0    
        for tag in post_info:
            if tag == "title":
                title_analysis = TextBlob(post_info[tag])
                sentiment_value = title_analysis.sentiment.polarity
                if sentiment_value >= 0.25:
                    post_sentiment = "POSITIVE"
                elif sentiment_value > -0.1 and sentiment_value < 0.25:
                    post_sentiment = "NEUTRAL"
                else:
                    post_sentiment = "NEGATIVE"

                coin, contained = self.check_title(post_info[tag])
                if contained == True:
                    print("Coin in title: {}".format(coin))
                if contained == True and post_sentiment == "POSITIVE":
                    print("Buy {}!".format(coin))
                print("Title: {}".format(post_info[tag]))
                print("Title Sentiment: {}, {}".format(post_sentiment, sentiment_value))
            else:
                print("{}: {}".format(tag, post_info[tag]))
        print("")
    
    def check_title(self, title):
        """
        Check the CoinMarketCap API and grab each of the top 250 coins.
        Check if the title contains the name of a coin, return the coin name and True or False.
        """
        cmc_api = urlopen("https://api.coinmarketcap.com/v1/ticker/?limit=250")
        cmc_data = json.loads(cmc_api.read().decode())
        for coin in range(0, 250):
            curr_coin = cmc_data[coin]["name"]
            coin_symbol = cmc_data[coin]["symbol"]
            if self.find_word(curr_coin)(title) or self.find_word(coin_symbol)(title):
                return curr_coin, True
        return "None", False
            
    def find_word(self, word):
        """
        Checks if the word is in the title using regular expressions
        Answers found at: 
        https://stackoverflow.com/questions/5319922/python-check-if-word-is-in-a-string
        """            
        return re.compile(r'\b({0})\b'.format(word)).search

crawler = Crawler()
subreddit_json = crawler.get_json("cryptocurrency")
crawler.iterate_json(subreddit_json, ['title', 'link_flair_text', 'score', 'num_comments'])
