# class template for calculating user counts in each state
class StateStatsCounter():
    def __init__(self):
        self.states = [
            {"state":"Alabama", "count": 0},
            {"state":"Alaska", "count": 0},
            {"state":"Arizona", "count": 0},
            {"state":"Arkansas", "count": 0},
            {"state":"California", "count": 0},
            {"state":"Colorado", "count": 0},
            {"state":"Connecticut", "count": 0},
            {"state":"Delaware", "count": 0},
            {"state":"Florida", "count": 0},
            {"state":"Georgia", "count": 0},
            {"state":"Hawaii", "count": 0},
            {"state":"Idaho", "count": 0},
            {"state":"Illinois", "count": 0},
            {"state":"Indiana", "count": 0},
            {"state":"Iowa", "count": 0},
            {"state":"Kansas", "count": 0},
            {"state":"Kentucky", "count": 0},
            {"state":"Louisiana", "count": 0},
            {"state":"Maine", "count": 0},
            {"state":"Maryland", "count": 0},
            {"state":"Massachusetts", "count": 0},
            {"state":"Michigan", "count": 0},
            {"state":"Minnesota", "count": 0},
            {"state":"Mississippi", "count": 0},
            {"state":"Missouri", "count": 0},
            {"state":"Montana", "count": 0},
            {"state":"Nebraska", "count": 0},
            {"state":"Nevada", "count": 0},
            {"state":"New Hampshire", "count": 0},
            {"state":"New Jersey", "count": 0},
            {"state":"New Mexico", "count": 0},
            {"state":"New York", "count": 0},
            {"state":"North Carolina", "count": 0},
            {"state":"North Dakota", "count": 0},
            {"state":"Ohio", "count": 0},
            {"state":"Oklahoma", "count": 0},
            {"state":"Oregon", "count": 0},
            {"state":"Pennsylvania", "count": 0},
            {"state":"Rhode Island", "count": 0},
            {"state":"South Carolina", "count": 0},
            {"state":"South Dakota", "count": 0},
            {"state":"Tennessee", "count": 0},
            {"state":"Texas", "count": 0},
            {"state":"Utah", "count": 0},
            {"state":"Vermont", "count": 0},
            {"state":"Virginia", "count": 0},
            {"state":"Washington", "count": 0},
            {"state":"West Virginia", "count": 0},
            {"state":"Wisconsin", "count": 0},
            {"state":"Wyoming", "count": 0}
        ]



# The ProcessUserData class is built to process the data sent to the API
class ProcessUserData():
    def __init__(self, data):
        self.data = data
        self.population = len(data)
        self.females = 0
        self.males = 0

    # build a results dictionary to be processed by the app to be sent back to the user
    def build_results(self):
        result = {
            "gender_distribution": 
                self.get_gender_distribution(),
            "first_name_distribution": 
                self.get_name_distribution_AM_versus_NZ('first_name'),
            "last_name_distribution": 
                self.get_name_distribution_AM_versus_NZ('last_name'),
            "percentage_in_top_ten_most_populous_states": 
                self.get_percentage_of_people_ten_most_populous_states(),
            "percentage_of_females_in_top_ten_most_populous_states": 
                self.get_percentage_of_gender_in_ten_most_populous_states('gender', 'female', self.females),
            "percentage_of_males_in_top_ten_most_populous_states": 
                self.get_percentage_of_gender_in_ten_most_populous_states('gender', 'male', self.males),
            "age_distribution": 
                self.get_percentage_in_age_groups()
            }

        return result

    # function for calculating the gender distribution amount the data set
    def get_gender_distribution(self):
        male = 0

        # calculates the male population and the total population
        for elm in self.data:
            if elm['gender'] == "male":
                male += 1

        self.males = male
        self.females = self.population - male

        # return a dictionary with the gender distribution
        return {
            "male": round((male/self.population)*100, 2),
            "female": round(100 - (male/self.population)*100, 2)
            }

    #function for finding name distribution for the specified name type
    def get_name_distribution_AM_versus_NZ(self, name):
        # uses python's built in TimSort to sort the data
        data_sorted = sorted(
            self.data, key=lambda i: str(i[name])
        )       

        # binary search on sorted data to find amount of users A-M
        index = binary_search_right_most(data_sorted, len(data_sorted), name, 'N')
        if index == -1:
            names_below_n = 0
        else:
            names_below_n = index

        return {
            "A_to_M": round((names_below_n/self.population)*100, 2),
            "N_to_Z": round(100 - (names_below_n/self.population)*100, 2)
            }

    # finds the population distribution among the top 10 states in data set
    def get_percentage_of_people_ten_most_populous_states(self):
        states_data = StateStatsCounter()

        # count the users from each state
        for user in self.data:
            key = user['state']
            i = binary_search_state_for_index(states_data.states, key)
            states_data.states[i]['count'] += 1

        # sort based on the state population in the data set
        sorted_states = sorted(
            states_data.states, key=lambda i: int(i["count"]), reverse=True
        )

        # slice list to top ten states
        top_ten = sorted_states[0:10]

        top_ten_dict = {}

        # get the data set population distribution for top ten states in data set
        for state in top_ten:
            try:
                percent = round((state["count"]/self.population)*100, 2)
            except ZeroDivisionError:
                percent = 0

            top_ten_dict.update({state["state"]: percent})

        return top_ten_dict

    # the population distribution among the specified key value, pair, and population type
    # for example key="gender" val="female" and pop=the total female population
    def get_percentage_of_gender_in_ten_most_populous_states(self, key, val, pop):
        states_data = StateStatsCounter()

        # count the specified user key matching a value for a given population
        for user in self.data:
            if user[key] == val:
                state = user['state']
                i = binary_search_state_for_index(states_data.states, state)
                states_data.states[i]['count'] += 1        

        sorted_states = sorted(
            states_data.states, key=lambda i: int(i["count"]), reverse=True
        )

        # top ten states by key value population
        top_ten = sorted_states[0:10]

        top_ten_dict = {}

        for state in top_ten:
            try:
                percent = round((state["count"]/pop)*100, 2)
            except ZeroDivisionError:
                percent = 0

            top_ten_dict.update({state["state"]: percent})

        return top_ten_dict            

    # calculates the amount of users by age group
    def get_percentage_in_age_groups(self):
        age_0_to_20 = 0
        age_21_to_40 = 0
        age_41_to_60 = 0
        age_61_to_80 = 0
        age_81_to_100 = 0
        age_over_100 = 0

        for user in self.data:
            if user['age'] >= 0 and user['age'] <=20:
                age_0_to_20 += 1
            elif user['age'] >= 21 and user['age'] <=40: 
                age_21_to_40 += 1   
            elif user['age'] >= 41 and user['age'] <=60:
                age_41_to_60 += 1
            elif user['age'] >= 61 and user['age'] <=80:
                age_61_to_80 += 1
            elif user['age'] >= 81 and user['age'] <=100:
                age_81_to_100 += 1
            elif user['age'] >= 101:
                age_over_100 += 1
            else: 
                continue
        
        # format for the results to be returned
        results = {
            "age_0_to_20": round((age_0_to_20/self.population)*100, 2),
            "age_21_to_40": round((age_21_to_40/self.population)*100, 2),
            "age_41_to_60": round((age_41_to_60/self.population)*100, 2),
            "age_61_to_80": round((age_61_to_80/self.population)*100, 2),
            "age_81_to_100": round((age_81_to_100/self.population)*100, 2),
            "age_over_100": round((age_over_100/self.population)*100, 2)
        }

        return results


# helps find the highest string value up to a target
# used to find how many users with names starting with A-M and N-Z
def binary_search_right_most(a, n, key, target):
    left = 0
    right = n
    while left < right:
        i = (left + right) // 2
        if a[i][key] > target:
            right = i
        else:
            left = i + 1
    return right 


# matches state to in target to state in the states data list object
def binary_search_state_for_index(a, target):
    left = 0
    right = 49
    i = (left + right) // 2
    while a[i]['state'] != target:
        i = (left + right) // 2
        if a[i]['state'] == target:
            return i
        elif a[i]['state'] > target:
            right = i
        elif a[i]['state'] < target:
            left = i + 1
    return i




