from datetime import datetime
import requests
import boto3
import json
from requests_ip_rotator import ApiGateway, ip_rotator
import os



AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION')


# Initialize S3 client
s3 = boto3.client('s3' 
                  ,aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
                  region_name=AWS_REGION
                )



industry_list = ['business','copywriting','supporting','data-science',
            'design-multimedia','admin','accounting-finance','hr','marketing',
            'management','dev','seller','seo','smm','engineering',
            'technical-support','web-app-design']

dt_string = datetime.now().strftime("%d%m%Y%H%M%S")


def handler(event, context):
    
    site_url = 'https://jobicy.com/'
    gateway =ApiGateway(site_url, regions= ip_rotator.DEFAULT_REGIONS 
                        ,access_key_id=AWS_ACCESS_KEY_ID, access_key_secret=AWS_SECRET_ACCESS_KEY
                        )
    
    gateway.start(force=True)
    session = requests.Session()
    session.mount(site_url, gateway)
    for industry in industry_list:
        
        
        querystring = {'industry': industry, 'count': 50}
        
        #Extract data from jobicy api
        response = session.get(site_url+'api/v2/remote-jobs',params=querystring)
        # response_results = response.json()
        
        #Upload data to S3 bucket
        
        bucket_name = 'raw-json-jobicy-bucket'
        object_key = f'output_{industry}_{dt_string}.json'
        
            
        s3.put_object(Body=response.text, Bucket=bucket_name, Key=object_key) 

    gateway.shutdown()
    
        
    return {
                'statusCode': 200,
                'body': 'Data uploaded to S3 successfully'
            }
        
    
    
