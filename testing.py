"""Simple implementation of a B+ tree, a self-balancing tree data structure that (1) maintains sort
data order and (2) allows insertions and access in logarithmic time.
"""

class Node(object):
    """Base node object.
    Each node stores keys and values. Keys are not unique to each value, and as such values are
    stored as a list under each key.
    Attributes:
        order (int): The maximum number of keys each node can hold.
    """
    def __init__(self, order):
        """Child nodes can be converted into parent nodes by setting self.leaf = False. Parent nodes
        simply act as a medium to traverse the tree."""
        self.order = order
        self.keys = []
        self.values = []
        self.parent = None
        self.leaf = True
        self.buffer=[]
        self.BUFFER_SIZE = 1
        self.dict={}


    def add_to_buffer(self,message):
        """adds an insert/delete message to the self node's buffer. 
        
        Return values: 
        If: the buffer is full, return None 
        else: returns the message itself
        """ 

        if len(self.buffer)==self.BUFFER_SIZE: # If buffer is full, return the message as an indication 
            self.buffer.append(message)    
            return message 
        
        else: #if buffer is not full, return None. 
            self.buffer.append(message)
            return None

    def add(self, key, value):
        """Adds a key-value pair to the node."""
        # If the node is empty, simply insert the key-value pair.
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            # If new key matches existing key, add to list of values.
            if key == item:
                self.values[i].append(value)
                break

            # If new key is smaller than existing key, insert new key to the left of existing key.
            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            # If new key is larger than all existing keys, insert new key to the right of all
            # existing keys.
            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    def split(self):
        """Splits the node into two and stores them as child nodes."""
        left = Node(self.order)
        right = Node(self.order)
        mid = self.order // 2

        left.parent = self
        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        right.parent = self
        right.keys = self.keys[mid:]
        right.values = self.values[mid:]

        # When the node is split, set the parent key to the left-most key of the right child node.
        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False
    

    def is_full(self):
        """Returns True if the node is full."""
        return len(self.keys) == self.order

    def val(self):
        if self.leaf:
            for ind,i in enumerate(self.keys):
                self.dict[i]=self.keys[ind]
                # return [self.keys,self.values]
            return self.dict
        else:
            for item in self.values:
                self.dict.update(item.val())
            return self.dict 

    def show(self, counter=0):
        """Prints the keys at each level."""
        print(counter, str(self.keys))

        # Recursively print the key of child nodes (if these exist).
        if not self.leaf:
            for item in self.values:
                item.show(counter + 1)
               
    

class BPlusTree(object):
    """B+ tree object, consisting of nodes.
    Nodes will automatically be split into two once it is full. When a split occurs, a key will
    'float' upwards and be inserted into the parent node to act as a pivot.
    Attributes:
        order (int): The maximum number of keys each node can hold.
    """
    def __init__(self, order=8):
        self.root = Node(order)
        self.dict={}

    
    def _find(self, node, key):
        """ For a given node and key, returns the index where the key should be inserted and the
        list of values at that index."""
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i

        return node.values[i + 1], i + 1

    def _merge(self, parent, child, index):
        """For a parent and child node, extract a pivot from the child to be inserted into the keys
        of the parent. Insert the values from the child into the values of the parent.
        """
        parent.values.pop(index)
        pivot = child.keys[0]

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, parent_node: Node, leaf_node: Node, key, value):
        """Inserts a key-value pair to a leaf node. If the leaf node is full, split
        the leaf node into two.
        """
        # parent = None
        # child = self.root

        # # Traverse tree until leaf node is reached.
        # while not child.leaf:
        #     parent = child
       

        
        leaf_node.add(key, value)

        # If the leaf node is full, split the leaf node into two.
        if leaf_node.is_full():
            leaf_node.split()

            # Once a leaf node is split, it consists of a internal node and two leaf nodes. These
            # need to be re-inserted back into the tree.
            if parent_node and not parent_node.is_full():
                #find out the index at which leaf_node is stored in parent 
                child, index = self._find(leaf_node, key)
                #merge the parent and leaf node 
                self._merge(parent_node, leaf_node, index)
    
        
    def retrieve(self, key):
        """Returns a value for a given key, and None if the key does not exist."""
        child = self.root

        while not child.leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]

        return None

    def calling_ra(self):
      return(self.root.val())

    
    def show(self):
        """Prints the keys at each level."""
        self.root.show()


    def buffer(self,message):
        """Buffers an incoming message of insert/delete to Tree.""" 
        
        # add the message to the root node
        output = self.root.add_to_buffer(message)

        #if the root node is a leaf node, directly apply the message: 
        if (self.root.leaf):
            self.apply_msg(self.root)
            return 
        
        else:
            #if output is not None, it means the buffer is full. 
            if output!=None: 
                self.flush(self.root)
    
    # def all_buffer_flush(self,node):
    #     if node.leaf==False:
    #         self.flush(node)
    #         for i in node.keys:
    #             child=node
    #             child,ind=self._find(child,i)
    #             self.all_buffer_flush(child)
    #     else:
    #         return
    #         #still working on it

    
    def flush(self, node: Node):
        ## flush msgs from node down a level:
        

        #check if the node is leaf_node: if yes then apply messages
        if (node.leaf == True):
            self.apply_msg(node)
            #all msgs flushed. Now clear the node's buffer messages: 
            node.buffer= [] 
            return 

        ## else traverse the messages in buffer and flush them down
        for msg in node.buffer:

            #else check which child the message should traverse down to
            key, value = msg[0], msg[1]

            child,indx = self._find(node,key)
            
            #copy message to childs buffer
            child.add_to_buffer(msg)

            # check if childs buffer is full 
            if len(child.buffer)>=child.BUFFER_SIZE:
                #flush and then add the message
                self.flush(child)
            
                
            else:
                #add the message to this child
                if msg not in child.buffer:
                    child.add_to_buffer(msg)

        #all msgs flushed. Now clear the node's buffer messages: 
        node.buffer = [] 


            

                
                

    def apply_msg(self, node):
        """Applies the insert/delete message on the -> node"""
        for msg in node.buffer:

            command = "insert" #hardcoding command for now
            
            if command =="insert":
                key, value = msg[0], msg[1]
                ## insertion code goes here
                self.insert(node.parent,node, key, value)
        
        #now clear the buffer: 
        node.buffer = []

import random

bplustree = BPlusTree(order=4)
for i in range(1000):
    x = random.randint(1, 1000)
    bplustree.buffer((x, str(i)))
# bplustree.buffer((1,"1"))
# bplustree.buffer((4, "4"))
# bplustree.buffer((7, "7"))
# bplustree.buffer((10,"10"))
# bplustree.buffer((17,"17"))
# bplustree.buffer((21,"21"))
# bplustree.buffer((31,"name"))
# bplustree.buffer((25,"25"))
# bplustree.buffer((19,"19"))
# bplustree.buffer((20,"20"))
# bplustree.buffer((28,"28"))
# bplustree.buffer((42,"42"))
# bplustree.buffer((15,"15"))
# bplustree.buffer((41,"41"))

# bplustree.buffer((5,"5"))
# bplustree.buffer((3,"3"))
# bplustree.buffer((2,"2"))
bplustree.show()
# bplustree.calling_ra()
# bplustree.all_buffer_flush(bplustree.root)