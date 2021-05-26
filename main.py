import random
from FractalTree import FractalTree

bplustree = FractalTree(order=8)
# for i in range(1000000):
#     x = random.randint(1, 1000)
#     bplustree.buffer((x, str(i)))

bplustree.buffer((1,"1", "insert"))
bplustree.buffer(( 4, "4", "insert"))
bplustree.buffer((7, "7", "insert"))
bplustree.buffer((10,"10", "insert"))
bplustree.buffer((17,"17", "insert"))
bplustree.buffer((21,"21", "insert"))
bplustree.buffer((31,"name", "insert"))
bplustree.buffer((25,"25", "insert"))
bplustree.buffer((19,"19", "insert"))
bplustree.buffer((20,"20", "insert"))
bplustree.buffer((28,"28", "insert"))
bplustree.buffer((42,"42", "insert"))
bplustree.buffer((15,"15", "insert"))
bplustree.buffer((41,"41", "insert"))

bplustree.buffer((5,"5", "insert"))
bplustree.buffer((3,"3", "insert"))
bplustree.buffer((2,"2", "insert"))

bplustree.buffer((100,"5", "insert"))
bplustree.buffer((-2,"3", "insert"))
bplustree.buffer((-200,"2", "insert"))
bplustree.buffer((-100,"5", "insert"))
bplustree.buffer((97,"3", "insert"))
bplustree.buffer((-96,"2", "insert"))
bplustree.show()

print(bplustree.search_retrieval(-96))
# bplustree.calling_ra()
# bplustree.all_buffer_flush(bplustree.root)

