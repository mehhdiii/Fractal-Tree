
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

        # Tree variables
        self.order = order
        self.max_children = order
        self.max_keys = order-1 
        self.min_keys = order//2 -1 

        #data variable
        self.keys = []
        self.values = []
        self.leaf = True
        
        #pointers
        self.parent = None
        self.children = [None]*self.order

        #Fractal tree index specific variables
        self.buffer = order//2 # size needs to be corrected later
        self.messages = []

    def update_leaf(self):
        """
        updates the leaf status of a node 
        """
        if [None]*self.order == self.children:
            self.leaf = False



    def is_full(self):
        """Returns True if the node is full."""
        return len(self.keys) == self.order



class FractalTree(object):


    def __init__(self, order=8):
        self.root = Node(order)
        print("Tree created!")



    def _find(self, node, key):
        #### finds the child where key values should move down to  
        pass 




    def add(self, node: Node, key, value): 
        """Adds a key-value pair to the passed node. if node is full, split and perform the necessary steps.
        returns the index at which the value was inserted. 
        """

        #check if tree is empty: 
        if (self.root.keys == []):
            node.keys.append(key)
            node.values.append(value)


        else:

            #search for its place in the node: 
            for indx, k in enumerate(node.keys):
                if (k > key):
                    #insert at this position:
                    node.keys = node.keys[:indx]+[key] + node.keys[indx:]
                    if (node.leaf):
                        node.values = node.values[:indx] + [value] + node.values[indx:]
                    break
                #check if key is even greater than last element: 
                if (indx == len(node.keys)-1 and key >= k ):
                    #add the key to the end of list
                    node.keys.append(key)
                    if (node.leaf):
                        node.values.append(value)
                    break

            
        #now check if the node's space has exceeded
        if len(node.keys) > node.max_keys:
            self.split(node)

         



    def split(self, node: Node):

        """Splits the node into two and stores them as child nodes."""

        center_node_index = node.order//2
        center_key, center_value = node.keys[center_node_index], node.values[center_node_index]

        left = Node(node.order)
        right = Node(node.order)

        #copying data:

        #copy children: 
        left.children = node.children[:center_node_index+1]
        right.children = node.children[center_node_index+1:]
        
        #update thier leaf status
        left.update_leaf()
        right.update_leaf()

        
        #if the node is leaf node, then copy center_node_index to the right_node as well: 
        if(node.leaf): 
            ## add the center key value pair as well into the left and right child along with the right half of it. 
            right.keys, right.values = node.keys[center_node_index+1:], node.values[center_node_index+1:]
            left.keys, left.values = node.keys[:center_node_index], node.values[:center_node_index]
        
        else:
            right.keys, right.values = node.keys[center_node_index:]
            left.keys, left.values = node.keys[:center_node_index]

        

        
        if (node.parent==None): #if the node doesnt have any parent, it means we are at root node


            #make a new node from this center key: 
            new_parent_node = Node(node.order)
            #add the center key to this parent node: 
            new_parent_node.keys.append(center_key) 

            # make left, right the child of new_parent_node: 
            new_parent_node.children[0] = left
            new_parent_node.children[1] = right
            
            # update leaf status: 
            new_parent_node.update_leaf()
            
            #make this node the new root node: 
            self.root = new_parent_node 
            
            #add reference to parent 
            left.parent, right.parent = self.root, self.root


        
        
        elif (node.parent!=None): #if the node has a parent
            #now update the parents children to include left and right nodes 
            parents_children = node.parent.children
            
            #search for node in parents_children
            for indx, n in enumerate(parents_children):
                if (n==node):
                    ##add left and right to indx and indx+1 location in children list 
                    node.parent.children[indx] = left

                    try:
                        node.parent.children[indx+1] = right
                    except:
                        node.parent.children.append(right)


            #add the element to its parent node
            self.add(node.parent, center_key, center_value) 

            


    def insert_msg(self, key, value):
        """
        Inserts a message to insert the key value pair in the tree.
        
        """

        # if buffer is not full, add the msg to buffer
        if(self.root.buffer != len(self.root.messages)):
            print((key, value), ":=", "msg added to buffer!")
            self.root.messages.append(("insert", key, value))

        else:
            ##flush the buffer messages down a level
            print("Buffer full, Flushing")
            self.flush(self.root)
            self.root.messages.append(("insert", key, value))



    def flush(self, node: Node):
        ## flush msgs from node down a level:


        #check if the node is leaf_node: if yes then apply messages
        if (node.leaf == True):

            self.apply_msg(node)
            #all msgs flushed. Now clear the node's buffer messages: 
            node.messages = [] 
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
                self.add(node, key, value)



    # def retrieve(self, key):
    #     """Returns a value for a given key, and None if the key does not exist."""
    #     child = self.root

    #     while not child.leaf:
    #         child, index = self._find(child, key)

    #     for i, item in enumerate(child.keys):
    #         if key == item:
    #             return child.values[i]

    #     return None


    
mytree = FractalTree(4)
# mytree.print_children()
mytree.add(mytree.root, 1, "1")
mytree.add(mytree.root, 4, "4")
mytree.add(mytree.root, 7, "7")
mytree.add(mytree.root, 10,"10")
mytree.add(mytree.root.children[1], 17,"17")
mytree.add(mytree.root.children[1], 21,"21")
mytree.add(mytree.root.children[2], 31,"31")
mytree.add(mytree.root.children[2], 25,"25")
mytree.add(mytree.root.children[2], 19,"19")
mytree.add(mytree.root.children[2], 20,"20")
# mytree.add(6, "panda")
print(mytree.root.values)
    
