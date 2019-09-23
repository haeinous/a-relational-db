#!/usr/bin/python3

import csv
import typing
import unittest

from planner import FileScanNode, SelectionNode, ProjectionNode, QueryPlan


class TestFileScanNode(unittest.TestCase):

    def test_file_scan_node(self):
        file_scan_node = FileScanNode()
        self.assertEqual(next(file_scan_node), 'something')


class TestQueryPlan(unittest.TestCase):

    def test_return_id_equals_2_return_name(self):
        def project_first_and_last_name(row) -> str:
            return f'name: {row["first_name"]} {row["last_name"]}'

        def predicate_id_eq_2(row) -> bool:
            return row['id'] == 2

        query_plan = create_query_plan(project_first_and_last_name, predicate_id_eq_2)

        self.assertEqual(next(query_plan), 'name: Nancy Reagan')


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
