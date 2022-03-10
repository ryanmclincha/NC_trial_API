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

        save_txt_file(processed_data)

        res = processed_data

        return res

def save_txt_file(data):
    with open('test.txt', 'w') as f:
        f.write('Percentage female versus male: {}%\n'.format(data['gender_distribution']['female']))
        f.write('Percentage of first names that start with A-M versus N-Z: {}%\n'.format(data['first_name_distribution']['A_to_M']))
        f.write('Percentage of last names that start with A-M versus N-Z: {}%\n'.format(data['last_name_distribution']['A_to_M']))
        f.write('Percentage of people in each state (up to top ten popultaions): \n')
        for state, percent in data['percentage_in_top_ten_most_populous_states'].items():
            f.write(f'\t{state}: {percent}\n')
        f.write('Percentage of females in each state (up to top ten popultaions): \n')
        for state, percent in data['percentage_of_females_in_top_ten_most_populous_states'].items():
            f.write(f'\t{state}: {percent}\n')
        f.write('Percentage of males in each state (up to top ten popultaions): \n')
        for state, percent in data['percentage_of_males_in_top_ten_most_populous_states'].items():
            f.write(f'\t{state}: {percent}\n')
        f.write('Percentage of people in age groups: \n')
        for age, percent in data['age_distribution'].items():
            f.write(f'\t{age}: {percent}\n')


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