# -*- coding: utf-8 -*-
"""
instagram scraper
Created on Mon Jul 23 15:08:10 2018

@author: fabia

"""
import requests, bs4, csv, time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import getcwd
import string
import random
import pyperclip
import time
print(''' INFORMATION:
    First pyperclip activates and will save everything that you will copy to your clip board.
    What you need are the instagram adresses of the pictures
    To immediately copy a link adress just right click an instagram picture in chrome and then press E.
    To stop pyperclip and run the rest of the programme run keyboard interrupt with CTRL-C'''
    )
print ('Choose account:')
print('account_name_1,account_name2')
choose_account = input('Enter now: ')

csv_file = open(choose_account + '.csv', 'w+', newline='', encoding='utf-8-sig')
csv_writer =csv.writer(csv_file)
if choose_account == 'account_name_1':
      tags = '''#example 1
example 2
example 3'''
if choose_account == 'account_name_2':
      tags = '''#example1
#example2
#example3
'''
        
#getting the picture urls in urls list
print('pyperclip activated', 'select posts to download by right-clicking them in chrome and then pressing \'E\' this copies the link to the post to your clipboard,
     'press CTRL-C to finish pyperclip and start downloading')
#%%
urls = []
pyperclip.copy('filler to delete')

try: 
    while True:
        time.sleep(0.4)
        text = pyperclip.paste()
        if text in urls:
            continue
        else:
            urls.append(text)
            print(text)
except KeyboardInterrupt:        
    del urls[0]
    urls = list(set(urls))
    with open('url_list.txt', 'w') as f:
    for item in urls:
        f.write("%s\n" % item)
    pass
print('pyperclip finished')

#%%
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

browser = webdriver.Chrome(chrome_options=chrome_options, executable_path= getcwd() + '\\chromedriver.exe')
print('starting browser')
counter =0
for url in urls:
    value_list =[]      
    url = url.strip('\r').strip('\n')
    browser.get(url)
    counter += 1
## add a loop here for the urls


    html_file= browser.page_source
    soup = bs4.BeautifulSoup(html_file, 'lxml')
    
    
    #get pic link, name, location        
    try:
        pic_link = soup.find('img', class_= 'FFVAD').get('srcset').split(',')[-1].rsplit(' ')[0]
    except AttributeError:
        continue
    name = soup.find('a', class_= 'FPmhX notranslate nJAzx').get('title')
    if name == 'discoversouthkorea':
        continue
    quote_list =['Tag us with @'+choose_account +' to be featured! Credits to @' + name, 'Submitted by @' + name + ' tag us on your pictures to be featured too.', 'Thank you for the picture @' + name + ' If you want to be featured tag us on your pictures', '@' +name + ' sent this one in. Thanks a lot. Tag us in your pictures of SK to be featured.', 'This submission is by @' + name +' tag us if you want to be featured too and have a wonderful day!', 'This one is from @' + name + ' thank you for submitting. If you want to get a chance to get featured tag us with @' + choose_account]
    try:
        location = soup.find('a', class_='O4GlU').getText()
        browser.get('http://www.google.com/search?q=' + location + '&hl=en&gl=us')
        html_file= browser.page_source
        soup = bs4.BeautifulSoup(html_file, 'lxml')
        wiki_text = soup.find(class_='kno-rdesc').next.next.getText()
        if 'Description' in wiki_text:
            wiki_text = ''
        quote = quote_list[random.randint(0,len(quote_list)-1)] + '\n\n' + wiki_text
    except:
        location = ''
        wiki_text = ''
        quote = quote_list[random.randint(0,len(quote_list)-1)]
        pass
    
    pic_file_name =  name + str(random.randint(1,100000)) + '.jpg'
    path = (r'C:\\Users\\Administrator\\Documents\\Follow Liker\\Share\\'+choose_account +r'\\' + pic_file_name )

    value_list.append(quote)
    value_list.append(tags)
    value_list.append(location)
    value_list.append(path)
    csv_writer.writerow(value_list)
    
    ##Download pic
    res=requests.get(pic_link)
    res.raise_for_status()
    picture = open(pic_file_name, 'wb')
    for chunk in res.iter_content(100000):
        picture.write(chunk)
    picture.close()
    print('successfully downloaded picture ' + str(counter) + ' of ' + str(len(urls)))

browser.close()
csv_file.close()
print('successfully printed csv file')



