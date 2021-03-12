import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import numpy as np
import datetime as dt
import pandas as pd

start_date = dt.datetime(2018,12,10)
end_date = dt.date.today()

def get_dates(start_date, end_date):
    """
    Returns all date which are not weekends
    """
    dates = [date for date in pd.date_range(start_date,end_date,freq='d') if date.isoweekday() not in (6,7) ]
    return dates

def url_date(date):
    """
    'url' for one date
    """
    url = 'https://www.bonjourmadame.fr/{}/{}/{}/'.format(date.year, date.strftime("%m"), date.strftime("%d"))
    return(url)

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images", disable = True):
        img_url = img.attrs.get("src")
        urls.append(img_url)
    return np.unique(urls)

def the_image(imgs):
    """
    Selects the good `url` ^^
    """
    for img in imgs:
        if img[-2:] != '=1':
            return img

def download(img, date):
    """
    Downloads image on a single `url` for one date
    """
    try:
        r = requests.get(img)
        with open(str(date.strftime("%Y%m%d")) + ".png", 'wb') as f:
            f.write(r.content) 
            f.close()
    except:
        print("{} failed, surely a video! you can check at:  ".format(date.strftime("%Y%m%d")) )
        print(url_date(date))
        
def main():     
    dates = get_dates(start_date, end_date)
    for date in dates:
        url = url_date(date)
        imgs = get_all_images(url)
        img = the_image(imgs)
        download(img, date)
    
if __name__ == "__main__":
    main()