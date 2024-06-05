#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import necessary Libraryies
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# In[ ]:


driver = webdriver.Chrome(r'C:\Users\DELL\Desktop\Python-project\WEB SCRAPING\chromedriver.exe')
driver.get('https://unica.vn/donggia')


# In[ ]:


soup = BeautifulSoup(driver.page_source, 'lxml')
df = pd.DataFrame({'Link':[''], 'Name':[''], 'Teacher':[''],'Image':[''],'Price':[''],'Ratings':[''],'Sales':[''],'Origin_price':['']}) 
#button = driver.find_element('xpath', '//*[@id="loadMore283"]')
while True:
    #wait = WebDriverWait(driver, 10);
    #button = wait.until(EC.element_to_be_clickable((By.ID,"loadMore283")));
    try:
        btn = driver.find_element('xpath','//*[@id="loadMore283"]')
       # class_name = btn.get_attribute("class")
        driver.execute_script ("arguments[0].click();",btn)
        time.sleep(5)
    except NoSuchElementException:
        print("element does not exist")
        break

courses = soup.find_all('div',class_ = "dg-box-course")
for course in courses:
    name = course.find('a', class_='dg-title-box').text
    link = course.find('a', class_='dg-title-box').get('href')
    teacher = course.find('a', class_='dg-bigname-gv').text
    image = course.find('img', class_='img-responsive').get('src')
    price = course.find('li', class_ ='dg-price-net pull-right').text
    ori_price = course.find('div', class_="text").text
    star = len(course.find_all('li',class_="color_yellow"))
    mems = course.find('div', 'dg-txt-mem').get('strong').text
    df = df.append({'Link':link, 'Name':name, 'Teacher':teacher,'Image':image,'Price':price,'Ratings':star,'Sales':mems,'Origin_price':ori_price}, ignore_index=True) 


# In[ ]:


df = pd.DataFrame({'Link':[''], 'Name':[''], 'Teacher':[''],'Image':[''],'Price':[''],'Ratings':[''],'Sales':[''],'Origin_price':['']})
courses = soup.find_all('div',class_ = "dg-box-course")
for course in courses:
    name = course.find('a', class_='dg-title-box').text
    link = course.find('a', class_='dg-title-box').get('href')
    teacher = course.find('a', class_='dg-bigname-gv').text
    image = course.find('img', class_='img-responsive').get('src')
    price = course.find('li', class_ ='dg-price-net pull-right').text
    ori_price = course.find('div', class_="text").text
    star = len(course.find_all('li',class_="color_yellow"))
    mems = course.find('div', 'dg-txt-mem').text.replace('\n','').replace(' ','')[4:]
    df = df.append({'Link':link, 'Name':name, 'Teacher':teacher,'Image':image,'Price':price,'Ratings':star,'Sales':mems,'Origin_price':ori_price}, ignore_index=True)


# In[ ]:


df = pd.DataFrame({'Link':[''], 'Name':[''], 'Teacher':[''],'Image':[''],'Price':[''],'Ratings':[''],'Sales':[''],'Origin_price':['']})
df=pd.read_excel(r'C:\Users\DELL\Desktop\unica_khoahocnoibat.xlsx')
df


# In[ ]:


df=df.drop(0)


# In[ ]:


df['Price'] = df['Price'].astype(str).apply(lambda x: x.strip('đ'))
df['Price']= df['Price'].apply(lambda x: float(x.replace('.', ''))).astype(float)
df['Price']


# In[ ]:


df['Price']


# ## SCRAPING KHÓA HỌC NỔI BẬT UNICA
# ## (Scrapping out standing courses on this Unica platform)

# In[ ]:


# using chrome driver for get the source of page on chrome web browser
driver = webdriver.Chrome(r'C:\Users\DELL\Desktop\Python-project\WEB SCRAPING\chromedriver.exe')
driver.get('https://unica.vn/khoa-hoc-noi-bat')

for i in range(0,10):
    try:
        btn = driver.find_element('xpath','//*[@id="btn-load-more"]')
       # class_name = btn.get_attribute("class")
        driver.execute_script ("arguments[0].click();",btn)
        time.sleep(5)
    except NoSuchElementException:
        print("element does not exist")
        break


# In[ ]:


# use bs4 for scraping all info of page
soup = BeautifulSoup(driver.page_source, 'lxml')
df = pd.DataFrame({'Link':[''], 'Name':[''], 'Teacher':[''],'Price':[''],'Ratings':[''],'Sales':[''],'Origin_price':['']})
courses = soup.find_all('div',class_ = "col-md-3 col-sm-6 col-xs-12 form-group")
for course in courses:
    name = course.find('h3', class_='title-course').text
    link = course.find('a', class_='course-box-slider pop').get('href')
    teacher = course.find('div', class_='name-gv').text
    #image = course.find('img', class_='img-responsive ').get('src')
    price = course.find('span', class_ ='price-a').text
    ori_price = course.find('span', class_="price-b").text
    star = len(course.find_all('i',class_="fa fa-star co-or"))
    mems = course.find('span', 'star-rate').text
    df = df.append({'Link':link, 'Name':name, 'Teacher':teacher,'Price':price,'Ratings':star,'Sales':mems,'Origin_price':ori_price}, ignore_index=True) 
# the scraped results will be stored in first data frame table named df (with all the field columns in the dictionary above)


# In[ ]:


# View the results
df


# In[ ]:


# upload the table need to be update 
dftt =pd.read_csv(r'C:\Users\DELL\Desktop\unica\total_update.csv')
dftt


# In[ ]:



for value in df['Name']:
    if value in dftt['Tên'].values:
        # Get the index of the row where the value exists in Table 2
        row_index = dftt[dftt['Tên'] == value].index[0]
        
        # Add a value to another column at the located row in Table 2
        dftt.at[row_index, 'Danh mục'] = dftt.at[row_index, 'Danh mục']+', Top bán chạy'


# In[ ]:


dftt['Danh mục'][0]


# In[ ]:


dftt.to_csv(r'C:\Users\DELL\Desktop\unica\total.csv')


# # cập nhật giá khóa học
# # (Updating the courses prices)

# In[ ]:


driver = webdriver.Chrome(r'C:\Users\DELL\Desktop\Python-project\WEB SCRAPING\chromedriver.exe')
driver.get('https://unica.vn/khoa-hoc-noi-bat')

while True:
    try:
        btn = driver.find_element('xpath','//*[@id="btn-load-more"]')
       # class_name = btn.get_attribute("class")
        driver.execute_script ("arguments[0].click();",btn)
        time.sleep(5)
    except NoSuchElementException:
        print("element does not exist")
        break


# In[ ]:


# I will scrape the data again to collect exactly prices and more infomation
df = pd.DataFrame({'Link':[''], 'Name':[''], 'Teacher':[''],'Price':[''],'Ratings':[''],'Sales':[''],'Origin_price':['']})
soup = BeautifulSoup(driver.page_source, 'lxml')
courses = soup.find_all('div',class_ = "col-md-3 col-sm-6 col-xs-12 form-group")
for course in courses:
    name = course.find('h3', class_='title-course').text
    link = course.find('a', class_='course-box-slider pop').get('href')
    teacher = course.find('div', class_='name-gv').text
    #image = course.find('img', class_='img-responsive ').get('src')
    price = course.find('span', class_ ='price-a').text
    ori_price = course.find('span', class_="price-b").text
    star = len(course.find_all('i',class_="fa fa-star co-or"))
    mems = course.find('span', 'star-rate').text
    df = df.append({'Link':link, 'Name':name, 'Teacher':teacher,'Price':price,'Ratings':star,'Sales':mems,'Origin_price':ori_price}, ignore_index=True) 


# In[ ]:


# Clean the wrong formats and errors in the raw data
df.dropna(inplace=True)
df['Origin_price']=df['Origin_price'].apply(lambda x: x.replace('\n','').replace('đ','').replace('.',''))
df['Price']=df['Price'].apply(lambda x: x.replace('\n','').replace('đ','').replace('.',''))


# In[ ]:


# convert data types
df = df.drop(0)
df['Origin_price']=df['Origin_price'].astype(int)
df['Price']=df['Price'].astype(int)


# In[ ]:


# check the price
df['Origin_price'][835]


# In[ ]:


# read the old products (courses) file
dftt =pd.read_csv(r'C:\Users\DELL\Desktop\unica\total.csv')
dftt


# In[ ]:


# I use this file multiple times, so the lib need to be called again
# update the price from new data to old data file
import pandas as pd
# Compare the 'Tên' column in df with dftt
for index, row in df.iterrows():
    ten = row['Name']
    matching_row = dftt[dftt['Tên'] == ten]
    
    if not matching_row.empty:
        gia_ban_thuong = row['Origin_price']
        gia_khuyen_mai = row['Price']
        
        dftt.loc[matching_row.index, 'Giá bán thường'] = gia_ban_thuong
        dftt.loc[matching_row.index, 'Giá khuyến mãi'] = gia_khuyen_mai


# In[ ]:


for index, row in dftt.iterrows():
    if pd.isna(row['Giá khuyến mãi']):
        row['Giá khuyến mãi'] == row['Giá bán thường']


# In[ ]:


index = dftt[dftt['Giá khuyến mãi'].isna() == True]
index


# In[ ]:


dftt['Giá khuyến mãi'][1643]


# In[ ]:


dftt.to_csv(r'C:\Users\DELL\Desktop\unica\total_update.csv')


# In[ ]:


#check the updated result
value = 'Đọc sách siêu tốc'
index = dftt[dftt['Tên']==value]
index


# In[ ]:


type(dftt['Giá khuyến mãi'][835])


# In[ ]:


dftt.columns


# # Cập nhật UNICA (New Version)
# # (The new verion data updating because of the change of the website structure

# In[ ]:


# because of the accurate rate of the first version, i decided to change a new version 
#that I only need to scrape 3 fields(name of course, original price and promotional price)


# In[1]:


import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# In[4]:


driver = webdriver.Chrome(r'C:\Users\DELL\Desktop\Python-project\WEB SCRAPING\chromedriver.exe')


# In[5]:


df_tt = pd.DataFrame({'Tên':[''], 'Giá bán thường':[''],'Giá khuyến mãi':['']})
for i in range(0,11):
    driver.get('https://unica.vn')
    btn1 = driver.find_element('xpath','//*[@id="today-learn-home"]/ul/li[' + str(i+1) + ']/a')
   # class_name = btn.get_attribute("class")
    driver.execute_script ("arguments[0].click();",btn1)
    time.sleep(5)
    
    while True:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        courses = soup.find_all('div', class_='detail-course')
        for course in courses:
            try:
                name = course.find('h3', class_='name-course').text
                price =course.find('div', class_='price_sale').text
                ori_price = course.find('div', class_='price_origin').text
            except:
                pass
            df_tt = df_tt.append({'Tên':name, 'Giá bán thường':ori_price, 'Giá khuyến mãi':price},ignore_index=True)
        try:
            btn2 = driver.find_element('xpath', '//*[@id="list_product"]/div[2]/ul/li[7]/a')
            driver.execute_script ("arguments[0].click();",btn2)
            time.sleep(5)
        except NoSuchElementException:
            print("element does not exist")
            break

df_tt = df_tt.drop(0)
df_tt['Giá khuyến mãi']=df_tt['Giá khuyến mãi'].apply(lambda x: int(x.replace('\n','').replace('                                                ','').replace('đ','').replace('.','')))
df_tt['Giá bán thường']=df_tt['Giá bán thường'].apply(lambda x: int(x.replace('\n','').replace('                                                ','').replace('đ','').replace('.','')))


# In[6]:


df_tt.head()


# In[5]:


df_tt.to_csv(r'C:\Users\DELL\Desktop\unica\file-csv-courses\total_update_price.csv')


# In[3]:


df_tt= pd.read_csv(r'C:\Users\DELL\Desktop\unica\file-csv-courses\total_update_price.csv')


# In[4]:


df_tt


# In[21]:


df_tt.to_csv(r'C:\Users\DELL\Desktop\unica\file-csv-courses\total_update_price.csv')


# In[8]:


dftt =pd.read_csv(r'C:\Users\DELL\Desktop\unica\file-csv-courses\total.csv')
for index, row in df_tt.iterrows():
    ten = row['Tên']
    matching_row = dftt[dftt['Tên'] == ten]
    
    if not matching_row.empty:
        gia_ban_thuong = row['Giá bán thường']
        gia_khuyen_mai = row['Giá khuyến mãi']
        
        dftt.loc[matching_row.index, 'Giá bán thường'] = gia_ban_thuong
        dftt.loc[matching_row.index, 'Giá khuyến mãi'] = gia_khuyen_mai


# In[9]:


dftt= dftt.drop('Unnamed: 0', axis=1)
dftt.to_csv(r'C:\Users\DELL\Desktop\unica\file-csv-courses\total.csv')


# In[11]:


df=pd.read_csv(r'C:\Users\DELL\Desktop\unica\file-csv-courses\total.csv')


# In[12]:


df_unique = df.drop_duplicates(subset=['Tên'], keep='first')    


# In[13]:


df_unique[df_unique['Tên']=='Bí mật Thiền ứng dụng thay đổi cuộc đời']['Danh mục']


# In[14]:


df_unique.to_csv(r'C:\Users\DELL\Desktop\unica\file-csv-courses\total.csv')


# In[8]:


dftt.to_csv(r'C:\Users\DELL\Desktop\unica\file-csv-courses\total.csv')


# In[ ]:




