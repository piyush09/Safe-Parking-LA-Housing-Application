import sys
import os
import math
import time
import string
import time

import operator

start_time = time.time()

data = open("input.txt").read().strip().splitlines()

output = open("/Users/Piyush/Desktop/output.txt", "w+") # Creating output file data
# output = open("output.txt", "w+")

filetext = [] # filetext is a list storing each line in input file

for line in data:
    filetext.append(line)  # appending each line in input file to filetext

bed = int(filetext[0]) # bed denoting the number of beds

park_space = int(filetext[1]) # park_space denoting the number of spaces in the parking lot

lahsa_num = filetext[2] # lahsa_num denoting the number of applicants chosen by LAHSA so far

lahsa_id = [] # lahsa_id list denoting applicant_id number chosen by LAHSA
lahsa_id = filetext[3:3+int(lahsa_num)] # Putting all elements from filetext's line 3 till line number of 'lahsa_num' into 'lahsa_id' list
# print lahsa_id

park_space_num_list = filetext[3+int(lahsa_num):4+int(lahsa_num)]
park_space_num = park_space_num_list[0] # park_space_num denoting the number of applicants chosen by SPLA so far
# print park_space_num

park_space_id = [] # park_space_id list denoting applicant_id number chosen by SPLA
park_space_id = filetext[4+int(lahsa_num):4+int(lahsa_num)+int(park_space_num)] # Putting all elements from filetext's line (4+int(lahsa_num)) till line number of 4+int(lahsa_num)+int(park_space_num) into 'park_space_id' list
# print park_space_id

applicant_num_list = filetext[4+int(lahsa_num)+int(park_space_num):5+int(lahsa_num)+int(park_space_num)]
applicant_num = applicant_num_list[0] # applicant_num denoting the total number of applicants
# print applicant_num

applicant_id = []
applicant_id = filetext[5+int(lahsa_num)+int(park_space_num):5+int(lahsa_num)+int(park_space_num)+int(applicant_num)] # applicant_id contains the list of applicant's information
# print "Applicant ID"
# print applicant_id

global lahsa_acceptance_list # making a global list for "lahsa_acceptance_list"
lahsa_acceptance_list = []  # applicant eligible for lahsa acceptance put into "lahsa_acceptance_list"
lahsa_acceptance_dict = {} # "lahsa_acceptance_dict" maintaining a count of days for a lahsa accepted applicant
def lahsa_accept(applicant_detail): #  function to check if a particular applicant is accepted by Lahsa, "applicant_detail" contains the applicant_id details
    gender = applicant_detail[5] # applicant's gender
    age = int(applicant_detail[6:9]) # applicant's age
    pet = applicant_detail[9] # variable to check if applicant has pets

    if (gender =="F" and (age > 17) and pet == "N" ):
        lahsa_acceptance_list.append(applicant_detail)

global spla_acceptance_list # making a global list for "spla_acceptance_list"
spla_acceptance_list = [] # applicant eligible for spla_acceptance put into "spla_acceptance_list"
spla_acceptance_dict = {} # "spla_acceptance_dict" maintaining a count of days for spla accepted applicant
def spla_accept(applicant_detail): #  function to check if a particular applicant is accepted by Spla
    medical_condition = applicant_detail[10] # variable to check if applicant has medical conditions
    car = applicant_detail[11] # variable to check if applicant has car
    driving_license = applicant_detail[12] # variable to check if applicant has driving license

    if (medical_condition == "N" and car == "Y"  and driving_license =="Y" ):
        spla_acceptance_list.append(applicant_detail)

def find(s,ch):
    return [i for i, ltr in enumerate(s) if ltr==ch]

def spla_play(spla_acceptance_dict, lahsa_acceptance_dict, spla_value, lahsa_value, bed_assigned_list, park_space_assigned_list, alpha, beta):

    if (len(spla_acceptance_dict)==0): # Returning spla_value if spla_acceptance_dict is empty
        return spla_value

    infinity = float('inf')
    max_value = -infinity

    for key, value in spla_acceptance_dict.iteritems(): # Iterating over all spla_acceptance_dict items

        bypass = True # bypass condition to check if there are available parking spaces for the incoming applicant for each corresponding day
        park_space_assigned_list_duplicate = park_space_assigned_list[:]
        for i in find(value, "1"):
            if(park_space_assigned_list_duplicate[i]-1 >= 0):
                park_space_assigned_list_duplicate[i] = park_space_assigned_list_duplicate[i] - 1

            else:
                bypass = None
                break

        if bypass:
            park_space_assigned_list = park_space_assigned_list_duplicate
            spla_value = spla_value + value.count('1') # adding first key's value to spla's value


            spla_acceptance_dict_duplicate = spla_acceptance_dict.copy() # creating copy of spla_acceptance_dict
            spla_acceptance_dict_duplicate.pop(key, None) # removing first_key and it's corresponding value from spla_acceptance_dict_duplicate

            lahsa_acceptance_dict_duplicate = lahsa_acceptance_dict.copy()
            lahsa_acceptance_dict_duplicate.pop(key, None) # removing first_key and it's corresponding value from lahsa_acceptance_dict_duplicate

            max_value = max(max_value, lahsa_play(spla_acceptance_dict_duplicate, lahsa_acceptance_dict_duplicate, spla_value, lahsa_value, bed_assigned_list, park_space_assigned_list, alpha, beta))

            for i in find(value, "1"):
                park_space_assigned_list_duplicate[i] = park_space_assigned_list_duplicate[i] + 1

            spla_value = spla_value - value.count('1')

            if max_value>= beta:
                return max_value
            alpha = max(alpha, max_value)
        else:
            return spla_value
    return max_value


def lahsa_play(spla_acceptance_dict, lahsa_acceptance_dict, spla_value, lahsa_value, bed_assigned_list, park_space_assigned_list, alpha, beta):

    if (len(lahsa_acceptance_dict)==0): # Checking if lahsa_acceptance_dict is empty
        if (len(spla_acceptance_dict)!=0):
            for key, value in spla_acceptance_dict.iteritems():
                park_space_assigned_list_duplicate = park_space_assigned_list[:]
                bypass = True
                for i in find(value, "1"):
                    if (park_space_assigned_list_duplicate[i] - 1 >= 0):
                        park_space_assigned_list_duplicate[i] = park_space_assigned_list_duplicate[i] - 1
                    else:
                        bypass = None
                        break

                if bypass:
                    park_space_assigned_list = park_space_assigned_list_duplicate
                    spla_value = spla_value + value.count('1')

        return spla_value


    infinity = float('inf')
    min_value = infinity

    for key, value in lahsa_acceptance_dict.iteritems():

        bypass = True # bypass condition to check if there are available beds for the incoming applicant for each corresponding day
        bed_assigned_list_duplicate = bed_assigned_list[:]
        for i in find(value, "1"):
            if(bed_assigned_list_duplicate[i]-1 >= 0):
                bed_assigned_list_duplicate[i] = bed_assigned_list_duplicate[i] - 1

            else:
                bypass = None
                break

        if bypass:
            bed_assigned_list = bed_assigned_list_duplicate

            lahsa_value = lahsa_value + value.count('1') # adding first key's value to lahsa's value

            lahsa_acceptance_dict_duplicate = lahsa_acceptance_dict.copy() # creating copy of lahsa_acceptance_dict
            lahsa_acceptance_dict_duplicate.pop(key, None) # removing first_key and it's corresponding value from lahsa_acceptance_dict_duplicate

            spla_acceptance_dict_duplicate = spla_acceptance_dict.copy()
            spla_acceptance_dict_duplicate.pop(key, None) # removing first_key and it's corresponding value from spla_acceptance_dict

            min_value = min(min_value, spla_play(spla_acceptance_dict_duplicate, lahsa_acceptance_dict_duplicate, spla_value, lahsa_value, bed_assigned_list, park_space_assigned_list, alpha, beta))

            for i in find(value, "1"):
                bed_assigned_list_duplicate[i] = bed_assigned_list_duplicate[i] + 1

            if min_value <= alpha:
                return min_value
            beta= min(beta,min_value)

        else:
            return spla_value
    return  min_value

def main():

    for i in applicant_id:
        lahsa_accept(i) # passing each applicant in applicant_id to check if it can be accepted into lahsa
    # print "Lahsa acceptance list"
    # print lahsa_acceptance_list # printing lahsa_acceptance_list

    for i in lahsa_acceptance_list:
        days = i[13:]
        i = i[0:5]  # extracting only first five characters of a key in lahsa_acceptance_list
        lahsa_acceptance_dict[i]=days # assigning value to a key in lahsa_acceptance_dict of the days

    for key in park_space_id:  # Removing elements in park_space_id from lahsa_acceptance_dict
        lahsa_acceptance_dict.pop(key, None)

    for key in lahsa_id:  # Removing elements in lahsa_id from lahsa_acceptance_dict
        lahsa_acceptance_dict.pop(key, None)

    # print "LAHSA-Dictionary"
    # print lahsa_acceptance_dict
    # print "End"

    for i in applicant_id:
        spla_accept(i) # passing each applicant in applicant_id to check if it can be accepted into spla
    # print spla_acceptance_list # printing spla_acceptance_list

    for i in spla_acceptance_list:
        days = i[13:]
        i=i[0:5] # extracting only first five characters of a key in spla_acceptance_list
        spla_acceptance_dict[i]=days # assigning value to a key in spla_acceptance_dict of the days

    for key in park_space_id:  # Removing elements in park_space_id from spla_acceptance_dict
        spla_acceptance_dict.pop(key, None)

    for key in lahsa_id:  # Removing elements in lahsa_id from spla_acceptance_dict
        spla_acceptance_dict.pop(key, None)

    # print "SPLA-Dictionary"
    # print spla_acceptance_dict
    # print "End"

    bed_assigned_list = [bed, bed, bed, bed, bed, bed, bed] # list of the beds in the bed_list with each day assigned as bed
    park_space_assigned_list = [park_space, park_space, park_space, park_space, park_space, park_space, park_space]

    for i in applicant_id:
        temp_key = i[0:5]
        if temp_key in lahsa_id:
            for idx in find(i[13:], "1"):
                bed_assigned_list[idx] = bed_assigned_list[idx] - 1

        if temp_key in park_space_id:
            for idx in find(i[13:], "1"):
                park_space_assigned_list[idx] = park_space_assigned_list[idx] - 1

    # print "BED ASSIGNMENT LIST"
    # print bed_assigned_list

    # print "Park Spaces assigned list"
    # print park_space_assigned_list

    result_dict = {}

    for key, value in spla_acceptance_dict.iteritems(): # iterating over all elements in spla_acceptance_dict

        spla_acceptance_dict_initial_duplicate = spla_acceptance_dict.copy()
        spla_acceptance_dict_initial_duplicate.pop(key, None) # Removing accessed key from spla_acceptance_dict_initial_duplicate dictionary

        lahsa_acceptance_dict_initial_duplicate = lahsa_acceptance_dict.copy()
        lahsa_acceptance_dict_initial_duplicate.pop(key, None)

        park_space_assigned_list_duplicate = park_space_assigned_list[:]
        for idx in find(value, "1"):
            park_space_assigned_list_duplicate[idx] = park_space_assigned_list_duplicate[idx] - 1

        spla_initial_value_frequency = value.count('1')

        infinity = float('inf')
        alpha = -infinity
        beta = infinity


        result = lahsa_play(spla_acceptance_dict_initial_duplicate, lahsa_acceptance_dict_initial_duplicate, spla_initial_value_frequency, 0, bed_assigned_list, park_space_assigned_list_duplicate, alpha, beta)

        spla_initial_value_frequency = 0

        for idx in find(value, "1"):
            park_space_assigned_list_duplicate[idx] = park_space_assigned_list_duplicate[idx] + 1

        # print key, result

        result_dict[key] = result


    value_list = []
    keys_list = []
    for key, value in result_dict.iteritems():
        value_list.append(value)
        keys_list.append(key)

    maximum_value = max(value_list)
    # print " Maximum Value"
    # print maximum_value # it contains the maximum_value returned by all the trees

    for key, value in result_dict.iteritems():
        if maximum_value == value:
            maximum_key = key

    # print "Maximum Key randomly selected"
    # print maximum_key # maximum_key has the Maximum Key randomly selected's value for maximum_value returned by the tree

    difference_value_list = [] # difference_value_list contains difference with the (park_space*7)-value_list element
    for i in value_list:
        i = park_space*7 - i
        difference_value_list.append(i)
    descending_sorted_keys = [x for _, x in sorted(zip(difference_value_list, keys_list))]

    # print " Descending Sorted Keys list:"
    # print descending_sorted_keys
    # print " 1st element of Descending Sorted Keys"
    final_key = descending_sorted_keys[0]
    # print final_key

    final_result = str(final_key)
    output.write(final_result)
    output.close()

if __name__=="__main__":
    main()

# print("%s seconds" % (time.time() - start_time)) # Printing execution time in seconds