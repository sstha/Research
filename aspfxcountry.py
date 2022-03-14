'''
Read prefix from main.py and identify geolocation of prefix from prefix_country and write to two different files.\
    allascn.csv has as to country mapping
    allpfxcn has prefix to country mapping.
'''

from main import bgpdata
import ipaddress
from prefix_country import prefix_country
import csv

asprefix,allas = bgpdata()
ip_id,id_cn=prefix_country()
pfx_id_cn = lambda c: id_cn.get(ip_id.get(c,'unknown'),'unknown')
prefix_cn=dict()
as_cn=dict()
fields=['nw','cn']
country='CL'

fo=open('allpfxcn.csv','a')
pfxwriter=csv.writer(fo)
fa=open('allascn.csv','a')
aswriter=csv.writer(fa)

print (allas)

with open('ixp_as.txt','r') as fo:
    x=[]
    fo_lines=fo.readlines()
    for line in fo_lines:
        a=line.strip()
        x.append(a)


for ases in allas:
    as_pfx_cn=[]
    as_cn={}
    print (ases)
    print("prefixes")

    if asprefix.get(ases) is not None :
        for prefix in asprefix[ases]:
            net=ipaddress.IPv4Network(prefix)
            octet=prefix.split(".")[0]
            last = net[-1]
            for network in ip_id.keys():
                if network.split(".")[0] == octet:
                    if (net.subnet_of(ipaddress.IPv4Network(network))) or net==ipaddress.IPv4Network(network) :
                        prefix_cn.update({prefix:pfx_id_cn(network)})
                        pfxwriter.writerow([prefix,pfx_id_cn(network)])
                        as_pfx_cn.append(pfx_id_cn(network))
                        break

    if ases in x:
        as_pfx_cn.append(country)
    #aswriter.writerows(as_pfx_cn)
    for allcn in set(as_pfx_cn):
        as_cn.setdefault(ases,[]).append(allcn)
    print(as_cn)
    for key,value in as_cn.items():
        aswriter.writerow([key,value])


fa.close()
fo.close()
    
