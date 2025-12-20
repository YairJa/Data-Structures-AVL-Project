
"""A class represnting a node in an AVL tree"""
from inspect import stack

class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.isVirtual = False

    def updateHeight(self):
        # time complexity O(1)
        self.height = (max(self.left.height, self.right.height)) + 1

    def balanceFactor(self):
        # time complexity O(1)

        return self.left.height - self.right.height

    def findMin(self):
        # gets a root and return the minimal node in this subtree
        # time complexity O(self.height) = O(logn)
        current = self
        if(current.is_real_node()):

            while current.left.is_real_node():
                current = current.left
            return current
        else:
            return current

    def findMax(self):
        # gets a root and return the maximal node in this subtree
        # time complexity O(self.height) = O(logn)
        current = self
        if(current.is_real_node()):
            while current.right.is_real_node():
                current=current.right
            return current
        else:
            return current


    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        # time complexity O(1)
        return not self.isVirtual



"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):

        self.virtual = AVLNode(None, None)
        self.virtual.isVirtual = True
        self.root = self.virtual
        self.max = None
        self.min = None
        self.Treesize = 0

    def createByRoot(self, rootNode):
    # specific helper function for split
    ## assumes self is an empty AVL tree, updating only its root to rootNode
    ## time complexity O(1)
        if(rootNode.is_real_node()):
            self.root = rootNode
            self.root.parent = self.virtual

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def search(self, key):
        # function search key in the AVL
        # time complexity O(h) = O(logn)
        e = 1
        node = self.root
        return self.searchFromNode(node, key, e)

    def searchFromNode(self, node, key, e):
        ## helper func to combine search from specified Node downwards until reaching key or virtual
        # time complexity O(node.height) = O(logn)
        while node.is_real_node():  # regular algorithem to search key in BST + e counting
            if node.key == key:
                return (node, e)
            elif node.key < key:
                node = node.right
                e += 1
            else:
                node = node.left
                e += 1
        return (None, e)

    """searches for a node in the dictionary corresponding to the key, starting at the max

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def finger_search(self, key):
        # search key in AVL tree starting from the maximal node
        # time complexity O(h) = O(logn) using helper functions

        if (self.root.is_real_node()):
            e = 1
            node = self.max
            node, e = self.fingerDownwardStart(key, e)  # step 1, find spot to start moving downwards

            return self.searchFromNode(node, key, e)  # regular search downwards
        else:  # special case, tree is empty
            return (None, 1)

    def fingerDownwardStart(self, key, e):
        # helper for finger functions.
        # Search from maximal node, return Node to start search downward to find key
        # complexity O(h) = O(logn)
        node = self.max
        while ((self.root is not node) and (node.key > key)):
            node = node.parent
            e += 1
        if ((node is self.root) and (node.key > key)) or (node is self.max):
            return (node, e)  ## cases we haven't repeated an edge on the route
        return (node, e - 2)

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    def insert(self, key, val):
        # insert Node(key, value) to an AVL tree
        # time complexity O(h) = O(logn) using helper functions
        node = AVLNode(key, val)
        node.height = 0
        current = self.root  ## physical creation
        self.Treesize += 1  ## of the Node
        node.left = self.virtual
        node.right = self.virtual

        e = 2

        if not self.root.is_real_node():  # special case, tree was empty
            node.parent = self.virtual
            self.root = node
            self.max = node
            self.min = node
            return (node, 1, 0)
        else:

            return self.insertHelper(current, node, e)

    def insertHelper(self, current, node, e):
        # helper func, unites node insert process from specified Node current downwards
        # time complexity O(h) = O(logn)
        Hcounter = 0
        while True:  # find the place to allocate the new node
            if current.key > node.key:  # node correct position in current left subtree
                if current.left.is_real_node():  # left move is to a real Node
                    current = current.left
                    e += 1
                else:
                    left = True  # place for insert, found, we are the left son of our father
                    break
            else:  # node correct position in current right subtree
                if current.right.is_real_node():  # right move is to a real Node
                    current = current.right
                    e += 1
                else:
                    left = False  # place for insert, found, we are the right son of our father
                    break
        node.parent = current  # adjust pointers from + to new Node
        if left:
            current.left = node
        else:
            current.right = node

        Hcounter = self.rotationsCheck(current, Hcounter, True)

        if (self.max.key < node.key):  ## adjust max/min nodes if necessary
            self.max = node
        if (self.min.key > node.key):
            self.min = node
        return (node, e, Hcounter)

    def rotateR(self, A):
        # function adjust pointers for Right rotation
        # time complexity O(1)
        B = A.left
        if (self.root is A):
            self.root = B
        else:
            if (A.parent.right is A):
                A.parent.right = B
            else:
                A.parent.left = B
        B.parent = A.parent
        A.parent = B
        A.left = B.right
        if (B.right.is_real_node()):
            B.right.parent = A
        B.right = A
        A.updateHeight()
        B.updateHeight()

    def rotateL(self, A):
        # function adjust pointers for Left rotation
        # time complexity O(1)
        B = A.right
        if (self.root is A):
            self.root = B
        else:
            if (A.parent.right is A):
                A.parent.right = B
            else:
                A.parent.left = B
        B.parent = A.parent
        A.parent = B
        A.right = B.left
        if (B.left.is_real_node()):
            B.left.parent = A
        B.left = A
        A.updateHeight()
        B.updateHeight()

    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    def finger_insert(self, key, val):
        # insert Node (key, value) in AVL tree starting from the maximal node
        # time complexity O(h) = O(logn) using helper functions
        node = AVLNode(key, val)
        node.height = 0
        self.Treesize += 1  ## physical creation
        node.left = self.virtual  ## of the node
        node.right = self.virtual

        e = 2

        if not self.root.is_real_node():  # special case, tree was empty
            node.parent = self.virtual
            self.root = node
            self.max = node
            self.min = node
            return (node, 1, 0)
        else:
            current, e = self.fingerDownwardStart(key, e)  ## find place to start searching downwards
            return self.insertHelper(current, node, e)  ## find place to allocate and preform the insert

    def isLeaf(self, node):
        # check if both of his son are vituals
        # time complexity O(1)
        return not (node.left.is_real_node() or node.right.is_real_node())

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
        # delete node from AVL tree. assumes node is in self
        # time complexity O(h) = O(logn) using helper functions
        if (self.max.key == node.key):  ## adjust max/min nodes if necessary
            self.max = self.predecessor(node)
        if (self.min.key == node.key):
            self.min = self.successor(node)
        self.Treesize -= 1
        ## differ physical Node removal and Pointers adjustment based on Node type of sons
        if self.isLeaf(node):  # no sons case
            if node.parent.left is node:
                node.parent.left = self.virtual
            elif node.parent.right is node:
                node.parent.right = self.virtual
            else:  # is also the root
                self.root = self.virtual
            current = node.parent
        elif not node.left.is_real_node():  ## has only right son
            self.selectedNode_father_sub_connection(node, node.parent, node.right)
            current = node.parent
        elif not node.right.is_real_node():  # has only left son
            self.selectedNode_father_sub_connection(node, node.parent, node.left)
            current = node.parent
        else:  # has two sons
            successorNode = self.successor(node)
            if (node.right is successorNode):  # successor is direct child of node
                current = successorNode
                successorNode.left = node.left  # update the left side
                node.left.parent = successorNode
                self.selectedNode_father_sub_connection(node, node.parent, node.right)

            else:  # the regular successor option, minimal in right subtree
                current = successorNode.parent
                successorNode.parent.left = successorNode.right
                if (successorNode.right.is_real_node()):
                    successorNode.right.parent = current

                successorNode.left = node.left  ## successor takes
                successorNode.right = node.right  ## node sons
                node.right.parent = successorNode  ## node sons
                node.left.parent = successorNode  ##changes their parent
                self.selectedNode_father_sub_connection(node, node.parent, successorNode)
                successorNode.updateHeight()

        self.rotationsCheck(current, 0, False)  ## rotation check from the node physically removes

        return

    def rotationsCheck(self, current, Hcounter, insert):
        # helper functions verify rotation by the algorithem from certain Node current upwards
        # boolean insert for break possibility in case 3
        # time complexity O(currentDepth) = O(logn)

        while current.is_real_node():  # search for possible BF violation by known algorithem
            previousHeight = current.height
            current.updateHeight()
            BF = current.balanceFactor()
            if ((previousHeight == current.height) and (abs(BF) < 2)):  ## case 1, Immediate termination
                break
            elif ((previousHeight != current.height) and (abs(BF) < 2)):  ## case 2, continue check upwards
                Hcounter += 1
                current = current.parent
            else:  ## case 3, rotation then terminate depend on insert
                temp = current.parent
                if BF == 2:  ## 4 BF violation options
                    BFChild = current.left.balanceFactor()
                    if BFChild == -1:
                        self.rotateL(current.left)
                        self.rotateR(current)
                    else:
                        self.rotateR(current)
                else:
                    BFChild = current.right.balanceFactor()
                    if BFChild == 1:
                        self.rotateR(current.right)
                        self.rotateL(current)

                    else:
                        self.rotateL(current)
                if (insert):  ## insert require 1 rotation at most
                    break
                else:
                    current = temp
        return Hcounter

    def selectedNode_father_sub_connection(self, node, father, subNode):
        ## helper function, assumes node.parent = father, adjust pointers between father and subNode
        ## subNode replaces node
        # time complexity O(1)
        if father.left is node:  # the usual checking of the father
            father.left = subNode
            subNode.parent = father
        elif father.right is node:
            father.right = subNode
            subNode.parent = node.parent
        else:  # is root
            subNode.parent = self.virtual
            self.root = subNode

    def successor(self, node):
        # helper function, finds successor of node in the AVL tree self
        # time complexity O(logn)
        if (node.right.is_real_node()):  ## case successor is minimal node in right subtree
            node = node.right
            node = node.findMin()
        else:
            prev = node
            node = node.parent
            while ((node.is_real_node()) and (prev is node.right)):  # case successor is first time
                prev = node  # were coming from left child
                node = node.parent
        return node

    def predecessor(self, node):
        # helper function, finds predecessor of node in the AVL tree self
        # time complexity O(logn)
        if (node.left.is_real_node()):  ## case predecessor is maximal node in left subtree
            node = node.left
            node = node.findMax()
        else:
            prev = node
            node = node.parent
            while ((node.is_real_node()) and (prev is node.left)):  # case predecessor is first time
                prev = node  # were coming from right child
                node = node.parent
        return node

    """joins self with item and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separting self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """

    def join(self, tree2, key, val):
        ## function joins tree2 into self using mediator Node(key,val)
        # time complexity O(logn)
        self.Treesize += +tree2.Treesize + 1  # updating size
        x = AVLNode(key, val)  # creating node
        x.right = x.left = x.parent = self.virtual
        if tree2.root.height < self.root.height:  # join by allocating tree2 as subtree for self
            self.genericJoin(self, tree2, x)

        elif tree2.root.height > self.root.height:  # join by allocating self as subtree for tree2
            self.genericJoin(tree2, self, x)
            self.root = tree2.root
        else:
            if (self.root.is_real_node()):  ## special case, x becomes root with self and tree 2 as subtrees
                self.genericJoin(tree2, self, x)
                self.root = x
            else:  ## special case, both trees are empty
                self.root, self.max, self.min = x, x, x

        x.updateHeight()
        self.rotationsCheck(x.parent, 0, False)  # balancing the tree

        return

    def genericJoin(self, big, small, x):
        # gets a big height tree and a small base on their heights , x is the node to connect between
        # time complexity O(logn)
        hSmall = small.root.height

        current = big.root  ## pointer for the current node
        if not small.root.is_real_node():  # special case, small is an empty tree

            x.height = 0
            if x.key > big.root.key:  # insert x as big new maximal node
                maxNode = big.root.findMax()
                x.parent = maxNode
                maxNode.right = x
                self.max = x  # adjusting self fields accordingly
                self.min = big.min
            else:  # insert x as big new minimal node
                minNode = big.root.findMin()
                x.parent = minNode
                minNode.left = x
                self.min = x  ## adjusting self fields accordingly
                self.max = big.max
        elif big.root.key > x.key:  # means small will be in his left subtree
            self.min = small.min
            self.max = big.max
            x.left = small.root

            small.root.parent = x

            while (current.height > hSmall) and (current.left.is_real_node()):
                # reaching the same height subtree root

                current = current.left
            if current.height > hSmall:  ## special case, small height<=0, big.min has right child,
                # avoiding arrival to virtual node
                current.left = x
                x.parent = current

            else:
                x.right = current
                x.parent = current.parent

                if current.parent.is_real_node():
                    current.parent.left = x
                current.parent = x

        else:  # means small will be in his right subtree
            self.min = big.min
            self.max = small.max
            x.right = small.root
            small.root.parent = x
            while (current.height > hSmall) and (current.right.is_real_node()):
                # reaching the same height subtree root
                current = current.right
            if current.height > hSmall:  ## special case, small height<=0, big.min has right child,
                # avoiding arrival to virtual node
                current.right = x
                x.parent = current

            else:
                x.left = current
                x.parent = current.parent

                if current.parent.is_real_node():
                    current.parent.right = x
                current.parent = x

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """

    def split(self, node):
        # delete node from the tree and return two subtress , one bigger values, other smaller values
        # size field invariant isnt correct after calling this method
        # time complexity O(logn)
        smallerTree = AVLTree()
        smallerTree.createByRoot(node.left)
        biggerTree = AVLTree()
        biggerTree.createByRoot(node.right)
        while node.key != self.root.key:

            uniteTree = AVLTree()
            if (node.parent.right is node):  # smaller  values tree Accumulation

                uniteTree.createByRoot(node.parent.left)

                smallerTree.join(uniteTree, node.parent.key, node.parent.value)
            else:  # bigger values tree Accumulation
                uniteTree.createByRoot(node.parent.right)
                biggerTree.join(uniteTree, node.parent.key, node.parent.value)

            node = node.parent
        smallerTree.max = smallerTree.root.findMax()
        smallerTree.min = smallerTree.root.findMin()
        biggerTree.max = biggerTree.root.findMax()
        biggerTree.min = biggerTree.root.findMin()
        return smallerTree, biggerTree

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        # regular InOrder tree walk
        # time complexity O(n)
        res = []

        def avlToArrayRec(node):
            # inner function preforming the recursion
            if not node.is_real_node():
                return
            avlToArrayRec(node.left)
            res.append((node.key, node.value))
            avlToArrayRec(node.right)

        if (self.root.is_real_node()):
            avlToArrayRec(self.root)
        return res

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """

    def max_node(self):
        # time complexity O(1) return field
        return self.max

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        # time complexity O(1) return field
        return self.Treesize

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        # time complexity O(1) return field
        return self.root

    """returns the root of the tree representing the dictionary
    @rtype: AVLNode
    """
