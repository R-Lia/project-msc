"""
This code :
    1) Read the data from the big JSON file and add it the db 
    2) Move all the JSON files withna true flag to an already processed dir
"""

import time
import json
import os 
import tarfile
import shutil
import sqlite3
import extract

#PATH = "test/"
PATH = "/vol/bitbucket/aab621/eWater-uploads/"
PATH_STORE = "store_raw"
PATH_TAR= "ewaterJSON.tar"
PATH_MOVE = "/vol/bitbucket/aab621/eWater_processed/"
PATH_DATABASE="eWater.db"
 


def write_json():

    # Connect to the database
    conn = sqlite3.connect('eWater.db')
    cursor = conn.cursor()

    # Create the table sensor if it does not exist
    cursor.execute('''create table if not exists ewaterdata(
                WaterSystemId      INT,
                AssetId        INT, 
                EWC_ID            INT,
                ErrorEventCode   INT,
                ErrorEventDescripton      TEXT,
                Date     TEXT,
                Hours      TEXT,
                Timestamp      INT,
                CardId         INT,
                [BatteryVoltage(V)]     REAL,
                UsageCounter       INT,
                StartCreditValue   REAL,   
                EndCreditValue     REAL,
                Operation          TEXT,
                [Liters(l)]         REAL,
                [Flow(l/m)]           REAL,
                [FlowTime(s)]       REAL,
                RawPacket      TEXT,
                DateOfCreation  TEXT
                )''')

    
    # Create the directory where I will move the already processed JSON files
    if not os.path.exists(PATH_MOVE):
        os.mkdir(PATH_MOVE)

    # Open the big JSON file ads fi
    with open(PATH_STORE,'r+') as fi:

        # First we load existing data of the big JSON file into a dict.
        file_data = json.load(fi)
        
        listJSON = file_data["Transaction"]

        for i in range(len(listJSON)):
                       #### 3) STORE THE DATA IN A DATABASE
                        raw_packet = listJSON[i]["Packet"]
                        waterSystemId = listJSON[i]["WaterSystemId"]
                        assetId =  listJSON[i]["AssetId"]
                        EWC_Id = extract.extract_EWCID(raw_packet)
                        ErrorEventCode = extract.error_code(raw_packet)
                        ErrorEventDesc = extract.error_code_description(raw_packet)
                        (date,hour) = extract.date(raw_packet)
                        timestamp = extract.timestamp(raw_packet)
                        cardID = extract.card_ID(raw_packet)
                        battery = extract.voltage(raw_packet)
                        usage = extract.usage_counter(raw_packet)
                        startCredit = extract.start_credit_value(raw_packet)
                        endCredit = extract.end_credit_value(raw_packet)
                        operation = extract.what_operation(raw_packet)
                        liters = extract.liters(raw_packet)
                        flow = extract.flow(raw_packet)
                        flowtime = extract.flow_time(raw_packet)
                        dateArrival = "NO DATA"
                        records = [waterSystemId, assetId, EWC_Id, ErrorEventCode, ErrorEventDesc, date, hour, timestamp, cardID, battery, usage, startCredit,endCredit, operation, liters, flow, flowtime, raw_packet, dateArrival]
                    

                        cursor.execute('INSERT INTO ewaterdata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', records)

                    
      
        # Close the database
        conn.commit()
        conn.close()
        
        # Close the big JSON file and the tar archive
        fi.close()
        
    """
    #### 2) MOVE THE FILES ALREADY PROCESSED
    for files in os.listdir(PATH):
        with open(PATH+files,'r') as JSONFile:
            print(JSONFile)
            try : 
                new_data = json.load(JSONFile)
                if "flag" in new_data["Transaction"][0]:
                    shutil.move(PATH + files, PATH_MOVE)
            except :
                # The error I have is due to an extra "}" at the end so just delete it
                with open(PATH+files, 'rb+') as filehandle:
                    data = filehandle.readlines()
                    filehandle.seek(0)
                    filehandle.write(data[0])
                    filehandle.truncate()
    """         




write_json()

