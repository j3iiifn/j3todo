#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
import math

INDENT = 4
MARK_DONE = 'x'


class Node:
    def __init__(self, mark, line, parent):
        self.mark = mark
        self.line = line
        self.parent = parent
        self.children = []
        self.flag = False  # print to output_report
        self.todo = True  # print to output_todo

    def __str__(self):
        return "mark=%s, flag=%s, todo=%s, line=%s" % (self.mark, self.flag, self.todo, self.line)


class TaskProcessor:
    def __init__(self, output_report=None, output_todo=None, debug=False):
        self.output_report = output_report
        self.output_todo = output_todo
        self.debug = debug

        self.contents = None

        self.root = Node(None, None, None)
        self.root.flag = False
        self.root.todo = False

        self.completed_lines = []
        self.todo_lines = []

    def add_flag_to_parent(self, node):
        if node == self.root:
            return

        node.flag = True
        if self.debug:
            print("add_flag_to_parent => %s" % node)

        if node.parent:
            self.add_flag_to_parent(node.parent)

    def add_flag_to_children(self, node):
        if node == self.root:
            return

        node.flag = True
        node.todo = False
        if self.debug:
            print("add_flag_to_children => %s" % node)

        for c in node.children:
            self.add_flag_to_children(c)

    def check(self, node=None):
        if not node:
            node = self.root

        if node.mark == MARK_DONE:
            # if the node is cleared, its children are also cleared regardless of their mark.
            self.add_flag_to_parent(node)
            self.add_flag_to_children(node)
            return

        for c in node.children:
            self.check(c)

    def create_completed_lines(self, node=None):
        if not node:
            node = self.root

        if node == self.root:
            self.completed_lines = []

        if node.flag:
            self.completed_lines.append(node.line)

        for c in node.children:
            self.create_completed_lines(c)

    def create_todo_lines(self, node=None):
        if not node:
            node = self.root

        if node == self.root:
            self.todo_lines = []

        if node.todo:
            self.todo_lines.append(node.line)

        for c in node.children:
            self.create_todo_lines(c)

    def finalize(self):
        self.check(self.root)
        self.create_completed_lines()
        print('\n'.join(self.completed_lines), file=self.output_report)
        self.create_todo_lines()
        print('\n'.join(self.todo_lines), file=self.output_todo)

    def read_from(self, input_todo):
        with open(input_todo, 'r') as f:
            self.contents = f.readlines()
        self.contents = [x.rstrip() for x in self.contents]

    def run(self):
        prev_node = None
        prev_level = 0

        for l in self.contents:
            try:
                l_strip = l.lstrip()
                if not l_strip:
                    # blank line
                    continue

                leading_spaces = len(l) - len(l_strip)
                pos_level = math.floor(leading_spaces / INDENT)
                mark = l_strip[0]
                parent = None

                if self.debug:
                    task = l_strip[1:].lstrip()
                    print("%d, %s, %s, %s" % (pos_level, mark, task, l))
    
                if pos_level == 0:
                    parent = self.root
    
                elif prev_level == pos_level:
                    parent = prev_node.parent
    
                elif prev_level < pos_level:
                    # down 1 level
                    parent = prev_node
    
                else:
                    # up 1 or more levels
                    parent = prev_node.parent
                    for i in range(prev_level - pos_level):
                        parent = parent.parent

                pos_node = Node(mark, l, parent)
                parent.children.append(pos_node)

                prev_node = pos_node
                prev_level = pos_level

            except Exception as e:
                print(l, file=sys.stderr)
                import traceback
                print(traceback.format_exc(), file=sys.stderr)
                exit(1)


def aparse():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_todo',
        help='todo.txt'
    )
    parser.add_argument(
        'output_report', type=argparse.FileType('w'),
        help='daily_report.txt'
    )
    parser.add_argument(
        'output_todo', type=argparse.FileType('w'),
        help='todo.txt'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='Debug option.'
    )
    return parser.parse_args()

def print_node(node):
    if node.children:
        print('-----')

    print("%s => %s" % (node.parent, node))

    for c in node.children:
        print_node(c)

def main():
    args = aparse()
    t = TaskProcessor(args.output_report, args.output_todo, args.debug)
    t.read_from(args.input_todo)
    t.run()
    t.finalize()

    if args.debug:
        print_node(t.root)


if __name__ == "__main__":
    main()
