import sys
import os
import praw
import json
from bs4 import BeautifulSoup
from google.cloud import storage

def html_to_plainstring(string):
    bs_string = BeautifulSoup(string)
    plaintext = bs_string.text
    return plaintext

def write_to_gcs(bucket, text, filename):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(filename)
    blob.upload_from_string(text)
def get_comments_from_url(url):
    praw_client_id = os.environ["praw_client_id"]
    praw_client_secret = os.environ["praw_client_secret"]
    
    reddit = praw.Reddit(user_agent="NBA Comment Extraction (by /u/nsutton00)",
    client_id=praw_client_id, client_secret=praw_client_secret)
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()
    return all_comments
    
if __name__ == "__main__":
    print('Starting up...')

    url = sys.argv[1]

    print(f'Getting comments from {url}')
    all_comments = get_comments_from_url(url)
    
    comments_dict = {}
    for i, comment in enumerate(all_comments):
        text = html_to_plainstring(comment.body_html)
        print(f'Processing comment: {text}') 
        if text not in ['[deleted]', ' [deleted]', '[deleted] ', ' [deleted] ']: #skip deleted comments
            comments_dict[i] = {}
            comments_dict[i]['timestamp'] = comment.created_utc
            comments_dict[i]['text'] = text
    
    #write to gcs
    for i in comments_dict:
        comments_json = json.dumps(comments_dict[i])
        print(f'Writing comment: {comments_json}')
        blob_name = url.split('/')[6] + '_' + str(i)
        write_to_gcs('nba_sentiment_raw', comments_json, blob_name)