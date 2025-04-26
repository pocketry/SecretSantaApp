import smtplib, ssl
from email.message import EmailMessage
import getpass
from typing import List

import santaConfigs.config as config
from santa import Santa

def getBody(santa, exchange):
    p = {
        "name": santa.getName(),
        "givingTo": santa.getGifteeName(),
        "parentName": santa.getParent(),
        'wishList': santa.getGifteeWishList()
    }
    body = exchange['body'].substitute(p)
    return body

def sendEmails(secretSantas, exchangeInput):
    exchange = config.exchanges[exchangeInput]
    port = 465  # For SSL
    password = getpass.getpass("Type your password and press enter: ")

    msg = EmailMessage()

    msg['To'] = ''
    msg['Subject'] = exchange['subject']
    msg['From'] = config.email

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(config.email, password)
        for s in secretSantas:
            msg.replace_header('To', s.getEmail())
            body = getBody(s, exchange)
            msg.set_content(body)
            if exchange['consoleLog']:
                print('--------------------')
                print(body)
            else:
                server.send_message(msg)