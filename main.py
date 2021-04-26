#import thư viện càn dùng
# import undetected_chromedriver as uc
#thư viện python dùng để lấy dữ liệu ra khỏi HTML và XML
from bs4 import BeautifulSoup
import re
#thư viện requests
import requests
import json
import os
import sys
import csv
checkpoint_dir = "checkpoint"
temp_checkpoint = ""
def init():
    if os.path.isdir(checkpoint_dir)==False:
        os.mkdir(checkpoint_dir)
def appendFieldCsv(field):
    with open(r'sample.csv', 'a', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
def getAllLinkFromFile(filepath):
    with open(filepath, 'r') as f:
        lines = f.read().splitlines() 
        return lines
    return []
def GetFieldInLink(URL):
    try:
        num_images = ''
        print("Crawl : "+URL)
        x = requests.get(url = URL)
        soup = BeautifulSoup(x.text,'html.parser')
        images = soup.find('a',{'class':"open-list-full-list-link"})
        if images == None:
            images_div = soup.findAll('div',{'class':"open-list-item open-list-block clearfix"})
            num_images = str(len(images_div))
        else:
            num_images = images.text.replace("images","")
            num_images = num_images.strip()
        votes = soup.find('footer',{'class':"footer post-shares-footer clearfix"})
        link_point = votes.find('div',{'class':"points"}).text.strip()
        list_image = soup.find('div',{'class':"open-list-item open-list-block clearfix"})
        first_img_point = list_image.find('div',{'class':"points"}).text.strip().replace('points','')
        print("Link Point : "+ link_point + "--" + "Images : "+ num_images + "--" +"FIP : "+ first_img_point)
        return [URL, link_point,num_images,first_img_point]
    except Exception as err:
        print("Failed : "+URL+" -- Erro : "+str(err))
        return False
def removeCheckpoint(checkpoint_file):
    try:
        os.remove(checkpoint_dir+"/"+ checkpoint_file)
    except:
        pass
def makeCheckpoint(checkpoint_file):
    try:
        with open(checkpoint_dir+"/"+ checkpoint_file,"w") as f:
            pass
    except:
        pass
def checkCheckpoint(checkpoint_file):
    return os.path.isfile(checkpoint_dir+"/"+ checkpoint_file)
def getAllLinkFromIndexPage(page):
    links = []
    try:
        x = requests.get("https://www.boredpanda.com/page/"+str(page))
        soup = BeautifulSoup(x.text,'html.parser')
        article = soup.findAll('article',{'class':"post"})
        if len(article)==0:
            return links
        for item in article:
            url = item.find('a')
            url = url['href']
            url = url.replace("https://www.boredpanda.com/","")
            url = re.sub(r'\/.*',"",url)
            links.append("https://www.boredpanda.com/"+url)
        return links
    except Exception as er:
        print(str(er))
        return links
if __name__=='__main__':
    init()
    mode = 1
    if mode == 1:
        page = 0
        run = True
        while run:
            links = getAllLinkFromIndexPage(page)
            for link in links:
                sub_name = link.replace('https://www.boredpanda.com/','')
                sub_name = sub_name.replace('-','_')
                if checkCheckpoint(sub_name)==False:
                    fields = GetFieldInLink(link)
                    # fields [URL, link_point,num_images,first_img_point]
                    if fields != False:
                        appendFieldCsv(fields)
                        makeCheckpoint(sub_name)
                else:
                    print("Checkpoint! End program")
                    exit()
            page += 1
    links = getAllLinkFromFile("data.txt")
    for link in links:
        sub_name = link.replace('https://www.boredpanda.com/','')
        sub_name = sub_name.replace('-','_')
        if checkCheckpoint(sub_name)==False:
            fields = GetFieldInLink(link)
            # fields [URL, link_point,num_images,first_img_point]
            if fields != False:
                appendFieldCsv(fields)
                makeCheckpoint(sub_name)
        else:
            print("Existed")