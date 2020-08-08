import numpy as np
import pandas as pd
import re



answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
arr_answer_key =  []
PATH_OUTPUT_FODER = "Data Files/Expected Output/"
PATH_DATA_FODER = "Data Files/"


#============String process============
def string_process(line):
    arr_str = line.split(",")
    for i in range(len(arr_str)):
        arr_str[i] = arr_str[i].strip() 
    return arr_str

#============Check valid status============
def check_valid(line):
    pattern = '(N)[0-9]{8}'
    match = re.fullmatch(pattern, line[0])
    len_line = len(line)
    if match and len_line == 26:               
        return 1
    elif len_line != 26:
        return 2
    elif match is None:
        return 3
    else:
        return 4

 #============Score compute============   
def score_compute(arr_answer):
    score = 0
    for i in range(1, len(arr_answer)):
        if arr_answer[i] != '':
            if arr_answer[i] == arr_answer_key[i - 1]:
                score += 4
            elif arr_answer[i] != arr_answer_key[i - 1]:
                score += -1
    return score

#============Main============   
def main():
    retry = True
    while(retry):    
        try:
            file_name = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
            class_grades_str = ""

            with open(PATH_DATA_FODER + file_name + ".txt","r") as file:
                print("Successfully opened " + file_name + ".txt\n")
                print("**** ANALYZING ****\n")
                total_valid = 0
                total_invalid = 0
                arr_score_class = []

                for line in file:
                    lines = string_process(line)
                    status_valid = check_valid(lines)
                    if status_valid == 1:
                        total_valid += 1
                        score = score_compute(lines)
                        arr_score_class.append(score)
                        N = line[:9]
                        class_grades_str += N + "," + str(score) + "\n"

                    elif status_valid == 2:
                        print("Invalid line of data: does not contain exactly 26 values:")
                        print(line)
                        total_invalid += 1    

                    elif status_valid == 3:
                        print("Invalid line of data: N# is invalid:")
                        print(line)
                        total_invalid += 1

                    elif status_valid == 4:
                        print("Invalid line of data: N# is invalid and does not contain exactly 26 values:")
                        print(line)
                        total_invalid += 1

                with open(PATH_OUTPUT_FODER + file_name + "_grades.txt","w") as fw:
                    fw.write(class_grades_str)

                if total_invalid == 0:
                    print("No errors found!\n")

                arr_score_class = np.array(arr_score_class)
                print("**** REPORT ****\n")
                score_max = np.amax(arr_score_class)
                score_min = np.amin(arr_score_class)
                print("Total valid lines of data:", total_valid)
                print("Total invalid lines of data:", total_invalid, "\n") 
                print("Mean (average) score:", round(np.average(arr_score_class),2))
                print("Highest score:", score_max) 
                print("Lowest score:", score_min)
                print("Range of scores:", score_max - score_min) 
                print("Median score:", round(np.median(arr_score_class),2),"\n\n")
                
        except FileNotFoundError:
            c = input("Sorry !, I can't find this filename, do you want to try again ?(T):")
            if c == 'T':
                retry = True
            else:
                retry = False

        except:
            c = input("Error !, do you want to try again ?(T):")
            if c == 'T':
                retry = True
            else:
                retry = False

if __name__ == '__main__':
    arr_answer_key = string_process(answer_key)
    main()