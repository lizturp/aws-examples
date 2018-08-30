#!/usr/bin/env python
import boto3
import argparse

# Available args:
#     Environment
#       -env                    dev, stage or prod
# 
# run the script from a command line like so:
# python download-creds.py -env=stage

# Purpose of this Snippet:
# An example of one way to pull credentials out of a secured s3 location at code execution time
# This method works locally and from within an application...
# Which helps users avoid accidentally committing their creds into repositories

# PRE REQ:  credentials file must located on S3 already 


parser = argparse.ArgumentParser()
parser.add_argument("-env", default='stage', help='environment to execute script against')
args = parser.parse_args()
env = args.env

def fetch_properties(s3file):
    s3Object = open(s3file, 'r')
    return {k: v.strip() for k, v in [tuple(line.split(':', 1)) for line in s3Object]}

bucket = 'BUCKET-NAME'
credentialsfilename = 'properties.txt'
credentialskey = "credentials-{environment}/application/adobe-api/properties.txt".format(environment=env)

# This is the same code as downloading a file example ... 
s3 = boto3.resource('s3')
s3.meta.client.download_file(bucket, credentialskey, credentialsfilename)

# This is an extra step that parses the credentials file and assigns the values to
# the config object so you can use it. 
config = fetch_properties(credentialsfilename)

print config["adobe_user"]
print config["adobe_secret"]
