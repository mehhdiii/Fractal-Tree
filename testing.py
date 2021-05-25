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
        self.leaf = True
        self.buffer=[]
        self.dict={}
    def add_buffer(self,message):
        if len(self.buffer)==self.order:
            # print("overflow")
            self.buffer.append(message)
            
            return message
        else:
            # print("adding to buffer")
            self.buffer.append(message)
            # print(self.buffer)
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

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

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

    def insert(self, key, value):
        """Inserts a key-value pair after traversing to a leaf node. If the leaf node is full, split
        the leaf node into two.
        """
        parent = None
        child = self.root

        # Traverse tree until leaf node is reached.
        while not child.leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)

        # If the leaf node is full, split the leaf node into two.
        if child.is_full():
            child.split()

            # Once a leaf node is split, it consists of a internal node and two leaf nodes. These
            # need to be re-inserted back into the tree.
            if parent and not parent.is_full():
                self._merge(parent, child, index)
    
        
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
        output=self.root.add_buffer(message)
        if output!=None:
            self.flush(self.root)
    
    def all_buffer_flush(self,node):
        if node.leaf==False:
            self.flush(node)
            for i in node.keys:
                child=node
                child,ind=self._find(child,i)
                self.all_buffer_flush(child)
        else:
            return
            #still working on it
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
            child=node
            child,indx = self._find(child,key)
            # print ("going to "+str(child.keys))
            if len(child.buffer)==node.order:
                self.flush(child)
            #check if this childs buffer is full: 
            # if (len(node.children[loc].messages) == len(node.children[loc].buffer)):
                #if full, then flush this child first: (recursively)
                
            else:
                #add the message to this child
                if msg not in child.buffer:
                    child.add_buffer(msg)

        #all msgs flushed. Now clear the node's buffer messages: 
        node.messages = [] 


            

                
                

    def apply_msg(self, node):
        for msg in node.buffer:
            command = msg[0]
            
            if command =="insert":
                key, value = msg[1], msg[2]
                ## insertion code goes here
                self.add(node, key, value)



bplustree = BPlusTree(order=4)
bplustree.insert(1,"1")
bplustree.insert(4, "4")
bplustree.insert(7, "7")
bplustree.insert(10,"10")
bplustree.insert (17,"17")
bplustree.insert(21,"21")
bplustree.insert(31,"name")
bplustree.insert(25,"25")
bplustree.insert(19,"19")
bplustree.insert(20,"20")
bplustree.insert(28,"28")
bplustree.insert(42,"42")
# bplustree.buffer((15,"15"))
# bplustree.buffer((41,"41"))

# bplustree.buffer((5,"5"))
# bplustree.buffer((3,"3"))
# bplustree.buffer((2,"2"))
bplustree.show()
# bplustree.calling_ra()
bplustree.all_buffer_flush(bplustree.root)