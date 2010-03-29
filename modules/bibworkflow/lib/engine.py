
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

import logging
import new

DEBUG = False

class StopProcessing(Exception): pass #stops everything
class ContinueNextToken(Exception): pass # can be called many levels deep, jumps up to next token
class JumpTokenForward(Exception): pass
class JumpTokenBack(Exception): pass

class JumpCallForward(Exception): pass #in one loop [call, call...] jumps x steps forward
class JumpCallBack(Exception): pass #in one loop [call, call...] jumps x steps forward
class BreakFromThisLoop(Exception): pass #break from this loop, but do not stop processing


class WorkflowMissingKey(Exception): pass # when trying to use unregistered workflow key
class WorkflowError(Exception): pass # general error

class GenericWorkflowEngine():
    """Wofklow engine is a Finite State Machine with memory
    It is used to execute set of methods in a specified order
    example: ....

    """

    def __init__(self,
                 processing_factory=None,
                 callback_chooser=None,
                 before_processing=None,
                 after_processing=None):

        for name, x in [('processing_factory', processing_factory),
                        ('callback_chooser', callback_chooser),
                        ('before_processing', before_processing),
                        ('after_processing', after_processing)]:
            if x:
                if not callable(x):
                    raise WorkflowError('Callback must be a callable object')
                else:
                    setattr(self, name, x)

        self.__callbacks = {}
        self._store = {}
        self._objects = [] # tmp storage of processed objects
        self._i = [0] # holds id of the currently processed object
        self.log = logging

    def continueNextToken(self):
        """Continue with the next token"""
        raise ContinueNextToken

    def stopProcessing(self):
        """Break out, stops everything"""
        raise StopProcessing

    def jumpTokenForward(self, offset):
        """Jumps to xth token"""
        raise JumpTokenForward(offset)

    def jumpTokenBack(self, offset):
        """Returns x tokens back - be careful with circular loops"""
        raise JumpTokenBack(offset)

    def jumpCallForward(self, offset):
        """Jumps to xth call in this loop"""
        raise JumpCallForward(offset)

    def jumpCallBack(self, offset):
        """Returns x calls back in the current loop - be careful with circular loop"""
        raise JumpCallBack(offset)

    def breakFromThisLoop(self):
        """Stops in the current loop but continues in those above"""
        raise BreakFromThisLoop

    def configure(self, **kwargs):
        """Method to set attributes of the workflow engine - use with extreme care
        (well, you can set up the attrs directly, I am not protecting them, but
        that is not nice)
        Used mainly if you want to change the engine's callbacks - if processing factory
        before_processing, after_processing

        @var **kwargs: dictionary of values
        """
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise WorkflowError("Object %s does not have attr %s - it is not allowed to set nonexisting attribute (and you don't circumvent interface, do you?)" % (str(self), key))

    def process(self, objects):
        """Start processing
        @param  objects: either a list of object or
                instance of TokenizedDocument
        @return: You never know what will be returned from the workflow ;-)
                But many exceptions can be raised, so watch out for them,
                if there happened an exception, you can be sure something
                wrong happened (something that your workflow should handle
                and didn't). Workflow engine is not interfering into the
                processing chain, it is not catching exceptions for you.
        """
        if isinstance(objects, list):
            return self.processing_factory(objects, self)
        elif hasattr(objects, 'TokenizedDocument') and objects.TokenizedDocument:
            return self.processing_factory(objects.tokens(), self)
        else:
            raise WorkflowError('Passed in object %s is neither list nor TokenizedDocument' % (objects.__class__))



    @staticmethod
    def before_processing(objects, self):
        """Standard pre-processing callback - saves a pointer to the processed objects"""
        self.reset()
        self._objects = objects


    @staticmethod
    def after_processing(objects, self):
        """Standard post-processing callback, basic cleaning"""
        self._objects = []
        self._i = [0]

    @staticmethod
    def callback_chooser(obj, self):
        """There are possibly many workflows inside this workflow engine
        and they are meant for different types of objects, this method
        should choose and return the callbacks appropriate for the currently
        processed object
        @var obj: currently processed object
        @var eng: the workflow engine object
        @return: set of callbacks to run
        """
        if hasattr(obj, 'getFeature'):
            t = obj.getFeature('type')
            if t:
                return self.getCallbacks(t)
        else:
            return self.getCallbacks('*') #for the non-token types return default workflows

    @staticmethod
    def processing_factory(objects, self):
        """Default processing factory
        Will process objects
        @var objects: list of objects (passed in by self.process())
        @keyword cls: engine object itself, because this method may
            be implemented by the standalone function, we pass the
            self also as a cls argument
        """

        self.before_processing(objects, self)

        i = self._i
        i[0] = -1
        while i[0] < len(objects)-1 and i[0] >= -1: # negative index not allowed, -1 is special
            i[0] += 1
            obj = objects[i[0]]
            callbacks = self.callback_chooser(obj, self)
            if callbacks:
                try:
                    self.run_callbacks(i, callbacks, objects, obj)
                except StopProcessing:
                    if DEBUG:
                        self.log.debug("Processing was stopped: '%s' (object: %s)" % (str(callbacks), repr(obj)))
                    break
                except JumpTokenBack, step:
                    if step.args[0] > 0:
                        raise WorkflowError("JumpTokenBack cannot be positive number")
                    if DEBUG:
                        self.log.debug('Warning, we go back [%s] objects' % step.args[0])
                    i[0] = max(0, i[0] - 1 + step.args[0])
                except JumpTokenForward, step:
                    if step.args[0] < 0:
                        raise WorkflowError("JumpTokenForward cannot be negative number")
                    if DEBUG:
                        self.log.debug('We skip [%s] objects' % step.args[0])
                    i[0] = min(len(objects), i[0] - 1 + step.args[0])
                except ContinueNextToken:
                    if DEBUG:
                        self.log.debug('Stop processing for this object, continue with next')
                    continue

        self.after_processing(objects, self)



    def run_callbacks(self, i, callbacks, objects, obj, indent=0):
        """This method will execute callbacks in the workflow
        @var i: index of the currently processed object
        @var callbacks: list of callables (may be deep nested)
        @var objects: list of processed objects
        @var obj: currently processed object
        @keyword indent: int, indendation level
        """
        c = -1
        y = 0
        while y < len(callbacks):
            f = callbacks[y]
            y += 1
            try:
                c += 1
                if isinstance(f, list) or isinstance(f, tuple):
                    self.run_callbacks(i, f, objects, obj, indent+1)
                    continue
                if DEBUG:
                    self.log.debug("Running (%s%s.) callback '%s' for obj: %s" % (indent * '-', c, f.__name__, repr(obj)))
                self.execute_callback(f, obj)
                if DEBUG:
                    self.log.debug('+ok')
            except BreakFromThisLoop:
                if DEBUG:
                    self.log.debug('Break from this loop')
                return
            except JumpCallBack, step:
                if DEBUG:
                    self.log.debug('Warning, we go [%s] calls back' % step.args[0])
                if step.args[0] > 0:
                    raise WorkflowError("JumpCallBack cannot be positive number")
                y = max(0, y - 1 + step.args[0])
            except JumpCallForward, step:
                if DEBUG:
                    self.log.debug('We skip [%s] calls' % step.args[0])
                if step.args[0] < 0:
                    raise WorkflowError("JumpCallForward cannot be negative number")
                y = min(len(callbacks), y - 1 + step.args[0])

    def execute_callback(self, callback, obj):
        """Executes the callback - override this method to implement logging"""
        
        callback(obj, self)




    def getCallbacks(self, key='*'):
        """Returns callbacks for the given workflow
        @keyword key: name of the workflow (default: *)
                if you want to get all configured workflows
                pass None object as a key
        @return: list of callbacks
        """
        if key:
            try:
                return self.__callbacks[key]
            except KeyError, e:
                raise WorkflowMissingKey('No workflow is registered for the key: %s. Perhaps you forgot to load workflows or the workflow definition for the given key was empty?' % key)
        else:
            return self.__callbacks

    def addCallback(self, key, func, before=None, after=None, relative_weight=None):
        try:
            if func: #can be None
                self.getCallbacks(key).append(func)
        except WorkflowMissingKey:
                self.__callbacks[key] = []
                return self.__callbacks[key].append(func)
        except Exception, e:
            self.log.debug('Impossible to add callback %s for key: %s' % (str(func), key))
            self.log.debug(e)

    def addManyCallbacks(self, key, list_or_tuple):
        list_or_tuple = list(self._cleanUpCallables(list_or_tuple))
        for f in list_or_tuple:
            self.addCallback(key, f)
    
    @classmethod
    def _cleanUpCallables(cls, callbacks):
        """helper method to remove non-callables from the passed-in callbacks"""
        for x in callbacks:
            if isinstance(x, list):
                yield list(cls._cleanUpCallables(x))
            elif isinstance(x, tuple):
                # tumples are simply converted to normal members
                for fc in cls._cleanUpCallables(x):
                    yield fc
            elif x is not None:
                yield x

    def removeAllCallbacks(self):
        self.__callbacks = {}

    def removeCallbacks(self, key):
        """for the given key, remove callbacks"""
        try:
            del(self.__callbacks[key])
        except KeyError:
            pass

    def reset(self):
        """Empties the stack memory"""
        self._store = {}

    def replaceCallbacks(self, key, funcs):
        """replace processing workflow with a new workflow"""
        list_or_tuple = list(self._cleanUpCallables(funcs))
        self.removeCallbacks(key)
        for f in list_or_tuple:
            self.addCallback(key, f)

    def setWorkflow(self, list_or_tuple):
        """Sets the (default) workflow which will be run when
        you call process()
        @var list_or_tuple: workflow configuration
        """
        self.replaceCallbacks('*', list_or_tuple)

    def setVar(self, key, what):
        """Stores the obj in the internal stack"""
        self._store[key] = what

    def getVar(self, key, default=None):
        """returns named obj from internal stack. If not found, returns None"""
        try:
            return self._store[key]
        except:
            if default is not None:
                self.setVar(key, default)
            return default

    def getCurrObjId(self):
        """Returns id of the currently processed object"""
        return self._i[0]

    def getObjects(self):
        """Returns iterator for walking through the objects"""
        i = 0
        for obj in self._objects:
            yield (i, obj)
            i += 1


class TalkativeWorkflowEngine(GenericWorkflowEngine):
    def execute_callback(self, callback, obj):
        obj_rep = []
        max_len = 30
        def val_format(v):
            return '<%s ...>' % repr(v)[:max_len]
        def func_format(c):
            return '<%s ...%s:%s>' % (c.func_name, c.func_code.co_filename[-max_len:], c.func_code.co_firstlineno)
        if isinstance(obj, dict):
            for k, v in obj.items():
                obj_rep.append('%s:%s' % (k, val_format(v)))
            obj_rep = '{%s}' % (', '.join(obj_rep))
        elif isinstance(obj, list):
            for v in obj:
                obj_rep.append(val_format(v))
            obj_rep = '[%s]' % (', '.join(obj_rep))
        else:
            obj_rep = val_format(obj)
        self.log.debug('%s ( %s )' % (func_format(callback), obj_rep))
        callback(obj, self)
