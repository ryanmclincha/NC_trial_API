from flask import Flask, Response, request
from user import User
from processuserdata import ProcessUserData
import xmltodict
import json



app = Flask(__name__)


@app.route("/NC_trialAPI", methods=['POST'])
def process_user_stats():
    if request.method == 'POST':

        users = []

        if 'multipart/form-data' in request.headers['Content-Type']:
            f = request.files['file']   

            if f.content_type == 'application/xml':
                data = xmltodict.parse(f)['user']
                users = parse_users_list(data)

                processed_data = ProcessUserData(users).build_results()
            elif f.content_type == 'application/json':
                data = json.load(f)
                users = parse_users_list(data)

                processed_data = ProcessUserData(users).build_results()
            else:
                return 'unsupported mimetype'

        res = processed_data

        return res





def parse_users_list(data):
    users = []
    for elm in data['results']:
        user = {
            "first_name":elm["name"]["first"],
            "last_name":elm["name"]["last"],
            "gender":elm["gender"],
            "state":elm["location"]["state"],
            "age":int(elm["dob"]["age"])
        }
        users.append(user)

    return users


if __name__ == '__main__':
    app.run(debug=True)