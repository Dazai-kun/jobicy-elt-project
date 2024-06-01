
The purpose of this project is to create a simple ELT pipeline on AWS. 

It extracts daily job post data from [Jobicy](https://jobicy.com/), loads the raw json files into an s3 bucket. It then creates DataFrames from the JSON files and converts them into parquet format. The converted parquet files are then loaded into another s3 bucket and are partitioned by day, month, and year. 

**Tech stack:**
* AWS Lambda
* S3 bucket
* Amazon EventBridge

Here's the visualization of the project:

![jobicy-elt-viz](https://github.com/Dazai-kun/my-project/blob/fb70aa3002080189f4a5b2b0e8f29132a8d61cdf/image/Pasted%20image%2020240601134546.png)
### Why on AWS and not on-premise?

I want to have a simple serverless ELT that is automatically triggered based on a set schedule without me having to leave my laptop on 24/7. 

AWS is the best choice for this purpose because its free tier services are more than enough for the project. The Lambda function offers 1 million free requests per month and is completely serverless. Moreover, AWS EventBridge allows for scheduled triggers of lambda function, which makes the project fully automatic. 

Finally, an AWS account with API Gateway permissions is vital to perform IPs rotation for reasons that are discussed in the following section.  
### **IPs Rotation**

Since [Jobicy](https://jobicy.com/) limits the request volumes to only a few times per day, I have to use a proxy server to rotate my IP address for each GET request sent to Jobicy API. 

To do this free of charge, I use the [requests-ip-rotator](https://github.com/Ge0rg3/requests-ip-rotator) package, which is a Python library to utilize AWS API Gateway's large IP pool as a proxy to generate pseudo-infinite IPs for web scraping and brute forcing.
