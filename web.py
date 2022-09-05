from flask import Flask, render_template

app = Flask(__name__) #

@app.route('/')
def main():
    return render_template("main.html")
@app.route('/pricing')
def pricing():
    return render_template("pricing.html")
@app.route('/old')
def oldmain():
    return render_template("pricing_old.html")
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)