'''
Map AS to organization id and AS to country. The file is obtained from CAIDA AS to organization dataset.\
    The dataset maps AS to country using the whois and RIR recond. but the dataset is obsolete and no longer maintained
    
'''

import json
from collections import defaultdict
from itertools import chain

file = "20211001.as-org2info.jsonl"
with open(file) as fp:
    data = fp.readlines()
"""
{Country, orgid, type=organization}
{asn, orgid, type=ASN}
"""
"""def get_asn_country_mappings():"""
"""
{
    "asn":"org_id"
},{
    "org_id": "country"
}
"""
orgid_country_map = {}
org_id_asn_map = {}
country={}
org_details_map={}
asn_to_orgname={}
orgid_to_orgname={}

def get_asn_country_mappings():
    for record in data:
        record = json.loads(record)
        type = record.get("type", None)
        if not type:
            continue
        elif type == "ASN":
            org_id_asn_map.update({record.get("asn", "default"): record.get("organizationId", "default")})
        elif type == "Organization":
            orgid_country_map.update({record.get("organizationId","default"): record.get("country", "default")})
            orgid_to_orgname.update({record.get("organizationId","default"): record.get("name", "default")})

    return org_id_asn_map,orgid_country_map,orgid_to_orgname

def country_asn_mapping():
    for key,value in orgid_country_map.items():
        country.setdefault(value,[]).append(org_id_asn_map[key])
    return country


def get_asn_groups():
    country_org_id_map = {}
    org_id_asn_map = {}
    for record in data:
        record = json.loads(record)
        type = record.get("type", None)
        if not type:
            continue
        elif type == "ASN":
            organization = record.get("organizationId", "default")
            asn_ids = org_id_asn_map.get(organization, [])
            asn_ids.append(record.get("asn", "default"))
            org_id_asn_map[organization] = asn_ids
        elif type == "Organization":
            country = record.get("country", "default")
            org_ids = country_org_id_map.get(country, [])
            org_ids.append(record.get("organizationId", "default"))
            country_org_id_map[country] = org_ids
    for key, value in country_org_id_map.items():
        country_org_id_map[key] = set(chain.from_iterable(list(map(org_id_asn_map.get, value))))
    return country_org_id_map

def org_details():
    as_org_name={}
    for key,value in org_details_map.items():
        as_org_name[key]=value
    return as_org_name




