from bottle import *
import json
import os
import sys
import mysql.connector

pagePort = 18155

mydb = mysql.connector.connect(
    host="localhost",
    user="student",
    passwd="fredfredburger",
    database="chickadees"

)
print("**mydb is: ",mydb)
print("**database: ", mydb.database)

@post('/api/visits')
def getJson():
    data = request.json
    payload = base64.b64decode(data['payload_raw'])
    #payloadTimestamp = data.metadata.gateways['timestamp']
    payloadTimestamp = data['metadata']['time']
    #payloadTimestamp = 'seven'
    dataParseTesting = data['metadata']
    '''
    # ** Testing Purposes **
    print("*** METADATA ***")
    print(dataParseTesting)
    print("*** END-METADATA ***")
    print("------------------------------------------")
    print("*** TIME ***")
    print(payloadTimestamp)
    print("*** END-TIME ***")
    print("------------------------------------------")
    print("*** DATA ***")
    print(data)     #print entire data packet. Including meta data
    print("*** END-DATA ***")
    print("------------------------------------------")
    '''
    
    print("**payload: ",payload)
    print("**Count: ",data['counter'])
    print("timestamp: ", payloadTimestamp)

    timestamp = (payload[10:20]).decode("utf-8")
    rfid = (payload[0:10]).decode("utf-8")
    print("*TIMESTAMP: ",timestamp)
    print("*RFID: ", rfid)

    insert_tuple = (rfid,timestamp)

    mycursor = mydb.cursor()

    #tmpInsert = " INSERT INTO visits (rfid, visitTimestamp) VALUES (" + rfid + " , " + timestamp + ") "
    tmpSearch = "Select * from visits where rfid = %s and visitTimestamp = %s"
    #sqlInsert = """ INSERT INTO visits (rfid, feederID, visitTimestamp, temperature, mass, bandCombo, isSynced) VALUES ('011016C1B6', 'SHRM', '%s', '24', '24', 'g0/Y#', '0')  """
    
    searchRes = mycursor.execute(tmpSearch,(rfid,int(timestamp)))
    rowCount = mycursor.fetchone()
    if not rowCount:
        tmpInsert = "INSERT INTO visits (rfid,feederID,visitTimestamp,temperature, mass, bandCombo, isSynced) VALUES (%s, 'CLIF', %s, 0, 0, '', 0)"
        insertRes = mycursor.execute(tmpInsert,(rfid,int(timestamp)))
        mydb.commit()  #uncomment to actually commit INSERT into DB.
        print("RowCount: ",rowCount)
    

    return data


run(host='euclid.nmu.edu', port=pagePort, debug=True)



"""
    ** Test Tags **
0700EDFC4A
011016A32F


    ** JSON data **
    
{
    'app_id': 'production2019jan', 
    'dev_id': 'node1', 
    'hardware_serial': '0099DF663BAB7B4B', 
    'port': 1, 
    'counter': 0, 
    'confirmed': True, 
    'is_retry': True, 
    'payload_raw': 'MDExMDE2QTMyRg==', 
    'metadata':{
                'time': '2019-03-20T00:45:16.959721306Z', 
                'frequency': 904.5, 
                'modulation': 'LORA', 
                'data_rate': 'SF10BW125', 
                'coding_rate': '4/5', 
                'gateways': [{
                            'gtw_id': 'eui-b827ebfffe11f166', 
                            'timestamp': 176353300,                 # NEED THIS VALUE!!
                            'time': '2019-03-20T00:45:16.926417Z',  # or this I guess...
                            'channel': 3, 
                            'rssi': -114, 
                            'snr': -15.2, 
                            'rf_chain': 0, 
                            'latitude': 46.54527, 
                            'longitude': -87.40362, 
                            'location_source': 'registry'
                    }]
        },
    'downlink_url': 'https://integrations.thethingsnetwork.org/ttn-us-west/api/v2/down/production2019jan/euclid?key=ttn-account-v2.qnXQCj7ir6DDJ7-YwbF5qbnRQTWB4CG1RcqvQOSsmKM'
}



{'app_id': 'production2019jan', 'dev_id': 'node1', 'hardware_serial': '0099DF663BAB7B4B', 'port': 1, 'counter': 0, 'confirmed': True, 'is_retry': True, 'payload_raw': 'MDExMDE2QTMyRg==', 'metadata': {'time': '2019-03-20T00:45:16.959721306Z', 'frequency': 904.5, 'modulation': 'LORA', 'data_rate': 'SF10BW125', 'coding_rate': '4/5', 'gateways': [{'gtw_id': 'eui-b827ebfffe11f166', 'timestamp': 176353300, 'time': '2019-03-20T00:45:16.926417Z', 'channel': 3, 'rssi': -114, 'snr': -15.2, 'rf_chain': 0, 'latitude': 46.54527, 'longitude': -87.40362, 'location_source': 'registry'}]}, 'downlink_url': 'https://integrations.thethingsnetwork.org/ttn-us-west/api/v2/down/production2019jan/euclid?key=ttn-account-v2.qnXQCj7ir6DDJ7-YwbF5qbnRQTWB4CG1RcqvQOSsmKM'}


"""
