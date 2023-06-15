from flask import Flask, redirect, render_template, render_template_string, request, url_for, Response
import bridge 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/input", methods = ["POST", "GET"])
def input():
    if request.method == "POST":
        formdata = request.form['input']
        final = bridge.userinput(link = formdata)
        def generate():
            for line in final.split("\n\n"):
                yield line 

        showdata = ""
        for i in generate():
            showdata += i
            showdata += "<br>"
        return render_template("input.html", r = showdata)
    else:
        return render_template("input.html")


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
