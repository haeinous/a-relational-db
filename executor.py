#!/usr/bin/python3

def execute_query(query_plan):
    """
    Given a QueryPlan object, execute the query.
    """
    for record in query_plan:
        yield record
