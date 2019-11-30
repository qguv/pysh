#!/usr/bin/env python3.8

import unittest
import syntax

class TestSyntax(unittest.TestCase):
    def batched(self, s):
        lines = [line.strip() for line in s.strip().split('\n')]
        lines = [line for line in lines if line]
        for i in range(0, len(lines), 3):
            name, source, expected = lines[i], lines[i+1], lines[i+2]
            source = source.partition('#')[0]
            if not source:
                continue

            name = name.lstrip('#').lstrip()

            with self.subTest(name=name):
                self.assertEqual(syntax.dumps(source), expected)

    def test_quotes(self):
        self.batched('''

            # bare words
            cd newdir
            cd("newdir")

            # single quoted str
            cd '~/new dir'
            cd('~/new dir')

            # double quoted str
            cd "~/new dir"
            cd("~/new dir")

            # single quoted fstr
            cd f'~/new dir'
            cd(f'~/new dir')

            # double quoted fstr
            cd f"~/new dir"
            cd(f"~/new dir")

            # single quoted rstr
            cd r'~/new dir'
            cd(r'~/new dir')

            # double quoted rstr
            cd r"~/new dir"
            cd(r"~/new dir")

            # escaped space
            #cd new\ dir
            #cd("new dir")
        ''')

    def test_numbers(self):
        self.batched('''

            # int zero
            int 0
            int(0)

            # pos int zero
            int +0
            int(+0)

            # neg int zero
            int -0
            int(-0)

            # float zero
            int 0.0
            int(0.0)

            # pos float zero
            int +0.0
            int(+0.0)

            # neg float zero
            int -0.0
            int(-0.0)

            # decimal
            int 0.1
            int(0.1)

            # e
            int 1e1
            int(1e1)

            # hex
            int -0xcafed00d
            int(-0xcafed00d)

            # octal
            int -0o755
            int(-0o755)

            # bad octal
            int 00
            int("00")

            # good dec separator
            int 111_111_111.111_111_111
            int(111_111_111.111_111_111)

            # good hex separator
            int 0x_1
            int(0x_1)

            # good octal separator
            int 0o_1
            int(0o_1)

            # good bin separator
            int 0b_1
            int(0b_1)

            # bad separator
            int _1
            int("_1")

            # ip
            conn 192.168.1.1
            conn("192.168.1.1")
        ''')

    def test_numbers(self):
        self.batched('''

            # good ident
            print hello world
            print("hello", "world")

            # weird good ident
            _1 hello world
            _1("hello", "world")

            # bad number ident
            23 hello world
            23 hello("world")

            # bad string ident
            !hello world
            "!hello" world()
        ''')

if __name__ == '__main__':
    unittest.main()
