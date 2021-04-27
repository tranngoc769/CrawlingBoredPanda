from bs4 import BeautifulSoup
import re
import requests
import json
import os
import sys
import csv
import logging
from configparser import ConfigParser
# Global Variable
config_object = ConfigParser()
checkpoint_dir = "checkpoint"
excel_name = "data.csv"
txt_name = "data.txt"
log_path = "erro.log"
mode = 1
logger = None
# 
# Get all config variable
def init():
    global checkpoint_dir,txt_name,txt_name,log_path,mode,excel_name, logger
    config = None
    try:
        config_object.read("config.ini")
        config = config_object["APPLICATION_CONFIG"]
    except Exception as err:
        print("Cannot read config.ini")
    try:
        log_path = config["log_file"]
    except Exception as err:
        print("Cannot init log path: ",str(err))
    try:
        logging.basicConfig(filename=log_path, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logger = logging.getLogger(__name__)
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_path)
        c_handler.setLevel(logging.WARNING)
        f_handler.setLevel(logging.ERROR)
        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)
        # Add handlers to the logger
        if (logger.hasHandlers()):
            logger.handlers.clear()
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        logger.propagate = False
    except Exception as err:
        print("Cannot init logging: ",str(err))
    if config == None:
        return
    try:
        excel_name = config["excel_name"]
    except Exception as err:
        logger.error("Cannot read excel_name, using default: %s", excel_name)
    try:
        txt_name = config["txt_name"]
    except Exception as err:
        logger.error("Cannot read txt_name, using default: %s", txt_name)
    try:
        checkpoint_dir = config["checkpoint_dir"]
    except Exception as err:
        logger.error("Cannot read checkpoint_dir, using default: %s", checkpoint_dir)
    try:
        mode = config["mode"]
    except Exception as err:
        logger.error("Cannot read mode, using default: %s", mode)
    if os.path.isdir(checkpoint_dir)==False:
        os.mkdir(checkpoint_dir)
def appendFieldCsv(field):
    global excel_name
    with open(excel_name, 'a', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
def getAllLinkFromFile():
    global txt_name
    with open(txt_name, 'r') as f:
        lines = f.read().splitlines() 
        return lines
    return []
def GetFieldInLink(URL):
    global logger
    try:
        num_images = ''
        logger.warning("Crawl: %s",URL)
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
        logger.warning("Point: "+ link_point + "," + "Images: "+ num_images + "," +"FIP: "+ first_img_point)
        return [URL, link_point,num_images,first_img_point]
    except Exception as err:
        logger.warning("Failed: "+URL+",Erro: "+str(err))
        return False
def removeCheckpoint(checkpoint_file):
    global checkpoint_dir
    try:
        os.remove(checkpoint_dir+"/"+ checkpoint_file)
    except:
        pass
def makeCheckpoint(checkpoint_file):
    global checkpoint_dir
    try:
        with open(checkpoint_dir+"/"+ checkpoint_file,"w") as f:
            pass
    except:
        pass
def checkCheckpoint(checkpoint_file):
    global checkpoint_dir
    return os.path.isfile(checkpoint_dir+"/"+ checkpoint_file)
def getAllLinkFromIndexPage(page):
    global logger
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
        logger.error(str(er))
        return links
if __name__=='__main__':
    init()
    if mode == 1  or mode == '1':
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
                    logger.warning("React to checkpoint! End program")
                    exit()
            page += 1
    links = getAllLinkFromFile()
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
            logger.warning("React to checkpoint! End program")
            exit()