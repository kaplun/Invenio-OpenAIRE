# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2008, 2009, 2010, 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Unit tests for shellutils library."""

__revision__ = "$Id$"

import unittest
import time
import os

from invenio.config import CFG_TMPDIR

from invenio.shellutils import escape_shell_arg, run_shell_command, \
    run_process_with_timeout, Timeout
from invenio.testutils import make_test_suite, run_test_suite

class EscapeShellArgTest(unittest.TestCase):
    """Testing of escaping shell arguments."""

    def test_escape_simple(self):
        """shellutils - escaping simple strings"""
        self.assertEqual("'hello'",
                         escape_shell_arg("hello"))

    def test_escape_backtick(self):
        """shellutils - escaping strings containing backticks"""
        self.assertEqual(r"'hello `world`'",
                         escape_shell_arg(r'hello `world`'))

    def test_escape_quoted(self):
        """shellutils - escaping strings containing single quotes"""
        self.assertEqual("'hello'\\''world'",
                         escape_shell_arg("hello'world"))

    def test_escape_double_quoted(self):
        """shellutils - escaping strings containing double-quotes"""
        self.assertEqual("""'"hello world"'""",
                         escape_shell_arg('"hello world"'))

    def test_escape_complex_quoted(self):
        """shellutils - escaping strings containing complex quoting"""
        self.assertEqual(r"""'"Who is this `Eve'\'', Bob?", asked Alice.'""",
             escape_shell_arg(r""""Who is this `Eve', Bob?", asked Alice."""))

    def test_escape_windows_style_path(self):
        """shellutils - escaping strings containing windows-style file paths"""
        self.assertEqual(r"'C:\Users\Test User\My Documents" \
                          "\funny file name (for testing).pdf'",
                         escape_shell_arg(r'C:\Users\Test User\My Documents' \
                          '\funny file name (for testing).pdf'))

    def test_escape_unix_style_path(self):
        """shellutils - escaping strings containing unix-style file paths"""
        self.assertEqual(r"'/tmp/z_temp.txt'",
                         escape_shell_arg(r'/tmp/z_temp.txt'))

    def test_escape_number_sign(self):
        """shellutils - escaping strings containing the number sign"""
        self.assertEqual(r"'Python comments start with #.'",
                         escape_shell_arg(r'Python comments start with #.'))

    def test_escape_ampersand(self):
        """shellutils - escaping strings containing ampersand"""
        self.assertEqual(r"'Today the weather is hot & sunny'",
                         escape_shell_arg(r'Today the weather is hot & sunny'))

    def test_escape_greater_than(self):
        """shellutils - escaping strings containing the greater-than sign"""
        self.assertEqual(r"'10 > 5'",
                         escape_shell_arg(r'10 > 5'))

    def test_escape_less_than(self):
        """shellutils - escaping strings containing the less-than sign"""
        self.assertEqual(r"'5 < 10'",
                         escape_shell_arg(r'5 < 10'))

class RunShellCommandTest(unittest.TestCase):
    """Testing of running shell commands."""

    def test_run_cmd_hello(self):
        """shellutils - running simple command"""
        self.assertEqual((0, "hello world\n", ''),
                         run_shell_command("echo 'hello world'"))

    def test_run_cmd_hello_args(self):
        """shellutils - running simple command with an argument"""
        self.assertEqual((0, "hello world\n", ''),
                         run_shell_command("echo 'hello %s'", ("world",)))

    def test_run_cmd_hello_quote(self):
        """shellutils - running simple command with an argument with quote"""
        self.assertEqual((0, "hel'lo world\n", ''),
                         run_shell_command("echo %s %s", ("hel'lo", "world",)))

    def test_run_cmd_errorneous(self):
        """shellutils - running wrong command should raise an exception"""
        self.assertRaises(TypeError, run_shell_command,
                          "echo %s %s %s", ("hello", "world",))

class RunProcessWithTimeoutTest(unittest.TestCase):
    """Testing of running a process with timeout."""
    def setUp(self):
        self.script_path = os.path.join(CFG_TMPDIR, 'test_sleeping.sh')
        script = open(self.script_path, 'w')
        print >> script, "#!/bin/sh"
        print >> script, "date"
        print >> script, "echo 'foo'"
        print >> script, "echo 'bar' > /dev/stderr"
        print >> script, "sleep $1"
        print >> script, "date"
        script.close()
        os.chmod(self.script_path, 0700)
        self.python_script_path = os.path.join(CFG_TMPDIR, 'test_sleeping.py')
        script = open(self.python_script_path, 'w')
        print >> script, """\
#!/usr/bin/env python
import os
print os.getpid(), os.getpgrp()
if os.getpid() == os.getpgrp():
    print "PID == PGID"
else:
    print "PID != PGID"
"""
        script.close()
        os.chmod(self.python_script_path, 0700)

    def tearDown(self):
        os.remove(self.script_path)
        os.remove(self.python_script_path)

    def test_run_cmd_timeout(self):
        """shellutils - running simple command with expiring timeout"""
        t1 = time.time()
        self.assertRaises(Timeout, run_process_with_timeout, (self.script_path, '15'), timeout=5)
        self.failUnless(time.time() - t1 < 8, "%s < 8" % (time.time() - t1))

    def test_run_cmd_timeout_no_zombie(self):
        """shellutils - running simple command no zombie"""
        t1 = time.time()
        self.assertRaises(Timeout, run_process_with_timeout, (self.script_path, '15', "THISISATEST"), timeout=5)
        ps_output = run_shell_command('ps aux')[1]
        self.failIf('THISISATEST' in ps_output)
        self.failIf('sleep' in ps_output)

    def test_run_cmd_timeout_no_timeout(self):
        """shellutils - running simple command without expiring timeout"""
        exitstatus, stdout, stderr = run_process_with_timeout([self.script_path, '5'], timeout=10)
        self.failUnless('foo' in stdout)
        self.failUnless('bar' in stderr)
        self.assertEqual(exitstatus, 0)

    def test_run_cmd_timeout_big_stdout(self):
        """shellutils - running simple command with a big standard output"""
        from invenio.config import CFG_PYLIBDIR
        test_file = os.path.join(CFG_PYLIBDIR, 'invenio', 'bibcirculation_templates.py')
        exitstatus, stdout, stderr = run_process_with_timeout(['cat', test_file], timeout=10)
        self.assertEqual(open(test_file).read(), stdout)
        self.assertEqual(exitstatus, 0)

    def test_run_cmd_timeout_pgid(self):
        """shellutils - running simple command should have PID == PGID"""
        exitstatus, stdout, stderr = run_process_with_timeout([self.python_script_path, '5'])
        self.failIf('PID != PGID' in stdout, 'PID != PGID was found in current output: %s (%s)' % (stdout, stderr))
        self.failUnless('PID == PGID' in stdout, 'PID == PGID wasn\'t found in current output: %s (%s)' % (stdout, stderr))

TEST_SUITE = make_test_suite(EscapeShellArgTest,
                             RunShellCommandTest,
                             RunProcessWithTimeoutTest)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)
