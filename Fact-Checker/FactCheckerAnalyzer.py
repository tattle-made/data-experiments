import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from datetime import datetime,timedelta
import calendar
import pandas as pd
import json
import plotly.express as px

DB_NAME = os.environ.get("DB_NAME")
DB_COLLECTION = os.environ.get("DB_COLLECTION")


def initialize_mongo():

    client = MongoClient('localhost:27017')
    db = client[DB_NAME]
    coll = db[DB_COLLECTION]

    return coll

def get_day(date):

    born = datetime.strptime(date, '%Y-%m-%d').weekday()
    return (calendar.day_name[born])

def get_today_date():
    
    date = datetime.today()
    return str(date.strftime("%Y-%m-%d"))
    
def get_lastweek_data(coll,today=get_today_date()):
    
    if get_day(today) != 'Sunday':
     
        date_obj = datetime.strptime(today, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday()) - timedelta(days=7) # Last Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        print(start_of_week)
        print(end_of_week)
        
    else:
        
        date_obj = datetime.strptime(today, '%Y-%m-%d')
        start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        print(start_of_week)
        print(end_of_week)
        
    query = {"$and": [{"date_updated_UTC": {"$gte": start_of_week}}, {"date_updated_UTC": {"$lte": end_of_week}}]}
    
    docs_df = pd.DataFrame(coll.find(query))
    if docs_df.empty:
        return docs_df

    docs_df = docs_df.explode('docs').reset_index(drop=True)
    docs_df['media_type'] = docs_df['docs'].apply(lambda x: x.get('mediaType'))
    print(docs_df.shape)

    return docs_df

def num_articles(docs):
    
    num = len(pd.unique(docs['postURL']))
    return num

def day_wise_count(docs):
    
    df    =  docs.groupby(['date_updated_UTC']).size().reset_index(name='counts')
    df.columns = ['date','count']
    fig   =  px.bar(df, x='date', y='count')
    filename =  day_wise_count.__name__ + ".html"

    fig.write_html(filename)

    return filename

def count_domains(docs):
    
    return len(docs['domain'].unique())

def domain_wise_count(docs):
    
    docs['factcheck_site'] = docs['domain'].apply(lambda x : x.split('.')[0])
    return docs.groupby(['factcheck_site']).size().reset_index(name='counts')

def dist_media_type(docs):
    
    docs['media_type'] = docs['docs'].apply(lambda x: x.get('mediaType'))    
    return docs['media_type'].value_counts()

def count_media_wrt_day(docs):
    
    return docs.groupby('date_updated_UTC')['media_type'].value_counts()

def count_media_wrt_domain(docs):
    
    return docs.groupby('factcheck_site')['media_type'].value_counts()


#returns dict
def count_articles_wrt_socialmedia(docs):
    
    a = len(pd.unique(docs[docs['media_type']=="tweet"]['postURL']))
    b = len(pd.unique(docs[docs['media_type']=="fbpost"]['postURL']))
    c = len(pd.unique(docs['postURL']))
    
    return {"tweet" : round(a/c),"fbposts" : round(b/c)}

def avg_images_per_article(docs):
    
    val = docs[docs['media_type']=="image"].groupby(['postURL']).size().reset_index(name='counts')['counts'].mean()
    
    return round(val)

def get_authors_list(docs):
    
    docs['author_name'] = docs['author'].apply(lambda x: x['name'])
    
    return list(docs['author_name'].unique())

if __name__ == "__main__":

    coll = initialize_mongo()
    
    data = get_lastweek_data(coll,"2021-05-01")
    #data = get_lastweek_data(coll)
    
    print(data)

    if not data.empty:

        analysis_dict = {
            "status" : "Found Data",
            "num_articles" : num_articles(data),
            "num_sites" : count_domains(data), 
            "authors_list" : get_authors_list(data),  
            "avg_images_per_article" : avg_images_per_article(data),
            "day_wise_count" : day_wise_count(data),
        }

    else:

        analysis_dict = {
            "status" : "No Data"
        }

    with open('analysis1.json','w') as json_file:

            json.dump(analysis_dict,json_file)
 
