## This file is part of Invenio.
## Copyright (C) 2010, 2011 CERN.
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

"""
HTTP Test web interface. This is the place where to put helpers for
regression tests related to HTTP (or WSGI or SSO).
"""

__revision__ = \
     "$Id$"

__lastupdated__ = """$Date$"""

import cgi
import os
import tempfile
import time

from invenio.config import CFG_SITE_URL, CFG_TMPDIR
from invenio.webpage import page
from invenio.webinterface_handler import WebInterfaceDirectory
from invenio.urlutils import redirect_to_url

class WebInterfaceHTTPTestPages(WebInterfaceDirectory):
    _exports = ["", "post1", "post2", "sso", "dumpreq", "whatismyip", "plupload", "plupload_ajax"]

    def __call__(self, req, form):
        redirect_to_url(req, CFG_SITE_URL + '/httptest/post1')

    index = __call__

    def sso(self, req, form):
        """ For testing single sign-on """
        req.add_common_vars()
        sso_env = {}
        for var, value in req.subprocess_env.iteritems():
            if var.startswith('HTTP_ADFS_'):
                sso_env[var] = value
        out = "<html><head><title>SSO test</title</head>"
        out += "<body><table>"
        for var, value in sso_env.iteritems():
            out += "<tr><td><strong>%s</strong></td><td>%s</td></tr>" % (var, value)
        out += "</table></body></html>"
        return out

    def dumpreq(self, req, form):
        """
        Dump a textual representation of the request object.
        """
        return "<pre>%s</pre>" % cgi.escape(str(req))

    def post1(self, req, form):
        """
        This is used by WSGI regression test, to test if it's possible
        to upload a file and retrieve it correctly.
        """
        if req.method == 'POST':
            if 'file' in form:
                for row in form['file'].file:
                    req.write(row)
            return ''
        else:
            body = """
<form method="post" enctype="multipart/form-data">
<input type="file" name="file" />
<input type="submit" />
</form>"""
        return page("test1", body=body, req=req)

    def post2(self, req, form):
        """
        This is to test L{handle_file_post} function.
        """
        from invenio.webinterface_handler_wsgi_utils import handle_file_post
        from invenio.bibdocfile import stream_file
        if req.method != 'POST':
            body = """<p>Please send a file via POST.</p>"""
            return page("test2", body=body, req=req)
        path, mimetype = handle_file_post(req)
        return stream_file(req, path, mime=mimetype)

    def whatismyip(self, req, form):
        """
        Return the client IP as seen by the server (useful for testing e.g. Robot authentication)
        """
        req.content_type = "text/plain"
        return req.remote_ip

    def plupload_ajax(self, req, form):
        log = tempfile.NamedTemporaryFile(suffix=".log", prefix="plupload-%s-" % time.strftime('%Y%m%d%H%M%S'), dir=CFG_TMPDIR, delete=False)
        print >> log, req
        print >> log, form
        for key, value in form.items():
            if value.filename:
                chunk = tempfile.NamedTemporaryFile(suffix=".chunk", prefix="plupload-%s-" % time.strftime('%Y%m%d%H%M%S'), dir=CFG_TMPDIR, delete=False)
                buf = None
                while buf != "":
                    buf = value.file.read(1024)
                    chunk.write(buf)
                chunk.flush()
                print >> log, "chunk %s -> %s (%s)" % (value.filename, chunk.name, os.path.getsize(chunk.name))
            else:
                print >> log, "%s -> %s" % (key, value.value)
        print >> log, "-" * 80
        return ""

    def plupload(self, req, form):
        """
        To test plupload implementation
        """
        CFG_PLUPLOAD_PATH = "/js/plupload"
        metaheader = """\
<style type="text/css">@import url(%(plupload_path)s/jquery.plupload.queue/css/jquery.plupload.queue.css);</style>
<script type="text/javascript" src="/js/jquery.min.js"></script>
<script type="text/javascript" src="%(plupload_path)s/plupload.full.js"></script>
<script type="text/javascript" src="%(plupload_path)s/jquery.plupload.queue/jquery.plupload.queue.js"></script>
""" % {'plupload_path': CFG_PLUPLOAD_PATH}
        body = "<pre>%s</pre>" % cgi.escape(str(req))
        body += "<pre>%s</pre>" % cgi.escape(str(form))
        body += """\
<script type="text/javascript">
//<![CDATA[

// Convert divs to queue widgets when the DOM is ready
$(function() {
    $("#uploader").pluploadQueue({
        // General settings
        runtimes : 'html5,silverlight,html4',
        url : '/httptest/plupload_ajax',
        max_file_size : '10mb',
        chunk_size : '1mb',
        unique_names : true,

        // Resize images on clientside if we can
        resize : {width : 320, height : 240, quality : 90},

        // Specify what files to browse for
        filters : [
            {title : "Image files", extensions : "jpg,gif,png"},
            {title : "Zip files", extensions : "zip"}
        ],

        // Flash settings
        // flash_swf_url : '%(plupload_path)s/plupload.flash.swf',

        // Silverlight settings
        silverlight_xap_url : '%(plupload_path)s/plupload.silverlight.xap'
    });

    // Client side form validation
    $('form').submit(function(e) {
        var uploader = $('#uploader').pluploadQueue();

        // Validate number of uploaded files
        if (uploader.total.uploaded == 0) {
            // Files in queue upload them first
            if (uploader.files.length > 0) {
                // When all files are uploaded submit form
                uploader.bind('UploadProgress', function() {
                    if (uploader.total.uploaded == uploader.files.length)
                        $('form').submit();
                });

                uploader.start();
            } else
                alert('You must at least upload one file.');

            e.preventDefault();
        }
    });
});
//]]>
</script>

<form post="/httptest/plupload">
    <div id="uploader">
        <p>You browser doesn't have Flash, Silverlight or HTML5 support.</p>
    </div>
</form>
""" % {'plupload_path': CFG_PLUPLOAD_PATH}
        return page("plupload test", metaheaderadd=metaheader, body=body, req=req)