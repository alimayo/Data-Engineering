import requests 
from bs4 import BeautifulSoup 
from datetime import datetime
import sys
import re
today=datetime.today()
url = 'https://www.dailytimes.com.pk'
urls = [] 
urls.append(url)

partial=[]
unknown=[]
failed=[]
writer=[]
partial_links=open('partial.text','w',)
for href in urls:
  href1=str(href)
  # print(href)
  # time.sleep(2)
  reqst = requests.get(href)
  # print(reqst)
  soup1 = BeautifulSoup(reqst.text, 'html.parser')
  # 
  # heading=soup1.find('h1',class_="sp-ttl")
  art_div=soup1.find('div',class_="post-header")
  # author=soup1.find('span',itemprop="author")
  if href1.startswith("https://dailytimes.com.pk/writer/"):
    # print("writer link:"+href)
    writer.append(href)
  elif href1.startswith("https://dailytimes.com.pk"):
    try:
      # if link1.startswith("https://www.ndtv.com/"):
        # if(heading!= (None) or author !=(None)):
      if(art_div != None):
        
        # print(art_div)
        # get_data(art_div)
        # heading=BeautifulSoup(art_div, 'html.parser').find('h1',itemprop_="headline").get_text()
        # print(heading)
        # heading=soup1.find_all('h1',class_="sp-ttl")
        # print(heading.text)
        heading= art_div.find("h1",{"class":"entry-title"})
        # print(heading.text)
        author= art_div.find("a",{"class":"author-name"})
        # print(author.text)
        publish_date= art_div.find("time",{"class":"entry-time"})
        # print(publish_date.text)
        # article_c=art_div.find("div",{"class":"sp-cn ins_storybody"}).find_all("p")
        # article_c=art_div.find_all("div",{"class":"sp-entry-content"})
        # print(article_c)
        art_div1=soup1.find('div',class_="entry-content")
        # print(art_div1.p.text)
        art_data=""
        for art in art_div1.stripped_strings:  
          art_data += repr(art)+"\n"
        data = "Source: DAILYTIMES; Link:" + href + ";"+" DateOfExtraction:" + today.strftime("%Y-%m-%d") + "; "
        #date conversion using datetime object
        objDate = datetime.strptime(publish_date.text, '%B %d, %Y')
        data += "DateOfPublication:" + datetime.strftime(objDate,'%Y-%m-%d') +"; "
        data += "Author:"+author.text+";"+" Title:" + heading.text + ";"+"\nArticle:"+art_data  
        # print(data)
        f=open(re.sub('[^a-zA-Z0-9]', '_', heading.text)+'.txt','w',errors="ignore")
        f.write(data)
        f.close()

    except:
          print("no a artical page:"+href+"\n"+str(sys.exc_info()))
  # 
  for link in soup1.find_all('a'): 
    # print(link.get('href')) 
    link1=link.get('href')
    try:
      if link1.startswith("https://dailytimes.com.pk"):
        if link1 in urls :
          continue
        else:
          urls.append(link.get('href'))
          # print(link.get('href'))
      elif link1.startswith("/"):
        partial.append(link.get('href'))
        print("partial link:"+str(link.get('href')),file=f)
        f.close()

      else:
        unknown.append(link1)
        # print("unkown link")
        continue
    except:
      # print("invalid href"+str(link1))
      failed.append(link1)

print("failled failledfailed:"+str(len(failed)))
print("unknown links:"+ str(len(unknown)))
print( "intrested links found:"+str(len(urls)))
print("writer links:"+str(len(writer)))