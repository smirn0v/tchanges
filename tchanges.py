#!/usr/bin/python

import sys, requests, json, subprocess

def main(teamcity,tuser,tpass,tbuildtype,jira,juser,jpass):
    try:
        headers = {'Accept' : 'application/json'}
        r = requests.get("%s/app/rest/buildTypes/id:%s/builds/status:SUCCESS"%(teamcity,tbuildtype),auth=(tuser,tpass),headers=headers)

        teamcity_response = json.loads(r.text)
        revision = teamcity_response["revisions"]["revision"][0]["version"]

        changes = subprocess.check_output("git log --pretty=format:'%%s' %s..HEAD"%revision,shell=True).split("\n")

        tasks = set([change[:change.find(":")] for change in changes if change.find(":")!=-1])

        for task in tasks:
            try:
                r = requests.get("%s/rest/api/latest/issue/%s"%(jira,task),auth=(juser,jpass),headers=headers)
                summary = json.loads(r.text)["fields"]["summary"]
                print ("%s: %s"%(task,summary)).encode('utf8')
            except: pass
    except:pass

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print "usage: %s <teamcity url> <user>:<pass> <build type> <jira url> <user>:<pass>"%sys.argv[0]
        sys.exit(1)
    main(sys.argv[1],               # teamcity url
         sys.argv[2].split(":")[0], # user
         sys.argv[2].split(":")[1], # pass
         sys.argv[3],               # build type
         sys.argv[4],               # jira url
         sys.argv[5].split(":")[0], # user
         sys.argv[5].split(":")[1]  # pass
        )
