## -*- mode: python; coding: utf-8; -*-
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008 CERN.
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""OAI harvestor - 'wget' records from an OAI repository.

This 'getter' simply retrieve the records from an OAI repository.
"""

__revision__ = "$Id$"

try:
    import sys
    import httplib
    import urllib
    import getpass
    import socket
    import re
    import time
    import base64
    import os
    import urlparse
    from cStringIO import StringIO
    from xml.dom.minidom import parseString
except ImportError, e:
    print "Error: %s" % e
    sys.exit(1)

from invenio.bibconvert_xslt_engine import convert
from invenio.config import CFG_SITE_ADMIN_EMAIL, CFG_VERSION, \
    CFG_PYLIBDIR

CFG_BIBHARVEST_REGISTRY_PATHNAME = os.path.join(CFG_PYLIBDIR, 'invenio', 'bibharvest_registries', 'bhr_*.py')

RE_BIBHARVEST_VALID_OAIID = re.compile(r"oai:[a-zA-Z][a-zA-Z0-9\-]*(\.[a-zA-Z][a-zA-Z0-9\-]+)+:[a-zA-Z0-9\-_\.!~\*'\(\);/\?:@&=\+$,%]+")

RE_BIBHARVEST_DSPACE_HANDLE = re.compile(r"(http://hdl\.handle\.net/|hdl:)(?P<handle>\d+(\.\d+)?/\d+)")

from invenio.pluginutils import PluginContainer, create_enhanced_plugin_builder

def _load_bibharvest_registries():
    def get_full_registry_signature(): pass
    def guess_oai_pmh_handler_signature(url): pass

    plugin_builder = create_enhanced_plugin_builder(
        compulsory_objects={
            'get_full_registry': get_full_registry_signature,
            'guess_oai_pmh_handler': guess_oai_pmh_handler_signature})

    return PluginContainer([CFG_BIBHARVEST_REGISTRY_PATHNAME], plugin_builder=plugin_builder)

BIBHARVEST_REGISTRIES = _load_bibharvest_registries()

http_response_status_code = {

    "000" : "Unknown",
    "100" : "Continue",
    "200" : "OK",
    "302" : "Redirect",
    "401" : "Authentication Required",
    "403" : "Forbidden",
    "404" : "Not Found",
    "500" : "Error",
    "503" : "Service Unavailable"
}

def http_param_resume(http_param_dict, resumptionToken):
    "Change parameter dictionary for harvest resumption"

    http_param = {
        'verb'            : http_param_dict['verb'],
        'resumptionToken' : resumptionToken
    }

    return http_param

def http_request_parameters(http_param_dict, method="POST"):
    "Assembly http request parameters for http method used"

    return urllib.urlencode(http_param_dict)

class InvenioOAIHarvestGetterError(Exception): pass

def OAI_Session(server, script, http_param_dict , method="POST", output="",
                resume_request_nbr=0, secure=False, user=None, password=None,
                cert_file=None, key_file=None):
    """Handle one OAI session (1 request, which might lead
    to multiple answers because of resumption tokens)

    If output filepath is given, each answer of the oai repository is saved
    in corresponding filepath, with a unique number appended at the end.
    This number starts at 'resume_request_nbr'.

    Returns an int corresponding to the last created 'resume_request_nbr'.
    """

    write_to_open_file = hasattr(output, "write")

    if not write_to_open_file:
        sys.stderr.write("Starting the harvesting session at %s" %
            time.strftime("%Y-%m-%d %H:%M:%S --> ", time.localtime()))
        sys.stderr.write("%s - %s\n" % (server,
            http_request_parameters(http_param_dict)))

    a = OAI_Request(server, script,
                    http_request_parameters(http_param_dict, method), method,
                    secure, user, password, cert_file, key_file, interactive=not write_to_open_file)

    rt_obj = re.search('<resumptionToken.*>(.+)</resumptionToken>',
        a, re.DOTALL)

    i = resume_request_nbr

    while rt_obj is not None and rt_obj != "":

        if output:
            # Write results to a file named 'output'
            if a.lower().find('<'+http_param_dict['verb'].lower()) > -1:
                if write_to_open_file:
                    output.write(a)
                else:
                    write_file( "%s.%07d" % (output, i), a)
            else:
                # hmm, were there no records in output? Do not create
                # a file and warn user
                if not write_to_open_file:
                    sys.stderr.write("\n<!--\n*** WARNING: NO RECORDS IN THE HARVESTED DATA: "
                                 +  "\n" + repr(a) + "\n***\n-->\n")
        else:
            sys.stdout.write(a)

        i = i + 1

        time.sleep(1)

        http_param_dict = http_param_resume(http_param_dict, rt_obj.group(1))

        a = OAI_Request(server, script,
                        http_request_parameters(http_param_dict, method), method,
                        secure, user, password, cert_file, key_file, interactive=not write_to_open_file)

        rt_obj = re.search('<resumptionToken.*>(.+)</resumptionToken>',
            a, re.DOTALL)

    if output:
        # Write results to a file named 'output'
        if a.lower().find('<'+http_param_dict['verb'].lower()) > -1:
            if write_to_open_file:
                output.write(a)
            else:
                write_file("%s.%07d" % (output, i), a)
        else:
            # hmm, were there no records in output? Do not create
            # a file and warn user
            sys.stderr.write("\n<!--\n*** WARNING: NO RECORDS IN THE HARVESTED DATA: "
                                 +  "\n" + repr(a) + "\n***\n-->\n")
    else:
        sys.stdout.write(a)

    return i

def guess_oai_pmh_handler(url):
    """
    Given a URL guess the OAI-PMH base_url.
    @param url: the URL for which a guess is needed.
    @type url: string
    @return: a set of OAI-PMH bases.
    @rtpye: set([str, ...])
    """
    oai_pmh_bases = set()
    for registry in BIBHARVEST_REGISTRIES.values():
        oai_pmh_bases |= registry["guess_oai_pmh_handler"](url)
    return oai_pmh_bases

def guess_oai_pmh_id(url):
    """
    Given a URL guess the OAI-PMH id of the given document.
    @param url: the URL for which a guess is needed.
    @type url: string
    @return: the guessed OAI-PMH Id
    @rtpye: string
    """
    html = urllib.urlopen(url).read()
    the_id = RE_BIBHARVEST_VALID_OAIID.search(html)
    if the_id:
        return the_id.group()
    dspace_handle = RE_BIBHARVEST_DSPACE_HANDLE.search(html)
    if dspace_handle:
        hostname = urlparse.urlsplit(url)[1]
        return "oai:%s:%s" % (hostname, dspace_handle.group("handle"))
    return ""

def get_supported_metadata_prefix(oai_pmh_base, oai_id=None):
    protocol, server, script = urlparse.urlsplit(oai_pmh_base)[:3]
    secure = protocol == 'https'
    http_param_dict = {"verb": "ListMetadataFormats"}
    if oai_id:
        http_param_dict["identifier"] = oai_id
    output = StringIO()
    harvest(server, script, http_param_dict, secure=secure, output=output)
    output = parseString(output.getvalue())
    ret = []
    for item in output.getElementsByTagName("metadataPrefix"):
        ret.append(item.firstChild.nodeValue.encode("utf8"))
    return ret

def magic_harvest_a_record(url=None, oai_pmh_bases=None, oai_id=None):
    def empty_record():
        return """<?xml version="1.0" encoding="UTF-8"?>
<record xmlns="http://www.loc.gov/MARC21/slim"></record>"""
    def harvest_record(oai_pmh_base, oai_id, prefix):
        protocol, server, script = urlparse.urlsplit(oai_pmh_base)[:3]
        secure = protocol == 'https'
        output = StringIO()
        http_param_dict = {
            "verb": "GetRecord",
            "identifier": oai_id,
            "metadataPrefix": prefix,
        }
        harvest(server, script, http_param_dict, output=output, secure=secure)
        output = output.getvalue()
        if 'marc' in prefix.lower():
            output = convert(output, "oaimarc2marcxml.xsl")
        elif 'dc' in prefix.lower():
            output = convert(output, "oaidc2marcxml.xsl")
        else:
            output = empty_record()
        return output

    if not url and not oai_pmh_base and not oai_id:
        return empty_record()
    if not oai_pmh_bases:
        oai_pmh_bases = guess_oai_pmh_handler(url)
        if not oai_pmh_bases:
            return empty_record()
    if not oai_id:
        oai_id = guess_oai_pmh_id(url)
        if not oai_id:
            return empty_record()
    ret = empty_record()
    for oai_pmh_base in oai_pmh_bases:
        metadata_prefixes = get_supported_metadata_prefix(oai_pmh_base, oai_id)
        for prefix in metadata_prefixes:
            if 'marc' in prefix.lower() or 'dc' in prefix.lower():
                new_ret = harvest_record(oai_pmh_base, oai_id, prefix)
                if len(new_ret) > len(ret):
                    ret = new_ret
    return ret

def harvest(server, script, http_param_dict , method="POST", output="",
            sets=None, secure=False, user=None, password=None,
            cert_file=None, key_file=None):
    """
    Handle multiple OAI sessions (multiple requests, which might lead to
    multiple answers).

    Needed for harvesting multiple sets in one row.

    @param server: the server URL to harvest eg: cdsweb.cern.ch
    @type server: string

    @param script: path to the OAI script on the server to harvest
                  eg: /oai2d
    @type script: string

    @param http_param_dict: the URL parameters to send to the OAI script
                  eg: {'verb':'ListRecords', 'from'='2004-04-01'}
                  EXCLUDING the setSpec parameters. See 'sets'
                  parameter below.
    @type http_param_dict: dict

    @param method: if we harvest using POST or GET
                  eg: POST
    @type method: string

    @param output: the path (and base name) or a file object where results
                  are saved. In case of path, to handle multiple answers
                  (for eg. triggered by multiple sets harvesting or OAI
                  resumption tokens), this base name is suffixed with a
                  sequence number. Eg output='/tmp/z.xml' ->
                  '/tmp/z.xml.0000000', '/tmp/z.xml.0000001', etc.
                  If file at given path already exists, it is
                  overwritten.
                  When this parameter is left empty, the results are
                  returned on the standard output.
    @type output: string or open file object

    @param sets: the sets to harvest. Since this function
                 offers multiple sets harvesting in one row, the OAI
                 'setSpec' cannot be defined in the 'http_param_dict'
                 dict where other OAI parameters are.
    @type sets: list of string

    @param secure: of we should use HTTPS (True) or HTTP (false)
    @type secure: bool

    @param user: username to use to login to the server to
                  harvest in case it requires Basic authentication.
    @type user: string

    @param password: a password (in clear) of the server to harvest
                  in case it requires Basic authentication.
    @type password: string

    @param key_file: a path to a PEM file that contain your private
                  key to connect to the server in case it requires
                  certificate-based authentication
                  (If provided, 'cert_file' must also be provided)
    @type key_file: string

    @param cert_file: path to a PEM file that contain your public
                  key in case the server to harvest requires
                  certificate-based authentication
                  (If provided, 'key_file' must also be provided)
    @type cert_file: string
    @return: the number of files created by the harvesting
    @rtpe: integer

    @note: if L{output} is an open file then the function will not
        print any message to screen.
    """
    if sets:
        i = 0
        for aset in sets:
            http_param_dict['set'] = aset
            i = OAI_Session(server, script, http_param_dict, method,
                            output, i, secure, user, password,
                            cert_file, key_file)
            i += 1
        return i
    else:
        OAI_Session(server, script, http_param_dict, method,
                    output, secure=secure, user=user,
                    password=password, cert_file=cert_file,
                    key_file=key_file)
        return 1

def write_file(filename="harvest", a=""):
    "Writes a to filename"

    f = open(filename, "w")
    f.write(a)
    f.close()

def OAI_Request(server, script, params, method="POST", secure=False,
                user=None, password=None,
                key_file=None, cert_file=None, interactive=True):
    """Handle OAI request

    Parameters:

        server - *str* the server URL to harvest
                 eg: cdsweb.cern.ch

        script - *str* path to the OAI script on the server to harvest
                 eg: /oai2d

        params - *str* the URL parameters to send to the OAI script
                 eg: verb=ListRecords&from=2004-04-01

        method - *str* if we harvest using POST or GET
                 eg: POST

        secure - *bool* of we should use HTTPS (True) or HTTP (false)

          user - *str* username to use to login to the server to
                 harvest in case it requires Basic authentication.

      password - *str* a password (in clear) of the server to harvest
                 in case it requires Basic authentication.

      key_file - *str* a path to a PEM file that contain your private
                 key to connect to the server in case it requires
                 certificate-based authentication
                 (If provided, 'cert_file' must also be provided)

      cert_file - *str* a path to a PEM file that contain your public
                 key in case the server to harvest requires
                 certificate-based authentication
                 (If provided, 'key_file' must also be provided)
    """

    headers = {"Content-type":"application/x-www-form-urlencoded",
               "Accept":"text/xml",
               "From": CFG_SITE_ADMIN_EMAIL,
               "User-Agent":"CDS Invenio %s" % CFG_VERSION}

    if password:
        # We use basic authentication
        headers["Authorization"] = "Basic " + base64.encodestring(user + ":" + password).strip()

    i = 0
    while i < 10:
        i = i + 1
        if secure and not (key_file and cert_file):
            # Basic authentication over HTTPS
            try:
                conn = httplib.HTTPSConnection(server)
            except httplib.HTTPException, e:
                if not interactive:
                    raise e
                else:
                    sys.stderr.write("An error occured when trying to connect to %s: %s" % (server, e))
                    sys.exit(0)
        elif secure and key_file and cert_file:
            # Certificate-based authentication
            try:
                conn = httplib.HTTPSConnection(server,
                                               key_file=key_file,
                                               cert_file=cert_file)
            except httplib.HTTPException, e:
                if not interactive:
                    raise e
                else:
                    sys.stderr.write("An error occured when trying to connect to %s: %s" % (server, e))
                    sys.exit(0)
        else:
            # Unsecured connection
            try:
                conn = httplib.HTTPConnection(server)
            except httplib.HTTPException, e:
                if not interactive:
                    raise e
                else:
                    sys.stderr.write("An error occured when trying to connect to %s: %s\n" % (server, e))
                    sys.exit(0)

        try:
            if method == "GET":
                conn.request("GET", script + "?" + params, headers=headers)
            elif method == "POST":
                conn.request("POST", script, params, headers)
        except socket.gaierror, (err, str_e):
            if not interactive:
                raise e
            else:
                sys.stderr.write("An error occured when trying to connect to %s: %s\n" % (server, str_e))
                sys.exit(0)
        try:
            response = conn.getresponse()
        except httplib.HTTPException, e:
            if not interactive:
                raise e
            else:
                sys.stderr.write("An error occured when trying to read response from %s: %s\n" % (server, e))
                sys.exit(0)

        status = "%d" % response.status

        if interactive:
            if http_response_status_code.has_key(status):
                sys.stderr.write("%s(%s) : %s : %s\n" % (status,
                    http_response_status_code[status],
                    response.reason,
                    params))
            else:
                sys.stderr.write("%s(%s) : %s : %s\n" % (status,
                    http_response_status_code['000'],
                    response.reason, params))

        if response.status == 200:
            i = 10
            data = response.read()
            conn.close()
            return data

        elif response.status == 503:
            try:
                nb_seconds_to_wait = \
                    int(response.getheader("Retry-After", "%d" % (i*i)))
            except ValueError:
                nb_seconds_to_wait = 10
            if interactive:
                sys.stderr.write("Retry in %d seconds...\n" % nb_seconds_to_wait)
            time.sleep(nb_seconds_to_wait)

        elif response.status == 302:
            if interactive:
                sys.stderr.write("Redirecting...\n")
            server    = response.getheader("Location").split("/")[2]
            script    = "/" + \
                "/".join(response.getheader("Location").split("/")[3:])

        elif response.status == 401:
            if interactive:
                if user is not None:
                    sys.stderr.write("Try again\n")
                if not secure:
                    sys.stderr.write("*WARNING* Your password will be sent in clear!\n")
                # getting input from user
                sys.stderr.write('User:')
                try:
                    user = raw_input()
                    password = getpass.getpass()
                except EOFError, e:
                    sys.stderr.write("\n")
                    sys.exit(1)
                except KeyboardInterrupt, e:
                    sys.stderr.write("\n")
                    sys.exit(1)
                headers["Authorization"] = "Basic " + base64.encodestring(user + ":" + password).strip()
            else:
                raise InvenioOAIHarvestGetterError("Wrong password supplied")
        else:
            if interactive:
                sys.stderr.write("Retry in 10 seconds...\n")
            time.sleep(10)

    if interactive:
        sys.stderr.write("Harvesting interrupted (after 10 attempts) at %s: %s\n"
        % (time.strftime("%Y-%m-%d %H:%M:%S --> ", time.localtime()), params))

        sys.exit(1)
    raise InvenioOAIHarvestGetterError("Harvesting interrupted (after 10 attempts) at %s: %s\n"
        % (time.strftime("%Y-%m-%d %H:%M:%S --> ", time.localtime()), params))
