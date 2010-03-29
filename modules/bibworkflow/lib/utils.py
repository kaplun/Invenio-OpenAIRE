
import inspect
import traceback
import sys

from newseman.general.workflow.engine import GenericWorkflowEngine


def RUN_WF(workflow, engine=GenericWorkflowEngine,
           processing_factory = None,
           callback_chooser = None,
           before_processing = None,
           after_processing = None,
           data_connector = None,
           pass_eng = [],
           pass_always = None):
    """Task for running other workflow - ie. new workflow engine will
    be created and the workflow run. The workflow engine is garbage
    collected together with the function. Therefore you can run the
    function many times and it will reuse the already-loaded WE. In fact
    this WE has an empty before_processing callback.

    @see before_processing callback for more information.

    @var workflow: normal workflow tasks definition
    @keyword engine: class of the engine to create WE
    @keyword processing_factory: WE callback
    @keyword callback_chooser: WE callback
    @keyword before_processing: WE callback
    @keyword after_processing: WE callback
    ---
    @keyword data_connector: callback which will prepare data and pass
        the corrent objects into the workflow engine (from the calling
        engine into the called WE), if not present, the current obj is
        passed (possibly wrapped into a list)
    @keyword pass_eng: list of keys corresponding to the values, that should
        be passed from the calling engine to the called engine. This is
        called only once, during initialization.
    """

    if not before_processing: # the engine will not reset its state
        before_processing = lambda obj, eng: None

    wfe = engine(processing_factory, callback_chooser, before_processing, after_processing)
    wfe.setWorkflow(workflow)
    
    def x(obj, eng=None):
        
        # pass data from the old wf engine to the new one
        for k in pass_eng:
            wfe.setVar(k, eng.getVar(k))
            if not pass_always:
                pass_eng.remove(k)
        
        
        if data_connector:
            data = data_connector(obj, eng)
            wfe.process(data)
        else:
            if not isinstance(obj, list):
                wfe.process([obj])
            else:
                wfe.process(obj)
    x.__name__ = 'RUN_WF'
    return x

# -------------------------- useful structures------------------------------------- #

def EMPTY_CALL(obj, eng):
    """Empty call that does nothing"""
    pass

def ENG_GET(something):
    """this is the same as lambda obj, eng: eng.getVar('something')
    @var something: str, key of the object to retrieve
    @return: value of the key from eng object
    """
    def x(obj, eng):
        return eng.getVar(something)
    x.__name__ = 'ENG_GET'
    return x

def ENG_SET(key, value):
    """this is the same as lambda obj, eng: eng.setVar('key', value)
    @var key: str, key of the object to retrieve
    @var value: anything
    @attention: this call is executed when the workflow is created
        therefore, the key and value must exist at the time
        (obj and eng don't exist yet)
    """
    def _eng_set(obj, eng):
        return eng.setVar(key, value)
    _eng_set.__name__ = 'ENG_SET'
    return _eng_set

def OBJ_GET(something):
    """this is the same as lambda obj, eng: something in obj and obj[something]
    @var something: str, key of the object to retrieve
    @return: value of the key from obj object
    """
    def x(obj, eng):
        return something in obj and obj[something]
    x.__name__ = 'OBJ_GET'
    return x

def OBJ_SET(key, value):
    """this is the same as lambda obj, eng: obj.__setitem__(key, value)
    @var key: str, key of the object to retrieve
    @var value: anything
    @attention: this call is executed when the workflow is created
        therefore, the key and value must exist at the time
        (obj and eng don't exist yet)
    """
    def x(obj, eng):
        obj[key] = value
    x.__name__ = 'OBJ_SET'
    return x

# ----------------------- error handlling -------------------------------

def ERROR(msg='Error in the workflow'):
    """Throws uncatchable error stopping execution and printing the message"""
    caller = inspect.getmodule(inspect.currentframe().f_back)
    if caller :
        caller = caller.__file__
    else:
        caller = ''
    def x(obj, eng):
        raise Exception('in %s : %s' % (caller, msg))
    x.__name__ = 'ERROR'
    return x

def TRY(onecall, retry=1, onfailure=Exception, verbose=True):
    """Wrap the call in try...except statement and eventually
    retries when failure happens
    @keyword attempts: how many times to retry
    @keyword onfailure: exception to raise or callable to call on failure
    """

    if not callable(onecall):
        raise Exception('You can wrap only one callable with TRY')

    def x(obj, eng):
        tries = 1 + retry
        i = 0
        while i < tries:
            try:
                onecall(obj, eng)
                break # success
            except:
                if verbose:
                    traceback.print_exc()
                i += 1
                if i >= tries:
                    if isinstance(onfailure, Exception):
                        raise onfailure
                    elif callable(onfailure):
                        onfailure(obj, eng)
                    else:
                        raise Exception('Error after attempting to run: %s' % onecall)

    x.__name__ = 'TRY'
    return x

