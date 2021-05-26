import pandas
import testing as FT
class Query():
   def __init__(self,t:FT.BPlusTree) -> None:
         self.tree=t
   def messageProcess(message):
       pass
   def show(self):
       dict=self.tree.calling_ra()
       print(dict)
       keys=[]
       values=[]
       for k,v in dict.items():
           keys.append(k)
           values.append(v)
       print(keys,values)
    #    df=pandas.Series()
       df=pandas.DataFrame({"Value": values},index=keys)
       print(df)
       return
q=Query(FT.bplustree)
q.show()