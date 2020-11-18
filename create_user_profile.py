# ----------------------------
# Processes user data based
#
# Benjamin Buss, www.github.com/BenjaminBuss
# ----------------------------

import boto3
import pandas as pd

# Connect to S3 bucket
client = boto3.client('s3')
resource = boto3.resource('s3')
my_bucket = resource.Bucket('mpcrawlerdump')
files = list(my_bucket.objects.filter(Prefix='userCrawler/jsonData'))

# Create dataset
forum_posts = pd.DataFrame()
for i in range(len(files)):
    obj = files[i].get()
    grid_sizes = pd.read_json(obj['Body'], lines=True)
    forum_posts = forum_posts.append(grid_sizes)


