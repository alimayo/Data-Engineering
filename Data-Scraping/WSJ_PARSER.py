from bs4 import BeautifulSoup
from datetime import date
import datetime
import requests
import re
import os
from time import sleep
today = date.today()
f1="%b. %d, %Y %I:%M"
f2="%B %d, %Y %I:%M"
f3="%B %d, %Y"



#Updated Jan. 29, 2021 2:42 pm ET
#Sept. 14, 2020 11:51 am ET
#Correcting the link
def correct_link(current_link):
  #link='https://www.wsj.com/'
  if (current_link==None or current_link[0] == '/'): 
    pass
  elif current_link.startswith("https://www.wsj.com/"): 
    link=current_link
    str(link)
    return link
  elif (current_link[0] == '#'):
    pass
  elif not current_link.startswith("https://www.wsj.com/"): 
    pass 
  #else:
    #link='https://www.wsj.com/' 

#Filtering of links
def filter_link(list_link):  
    list_set = set(list_link)  
    all_links = (list(list_set)) 
    return all_links


#File Creation
def create_file(title, article_paragraphs):

  title = re.sub('[^ a-zA-Z0-9:)]', '', title)  
  f_name = "".join(i+" " for i in re.findall("[A-Za-z0-9]+",title))
  f_name = f_name + "_" + ".txt"
  with open(f_name, "w", encoding="utf-8") as file_object:
    file_object.write(article_paragraphs)
  return
#Extracting All the links to the  news articles

def date_check(time) :
    try:
        datetime.datetime.strptime(time, f1)
        date=datetime.datetime.strptime(time, f1).date()
        #print(date)
        return date
         
    except :
      pass
    try:
        datetime.datetime.strptime(time, f2)
        date=datetime.datetime.strptime(time, f2).date()
        #print(date)
        return date
         
    except :
      pass   
    try:
        datetime.datetime.strptime(time, f3)
        date=datetime.datetime.strptime(time, f3).date()
        #print(date)
        return date
         
    except :
      pass  
   
def all_links(url):
  source=requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
  soup=BeautifulSoup(source.text,'html.parser')
  l=[]
  links=soup.find_all('a')
  for n in range(0,len(links)):
    partial_link=links[n].get('href')
    link = correct_link(partial_link)
    if link:
      l.append(link)
      data = requests.get(link,headers={'User-Agent': 'Mozilla/5.0'})
      soup = BeautifulSoup(data.text,'html.parser')
      sublinks = soup.find_all("a")
      if sublinks:
        for i in sublinks:
          try:
            href = i['href']
            s_link = correct_link(href)
            if s_link:
              l.append(s_link)
            else:
              pass  

          
          except:
            continue
      else:
        pass      
    else:
      pass         
    
    
    
    
     
  
  return l


 
def parser(links_list):
  num=1
  print("Total Unique Links:",len(links_list))
  for i in range(0,len(links_list)):
    current_url=links_list[i] 
    #print(ur)
    
    try:
      
      source=requests.get(current_url,headers={'User-Agent': 'Mozilla/5.0'})
      #sleep(2)
    except requests.exceptions.ConnectionError:
        #source.status_code = "Connection refused"
        continue

    
    soup=BeautifulSoup(source.content,'lxml')
    #headline=soup.find("h1", class_="wsj-article-headline")
    #s_headline=soup.find("h2", class_="sub-head")

    arthur=soup.find('button',class_="author-button")

    time=soup.find('time',class_="timestamp article__timestamp flexbox__flex--1")
    
    
    #p_tags = soup.find_all('p')
    p_tags=soup.find("div",class_='wsj-snippet-body')
    #print(p_tags.text)

    #print(i)
    #print(current_url)
    ##para=[]

    
    if p_tags== None or time==None or arthur==None :
      pass
    else:
      #print(current_url)
      #para.append(headline.text)   
      #para.append(s_headline.text)
      
      #for d in range(0,len(p_tags)):
      #  d_=p_tags[d].text
      #  para.append(d_)
      #text="\n".join(para)  
      text=p_tags.text
      Current_Date = today.strftime("%Y-%m-%d")
      
      title=soup.find('title')
      
      time=time.text
      
#time1=time1.replace("          ",'')
      time=time.replace("Updated ",'')
      time=time.replace(" ET",'')
      time=time.replace("am","")
      time=time.replace("pm","")
      time=time.replace("Sept","Sep")
      
      #print(current_url)
      #print(time)
      #time=datetime.datetime.strptime(time, '%B %d, %Y').date()
  
      #print(time.strip())
      time=date_check(time.strip())
      time=str(time)
      #print(time)
      Content_="Source: The WSJ; "+"Link: " + current_url +"; " + "DateOfExtraction:"+ Current_Date + "; " + "DateOfPublication:" + time +"; " +"Authors:"  + arthur.text + "; " + "Title:" + title.text +"\n" +"Article:" + text
      #print(C
      if Content_:
        print(num,"Content Found on:",links_list[i])
        
      
        #title=soup.find('title')

        title=str(num)+":)"+ title.text
      
        create_file(title,Content_)
        num=num+1
        
  print("DONE:") 

def main():
  print(":::Welcome to the WSJ Parser:::") 
  A_links=all_links("https://www.wsj.com/")
  print("Total links are:",len(A_links))
  f_links=filter_link(A_links)
  
  print("Filtered links are:",len(f_links))
  #f_links=["https://www.wsj.com/articles/mrna-covid-19-vaccines-are-fast-to-make-but-hard-to-scale-11614776401?mod=tech_featst_pos2","https://www.wsj.com/articles/anya-taylor-joy-on-the-queens-gambit-and-dancing-at-the-end-of-the-pandemic-11604681940","https://www.wsj.com/articles/what-chip-shortage-toyota-sees-production-profit-rising-11612944257","https://www.wsj.com/articles/climates-big-unknown-whats-happening-beneath-antarcticas-ice-11546102801"]
  parser(f_links)

if __name__ == "__main__":
    main()  
  



