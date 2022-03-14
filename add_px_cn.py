import ipaddress
import csv
from attr import fields 
from main import bgpdata
from prefix_country import prefix_country

all_pfx=bgpdata()

ip_id,id_cn=prefix_country()
pfx_id_cn = lambda c: id_cn.get(ip_id.get(c,'unknown'),'unknown')
fields=['network','country_iso_code']
dest_pfx_cn=dict()

for origin,prefixes in all_pfx.items():
    for dest_pfx in prefixes:
        print(dest_pfx)
        net=ipaddress.IPv4Network(dest_pfx)
        first=dest_pfx.split(".")
        octet=first[0]
        last = net[-1]
        for network in ip_id.keys():
            if network.split(".")[0] == octet:
                if (net.subnet_of(ipaddress.IPv4Network(network))):
                    dest_pfx_cn.update({dest_pfx:pfx_id_cn(network)})
                    print (dest_pfx_cn)
                    break
                # else:
                #     dest_pfx_cn.update({dest_pfx:pfx_id_cn(dest_pfx)})
           

with open('name.csv','w') as fo:
    csvwriter=csv.writer(fo)
    csvwriter.writerow(fields)
    for nw,cn in dest_pfx_cn.items():
        csvwriter.writerow([nw,cn])
