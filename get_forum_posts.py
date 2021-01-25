# ---------------
# Imports and tidies data from XXX scraper to be used in the
# Get counts of each users forum posts
#
# Benjamin Buss, www.github.com/BenjaminBuss
# ---------------

import pandas as pd
import boto3

# Connect to S3 bucket.
client = boto3.client('s3')
resource = boto3.resource('s3')
my_bucket = resource.Bucket('mpcrawlerdump')
files = list(my_bucket.objects.filter(Prefix='forumScraper/jsonData'))

# Create dataset.
forum_posts = pd.DataFrame()
for i in range(len(files)):
    obj = files[i].get()
    grid_sizes = pd.read_json(obj['Body'], lines=True)
    forum_posts = forum_posts.append(grid_sizes)

f = lambda x: x['mess_date'].split(",")[-1].strip()
forum_posts['year'] = forum_posts.apply(f, axis=1)

latest_posts = forum_posts[forum_posts['year'] == '2020']
latest_posts = latest_posts[['thread_id', 'user_id']]

# Tidy and upload.
user_posts = latest_posts.groupby("user_id").size().reset_index().rename(columns={0: 'count'})
user_posts = user_posts[user_posts['count'] > 5]

user_posts.to_csv(r'user_posts.csv', index=False, header=True)
my_bucket.upload_file('user_posts.csv', Key='forumScraper/tidyied/user_posts.csv')

user_url = []
user_id = user_posts['user_id'].tolist()

# Create start URLs and upload separately.
for i in user_id:
    user_url.append('https://www.mountainproject.com/user/' + str(i))

user_url = pd.DataFrame(user_url, columns=['url'])

user_url.to_csv(r'user_urls.csv', index=False, header=True)
my_bucket.upload_file('user_urls.csv', Key='forumScraper/tidyied/user_urls.csv')

