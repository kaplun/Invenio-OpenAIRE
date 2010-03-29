# -*- coding: utf8 -*-
import unittest
import sys
import os

p = os.path.abspath(os.path.dirname(__file__) + '/../')
if p not in sys.path:
    sys.path.append(p)

from engine import GenericWorkflowEngine


def m(key=None):
    def _m(token, inst):
        token.setFeatureKw(sem=((token.getFeature('sem') or '') + ' ' + key).strip())
    return _m

def if_str_token_back(value='', step=0):
    def x(token, inst):
        if str(token) == value and not token.getFeature('token_back'):
            token.setFeature('token_back', 1)
            inst.jumpTokenBack(step)
    return lambda token, inst: x(token, inst)

def if_str_token_forward(value='', step=0):
    def x(token, inst):
        if str(token) == value and not token.getFeature('token_forward'):
            token.setFeature('token_forward', 1)
            inst.jumpTokenForward(step)
    return lambda token, inst: x(token, inst)

def call_back(step=0):
    def x(token, inst):
        if not token.getFeature('back'):
            token.setFeature('back', 1)
            inst.jumpCallBack(step)
    return lambda token, inst: x(token, inst)

def call_forward(step=0):
    return lambda token, inst: inst.jumpCallForward(step)
def break_loop():
    return lambda token, inst: inst.breakFromThisLoop()
def stop_processing():
    return lambda token, inst: inst.stopProcessing()
def next_token():
    return lambda token, inst: inst.continueNextToken()

def get_first(doc):
    return doc[0].getFeature('sem')

def get_xth(doc, xth):
    return doc[xth].getFeature('sem')

def stop_if_str(value=None):
    def x(token, inst):
        if str(token) == value:
            inst.stopProcessing()
    return lambda token, inst: x(token, inst)

class FakeToken(object):
    def __init__(self, data, **attributes):
        if isinstance(data, basestring):
            self.data = unicode(data)
        else:
            self.data = data
        self.pos = None #tohle nastavi TokenCollection pri vystupu objektu
        self.backreference = None #tady bude odkaz na TokenCollection (pri vystupu)
        self.__prev = 0
        self.__next = 0
        self.__attributes = {}
        for attr_name, attr_value in attributes.items():
            self.setFeature(attr_name, attr_value)

    def __str__(self):
        if isinstance(self.data, unicode):
            return self.data # tady byl jednoduchy return
        else:
            return str(self.data) #tady byl unicode(self.data)
    def __repr__(self):
        return 'Token(%s, **%s)' % (repr(self.data), repr(self.__attributes))
    def __eq__(self, y):
        return self.data == y
    def __ne__(self, y):
        return self.data != y

    def __get(self, index):
        if self.backreference is None:
            raise Exception("No collection available")
        backr = self.backreference()
        if index < len(backr) and index >= 0:
            return backr[index]
        else:
            return None
    def neighbour(self, index):
        return self.__get(self.pos + index)

    def reset(self):
        self.__prev = 0
        self.__next = 0

    def prev(self):
        self.__prev += 1
        return self.__get(self.pos - self.__prev)
    def next(self):
        self.__next += 1
        return self.__get(self.pos + self.__next)

    def isa(self, *args, **kwargs):
        if args and self.data != args[0]:
            return False
        for key, value in kwargs.items():
            if self.getFeature(key) != value:
                return False
        return True

    def setValue(self, value):
        self.data = value

    def getFeature(self, key):
        try:
            return self.__attributes[key]
        except KeyError:
            return None

    def setFeature(self, key, value):
        if isinstance(value, basestring):
            value = unicode(value)
        self.__attributes[key] = value

    def setFeatureKw(self, **kwargs):
        for key, value in kwargs.items():
            self.setFeature(key, value)

    def getAllFeatures(self):
        return self.__attributes

class TestWorkflowEngine(unittest.TestCase):
    """Tests using FakeTokens in place of strings"""

    def setUp(self):
        self.key = '*'
        self.we = GenericWorkflowEngine()
        self.data = u"one\ntwo\nthree\nfour\nfive"
        self.doc = [FakeToken(x, type='*') for x in self.data.splitlines()]

    def tearDown(self):
        pass

    # --------- call_forward ---------------

    def test_workflow_01(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), call_forward(1), m('cat'), m('puppy')],
                    m('horse'),
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog cat puppy horse'

    def test_workflow_02(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), call_forward(2), m('cat'), m('puppy'), m('python')],
                    m('horse'),
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog puppy python horse'

    def test_workflow_03(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), call_forward(50), m('cat'), m('puppy'), m('python')],
                    m('horse'),
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog horse'

    def test_workflow_04(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), call_forward(2), m('cat'), m('puppy'), m('python')],
                    m('horse'),
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog puppy python horse'

    def test_workflow_05(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), call_forward(-2), m('cat'), m('puppy'), m('python')],
                    m('horse'),
                    ])
        doc = self.doc
        try:
            self.we.process(doc)
        except:
            t = get_first(doc)
            assert t == 'mouse dog'
        else:
            raise Exception("call_forward allowed negative number")

    def test_workflow_06(self):
        self.we.addManyCallbacks(self.key, [
                    call_forward(3),
                    m('mouse'),
                    [ m('dog'), call_forward(2), m('cat'), m('puppy'), m('python')],
                    m('horse'),
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'horse'

    # ------------- call_back -------------------

    def test_workflow_01b(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), call_back(-1), m('cat'), m('puppy')],
                    m('horse'),
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog dog cat puppy horse'

    def test_workflow_02b(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), m('cat'), m('puppy'), m('python'), call_back(-2)],
                    m('horse'),
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog cat puppy python puppy python horse'

    def test_workflow_03b(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), m('cat'), call_back(-50), m('puppy'), m('python')],
                    m('horse'),
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog cat dog cat puppy python horse'

    def test_workflow_04b(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), m('cat'), m('puppy'), m('python')],
                    m('horse'),
                    call_back(-2)
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog cat puppy python horse dog cat puppy python horse'

    def test_workflow_05b(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    [ m('dog'), call_back(2), m('cat'), m('puppy'), m('python')],
                    m('horse'),
                    ])
        doc = self.doc
        try:
            self.we.process(doc)
        except:
            t = get_first(doc)
            assert t == 'mouse dog'
        else:
            raise Exception("call_back allowed positive number")

    # --------- complicated loop -----------

    def test_workflow_07(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                        [ m('dog'),
                            [ m('cat'), m('puppy')],
                            [ m('python'),
                                [m('wasp'), m('leon')],
                            ],
                        m('horse'),
                        ]
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog cat puppy python wasp leon horse'

    def test_workflow_07a(self):
        self.we.addManyCallbacks(self.key, [
                    call_forward(2),
                    m('mouse'),
                        [ m('dog'),
                            [ m('cat'), m('puppy')],
                            [ m('python'), call_back(-2),
                                [m('wasp'), m('leon')],
                            ],
                        m('horse'),
                        ]
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'dog cat puppy python python wasp leon horse'

    # ----------- BreakFromThisLoop -----------

    def test_workflow_07b(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                        [ m('dog'),
                            [ m('cat'), m('puppy')],
                            [ m('python'), break_loop(),
                                [m('wasp'), m('leon')],
                            ],
                        m('horse'),
                        ]
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == 'mouse dog cat puppy python horse'

    def test_workflow_07c(self):
        self.we.addManyCallbacks(self.key, [
                    break_loop(),
                    m('mouse'),
                        [ m('dog'),
                            [ m('cat'), m('puppy')],
                            [ m('python'),
                                [m('wasp'), m('leon')],
                            ],
                        m('horse'),
                        ]
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert t == None

    # ----------- processing of a whole collection --------

    # ----------- StopProcessing --------------------------

    def test_workflow_08(self):
        self.we.addManyCallbacks(self.key, [
                    stop_processing(),
                    m('mouse'),
                        [ m('dog'),
                            [ m('cat'), m('puppy')],
                            [ m('python'),
                                [m('wasp'), m('leon')],
                            ],
                        m('horse'),
                        ]
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        assert get_xth(doc, 0) == None
        assert get_xth(doc, 1) == None
        assert get_xth(doc, 2) == None
        assert str(doc[0]) == 'one'
        assert str(doc[1]) == 'two'
        assert str(doc[2]) == 'three'

    def test_workflow_08a(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                        [ m('dog'),
                            [ m('cat'), m('puppy')],
                            [ m('python'),
                                stop_if_str('four'),
                                [m('wasp'), m('leon')],
                            ],
                        m('horse'),
                        ]
                    ])
        doc = self.doc
        self.we.process(doc)
        r1 = 'mouse dog cat puppy python wasp leon horse'
        r2 = 'mouse dog cat puppy python'
        assert get_xth(doc, 0) == r1
        assert get_xth(doc, 1) == r1
        assert get_xth(doc, 2) == r1
        assert get_xth(doc, 3) == r2
        assert get_xth(doc, 4) == None
        assert str(doc[0]) == 'one'
        assert str(doc[1]) == 'two'
        assert str(doc[2]) == 'three'
        assert str(doc[3]) == 'four'
        assert str(doc[4]) == 'five'

    # ---------- jumpTokenNext -------------

    def test_workflow_09(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                        [ m('dog'),
                            [ m('cat'), m('puppy')],
                            [ m('python'),
                                next_token(),
                                [m('wasp'), m('leon')],
                            ],
                        m('horse'),
                        ]
                    ])
        doc = self.doc
        self.we.process(doc)
        r1 = 'mouse dog cat puppy python'
        r2 = 'mouse dog cat puppy python'
        assert get_xth(doc, 0) == r1
        assert get_xth(doc, 1) == r1
        assert get_xth(doc, 2) == r1
        assert get_xth(doc, 3) == r1
        assert get_xth(doc, 4) == r1
        assert str(doc[0]) == 'one'
        assert str(doc[1]) == 'two'
        assert str(doc[2]) == 'three'
        assert str(doc[3]) == 'four'
        assert str(doc[4]) == 'five'

    def test_workflow_09a(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                        [ m('dog'),
                         if_str_token_back('four', -2),
                            [ m('cat'), m('puppy')],
                        m('horse'),
                        ]
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        r1 = 'mouse dog cat puppy horse' #one, five
        r2 = 'mouse dog cat puppy horse mouse dog cat puppy horse' #two, three
        r3 = 'mouse dog mouse dog cat puppy horse' #four
        assert get_xth(doc, 0) == r1
        assert get_xth(doc, 1) == r2
        assert get_xth(doc, 2) == r2
        assert get_xth(doc, 3) == r3
        assert get_xth(doc, 4) == r1
        assert str(doc[0]) == 'one'
        assert str(doc[1]) == 'two'
        assert str(doc[2]) == 'three'
        assert str(doc[3]) == 'four'
        assert str(doc[4]) == 'five'

    def test_workflow_09b(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                        [ m('dog'),
                         if_str_token_forward('two', 2),
                            [ m('cat'), m('puppy')],
                        m('horse'),
                        ]
                    ])
        doc = self.doc
        self.we.process(doc)
        t = get_first(doc)
        r1 = 'mouse dog cat puppy horse' #one, four, five
        r2 = 'mouse dog' #two
        r3 = None #three
        assert get_xth(doc, 0) == r1
        assert get_xth(doc, 1) == r2
        assert get_xth(doc, 2) == r3
        assert get_xth(doc, 3) == r1
        assert get_xth(doc, 4) == r1
        assert str(doc[0]) == 'one'
        assert str(doc[1]) == 'two'
        assert str(doc[2]) == 'three'
        assert str(doc[3]) == 'four'
        assert str(doc[4]) == 'five'

    def test_workflow_21(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    if_str_token_forward('one', -1),
                    m('horse'),
                    ])
        doc = self.doc
        try:
            self.we.process(doc)
        except:
            t = get_first(doc)
            assert t == 'mouse'
        else:
            raise Exception("jumpTokenForward allowed negative number")

    def test_workflow_21b(self):
        self.we.addManyCallbacks(self.key, [
                    m('mouse'),
                    if_str_token_back('one', 1),
                    m('horse'),
                    ])
        doc = self.doc
        try:
            self.we.process(doc)
        except:
            t = get_first(doc)
            assert t == 'mouse'
        else:
            raise Exception("jumpTokenBack allowed positive number")



def suite():
    suite = unittest.TestSuite()
    #suite.addTest(WorkflowEngine('test_workflow'))
    suite.addTest(unittest.makeSuite(TestWorkflowEngine))
    return suite

if __name__ == '__main__':
    #unittest.main()
    unittest.TextTestRunner(verbosity=2).run(suite())

