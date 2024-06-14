from unittest import TestCase

from uel.brainfuck import Brainfuck

import contextlib
import io

class TestBrainFuck(TestCase):
    def test_simple(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            Brainfuck.run("""+++++++++
[->++++++++<]
>.[[-]<]
++++++++++
[->++++++++++<]
>+.[[-]<]
+++++++++
[->++++++++++++<]
>.[[-]<]
+++++++++
[->++++++++++++<]
>.[[-]<]
+++++++++
[->++++++++++++<]
>+++.[[-]<]
++++++++
[->++++<]
>.[[-]<]
++++++++
[->+++++++++++<]
>-.[[-]<]
+++++++++
[->++++++++++++<]
>+++.[[-]<]
+++++++++
[->++++++++++++<]
>++++++.[[-]<]
+++++++++
[->++++++++++++<]
>.[[-]<]
++++++++++
[->++++++++++<]
>.[[-]<]
++++++++
[->++++<]
>+.[[-]<]""")
        self.assertEqual(stdout.getvalue(), "Hello World!")
