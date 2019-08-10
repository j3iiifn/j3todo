#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


class TaskProcessor:
    def __init__(self, args):
        self.in_todo = args.input_todo
        self.out_report = args.output_report
        self.out_todo = args.output_todo

    def add_flag_to_parent(self, node):
        node.flag = True

        if node.parent:
            self.add_flag_to_parent(node.parent)

    def add_flag_to_children(self, node):
        node.flag = True
        node.todo = False

        for c in node.children:
            self.add_flag_to_children(c)

    def check(self, node):
        if node.mark == MARK_DONE:
            # if the node is cleared, its children are also cleared regardless of their mark.
            self.add_flag_to_parent(node)
            self.add_flag_to_children(node)
            return

        for c in node.children:
            self.check(c)

    def print_node(self, node):
        if node.flag:
            print >> self.out_report, node.line

        if node.todo:
            print >> self.out_todo, node.line

        for c in node.children:
            self.print_node(c)

    def finalize(self, root):
        self.check(root)
        self.print_node(root)

    def run(self):

        with open(self.in_todo, 'r') as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]

        root = None
        cursor = None
        prev_level = 0
        for l in content:
            try:
                l_strip = l.lstrip()
                leading_spaces = len(l) - len(l_strip)
                pos_level = leading_spaces / INDENT
                mark = l_strip[0]
                # task = l_strip[1:].lstrip()
                # print "%d, %s, %s, %s" % (pos_level, mark, task, l)
    
                if pos_level == 0:
                    if root:
                        self.finalize(root)
    
                    node = Node(mark, l, None)
                    root = node
    
                elif prev_level == pos_level:
                    node = Node(mark, l, cursor.parent)
                    cursor.parent.children.append(node)
    
                elif prev_level < pos_level:
                    # down 1 level
                    node = Node(mark, l, cursor)
                    cursor.children.append(node)
    
                else:
                    # up 1 level
                    node = Node(mark, l, cursor.parent.parent)
                    cursor.parent.parent.children.append(node)
    
                cursor = node
                prev_level = pos_level
            except:
                print l
                exit(1)

        self.finalize(root)


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
    return parser.parse_args()


def main():
    args = aparse()
    t = TaskProcessor(args)
    t.run()


if __name__ == "__main__":
    main()
