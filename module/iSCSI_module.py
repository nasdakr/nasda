import requests
import json
import random
import time

def iSCSI_init(license):
    start_time = time.time() # 시간 측정 함수.
    STRING_POOL = "1234567890qwertyuiopasdfghjklzxcvbnm"
    initiator = ""
    for i in range(12):
        initiator += random.choice(STRING_POOL)
    secret_key = ""
    for i in range(16):
        secret_key += random.choice(STRING_POOL)
    SERVER_ADDY = "http://iscsi.nasda.kr/api/v2.0/"

    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer 1-FTmVzuWj1QidtKPrcJxuV2MZUTS32mcApFnG8c46fknMXp9QdlBUAG60uCy39XCl'}
    with open("module/db.json", "r") as f:
        data = json.load(f)
    id = str(random.randrange(10000, 99999))
    for i in data:
        if "nsda" + id == data[i]['AuthChopID']:
            print("재귀 발생")
            iSCSI_init(license)
    id = "nsda" + id
    print(f"[*] 할당 id : {id}")
    #10GB Zvol 생성
    print("[*] Zvol 생성 시작")
    volsize = 1073743462 * data[license]["ServiceSize"]
    gbs = data[license]["ServiceSize"]
    r = requests.post(
      f'{SERVER_ADDY}pool/dataset',
      headers=headers,
      data=json.dumps({
           "name": f"nasda_SSD_1/{gbs}GB_{id}",
           "comments": "made by python init server",
           "volsize": volsize,
           "sync": "STANDARD",
           "compression":"LZ4",
           "deduplication":"OFF",
           "volblocksize":"16K",
           "inherit_encryption": True,
           "type":"VOLUME"
       })
    )
    print(r.json())
    if r.json()["id"] == f"nasda_SSD_1/{gbs}GB_{id}":
        print("SUCESS")
    else:
        print(r.json())
        exit(0)
    #initiator 생성
    print("[*] Initiator 생성 시작")
    r = requests.post(
      f'{SERVER_ADDY}iscsi/initiator',
      headers=headers,
      data=json.dumps({
           "initiators": [f"data.2022-09.kr.nasda.cluster1:pass-{initiator}"],
           "auth_network": [],
           "comment": "made by python init server"
       })
     )
    if r.json()["initiators"][0] == f"data.2022-09.kr.nasda.cluster1:{initiator}":
        print("SUCESS")
        initiator_id = int(r.json()["id"])
    else:
        print(r.json())
        exit(0)
    #target 생성 
    print("[*] Target 생성 시작")   
    r = None
    r = requests.post(
      f'{SERVER_ADDY}iscsi/target',
      headers=headers,
      data=json.dumps({
           "name": f"{id}",
           "mode": "ISCSI",
           "groups": [{"portal": 1, "initiator": initiator_id, "authmethod": "NONE", "auth": 0}]
       })
     )
    if r.json()["name"] == f"{id}":
        print("SUCESS")
        target_id = r.json()["id"]
    else:
        print(r.json())
        exit(0)
    #extent 생성
    print("[*] Extent 생성 시작")
    r = None
    r = requests.post(
      f'{SERVER_ADDY}iscsi/extent',
      headers=headers,
      data=json.dumps({
            "blocksize": 512,
            "disk": f"zvol/nasda_SSD_1/10GB_{id}", #나중에 하드 여러개 생겼을 경우 능동적으로 pool 선택 하는거 추가 필요. ex) 1 ~ 순서대로 용량 차면 다음 풀 이용.
            "enabled": True,
            "filesize": 0,
            "insecure_tpc": True,
            "name": f"{id}",
            "rpm": "SSD",
            "type": "DISK"
       })
     )
    if r.json()["name"] == f"{id}":
        print("SUCESS")
        extent_id = r.json()["id"]
    else:
        print(r.json())
        exit(0)
    #Associated Target 생성
    print("[*] Associated Target 생성 시작")
    r = None
    r = requests.post(
      f'{SERVER_ADDY}iscsi/targetextent',
      headers=headers,
      data=json.dumps({
            "target": target_id,
            "extent": extent_id
       })
     )
    if r.json()["extent"] == extent_id:
        print("SUCESS")
    else:
        print(r.json())
        exit(0)

    #Auth 생성 == 로그인 정보
    print("[*] 로그인 정보 생성 시작")
    r = None
    r = requests.post(
      f'{SERVER_ADDY}iscsi/auth',
      headers=headers,
      data=json.dumps({
            "tag": 1,
            "user": f"{id}",
            "secret": f"{secret_key}",
            "peeruser": "",
            "peersecret": ""
       })
     )
    if r.json()["user"] == f"{id}":
        print("SUCESS")
        auth_id = r.json()["id"]
    else:
        print(r.json())
        exit(0)

    print("===========================================")
    print(f"[+] 연결 CHOP id : {id}")
    print(f"[+] 연결 CHOP PW : {secret_key}") 
    print(f"[+] 연결 Target : data.2022-09.kr.nasda.cluster1:{id}") 
    print(f"[+] Initiator 이름 : data.2022-09.kr.nasda.cluster1:pass-{initiator}")
    print(f"[+] Initiator 그룹 id (관리자용) : {initiator_id}")
    print(f"[+] 소요 시간 : {time.time() - start_time}")
iSCSI_init("66GTQ-1CXFW-HZZZ2-JIANT-MTI3V")