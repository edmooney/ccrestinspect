#!/usr/bin/env python

import os
from lxml import etree
import lxml.html as lh
import sqlite3
import datetime

a_full = [] 
a_full_clean = [] 
a_add_only = []
a_phone_only = []
a_inspect_date = []
a_inspect_date_clean = []
a_inspect_type = []
a_currstate = []
a_violations = []


def get_a_full():
  full = chtml.xpath("//table[@id='MainContent_gvInspections']//tr[@nonformattednameaddress]/td[1]");
  for f in full:
    if len(f.text_content())>10: #sometimes the date ends up in there - clean
      print f.text_content()
      a_full.append(f.text_content().strip())
      #print f.text_content()
  print a_full
  print 'len: '+str(len(a_full))


def get_add_only():
  full = chtml.xpath("//table[@id='MainContent_gvInspections']//tr[@nonformattednameaddress]/td[1]/div[1][text()!='']");
  for f in full:
    print f.text_content()
    a_add_only.append(f.text_content().strip())
  print a_add_only
  print 'len: '+str(len(a_add_only))

def get_phone_only():
  full = chtml.xpath("//table[@id='MainContent_gvInspections']//tr[@nonformattednameaddress]/td[1]/div[2][text()!='']");
  for f in full:
    print f.text_content()
    a_phone_only.append(f.text_content().strip())
  print a_phone_only
  print 'len: '+str(len(a_phone_only))


def get_inspect_date():
  full = chtml.xpath("//table[@id='MainContent_gvInspections']//tr/td[2]/text()");
  for f in full:
    f = f.strip()
    if f is not None and '/' in f:
      print f
      a_inspect_date.append(f)
  print a_inspect_date
  print 'len: '+str(len(a_inspect_date))

def get_inspect_type():
  full = chtml.xpath("//table[@id='MainContent_gvInspections']//tr/td[3]");
  for f in full:
    f = f.text_content().strip();
    if len(f)>4:
      print f
      a_inspect_type.append(f.strip())
  print a_inspect_type
  print 'len: '+str(len(a_inspect_type))


def get_currstate():
  full = chtml.xpath("//table[@id='MainContent_gvInspections']//tr/td[4]/b/text()");
  for f in full:
    f = f.strip()
    if f !='':
      print f
      a_currstate.append(f)
  print a_currstate
  print 'len: '+str(len(a_currstate))

def get_violations():
  full = chtml.xpath("//table[@id='MainContent_gvInspections']//tr/td[6]/a/text()");
  for f in full:
      f = f.replace('Violation(s)','')
      f = f.strip()
      print f
      a_violations.append(f)
  print a_violations
  print 'len: '+str(len(a_violations))

fdir = os.listdir(".")
fdir.sort()
for files in fdir:

  if files.endswith('.htm'):
    with open(files,'r') as r:
      read_data= r.read()

    read_data = unicode(read_data,errors='ignore');

    chtml = lh.fromstring(read_data)
    get_a_full()
    get_add_only()
    get_phone_only()
    get_inspect_date()
    get_inspect_type()
    get_currstate()
    get_violations()

    #convert the dates to sqliteformat YYYY-MM-DD
    #for d in a_inspect_date:
 
    for i in range(len(a_inspect_date)):
      d_arr = a_inspect_date[i].split('/')
      nd_arr = [d_arr[2],d_arr[0],d_arr[1]]
      nd = '-'.join(nd_arr)
      a_inspect_date_clean.append(nd)

#prep work/clean up

for i in range(len(a_full)):
# remove the phone num
# remove the address... what we have left should be the name
  f = a_full[i].replace(a_phone_only[i],'').replace(a_add_only[i],'')
  a_full_clean.append(f)


# create the sqlitedb
conn = sqlite3.connect('inspect.sqlite3')

c = conn.cursor()
#conn.commit()

c.execute(''' DROP TABLE IF EXISTS 'locations';''')
c.execute('''
CREATE TABLE 'locations' (
  'id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
  'rname' TEXT,
  'rphone' TEXT,
  'raddress' TEXT,
  'inspectdate' DATETIME,
  'inspecttype' TEXT,
  'currstate' TEXT,
  'violationscnt' INTEGER,
  'lat' TEXT,
  'long' TEXT,
  'lastupdated' TIMESTAMP
);''')
conn.commit()

#Let's Roll
t = datetime.datetime.now()
lud = t.strftime("%Y-%m-%d")
for i in range(len(a_full_clean)):
  c.execute("INSERT INTO LOCATIONS (rname,rphone,raddress,inspectdate,inspecttype,currstate,violationscnt,lastupdated) VALUES (?,?,?,?,?,?,?,?)",(a_full_clean[i],a_phone_only[i],a_add_only[i],a_inspect_date_clean[i],a_inspect_type[i],a_currstate[i],a_violations[i],lud))

conn.commit()
conn.close()
