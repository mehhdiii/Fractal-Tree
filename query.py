import pandas
import json
import FractalTree as FT
class Query():
    def __init__(self,t:FT.FractalTree) -> None:
        self.tree=t

    def isvalid_input(self,str):
        # this checks if the input provided is in valid syntax
        # function is only true when there is valid syntax or input is "Q" that is quit
        lst = str.split()
        if lst[0].lower() in ['insert','delete'] and lst[1].isnumeric():
            return True
        elif str == "Q":
            return True
        elif not lst[1].isnumeric():
            print("ERROR: Key must be a positive integer.")
            print()
            return False
        else:
            print(lst)
            print("ERROR: Please enter a command following the format - <insert/delete> <key> <value> or enter 'Q' to quit!")
            print()
            return False

    def user_input(self):
        # this takes in the input from the user until the user quits by writing Q
        print()
        print(" - Command format: <insert/delete> <key> <value>")
        print(" - Enter 'Q' to quit")
        print()
        while True: #keep taking input till user quits
            print("Enter command: ", end = "")
            str = input()
            #taking input and adding to buffer in the form of a list
            if str != "Q" and self.isvalid_input(str):
                command=str.split()
                if '{' in str:
                    ins=str[str.find('{'):] # this is for taking value which is in the form of a dictionary
                    print(ins)
                    command=command[:2]
                    command.append(json.loads(ins))
                command=command[1:]+[command[0]]
                self.tree.buffer(command)
            elif str == "Q":
                break
            else:
                continue

    def show(self):
        # this function shows the data in the form of a table
        print()
        dict=self.tree.calling_ra() # taking data from Fractal Trees
        print(dict)
        keys=[]
        values=[]
        print()
        print("Displaying Tree: ")
        for k,v in dict.items():
            keys.append(k) # making separate lists for keys and valued
            for i in v:
                    if type(i)!=str:
                        values.append(i)
        set={}
        for i in values:
            for j,v in values[0].items(): # this makes a dictionary where the the index of the values in the array correspond to that of in the key array
                if j not in set.keys():
                    set[j]=[]
                    set[j].append(i.get(j))
                else:
                    set[j].append(i.get(j))
        print(set)
        df=pandas.DataFrame(set,index=keys) # makes a 'dataframe' or table for the data
        print(df)
        return



