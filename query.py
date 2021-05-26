import pandas
import json
import FractalTree as FT
class Query():
    def __init__(self,t:FT.FractalTree) -> None:
        self.tree=t

    def isvalid_input(self,str):
        lst = str.split()
        if lst[0].lower() in ['insert','delete'] and lst[1].isnumeric():
            return True
        
        # if len(lst) == 3 and lst[0].lower() in ['insert','delete'] and lst[1].isnumeric():
            
        #     return True
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
                    ins=str[str.find('{'):]
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
        print()
        dict=self.tree.calling_ra()
        print(dict)
        keys=[]
        values=[]
        print()
        print("Displaying Tree: ")
        for k,v in dict.items():
            keys.append(k)
            values.append(v[0])
        print(keys,values)
        print()
        set={}
        for i in values:
            for j,v in values[0].items():
                if j not in set.keys():
                    set[j]=[]
                    set[j].append(i.get(j))
                else:
                    set[j].append(i.get(j))
        print(set)
        df=pandas.DataFrame(set,index=keys)
        print(df)
        return

q=Query(FT.FractalTree())
q.user_input()
q.show()

# def apply_msg(self, node):
#         """Applies the insert/delete message on the -> node"""
#         for msg in node.buffer:
#             command, key, value = msg
#             if command.lower() == "insert":
#                 key, value = int(msg[1]), msg[2]
#                 ## insertion code goes here
#                 self.insert(node.parent,node, key, value)
#         #now clear the buffer: 
#         node.buffer = []
