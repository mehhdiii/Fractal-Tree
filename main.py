import random
from FractalTree import FractalTree
import query
bplustree = FractalTree(order=8)  # fractal tree object
# This is the dummmy data for the Fractal Tree where it takes a key, a dictionary for a value and the operation that needs to be done on it
bplustree.buffer((1, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((4, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((7, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((10, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((17, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((21, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((31, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((25, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((19, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((20, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((28, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((42, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((15, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((41, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))


q = query.Query(bplustree)  # query class
q.user_input()  # takes user input
q.show()  # this shows the data we have put as input as table
