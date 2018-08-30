#!/usr/bin/env python
import boto3
import argparse

# Available args:
#     Environment
#       -env                    dev, stage or prod
# 
# run the script from a command line like so:
# python upload.py -env=stage

# The environment parameter allows you to run the script for stage vs. prod
# This way, you can test changes to your process without messing up what you already have scheduled

# Purpose of this snippet:
# To show how to upload data files that will be mapped to a Hive table
# Comments show some important questions to consider when making location decisions in the script
# Naming is specific to the infrastructure that my current user base is working on, but works anywhere


parser = argparse.ArgumentParser()
parser.add_argument("-env", default='stage', help='environment to execute script against')
args = parser.parse_args()
env = args.env

if env == "prod" :
  schemaname="product"
else :
  schemaname="product_stage"  

# UPLOAD A FILE THAT IS MAPPED TO A HIVE TABLE
# See create-example-table.sql file

# SET LOCATION FOR FINAL DESTINATION
bucket = 'BUCKET-NAME'
resultsfilename = 'results.csv'

# DO YOU WANT TO ADD IN ANY PARTITIONS FOR RSID ?
# WILL THIS DATA BE HISTORICAL, OR OVERWRITTEN EVERY DAY?
resultstablekey = "defloc/warehouse/{schema}.db/adobe_api_sas_ex/{file}".format(schema=schemaname, file=resultsfilename)

# This uploads the file to the location that is mapped to the HIVE table named "adobe_api_sas_ex"
s3 = boto3.client('s3')
s3.upload_file(resultsfilename, bucket, resultstablekey, ExtraArgs={'ServerSideEncryption': 'AES256'})

# If the table is NOT partitioned, anytime you upload a new file to this location, the table will immediately
# show the new data when queried in Hive.  No additional steps are required for unpartitioned tables...
# data does not need to be "loaded into the table" - once a table is mapped to a location, you are done.
