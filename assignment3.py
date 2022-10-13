#Web crawler 
from bs4 import BeautifulSoup
import queue
import os
import re
from urllib.parse import urlparse
from urllib.parse import urljoin
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import time

email_address = []
t_end = time.time() + 60 * 60

driver = webdriver.Chrome(ChromeDriverManager().install())

os.chdir('C:/root')
baseDir=os.getcwd()

url_base = "https://www.stevens.edu"

#Check for net location 
def is_absolute(url):
       return bool(urlparse(url).netloc)    

#Writes to csv 
def csv_generat(domain, view_source):    
    file_name = domain.replace("#","/").split('/')[-1]
    folder_name = domain.replace("#","/").removeprefix(url_base)    
    print(baseDir+folder_name+"/"+str(file_name)+'.csv')
    fieldnames = ['domain', 'output']    
    if domain == url_base:
       with open(baseDir+"/"+'root.csv', 'w', newline='') as csvfile:
              writer = csv.DictWriter(csvfile, fieldnames=fieldnames)              
              writer.writerow({'domain': domain, 'output': str(view_source)})
    else:      
       folder_exist = os.path.exists(baseDir+folder_name)
       if folder_exist:
              with open(baseDir+folder_name+"/"+str(file_name)+'.csv', 'w', newline='') as csvfile:
                     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)              
                     writer.writerow({'domain': domain, 'output': str(view_source)})

q = queue.Queue()

q.put(url_base)       

while time.time() < t_end:   
           
    url = q.get()
    print(url)
    driver.get(url)
    
    #Scroll to the end of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)#sleep_between_interactions    
    
    view_source = BeautifulSoup(driver.page_source, 'html.parser')   
    
    if "#page" not in url:
       csv_generat(url,view_source.prettify().encode('cp1252', errors='ignore'))
    
    email_address += re.findall("\S+@\S+",view_source.get_text())

    links = view_source.find_all('a')

    for link in links:
        u = link.get("href")    
       #  print("href :" +u)   
        if not is_absolute(u):     
            url_join = urljoin(url,u)  
            if is_absolute(url_join):                   
              #  print("url_join :"+ url_join)  
               if u != None:                     
                     dirName = str(baseDir) +"/"+(u.replace("?","/").replace(":","/").replace("#","/")) 
                     # print("dirName :"+ dirName)   
                     if not os.path.exists(dirName):
                            os.makedirs(dirName)                               
                            print("Directory " , dirName ,  " Created ")
                     else:
                            print("Directory " , dirName ,  " already exists")
              
                     if url_join not in q.queue:                
                            q.put(url_join)
    print(q._qsize())
        
print(email_address)
with open(baseDir+'email_address.csv', 'w', newline='') as csvfile:
       fieldnames = ['email_address']    
       writer = csv.DictWriter(csvfile, fieldnames=fieldnames)              
       writer.writerow({'email_address': email_address})