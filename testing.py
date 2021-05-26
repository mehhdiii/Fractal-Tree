"""Simple implementation of a B+ tree, a self-balancing tree data structure that (1) maintains sort
data order and (2) allows insertions and access in logarithmic time.
"""

import math


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
        self.BUFFER_SIZE = order//2
        self.dict={}


        # #check if the node is leaf_node: if yes then apply messages
        # if (node.leaf == True):


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
               
    

class FractalTree(object):
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
        child/value at that index."""
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
        This method can be called from within the class's apply_message() method
        """

        #Inputs: 
        #parent_node: parent of the leaf node
        #leaf_node: The leaf node on which to insert key, value
        #key: The key of the data
        #value: Data value corresponding to the key

        
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
            #if output is not None, it means the buffer is full and root is not leaf. 
            if output!=None: 
                self.flush(self.root)
    

    def flush(self, node: Node):
        """flushes msgs in the node's buffer down a level"""
        

        #check if the node is leaf_node: if yes then apply messages
        # if (node.leaf == True):
        #     self.apply_msg(node)
        #     #all msgs flushed. Now clear the node's buffer messages: 
        #     node.buffer= [] 
        #     return 


        ## else traverse the messages in buffer and flush them down
        for msg in node.buffer:

            #else check which child the message should traverse down to
            key, value = msg[0], msg[1]


            child,indx = self._find(node,key)
            
            #copy message to childs buffer
            child.add_to_buffer(msg)

            #check if the child is leaf, if yes then apply the message: 
            if(child.leaf):
                self.apply_msg(child)


            # If child is not a child, then check if childs buffer is full 
            elif len(child.buffer)>=child.BUFFER_SIZE:
                #flush and then add the message
                self.flush(child)
            
            # else: # if not leaf and buffer also not full, then just write the message to child
            #     if msg not in child.buffer:
            #         child.add_to_buffer(msg)

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





    def search(self, key):
        """
        Searches for a key value in the tree

        Return value: 
        leaf node object that contains the key"""

        #store the root node
        current_node = self.root
        #recursively traverse until a leaf is reached
        while(current_node.leaf == False):
            #traverse on the keys of the non-leaf node to find next child
            temp2 = current_node.keys
            for i in range(len(temp2)):
                if (key == temp2[i]):
                    #if the key is found, traverse to its right child 
                    current_node = current_node.values[i + 1]
                    break
                elif (key < temp2[i]):
                    #if key is less than the node.key, goto left child 
                    current_node = current_node.values[i]
                    break
                elif (i + 1 == len(current_node.keys)):
                    #if key is not found and end of node reached, goto right child 
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

    # Delete a node
    def delete(self, key, value):
        
        # search and find the leaf node where the value may exists
        node_ = self.search(key)

        exists = 0 #flag to indicate whether the value exists.  
        for i, item in enumerate(node_.values):
            if item == value:
                exists = 1
                if node_ == self.root:
                    node_.values.pop(i)
                    node_.keys.pop(i)
                else:
                    node_.keys.pop(i)
                    node_.values.pop(i)
                    self.deleteEntry(node_, value, key)
        if not exists:
            print("Value not in Tree")
            return

    # Delete an entry
    def deleteEntry(self, node_, value, key):
        if not node_.leaf:
            for i, item in enumerate(node_.keys):
                if item == key:
                    node_.keys.pop(i)
                    break
            for i, item in enumerate(node_.values):
                if item == value:
                    node_.values.pop(i)
                    break

        if self.root == node_ and len(node_.keys) == 1:
            self.root = node_.keys[0]
            node_.keys[0].parent = None
            del node_
            return
        elif (len(node_.keys) < int(math.ceil(node_.order / 2)) and node_.leaf == False) or (len(node_.values) < int(math.ceil((node_.order - 1) / 2)) and node_.leaf == True):

            is_predecessor = 0
            parentNode = node_.parent
            PrevNode = -1
            NextNode = -1
            PrevK = -1
            PostK = -1
            for i, item in enumerate(parentNode.keys):

                if item == node_:
                    if i > 0:
                        PrevNode = parentNode.keys[i - 1]
                        PrevK = parentNode.values[i - 1]

                    if i < len(parentNode.keys) - 1:
                        NextNode = parentNode.keys[i + 1]
                        PostK = parentNode.values[i]

            if PrevNode == -1:
                ndash = NextNode
                value_ = PostK
            elif NextNode == -1:
                is_predecessor = 1
                ndash = PrevNode
                value_ = PrevK
            else:
                if len(node_.values) + len(NextNode.values) < node_.order:
                    ndash = NextNode
                    value_ = PostK
                else:
                    is_predecessor = 1
                    ndash = PrevNode
                    value_ = PrevK

            if len(node_.values) + len(ndash.values) < node_.order:
                if is_predecessor == 0:
                    node_, ndash = ndash, node_
                ndash.keys += node_.keys
                if not node_.leaf:
                    ndash.values.append(value_)
                else:
                    ndash.nextKey = node_.nextKey
                ndash.values += node_.values

                if not ndash.leaf:
                    for j in ndash.keys:
                        j.parent = ndash

                self.deleteEntry(node_.parent, value_, node_)
                del node_
            else:
                if is_predecessor == 1:
                    if not node_.leaf:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm_1 = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [value_] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                p.values[i] = ndashkm_1
                                break
                    else:
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [ndashkm] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(p.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm
                                break
                else:
                    if not node_.leaf:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [value_]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [ndashk0]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndash.values[0]
                                break

                if not ndash.leaf:
                    for j in ndash.keys:
                        j.parent = ndash
                if not node_.leaf:
                    for j in node_.keys:
                        j.parent = node_
                if not parentNode.leaf:
                    for j in parentNode.keys:
                        j.parent = parentNode
        



import random

bplustree = FractalTree(order=8)
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
bplustree.buffer((-2,"3"))
bplustree.buffer((-200,"2"))
bplustree.buffer((-100,"5"))
bplustree.buffer((-97,"3"))
bplustree.buffer((-96,"2"))
bplustree.show()
# bplustree.calling_ra()
# bplustree.all_buffer_flush(bplustree.root)
