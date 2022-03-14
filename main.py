import pybgpstream
import itertools 
import collections 
from collections import defaultdict
from asn_country_mapping import get_asn_groups
from asn_country_mapping import get_asn_country_mappings,org_details
from allascn_read import asndict
from json import loads
from ast import literal_eval



prefix_origin={}
country_nodes=[]
asn_country_dict={}
asn_test=[]
bgp_lens = defaultdict(lambda: defaultdict(lambda: None))
path_for_analysis=[]
fullpath=[]
path_set=[]
#Set the country for observation
main_cn='CL'                    

asn_mapping, country_mapping,orgid_name= get_asn_country_mappings()
#get_country = lambda x: country_mapping.get(asn_mapping.get(x, x), x)

#asn_cn_map=as_country_map()
asn_cn_map=asndict()
get_country=lambda c:(asn_cn_map.get(c,'["unknown"]'))



###Map ASNs in a list to country ['27678','27986','12956','13335'] ['CL','CL','US','CL']

def asn_to_country(path_to_map):
    country_path=[]
    for a in path_to_map:
        country=literal_eval(get_country(a))
        country_path.append(country)    
    return (country_path)



def bgpdata():
    global thisdict
    global anotherdict

    ###{thisdict:[path_combination]:[path]} and anotherdict:{[pathcombination]:[country]
    thisdict={}                             
    anotherdict={}                         
    
    stream = pybgpstream.BGPStream(
            from_time="2021-10-10 00:00:00", until_time="2021-10-10 00:10:00 UTC",
            collectors=["route-views.chile"],
            record_type="ribs",
        )

    '''
    27678 27986 12956 13335 
    27678 14259 3356 4826 38803 
    27678 27986 12956 4637 7670 18144 
    27678 27986 6762 38040 23969 
    '''
    ###go through each path, create all combination as key and nodes between those combination as values
    '''
    (27678,27986):[27678,27986];(27678,12956):[27678,27986,12956];(27678,13335):[27678,27986,12956,13335],(27986,12956):[27986,12956]\
        (27986,13335):[27986,12956,13335],(12956,13335):[12956,13335]
    '''
    ###for next path if pair already exists; add values to the existing key

    ###create dictionaries 

    for rec in stream.records():
        for elem in rec:
            path=elem.fields["as-path"].split()    
            for items in path:
                path_set.append(items)           #set of all AS in the dataset

            prefix=elem.fields["prefix"]
            origin=path[-1]
            prefix_origin.setdefault(origin,[]).append(prefix)          #{originAS:prefix_announced}
            peer=elem.peer_asn
            if '{' in origin:                                            #some aspath format is not consistent ignoring them now.27678 27986 6762 20485 49973 49973 49973 49973 49973 49973 {48282,212441}
                continue
            
            #Contains full path only
            bgp_lens[peer].setdefault(int(origin),[]).append(path)

            x=set(itertools.combinations(path,2)) 

            for node_pair in x:
                node_path=[]
                a=path.index(node_pair[0])
                b=path.index(node_pair[1])
                for i in range(a,b+1):
                    node_path.append(path[i])
                thisdict.setdefault(node_pair,[]).append(node_path)                                     #creates a dictionary to get nodes pair and corresponding path
                anotherdict.update({node_pair:[get_country(node_pair[0]),get_country(node_pair[1])]})       
    
    return prefix_origin,set(path_set)



def asn_not_country():
    ###get list of  path combination in selected country to obtain pat

    in_country={}
    not_in_country={}
    unknown_as={}

    #check country of node pair combination and select only pair with both soure and destination in Chile

    for key,values in anotherdict.items():
        if (values[0]==values[1] and values[0]== "['CL']"):
            country_nodes.append(key)                           #List of all Nodes that are in the same country

               
    ###Obtain path for the selected nodes and their country;create dictionary path to country
    ###Dict{as_path}:{country}
    for nodes in country_nodes:
        for asn_path in thisdict[nodes]:
        #asn_path=thisdict[nodes]
            country_asn=asn_to_country(asn_path)
            asn_country_dict.update({tuple(asn_path):country_asn})  

    ###Obtain only path that has other country than selected country in the path
    for key,values in asn_country_dict.items():
        if all(country == 'CL' for country in list(itertools.chain(*values[1:-1]))):
            in_country.update({key:values})
            continue
        for cn in values[1:-1]:
            if all(country != 'CL' and  country!='unknown' for country in cn):
                not_in_country.update({key:values})
                break
            if any(country=='unknown' for country in cn):
                unknown_as.update({key:values})
    ###List asn that do not have prefix in CL

    ###Obtain the AS that is not in the country
    for keys in not_in_country.keys():
        for asn in keys:
            if (main_cn not in literal_eval(get_country(asn))):
                asn_test.append(asn)   
   
    return not_in_country,unknown_as,set(asn_test)
