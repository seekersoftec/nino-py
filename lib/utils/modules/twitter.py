import twint
from bs4 import BeautifulSoup
#
from requests_lib import AsyncRequests, TorRequests


def twitter_search(email):

    splitAddress = email.split('@')
    user = str(splitAddress[0])
    domain = str(splitAddress[1].split('.')[0])
    tweets = []
    sources = []

    try:
        config = twint.Config()
        config.Search = user + ' ' + domain
        config.Store_object = True
        config.Hide_output = True
        config.Limit = 10

        config.Store_object_tweets_list = tweets
        twint.run.Search(config)

        for tweet in tweets:
            if(user in tweet.tweet and domain in tweet.tweet):
                sources.append(tweet.link)
    except:
        print("[=]Warning:Something went wrong while attempting to scrap twitter.com")

    return sources


#
class TwitterPermutator:
    def __init__(self):
        self.special_char = '_'

    def permutate(self):
        max_chars = 15

    #
    def analyse(self, username):
        #
        def follower_wonk(username):
            results = []
            analysis_url = f"https://followerwonk.com/analyze/{username}"
            analysis_res = AsyncRequests().request(method='GET', url=analysis_url).result()
            # analysis_res = TorRequests().get(analysis_url)
            #
            if (analysis_res.status_code != 200):
                results.append('An Error occurred')
            else:
                #
                soup = BeautifulSoup(analysis_res.text, features="lxml").find_all(
                    "div", {"class": "slice_body_1"})[3]
                #
                #
                results.append(soup)
            #
            return results
        #
        results = {
            'interests': []
        }

        if (('twitter' not in username.lower()) or ('admin' not in username.lower())):
            results['interests'] = follower_wonk(username)
        #
        return results


class UsernamePermutator:
    def __init__(self, email):
        self.email = email
        self.general_char_set = {
            'letters': 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z'.split(','),
            'numbers': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        }
    #

    class Twitter(TwitterPermutator):
        pass


email = 'seekersoftec@gmail.com'
# m = twitter_search(email)
# print(m)
#
#
#
# AnnaJMcDougall
k = UsernamePermutator(email).Twitter().analyse('seekersoftec')
print(k)
