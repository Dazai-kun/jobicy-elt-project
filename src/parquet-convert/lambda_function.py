import pandas as pd
import awswrangler as wr
import boto3
import json

s3_client = boto3.client('s3')
def lambda_handler(event, context):
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    target_item = event["Records"][0]["s3"]["object"]["key"]
    
    # A bucket with this name must be created beforehand
    target_bucket = 'clean-parquet-bucket'

    
    response = s3_client.get_object(Bucket=source_bucket, Key=target_item)
    data = response['Body'].read().decode('utf-8')
    data = json.loads(data)
    
    df = pd.DataFrame(data["jobs"])

    selected_columns = ["jobSlug", "jobTitle", "companyName", "jobIndustry",
                        "jobType", "jobGeo", "jobLevel", "jobDescription", "pubDate"]

    df = df[selected_columns]
    
    #The bucket will be partitioned as follows
    #s3://{bucket_name}/{year}/{month}/{day}/{file_name}.parquet
    key_path = f"{target_bucket}/{target_item[-15:-11]}/{target_item[-17:-15]}/{target_item[-19:-17]}/{target_item[:-20]}.parquet"

    wr.s3.to_parquet(df=df, path=f"s3://{key_path}")

    parquet_data = df.to_parquet(index=False)

    return {
        'statusCode': 200,
        'body': json.dumps('File converted to parquet successfully!')
    }
