import tweepy

api_key = hS10Xio9mRbBy4N0riEgjQQKi
api_secret = 8We8BsYp7URbQpTzmmNrMt3ks9gWrbE9iwpmYB3il1ZTMAmo2E

bearer_token = rAAAAAAAAAAAAAAAAAAAAALqWqgEAAAAAMXyB9WVoFWTITP7gvzj9fd40Ylo%3D8xHDzABlDt92jsZ5z4SitXUABMI9qSPwTME5n0cT6wsNge1Kjw
access_token = 170373418-avdZvMtlLKozxjJhPf2IRuTabT2KcTAnaCKZg8UI
access_token_secret = zd960VlvgVwv9gFdigNWK7HhsOUvoZK293dmSAi0x9ctf

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

client.create_tweet(text = What would you do if you could automate several tasks?)

# client.like(1613078224539615233)

# client.retweet(1613078224539615233)

# client.create_tweet(in_reply_to_tweet_id=1613078224539615233, text = Keep learning Simplilearners)

# for tweet in api.home_timeline():
#     print(tweet.text)

# person = client.get_user(username = narendramodi).data.id

# for tweet in client.get_users_tweets(person).data:
#     print(tweet.text)
