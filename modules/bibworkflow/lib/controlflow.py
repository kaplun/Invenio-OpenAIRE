
#######################################################################################
## Copyright (c) 2010, Roman Chyla, http://www.roman-chyla.net                       ##
## All rights reserved.                                                              ##
##                                                                                   ##
## Redistribution and use in source and binary forms, with or without modification,  ##
## are permitted provided that the following conditions are met:                     ##
##                                                                                   ##
##     * Redistributions of source code must retain the above copyright notice,      ##
##       this list of conditions and the following disclaimer.                       ##
##     * Redistributions in binary form must reproduce the above copyright notice,   ##
##       this list of conditions and the following disclaimer in the documentation   ##
##       and/or other materials provided with the distribution.                      ##
##     * Neither the name of the author nor the names of its contributors may be     ##
##       used to endorse or promote products derived from this software without      ##
##       specific prior written permission.                                          ##
##                                                                                   ##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND   ##
## ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED     ##
## WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.##
## IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,  ##
## INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    ##
## BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,     ##
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF   ##
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE   ##
## OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED ##
## OF THE POSSIBILITY OF SUCH DAMAGE.                                                ##
#######################################################################################

import threading
import thread
import Queue
import time
import copy


MAX_TIMEOUT = 30000


# HACK, should not be up-depenedent
from newseman.general.workflow.engine import GenericWorkflowEngine as engine

# ----------------------- helper calls -------------------------------- #



def TASK_JUMP_BWD(step=-1):
    """Jumps to the previous task - eng.jumpCallBack
    example: A, B, TASK_JUMP_FWD(-2), C, D, ...
    will produce: A, B, A, B, A, B, ... (recursion!)
    @var step: int, must not be positive number
    """
    def _move_back(obj, eng):
        eng.jumpCallBack(step)
    _move_back.__name__ = 'TASK_JUMP_BWD'
    return _move_back

def TASK_JUMP_FWD(step=1):
    """Jumps to the next task - eng.jumpCallForward()
    example: A, B, TASK_JUMP_FWD(2), C, D, ...
    will produce: A, B, D
    @var step: int
    """
    def _x(obj, eng):
        eng.jumpCallForward(step)
    _x.__name__ = 'TASK_JUMP_FWD'
    return _x

def TASK_JUMP_IF(cond, step):
    """Jumps in the specified direction if the condition
    evaluates to True, the difference from other IF conditions
    is that this one does not insert the code inside a [] block
    @var cond: function
    @var step: int, negative jumps back, positive forward
    """
    def minus(obj, eng):
        return cond(obj, eng) and eng.jumpCallBack(step)
    def plus(obj, eng):
        return cond(obj, eng) and eng.jumpCallForward(step)
    if int(step) < 0:
        return minus
    else:
        return plus

def BREAK():
    """Stops execution of the current block, but keeps running
    in the workflow - eng.breakFromThisLoop()
    """
    def x(obj, eng):
        eng.breakFromThisLoop()
    x.__name__ = 'BREAK'
    return x

def STOP():
    """Unconditional stop of the workflow execution"""
    def x(obj, eng):
        eng.stopProcessing()
    x.__name__ = 'STOP'
    return x

def OBJ_NEXT():
    """Stops the workflow execution for the current object and start
    the same worfklow for the next object - eng.continueNextToken()"""
    def x(obj, eng):
        eng.continueNextToken()
    x.__name__ = 'OBJ_NEXT'
    return x

def OBJ_JUMP_FWD(step=1):
    """Stops the workflow execution, jumps to xth consecutive object
    and starts executing the workflow on it - eng.jumpTokenForward()
    @var step: int, relative jump from the current obj, must not be
        negative number
    """
    def x(obj, eng):
        eng.jumpTokenForward(step)
    x.__name__ = 'OBJ_JUMP_FWD'
    return x

def OBJ_JUMP_BWD(step=-1):
    """Stops the workflow execution, jumps to xth antecedent object
    and starts executing the workflow on it - eng.jumpTokenForward()
    @var step: int, relative jump from the current obj, must not be
        negative number
    """
    def _x(obj, eng):
        eng.jumpTokenBackward(step)
    _x.__name__ = 'OBJ_JUMP_BWD'
    return _x

# -------------------------- some conditions -------------------------------------- #

def IF(cond, branch):
    """Implements condition, if cond evaluates to True
    branch is executed
    @var cond: callable, function that decides
    @var branch: block of functions to run

    @attention: the branch is inserted inside [] block, therefore jumping is limited
                only inside the branch
    """
    x = lambda obj, eng: cond(obj,eng) and eng.jumpCallForward(1) or eng.breakFromThisLoop()
    x.__name__ = 'IF'
    return (x, branch)

def IF_NOT(cond, branch):
    """Implements condition, if cond evaluates to False
    branch is executed
    @var cond: callable, function that decides
    @var branch: block of functions to run

    @attention: the branch is inserted inside [] block, therefore jumping is limited
                only inside the branch
    """
    return [lambda obj, eng: cond(obj,eng) and eng.breakFromThisLoop() or 1,
       branch
     ]

def IF_ELSE(cond, branch1, branch2):
    """Implements condition, if cond evaluates to True
    branch1 is executed, otherwise branch2
    @var cond: callable, function that decides
    @var branch1: block of functions to run [if=true]
    @var branch2: block of functions to run [else]

    @attention: the branch is inserted inside [] block, therefore jumping is limited
                only inside the branch
    """
    if branch1 is None or branch2 is None:
        raise Exception ("Neither of the branches can be None/empty")
    x = lambda obj, eng: cond(obj, eng) and eng.jumpCallForward(1) or eng.jumpCallForward(3)
    x.__name__ = 'IF_ELSE'
    return [x, branch1, BREAK(), branch2]

def WHILE(cond, branch):
    """Keeps executing branch as long as the condition cond is True
    @var cond: callable, function that decides
    @var branch: block of functions to run [if=true]
    """
    # we don't know what is hiding inside branch
    branch = tuple(engine._cleanUpCallables(branch))
    def x(obj, eng):
        if not cond(obj, eng):
            eng.breakFromThisLoop()
    x.__name__ = 'WHILE'
    return [x, branch, TASK_JUMP_BWD(-(len(branch)+1))]

# -------------------- basic control flow patterns -------------------------------- #
# -------- http://www.yawlfoundation.org/resources/patterns.html#basic ------------ #

def PARALLEL_SPLIT(*args):
    """
    Tasks A,B,C,D... are all started in parallel
    @attention: tasks A,B,C,D... are not addressable, you can't
        you can't use jumping to them (they are invisible to
        the workflow engine). Though you can jump inside the
        branches
    @attention: tasks B,C,D... will be running on their own
        once you have started them, and we are not waiting for
        them to finish. Workflow will continue executing other
        tasks while B,C,D... might be still running.
    @attention: a new engine is spawned for each branch or code,
        all operations works as expected, but mind that the branches
        know about themselves, they don't see other tasks outside.
        They are passed the object, but not the old workflow
        engine object
    @postcondition: eng object will contain lock (to be used
        by threads)
    """

    def _parallel_split(obj, eng, calls):
        lock=thread.allocate_lock()
        i = 0
        eng.setVar('lock', lock)
        for func in calls:
            new_eng = duplicate_engine_instance(eng)
            new_eng.setWorkflow([lambda o,e: e.setVar('lock', lock), func])
            thread.start_new_thread(new_eng.process, ([obj], ))
            #new_eng.process([obj])
    return lambda o, e: _parallel_split(o, e, args)


def SYNCHRONIZE(*args, **kwargs):
    """
    After the execution of task B, task C, and task D, task E can be executed.
    @var *args: args can be a mix of callables and list of callables
                the simplest situation comes when you pass a list of callables
                they will be simply executed in parallel.
                   But if you pass a list of callables (branch of callables)
                which is potentionally a new workflow, we will first create a
                workflow engine with the workflows, and execute the branch in it
    @attention: you should never jump out of the synchronized branches
    """
    timeout = MAX_TIMEOUT
    if 'timeout' in kwargs:
        timeout = kwargs['timeout']

    if len(args) < 2:
        raise Exception('You must pass at least two callables')

    def _synchronize(obj, eng):
        queue = MyTimeoutQueue()
        #spawn a pool of threads, and pass them queue instance
        for i in range(len(args)-1):
            t = MySpecialThread(queue)
            t.setDaemon(True)
            t.start()

        for func in args[0:-1]:
            if isinstance(func, list) or isinstance(func, tuple):
                new_eng = duplicate_engine_instance(eng)
                new_eng.setWorkflow(func)
                queue.put(lambda: new_eng.process([obj]))
            else:
                queue.put(lambda: func(obj, eng))

        #wait on the queue until everything has been processed
        queue.join_with_timeout(timeout)

        #run the last func
        args[-1](obj, eng)
    return _synchronize

def CHOICE(arbiter, *predicates, **kwpredicates):
    """
    A choice is made to execute either task B, task C or task D
    after execution of task A.
    @var arbiter: a function which returns some value (the value
        must be inside the predicates dictionary)
    @var predicates: list of callables, the first item must be the
        value returned by the arbiter, example:
        ('submit', task_a),
        ('upload' : task_a, [task_b, task_c]...)
    @keyword **kwpredicates: you can supply predicates also as a
        keywords, example
        CHOICE(arbiter, one=lambda...., two=[lambda o,e:...., ...])
    @postcondition: all tasks are 'jumpable'

    """
    workflow = []
    mapping = {}
    for branch in predicates:
        workflow.append(branch[1:])
        mapping[branch[0]] = len(workflow)
        workflow.append(BREAK())

    for k, v in kwpredicates.items():
        workflow.append(v)
        mapping[k] = len(workflow)
        workflow.append(BREAK())

    def _exclusive_choice(obj, eng):
        val = arbiter(obj, eng)
        i = mapping[val] # die on error
        eng.jumpCallForward(i)
    c = _exclusive_choice
    c.__name__ = arbiter.__name__
    workflow.insert(0, c)
    return workflow


def SIMPLE_MERGE(*args):
    """
    Task E will be started when any one of the tasks B, C or D completes.
    This pattern though makes a context assumption: there is no
    parallelism preceding task E.
    """
    
    if len(args) < 2:
        raise Exception("You must suply at least 2 callables")
    
    final_task = args[-1]
    workflow = []
    mapping = {}
    total = ((len(args)-1) * 2) + 1
    for branch in args[0:-1]:
        total -= 2
        workflow.append(branch)
        workflow.append(TASK_JUMP_FWD(total))
        
    workflow.append(final_task)
    return workflow


# ------------------------------------------------------------- #
#                       helper methods/classes                  #
# ------------------------------------------------------------- #

def duplicate_engine_instance(eng):
    """creates a new instance of the workflow engine based on existing instance"""
    #new_eng = copy.deepcopy(eng)
    #new_eng.removeAllCallbacks()
    #new_eng.reset()


    new_eng = eng.__class__(processing_factory=eng.processing_factory,
                      callback_chooser=eng.callback_chooser,
                      before_processing=eng.before_processing,
                      after_processing=eng.after_processing)
    return new_eng




class MyTimeoutQueue(Queue.Queue):
    def __init__(self, *args):
        Queue.Queue.__init__(self, *args)

    def join_with_timeout(self, timeout):
        self.all_tasks_done.acquire()
        try:
            endtime = time.time() + timeout
            while self.unfinished_tasks:
                remaining = endtime - time.time()
                if remaining <= 0.0:
                    raise threading.ThreadError('NotFinished')
                self.all_tasks_done.wait(remaining)
        finally:
            self.all_tasks_done.release()

class MySpecialThread(threading.Thread):
    def __init__(self, itemq, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.itemq = itemq

    def run(self):
        call = self.itemq.get()
        call()
