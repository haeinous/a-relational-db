"""
Implement a Scan node that yields a single record each time its next method is called, as well as 
a Selection node initialized with a predicate function (one which returns true or false), which yields
the next record for which the predicate function returns true whenever its own next method is called.
"""

class QueryPlan:

    """
    Tree-like object returned by the query planner that the query exeuctor
    takes during initialization in order to actually execute the query.
    """

    def __init__(self, root_node):
        self.root = root_node


class QueryPlanNode:

    """
    Nodes that make up the query plan
    """

    pass
