# -*- coding: utf-8 -*-
"""TheHindu_WebScraper_final.ipynb
"""
# importing the necessary packages
import requests
from bs4 import BeautifulSoup
import re
import datetime

#function definition for getting the main categories and subcategories of website---------------------------
def get_sites_from_website(website) :
  #getting html content from webpage
  theHindu = requests.get(website)
  mainpage = theHindu.content
  #making soup to deal with/ extract from HTML content
  soup = BeautifulSoup(mainpage, 'html5lib')
  #dealing with the html content
  sites = soup.find('div', {"id": "main-menu"}).find_all('meta', content=True)
  return sites

#function definition for getting relevant article from site---------------------------
def get_ahrefs_from_site(site, ahrefs) :
  #getting html content from webpage
  fox = requests.get(site)
  coverpage = fox.content
  #making soup to deal with/ extract from HTML content
  soup = BeautifulSoup(coverpage, 'html5lib')
  #dealing with the html content
  if soup.find('div', {"class": "main"}):
    ahrefs.append(soup.find('div', {"class": "main"}).find_all('a', href=True))
  elif soup.find('section', {"class": " "}):
    ahrefs.append(soup.find('section', {"class": " "}).find_all('a', href=True))
  else: 
    #print('error^')
    pass


#function definition for getting list of unique hrefs which will be extracted-----------------------
def get_hrefs(website, hrefs = []): 
  sites = get_sites_from_website(website)
  ahrefs = []
  for site in sites:
    get_ahrefs_from_site(site['content'],ahrefs)

  for ahlist in ahrefs:
    for ahref in ahlist:
      if (ahref['href']).startswith('https://'):
        hrefs.append(ahref['href'])
      else:    
        pass   
  hrefs_set = set(hrefs)  
  uhrefs = list(hrefs_set)
  return uhrefs

#function definition for getting article content saved into file for any href passsed to it-------------
def get_content(href):
  h = requests.get(href)
  article_page = h.content
  soup2 = BeautifulSoup(article_page, 'lxml')

  if ("thehindu.com/thread" in href): #thread series of the newspaper#it has different pattern of tags and classes
    title=soup2.find('h1' , {'itemprop' : 'headline'})
  else: 
    title=soup2.find('h1' , {'class' : 'title'})
  
  #saving title and content of article in file
  if title != None :
    pp = soup2.find("div", id=re.compile("^content-body-")) 
    if pp != None :
      ##  getting all paragraph content 
      ppp = pp.find_all('p') 
      paras = "" #list for storing all p tag content of article 
      #iterating over list to create content output of article to store in file
      for p in ppp: 
        paras = paras + (p.text)

      ## getting author name
      if ("thehindu.com/thread" in href):
        author_name = (soup2.find('ul' , {'class' : 'authorUL'}).find('h4' , {'itemprop' : 'name'})).text
      else :  
        author_name = soup2.select("a[class^=auth-nm]")
        if author_name:
          author_name = author_name[0].text
        else:
          author_name = " name not mentioned"

      ## getting publish date
      if ("thehindu.com/thread" in href):
        dop = (soup2.find('ul' , {'class' : 'authorUL'}).find('h5' , {'itemprop' : 'datePublished'})).text
      else : 
        dop = ((soup2.find('div' , {'class' : 'ut-container'}).find_all('span' , {'class' : 'blue-color ksl-time-stamp'})))
        try:
            dop[1]
        except :
            dop = dop[0].text
        else:
            dop = dop[1].text
        
      dopp = datetime.datetime.strptime((dop.replace(",","").replace(":"," ").replace("IST","")).strip(), "%B %d %Y %H %M").strftime('%Y-%m-%d')

      ## getting extraction date
      doe = str(datetime.date.today())
      
      ## gathering all file data stored
      article_content = ("Source : " + "The Hindu"  + 
                         "\nLink : " + href  +
                      "\nDate of Publication : " + dopp +
                      "\nDate of Extraction : " + doe +
                      "\nAuthor : " + author_name.strip() +
                      "\nTitle : " + (title.text).strip()  +  
                      "\nArticle : " + paras)

      create_file(title, article_content)

  return


#function definition for saving title and content of article in file--------------------------
def create_file(title, article_content):
  t=title.string
  t = re.sub('[^a-zA-Z0-9]', '_', t)
  filename = t + ".txt"
  
  # write in file
  with open(filename, "w", encoding="utf-8") as file_object:
    #str_to_write = 'Title : '+ t +'\n\n'+ 'Article content : \n'+ article_content
    file_object.write(article_content)
  return

def main(): 
  uhrefs = get_hrefs("https://www.thehindu.com/")
  for href in uhrefs:
    get_content(href)

main()