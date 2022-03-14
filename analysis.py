'''Obtain path not in country and unkown as for analysis from main.py'''

#from obtain_path import asn_not_country
from main import bgpdata,asn_not_country

pfx_origin,all_as = bgpdata()
not_in_cn,unknown_as,asn_analysis=asn_not_country()
country_result={}
dest_asn=[]

print("\nPath with AS not in country\n ")
for aspath,paths in not_in_cn.items():
    dest_asn.append(aspath[-1])
    print (aspath,"-",paths)
   
print("\nDestination AS of Path for Analysis for validation\n")
for ases in set(dest_asn):
    print("Destination AS numnber:",ases)
    print(pfx_origin.get(ases))

print("Path with unknown AS")
for key,values in unknown_as.items():
    print (key,"-",values)




