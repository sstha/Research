'''
Maxmind dataset has two file
GeoLite2-Country-Blocks-IPv4.csv containg {ip_prefix:country_code}
GeoLite2-Country-Locations-en.csv {country_code:country_id}

The file reads the csv file and make a dataset of only required components.
'''

import csv
import ipaddress


ip_result={}
country_result={}
pfx_country={}
subnets=dict()


id_reader = csv.DictReader(open('GeoLite2-Country-Blocks-IPv4.csv'))
country_reader=csv.DictReader(open('GeoLite2-Country-Locations-en.csv'))

def prefix_country():
    for row in id_reader:
        ip_result[row['network']] = row['geoname_id']
    for row in country_reader:
        country_result[row['geoname_id']] = row ['country_iso_code']
    return ip_result,country_reader
