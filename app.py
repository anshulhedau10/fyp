from flask import Flask, render_template


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.static_folder = 'static'

@app.route("/")
def index():

    # Render HTML
    return render_template("index.html")

if __name__ == "__main__":
    app.run()