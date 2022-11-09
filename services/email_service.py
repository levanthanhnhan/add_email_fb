import jsonpickle
from models.email_model import Email

# function parse json email from api
def parse_email_from_api(json_string):
    # list email return
    res = []

    # decode json response from api
    json_decode = jsonpickle.decode(json_string)
    json_emails = json_decode["value"]

    # loop get email in list email json
    for json_email in json_emails:
        email = Email(json_email["id"], json_email["subject"], json_email["body"]["content"])
        res.append(email)

    # return list email
    return res

