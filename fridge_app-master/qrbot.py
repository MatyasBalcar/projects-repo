
import cherrypy
import urllib
import requests
import csv
import datetime
import uuid
import time

scans = []
codes=[]
result=[]

exeptions_dict={
  "4008400280127": "Cokobonbony",
  "5997255703280": "Multi vitaminy",
  "5997255703754": "Magnesium Vitaminy B6"
}

#lookup token 
class Scans:
        
  exposed = True
        
  def GET(self):

    with open('scans.txt', 'r')as file:
       items=file.readlines()

    with open('scans.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        
        next(csvreader)
        
        for row in csvreader:
          code, data,open_, exp,id_=row
          codes.append(code)
    return codes
        
  def POST(self, **kwargs):

    cherrypy.response.headers['Custom-Time'] = '5000'
        
    content = "unknown content"
    format = "unknown format"
        
    if "content" in kwargs:
        content = kwargs["content"]
    if "format" in kwargs:
        format = kwargs["format"]
        
    response_final=""
    if str(content) in exeptions_dict:
      response_final = exeptions_dict[content]

    url = f"https://world.openfoodfacts.org/api/v2/product/{content}.json"
    response = requests.get(url)
    response_json = response.json()
    print(response_json["status"])
    if response_json["status"]==0:
      response_final = "no name found"
      with open('errors.txt','a') as error:
        error.write(content+"\n")

    if response_final=="" and "product_name" in response_json["product"] :
      response_final = response_json["product"]["product_name"]
    if response_final=="":
      response_final = "no name found"
      with open('errors.txt','a') as error:
        error.write(content+"\n")


    with open('scans.txt','a') as file:
      file.write(response_final+"\n")
    with open('scans.csv', 'a', newline='') as csvfile:
      # Create a CSV writer object
      csvwriter = csv.writer(csvfile)
      
      # Write a new line to the CSV file
      unique_id = uuid.uuid4()
      csvwriter.writerow([response_final, datetime.datetime.now().date().strftime("%Y-%m-%d "),"Ne","Zadne", unique_id])
    return ('Append new scan with content: %s, format %s' % (content, format))
        
if __name__ == '__main__':
        
  conf = {
  'global': {
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080
  },
  '/': {
    'request.dispatch': cherrypy.dispatch.MethodDispatcher()
  }
  }
        
  cherrypy.quickstart(Scans(), '/scans/', conf)