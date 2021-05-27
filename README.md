# Fractal Tree 

Fractal Tree Index implementation in Python. 

## Description

This repository contains an implementation of Fractal Tree Index. These indexes are built up on B+ Trees and provide faster insertion speeds. The following two classes are the principle components of the implementation: 

## Class Node()

Each node stores keys and values. Keys are not unique to each value, and as such values are stored as a list under each key.

### Attributes:

`order (int)` : The maximum number of keys each node can hold.

`keys (List)`:  Contains the list of all keys at a Node. 

`values (List)`: Contains a list of all values (if leaf is True) or else a list of child objects of type `FractalTree` of the Node.  

`parent (FractalTree Object)`: Stores the parent `FractalTree` Object of the Node. 

`leaf (bool)`: True if Node is a leaf Node, False otherwise. (True by default). 

`buffer (List)`: Contains the list of all messages buffered in Node. Size of buffer equals `order//2`. 

### Methods:

#### `add_to_buffer(self, message)`:

adds an insert/delete message to the self node's buffer.    

**Return value**: 

If: the buffer is full, return `None` 

else: returns the message itself

#### `add(self, key, value)`:

Adds a key-value pair to the node.

**Return value**: `None`

#### `split(self)`:

Splits the node into two and stores them as child nodes.

**Return value:** `None`

#### `is_full(self)`:

Returns True if the node is full.

**Return type:** bool

#### `show(self, counter=0)`:

Prints the keys at each level.

**Return type:** `None`



## Class FractalTree()

Fractal Tree object, consisting of nodes. Adheres to the self balancing property. Nodes split automatically into two once full. After a split, the center of split **floats** upward to be inserted in the parent node (merge).

### Attributes:

`root (Node)`: Stores the root node of the Tree (Contains empty `Node` object by default). 

### Methods:

#### `_find(self, node, key)`:

For a given node and key, returns the index where the key should be inserted and the child/value at that index.

**Return Type:** a `list` of two items of the following type: [`Node` or `int`, `int`]

#### `_merge(self, parent, child, index)`:

For a parent and child node, extract a pivot from the child to be inserted into the keys of the parent. Insert the values from the child into the values of the parent.

**Return Type:** `None`

#### `insert(self, parent_node: Node, leaf_node: Node, key, value)`:

Inserts a key-value pair to a leaf node. If the leaf node is full, split the leaf node into two. This method can be called from within the class's apply_message() method. 

**Inputs:** 

`parent_node`: parent of the leaf node

`leaf_node`: The leaf node on which to insert key, value

`key`: The key of the data

`value`: Data value corresponding to the key

**Return Type:** `None`

#### `retrieve(self, key)`:

Returns a value for a given key, and None if the key does not exist.

**Return Type:** `Node` Object or `None` if key doesn't exist

#### `show(self)`:

Prints the keys at each level.

**Return Type:** `None`

#### `search_retrieval(self, key)`:

Searches for a key value in the tree along with its buffers. 

**Return Type:** a list containing key and value of the used data type.

#### `buffer(self,message)`:

Buffers an incoming message of insert/delete to Tree.

**Return Type:** `None`

#### `flush(self, node: Node)`:

Flushes messages in the node's buffer down a level. 

**Return Type:** `None`

#### `apply_msg(self, node)`:

Applies the insert/delete message on the -> node. 

**Return Type:** `None`

#### `search(self, key)`:

Searches for a key value in the tree. 

**Return Type:** leaf node object of `Node` type that contains the key. 

#### `delete(self, key, value)`:

search and find the leaf node where the value may exists

**Return Type:** `None` 



## Dependencies

This project was built on Python 3.9.0 64-bit. No external dependences and libraries used.  



# How To Use Our implementation

The implementation is stored on FractalTree.py file. The Data is stored as python List, enabling the tree to be compatible across data types. 
The following steps must be followed to utilize the tree for creating an index: 

#### Create a Tree object: 

To create a tree object, use the following syntax: 

```python
tree = FractalTree(order)
```

where `order` is the order of Nodes in the tree.

#### Insert Data in the tree:

To insert data in the tree, a key, value pair must be passed to the `FractalTree.buffer()` method. If the data is not in a (key, value) format, use the python builtin `Hash` Method to generate a key for your data point. 

Once data is in a (key, value) pair, use the following syntax for insertion: 

```python
message = (key, value, "insert")
tree.buffer(message)
```

#### Retrieve Data from the Tree:

To retrieve stored data from the tree, call the `FractalTree.search_retrieval` Method. The method can be called as follows: 

```python
tree.search_retrieval(key)
```

#### Delete Data from Tree:

Deletion follows a similar syntax to insertion. There are two methods to delete from the tree.

##### Method 1: 

Call the `FractalTree.delete` Method directly: 

```python
tree.delete(key)
```

##### Method 2 (Beta):

Push a delete message to the tree using the `FractalTree.buffer` Method: 

```
message = (key, "delete")
tree.buffer(message)
```

