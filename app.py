from flask import Flask, Response, request, send_file
from processuserdata import ProcessUserData
from dicttoxml import dicttoxml
from random import randint
from requests import get
import xmltodict
import json
import os
import io


app = Flask(__name__)

# quick test endpoint to see what ips on my swarm receive the request
@app.route("/")
def hello():
    ip = get('https://api.ipify.org').content.decode('utf8')
    return f'hello from Ryan\'s Swarm node at {ip}'

# Entry point for the API. 
# The API endpoint can accept content types of multipart/form, application/xml, and application/json
# If sent with multipart/form the API will search for the file's mimetype and process the data accodingly
# 'Accept' headers of application/xml, application/json, and text/plain can be specified by the requesting application
# If there is no acceptable 'Accept' header specified the API will default to a json response
@app.route("/NC_trialAPI", methods=['POST'])
def process_user_stats():
    if request.method == 'POST':

        users = []

        # Handling for a multipart/form-data Content-Type request header
        if 'multipart/form-data' in request.headers['Content-Type']:
            f = request.files['file']   

            # Parses both xml and json to a python dictionary to be processed by the ProcessUserData class
            if f.content_type == 'application/xml':
                data = xmltodict.parse(f)['user']
                users = parse_users_list(data)

                processed_data = ProcessUserData(users).build_results()
            elif f.content_type == 'application/json':
                data = json.load(f)
                users = parse_users_list(data)

                processed_data = ProcessUserData(users).build_results()
            else:
                return 'Unsupported Media Type', 415
        # Handling for a application/json and application/xml Content-Type request header
        # Parses both xml and json to a python dictionary to be processed by the ProcessUserData class
        elif 'application/json' in request.headers['Content-Type']:
            data = request.json
            users = parse_users_list(data)

            processed_data = ProcessUserData(users).build_results()
        elif 'application/xml' in request.headers['Content-Type']:
            data = xmltodict.parse(request.data)['user']
            users = parse_users_list(data)

            processed_data = ProcessUserData(users).build_results()
        else:
            return 'Unsupported Media Type', 415  
                
        # Handling for the Accept header to send back the appropriate response format
        # If no Accept header specified json will be the default response
        # plain text files are build and stored in a temp folder to be delete periodically (TODO)
        if 'application/json' in request.headers['Accept']:
            res = processed_data
        elif 'application/xml' in request.headers['Accept']:
            xml = dicttoxml(processed_data)
            res = Response(xml, mimetype='application/xml')
        elif 'text/plain' in request.headers['Accept']:
            x = randint(1, 100000)
            return_data = get_txt_file(processed_data, x)
            res = send_file(return_data, mimetype='text/plain')
        else:
            res = processed_data

        return res

# function to make a plain text version of the results. 
# This function is invoked if the 'Accept' header is set to 'text/plain' as the mimetype
# This is kind of an inefficient way to build and clean up a plain text file.
# If time permits come back and restructure how this is handled.
def get_txt_file(data, num):
    with open(f'temp/plain_{num}.txt', 'w') as f:
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

    # read the text file and store as bytes in return_file_data
    return_file_data = io.BytesIO()
    with open(f'temp/plain_{num}.txt', 'rb') as file_out:
        return_file_data.write(file_out.read())
    
    return_file_data.seek(0)

    os.remove(f'temp/plain_{num}.txt')

    return return_file_data

# function for parsing the necessary data from the the files generated by https://randomuser.me/
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
    app.run(host='0.0.0.0', port=5000)