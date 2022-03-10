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




class ProcessUserData():
    def __init__(self, data):
        self.data = data
        self.population = 0
        self.females = 0
        self.males = 0

    def build_results(self):
        result = {
            "gender_distribution": self.get_gender_distribution(),
            "first_name_distribution": self.get_fname_distribution_AM_versus_NZ(),
            "last_name_distribution": self.get_lname_distribution_AM_versus_NZ(),
            "percentage_in_top_ten_most_populous_states": self.get_percentage_of_people_ten_most_populous_states(),
            "percentage_of_females_in_top_ten_most_populous_states": self.get_percentage_of_gender_in_ten_most_populous_states('gender', 'female', self.females),
            "percentage_of_males_in_top_ten_most_populous_states": self.get_percentage_of_gender_in_ten_most_populous_states('gender', 'male', self.males),
            "age_distribution": self.get_percentage_in_age_groups()
            }

        return result

    def get_gender_distribution(self):
        population = 0
        male = 0

        for elm in self.data:
            if elm['gender'] == "male":
                male += 1
            population += 1

        self.population = population
        self.males = male
        self.females = population - male

        return {
            "male": round((male/population)*100, 2),
            "female": round(100 - (male/population)*100, 2)
            }

    def get_fname_distribution_AM_versus_NZ(self):
        data_sorted = sorted(
            self.data, key=lambda i: str(i['first_name'])
        )
        count_a_to_m = 0
         
        # this could be faster with a binary search to get the index value of the last M name
        for user in data_sorted:
            if user['first_name'] > 'M':
                break
            count_a_to_m += 1

        return {
            "A_to_M": round((count_a_to_m/self.population)*100, 2),
            "N_to_Z": round(100 - (count_a_to_m/self.population)*100, 2)
            }

    def get_lname_distribution_AM_versus_NZ(self):
        data_sorted = sorted(
            self.data, key=lambda i: str(i['last_name'])
        )
        count_a_to_m = 0
         

        # this could be faster with a binary search to get the index value of the last M name
        for user in data_sorted:
            if user['last_name'] > 'M':
                break
            count_a_to_m += 1

        return {
            "A_to_M": round((count_a_to_m/self.population)*100, 2),
            "N_to_Z": round(100 - (count_a_to_m/self.population)*100, 2)
            }

    def get_percentage_of_people_ten_most_populous_states(self):
        states_data = StateStatsCounter()

        # Refactor this if possible 
        for user in self.data:
            key = user['state']
            for state in states_data.states:
                if key in state.values():
                    state["count"] +=1

        sorted_states = sorted(
            states_data.states, key=lambda i: int(i["count"]), reverse=True
        )

        top_ten = sorted_states[0:10]

        top_ten_dict = {}

        for state in top_ten:
            try:
                percent = round((state["count"]/self.population)*100, 2)
            except ZeroDivisionError:
                percent = 0

            top_ten_dict.update({state["state"]: percent})

        return top_ten_dict

    def get_percentage_of_gender_in_ten_most_populous_states(self, key, val, pop):
        states_data = StateStatsCounter()

        for user in self.data:
            user_state = user['state']
            for state in states_data.states:
                if user_state in state.values() and user[key] == val:
                    state["count"] +=1

        sorted_states = sorted(
            states_data.states, key=lambda i: int(i["count"]), reverse=True
        )

        top_ten = sorted_states[0:10]

        top_ten_dict = {}

        for state in top_ten:
            try:
                percent = round((state["count"]/pop)*100, 2)
            except ZeroDivisionError:
                percent = 0

            top_ten_dict.update({state["state"]: percent})

        return top_ten_dict            

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
        
        results = {
            "age_0_to_20": round((age_0_to_20/self.population)*100, 2),
            "age_21_to_40": round((age_21_to_40/self.population)*100, 2),
            "age_41_to_60": round((age_41_to_60/self.population)*100, 2),
            "age_61_to_80": round((age_61_to_80/self.population)*100, 2),
            "age_81_to_100": round((age_81_to_100/self.population)*100, 2),
            "age_over_100": round((age_over_100/self.population)*100, 2)
        }

        return results


    





