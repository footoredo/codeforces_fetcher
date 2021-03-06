import requests
import re
import socket
from BeautifulSoup import BeautifulSoup

failure_links = open("failure_links","a")

key_word = "random"

def get_editorial(link):
  failed_connection_count=0;
  while(failed_connection_count<3):
    try:
      r = requests.get(link,timeout=10)
      break
    #except (requests.exceptions.Timeout,socket.timeout):
    #  print "Timeout connecting " + link +". Reconnecting.."
    #  time_out_count+=1
    except (requests.exceptions.RequestException,socket.timeout):
      print "Failed connecting " + link +". Reconnecting.."
      failed_connection_count+=1
  
  if (failed_connection_count==3):
    failure_links.write(link+'\n');
    return []
  
  soup = BeautifulSoup(r.text)
    
  return map( lambda x: x.parent['href'] if re.match(r"http.*",x.parent['href']) else "http://codeforces.com"+x.parent['href'], soup.findAll(name='a',text=re.compile(r"Tutorial")) )
    
def contenting_random(link):
  failed_connection_count=0;
  while(failed_connection_count<3):
    try:
      r = requests.get(link,timeout=10)
      break
    #except (requests.exceptions.Timeout,socket.timeout):
    #  print "Timeout connecting " + link +". Reconnecting.."
    #  time_out_count+=1
    except (requests.exceptions.RequestException,socket.timeout):
      print "Failed connecting " + link +". Reconnecting.."
      failed_connection_count+=1
  
  if (failed_connection_count==3):
    failure_links.write(link+'\n');
    return []
  
      
  soup = BeautifulSoup(r.text)
  entry = soup.findAll(attrs={'class':'ttypography'})[0].text
 
  return re.compile(r'.*'+key_word+'*').match(entry)

def check(link):
  return filter( contenting_random, get_editorial(link) )
  
entries = open('entries.txt','a')
suffix = "http://codeforces.com/contest/"
for i in range(1,600):
  print "Checking contest #"+str(i)+'...'
  valids = check(suffix+str(i))
  #print valids
  for link in valids:
    entries.write(link+"\n")
    
entries.close()
failure_links.close()

