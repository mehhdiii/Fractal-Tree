import random
from FractalTree import FractalTree

bplustree = FractalTree(order=4)
# for i in range(1000000):
#     x = random.randint(1, 1000)
#     bplustree.buffer((x, str(i)))

bplustree.buffer((1,"1"))
bplustree.buffer((4, "4"))
bplustree.buffer((7, "7"))
bplustree.buffer((10,"10"))
bplustree.buffer((17,"17"))
bplustree.buffer((21,"21"))
bplustree.buffer((31,"name"))
bplustree.buffer((25,"25"))
bplustree.buffer((19,"19"))
bplustree.buffer((20,"20"))
bplustree.buffer((28,"28"))
bplustree.buffer((42,"42"))
bplustree.buffer((15,"15"))
bplustree.buffer((41,"41"))

bplustree.buffer((5,"5"))
bplustree.buffer((3,"3"))
bplustree.buffer((2,"2"))

bplustree.buffer((100,"5"))
bplustree.buffer((-2,"-2"))
bplustree.buffer((-200,"-200"))
bplustree.buffer((-100,"-100"))
bplustree.buffer((-97,"-97"))
# bplustree.buffer((-96,"-96"))
bplustree.show()
# bplustree.calling_ra()
# bplustree.all_buffer_flush(bplustree.root)

