import os

current_dir_path = os.getcwd()

def create(patient):
    patient_list.append(patient)

def remove(patient):
    patient_list.remove(patient)

def list():
    global output
    output += "Patient\tDiagnosis\tDisease\t\t\tDisease\t\tTreatment\t\tTreatment\n"
    output += "Name\tAccuracy\tName\t\t\tIncidence\tName\t\t\tRisk\n" + "-" * 73 + "\n"
    for patient in patient_list:
        # It ensures that each line is equal width where there are variable-length inputs.
        # Since \t makes the line width a multiple of 4. 
        # It divides the variable lengths by 4 to find the desired number of \t.
        output += "{}{}{:.2f}%\t\t{}{}{}\t{}{}{:g}%\n".format(patient[0],
        "\t" * (2 - len(patient[0]) // 4),float(patient[1]) * 100,
        patient[2],"\t" * (4 - len(patient[2]) // 4),patient[3],patient[4],
        "\t" * (4 - len(patient[4]) // 4),float(patient[5]) * 100,)

def probability(patient):
    incidence = eval(patient[3])
    accuracy = float(patient[1])
    true_positives = incidence * accuracy
    false_positives = (1 - incidence) * (1 - accuracy)
    prob = round(true_positives / (true_positives + false_positives),4)
    return prob
    
def recommendation(patient):
    global recom_output
    if(probability(patient)>float(patient[5])):
        recom_output = "System suggests {} to have the treatment.\n".format(patient[0])
    else:
        recom_output = "System suggests {} NOT to have the treatment.\n".format(patient[0])

# It opens, reads and saves all data of the chosen file's
def read(file_name):
    reading_file_name = file_name
    reading_file_path = os.path.join(current_dir_path, reading_file_name)
    with open(reading_file_path, "r") as f:
        data = f.readlines()
    return data

# It saves final output of the program to chosen file
def save(file_name, output):
    writing_file_name = file_name
    writing_file_path = os.path.join(current_dir_path, writing_file_name)
    with open(writing_file_path,"w") as f:
        f.writelines(output)

# Every command adds their output statement into the output variable
output = ""

data = read("doctors_aid_inputs.txt")

patient_list = []

for line in data:
    new_line = line.strip()    # Strip function erases every line's spaces
    # It separates the information and commands in each line and creates a list
    l = new_line.split(" ",1)
    # If conditions control which command the command in the list is
    if(l[0]=="create"):
        new_patient = l[1].split(", ") # It seperates patient's infos and creates another list
        if(new_patient not in patient_list):
            create(new_patient)
            output += "Patient {} is recorded.\n".format(new_patient[0])
        else:
            output += "Patient {} cannot be recorded due to duplication.\n".format(new_patient[0])
    elif(l[0]=="remove"):
        # If it can't find name of the patient it uses the default negative statement
        removes_output = "Patient {} cannot be removed due to absence.\n".format(l[1])
        # It checks if the patient is on the list
        for patient in patient_list:
            if(l[1]==patient[0]):
                remove(patient)
                removes_output = "Patient {} is removed.\n".format(l[1])
                break
        output += removes_output
    elif(l[0]=="list"):
        list()
    elif(l[0]=="recommendation"):
        # If it can't find it uses the default negative statement
        recom_output = "Recommendation for {} cannot be calculated due to absence.\n".format(l[1])
        # It checks if the patient is on the list
        for patient in patient_list:
            if(l[1]==patient[0]):
                recommendation(patient)
                break
        output += recom_output
    elif(l[0]=="probability"):
        # If it can't find it uses the default negative statement
        probs_output = "Probability for {} cannot be calculated due to absence.\n".format(l[1])
        # It checks if the patient is on the list
        for patient in patient_list:
            if(l[1]==patient[0]):
                probs_output = "Patient {} has a probability of {:g}% of having breast cancer.\n".format(l[1],probability(patient)*100)
                break
        output += probs_output

save("doctors_aid_outputs.txt", output)

# Name: Ahmet İkbal
# Surname: Kayapınar
# Number: 2210356043