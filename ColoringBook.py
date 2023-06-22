
from urllib.request import urlopen, Request, build_opener, install_opener, urlretrieve
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import bs4
import os
import cv2 as cv


def callUrl(req)-> bs4:
    try:
        return BeautifulSoup(urlopen(req).read(),'html.parser')
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)

def printPage(page):
    print(page.getText())

def printHtml(page):
    print(page)

def stripurl(url):
    url = url.replace('https://www.','')
    urlparts = url.split('.')
    return urlparts[0]

def writeHtml(page, url):
    url = stripurl(url)
    f = open(f'{url}page.html', "w")
    f.write(str(page))
    f.close()

def createFolder(name):
    if os.path.exists(name):
        return
    os.mkdir(name)

def getGoogleSearch(searchTerm):
    cleanedSearchTerm = cleanSearchTerm(searchTerm)
    url = f"https://www.google.com/search?q={cleanedSearchTerm}&tbm=isch"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    bs = callUrl(req)
    downloadImages(bs, searchTerm, searchTerm)

def cleanSearchTerm(term):
    term = term.strip()
    term = term.replace(" ","+")
    print(term)
    return term

def getImageLinks(bs):
    imageLinks = bs.find_all('img')
    return imageLinks

def downloadImages(bs, searchTerm,bookName):
    #bookTitle = bookTitle.replace(" ","")
    # Adding information about user agent
    opener=build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    install_opener(opener)

    # setting filename and image URL
    image_urls = getImageLinks(bs)
    imageLinks = filterImageLinks(image_urls)
    createFolder(bookName+" rawImages")
    createFolder(bookName)
    count = 0
    # calling urlretrieve function to get resource
    try:
        for x in imageLinks:
            filename = f'./{bookName} rawImages/{searchTerm}{count}.jpg'
            count = count+1
            urlretrieve(x.attrs.get('src'), filename)
            ConvertImageToEdges(filename,bookName,searchTerm,count)
        
    except Exception as e:
        print(e)
        print('Failed to get Image')

def filterImageLinks(links):
    validLinks = []
    for link in links:
        if 'http' in link.attrs.get('src'):
            validLinks.append(link)
    return validLinks

def ConvertImageToEdges(imagePath,bookName,searchterm, count):
    img = cv.imread(imagePath)
    grayImage = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    edgeImage = cv.Canny(grayImage, 250,300, 7)
    scale = 600

    width = int(grayImage.shape[1] *scale/100)
    height = int(grayImage.shape[0]*scale/100)
    dim = (width, height)
    resize = cv.resize(grayImage,dim,interpolation = cv.INTER_AREA)
    invert = cv.bitwise_not(resize)
    cv.imshow('Original',invert)
    cv.waitKey(0)
    cv.imwrite(f'./{bookName}/{searchterm}{count}.jpg', invert)
    pass

def test_best_low_high_canny(image):
    img = cv.imread(image)

    for  low in range(300,301,50):
        for high in range(250,501,50):
            edgeImage = cv.Canny(img,low,high,7)
            width = int(edgeImage.shape[1] *300/100)
            height = int(edgeImage.shape[0]*300/100)
            dim = (width, height)
            resize = cv.resize(edgeImage,dim,interpolation = cv.INTER_AREA)
            cv.imshow(f'low: {low},high: {high},apt: {7}',resize)
            cv.waitKey(0)

def main():
    try:
        getGoogleSearch("Cartoon Sheep ")
       #ConvertImageToEdges('.\mario adn Luigi rawImages\mario adn Luigi1.jpg')
    #    test_best_low_high_canny('Cartoon Space witch rawImages\Cartoon Space witch0.jpg')
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    except Exception as e:
        print(e)


if __name__=="__main__":
    main()




"""
image Search
https://www.google.com/search?q=baseball&tbm=isch

for multi word search swap space for +
"""