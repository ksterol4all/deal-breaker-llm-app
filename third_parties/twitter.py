import os
from dotenv import load_dotenv
import requests
import tweepy


load_dotenv()

twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],   
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET_KEY"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
)

def scrape_user_tweets(username: str, num_tweets: int=5, mock: bool = False):
    """Scrapes a Twitter user's original tweets(i.e, not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """

    tweets = []
    if mock:
        # Mock data from github gist
        mock_data_url = "https://gist.githubusercontent.com/ksterol4all/1a3d9d82c2a0286e748d0fd3fa908038/raw/144b5fd2a3b0a2b9a97cb365d00a630dbd92b5f9/tweets-scrappin.json"
        response = requests.get(mock_data_url, timeout=10).json()
        for tweet in response:  
            tweets.append({
                "time_posted": tweet["created_at"],
                "text": tweet["text"],
                "url": f"https://twitter.com/{username}/status/{tweet['id']}"
            })
    else:
        # Fetch tweets using Twitter API
        user = twitter_client.get_user(username=username)
        if user.data:
            user_id = user.data.id
            response = twitter_client.get_users_tweets(id=user_id, max_results=num_tweets, tweet_fields=["created_at", "text", "id"])
            for tweet in response.data:
                if not tweet.text.startswith("RT @") and not tweet.in_reply_to_user_id:
                    tweets.append({
                        "time_posted": tweet.created_at,
                        "text": tweet.text,
                        "url": f"https://twitter.com/{username}/status/{tweet.id}"
                    })
    
    return tweets
    
if __name__ == "__main__":
    tweets = scrape_user_tweets(username="elonmusk")
    print(tweets)