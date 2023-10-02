import requests
from bs4 import BeautifulSoup
import re
import datetime
import validators

#function definition for getting the main categories and subcategories of website---------------------------
def get_categorypages_from_website(website) :
  #a category page is one which contains all articles related to that category
  categ_pages_f = []
  finding_categ(website, categ_pages_f)
  cp2 = categ_pages_f.copy()
  for link in cp2:
    finding_categ(link, categ_pages_f)

  #rechecking if category page
  cp3 = categ_pages_f.copy()
  for cuuu in cp3:
    if validators.url(cuuu):
      cpr = requests.get(cuuu)
      page = cpr.content
      soup = BeautifulSoup(page, 'html5lib')
      if (soup.find('h1', {"class": "category-heading"}) == None):
        #print("removing : " + cuuu)
        categ_pages_f.remove(cuuu)
      else:
        #print("not removing : " + cuuu)
        pass
    else:
      #print("removing invalid url : " + cuuu)
      categ_pages_f.remove(cuuu)

  return categ_pages_f

#a function for finding possible category page links from a given site link
def finding_categ(site, categ_pages):
  #getting html content from site
  IndiaToday = requests.get(site)
  mainpage = IndiaToday.content
  #making soup to deal with/ extract from HTML content
  soup = BeautifulSoup(mainpage, 'html5lib')
  #dealing with the html content
  if (soup.find_all('span', {"class": "widget-title"})):
    titles = soup.find_all('span', {"class": "widget-title"})
    for s in titles:
      if s.find('a'):
        categ_pages.append('https://www.indiatoday.in' + (s.find('a'))['href'])
  return categ_pages

#function for getting article links
def get_hrefs(website):
  categ_pages_ff = get_categorypages_from_website(website)
  ahrefs = []
  for cp in categ_pages_ff:
     cp_req = requests.get(cp)
     page = cp_req.content
     soup = BeautifulSoup(page, 'html5lib')
     container = soup.find('div', {"class": "view-content"})
     ahrefs.append(container.find_all('a'))
  
  hrefs = []
  for ahlist in ahrefs:
    for ahref in ahlist:
      if (ahref['href']).startswith('https://www'):
        hrefs.append(ahref['href'])
      else:
        hrefs.append('https://www.indiatoday.in' + ahref['href'])
      

  hrefs_set = set(hrefs)  
  uhrefs = list(hrefs_set)
  
  return uhrefs

#function definition for getting article content saved into file for any href passsed to it-------------
def get_content(href):
  h = requests.get(href)
  article_page = h.content
  soup2 = BeautifulSoup(article_page, 'lxml')

  title = soup2.find('h1' , {'itemprop' : 'headline'})

  if title != None :
    pp = soup2.find("div",  {'class' : 'story-left-section story-update'}) 
    if pp != None :
      ##  getting all paragraph content 
      ppp = pp.find_all('p') 
      paras = "" #list for storing all p tag content of article 
      #iterating over list to create content output of article to store in file
      for p in ppp: 
        paras = paras + (p.text)
      
      ## getting author name
      author_name = (soup2.find('span' , {'itemprop' : 'author'}).find('dt' , {'itemprop' : 'name'})).text

      ## getting publish date
      dop = ((soup2.find('dl' , {'class' : 'profile-byline'}).find('dt' , {'class' : 'pubdata'})).text).strip()
      dopp = datetime.datetime.strptime((dop.replace(",","")), "%B %d %Y").strftime('%Y-%m-%d')
      
      ## getting extraction date
      doe = str(datetime.date.today())

      ## gathering content to be saved in file
      article_content = ("Source : " + "India Today"  + 
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
  t=title.text
  t = re.sub('[^a-zA-Z0-9]', '_', t)
  filename = t + ".txt"
  
  # write in file
  with open(filename, "w", encoding="utf-8") as file_object:
    #str_to_write = 'Title : '+ t +'\n\n'+ 'Article content : \n'+ article_content
    file_object.write(article_content)
  return

def main(): 
  hrefs = get_hrefs('https://www.indiatoday.in')
  for href in hrefs:
    print(href)
    get_content(href)

main()