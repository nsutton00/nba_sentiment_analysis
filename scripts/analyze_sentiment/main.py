from google.cloud import language_v1
from google.cloud.language_v1 import *
from google.cloud import storage
import json

def get_from_gcs(bucket_name, source_blob_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blob.download_as_string()

def write_to_gcs(bucket, text, filename):
    blobname =  filename
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(blobname)
    blob.upload_from_string(text)

def analyze_sentiment(text_content):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(request={'document': document})
    return (response.document_sentiment.score, response.document_sentiment.magnitude)

def main(event, context):
    bucket_name = event['bucket']
    source_blob_name = event['name']
    text = get_from_gcs(bucket_name, source_blob_name)

    comment = json.loads(text)

    sentiment = analyze_sentiment(comment['text']) 
    comment['sentiment'] = sentiment[0]
    comment['magnitude'] = sentiment[1]

    comment_json = json.dumps(comment)
    write_fn = "processed-" + source_blob_name
    write_to_gcs('nba_sentiment_processed_new', comment_json, write_fn)