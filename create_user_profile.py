# ----------------------------
# Processes user data
#
# Benjamin Buss, www.github.com/BenjaminBuss
# ----------------------------

import boto3
import pandas as pd
import matplotlib.pyplot as plt


# Connect to S3 bucket
client = boto3.client('s3')
resource = boto3.resource('s3')
my_bucket = resource.Bucket('mpcrawlerdump')
files = list(my_bucket.objects.filter(Prefix='userScraper/jsonData'))

# Create initial dataset from S3
user_ticks = pd.DataFrame()
for i in range(len(files)):
    obj = files[i].get()
    grid_sizes = pd.read_json(obj['Body'], lines=True)
    user_ticks = user_ticks.append(grid_sizes)

# Do some cleaning I should have done in the scraper
user_ticks['dateand'] = user_ticks['route_notes'].str.split('.').str[0]
user_ticks['date'] = user_ticks['dateand'].str.split('\u00b7').str[0]
user_ticks['tick'] = user_ticks['dateand'].str.split('\u00b7').str[1]
user_ticks['notes'] = user_ticks['route_notes'].str.split('.').str[1:]
user_ticks = user_ticks.drop(6)

# Do some shit
tick_boulders = user_ticks[user_ticks.route_type == 'Boulder']
tick_boulders = tick_boulders[tick_boulders['route_grade'].str.contains('V')]

# ***** REGEX OUT SEND TYPE?

tick_sport = user_ticks[user_ticks.route_type == 'Sport']
tick_sport = tick_sport[tick_sport['route_grade'].str.contains('5.')]
tick_sport = tick_sport[tick_sport['route_grade'].str.contains('V') == False]

tick_trad = user_ticks[user_ticks.route_type == 'Trad']
tick_trad = tick_trad[tick_trad['route_grade'].str.contains('5.')]

# Useless function
def user_profile(user_id):
    ticks = user_ticks[user_ticks.user_id == user_id]
    tick_boulders = ticks[ticks.route_type == 'Boulder']
    tick_sport = ticks[ticks.route_type == 'Sport']
    tick_trad = ticks[ticks.route_type == 'Trad']

    bould = 1
    sport = 1
    trad = 1

    send_grade = [bould, sport, trad]

    return send_grade

# Yah, I created these lists manually, sue me, it was probably faster than writing a function to do it.
# You gotta know when to quit.
# Create ordered list of boulder grades and a dictionary
bo_grades = ['V-easy', 'V0-', 'V0', 'V0+', 'V0-1', 'V1-', 'V1', 'V1+', 'V1-2', 'V2-', 'V2', 'V2+', 'V2-3', 'V3-', 'V3', 'V3+', 'V3-4',
             'V4-', 'V4', 'V4+', 'V4-5', 'V5-', 'V5', 'V5+', 'V5-6', 'V6-', 'V6', 'V6+', 'V6-7', 'V7-', 'V7', 'V7+', 'V7-8', 'V8-', 'V8', 'V8+',
             'V8-9', 'V9-', 'V9', 'V9+', 'V9-10', 'V10-', 'V10', 'V10+', 'V10-11', 'V11', 'V11-12', 'V13', 'V17']

boulders = tick_boulders.route_grade.value_counts().rename_axis('route_grade').reset_index(name='counts')
boulders.route_grade = boulders.route_grade.astype("category")
boulders.route_grade.cat.set_categories(bo_grades, inplace=True)
boulders = boulders.sort_values(['route_grade']).drop(0)

# Create ordered list of sport grades
sp_grades = ['Easy 5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.7+', '5.8-', '5.8', '5.8+', '5.9-', '5.9', '5.9+',
             '5.10-', '5.10a', '5.10a/b', '5.10b', '5.10', '5.10b/c', '5.10c', '5.10c/d', '5.10d', '5.10+',
             '5.11-', '5.11a', '5.11a/b', '5.11b', '5.11', '5.11b/c', '5.11c', '5.11c/d', '5.11d', '5.11+',
             '5.12-', '5.12a', '5.12a/b', '5.12b', '5.12', '5.12b/c', '5.12c', '5.12c/d', '5.12d', '5.12+',
             '5.13-', '5.13a', '5.13a/b', '5.13b', '5.13', '5.13b/c', '5.13c', '5.13c/d', '5.13d', '5.13+',
             '5.14a', '5.14b', '5.14', '5.14c/d', '5.15a']

sport = tick_sport.route_grade.value_counts().rename_axis('route_grade').reset_index(name='counts')
sport.route_grade = sport.route_grade.astype("category")
sport.route_grade.cat.set_categories(sp_grades, inplace=True)
sport = sport.sort_values(['route_grade']).drop(0)

# Create ordered list of trad grades
tr_grades = ['Easy 5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.7+', '5.8-', '5.8', '5.8+', '5.9-', '5.9', '5.9+',
             '5.10-', '5.10a', '5.10a/b', '5.10b', '5.10', '5.10b/c', '5.10c', '5.10c/d', '5.10d', '5.10+',
             '5.11-', '5.11a', '5.11a/b', '5.11b', '5.11', '5.11b/c', '5.11c', '5.11c/d', '5.11d', '5.11+',
             '5.12-', '5.12a', '5.12a/b', '5.12b', '5.12', '5.12b/c', '5.12c', '5.12c/d', '5.12d', '5.12+',
             '5.13-', '5.13a', '5.13a/b', '5.13b', '5.13', '5.13b/c', '5.13c', '5.13d',
             '5.14-', '5.14a', '5.14a/b']

trad = tick_trad.route_grade.value_counts().rename_axis('route_grade').reset_index(name='counts')
trad.route_grade = trad.route_grade.astype("category")
trad.route_grade.cat.set_categories(tr_grades, inplace=True)
trad = trad.sort_values(['route_grade']).drop(0)


# Exploratory Data Analysis
boulders.plot.bar(x='route_grade', y='counts')
sport.plot.bar(x='route_grade', y='counts')
trad.plot.bar(x='route_grade', y='counts')

#plt.show()


users = user_ticks.user_id.unique()





