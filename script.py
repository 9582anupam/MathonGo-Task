# Author: "Anupam"(https://github.com/9582anupam/)

import json  # to convert to json file




# handling file

file = open("Task.txt", "r")  # opening latex file in read mode
data = file.read()  # making a file object
file.close()  # closing the file as no need anymore





# formatting data

new_data = ""  # initialising a string variable replacing \ with \\ to prevent error
for i in range(len(data)):
    if data[i] == "\\":  # replacing \ with \\ as instructed
        new_data = new_data + "\\"
    else:
        new_data = new_data + data[i]

split_data = new_data.split("\n")  # splitting the data to remove empty lines
# removing the empty elements in the list of the data
while "" in split_data:
    split_data.remove("")
temp_options = []  # variable for all the options of the questions






# variables needed for the parser

ctr = 0  # line counter
ans = []  # list of dictionary  to be converted to json
questionNumber = 0  # ques no. Counter
temp_text = ""  # question text for each question
new_question_flag = False  # flag for questions
temp_dictionary = {}  # for each question
option_counter = 0  # for each option
option_started = False  # flag for options for each question
sol_started = False  # flag for Solution  for each question
temp_sol = ""  # cumulative solution text
sol_counter = 0  # solution counter for each question






# parsing start here

for i in split_data:

    ctr = ctr + 1  # increment counter for each line


    # parsing question number, question id, question text
    if (
        "question" in i.lower() and "id" in i.lower()
    ):  # check if QuestionID  in line I so we know question starts here
        questionNumber = (
            questionNumber + 1
        )  # quesno is incremented when a new question is found
        temp_dictionary["questionNumber"] = (
            questionNumber  # add key-value pair of quesno
        )
        temp_dictionary["questionId"] = (
            i.split(":")[1].strip().strip("}").strip("{").strip(" ")
        )  # add key-value pair for question id
        new_question_flag = True  # true to let us know a question has begun
    elif (
        new_question_flag == True
    ):  # when question is begun so we start collecting questiontext
        temp_text += i + "\n"
    # questions ends here
    try:
        # checking if questions are starting here by comparing first 3 letter
        if (
            "(A)" == split_data[ctr][0:3] 
            and "(B)" == split_data[ctr + 1][0:3]
            and "(C)" == split_data[ctr + 2][0:3]
            and "(D)" == split_data[ctr + 3][0:3]
        ):  # when question text is over we need to add to dictionary
            temp_dictionary["questionText"] = temp_text[
                0:-1
            ]  # adding key-value pair of question text
            temp_text = ""  # emptying for next question
            new_question_flag = False  # question has ended
            continue
    except:
        pass
    
    
    
    
    # parsing correct answer
    if (
        "(A)" in i[0:3] and "answer" in split_data[ctr + 3].lower()
    ):  
        correct_answer = split_data[ctr + 3]
        option_started = True
        # checking which option is correct
        if "(A)" in correct_answer:
            correct_answer = 1
        elif "(B)" in correct_answer:
            correct_answer = 2
        elif "(C)" in correct_answer:
            correct_answer = 3
        elif "(D)" in correct_answer:
            correct_answer = 4






    # parsing option text
    if option_started and option_counter < 4:
        option_counter += 1
        # for correct answer
        if correct_answer == option_counter:
            temp_options.append(
                {
                    "optionNumber": option_counter,
                    "optionText": i[4:], # remove (A) from options
                    "isCorrect": True
                }
            )
        # for wrong answer
        else:
            temp_options.append(
                {
                    "optionNumber": option_counter,
                    "optionText": i[4:],
                    "isCorrect": False,
                }
            )


    
    
    # parsing solution
    if "Sol" in i:
        sol_started = True
        temp_sol2 = ""
    elif "question" in i.lower() and "id" in i.lower():
        if sol_started == False:
            temp_sol += "Sol. "
        else:
            temp_sol = temp_sol + temp_sol2
            temp_sol2 = ""
            sol_started = False

    if sol_started:
        temp_sol2 += i + "\n"



    # adding parsed data into final data
    if option_counter >= 4:
        option_counter = 0
        option_started = False
        ans.append(temp_dictionary)
        temp_dictionary = {}
        
        




# solution parsing extras, when temp_sol is not empty i.e. it contains some data that has to be put in final sol
if temp_sol2 != "":
    temp_sol += temp_sol2
    temp_sol2 = ""
# splling data so that corresponding sol can be distributed to each question
temp_sol = temp_sol.split("Sol. ")
# remove useless elements
temp_sol = temp_sol[2:]






# adding solutions and options to final dictionary
sol_ctr = 0
for i in range(0, len(temp_options), 4):
    try:  # to handle empty solutions
        ans[sol_ctr]["solutionText"] = temp_sol[sol_ctr]
    except:
        ans[sol_ctr]["solutionText"] = "" # adding empty solutions
    ans[sol_ctr]["options"] = [
        temp_options[i],
        temp_options[i + 1],
        temp_options[i + 2],
        temp_options[i + 3],
    ]
    sol_ctr = sol_ctr + 1






# converting list of dictionaries into json
json_data = json.dumps(ans, indent=4)

#adding json data into .json file
with open("output.json", "w") as json_file:
    json_file.write(json_data)

# conformation message
print("JSON data has been saved to output.json")
