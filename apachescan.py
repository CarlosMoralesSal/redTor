import glob
import json
import shodan
import time
 
#shodan_client = shodan.Shodan("SxaULPrsq9QnWHCi70G66riC87JdQQCk")
 
file_list = glob.glob("onionscan_results/*.json")
 
bitcoin_list = []
bitcoin_to_mint = {}
for json_file in file_list:
 
    with open(json_file,"rb") as fd:
 
        scan_result = json.load(fd)
 
        if scan_result['identifierReport']['foundApacheModStatus']:
            print("%s => %s" % (scan_result['hiddenService'],scan_result['identifierReport']['foundApacheModStatus']))
            #if tuple(scan_result['identifierReport']['bitcoinAddresses']) in bitcoin_to_mint:
            #    bitcoin_to_mint[tuple(scan_result['identifierReport']['bitcoinAddresses'])].append(scan_result['hiddenService'])
            #else:
            #    bitcoin_to_mint[tuple(scan_result['identifierReport']['bitcoinAddresses'])] = [scan_result['hiddenService']]

#for address in bitcoin_to_mint:
    
#    if len(bitcoin_to_mint[address]) > 1:
        
#        print("\n[!] Bitcoin Address {0} is used on multiple hidden services." .format(address))
        
#        for key in bitcoin_to_mint[address]:
            
#            print("\t%s" % key)

    #while True:
    
    #    try:
            
    #        shodan_result = shodan_client.search(ssh_key)
    #        break
    #    except:
    #        time.sleep(5)
    #        pass
        
   # if shodan_result['total'] > 0:
        
    #    for hit in shodan_result['matches']:
    #        print("[!] Hit for %s on %s for hidden services %s" % (ssh_key,hit['ip_str'],",".join(key_to_hosts[ssh_key])))
