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
            "!hello" "world"
        ''')

    def test_call(self):
        self.batched('''

            # single call
            x()
            x()

            # bad ident single call
            32()
            "32()"

            # no single call without parens
            x
            "x"

            # one string argument
            x y
            x("y")

            # two string arguments
            x y z
            x("y", "z")

            # delayed fn call
            $x y z
            x y("z")

            # interrupted fn call
            x $y z
            x(y, "z")

            # single num arg
            x 0b_10
            x(0b_10)

            # mixed args
            x y 0b_10
            x("y", 0b_10)

            # nested constructor brackets
            #list [ 1 2 3 ]
            #list([1, 2, 3])
        ''')

    def test_comprehension(self):
        self.batched('''
            # list comprehension, no variables
            [ abc for abc in range 20 ]
            [ "abc" for "abc" in range(20) ]

            # list comprehension, iter variables
            [ abc for $abc in range 20 ]
            [ "abc" for abc in range(20) ]

            # list comprehension, item variables
            [ $abc for abc in range 20 ]
            [ abc for "abc" in range(20) ]

            # list comprehension, both variables
            [ $abc for $abc in range 20 ]
            [ abc for abc in range(20) ]

            # set comprehension, no variables
            { abc for abc in range 20 }
            { "abc" for "abc" in range(20) }

            # set comprehension, iter variables
            { abc for $abc in range 20 }
            { "abc" for abc in range(20) }

            # set comprehension, item variables
            { $abc for abc in range 20 }
            { abc for "abc" in range(20) }

            # set comprehension, both variables
            { $abc for $abc in range 20 }
            { abc for abc in range(20) }
        ''')

    def test_operators(self):
        self.batched('''

            # very prosey
            20 is not None
            20 is not None

            # less prosey
            a20 is not None
            "a20" is not None

            # even less prosey
            a20 is not none
            "a20" is not "none"

            # pretty prosey
            20 not in ( 30 , 40 , 50 )
            20 not in ( 30 , 40 , 50 )
        ''')

if __name__ == '__main__':
    unittest.main()
