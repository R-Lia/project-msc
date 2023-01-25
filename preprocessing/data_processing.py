"""
This code :
    1) Append the JSON data of all the JSON files of a directory to a big JSON file
    2) Append the JSON files to a tar archive 
    3) Append human readable data to a SQLite database
    3) Move the JSON files 
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

    # Create the big JSON file to append the data of all the real time JSON files to it
    if not os.path.exists(PATH_STORE):
        f =  open(PATH_STORE,'w+') 
        data_dict = { "Transaction" : [] }
        json.dump(data_dict, f)
        f.close()
    
    # Create the directory where I will move the already processed JSON files
    if not os.path.exists(PATH_MOVE):
        os.mkdir(PATH_MOVE)

    # Open the tar archive 
    file_tar= tarfile.open(PATH_TAR,"w")

    # Open the big JSON file ads fi
    with open(PATH_STORE,'r+') as fi:

        # First we load existing data of the big JSON file into a dict.
        file_data = json.load(fi)

        # Browse all the files in the directory where ewater sends the data
        for files in os.listdir(PATH):
            

            # Open each of these little JSON file 
            with open(PATH + files,'r+') as jsonFile: 
                
                # Try to load the little JSON files (raise an error if there are malformatted)
                try:
                    new_data = json.load(jsonFile)
                    

                    #### 1) ADD DATA TO THE BIG JSON FILE
                    # Add new_data (little JSON files) to the big JSON 
                    file_data["Transaction"].append(new_data["Transaction"][0])

                    # Put the cursor at the beginning of the big JSON file to rewrite it
                    fi.seek(0)

                    # Put the data back into the big JSON file with the data added before
                    json.dump(file_data, fi, indent = 4)

                    #### 2) ADD DATA TO THE TAR ARCHIVE
                    # Add the little json file with the flag to the tar archive
                    file_tar.add(os.path.join(PATH, files))

                    #### 3) STORE THE DATA IN A DATABASE
                    raw_packet = new_data["Transaction"][0]["Packet"]
                    waterSystemId = new_data["Transaction"][0]["WaterSystemId"]
                    assetId =  new_data["Transaction"][0]["AssetId"]
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
                    dateArrival = time.ctime(os.path.getctime(PATH + files))
                    records = [waterSystemId, assetId, EWC_Id, ErrorEventCode, ErrorEventDesc, date, hour, timestamp, cardID, battery, usage, startCredit,endCredit, operation, liters, flow, flowtime, raw_packet, dateArrival]
                

                    cursor.execute('INSERT INTO ewaterdata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', records)

                    #### 4) MOVE THE LITTLE JSON FILES TO AN ALREADY PROCESSED DIRECTORY
                    try :
                        shutil.move(PATH + files, PATH_MOVE)
                    except :
                        time_store = str(time.time())
                        shutil.move(PATH + files, PATH_MOVE+time_store)

                    
                # Useful when debugging for malformatted JSON
                except ValueError as err:
                    # The error I have is due to an extra "}" at the end so just delete it
                    with open(PATH+files, 'rb+') as filehandle:
                        data = filehandle.readlines()
                        filehandle.seek(0)
                        filehandle.write(data[0])
                        filehandle.truncate()

                    """ 
                    with open(PATH+files, "r") as f:

                        # read data line by line
                        data = f.readlines()
                        #print(data)

                    # open file in write mode
                    with open(PATH+files, "w") as f:
                        isflag =False
                        counter = 0

                        for line in data :
                            if "flag" in line:
                                isflag = True
                            f.write(line)
                            counter +=1
                            if not isflag and counter == 7:
                                break
                            if isflag and counter == 8:
                                break
                        #if isflag:
                        f.write("]"+ "\n")
                        f.write("}")
                    """

                    #print(files,"corrected")


        # Close the database
        conn.commit()
        conn.close()
        
        # Close the big JSON file and the tar archive
        fi.close()
        file_tar.close()
        #print("The end")

start=time.time()
write_json()
end=time.time()
print("Execution time :",end-start)

