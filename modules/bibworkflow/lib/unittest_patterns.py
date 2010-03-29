# -*- coding: utf8 -*-
import unittest
import sys
import os
import time
import random

p = os.path.abspath(os.path.dirname(__file__) + '/../')
if p not in sys.path:
    sys.path.append(p)

from engine import GenericWorkflowEngine
import patterns.controlflow as cf

def i(key):
    def _i(obj, eng):
        obj.insert(0, key)
    return _i

def a(key):
    def _a(obj, eng):
        obj.append(key)
    return _a

def printer(val):
    def _printer(obj, eng):
        lock = eng.getVar('lock')
        end = time.time() + .2
        w = float(random.randint(1, 5)) / 100
        i = 0
        while i < 5:
            try:
                lock.acquire()
                obj.append(val)
            finally:
                lock.release()
            time.sleep(w)
            i += 1
    return _printer



class TestGenericWorkflowEngine(unittest.TestCase):
    """Tests of the WE interface"""

    def setUp(self):
        self.key = '*'

    def tearDown(self):
        pass

    def getDoc(self, val=None):
        if val:
            return [[x] for x in val.split()]
        return [[x] for x in u"one two three four five".split()]

    def addTestCallbacks(self, no, eng):
        if type == 1:
            eng.addManyCallbacks()

    # --------- initialization ---------------

    def test_IF_ELSE01(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()

        we.setWorkflow([i('add'),
                        cf.IF_ELSE(lambda o,e: o[1] == 'three',
                                   [a('3'), a('33')],
                                   [a('other'), [a('nested'), a('branch')]] ),
                        a('end')])
        we.process(doc)

        r = [' '.join(doc[x]) for x in range(len(doc))]

        assert r[0] == 'add one other nested branch end'
        assert r[1] == 'add two other nested branch end'
        assert r[2] == 'add three 3 33 end'
        assert r[3] == 'add four other nested branch end'
        assert r[4] == 'add five other nested branch end'


    def test_IF_ELSE02(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()

        we.setWorkflow([i('add'),
                        cf.IF_ELSE(lambda o,e: o[1] == 'three',
                                   a('3'),
                                   a('other'))
                        ])
        we.process(doc)

        r = [' '.join(doc[x]) for x in range(len(doc))]

        assert r[0] == 'add one other'
        assert r[1] == 'add two other'
        assert r[2] == 'add three 3'
        assert r[3] == 'add four other'
        assert r[4] == 'add five other'

    def test_IF_ELSE03(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()

        doc[3].append('4')

        def test(v):
            return lambda o,e: v in o

        we.setWorkflow([i('add'),
                        cf.IF_ELSE(
                                   test('three'),
                                   [a('xxx'), cf.IF_ELSE(test('xxx'),
                                                         [a('6'), cf.IF_ELSE(
                                                                             test('6'),
                                                                             a('six'),
                                                                             (a('only-3s'), a('error')))],
                                                         a('ok'))],
                                   [cf.IF_ELSE(
                                        test('4'),
                                        cf.IF_ELSE(test('four'),
                                                [a('44'), [[[a('forty')]]]],
                                                a('error')),
                                        a('not-four'))]),
                        a('end'),
                        cf.IF_ELSE(test('error'),
                                a('gosh!'),
                                a('OK'))
                        ])
        we.process(doc)

        r = [' '.join(doc[x]) for x in range(len(doc))]

        assert r[0] == 'add one not-four end OK'
        assert r[1] == 'add two not-four end OK'
        assert r[2] == 'add three xxx 6 six end OK'
        assert r[3] == 'add four 4 44 forty end OK'
        assert r[4] == 'add five not-four end OK'

    # -------------- parallel split ------------------

    def test_PARALLEL_SPLIT01(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()

        we.setWorkflow([i('start'),
                        cf.PARALLEL_SPLIT(
                                          printer('p1'),
                                          printer('p2'),
                                          printer('p3'),
                                          printer('p4'),
                                          printer('p5')),
                        lambda o,e: time.sleep(.1),
                        a('end')
                        ])
        we.process(doc)
        r = [' '.join(doc[x]) for x in range(len(doc))]

        assert doc[0][0] == 'start'
        assert doc[0][1] == 'one'
        assert doc[1][0] == 'start'
        assert doc[1][1] == 'two'

        # end must have been inserted while printers were running
        # mixed together with them
        all_pos = set()
        for x in range(len(doc)):
            pos = doc[x].index('end')
            assert pos > 2
            assert pos < len(doc[x])
            all_pos.add(pos)


    # --------------- nested parallel splits --------------------
    def test_PARALLEL_SPLIT02(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()[0:1]

        we.setWorkflow([i('start'),
                        cf.PARALLEL_SPLIT(
                                          [cf.PARALLEL_SPLIT(
                                                            printer('p0'),
                                                            printer('p0a'),
                                                                cf.PARALLEL_SPLIT(printer('p0b'), printer('p0c')),
                                                            ), printer('xx')],
                                          [a('AAA'), printer('p2b')],
                                          printer('p3'),
                                          [a('p4a'), printer('p4b'), printer('p4c')],
                                          [printer('p5'), cf.PARALLEL_SPLIT(
                                                                            printer('p6'),
                                                                            printer('p7'),
                                                                            [printer('p8a'), printer('p8b')],
                                                                            )]),
                        a('end')
                        ])
        we.process(doc)

        # give threads time to finish
        time.sleep(.5)

        assert doc[0][0] == 'start'
        assert doc[0][1] == 'one'

        # at least the fist object should have them all
        # print doc[0]
        for x in ['p0', 'p0a', 'p0b', 'p0c', 'xx', 'AAA', 'p2b', 'p3', 'p4a', 'p4b', 'p4c', 'p5', 'p6', 'p8a', 'p8b']:
            doc[0].index(x) #will fail if not present



    # ------------ parallel split that does nasty things --------------
    def test_PARALLEL_SPLIT03(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()

        we.setWorkflow([i('start'),
                        cf.PARALLEL_SPLIT(
                          [cf.IF(lambda obj, eng: 'jump-verified' in obj, a('error')),
                           cf.PARALLEL_SPLIT(
                                [cf.IF(lambda obj, eng: 'nasty-jump' in obj,
                                       [a('jump-ok'),
                                        lambda obj, eng: ('nasty-jump' in obj and obj.append('jump-verified'))]),
                                cf.PARALLEL_SPLIT(
                                                  a('ok-1'),
                                                   a('ok-2'),
                                                   cf.IF(lambda obj, eng: 'ok-3' not in obj,
                                                            lambda obj, eng: obj.append('ok-3') and eng.breakFromThisLoop()),
                                                            a('ok-4')),

                                a('xx'),
                                lambda obj, eng: 'jump-verified' in obj and eng.breakFromThisLoop(),
                                a('nasty-jump'),
                                cf.TASK_JUMP_IF(lambda obj, eng: 'jump-verified' not in obj, -100)]),
                                ],
                          [a('AAA'), a('p2b')]),
                        a('end')
                        ])
        we.process(doc)
        # give threads time to finish
        time.sleep(.5)

        d = doc[0]

        # at least the fist object should have them all
        # print doc[0]
        for x in ['nasty-jump', 'jump-verified', 'ok-3']:
            d.index(x) #will fail if not present

        assert d.count('ok-1') > 1


    # --------------- choice pattern --------------------

    def test_CHOICE01(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()[0:1]

        def arbiter(obj, eng):
            return obj[-1]

        we.setWorkflow([i('start'),
                        cf.CHOICE(arbiter,
                                  end=(lambda obj, eng: obj.append('error')),
                                  bam=(lambda obj, eng: obj.append('bom')),
                                  bim=(lambda obj, eng: obj.append('bam')),
                                  bom=(lambda obj, eng: obj.append('bum')),
                                  one=(lambda obj, eng: obj.append('bim')),
                                  bum=cf.STOP(),
                                  ),
                        cf.TASK_JUMP_BWD(-1)])
        we.process(doc)

        d = ' '.join(doc[0])

        assert 'bim bam bom bum' in d
        assert 'error' not in d
        assert len(doc[0]) == 6


    def test_CHOICE02(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()[0:1]

        def arbiter(obj, eng):
            return obj[-1]

        we.setWorkflow([i('start'),
                        cf.CHOICE(arbiter,
                                  ('bom', lambda obj, eng: obj.append('bum')),
                                  ('one', lambda obj, eng: obj.append('bim')),
                                  ('bum', cf.STOP()),
                                  ('end', lambda obj, eng: obj.append('error')),
                                  ('bam', lambda obj, eng: obj.append('bom')),
                                  ('bim', lambda obj, eng: obj.append('bam'))),
                        cf.TASK_JUMP_BWD(-1)])
        we.process(doc)

        d = ' '.join(doc[0])

        assert 'bim bam bom bum' in d
        assert 'error' not in d
        assert len(doc[0]) == 6


    def test_CHOICE03(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()[0:1]

        def arbiter(obj, eng):
            return obj[-1]

        we.setWorkflow([i('start'),
                        cf.CHOICE(arbiter,
                                  ('bam', lambda obj, eng: obj.append('bom')),
                                  ('end', lambda obj, eng: obj.append('error')),
                                  ('bim', lambda obj, eng: obj.append('bam')),
                                  bom=(lambda obj, eng: obj.append('bum')),
                                  one=(lambda obj, eng: obj.append('bim')),
                                  bum=cf.STOP(),
                                  ),
                        cf.TASK_JUMP_BWD(-1)])
        we.process(doc)

        d = ' '.join(doc[0])

        assert 'bim bam bom bum' in d
        assert 'error' not in d
        assert len(doc[0]) == 6

    # ------------------- testing simple merge -----------------------
    def test_SIMPLE_MERGE03(self):
        we = GenericWorkflowEngine()
        doc = self.getDoc()[0:1]

        we.setWorkflow([i('start'),
                        cf.SIMPLE_MERGE(
                                  lambda obj, eng: obj.append('bom'),
                                  lambda obj, eng: obj.append('error'),
                                  lambda obj, eng: obj.append('bam'),
                                  lambda obj, eng: obj.append('bum'),
                                  lambda obj, eng: obj.append('end'),
                                  ),
                        ])
        we.process(doc)

        d = ' '.join(doc[0])

        assert 'start' in d
        assert 'bom' in d
        assert 'error' not in d
        assert 'end' in d
        


def suite():
    suite = unittest.TestSuite()
    #suite.addTest(TestGenericWorkflowEngine('test_CHOICE03'))
    suite.addTest(unittest.makeSuite(TestGenericWorkflowEngine))
    return suite

if __name__ == '__main__':
    #unittest.main()
    unittest.TextTestRunner(verbosity=2).run(suite())

