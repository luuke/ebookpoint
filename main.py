import os
import sys
import requests
import winrt.windows.data.xml.dom as dom
import winrt.windows.ui.notifications as notifications
from bs4 import BeautifulSoup

def toast(img, price, link):
    # Open PowerShell and run 'get-StartApps' command
    # AppId = 'C:\\Users\\<USER>\\AppData\\Local\\Programs\\Python\\Python38-32\\python.exe'
    # or use Python path from variable
    AppId = sys.executable

    # Build image path from execution path and image file name
    imgPath = os.path.dirname(os.path.realpath(__file__)) + '\\' + img
    
    # Create notifier
    manager = notifications.ToastNotificationManager
    notifier = manager.create_toast_notifier(AppId)

    # Define your notification as string
    tString = """
    <toast>
        <visual>
        <binding template="ToastGeneric">
            <text hint-maxLines="1">Cena: """ + str(price) + """</text>
            <image src=" """ + imgPath + """" />
        </binding>
        </visual>
        <actions>
            <action arguments=" """ + link + """ " content="Open" activationType="protocol" />
        </actions>
    </toast>
    """

    # Convert notification to an XmlDocument
    xDoc = dom.XmlDocument()
    xDoc.load_xml(tString)

    # Display notification
    notifier.show(notifications.ToastNotification(xDoc))

ebook_url = "https://ebookpoint.pl/"
audio_url = "https://audiobooki.ebookpoint.pl/"

ebookPage = requests.get(ebook_url)
audioPage = requests.get(audio_url)

ebookSoup = BeautifulSoup(ebookPage.content, 'html.parser')
ebookPromotionSoup = ebookSoup.find_all("div", {"class": "promotion-book"})[0]
ebookImageUrl = ebookPromotionSoup.find("img")["src"]
ebookPrice = float(ebookPromotionSoup.find("strong").find("ins").get_text())/100
ebookLink = ebook_url[0:-1] + ebookPromotionSoup.find("a")["href"]

audioSoup = BeautifulSoup(audioPage.content, 'html.parser')
audioPromotionSoup = audioSoup.find_all("div", {"class": "promotion-book"})[0]
audioImageUrl = audioPromotionSoup.find("img")["src"]
audioPrice = float(audioPromotionSoup.find("strong").find("ins").get_text())/100
audioLink = audioPromotionSoup.find("a")["href"]

ebookImageData = requests.get(ebookImageUrl).content
with open('ebook.jpg', 'wb') as handler:
    handler.write(ebookImageData)

audioImageData = requests.get(audioImageUrl).content
with open('audio.jpg', 'wb') as handler:
    handler.write(audioImageData)

toast("ebook.jpg", ebookPrice, ebookLink)
toast("audio.jpg", audioPrice, audioLink)
