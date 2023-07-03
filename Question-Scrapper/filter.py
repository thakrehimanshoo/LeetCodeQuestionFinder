import re  #for pattern
questions = []  
with open("questionrun1.txt", "r") as file:
    for line in file:
        questions.append(line) 

#to remove solution links 
def remove_sol(array, pattern):
    new_array = []
    for element in array:
        if pattern not in element:
            new_array.append(element)
        else:
            print("Removed: " + element) 
    return new_array


arr = remove_sol(questions, "/solution") #will filter for us
print(len(arr)) 
arr = list(set(arr))

with open('filtered_problems.txt', 'a') as f:
    for j in arr:
        f.write(j)
