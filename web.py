from flask import Flask, render_template
from flask_restx import Resource, Api

app = Flask(__name__) #
api = Api(app)

@app.route('/')
def main():
    return render_template("main.html")
@app.route('/pricing')
def pricing():
    return render_template("pricing.html")
@app.route('/license')
def license():
    return render_template("license_page.html")
@app.route('/old')
def oldmain():
    return render_template("pricing_old.html")
@api.route('/api/license/<string:license>')
class apihandler(Resource):
    def get(self, license):
        try:
            if license == "N8M9A-A572N-FBU4F-AXPG7-PYUHZ":            
                return {"isTrue": 1, "ServiceCreationDate": 20220801, "ServiceExpirationDate": 20220931, "ServiceSize": 10, "ServiceType": 1, "AuthServer": "iscsi.nasda.kr", "AuthChopID": "nsda19402", "AuthChopPW": "67wfm2kknstqqq57", "InitiatorName": "data.2022-09.kr.nasda.cluster1:pw-ri06x4e2d77a"}
            if license == "HFTH7-PKVQ3-BYQXC-HNELH-9J2GF":            
                return {"isTrue": 1, "ServiceCreationDate": 20220816, "ServiceExpirationDate": 20220915, "ServiceSize": 300, "ServiceType": 1, "AuthServer": "iscsi.nasda.kr", "AuthChopID": "nsda40303", "AuthChopPW": "d1nogmsnppdg86fu", "InitiatorName": "data.2022-09.kr.nasda.cluster2:pw-1udma94kfmvk"}
            if len(license) == 29:
                return {"isTrue": 0, "msg": "Invaild License."}
            else:
                return {"isTrue": 0, "msg": "Invaild Format."}
        except:
            return {"isTrue": 0, "msg": "Excepted Unknown Error."}
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)