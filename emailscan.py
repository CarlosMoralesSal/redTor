import glob
import json
import shodan
import time
 
#shodan_client = shodan.Shodan("SxaULPrsq9QnWHCi70G66riC87JdQQCk")
 
file_list = glob.glob("onionscan_results/*.json")
 
email_list = []
email_to_mint = {}
for json_file in file_list:
 
    with open(json_file,"rb") as fd:
 
        scan_result = json.load(fd)
 
        if scan_result['identifierReport']['emailAddresses']:
            print("%s => %s" % (scan_result['hiddenService'],scan_result['identifierReport']['emailAddresses']))
            if tuple(scan_result['identifierReport']['emailAddresses']) in email_to_mint:
                email_to_mint[tuple(scan_result['identifierReport']['emailAddresses'])].append(scan_result['hiddenService'])
            else:
                email_to_mint[tuple(scan_result['identifierReport']['emailAddresses'])] = [scan_result['hiddenService']]

for address in email_to_mint:
    
    if len(email_to_mint[address]) > 1:
        
        print("\n[!] Email Address {0} is used on multiple hidden services." .format(address))
        
        for key in email_to_mint[address]:
            
            print("\t%s" % key)

