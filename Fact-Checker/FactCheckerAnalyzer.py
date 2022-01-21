import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from datetime import datetime,timedelta
import calendar
import pandas as pd
import json
import plotly.express as px
import date_converter
import plotly.graph_objects as go

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
        #print(type(start_of_week))
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

    docs_df.drop_duplicates(subset = "postURL", inplace = True)
    docs_df = docs_df.explode('docs').reset_index(drop=True)
    docs_df['media_type'] = docs_df['docs'].apply(lambda x: x.get('mediaType'))
    print(docs_df['media_type'].unique())
    value_counts = docs_df['media_type'].value_counts()
    print(value_counts)
    docs_df['factcheck_site'] = docs_df['domain'].apply(lambda x : x.split('.')[0])

    print(docs_df.shape)

    start_of_week = date_converter.datetime_to_string(start_of_week, '%Y-%m-%d')
    end_of_week = date_converter.datetime_to_string(end_of_week,'%Y-%m-%d')

    return docs_df,start_of_week,end_of_week

def get_week_num(input_date):

    input_date = date_converter.string_to_datetime(input_date, '%Y-%m-%d', '%Y-%m-%d')
    _, week_num, _ = input_date.isocalendar()

    return week_num

def num_articles(docs):
    
    num = len(pd.unique(docs['postURL']))
    return num

def day_wise_count(docs,week):
    
    #df    =  docs.groupby(['date_updated_UTC']).size().reset_index(name='counts')
    #df.columns = ['date','count']
    #fig   =  px.bar(df, x='date', y='count')
    docs_dup = docs.drop_duplicates(subset = "postURL")

    df = docs_dup.groupby(['date_updated_UTC']).size().reset_index(name='counts')
    #import plotly.express as px
    df.columns  = ['date','count']
    fig = px.line(df, x="date", y="count", markers=True, template="simple_white")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True)
    fig.update_traces(line=dict(color="#9467bd",width=1.5))
    fig.update_layout(title="Day Wise Distribution of Articles",xaxis_title="date",yaxis_title="number of articles")
    
    filename = week + "_" + day_wise_count.__name__ + ".html"
    fig.write_html(filename)

    return filename

def count_domains(docs):
    
    return len(docs['domain'].unique())

def domain_wise_count(docs,week):
    
    # docs['factcheck_site'] = docs['domain'].apply(lambda x : x.split('.')[0])
    # return docs.groupby(['factcheck_site']).size().reset_index(name='counts')
    
    docs_dup = docs.drop_duplicates(subset = "postURL")
    #docs.drop_duplicates(subset = "postURL", inplace = True)
    df = docs_dup.groupby(['factcheck_site']).size().reset_index(name='counts')
    
    x = df['factcheck_site']
    y = df['counts']

    fig = go.Figure(data=[go.Bar(x=x,y=y,width=0.5)])
    fig.update_traces(marker_color='#f08080', marker_line_color='#663399',marker_line_width=2.5, opacity=0.7)
    fig.update_layout(title="Domain Wise Distribution of Articles",xaxis_title="factcheck_site",yaxis_title="number of articles")
    fig.layout.plot_bgcolor = '#fff'
    
    filename = week + "_" + domain_wise_count.__name__ + ".html"
    fig.write_html(filename)

    return filename

def dist_media_type(docs,week):
    
    value_counts = docs['media_type'].value_counts()
    print(value_counts)
    df = pd.DataFrame(value_counts)
    df = df.reset_index()
    df.columns = ['media_type', 'counts'] 
    
    x = df['media_type']
    y = df['counts']

    fig = go.Figure(data=[go.Bar(x=x,y=y,width=0.5)])
    fig.update_traces(marker_color='#f08080', marker_line_color='#663399',marker_line_width=2.5, opacity=0.7)
    fig.update_layout(title="Count of Media types across all articles",xaxis_title="media_type",yaxis_title="count")
    fig.layout.plot_bgcolor = '#fff'
    
    filename = week + "_" + dist_media_type.__name__ + ".html"
    fig.write_html(filename)

    return filename

def count_media_wrt_day(docs,week):
    
    docs.groupby('date_updated_UTC')['media_type'].value_counts()
    df = docs.groupby( [ "date_updated_UTC", "media_type"] ).size().to_frame(name = 'count').reset_index()

    fig = px.line(df, x="date_updated_UTC", y="count", color='media_type',markers=True, template="simple_white", color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_xaxes(showgrid=False)
    fig.update_layout(title="Daywise count of Media types",xaxis_title="date",yaxis_title="count")
    
    filename = week + "_" + count_media_wrt_day.__name__ + ".html"
    fig.write_html(filename)

    return filename

def count_media_wrt_domain(docs,week):
    
    
    docs.groupby('factcheck_site')['media_type'].value_counts()
    df = docs.groupby( [ "factcheck_site", "media_type"] ).size().to_frame(name = 'count').reset_index()

    fig = px.bar(df, x="factcheck_site", y="count", color="media_type",text_auto=True)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_traces(marker_line_color='#663399',marker_line_width=2, opacity=0.8)
    fig.update_layout(title="Domain wise count of Media types",xaxis_title="factcheck_site",yaxis_title="count")
    fig.layout.plot_bgcolor = '#fff'
    
    filename = week + "_" + count_media_wrt_domain.__name__ + ".html"
    fig.write_html(filename)

    return filename

def count_articles_wrt_socialmedia(docs,week):
    
    a = len(pd.unique(docs[docs['media_type']=="tweet"]['postURL']))
    b = len(pd.unique(docs[docs['media_type']=="fbpost"]['postURL']))
    c = len(pd.unique(docs['postURL']))
    
    count_dict = {"tweet" : float(a/c)*100,"fbposts" : float(b/c)*100}
    
    df = pd.DataFrame.from_dict(count_dict,orient='index')
    df = df.reset_index()
    df.columns = ['social_media', 'counts'] 

    x = df['social_media']
    y = df['counts']

    fig = go.Figure(data=[go.Bar(x=x,y=y,width=0.5)])
    fig.update_traces(marker_color='#f08080', marker_line_color='#663399',marker_line_width=2.5, opacity=0.7)
    fig.update_layout(title="Count of Social Media posts across all articles",xaxis_title="social media",yaxis_title="count")
    fig.layout.plot_bgcolor = '#fff'
    
    filename = week + "_" + count_articles_wrt_socialmedia.__name__ + ".html"
    fig.write_html(filename)

    return filename  

def avg_images_per_article(docs):
    
    val = docs[docs['media_type']=="image"].groupby(['postURL']).size().reset_index(name='counts')['counts'].mean()
    
    return round(val)

def get_authors_list(docs):
    
    docs['author_name'] = docs['author'].apply(lambda x: x['name'])
    
    return list(docs['author_name'].unique())

def convert_data_to_string(date):
    
    str_date = date_converter.string_to_string(date, '%Y-%m-%d', '%d %B %Y')
    str_date = str_date.replace(" ", "")
    
    return str_date

if __name__ == "__main__":

    coll = initialize_mongo()
    input_date = "2021-05-01"
    data,start,end = get_lastweek_data(coll,input_date)

    
    print(f"input date : {input_date}")

    """
    Fetch data today
    data = get_lastweek_data(coll)
    """

    if not data.empty:

        week = convert_data_to_string(start) + "-" + convert_data_to_string(end)
        #docs_df.drop_duplicates(subset = "postURL", inplace = True)

        analysis_dict = {
            "status" : "Found Data",
            "num_articles" : num_articles(data),
            "num_sites" : count_domains(data), 
            "authors_list" : get_authors_list(data),  
            "avg_images_per_article" : avg_images_per_article(data),
            "count_wrt_day" : day_wise_count(data,week),
            "count_wrt_domain" : domain_wise_count(data,week),
            "count_wrt_mediatype" : dist_media_type(data,week),
            "count_media_wrt_day" : count_media_wrt_day(data,week),
            "count_media_wrt_domain" : count_media_wrt_domain(data,week),
            "count_articles_wrt_socialmedia" : count_articles_wrt_socialmedia(data,week),
            "week" : week,
            "week_num" : get_week_num(start)    
        }
    
    else:

        analysis_dict = {
            "status" : "No Data"
        }

    with open('analysis1.json','w') as json_file:

            json.dump(analysis_dict,json_file)