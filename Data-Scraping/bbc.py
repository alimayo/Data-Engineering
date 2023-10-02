import requests
from bs4 import BeautifulSoup
import numpy as np
import re
from datetime import datetime

# ----------------- /architecture0 www.bbc.com homepage parser--------------------------------------------
def arch0_extract_urls(url):
  r1 = requests.get(url)
  bbcnews_coverpage = r1.content

  soup1 = BeautifulSoup(bbcnews_coverpage, 'lxml')
  #coverpage_news = soup1.find_all('a', class_= 'media__link')
  coverpage_news = soup1.find_all('a', class_= ['media__link', 'block-link__overlay-link'])

  # list_link = []
  for n in range(0,len(coverpage_news)):
    partial_link=coverpage_news[n].get('href')
    link = correct_link(partial_link)

    if (link == None):
      continue
    else:
      list_link.append(link)

  # print(list_link)
  print(len(list_link))
  return list_link

# ----------------- /architecture1 parser--------------------------------------------
def arch1_extract_urls(url):
  r1 = requests.get(url)
  bbcnews_coverpage = r1.content

  soup1 = BeautifulSoup(bbcnews_coverpage, 'lxml')
  coverpage_news = soup1.find_all('a', class_= 'gs-c-promo-heading')

  # list_link = []
  for n in range(0,len(coverpage_news)):
    partial_link=coverpage_news[n].get('href')
    link = correct_link(partial_link)

    if (link == None):
      continue
    else:
      list_link.append(link)

  print(len(list_link))
  # print(list_link)
  return list_link

# ----------------- /architecture2 parser--------------------------------------------
def arch2_extract_urls(url):
  r1 = requests.get(url)
  bbcnews_coverpage = r1.content

  soup1 = BeautifulSoup(bbcnews_coverpage, 'lxml')
  coverpage_news = soup1.find_all('a', class_= 'rectangle-story-item__title')
  # coverpage_news = soup1.find_all('a')

  # list_link = []
  for n in range(0,len(coverpage_news)):
    partial_link=coverpage_news[n].get('href')
    link = correct_link(partial_link)
    
    if (link == None):
      continue
    else:
      list_link.append(link)

  # print(list_link)
  print(len(list_link))
  return list_link

# ----------------- /architecture3 parser-------------------------------------
def arch3_extract_urls(url):
  r1 = requests.get(url)
  bbcnews_coverpage = r1.content
  soup1 = BeautifulSoup(bbcnews_coverpage, 'lxml')
  coverpage_news = soup1.find_all('a', {"data-cs-element-type": "story-promo-link"})
  # coverpage_news = soup1.find_all('a')
  # list_link = []
  for n in range(0,len(coverpage_news)):
    partial_link=coverpage_news[n].get('href')
    link = correct_link(partial_link)
    if (link == None):
      continue
    else:
      list_link.append(link)
  # print(list_link)
  print(len(list_link))
  return list_link


# ------------------------- CORRECT LINK ----------------------------------
discarded_url_list= []
def correct_link(partial_link):
  if (partial_link[0] == 'h'): #i.e. link starts with https://...
    link = partial_link
  else: 
    link = 'https://www.bbc.com' + partial_link #i.e. link starts with /news or /sports...

  str(link)
  numberLinkFlag = hasNumbers(link) #hasnumbers function called

  if (numberLinkFlag == True) & (link[8] == 'w'):
    return link
  else:
    discarded_url_list.append(partial_link)
    return None


  return

# ------------------------- HAS NUMBERS ----------------------------------
# Inferred by research: any link containing numeric value is an article(i.e. has detailed content) therefore we will parse it
def hasNumbers(inputString):
  if(inputString==None) or ('covid-19' in inputString):
  # if(inputString==None):
    flag= False
    return flag
  else:
    flag = any(char.isdigit() for char in inputString)
  # print(flag)
  return flag


# ------------------------- UNIQUE URLS ----------------------------------
# check for redundant elements in list, get only unique links
def unique(list_link): 

    # print("list link length") 
    # print(len(list_link))

    list_set = set(list_link) 
    coverpage_news = (list(list_set)) 

    print("unique coverpage news length")
    print(len(coverpage_news))
    return coverpage_news
# ------------------------- SCRAPING ARTICLES ----------------------------------
def scraping_articles(unique_list_link):
  number_of_articles = len(unique_list_link)

  for n in np.arange(0, number_of_articles):
    print(n)
    url= unique_list_link[n]
    print(url)
    r2 = requests.get(url)
    article_coverpage = r2.content

    soup2 = BeautifulSoup(article_coverpage, 'lxml')
    x = soup2.find_all('p')

    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
      paragraph = x[p].get_text()
      list_paragraphs.append(paragraph)
    article_paragraphs = "\n".join(list_paragraphs)

    title=soup2.find('title')
    print(title)
    if (title == None):
      title = url[20:]
    else:
      title=title.string


# ------------------------- FIND DATE AND AUTHOR -----------------------------
    try:
      author = None
      date = None
      if (soup2.find('time') is not None):
        date = soup2.find('time').get('datetime') #string returned format 2020-12-25T12:20:39:000Z
        if (len(date)>12) and (soup2.find('time').get('datetime') is not None):
          date = date[0:10]
        print('date: {}'.format(date))

        if (soup2.find('span', class_="qa-contributor-name") is not None):
          author = soup2.find('span', class_="qa-contributor-name").text
          print('author: {}'.format(author))

        elif (soup2.find('p', class_="css-1pjc44v-Contributor") is not None):
          author = soup2.find('p', class_="css-1pjc44v-Contributor").span.text
          print('author: {}'.format(author))
          
        print("\n")

      elif ((soup2.find_all('span', class_="publication-date") is not None) and len(soup2.find_all('span', class_="publication-date")) != 0 ): # condition: or len(soup2.find_all() == 0)
        date=soup2.find('span', class_="publication-date index-body").text
        print('date: {}'.format(date))

        author = soup2.find('div', class_ = 'source-attribution-detail').span.text #only returns author
        print("author: {}".format(author))
        print("\n")
        
      elif ((soup2.find_all('b', class_ = 'gel-brevier-bold') is not None) and (len(soup2.find_all('b', class_ = 'gel-brevier-bold')) != 0)): 
        date = soup2.find('b', class_ = 'gel-brevier-bold').text
        print (date)
        print("\n")

      elif ((soup2.find_all('div', class_ = 'author-unit__container') is not None) and (len(soup2.find_all('div', class_ = 'author-unit__container')) != 0 )):
        date = soup2.find('div', class_ = 'author-unit__container').span.text #------------------
        print('date: {}'.format(date))

        author = soup2.find('div', class_ = 'author-unit__container').a.text
        print('author: {}'.format(author))
        print("\n")
      
      elif ((soup2.find_all('span', class_ = 'publication') is not None) and (len(soup2.find_all('span', class_ = 'publication')) != 0)): #error

        date = soup2.find('div', class_ = 'source-attribution-detail')
        print(date)
        print("\n")

      else:
        date = "Date not found"
        author = "Author not found"
        print('date: {}'.format(date))
        print('author: {}'.format(author))
        print("\n")

      if (author == None ):
        author = "Author not found"
        print('author: {}'.format(author))

      if (date == None):
        date = "Date not found"
        print('date: {}'.format(date))
        print("\n")

    except:
      date= "Date not found"
      author = "Author not found"
#----------------------- end of date try-catch ---------------------------------
      
    create_file(url, title, date, author, article_paragraphs) #call to create file
  return

# ------------------------- CREATE FILE ----------------------------------
def create_file(url, title, date, author, article_paragraphs):
  print(datetime.date(datetime.now()))
  link =  url
  date_of_extraction = datetime.date(datetime.now())
  date_of_publication = date
  #title = title
  
  meta_data_article = "Source: BBC; Link: {}; DateOfExtraction: {}; DateOfPublication: {}; Author: {}; Title: {};".format(
                    link, date_of_extraction, date_of_publication, author, title)

  t = re.sub('[^a-zA-Z0-9]', '_', title)
  filename = t + ".txt"
  
  # write in file
  with open(filename, "w", encoding="utf-8") as file_object:
    file_object.write(meta_data_article)
    file_object.write(article_paragraphs)
  return

#------------------------- MAIN FUNCTION ----------------------------------
list_link=[]
def main():

    print("Extracting URLs")
    list_arch0=['https://www.bbc.com']
    for url in list_arch0:
      list_link = arch0_extract_urls(url)

    list_arch1=['https://www.bbc.com/news', 'https://www.bbc.com/sport', 'https://www.bbc.com/weather']
    for url in list_arch1:
      list_link = arch1_extract_urls(url)

    list_arch2=['https://www.bbc.com/worklife', 'https://www.bbc.com/future', 'https://www.bbc.com/culture', 'https://www.bbc.com/culture/music']
    for url in list_arch2:
      list_link = arch2_extract_urls(url)

    list_arch3=['https://www.bbc.com/travel']
    for url in list_arch3:
      list_link = arch3_extract_urls(url)
    # reels, TV, sounds discarded

    unique_list_link = unique(list_link)
    scraping_articles(unique_list_link)

    #print(discarded_url_list)

# ------------------------- DRIVER CODE ----------------------------------
if __name__ == "__main__":
    main()

