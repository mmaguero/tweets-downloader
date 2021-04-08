"""
utils
"""
import pandas as pd
import json
import ast
from operator import itemgetter        
import csv
import datetime
import glob
import string
#
import Levenshtein
import preprocessor as p


p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.RESERVED) # remove this options


def datetime_filename(prefix='output_',extension='.txt'):
  """
  creates filename with current datetime string suffix
  """
  outputname = prefix + '{:%Y%m%d%H%M%S}utc{}'.format(
    datetime.datetime.utcnow(),extension)
  return outputname
  

def get_track_words(words_per_track,hour_count,lst):
  """
  read a list with words in gn
  """
  i = hour_count * words_per_track 
  j = i + words_per_track - 1  
  
  return lst[i:j]
  
  
def read_tweets(data_path):
    """
    read a file with tweets in json and convert to csv
    """

    json_list = []
    with open(data_path, 'r') as json_file_:
      for line in json_file_:
        json_file = json.dumps(ast.literal_eval(line))
        json_list += json_file,
    
    header = ['tweet_id', 'tweet', 'date', 'lang_twitter', 'retweeted', 'user_id']
    required_cols = itemgetter(*header)

    #with open(data_path) as f_input, open('out/'+data_path[:-4]+'.csv', 'w', newline='') as f_output:
    output = data_path.split("/")[-1]
    output = 'out/{}.csv'.format(output[:-4])
    with open(output, 'w', newline='') as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerow(header)
        for row in json_list:
            if row.strip():
                tweet = json.loads(row)
                tweet['tweet_id'] = tweet['id_str']
                tweet['tweet'] = tweet['extended_tweet']['full_text'] if ("extended_tweet" in tweet or "full_text" in tweet) and bool(tweet["truncated"]) else tweet['text']
                tweet['date'] = tweet['created_at']
                tweet['lang_twitter'] = tweet['lang']
                tweet['user_id'] = tweet['user']['id_str']
                csv_output.writerow(required_cols(tweet))
                
    return True


## uniques
def uniqueList(l):
    ulist = []
    [ulist.append(x.strip().lower()) for x in l if x.strip().lower() not in ulist and x.strip().lower() not in ['nan','na','',None]]
    return ulist  


def compareTweets(df, col, tweet1, threshold=0.90):
    tweet1_clean = p.clean(tweet1)
    # compare tweets using Levenshtein distance (or whatever string comparison metric) 
    matches = df[col].apply(lambda tweet2: (Levenshtein.ratio(tweet1_clean, p.clean(tweet2)) >= threshold))

    # get positive matches
    matches = matches[matches].index.tolist()

    # convert to list of tuples
    return [*zip(iter(matches[:-1]), iter(matches[1:]))]
      
