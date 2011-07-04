"""
Callables that are used in the specification of the workflows 
in the configuration file.

Using the following methods in the workflow engine
    setVar(variable_name, variable_value), 
    getVar(variable_name),
    delVar(variable_name),
    hasVar(variable_name)
the callables can communicate with the webinterface handler and 
in between themselves.

Two specific variables stand out in particular:
 'interface_id': The interface(as specified in the configuration file) 
                 that should be displayed upon halting the engine.
                 Set this variable before halting the engine.
                 Delete it as soon as the workflow resumes.

 'next_user':    The list of users ids who are allowed to access the workflow 
                 through the web interface. Set them in the callables as required.
                 Deleting the variable implies universal access.

Another noteworthy variable is 'status', which is the status of the workflow and
is displayed when the session is accessed through it's id.  
"""

from engine import HaltProcessing
from invenio.mailutils import send_email

def buildInterface(interface):
    def _buildInterface(session, engine):        
        engine.setVar('interface_id', interface)
        engine.setVar('status', 'Halted')
        raise HaltProcessing  
    return _buildInterface

def checkValues(interface):
    """
    Authenticate the values submitted through the form.
    Either jump one step back or continue through one step 
    forward depending on the success or failue of the checks.
    Jumping back would mean redisplay of the form.

    Note: The actual checks will not be done here. A seperate
    class should be added for the checks.
    (The checks will be specified in the configuartion file)
    """
    def _checkValues(session, engine):
        #raise Exception(interface)
        if interface == 'interface-submission':
            if session['language'] == 'fr':
                engine.delVar('interface_id')
                session['uri'] = session['uri'] + '/interface-approval'
                engine.setVar('next_user', [1])
                engine.setVar('status','Waiting for approval.')
                engine.jumpCallForward(1)
            elif session['language'] == 'en': engine.jumpCallBack(-1)
        if interface == 'interface-approval':
            if session['decision'] in ['approve', 'reject']:
                engine.delVar('interface_id') 
                engine.delVar('next_user')
                engine.jumpCallForward(1)
            else: engine.jumpCallBack(-1)
    return _checkValues

def sendEmails(from_addr, to_addrs, email_subj, email_txt):
    def _sendEmails(session, engine):
        try:
            txt = email_txt + session['uri']
        except KeyError:
            raise Exception("Key(s) to be substituted in the email \
                            text not found in the session.")
            return
        send_email(from_addr, to_addrs, email_subj, txt)
    return _sendEmails

def createUploadRecord():
    """
    Create the record.
    """
    def _createUploadRecord(session, engine):
        pass
    return _createUploadRecord

def checkApprovalStatus():
    def _checkApprovalStatus(session, engine):
        if session['decision'] == 'approve': 
            engine.setVar('status', 'Completed')
            return True
        elif session['decision'] == 'reject': 
            engine.setVar('status', 'Completed')
            return False
    return _checkApprovalStatus

def if_else(call):
    """
    Copied from the Workflow Engine documentation.
    Not really an if-else. If the 'if' conditional holds true, 
    a 'jump' should be made(by one step) after the functions in the list
    corresponding to the 'if' are executed. Or else, the functions in the
    list corresponding to the 'else' are also executed.
    """
    def inner_call(obj, eng):
       if call(obj, eng):     #if True, continue processing
          eng.jumpCallForward(1)
       else:                  #else, skip the next step
          eng.jumpCallForward(2)
    return inner_call
