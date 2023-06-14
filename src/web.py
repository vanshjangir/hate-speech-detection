from flask import Flask, redirect, render_template, request, url_for
import bridge 

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/input", methods = ["POST", "GET"])
def input():
    if request.method == "POST":
        test = request.form['input']
        final = bridge.userinput(text = test)
        return redirect(url_for("result", rs = final))
    else:
        return render_template("input.html")

@app.route("/<rs>")
def result(rs):
    return render_template("result.html", Result = rs)



def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
