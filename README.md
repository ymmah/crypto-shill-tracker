# Crypto Shill Tracker
*Shill* - an accomplice of a hawker, gambler, or swindler who acts as an enthusiastic customer to entice or encourage others.

*Crypto Shill* - someone who posts on Reddit about a coin they *usually* know nothing about either for karma or to try and raise the value of the coin for their own gain. **Minimal** technical information given and **100,000x** gains in a week!

## Description
Crypto Shill Tracker goes through a desired subreddit (cryptocurrency related) and analyzes the top posts of the day to determine if they are positive, negative, or neutral. The tracker then searches through the title of the post to see if the post is about a coin/token in particular, if the post is positive and about a coin then the Crypto Shill Tracker will recommend buying the coin.

## Code Example
```python
def analyze_post(self, post_info, post_number):
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
```
The code above uses TextBlob to perform a sentiment analysis on the title, based on the returned score it is classified as POSITIVE, NEUTRAL, or NEGATIVE. The title of the post is then check to see if it contains a coin, and based on that prints the remainder of the post information.

## Future Updates
1. Consider the amount of views, comments, and upvotes the post has.
2. Create a bot that automatically purchases the coin if determined worth buying and sells several hours later (for profit of course, Reddit knows all).
3. other stuff...
