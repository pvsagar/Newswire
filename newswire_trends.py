

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 22:24:58 2018

@author: VidyaSagar
 

"""
# import required libraries
import timeit
start = timeit.default_timer()
import tracemalloc
tracemalloc.start()
import re
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen

# start scraping urls
news = "https://www.newswire.com/"
newsroom = "https://www.newswire.com/newsroom"
all_newsitems_urls =[]
for i in range (1,51):
    if int(i) > 1:
        newsroom = "https://www.newswire.com/newsroom/page/"+str(i)
    try:
        page = urlopen(newsroom)
    except Exception as e:
        print(e)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page, "lxml")
    all_newsitems= soup.find_all('a', attrs={'class': 'content-link'})
    for item in all_newsitems:
        all_newsitems_urls.append(item.get("href"))

# declare required variables
location = []
time = []
date = []
category = ""
category_data = []
tags = ""
tags_data = []

# start scraping data from articles
for url in all_newsitems_urls:
    new_url = news + url
    newpage = urlopen(new_url)
    newsoup = BeautifulSoup(newpage, "lxml")
    
    # location data
    try:
        single_newsitem_place = newsoup.find('strong',attrs={'class':'date-line color-pr'})
        loc = re.sub('\s+', ' ', single_newsitem_place.text)
        local = loc.split(',')
        city = local[0]
        location.append(city)
    except Exception as e:
        print(e)
    
    # date data
    try:
        single_newsitem_time = newsoup.find('span',attrs={'class':'status-true'})
        date1 = single_newsitem_time.text.strip()
        date1 = date1.replace(',', '')
        date2 = date1.split(" ")
        date3 = date2[1:3]
        date4 = ' '.join(date3)
        time.append(date4)
    except Exception as e:
        print(e)
    
    # category and Tags data
    #print(new_url)
    try:
        paragraphs = newsoup.find_all('p',attrs={'class':'mb-0'})
        result = [x.text for x in paragraphs]
        if len(result) == 3:
            result.pop(0)   
        if len(result) == 2:
            category1 = result[0]
            tags1 = result[1]
        elif len(result) == 1:
            tags1 = result[0]
        else:
            continue
    except Exception as e:
        print(e)

    category2 = re.sub('\s+', ' ', category1)
    category3 = category2.split(" ")
    category4 = category3[2:-1]
    category5 = ' '.join(category4)
    category = category + ", " + category5
    
    tags2 = re.sub('\s+', ' ', tags1)
    tags3 = tags2.split(" ")
    tags4 = tags3[2:-1]
    tags5 = ' '.join(tags4)
    tags = tags + ", " + tags5
    
category_data = category.split(",")
tags_data = tags.split(",")

category_data = category_data[1:]
tags_data = tags_data[1:]    


# plots start here

# 1. Plot for locations
df1 = pd.DataFrame(location)
df1.columns =['Location']
# location frequency
location_data = df1['Location'].value_counts()

# selecting top 20 locations
top20_Locations = location_data.head(20)
top20_dataframe = pd.DataFrame({'Location':top20_Locations.index,
                                'Frequency':top20_Locations.values})
x_labels = top20_dataframe["Location"].tolist()

# plot
ax = top20_Locations.plot(kind='bar',figsize=(20, 10))
# labeling
plt.ylabel('Number of articles published',fontsize=16)
plt.xlabel('Name of city',fontsize=16)
plt.title('Locations and Frequency of News articles', fontsize=20)
ax.set_xticklabels(x_labels,fontsize=14)
rects = ax.patches
labels = top20_dataframe["Frequency"].tolist()
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, label,
            ha='center', va='bottom',fontsize=16)
# save the Plot as image    
plt.savefig('Top 20 Locations with most number of News articles.png',
            bbox_inches = 'tight')
plt.show()

# 2. Date Plot
df2 = pd.DataFrame(time)
df2.columns = ['Date']
date_data = df2['Date'].value_counts()
dates = date_data.head(30)
dates_dataframe = pd.DataFrame({'Date':dates.index,
                                'Frequency':dates.values})
x_labels1 = dates_dataframe["Date"].tolist()
# plot
ax = dates.plot(kind='bar',figsize=(20, 10))
# labels
plt.ylabel('Number of articles published',fontsize=15)
plt.xlabel('Date',fontsize=15)
plt.title('Date and Frequency of News articles', fontsize=20)
ax.set_xticklabels(x_labels1,fontsize=14)
rects = ax.patches
labels1 = dates_dataframe["Frequency"].tolist()
for rect, label in zip(rects, labels1):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, label,
            ha='center', va='bottom',fontsize=16)
# save the Plot as image
plt.savefig('Dates and Number of articles published on that date.png',
            bbox_inches = 'tight')
plt.show()

# 3. category plot
df3 = pd.DataFrame(category_data)
df3.columns =['Category']
category_data1 = df3['Category'].value_counts()
top20_category = category_data1.head(20)
category_dataframe = pd.DataFrame({'Category':top20_category.index,
                                   'Frequency':top20_category.values})
x_labels2 = category_dataframe["Category"].tolist()
# plot
ax = top20_category.plot(kind='bar',figsize=(20, 10))
# labels
plt.ylabel('Number of articles published',fontsize=15)
plt.xlabel('Name of Category',fontsize=15)
plt.title('Category and Frequency of News articles', fontsize=20)
ax.set_xticklabels(x_labels2,fontsize=14)
rects = ax.patches
labels2 = category_dataframe["Frequency"].tolist()
for rect, label in zip(rects, labels2):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, label,
            ha='center', va='bottom',fontsize=16)
# save the Plot as image
plt.savefig('Top 20 Categories and their frequencies.png',
            bbox_inches = 'tight')
plt.show()

# 4. Tags Plot
df4 = pd.DataFrame(tags_data)
df4.columns =['Tags']
tags_data1 = df4['Tags'].value_counts()
top20_tags = tags_data1.head(20)
tags_dataframe = pd.DataFrame({'Tag':top20_tags.index,
                                   'Frequency':top20_tags.values})
x_labels3 = tags_dataframe["Tag"].tolist()
# plot
ax = top20_tags.plot(kind='bar',figsize=(20, 10))
# labels
plt.ylabel('Number of articles published',fontsize=15)
plt.xlabel('Tag attached',fontsize=15)
plt.title('Tags included and Frequency of News articles', fontsize=20)
ax.set_xticklabels(x_labels3,fontsize=14)
rects = ax.patches
labels3 = tags_dataframe["Frequency"].tolist()
for rect, label in zip(rects, labels3):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, label,
            ha='center', va='bottom',fontsize=16)
# save the Plot as image
plt.savefig('Top 20 Tags included in articles and their frequencies.png',
            bbox_inches = 'tight')
plt.show()

# Summary
print("Total number of News articles analysed for Trends:",len(all_newsitems_urls))
print("Number of unique locations from which News articles are published",len(location_data))
print("Number of days considered",len(date_data))
print("Number of unique catogeries",len(category_data1))
print("Number of uniquet tags included",len(tags_data1))

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

memory = ''
for stat in top_stats[:1]:
    memory = str(stat)
    memory = memory.split(':')
    memory = memory[-1]
    memory = memory.split(',')
    memory = memory[0]
    memory = memory.split('=')
    memory = memory[-1]

print("Memory Allocated:",memory)

stop = timeit.default_timer()

print('Total execution Time: ', stop - start, 'Seconds')

