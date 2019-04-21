
# Find the least weight edge, delete the weight from all the edges in a cycle and create a new graph
def shuffle(cycleNodes):
    weightEdges = []
    lenCycle = len(cycleNodes)
    for i in range(lenCycle):
        weightEdges.append(graph[cycleNodes[i]][cycleNodes[(i + 1) % lenCycle]])
    edgeWeightToRemove = min(weightEdges)
    print edgeWeightToRemove
    for i in range(lenCycle):
        newWeight = graph[cycleNodes[i]][cycleNodes[(i + 1) % lenCycle]] - edgeWeightToRemove
        if newWeight > 0:
            graph[cycleNodes[i]][cycleNodes[(i + 1) % lenCycle]] = newWeight
        else:
            del graph[cycleNodes[i]][cycleNodes[(i + 1) % lenCycle]]
    return graph


# Get all the nodes of the graph
def getNodes(graph):
    return graph.keys()


# Return the children of node
def getEdges(graph, node):
    return graph[node].keys()


def strongly_connected_components(graph):
    """
    Tarjan's Algorithm (named for its discoverer, Robert Tarjan) is a graph theory algorithm
    for finding the strongly connected components of a graph.

    Based on: http://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
    """

    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    result = []

    def strongconnect(node):
        # set the depth index for this node to the smallest unused index
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        # Consider successors of `node`
        try:
            successors = graph[node]
        except:
            successors = []
        for successor in successors:
            if successor not in lowlinks:
                # Successor has not yet been visited; recurse on it
                strongconnect(successor)
                lowlinks[node] = min(lowlinks[node], lowlinks[successor])
            elif successor in stack:
                # the successor is in the stack and hence in the current strongly connected component (SCC)
                lowlinks[node] = min(lowlinks[node], index[successor])

        # If `node` is a root node, pop the stack and generate an SCC
        if lowlinks[node] == index[node]:
            connected_component = []

            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            component = tuple(connected_component)
            # storing the result
            result.append(component)

    for node in graph:
        if node not in lowlinks:
            strongconnect(node)

    return result


def dfs(node, graph, visited=[], path=[]):
    print node
    if node not in visited:
        visited.append(node)
        path = path + [node]
        neighbors = graph.get(node).keys() if graph.get(node) else []
        for neighbor in neighbors:
            cycle = dfs(neighbor, graph, visited, path)
            if cycle:
                return cycle
    else:
        return path + [node]
    return None


graph = {'a': {'b': 3},
         'b': {'c': 2},
         'c': {'d': 5},  # cycle
         'd': {'e': 6, 'a': 2},
         'e': {'g': 2},
         }

# graph1 has a cylce where 'b' comes before 'e' and thus dfs on 'b' takes place first. This graph would fail on the code copied from the ne
graph1 = {'a': {'e': 3},
          'e': {'c': 2},
          'c': {'d': 5},
          'd': {'b': 6, 'e': 2},
          'b': {'g': 2},
          }

##print graph
##while findCycle(graph):
##    print "cycles: %s" % findCycle(graph)
##    g = shuffle(findCycle(graph))
##    graph=g
##    print g

print dfs('a', graph1)
