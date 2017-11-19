from services import root_dir
from ndnflask import Flask
from werkzeug.exceptions import NotFound
import json


app = Flask("172.17.0.1")

with open("{}/database/showtimes.json".format(root_dir()), "r") as f:
    showtimes = json.load(f)


@app.route("/hello", methods=['GET'])
def hello():
    return {
        "uri": "/",
        "subresource_uris": {
            "showtimes": "/showtimes",
            "showtime": "/showtimes/<date>"
        }
    }

@app.route("/showtimes", methods=['GET'])
def showtimes_list():
    return showtimes

@app.route("/changeshowtimes", methods=['POST'])
def change_showtimes(data):
    print data
    return showtimes

#@app.route("/showtimes/<date>", methods=['GET'])
#def showtimes_record(date):
#    if date not in showtimes:
#        raise NotFound
#    print showtimes[date]
#    return showtimes[date]

if __name__ == "__main__":
    app.run()
