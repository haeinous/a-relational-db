# #!/usr/bin/python3
# TODO: This was an attempt at using StopIteration (currently I return False if there are no more records)
# """
# Implement a Scan node that yields a single record each time its next method is called, as well as
# a Selection node initialized with a predicate function (one which returns true or false), which yields
# the next record for which the predicate function returns true whenever its own next method is called.
# """
#
# import csv
# import typing
# import unittest
#
#
# def execute_query(query_plan):
#     """
#     Given a QueryPlan object, execute the query.
#     """
#     for record in query_plan:
#         if record is not None:
#             yield record
#
#
# class QueryPlan:
#     """
#     Tree-like object returned by the query planner that the query exeuctor
#     takes during initialization in order to actually execute the query.
#     """
#
#     def __init__(self, root_node):
#         self.root = root_node
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         next_record = next(self.root)
#         if not next_record:
#             return
#
#         return next_record
#
#
# class PlanNode:
#     """
#     Nodes that make up the query plan
#     """
#
#     def __init__(self):
#         self.children = []
#
#     def add_child(self, child_node):
#         self.children.append(child_node)
#
#     def __repr__(self):
#         class_name = type(self)
#         return f'[Node: {class_name}]'
#
#
# class ProjectionNode(PlanNode):
#     """
#     Node that projects the data into the format requested by the query.
#     """
#
#     def __init__(self, projection_function):
#         super().__init__()
#         self.projection_function = projection_function
#
#     # def __iter__(self):
#     #     return self
#
#     def __next__(self):
#         return self.projection_function(next(self.children[0]))
#
#
# class SelectionNode(PlanNode):
#     """
#     Node that checks whether the row being examined meets query criteria.
#     """
#
#     def __init__(self, predicate_function):
#         super().__init__()
#         self.predicate_function = predicate_function
#
#     # def __iter__(self):
#     #     return self
#
#     def __next__(self):
#         next_row = next(self.children[0])
#
#         while not self.predicate_function(next_row):
#             # print('[Select] predicate function not satisfied')
#             next_row = next(self.children[0])
#             try:
#                 predicate_func_result = self.predicate_function(next_row)
#             except TypeError:
#                 break
#
#             if predicate_func_result:
#                 break
#
#         return next_row
#
#
# class FileScanNode(PlanNode):
#     """
#     Node that returns each row of the relation.
#     """
#     # TODO: Write an __init__ method that retrieves the data from the db and place it into a list of dicts, with each
#     #       dict representing a single row
#     def __init__(self):
#         super().__init__()
#         data_list = process_data_as_list('test_data.csv')[:3]  # TODO: Don't hard-code data ingestion
#         self.data = iter(data_list)
#         self.num_rows = len(data_list)
#         self.count = 0
#
#     # def __iter__(self):
#     #     return self.data
#
#     def __next__(self):
#         # print('[Scan] called')
#         if self.count < self.num_rows:
#             self.count += 1
#             for row in self.data:
#                 return row
#
#
# class IndexScanNode(PlanNode):
#     """
#     Node that performs an index scan.
#     """
#
#     pass  # TODO: implement me
#
#
# # Test utility functions #######################################
# def process_data_as_list(csv_filename: str) -> typing.List[dict]:
#     """
#     Given a csv file name, process the data in to a list of dictionaries.
#     """
#     data_as_list_of_dicts = []
#
#     with open(csv_filename) as f:
#         reader = csv.DictReader(f)
#
#         for row in reader:
#             data_as_list_of_dicts.append(row)
#
#     return data_as_list_of_dicts
#
#
# def create_query_plan(projection_function, predicate_function):
#     """
#     Given two functions, it generates a three-node query plan.
#     """
#     selection_node = SelectionNode(predicate_function)
#     selection_node.add_child(FileScanNode())
#     projection_node = ProjectionNode(projection_function)  # this will be the root node
#     projection_node.add_child(selection_node)
#
#     return QueryPlan(projection_node)
#
#
# def project_first_and_last_name(row) -> str:
#     return f'name: {row["first_name"]} {row["last_name"]}'
#
#
# def predicate_if_id_eq_2(row) -> bool:
#     print(f"predicate func is returning {row.get('id') == '2'}")
#     return row.get('id') == '2'
#
# def predicate_generator(column_name: str, operator: str, value: str):
#     if operator == 'eq':
#         return lambda x: x[column_name] == value
#     elif operator == 'not_eq':
#         return lambda x: x[column_name] != value
#     elif operator == 'gt':
#         return lambda x: x[column_name] > value
#     elif operator == 'lt':
#         return lambda x: x[column_name] < value
#     else:
#         print('something is wrong with the predicate function')
#         return lambda x: False
#
# # Actual tests #######################################
# class TestPlanner(unittest.TestCase):
#
#     def test_file_scan_node(self):
#         file_scan_node = FileScanNode()
#         self.assertIsInstance(file_scan_node, FileScanNode)
#
#         self.assertEqual(next(file_scan_node)['first_name'], 'Bob')
#         self.assertEqual(next(file_scan_node)['first_name'], 'Nancy')
#         self.assertEqual(next(file_scan_node)['first_name'], 'Bruce')
#         self.assertFalse(next(file_scan_node))
#
#     def test_selection_node(self):
#         selection_node = SelectionNode(predicate_generator('id', 'eq', '1'))
#         selection_node.add_child(FileScanNode())
#         self.assertEqual(next(selection_node)['first_name'], 'Bob')
#         self.assertIsNone(next(selection_node))
#
#         selection_node = SelectionNode(predicate_generator('id', 'not_eq', '2'))
#         selection_node.add_child(FileScanNode())
#         self.assertEqual(next(selection_node)['first_name'], 'Bob')
#         self.assertEqual(next(selection_node)['first_name'], 'Bruce')
#         self.assertIsNone(next(selection_node))
#
#         selection_node = SelectionNode(predicate_generator('id', 'eq', '5'))  # does not exist
#         selection_node.add_child(FileScanNode())
#         self.assertIsNone(next(selection_node))
#
#     def test_projection_node(self):
#         projection_node = ProjectionNode(project_first_and_last_name)
#         selection_node = SelectionNode(predicate_generator('id', 'eq', '2'))
#         selection_node.add_child(FileScanNode())
#         projection_node.add_child(selection_node)
#         self.assertEqual(next(projection_node), 'name: Nancy Reagan')
#         self.assertFalse(next(projection_node))
#
#         projection_node = ProjectionNode(project_first_and_last_name)
#         selection_node = SelectionNode(predicate_generator('id', 'gt', '1'))
#         selection_node.add_child(FileScanNode())
#         projection_node.add_child(selection_node)
#         self.assertEqual(next(projection_node), 'name: Nancy Reagan')
#         self.assertEqual(next(projection_node), 'name: Bruce Maslin')
#         self.assertFalse(next(projection_node))
#
#     def test_query_plan(self):
#         query_plan = create_query_plan(project_first_and_last_name, predicate_generator('id', 'eq', '2'))
#         self.assertEqual(next(query_plan), 'name: Nancy Reagan')
#         self.assertFalse(next(query_plan))
#
#         query_plan = create_query_plan(project_first_and_last_name, predicate_generator('first_name', 'not_eq', 'Coco'))
#         self.assertEqual(next(query_plan), 'name: Bob Long')
#         self.assertEqual(next(query_plan), 'name: Nancy Reagan')
#         self.assertEqual(next(query_plan), 'name: Bruce Maslin')
#         self.assertFalse(next(query_plan))
#
#     def test_query_executor(self):
#         query_plan = create_query_plan(project_first_and_last_name, predicate_generator('id', 'eq', '2'))
#         self.assertListEqual(list(execute_query(query_plan)), ['name: Nancy Reagan'])
#
#         query_plan = create_query_plan(project_first_and_last_name, predicate_generator('id', 'eq', '5'))
#         self.assertListEqual(list(execute_query(query_plan)), [])
#
#         query_plan = create_query_plan(project_first_and_last_name, predicate_generator('id', 'gt', '1'))
#         self.assertListEqual(list(execute_query(query_plan)), ['name: Nancy Reagan', 'name: Bruce Maslin'])
