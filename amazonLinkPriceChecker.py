import requests
from bs4 import BeautifulSoup
import smtplib
import time
import sys

# You need to provide each one of these arguments when calling this script

price_target = sys.argv[1]
email = sys.argv[2]
secret = sys.argv[3]
to_email = sys.argv[4]
URL = sys.argv[5]

# This should be your user agent
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    price_element = soup.find(id="priceblock_ourprice")

    if(price_element):
        price = price_element.get_text()
        converted_price = float(price[0:5])

        if(converted_price < float(price_target)):
            send_email()
    else:
        print('No price has been found.')
        quit()

def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, secret)

    subject = 'Price fell down'
    body = f"Check the amazon link {URL}"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        email,
        to_email,
        msg
    )

    print('Email has been sent successfully!')

    server.quit()

while(True):
    check_price()
    time.sleep(3600)

