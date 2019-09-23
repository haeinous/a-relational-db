import csv
import typing

from planner import FileScanNode, SelectionNode, ProjectionNode, QueryPlan

def process_data_as_list(csv_filename: str) -> typing.List[dict]:
    """
    Given a csv file name, process the data in to a list of dictionaries.
    """
    data_as_list_of_dicts = []

    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            data_as_list_of_dicts.append(row)
    
    return data_as_list_of_dicts


def create_query_plan(projection_function, predicate_function):
    """
    Given two functions, it generates a three-node query plan.
    """
    # Generate the nodes
    file_scan_node = FileScanNode()
    selection_node = SelectionNode(predicate_function)
    selection_node.add_child(file_scan_node)
    projection_node = ProjectionNode(projection_function)  # this will be the root node
    projection_node.add_child(selection_node)

    return QueryPlan(projection_node)
