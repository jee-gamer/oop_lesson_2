import csv, os
import re
from combination_gen import gen_comb_list

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))

players = []
with open(os.path.join(__location__, 'Players.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        players.append(dict(r))

teams = []
with open(os.path.join(__location__, 'Teams.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        teams.append(dict(r))

titanic = []
with open(os.path.join(__location__, 'Titanic.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        titanic.append(dict(r))

class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None
    
import copy
class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
    
    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table
    
    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table
    
    def __is_float(self, element):
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)

    
    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def pivot_table(self, keys_to_pivot_list, keys_to_aggreagte_list,
                    aggregate_func_list):

        def find_unique(listt):
            unique = []
            for i in listt:
                if isinstance(i, float):  # Check if class is float or not
                    i = int(i)
                    i = str(i)
                if i not in unique:
                    unique.append(i)
            return unique

        def custom_sort(item):  # SPECIFIC SHENANIGANS
            number_sort = item[2]
            gender_sort = item[1]
            name_sort = item[0]
            return (number_sort, gender_sort, name_sort)

        # First create a list of unique values for each key
        unique_values_list = []
        for key in keys_to_pivot_list:
            key_list = my_table3.aggregate(lambda x: x, key)
            unique_values_list.append(find_unique(key_list))

        # print(unique_values_list)
        combi = gen_comb_list(unique_values_list)
        # SORTING SHENANIGANS still fail...
        combi = sorted(combi, key=custom_sort)
        combi.reverse()
        print(combi)
        head_list = []

        for head_row in combi:
            table = table5
            for i in range(len(head_row)):
                table = table.filter(lambda x: x[keys_to_pivot_list[i]] == head_row[i])
                # print(f"filtering {keys_to_pivot_list[i]} and {head_row[i]}")
            """Done filtering table for each combination"""
            value_list = []
            for i in range(len(keys_to_aggreagte_list)):
                agg = table.aggregate(aggregate_func_list[i],
                                      keys_to_aggreagte_list[i])
                value_list.append(agg)
            head_list.append([head_row] + [value_list])
        print(head_list)
        return Table(self.table_name, head_list)

    # Here is an example of unique_values_list for
    # keys_to_pivot_list = ['embarked', 'gender', 'class']
    # unique_values_list =
    # [['Southampton', 'Cherbourg', 'Queenstown'], ['M', 'F'], ['3', '2',
    # '1']]

    # Get the combination of unique_values_list
    # You will make use of the function you implemented in Task 2

    import combination_gen

    # code that makes a call to combination_gen.gen_comb_list

    # Example output:
    # [['Southampton', 'M', '3'],
    #  ['Cherbourg', 'M', '3'],
    #  ...
    #  ['Queenstown', 'F', '1']]

          # code that filters each combination

        # for each filter table applies the relevant aggregate functions
        # to keys to aggregate
        # the aggregate functions is listed in aggregate_func_list
        # to keys to aggregate is listed in keys_to_aggreagte_list

        # return a pivot table

    def __str__(self):
        return self.table_name + ':' + str(self.table)

table1 = Table('cities', cities)
table2 = Table('countries', countries)
table3 = Table('players', players)
table4 = Table('teams', teams)
table5 = Table('titanic', titanic)
my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)
my_DB.insert(table3)
my_DB.insert(table4)
my_DB.insert(table5)
my_table1 = my_DB.search('players')
my_table2 = my_DB.search('teams')
my_table_pt = my_table1.join(my_table2, 'team')
my_table_pt_filtered = (my_table_pt
                        .filter(lambda x: re.search('ia', x['team']))
                        .filter(lambda x: int(x['minutes']) < 200)
                        .filter(lambda x: int(x['passes']) > 100))
print(my_table_pt_filtered)
for player in my_table_pt_filtered.table:
    print(f"surname: {player['surname']}, team: {player['team']}, position: "
          f"{player['position']}")
    print()

my_table_below_10 = my_table2.filter(lambda x: int(x['ranking']) < 10)
my_table_above_10 = my_table2.filter(lambda x: int(x['ranking']) >= 10)
average_b10 = my_table_below_10.aggregate(lambda x: sum(x)/len(x), 'games')
average_a10 = my_table_above_10.aggregate(lambda x: sum(x)/len(x), 'games')

print("The average number of games played")
print(f"Teams ranking below 10: {average_b10}")
print(f"Teams ranking above 10: {average_a10}")

my_table_forwards = my_table1.filter(lambda x: x['position'] == 'forward')
my_table_midfielder = my_table1.filter(lambda x: x['position'] == 'midfielder')
avg_forward = my_table_forwards.aggregate(lambda x: sum(x)/len(x), 'passes')
avg_midfielder = my_table_midfielder.aggregate(lambda x: sum(x)/len(x),
                                               'passes')

print()
print("The average number of passes")
print(f"Forwards : {avg_forward}")
print(f"Midfielder : {avg_midfielder}")
print()

my_table3 = my_DB.search('titanic')
my_table3_first = my_table3.filter(lambda x: int(x['class']) == 1)
my_table3_third = my_table3.filter(lambda x: int(x['class']) == 3)
avg_first = my_table3_first.aggregate(lambda x: sum(x)/len(x), 'fare')
avg_third = my_table3_third.aggregate(lambda x: sum(x)/len(x), 'fare')

print("The average fare paid by passengers")
print(f"First class: {avg_first}")
print(f"Third class: {avg_third}")
print()

my_table3_male = my_table3.filter(lambda x: x['gender'] == "M")
my_table3_male_s = my_table3_male.filter(lambda x: x['survived'] == "yes")
my_table3_female = my_table3.filter(lambda x: x['gender'] == "F")
my_table3_female_s = my_table3_female.filter(lambda x: x['survived'] == "yes")

count_M = my_table3_male.aggregate(lambda x: len(x), 'fare')
survived_M = my_table3_male_s.aggregate(lambda x: len(x), 'fare')
count_F = my_table3_female.aggregate(lambda x: len(x), 'fare')
survived_F = my_table3_female_s.aggregate(lambda x: len(x), 'fare')

rate_M = survived_M/count_M
rate_F = survived_F/count_F

print("The survival rate")
print(f'Of male {rate_M}')
print(f'Of female {rate_F}')
print()

table4 = Table('titanic', titanic)
my_DB.insert(table4)
my_table4 = my_DB.search('titanic')
my_pivot = my_table4.pivot_table(['embarked', 'gender', 'class'], ['fare', 'fare', 'fare', 'last'], [lambda x: min(x), lambda x: max(x), lambda x: sum(x)/len(x), lambda x: len(x)])


# print("Test filter: only filtering out cities in Italy")
# my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
# print(my_table1_filtered)
# print()
#
# print("Test select: only displaying two fields, city and latitude, for cities in Italy")
# my_table1_selected = my_table1_filtered.select(['city', 'latitude'])
# print(my_table1_selected)
# print()
#
# print("Calculting the average temperature without using aggregate for cities in Italy")
# temps = []
# for item in my_table1_filtered.table:
#     temps.append(float(item['temperature']))
# print(sum(temps)/len(temps))
# print()
#
# print("Calculting the average temperature using aggregate for cities in Italy")
# print(my_table1_filtered.aggregate(lambda x: sum(x)/len(x), 'temperature'))
# print()
#
# print("Test join: finding cities in non-EU countries whose temperatures are below 5.0")
# my_table2 = my_DB.search('countries')
# my_table3 = my_table1.join(my_table2, 'country')
# my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
# print(my_table3_filtered.table)
# print()
# print("Selecting just three fields, city, country, and temperature")
# print(my_table3_filtered.select(['city', 'country', 'temperature']))
# print()
#
# print("Print the min and max temperatures for cities in EU that do not have coastlines")
# my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
# print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
# print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
# print()
#
# print("Print the min and max latitude for cities in every country")
# for item in my_table2.table:
#     my_table1_filtered = my_table1.filter(lambda x: x['country'] == item['country'])
#     if len(my_table1_filtered.table) >= 1:
#         print(item['country'], my_table1_filtered.aggregate(lambda x: min(x), 'latitude'), my_table1_filtered.aggregate(lambda x: max(x), 'latitude'))
# print()
