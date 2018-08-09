# Compatible w ES V 6.*

from __future__ import print_function
from pprint import pprint

import boto3
import json
import urllib
import json
import StringIO
import gzip
import os

from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
from datetime import datetime, timedelta
from requests_aws4auth import AWS4Auth

from snowplow_columns import snowplow_columns
from index_mapping import index_mapping

s3 = boto3.client('s3')
session = boto3.session.Session()
credentials = session.get_credentials()

es_end_point = os.environ['ES_END_POINT']
days_to_keep_index = os.environ['DAYS_TO_KEEP_INDEX']

print('Loading function')

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    print("Bucket: " + bucket)
    print("Key: " + key)
    
    current_index_name_modifier = str(key).split("/")[-2][4:]
    current_index_name = "snowplow_events_{0}".format(current_index_name_modifier)
    
    es_client = connect_es(es_end_point)
    create_index(es_client, current_index_name)
    
    actions = []
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        actions = extract_actions_from_response(response, bucket, key, current_index_name)
    except:
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise
        
    index_events(es_client, actions)
    es_houskeeping(es_client)

def connect_es(es_end_point):
    print ('Connecting to the ES Endpoint {0}'.format(es_end_point))
    try:
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            session.region_name, 
            'es',
            session_token=credentials.token)
        
        es_client = Elasticsearch(
            hosts=[{'host': es_end_point, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection)
        return es_client
    except Exception:
        print("Unable to connect to {0}".format(esEndPoint))
        raise
        

def create_index(es_client, current_index_name):
    try:
        res = es_client.indices.exists(current_index_name)
        if res:
            print("Index {} already exists".format(current_index_name))
        else:
            print("Creating index {}".format(current_index_name))
            print(index_mapping)
            es_client.indices.create(current_index_name, index_mapping)
    except Exception as E:
        print("Unable to Create Index {0}".format(current_index_name))
        raise E
         
def extract_actions_from_response(response, bucket, key, current_index_name):
    snowplow_event_type = '_'.join(str(key).split("/")[1:3])
    
    # Extract the S3 object
    body = response['Body']
    data = body.read()

    # If the name has a .gz extension, then decompress the data
    if key[-3:] == '.gz':
        with gzip.GzipFile(fileobj=StringIO.StringIO(data)) as decompress_stream:
            data = decompress_stream.read()
        
    actions = []
    if (snowplow_event_type == "enriched_good"):
        for line in data.splitlines():
            # Create structured object and send it
            event = snowplow_extract_event_from_string(line)
            structured_event = {"meta": {"aws": {"s3": {"bucket": bucket, "key": key}}, "source": "snowplow", "type": snowplow_event_type}, "event": event, "message": line}
            action = {"_index": current_index_name, "_type": "snowplow_events","_source": structured_event}
            actions.append(action)
    else:
        for line in data.splitlines():
            # Create structured object and send it
            structured_event = {"meta": {"aws": {"s3": {"bucket": bucket, "key": key}}, "source": "snowplow", "type": snowplow_event_type}, "message": line}
            action = {"_index": current_index_name, "_type": "snowplow_events","_source": structured_event} 
            actions.append(action)
    return actions

def index_events(es_client, actions):
    if (actions):
        try:
            helpers.bulk(es_client, actions)
        except Exception:
            print("Failed to index documents")
            raise
    else:
        print("There are no documents to index!")
        exit(0)
        
        
def snowplow_extract_event_from_string(line):
    return dict(list(zip(snowplow_columns, line.split("\t"))))
    
    
def es_houskeeping(es_client):
    date_today = datetime.today()
    earliest_date_to_keep = date_today - timedelta(days=int(days_to_keep_index))
    
    indices_list = map(
        lambda i: i, 
        es_client.indices.get('*'))
        
    indices_to_delete = filter(
        lambda i_name: to_delete(i_name, earliest_date_to_keep),
        indices_list)
    print(indices_to_delete)
    
    if (indices_to_delete):
        try:
            es_client.indices.delete(index=",".join(indices_to_delete))
        except Exception:
            print("Failed to delete indices.")
            raise
    else:
        print("There are no indeces to delete")
        
def to_delete(i_name, earliest_date_to_keep):
    snowplow_events_index = i_name.startswith("snowplow_events_")
    if (snowplow_events_index):
        creation_date = datetime.strptime(i_name.replace('snowplow_events_', ''), '%Y-%m-%d-%H-%M-%S')
        old_index = creation_date < earliest_date_to_keep
        return old_index
    else:
        return False