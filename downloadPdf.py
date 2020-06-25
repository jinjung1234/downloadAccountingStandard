# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 10:34:20 2020

@author: YongYong
"""


import requests, bs4, os
res = requests.get('http://www.kasb.or.kr/fe/accstd/NR_list.do?sortCd=G-COMPANY')
res.raise_for_status()
page_source = bs4.BeautifulSoup(res.text,'html.parser')
num = 1
while True:
    try:
        download_elems = page_source.select(f'#content > div.content-bg-top > div > section > div.content-board02 > table > tbody > tr:nth-child({num}) > td.board02-download > a.pdf')
        name_elems = page_source.select(f'#content > div.content-bg-top > div > section > div.content-board02 > table > tbody > tr:nth-child({num}) > td.board02-content > a')
        pdf_url = 'http://www.kasb.or.kr/' + download_elems[0].get('href')
        pdf_name = name_elems[0].contents[0].strip().replace(':','-')
        pdf = requests.get(pdf_url)
        pdf.raise_for_status()
        try:
            folder = '일반기업회계기준'
            os.mkdir(folder)
        except:
            pass
        pdf_file = open(os.path.join(os.getcwd(),folder,f'{pdf_name}.pdf'),'wb')
        for chunk in pdf.iter_content(100000):
            pdf_file.write(chunk)
        pdf_file.close()
        num += 1
    except:
        break