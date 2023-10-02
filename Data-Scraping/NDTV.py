import requests 
from bs4 import BeautifulSoup 
from datetime import datetime
import re
today=datetime.today()
url = 'https://www.ndtv.com'
urls = [] 
urls.append(url)

n=0
int(n)
partial=[]
unknown=[]
failed=[]
partial_links=open('partial.text','w',)
for href in urls:
  # print(href)
  # time.sleep(2)
  reqst = requests.get(href)
  # print(reqst)
  soup1 = BeautifulSoup(reqst.text, 'html.parser')
  # 
  # heading=soup1.find('h1',class_="sp-ttl")
  art_div=soup1.find('section',class_="col-900 mr-60")
  try:
    # if link1.startswith("https://www.ndtv.com/"):
      # if(heading!= (None) or author !=(None)):
    if(art_div != None):
      heading= art_div.find("h1",{"class":"sp-ttl"})
      # print(heading.text)
      author= art_div.find("span",{"itemprop":"author"})
      # print(author.text)
      # art_date= art_div.find("span",{"itemprop":"dateModified"})
      # art_published_date=soup1.find("meta",{"itemprop":"datePublished"})
      publish_date=soup1.find("span",{"class":"pst-by_lnk"})
      # print(publish_date.text)

      publish_date_string=publish_date.text
      for pd in soup1.find_all("span",{"class":"pst-by_lnk"}):
        pdate=pd.text
      # date format "Updated: %B %d, %Y %I:%M %p %z"
        if pdate.startswith("Updated"):
          objDate = datetime.strptime(pd.text, 'Updated: %B %d, %Y %I:%M %p IST')
          # print("DateOfPublication:" + datetime.strftime(objDate,'%Y-%m-%d') +"; ")
          publish_date_string= "DateOfPublication:" + datetime.strftime(objDate,'%Y-%m-%d') +"; "
          break
        # else:
        #   print('date format change')
      
     
      btag=''
      article_b=soup1.find("div",{"class":"sp-cn ins_storybody"}).find('b')
      if article_b:
        # print(article_b.text)
        btag=article_b.text

      # article_c1=soup1.find("div",{"class":"sp-wrp"})
      article_c1=soup1.find_all('p')

      art_data=""
      for art in article_c1: 
        if (art.get('class')) or (art.text=='') or (art.text=="Follow Us:") or (art.text=="................................ Advertisement ................................"):
          # print("irrelevant p tag")
          # art_data += repr(art)+"\n"
          continue 
        art_data += repr(art.text)+"\n"
      # print(art_data)
      data = "Source: NDTV; Link:" + href + ";"+" DateOfExtraction:" + today.strftime("%Y-%m-%d") + "; "
      data +=publish_date_string
      data += "Author:"+author.text+";"+" Title:" + heading.text + ";"+"\nArticle:"+btag+art_data

      # if (heading):
        # print(heading)
      # elif (heading!= (None)):
      #   print("1"+heading)
      # else:
      #   print("heading not found.")
      #     # print(author)
      f=open(re.sub('[^a-zA-Z0-9]', '_', heading.text)+'.txt','w',errors="ignore")
      f.write(data)
      f.close()
      
  except:
      print("no a artical page:"+href)
  # 
  for link in soup1.find_all('a'): 
  # print(link.get('href')) 
    link1=link.get('href')
    try:
      if link1.startswith("https://www.ndtv.com"):
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