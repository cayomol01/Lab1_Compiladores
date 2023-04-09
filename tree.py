from InfixPostfix import InfixPostfix

class Node():
    def __init__(self, name, value=None, left=None, right=None):
        self.name = name
        self.value = value
        self.left = left
        self.right = right
        self.firstPosition = self.getFirstPos()
        self.lastPosition = self.getLastPos()
        self.nullable = self.getNullable()
        self.followPos = None
        self.setFollowPos()

    def traverse(self):
        nodes_to_visit = [self]
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop(0)
            if current_node.left:
                nodes_to_visit.append(current_node.left)
            if current_node.right:
                nodes_to_visit.append(current_node.right)
            print(current_node.followPos)

    def getNodes(self):
        nodes_to_visit = [self]
        nodes = [self]
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop(0)
            if current_node.left:
                nodes_to_visit.append(current_node.left)
            if current_node.right:
                nodes_to_visit.append(current_node.right)
            nodes.append(current_node)
        return nodes

    def getFirstPos(self):
        symbol = self.name
        firstPosition = set()
        if symbol == "*":
            firstPosition = self.left.firstPosition
        elif symbol == "|":
            firstPosition.update(self.left.firstPosition)
            firstPosition.update(self.right.firstPosition)
        elif symbol == ".":
            firstPosition.update(self.left.firstPosition)
            if self.left.nullable == True:
                firstPosition.update(self.right.firstPosition)
        else:
            firstPosition = {self.value}
        return firstPosition


    def getLastPos(self):
        symbol = self.name
        lastPosition = set()
        if symbol == "*":
            lastPosition.update(self.left.lastPosition)
        elif symbol == "|":
            lastPosition.update(self.right.lastPosition)
            lastPosition.update(self.left.lastPosition)
        elif symbol == ".":
            lastPosition.update(self.right.lastPosition)
            if self.right.nullable == True:
                lastPosition.update(self.left.lastPosition)
        else:
            lastPosition = {self.value}
        return lastPosition
    
        
    def getNullable(self):
        symbol = self.name
        nullable = None
        if symbol == "*":
            nullable = True
        elif symbol == "|":
            nullable = self.left.nullable or self.right.nullable
        elif symbol == ".":
            nullable = self.left.nullable and self.right.nullable
        else:
            nullable = False
        return nullable
    
    def setFollowPos(self):
        symbol = self.name
        lastpos = self.lastPosition
        
        if symbol == "*":
            lastpos = self.lastPosition
            for i in lastpos:
                nodes_to_visit = [self]
                while len(nodes_to_visit) > 0:
                    current_node = nodes_to_visit.pop(0)
                    if current_node.value == i:
                        current_node.followPos.update(self.firstPosition)
                    if current_node.left:
                        nodes_to_visit.append(current_node.left)
                    if current_node.right:
                        nodes_to_visit.append(current_node.right)
                        
        elif symbol == ".":
            lastpos = self.left.lastPosition
            for i in lastpos:
                nodes_to_visit = [self]
                while len(nodes_to_visit) > 0:
                    current_node = nodes_to_visit.pop(0)
                    if current_node.value == i:
                        current_node.followPos.update(self.right.firstPosition)
                    if current_node.left:
                        nodes_to_visit.append(current_node.left)
                    if current_node.right:
                        nodes_to_visit.append(current_node.right)
                
        elif symbol == "+":
            lastpos = self.lastPosition
            for i in lastpos:
                nodes_to_visit = [self]
                while len(nodes_to_visit) > 0:
                    current_node = nodes_to_visit.pop(0)
                    if current_node.value == i:
                        current_node.followPos.update(self.firstPosition)
                    if current_node.left:
                        nodes_to_visit.append(current_node.left)
                    if current_node.right:
                        nodes_to_visit.append(current_node.right)
                        
        elif symbol not in ["*", "+", ".", "|"]:
            self.followPos = set()

                
            
    def getTable(self):
        nodes = self.getNodes()
        table = []
        for i in nodes:
            if i.value:
                table.append((i.name, i.value, i.followPos))

        table = sorted(table, key=lambda x: x[1])
        return table
        
        
def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        if node.value:
            print(' ' * 4 * level + '-> ' + str(node.name))
        else:
            print(' ' * 4 * level + '-> ' + str(node.name))
        printTree(node.right, level + 1)

        
    
def augmentedRegex(regex):
    return regex+"#"

def CreateSyntaxTree(regex):
    reg = augmentedRegex(regex)
    postfix = InfixPostfix(reg)
    
    stack = []
    node_count = 1
    for token in postfix:
        if token == '*':
            child = stack.pop()
            node = Node(token, left=child)
            stack.append(node)
        elif token == '+':
            child = stack.pop()
            node = Node(token, left=child)
            stack.append(node)
        elif token == '.':
            right_child = stack.pop()
            left_child = stack.pop()
            node = Node(token, left=left_child, right=right_child)
            stack.append(node)
        elif token == '|':
            right_child = stack.pop()
            left_child = stack.pop()
            if len(stack) > 0 and stack[-1].value == '|':
                # If the previous operator was also an alternation,
                # group the current expression with the previous right child
                prev_node = stack.pop()
                prev_node.right = Node(token, left=prev_node.right, right=right_child)
                stack.append(prev_node)
            else:
                node = Node(token, left=left_child, right=right_child)
                stack.append(node)
        else:
            node = Node(token, value=node_count)
            stack.append(node)
            node_count += 1
    
    return stack.pop()


            
    