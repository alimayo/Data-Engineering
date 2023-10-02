from bs4 import BeautifulSoup
from datetime import date
import datetime
import requests
import re
import os

from time import sleep
today = date.today()
f1="%d %B, %Y %I:%M "
f2=" %d %B, %Y %I:%M "
#File Creation
def create_file(title, article_paragraphs):

  title = re.sub('[^ a-zA-Z0-9:)]', '', title)  
  f_name = "".join(i+" " for i in re.findall("[A-Za-z0-9]+",title))
  f_name = f_name + "_" + ".txt"
  with open(f_name, "w", encoding="utf-8") as file_object:
    file_object.write(article_paragraphs)
  return
#Checking Date
def date_check(time) :
    try:
        datetime.datetime.strptime(time, f1)
        date=datetime.datetime.strptime(time, f1).date()
        #print(date)
    except :
        date=datetime.datetime.strptime(time,f2).date()
        #print(date)
    return date
#Correction of link
def correct_link(current_link):
  link='https://theprint.in/'
  if (current_link==None or current_link[0] == '/'): 
    pass
  elif current_link.startswith("https://theprint.in/"): 
    link=current_link
  elif (current_link[0] == '#'):
    pass
  elif not current_link.startswith("https://theprint.in/"): 
    pass 
  else:
    link='https://theprint.in/'

  str(link)
  return link
#Filtering of links
def filter_link(list_link):  
    list_set = set(list_link)  
    all_links = (list(list_set)) 
    return all_links
#Extracting All URLs  
def all_links(url):
  source=requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
  soup=BeautifulSoup(source.text,'html.parser')
  l=[]
  links=soup.find_all('a')
  for n in range(0,len(links)):
    partial_link=links[n].get('href')
    link = correct_link(partial_link)
    data = requests.get(link,headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(data.text,'html.parser')
    sublinks = soup.find_all("a")
    
    if sublinks:
      for i in sublinks:
        try:
          href = i['href']
          s_link = correct_link(href)
          l.append(s_link)
        except:
          continue
    l.append(link)
  
  return l
#Extracting the Content
def parser(links_list):
  num=1
  print("Total Unique Links:",len(links_list))
  for i in range(0,len(links_list)):
    current_url=links_list[i] 
    
    try:
      source=requests.get(current_url,headers={'User-Agent': 'Mozilla/5.0'})
     
    except requests.exceptions.ConnectionError:
        #source.status_code = "Connection refused"
        continue

    
    soup=BeautifulSoup(source.content,'lxml')
    headline=soup.find("h1",class_="entry-title")
    s_headline=soup.find("h2",class_="td-post-sub-title")
    arthur=soup.find('a',class_="author url fn")

    time=soup.find('span', class_= 'update_date')
    p_tags=soup.find_all('div',class_="td-post-content")
    para=[]
    if headline==None or s_headline== None or time== None or arthur== None or  p_tags== None  :
      pass
    else:
      para.append(headline.text)   
      para.append(s_headline.text)
      for div in p_tags:
        for p in div.find_all('p'):
          
          para.append(p.text)
      del para[len(para)-7:len(para)]    
     
      text="\n".join(para)  
      Current_Date = today.strftime("%Y-%m-%d")
      
      
      title=soup.find('title')
      time=time.text
      time=time.replace("IST",'')
      time=time.replace("am","")
      time=time.replace("pm","")
      
  
      
      time=date_check(time)
      time=str(time)
      Content_="Source: The Print; "+"Link: " + current_url +"; " + "DateOfExtraction:"+ Current_Date + "; " + "DateOfPublication:" + time +"; " +"Authors:"  + arthur.text + "; " + "Title:" + title.text +"\n" +"Article:" + text
      
      if Content_:
        print(num,"Content Found on:",links_list[i])

        title=str(num)+":)"+ title.text
      
        create_file(title,Content_)
        num=num+1
        
  print("DONE:") 
url="https://theprint.in/"
def main():
  print(":::Welcome to The Print Parser:::") 
  A_links=all_links(url)
  print("Total links:",len(A_links))
  f_links=filter_link(A_links)
  print("Filtered links:",len(f_links))
  parser(f_links)


if __name__ == "__main__":
    main()

