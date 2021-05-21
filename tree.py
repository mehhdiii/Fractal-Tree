# import math
# class Tree:
#     def __init__(self): 
#         pass

#     def search(self, item): 
#         pass

#     def insert(self, item): 
#         pass

#     def remove(self, item): 
#         pass
    
#     def is_empty(self): 
#         pass

#     def size(self): 
#         pass

# class node: 
#     """
#         Each node stores key value pair (not unique). In case of same keys, the values are stored as list

#         Attributes: 
#         order := Max number of keys in the node.
#         leaf := True if the node is a leaf node
#         Buffer_size := size of the Buffer 
#     """
#     def __init__(self, order):
#         self.order = order
#         self.BUFFER_SIZE = math.sqrt(order)
#         self.keys = []
#         self.values = []
#         self.leaf = False
    
#     def add()






class Node(object):
    """Base node object.
    Each node stores keys and values. Keys are not unique to each value, and as such values are
    stored as a list under each key.
    Attributes:
        order (int): The maximum number of keys each node can hold.
        buffer (int): The maximum number of messages each node can hold.
    """
    def __init__(self, order):
        """Child nodes can be converted into parent nodes by setting self.leaf = False. Parent nodes
        simply act as a medium to traverse the tree."""
        print("Node created")
        self.order = order
        self.buffer = order # size needs to be corrected later
        self.messages = []
        self.keys = []
        self.values = []
        self.leaf = True
        self.children = []


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
        print("Tree created!")



    def print_children(self):
        print(self.root.children)



    def _find(self, node, key):
        #### finds the child where key values should move down to  
        pass 

        # """ For a given node and key, returns the index where the key should be inserted and the
        # list of values at that index."""
        # for i, item in enumerate(node.keys):
        #     if key < item:
        #         return node.values[i], i

        # return node.values[i + 1], i + 1

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
        # if buffer is not full, add the msg to buffer
        if(self.root.buffer != len(self.root.messages)):
            print((key, value), ":=", "msg added to buffer!")
            self.root.messages.append(("insert", key, value))

        else:
            ##flush the buffer messages down a level
            print("Buffer full, Flushing")
            self.flush(self.root)


            



        # """Inserts a key-value pair after traversing to a leaf node. If the leaf node is full, split
        # the leaf node into two.
        # """
        # parent = None
        # child = self.root

        # # Traverse tree until leaf node is reached.
        # while not child.leaf:
        #     parent = child
        #     child, index = self._find(child, key)

        # child.add(key, value)

        # # If the leaf node is full, split the leaf node into two.
        # if child.is_full():
        #     child.split()

        #     # Once a leaf node is split, it consists of a internal node and two leaf nodes. These
        #     # need to be re-inserted back into the tree.
        #     if parent and not parent.is_full():
        #         self._merge(parent, child, index)

    def flush(self, node: Node):
        ## flush msgs from node down a level:


        #check if the node is leaf_node: if yes then apply messages
        if (node.leaf == True):
            self.apply_msg(node)
            return 

        ## else traverse the messages in buffer and flush them down
        for msg in node.messages:

            #else check which child the message should traverse down to
            key, value = msg[1], msg[2]
            loc = self._find(key, value)

            #check if this childs buffer is full: 
            if (len(node.children[loc].messages) == len(node.children[loc].buffer)):
                #if full, then flush this child first: (recursively)
                self.flush(node.children[loc])
            else:
                #add the message to this child
                node.messages.append(msg)

        #all msgs flushed. Now clear the node's buffer messages: 
        node.messages = [] 


            

                
                

    def apply_msg(self, node):
        for msg in node.messages:
            command = msg[0]
            
            if command =="insert":
                key, value = msg[1], msg[2]
                ## insertion code goes here








    def retrieve(self, key):
        """Returns a value for a given key, and None if the key does not exist."""
        child = self.root

        while not child.leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i]

        return None

    def show(self):
        """Prints the keys at each level."""
        self.root.show()

# def demo_node():
#     print('Initializing node...')
#     node = Node(order=4)

#     print('\nInserting key a...')
#     node.add('a', 'alpha')
#     print('Is node full?', node.is_full())
#     node.show()

#     print('\nInserting keys b, c, d...')
#     node.add('b', 'bravo')
#     node.add('c', 'charlie')
#     node.add('d', 'delta')
#     print('Is node full?', node.is_full())
#     node.show()

#     print('\nSplitting node...')
#     node.split()
#     node.show()

# def demo_bplustree():
#     print('Initializing B+ tree...')
#     bplustree = BPlusTree(order=4)

#     print('\nB+ tree with 1 item...')
#     bplustree.insert('a', 'alpha')
#     bplustree.show()

#     print('\nB+ tree with 2 items...')
#     bplustree.insert('b', 'bravo')
#     bplustree.show()

#     print('\nB+ tree with 3 items...')
#     bplustree.insert('c', 'charlie')
#     bplustree.show()

#     print('\nB+ tree with 4 items...')
#     bplustree.insert('d', 'delta')
#     bplustree.show()

#     print('\nB+ tree with 5 items...')
#     bplustree.insert('e', 'echo')
#     bplustree.show()

#     print('\nB+ tree with 6 items...')
#     bplustree.insert('f', 'foxtrot')
#     bplustree.show()

#     print('\nRetrieving values with key e...')
#     print(bplustree.retrieve('e'))

# if __name__ == '__main__':
#     demo_node()
#     print('\n')
#     demo_bplustree()
    
mytree = BPlusTree(4)
mytree.print_children()
mytree.insert(2, "panda")
mytree.insert(3, "panda")
mytree.insert(4, "panda")
mytree.insert(5, "panda")
mytree.insert(6, "panda")
    
