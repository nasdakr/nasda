from urllib import request
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
import os

import requests
app = Flask(__name__) #

@app.route('/')
def main():
    return render_template("main.html")
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='favicon.ico')
@app.route('/pricing')
def pricing():
    return render_template("pricing.html")
@app.route('/license')
def license():
    return render_template("license_page.html")
@app.route('/old')
def oldmain():
    return render_template("pricing_old.html")
@app.route('/api/payment/success')
def payment_sucess():
    headers = {
        'Authorization': 'Basic dGVzdF9za19aMFJuWVgydzUzMllBUHdaUktNOE5leXFBcFFFOg==',
        'Content-Type': 'application/json'
    }
    r = requests.post(url="https://api.tosspayments.com/v1/payments/confirm", headers=headers, json={"paymentKey": request.args.get('paymentKey'), "orderId": request.args.get('orderId'), "amount": request.args.get('amount')})
    print(r.status_code)
    #내부 라이센스 생성 서버 호출
    # -- 라이센스 먼저 리턴 한 후 생성 시작
    #
    license = "N8M9A-A572N-FBU4F-AXPG7-PYUHZ"
    return redirect(url_for('success_page', license=f"{license}")) #예시

@app.route('/payment_success/<string:license>')
def success_page(license):
    print(license)
    return render_template('payment_success.html')

@app.route('/api/license/<string:license>')
def get(license):
    try:
        if license == "N8M9A-A572N-FBU4F-AXPG7-PYUHZ":            
            return {"isTrue": 1, "ServiceCreationDate": 20220801, "ServiceExpirationDate": 20220931, "ServiceSize": 10, "ServiceType": 1, "AuthServer": "iscsi.nasda.kr", "AuthChopID": "nsda19402", "AuthChopPW": "67wfm2kknstq7", "InitiatorName": "data.2022-09.kr.nasda.cluster1:pw-ri06x4e2d77a"}
        if license == "HFTH7-PKVQ3-BYQXC-HNELH-9J2GF":            
            return {"isTrue": 1, "ServiceCreationDate": 20220816, "ServiceExpirationDate": 20220915, "ServiceSize": 300, "ServiceType": 1, "AuthServer": "iscsi.nasda.kr", "AuthChopID": "nsda40303", "AuthChopPW": "d1nogmsnpp6fu", "InitiatorName": "data.2022-09.kr.nasda.cluster2:pw-1udma94kfmvk"}
        if len(license) == 29:
            return {"isTrue": 0, "msg": "Invaild License."}
        else:
            return {"isTrue": 0, "msg": "Invaild Format."}
    except:
        return {"isTrue": 0, "msg": "Excepted Unknown Error."}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)