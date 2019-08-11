#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import daily_report

class TestTaskProcessor(unittest.TestCase):
    def _run(self, input, expected_report, expected_todo):
        t = daily_report.TaskProcessor()
        t.contents = input.split('\n')
        t.run()
        t.check()

        t.create_completed_lines()
        self.assertEqual(expected_report, '\n'.join(t.completed_lines))

        t.create_todo_lines()
        self.assertEqual(expected_todo, '\n'.join(t.todo_lines))

    def test_noone_completed(self):
        input='''
- 1
    - 1.1
    - 1.2
        - 1.2.1
        - 1.2.2
- 2
- 3
'''.strip()

        expected_report='''
'''.strip()

        expected_todo='''
- 1
    - 1.1
    - 1.2
        - 1.2.1
        - 1.2.2
- 2
- 3
'''.strip()

        self._run(input, expected_report, expected_todo)

    def test_go_up_2_levels(self):
        input='''
x 1
    x 1.1
    x 1.2
        x 1.2.1
        x 1.2.2
- 2
'''.strip()

        expected_report='''
x 1
    x 1.1
    x 1.2
        x 1.2.1
        x 1.2.2
'''.strip()

        expected_todo='''
- 2
'''.strip()

        self._run(input, expected_report, expected_todo)

    def test_print_parent_to_report(self):
        input='''
- 1
    - 1.1
    - 1.2
        x 1.2.1
        - 1.2.2
- 2
'''.strip()

        expected_report='''
- 1
    - 1.2
        x 1.2.1
'''.strip()

        expected_todo='''
- 1
    - 1.1
    - 1.2
        - 1.2.2
- 2
'''.strip()

        self._run(input, expected_report, expected_todo)

    def test_close_parent(self):
        input='''
x 1
    - 1.1
    - 1.2
        - 1.2.1
        - 1.2.2
- 2
'''.strip()

        expected_report='''
x 1
    - 1.1
    - 1.2
        - 1.2.1
        - 1.2.2
'''.strip()

        expected_todo='''
- 2
'''.strip()

        self._run(input, expected_report, expected_todo)

    def test_go_up_1_level(self):
        input='''
- 1
    x 1.1
    x 1.2
        x 1.2.1
        x 1.2.2
    - 1.3
'''.strip()

        expected_report='''
- 1
    x 1.1
    x 1.2
        x 1.2.1
        x 1.2.2
'''.strip()

        expected_todo='''
- 1
    - 1.3
'''.strip()

        self._run(input, expected_report, expected_todo)

if __name__ == "__main__":
    unittest.main()
