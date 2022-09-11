from urllib import request
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json
import requests

from module.license_gen import generate_license
from module.iSCSI_module import iSCSI_init
app = Flask(__name__) #

#WEB
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

#TEST SERVER
@app.route('/api/allocate_100_tsv')
def test_100():
    gen_license = generate_license(1, "100test")
    if gen_license == "400":
        return redirect(url_for(main)) #실패 페이지 만들어야댐
    got_license = (gen_license)
    try:
        return redirect(url_for('success_page', license=f"{gen_license}")) #예시
    finally:
        print("Starting")
        r_value = iSCSI_init(got_license)
        print("Done!")
        print(r_value)
        #여기에 d

#PAYMENT

@app.route('/api/iscsi_payment/success')
def payment_sucess():
    headers = {
        'Authorization': 'Basic dGVzdF9za19aMFJuWVgydzUzMllBUHdaUktNOE5leXFBcFFFOg==',
        'Content-Type': 'application/json'
    }
    r = requests.post(url="https://api.tosspayments.com/v1/payments/confirm", headers=headers, json={"paymentKey": request.args.get('paymentKey'), "orderId": request.args.get('orderId'), "amount": request.args.get('amount')})
    if r.status_code == 200:
        print("[*] 승인 완료")
    else:
        print("[*] 승인 오류")
        
    gen_license = generate_license(1, request.args.get('amount'))
    if gen_license == "400":
        return redirect(url_for(main)) #실패 페이지 만들어야댐
    got_license = (gen_license)
    try:
        return redirect(url_for('success_page', license=f"{gen_license}")) #예시
    finally:
        print("Starting")
        r_value = iSCSI_init(got_license)
        print("Done!")
        print(r_value)
        #여기에 d

@app.route('/payment_success/<string:license>')
def success_page(license):
    print(license)
    return render_template('payment_success.html')

#API

@app.route('/api/license/<string:license>') #0 = error, 1 = ready, 2 = working
def get(license):
    with open("module/db.json", "r") as f:
        data = json.load(f)
    print(data)
    if license in data:
        return data[license]
    else:
        return {"isTrue": 0, "msg": "Excepted Unknown Error."}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)