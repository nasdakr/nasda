from flask import Flask, render_template

app = Flask(__name__) #

@app.route('/')
def main():
    return render_template("pricing.html")
@app.route('/old')
def main():
    return render_template("pricing_old.html")
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)