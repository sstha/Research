1.Install python module pybgpstream

2.Run analysis.py to obtain paths that are not in the country and path with any of its AS geolocation unidentified.  
 -asn_country_mapping.py maps AS to organization id using the dataset from CAIDA 20211001.as-org2info.jsonl.   
 -prefix_country.py creates a dataset of MaxMind prefix to countrycode and country code to country name mapping.  
 -aspfxcountry.py maps Prefix to country and AS to country and writes to file allpfxcn.csv and allascn.csv respectively.  
    

3.The GeoLite2-Country-Blocks-IPv4.csv and GeoLite2-Country-Locations-en.csv are the databases obtained from MaxMind Lite for Prefix to Geolocation . ixp_as.txt contains the list of AS in the IXPs of a given country.

4.The 20211001.as-org2info.jsonl is obtained from CAIDA AS to organization dataset


