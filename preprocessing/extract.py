from EE import EE
import time

def extract_EWCID(packet_string,dec=True):
    '''
    Extract the EWC identifier in decimal format (or hex) 

            Parameters:
                    packet_string (string) : the 39 bytes hex string
                    dec (bool) : if True the returns the decimal value otherwise the hex one

            Returns:
                    (int or string) : the EWC identifier
    '''
    EWC_id = packet_string[2:10]
    
    if dec:
        return(int(EWC_id,16))

    else :
        return(packet_string[2:10])


def error_code(packet_string):
    '''
    Returns the error code

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    error_code (string) : error code in hex

    '''
    return(packet_string[10:12])



def error_code_description(packet_string):
    '''
    Returns the description of the error code

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    description (string) : description found in EE

    '''

    return(EE[packet_string[10:12]])





def date(packet_string):
    '''
    Returns the date 

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    date (string) : DD/MM/YYYY
                    hours (string) : HH:MM:SS

    '''
    day = packet_string[18:20] +"/" + packet_string[20:22] + "/" + packet_string[22:24] 
    hours = packet_string[16:18]+":"+packet_string[14:16]+":"+packet_string[12:14]
    return (day, hours)

def timestamp(packet_string):
    '''
    Returns a UNIX timestamp

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    UNIX timestamp

    '''
    day,hour = date(packet_string)

    try : 
        return time.mktime(time.strptime('{} {}'.format(day, hour), '%d/%m/%y %H:%M:%S'))
    # Happens when the date and time are not valid (receive a packet dated with weird seconds in hexadecimal)
    except:
        return 0

def card_ID(packet_string):
    '''
    Returns the card identifier

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    card_id (string) : card ID in hexadecimal
    '''
    return(packet_string[24:32])


def voltage(packet_string): 
    '''
    Returns the battery voltage 

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                   battery voltage (int) : ADC / 256 * 15 in Volts 
    '''
    ADC = int(packet_string[32:34],16)
    return (ADC/256 * 15)


def usage_counter(packet_string):
    '''
    Returns the usage counter

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    usage counter (int) :
    '''
    return(int(packet_string[36:40],16))



def start_credit_value(packet_string):
    '''
    Returns the start credit value

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    start credit value (int) :
    '''
    return(int(packet_string[40:48],16))



def end_credit_value(packet_string):
    '''
    Returns the end credit value

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    end credit value (int) :
    '''
    return(int(packet_string[48:56],16))


def what_operation(packet_string):
    '''
    Returns the type of operation : - a top up (charging), - a top down (getting water)

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    (string) : Top up, Getting water or Other
    '''
    if (start_credit_value(packet_string) > end_credit_value(packet_string) and card_ID(packet_string)!=0):
        return "Getting water"
    elif error_code(packet_string)=="14":
        return "Top up"
    else:
        return "Other"


def liters(packet_string):
    '''
    Returns the number of liters delivered 

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    (int) : number of liters
    '''
    return(int(packet_string[56:62],16)/360)

def flow_meter_count(packet_string):
    '''
    Returns the flow meter count 

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    (int) : flow volume 
    '''
    return(int(packet_string[56:62],16))


def flow_time(packet_string):
    '''
    Returns the flow time

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    (int) : flow time in seconds 
    '''
    return(int(packet_string[62:66],16))


def flow(packet_string):
    '''
    Returns the flow in liter/sec

    Parameter : 
                    packet_string (string) : the 39 bytes hex string

    Returns :
                    (int) : flow (l/m) 
    '''
    if flow_time(packet_string) > 6:
        return((liters(packet_string)/flow_time(packet_string))*60)
    else : 
        return 0

    
