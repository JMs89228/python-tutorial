import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import sqlite3

baseurl = 'https://www.starbucks.com.tw/products/drinks/view.jspx?catId=1'
html = requests.get(baseurl)
soup = BeautifulSoup(html.text, 'html.parser')

drinks = soup.find(class_='wrap view drinks')
articles = drinks.find_all('article')

# web scraping and save the data as table format
result = list()
for article in articles:
    lists = article.find_all('li')
    for li in lists:
        name_cn = li.select('h1')[0].text
        name_en = li.select('h3')[0].text
        href = li.select('a')[0]['href']
        full_url = urljoin(baseurl, href)

        base = full_url
        html = requests.get(base)
        soup = BeautifulSoup(html.text, 'html.parser')
        tabs = soup.find('div', class_='tabs')
        uls = tabs.find_all('ul')
        lists = uls[0].find_all('li')
        tables = tabs.find_all('table')
        
        for index, li in enumerate(lists):
            capacity = li.text
            ths = tables[index].find_all('th')
            tds = tables[index].find_all('td')
            for th, td in zip(ths, tds):
                tuple = (name_cn, name_en, capacity, th.text, td.text)
                result.append(tuple)

data = pd.DataFrame(result, columns=['name_cn', 'name_en', 'capacity', 'item', 'price'])

# Transform the data into pivot table and turn 
pivot = data.pivot_table(index=['name_cn', 'name_en', 'capacity'], columns='item', values='price', aggfunc='first')
pivot.to_csv('startbucks.csv', encoding='utf-8')

# import data from csv file
df = pd.read_csv('startbucks.csv', encoding='utf-8')

# convert the column '價格‘ to integer
df['價格'] = df['價格'].str.replace('$', '').astype(int)

'''
# analyze the pivot data with some graphs
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# plot the boxplot of price by each drink with different capacity
df.boxplot(column='價格', by='name_en', figsize=(30, 20))
# new line for the value of x axis if the name_en is too long
plt.xticks(rotation=90)
# Add the title of y axis
plt.ylabel('Price')
# Add the title of the graph
plt.title('Price of each drink with different capacity')
# save the picture
plt.savefig('price_boxplot.png')

# plot bar charts of price by each drink with capacity = '中杯', '大杯', '特大杯'
# the capacity
df[df['capacity'] == '中杯'].plot.bar(x='name_en', y='價格', figsize=(30, 10))
plt.ylabel('Price')
plt.xticks(rotation=90)
plt.title('Middle Cup')
#save the figure
plt.savefig('middle_cup.png')
plt.show()

df[df['capacity'] == '大杯'].plot.bar(x='name_en', y='價格', figsize=(30, 10), color='red')
plt.ylabel('Price')
plt.xticks(rotation=90)
plt.title('Large Cup')
# Use red color for the bar chart
# save the figure
plt.savefig('large_cup.png')
plt.show()

df[df['capacity'] == '特大杯'].plot.bar(x='name_en', y='價格', figsize=(30, 10), color = 'orange')
plt.ylabel('Price')
plt.xticks(rotation=90)
plt.title('Extra Large Cup')
# Use red orange for the bar chart
# save the figure
plt.savefig('extra_large_cup.png')
plt.show()
'''

conn = sqlite3.connect('starbucks_database')
# c = conn.cursor()

conn.execute('CREATE TABLE IF NOT EXISTS products (name_cn text, name_en text, capacity text , "價格" number , "咖啡因含量 (毫克)" number, "熱量(大卡)" number, "糖(公克)" number)')
# conn.commit()

df.to_sql('starbucks_database', conn, if_exists='replace', index = False)
