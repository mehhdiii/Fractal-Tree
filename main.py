import random
from FractalTree import FractalTree
import query
bplustree = FractalTree(order=8)
# for i in range(1000000):
#     x = random.randint(1, 1000)
#     bplustree.buffer((x, str(i)))

bplustree.buffer((1,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer(( 4,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((7, {"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((10,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((17,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((21,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((31,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((25,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((19,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((20,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((28,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((42,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((15,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))
bplustree.buffer((41,{"Name": "Ifrah Ilyas", "Age": "20"}, "insert"))

# bplustree.buffer((5,"5", "insert"))
# bplustree.buffer((3,"3", "insert"))
# bplustree.buffer((2,"2", "insert"))

# bplustree.buffer((100,"5", "insert"))
# bplustree.buffer((-2,"3", "insert"))
# bplustree.buffer((-200,"2", "insert"))
# bplustree.buffer((-100,"5", "insert"))
# bplustree.buffer((97,"3", "insert"))
# bplustree.buffer((-96,"2", "insert"))
bplustree.show()

print(bplustree.search_retrieval(-96))
# bplustree.calling_ra()
# bplustree.all_buffer_flush(bplustree.root)
q=query.Query(bplustree)
# q.user_input()
q.show()
