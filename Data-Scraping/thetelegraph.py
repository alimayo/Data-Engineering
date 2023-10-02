import requests
from bs4 import BeautifulSoup
import re
import datetime
import validators

def get_sites_from_website(website) :
  #getting html content from webpage
  theT = requests.get(website)
  mainpage = theT.content
  #making soup to deal with/ extract from HTML content
  soup = BeautifulSoup(mainpage, 'html5lib')
  #dealing with the html content
  #getting links to prinmary categories of the website
  site_a = (soup.find_all('a', {"class": "e-navigation-primary-item__link"}))
  p_sites = []
  for a in site_a:
    if ("https://" in (a['href'])):
      p_sites.append(a['href'])
    else:
      p_sites.append(("https://www.telegraph.co.uk" + a['href']))

  #getting links to secondary and tertiary categories in each primary category site of the website
  st_sites = []
  for site in p_sites:
    T_cat = requests.get(site)
    coverpage = T_cat.content
    soup2 = BeautifulSoup(coverpage, 'html5lib')

    s_sites = soup2.find_all('a', {"class": "e-navigation-secondary-item__link"})  
    t_sites = soup2.find_all('a', {"class": "e-navigation-tertiary-item__link"})

    st_sites.extend(s_sites)
    st_sites.extend(t_sites)
  
  for n in range(len(st_sites)):
    if ('https://' not in (st_sites[n])['href']):
      st_sites[n] = ("https://www.telegraph.co.uk" + (st_sites[n])['href'])
    else:
      st_sites[n] = (st_sites[n])['href']
  
  #getting article links from all site pages secondary and tertiary category pages
  links = []
  for st in st_sites:
    #print(st)
    if ((validators.url(st) == True) and ('https://www.' in st)):
      #print(st)
      T_stcat = requests.get(st)
      coverpage = T_stcat.content
      soup3 = BeautifulSoup(coverpage, 'html5lib')
      
      sections = soup3.find_all('section', {"class": "article-list"})
      for section in sections:
        links.extend(section.find_all('a', href=True))
    else:
      pass

  for n in range(len(links)):
    if 'https://' not in (links[n])['href']:
      links[n] = ("https://www.telegraph.co.uk" + (links[n])['href'])
    else:
      links[n] = ((links[n])['href'])
      
 
  links_set = set(links)  
  ulinks = list(links_set)
  return ulinks

#function definition for getting article content saved into file for any href passsed to it-------------
def get_content(href):
  h = requests.get(href,allow_redirects=False)
  article_page = h.content
  soup2 = BeautifulSoup(article_page, 'lxml')

  title = ''
  if (soup2.find('main' , {'class' : 'container article'})):
    title = soup2.find('h1' , {'itemprop' : 'headline'})
  elif soup2.find('main' , {'class' : 'row article__body'}):
    title = soup2.find('h1' , {'itemprop' : 'headline name'})
  else:
    #print("no title")
    title = None


  if title != None :
    if (soup2.find("div",  {'itemprop' : 'articleBody'})):
      pp = soup2.find("div",  {'itemprop' : 'articleBody'}) 
    else:
      pp = soup2.find("article",  {'itemprop' : 'articleBody'}) 
    if pp != None :
      ##  getting all paragraph content 
      ppp = pp.find_all('p')
      paras = "" #list for storing all p tag content of article 
      #iterating over list to create content output of article to store in file
      for p in ppp: 
        paras = paras + (p.text)
      
      ## getting author name
      author_name = ""
      if (soup2.find('div' , {'class' : 'article__byline-date'})):
        an = (soup2.find('div' , {'class' : 'article__byline-date'}).find_all('span' , {'itemprop' : 'name'}))
        for a in an:
            author_name += (a.text)
      elif (soup2.find('div' , {'class' : 'article-author__primary'})):
         an = (soup2.find('div' , {'class' : 'article-author__primary'}).find_all('span' , {'itemprop' : 'name'}))
         for a in an:
            author_name += (a.text)
      elif (soup2.find('div' , {'class' : 'byline--comment'})):
        an = (soup2.find('div' , {'class' : 'byline--comment'}).find_all('span' , {'itemprop' : 'name'}))
        for a in an:
            author_name += (a.text)
      else:
        #print("no author name")
        author_name = None
        pass

      if (not author_name.strip()) or (author_name == None):
        author_name = "Not mentioned"
        

      ## getting publish date
      if (soup2.find('time' , {'itemprop' : 'datePublished'})) :
        dp = (soup2.find('time' , {'itemprop' : 'datePublished'}).text).strip()
        e_index = ((dp[2:]).index('20'))
        dop = (dp.strip())[:e_index+6]
        dopp = datetime.datetime.strptime((dop.strip()), "%d %B %Y").strftime('%Y-%m-%d')
      else:
        dopp = "Not mentioned"
      
      ## getting extraction date
      doe = str(datetime.date.today())

      ## gathering content to be saved in file
      article_content = ("Source : " + "The Telegraph"  + 
                         "\nLink : " + href  +
                      "\nDate of Publication : " + dopp +
                      "\nDate of Extraction : " + doe +
                      "\nAuthor : " + author_name.strip() +
                      "\nTitle : " + (title.text).strip()  +  
                      "\nArticle : " + paras)
      
      #print(article_content)

      create_file(title, article_content)
    #else:
      #print("no pp")
  #else:
    #print("no title")

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
  hrefs = get_sites_from_website('https://www.telegraph.co.uk/')
  for href in hrefs:
    #print(href)
    get_content(href)

main()