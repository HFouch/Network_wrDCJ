from Class_wrDCJ_Node import Node
import networkx as nx


class Network:

    def __init__(self, start_node, target_node, adjacenciesB):
        self.hash_table = {}
        self.start_node = start_node
        self.target_node = target_node
        self.adjacenciesB = adjacenciesB

        hash_key_start = hash(str(self.start_node.state))
        hash_key_target = hash(str(self.target_node.state))
        self.hash_table.update({hash_key_start: self.start_node})
        self.hash_table.update({hash_key_target: self.target_node})
        self.level = 0

        # Build network

    def build_hash_table(self, current_node):
        node = current_node
        print()
        print()
        print('current node and state: ')
        print(node)
        print(node.state)
        print('____________________________________________________________________________________')

        #if the genome has a circular intermediate (i.e all of its children will be linear)
        if node.next_operation != 0:
            print('this genome has a circular intermediate')
            print('the op wieight is: ', node.next_operation_weight)
            operations = []
            # if point of cut = previous point of join:
            if node.next_operation_weight == 0.5:

                operations.append(node.next_operation)
                print('legal, operations: ', operations)

            elif node.next_operation_weight == 1.5:
                operations = []
                if type(node.next_operation) is list:
                    for operation in node.next_operation:
                        operations.append(operation)
                else:
                    operations.append(node.next_operation)
                print('illigal, operations: ', operations)

            else:
                print('You have got a problem with the .next_operation weights')

            for operation in operations:
                print('the operation: ', operation)
                child_state = node.take_action(operation)
                print('result of op: ', child_state)
                check_hash_table = Network.check_hash_key(self, child_state)

                if check_hash_table[0]:
                    child = check_hash_table[1]
                    node.children.append(child)
                    node.children_weights.append(node.next_operation_weight)

                else:
                    #remember the child will consist of linear chromosomes only because it is the result of a forced reinsertion
                    child = Node(child_state)
                    hash_key = hash(str(child.state))
                    self.hash_table.update({hash_key: child})
                    # print('#T: ', self.hash_table)
                    node.children.append(child)
                    node.children_weights.append(node.next_operation_weight)
                    print('node children: ', node.children)
                    print('node children weigths', node.children_weights)
                    Network.build_hash_table(self, child)


        #if the genome has no circular intermediates (i.e. some of its children may have circular chromosomes)
        else:

            operations = node.get_legal_operations(self.adjacenciesB)
            print('Operations: ', operations)
            for operation in operations:

                child_state = node.take_action(operation)
                print('operations - result: ', operation, ' - ', child_state)
                check_hash_table = Network.check_hash_key(self, child_state)

                if check_hash_table[0]:
                    child = check_hash_table[1]
                    node.children.append(child)
                    child.find_chromosomes(child.state)
                    if len(child.circular_chromosomes) != 0 :
                        node.children_weights.append(0.5)
                    else:
                        node.children_weights.append(1)

                else:
                    child = Node(child_state)

                    # check whether a circular chromosome has been created
                    child.find_chromosomes(child.state)


                    # if a circular chromosome has been created:
                    if len(child.circular_chromosomes) != 0:

                        legal_operation = child.get_legal_reinsertion_operation(operation, self.adjacenciesB)
                        print()
                        print('!!!!!!!!!!!!!!!!', legal_operation)
                        print()
                        if legal_operation:
                            child.next_operation = legal_operation
                            child.next_operation_weight = 0.5
                            hash_key = hash(str(child.state))
                            self.hash_table.update({hash_key: child})
                            # print('#T: ', self.hash_table)
                            node.children.append(child)
                            node.children_weights.append(0.5)
                            print('node children: ', node.children)
                            print('node.children weigths: ', node.children_weights)
                            Network.build_hash_table(self, child)
                        else:
                            child.next_operation = child.get_illegal_decircularization_operation(self.adjacenciesB)
                            print('the ilegal next operation: ', child.state)
                            print('illegal op: ', child.next_operation)
                            child.next_operation_weight = 1.5
                            hash_key = hash(str(child.state))
                            self.hash_table.update({hash_key: child})
                            # print('#T: ', self.hash_table)
                            node.children.append(child)
                            node.children_weights.append(0.5)
                            print('node children: ', node.children)
                            print('node.children weigths: ', node.children_weights)
                            Network.build_hash_table(self, child)

                        '''
                            
                        print('a cicular chromosome has been formed')

                        # potential_operation = False
                        # get legal reinsertion operation
                        for adjacency in operation[-1]:
                            if adjacency in child.circular_chromosomes[0]:
                                circular_join = adjacency
                                potential_operation = child.check_if_operation_exists(circular_join, self.adjacenciesB)
                                # print('legal op: ', potential_operation)

                                # if the a legal operation exists:

                                if potential_operation:
                                    print('there is a legal op for: ', child.state)
                                    print('legal op: ', potential_operation)

                                    child.next_operation = potential_operation
                                    child.next_operation_weight = 0.5
                                    hash_key = hash(str(child.state))
                                    self.hash_table.update({hash_key: child})
                                    # print('#T: ', self.hash_table)
                                    node.children.append(child)
                                    node.children_weights.append(0.5)
                                    print('node children: ', node.children)
                                    print('node.children weigths: ', node.children_weights)
                                    Network.build_hash_table(self, child)
                                    print()

                                # else if there exists no legal reinsertion operation
                                else:
                                    print('there was no legal op')

                        child.next_operation = child.get_illegal_decircularization_operation(self.adjacenciesB)
                        print('the ilegal next operation: ', child.state)
                        print('illegal op: ', child.next_operation)
                        child.next_operation_weight = 1.5
                        hash_key = hash(str(child.state))
                        self.hash_table.update({hash_key: child})
                        # print('#T: ', self.hash_table)
                        node.children.append(child)
                        node.children_weights.append(0.5)
                        print('node children: ', node.children)
                        print('node.children weigths: ', node.children_weights)
                        Network.build_hash_table(self, child)

                        # if not potential_operation:
                        #   child.next_operation = child.get_decircularization_operation(self.adjacenciesB)
                        #  child.next_operation_weight = 1.5
                        #  hash_key = hash(str(child.state))
                        #  self.hash_table.update({hash_key: child})
                        #  # print('#T: ', self.hash_table)
                        #  node.children.append(child)
                        #  node.children_weights.append(0.5)
                        #  Network.build_hash_table(self, child)
                        #  print()

                    '''
                    # else if no circular chromosome has been created:
                    else:
                        print('no cicular chrms')
                        hash_key = hash(str(child.state))
                        self.hash_table.update({hash_key: child})
                        # print('#T: ', self.hash_table)
                        node.children.append(child)
                        node.children_weights.append(1)
                        print('node children: ', node.children)
                        print('node.children weigths: ', node.children_weights)
                        Network.build_hash_table(self, child)



    def check_hash_key(self, child_state):
        key = hash(str(child_state))
        if key in self.hash_table.keys():
            return True, self.hash_table.get(key)
        return False, None

    def build_network(self):
        network = nx.DiGraph()
        nodes = []
        weighted_edges = []
        weights = []

        Network.build_hash_table(self, self.start_node)
        list_of_values = self.hash_table.values()
        for value in list_of_values:
            if value not in nodes:
                nodes.append(value)
        for node in nodes:
            network.add_node(node)
        for node in nodes:

            #for child in node.children:
             #   network.add_edge(node, child)

            for i in range(0, len(node.children)):
                weighted_edges.append((node, node.children[i], node.children_weights[i]))
                weights.append(node.children_weights[i])

        network.add_weighted_edges_from(weighted_edges)
        print()
        print("EDGES")
        print(network.edges)
        print()


        return network

    def get_all_shortest_paths(self, network, start_node, target_node):
        #network = Network.build_network(self)
        all_paths = nx.all_simple_paths(network, start_node, target_node)
        return all_paths