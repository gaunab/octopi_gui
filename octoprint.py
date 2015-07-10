#! /usr/bin/env python

# http://isbullsh.it/2012/06/Rest-api-in-python/#conclusion
import requests, json
import os.path

class Api():
    def __init__(self,url="localhost",api=None,apikeyfile=None):
        """ Create new Connection-Object to octoprint
        Params: - url (string)
                  Url of octoprint Server
                - api (string)
                  Apikey - if no apikey is given, apikeyfile is searched for
                - apikeyfile
        """
        self.url = url

        if api == None:
            if apikeyfile == None:
                try:
                    self.api = self.apikey()
                except:
                    self.api = ""
            else:
                self.api = self.apikey(apikeyfile)
        else:
            self.api = api


        self.headers ={'apikey': self.api, 'Content-Type':'application/json'}

    def apikey(self,filename='apikey'):
        """ Fetch APIKEY from File. If no Filename is given, ./apikey is used """
        f = open(filename)
        line = f.readline()
        f.close()
        return line.strip()

    def version(self):
        """ Return Version of Server """
        r = requests.get("http://%s/api/version" %(self.url), headers=self.headers)
        if r.status_code == 200:
            return True, r.content
        else:
            return False, {}

    def job(self):
        r = requests.get("http://%s/api/job" %(self.url), headers=self.headers)
        if r.status_code == 200:
            job = json.loads(r.content.decode())
            return True, job
        else:
            return False, {}
        
    def progress(self):
        """ Return Progress """ 
        r = requests.get("http://%s/api/job" %(self.url), headers=self.headers)
        if r.status_code == 200: 
            job = json.loads(r.content.decode())
            return True, job['progress']
        else:
            return False, {}

    def bedtemp(self):
        r = requests.get("http://%s/api/printer/bed" %(self.url), headers=self.headers)
        if r.status_code == 200:
            return True,json.loads(r.content.decode())
        else:
            return False, {}

    def tooltemp(self):
        r = requests.get("http://%s/api/printer/tool" %(self.url), headers=self.headers)
        if r.status_code == 200:
            return True, json.loads(r.content.decode())
        else:
            return False, {}
        
    def stop(self):
        """ Stop Current Job """
        payload = {'command':'cancel'}
        r = requests.post("http://%s/api/job" %(self.url), headers=self.headers,
                data=json.dumps(payload))
        if r.status_code == 204:
            return True
        else:
            return False

    def start(self):
        """ Start Current Job """
        payload = {'command':'cancel'}
        r = requests.post("http://%s/api/job" %(self.url), headers=self.headers,
                data=json.dumps(payload))
        if r.status_code == 204:
            return True
        else:
            return False


