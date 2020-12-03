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

# Create forum post dataset from .csv
user_posts = pd.read_csv('user_posts.csv', na_values=0)  #, dtype={'user_id': int, 'count': int})
user_posts = user_posts.fillna(0)
user_posts = user_posts.astype(int)

# Do some cleaning I should have done in the scraper ---------------------------
user_ticks['dateand'] = user_ticks['route_notes'].str.split('.').str[0]
user_ticks['date'] = user_ticks['dateand'].str.split('\u00b7').str[0]
user_ticks['tick'] = user_ticks['dateand'].str.split('\u00b7').str[1]
user_ticks['notes'] = user_ticks['route_notes'].str.split('.').str[1:]
user_ticks = user_ticks.drop(6)

user_tick = user_ticks
#send_types = ['Lead / Onsight', 'Lead / Flash', 'Lead / Redpoint', 'Send', 'Flash']
#user_tick = user_ticks[user_ticks['tick'] == 'Lead / Onsight']
user_tick = user_tick[user_tick['tick'].str.contains("Flash|Send|Onsight|Redpoint", na=False)]
#user_tick = user_tick[user_tick.tick.isin(send_types)]
#print(user_tick)
#print(user_ticks.head())
# Do some shit
tick_boulders = user_ticks[user_ticks.route_type == 'Boulder']
tick_boulders = tick_boulders[tick_boulders['route_grade'].str.contains('V')]
tick_boulders['grade'] = tick_boulders['route_grade'].str[:3]
tick_boulders['grade'] = tick_boulders['grade'].str.replace('+','')
tick_boulders['grade'] = tick_boulders['grade'].str.replace('-','')
# ***** REGEX OUT SEND TYPE?
tick_sport = user_ticks[user_ticks.route_type == 'Sport']
tick_sport = tick_sport[tick_sport['route_grade'].str.contains('5.')]
tick_sport = tick_sport[tick_sport['route_grade'].str.contains('V') == False]
tick_sport['grade'] = tick_sport['route_grade'].str[:4]
tick_sport['grade'] = tick_sport['grade'].str.replace('+','')
tick_sport['grade'] = tick_sport['grade'].str.replace('-','')
tick_sport['grade'] = tick_sport['grade'].str.replace('/','')

tick_trad = user_ticks[user_ticks.route_type == 'Trad']
tick_trad = tick_trad[tick_trad['route_grade'].str.contains('5.')]
tick_trad = tick_trad[tick_trad['route_grade'].str.contains('V') == False]
tick_trad['grade'] = tick_trad['route_grade'].str[:4]
tick_trad['grade'] = tick_trad['grade'].str.replace('+','')
tick_trad['grade'] = tick_trad['grade'].str.replace('-','')
tick_trad['grade'] = tick_trad['grade'].str.replace('/','')
# Yah, I created these lists manually, sue me, it was probably faster than writing a function to do it.
# You gotta know when to quit.
# Create ordered list of boulder grades and a dictionary
# bo_grades = ['V-easy', 'V0-', 'V0', 'V0+', 'V0-1', 'V1-', 'V1', 'V1+', 'V1-2', 'V2-', 'V2', 'V2+', 'V2-3', 'V3-', 'V3', 'V3+', 'V3-4',
#              'V4-', 'V4', 'V4+', 'V4-5', 'V5-', 'V5', 'V5+', 'V5-6', 'V6-', 'V6', 'V6+', 'V6-7', 'V7-', 'V7', 'V7+', 'V7-8', 'V8-', 'V8', 'V8+',
#              'V8-9', 'V9-', 'V9', 'V9+', 'V9-10', 'V10-', 'V10', 'V10+', 'V10-11', 'V11', 'V11-12', 'V13', 'V17']

bo_grades = ['V-easy', 'V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V17']

# boulders = tick_boulders.route_grade.value_counts().rename_axis('route_grade').reset_index(name='counts')
# boulders.route_grade = boulders.route_grade.astype("category")
# boulders.route_grade.cat.set_categories(bo_grades, inplace=True)
# boulders = boulders.sort_values(['route_grade']).drop(0)

# Create ordered list of sport grades
sp_grades = ['Easy 5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.7+', '5.8-', '5.8', '5.8+', '5.9-', '5.9', '5.9+',
             '5.10-', '5.10a', '5.10a/b', '5.10b', '5.10', '5.10b/c', '5.10c', '5.10c/d', '5.10d', '5.10+',
             '5.11-', '5.11a', '5.11a/b', '5.11b', '5.11', '5.11b/c', '5.11c', '5.11c/d', '5.11d', '5.11+',
             '5.12-', '5.12a', '5.12a/b', '5.12b', '5.12', '5.12b/c', '5.12c', '5.12c/d', '5.12d', '5.12+',
             '5.13-', '5.13a', '5.13a/b', '5.13b', '5.13', '5.13b/c', '5.13c', '5.13c/d', '5.13d', '5.13+',
             '5.14a', '5.14b', '5.14', '5.14c/d', '5.15a']

sp_grades = ['Easy 5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.7+', '5.8-', '5.8', '5.8+', '5.9-', '5.9', '5.9+',
             '5.10', '5.10a', '5.10a/b', '5.10b', '5.10', '5.10b/c', '5.10c', '5.10c/d', '5.10d', '5.10+',
             '5.11', '5.11a', '5.11a/b', '5.11b', '5.11', '5.11b/c', '5.11c', '5.11c/d', '5.11d', '5.11+',
             '5.12', '5.12a', '5.12a/b', '5.12b', '5.12', '5.12b/c', '5.12c', '5.12c/d', '5.12d', '5.12+',
             '5.13', '5.13a', '5.13a/b', '5.13b', '5.13', '5.13b/c', '5.13c', '5.13c/d', '5.13d', '5.13+',
             '5.14a', '5.14b', '5.14', '5.14c/d', '5.15a']

# sport = tick_sport.route_grade.value_counts().rename_axis('route_grade').reset_index(name='counts')
# sport.route_grade = sport.route_grade.astype("category")
# sport.route_grade.cat.set_categories(sp_grades, inplace=True)
# sport = sport.sort_values(['route_grade']).drop(0)

# Create ordered list of trad grades
tr_grades = ['Easy 5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.7+', '5.8-', '5.8', '5.8+', '5.9-', '5.9', '5.9+',
             '5.10-', '5.10a', '5.10a/b', '5.10b', '5.10', '5.10b/c', '5.10c', '5.10c/d', '5.10d', '5.10+',
             '5.11-', '5.11a', '5.11a/b', '5.11b', '5.11', '5.11b/c', '5.11c', '5.11c/d', '5.11d', '5.11+',
             '5.12-', '5.12a', '5.12a/b', '5.12b', '5.12', '5.12b/c', '5.12c', '5.12c/d', '5.12d', '5.12+',
             '5.13-', '5.13a', '5.13a/b', '5.13b', '5.13', '5.13b/c', '5.13c', '5.13d',
             '5.14-', '5.14a', '5.14a/b']

# trad = tick_trad.route_grade.value_counts().rename_axis('route_grade').reset_index(name='counts')
# trad.route_grade = trad.route_grade.astype("category")
# trad.route_grade.cat.set_categories(tr_grades, inplace=True)
# trad = trad.sort_values(['route_grade']).drop(0)


# Exploratory Data Analysis
#boulders.plot.bar(x='route_grade', y='counts')
#sport.plot.bar(x='route_grade', y='counts')
#trad.plot.bar(x='route_grade', y='counts')

#plt.show()

x_boulders = tick_boulders
x_boulders.grade = x_boulders.grade.astype("category")
x_boulders.grade.cat.set_categories(bo_grades, inplace=True)
x_boulders = x_boulders.sort_values(['grade']).drop(0)

x_sport = tick_sport
x_sport.grade = x_sport.grade.astype("category")
x_sport.grade.cat.set_categories(sp_grades, inplace=True)
x_sport = x_sport.sort_values(['grade']).drop(0)

x_trad = tick_trad
x_trad.grade = x_trad.grade.astype("category")
x_trad.grade.cat.set_categories(tr_grades, inplace=True)
x_trad = x_trad.sort_values(['grade']).drop(0)

users = user_ticks.user_id.unique()

def user_profile(user_id, boulders, sport, trad):
    tick_bould = boulders[boulders.user_id == user_id]
    tick_sport = sport[sport.user_id == user_id]
    tick_trad = trad[trad.user_id == user_id]

    tick_bo = tick_bould.tail(10)
    tick_sp = tick_sport.tail(10)
    tick_tr = tick_trad.tail(10)

    if len(tick_bo.index) < 5:
        boulder_send = 'N/A'
    else:
        boulder_send = tick_bo['grade'].to_list()
        boulder_send = boulder_send[4:5]
        boulder_send = boulder_send[0]

    if len(tick_sp.index) < 5:
        sport_send = 'N/A'
    else:
        sport_send = tick_sp['grade'].to_list()
        sport_send = sport_send[4:5]
        sport_send = sport_send[0]

    if len(tick_tr.index) < 5:
        trad_send = 'N/A'
    else:
        trad_send = tick_tr['grade'].to_list()
        trad_send = trad_send[4:5]
        trad_send = trad_send[0]

    send_grade = [user_id, boulder_send, sport_send, trad_send]
    return send_grade

# ASFGKHJJFJD
sendage = []
for user_id in users:
    temp = user_profile(user_id, x_boulders, x_sport, x_trad)
    sendage.append(temp)

user_sends = pd.DataFrame(sendage, columns= ['user_id', 'boulder', 'sport', 'trad'])

x = user_sends.join(user_posts.set_index('user_id'), on='user_id', how='inner')

print(x)

boulder_posts = x[x.boulder != 'N/A']
boulder_posts.boulder = boulder_posts.boulder.astype("category")
boulder_posts.boulder.cat.set_categories(bo_grades, inplace=True)
boulder_posts = boulder_posts.sort_values(['boulder']).drop(0)
boulder_posts = boulder_posts.groupby(['boulder'])['count'].median()
boulder_posts = boulder_posts.rename_axis('grade').reset_index(name='mean')

sport_posts = x[x.sport != 'N/A']
sport_posts.sport = sport_posts.sport.astype("category")
sport_posts.sport.cat.set_categories(sp_grades, inplace=True)
sport_posts = sport_posts.sort_values(['sport']).drop(0)
sport_posts = sport_posts.groupby(['sport'])['count'].median()
sport_posts = sport_posts.rename_axis('grade').reset_index(name='mean')

trad_posts = x[x.trad != 'N/A']
trad_posts.trad = trad_posts.trad.astype("category")
trad_posts.trad.cat.set_categories(tr_grades, inplace=True)
trad_posts = trad_posts.sort_values(['trad']).drop(0)
trad_posts = trad_posts.groupby(['trad'])['count'].median()
trad_posts = trad_posts.rename_axis('grade').reset_index(name='mean')

print(boulder_posts)

boulder_posts.plot(x='grade', y='mean')
sport_posts.plot(x='grade', y='mean')
trad_posts.plot(x='grade', y='mean')

plt.show()
