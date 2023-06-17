from flask import Flask, redirect, render_template, render_template_string, request, url_for, Response
import bridge 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/input", methods = ["POST", "GET"])
def input():
    if request.method == "POST":
        textdata = request.form['text']
        linkdata = request.form['youtube link']
        filedata = request.form['file']
        
        final = ""
        if len(textdata) != 0:
            final = bridge.userinput(text = textdata)
        else:
            final = bridge.userinput(link = linkdata)

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
