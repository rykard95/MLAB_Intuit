from email import message_from_file
# from IPython import embed
from eparser_utils import fileList, pullout, extract
from insert_py import add_email
from datetime import datetime
import sys
# from IPython import embed

# EXAMPLE PATH: C:/Users/M/Documents/Berkeley/ML/Intuit/got-your-back-1.0/GYB-GMail-Backup-matthewtrepte@gmail.com/2016/8

# CHANGE FIELDS AS NEEDED:
relevant_fields = ['From', 'To', 'Reply-To', 'Date', 'Subject']

if len(sys.argv) < 2:
    print("usage is eparser.py [path to email]")
    sys.exit(0)

source = sys.argv[1]

# LOCATE .eml FILES
emls = fileList(source)

# EXTRACT MESSAGES
messages = []
for eml in emls:
    f = open(eml, "r")
    try:
        messages.append(message_from_file(f))
    except:
        continue
lsts = []
everything = []

# PARSE MESSAGES
for message in messages:
    kvstore = {}

    # ADD RELEVANT FIELDS TO KVSTORE
    for key in message.keys():
        if key in relevant_fields:
            kvstore[key] = message[key]

    # PROVIDE KEYS WITH EMPTY VALUES FOR NON-EXISTANT KEYS
    for key in relevant_fields:
        if key not in kvstore:
            kvstore[key] = ''

    # ADD EMAIL BODY FIELDS TO KVSTORE
    kvstore['Text'], kvstore['Html'], kvstore['Files'], kvstore['Parts'] = extract(message)

    # CONVERT 'Date' TO Date_obj [CURRENTLY BROKEN]
    # s = kvstore['Date'].split(" ")
    # date = s[0] + " " + s[1] + " " + s[2]
    # date_obj = datetime.strptime(date, "%a, %d %b %Y")
    # kvstore['Date'] = date_obj
    # embed()

    # ADD KVSTORE TO MONGO
    add_email(kvstore)
