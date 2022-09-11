import random
from time import time
import json


STRING_POOL = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"

def generate_license(service_type, amount):
    amount = str(amount)
    
    if service_type == 1: #iSCSI
        size = None
        if amount == "500":
            size = 10
        if amount == "100test":
            size = 100
        if amount == "9900":
            size = 300
        if size == None:
            return "400" # amount 오류
        code = gen()
        with open("module/db.json", "r") as f:
            data = json.load(f)
        if code in data:
            generate_license(service_type, amount) #재귀
        print(code)
        data[code] = {"isTrue": 2, "ServiceCreationDate": time(), "ServiceSize": size, "ServiceType": 1, "AuthServer": None, "AuthChopID": "0", "AuthChopPW": None, "InitiatorName": None}
        with open("module/db.json", "w") as f: #isTrue 2 = 준비중 표시
            json.dump(data, f)

    return code

def gen():
    code = ""
    for c in range(5):
        for i in range(5):
            code += random.choice(STRING_POOL)
        if c < 4:
            code += "-"
    return code