# -*- coding: utf-8 -*-
#
# django-atompub by James Tauber <http://jtauber.com/>
# http://code.google.com/p/django-atompub/
# An implementation of the Atom format and protocol for Django
#
# For instructions on how to use this module to generate Atom feeds,
# see http://code.google.com/p/django-atompub/wiki/UserGuide
#
#
# Copyright (c) 2007, James Tauber
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from xml.sax.saxutils import XMLGenerator
from datetime import datetime
from invenio.config import CFG_VERSION


GENERATOR_TEXT = 'Invenio-SWORD'
GENERATOR_ATTR = {
    'uri': 'http://cdsware.cern.ch/invenio/index.html',
    'version': 'CFG_VERSION'
}



## based on django.utils.xmlutils.SimplerXMLGenerator
class SimplerXMLGenerator(XMLGenerator):
    def addQuickElement(self, name, contents=None, attrs=None):
        "Convenience method for adding an element with no children"
        if attrs is None: attrs = {}
        self.startElement(name, attrs)
        if contents is not None:
            self.characters(contents)
        self.endElement(name)



## based on django.utils.feedgenerator.rfc3339_date
def rfc3339_date(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')



## based on django.utils.feedgenerator.get_tag_uri
def get_tag_uri(url, date):
    "Creates a TagURI. See http://diveintomark.org/archives/2004/05/28/howto-atom-id"
    tag = re.sub('^http://', '', url)
    if date is not None:
        tag = re.sub('/', ',%s:/' % date.strftime('%Y-%m-%d'), tag, 1)
    tag = re.sub('#', '/', tag)
    return 'tag:' + tag


class ValidationError(Exception):
    pass



## based on django.utils.feedgenerator.SyndicationFeed and django.utils.feedgenerator.Atom1Feed
class AtomFeed(object):


    mime_type = 'application/atom+xml'
    ns = u'http://www.w3.org/2005/Atom'


    def __init__(self, atom_id, title, updated=None, icon=None, logo=None, rights=None, subtitle=None,
        authors=[], categories=[], contributors=[], links=[], extra_attrs={}, hide_generator=False):
        if atom_id is None:
            raise LookupError('Feed has no feed_id field')
        if title is None:
            raise LookupError('Feed has no feed_title field')
        # if updated == None, we'll calculate it
        self.feed = {
            'id': atom_id,
            'title': title,
            'updated': updated,
            'icon': icon,
            'logo': logo,
            'rights': rights,
            'subtitle': subtitle,
            'authors': authors,
            'categories': categories,
            'contributors': contributors,
            'links': links,
            'extra_attrs': extra_attrs,
            'hide_generator': hide_generator,
        }
        self.items = []


    def add_item(self, atom_id, title, updated, content=None, published=None, rights=None, source=None, summary=None,
        authors=[], categories=[], contributors=[], links=[], extra_attrs={}):
        if atom_id is None:
            raise LookupError('Feed has no item_id method')
        if title is None:
            raise LookupError('Feed has no item_title method')
        if updated is None:
            raise LookupError('Feed has no item_updated method')
        self.items.append({
            'id': atom_id,
            'title': title,
            'updated': updated,
            'content': content,
            'published': published,
            'rights': rights,
            'source': source,
            'summary': summary,
            'authors': authors,
            'categories': categories,
            'contributors': contributors,
            'links': links,
            'extra_attrs': extra_attrs,
        })


    def latest_updated(self):
        """
        Returns the latest item's updated or the current time if there are no items.
        """
        updates = [item['updated'] for item in self.items]
        if len(updates) > 0:
            updates.sort()
            return updates[-1]
        else:
            return datetime.now() # @@@ really we should allow a feed to define its "start" for this case


    def write_text_construct(self, handler, element_name, data):
        if isinstance(data, tuple):
            text_type, text = data
            if text_type == 'xhtml':
                handler.startElement(element_name, {'type': text_type})
                handler._write(text) # write unescaped -- it had better be well-formed XML
                handler.endElement(element_name)
            else:
                handler.addQuickElement(element_name, text, {'type': text_type})
        else:
            handler.addQuickElement(element_name, data)


    def write_person_construct(self, handler, element_name, person):
        handler.startElement(element_name, {})
        handler.addQuickElement(u'name', person['name'])
        if 'uri' in person:
            handler.addQuickElement(u'uri', person['uri'])
        if 'email' in person:
            handler.addQuickElement(u'email', person['email'])
        handler.endElement(element_name)


    def write_link_construct(self, handler, link):
        if 'length' in link:
            link['length'] = str(link['length'])
        handler.addQuickElement(u'link', None, link)


    def write_category_construct(self, handler, category):
        handler.addQuickElement(u'category', None, category)


    def write_source(self, handler, data):
        handler.startElement(u'source', {})
        if data.get('id'):
            handler.addQuickElement(u'id', data['id'])
        if data.get('title'):
            self.write_text_construct(handler, u'title', data['title'])
        if data.get('subtitle'):
            self.write_text_construct(handler, u'subtitle', data['subtitle'])
        if data.get('icon'):
            handler.addQuickElement(u'icon', data['icon'])
        if data.get('logo'):
            handler.addQuickElement(u'logo', data['logo'])
        if data.get('updated'):
            handler.addQuickElement(u'updated', rfc3339_date(data['updated']))
        for category in data.get('categories', []):
            self.write_category_construct(handler, category)
        for link in data.get('links', []):
            self.write_link_construct(handler, link)
        for author in data.get('authors', []):
            self.write_person_construct(handler, u'author', author)
        for contributor in data.get('contributors', []):
            self.write_person_construct(handler, u'contributor', contributor)
        if data.get('rights'):
            self.write_text_construct(handler, u'rights', data['rights'])
        handler.endElement(u'source')


    def write_content(self, handler, data):
        if isinstance(data, tuple):
            content_dict, text = data
            if content_dict.get('type') == 'xhtml':
                handler.startElement(u'content', content_dict)
                handler._write(text) # write unescaped -- it had better be well-formed XML
                handler.endElement(u'content')
            else:
                handler.addQuickElement(u'content', text, content_dict)
        else:
            handler.addQuickElement(u'content', data)


    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        feed_attrs = {u'xmlns': self.ns}
        if self.feed.get('extra_attrs'):
            feed_attrs.update(self.feed['extra_attrs'])
        handler.startElement(u'feed', feed_attrs)
        handler.addQuickElement(u'id', self.feed['id'])
        self.write_text_construct(handler, u'title', self.feed['title'])
        if self.feed.get('subtitle'):
            self.write_text_construct(handler, u'subtitle', self.feed['subtitle'])
        if self.feed.get('icon'):
            handler.addQuickElement(u'icon', self.feed['icon'])
        if self.feed.get('logo'):
            handler.addQuickElement(u'logo', self.feed['logo'])
        if self.feed['updated']:
            handler.addQuickElement(u'updated', rfc3339_date(self.feed['updated']))
        else:
            handler.addQuickElement(u'updated', rfc3339_date(self.latest_updated()))
        for category in self.feed['categories']:
            self.write_category_construct(handler, category)
        for link in self.feed['links']:
            self.write_link_construct(handler, link)
        for author in self.feed['authors']:
            self.write_person_construct(handler, u'author', author)
        for contributor in self.feed['contributors']:
            self.write_person_construct(handler, u'contributor', contributor)
        if self.feed.get('rights'):
            self.write_text_construct(handler, u'rights', self.feed['rights'])
        if not self.feed.get('hide_generator'):
            handler.addQuickElement(u'generator', GENERATOR_TEXT, GENERATOR_ATTR)

        self.write_items(handler)

        handler.endElement(u'feed')


    def write_items(self, handler):
        for item in self.items:
            entry_attrs = item.get('extra_attrs', {})
            handler.startElement(u'entry', entry_attrs)

            handler.addQuickElement(u'id', item['id'])
            self.write_text_construct(handler, u'title', item['title'])
            handler.addQuickElement(u'updated', rfc3339_date(item['updated']))
            if item.get('published'):
                handler.addQuickElement(u'published', rfc3339_date(item['published']))
            if item.get('rights'):
                self.write_text_construct(handler, u'rights', item['rights'])
            if item.get('source'):
                self.write_source(handler, item['source'])

            for author in item['authors']:
                self.write_person_construct(handler, u'author', author)
            for contributor in item['contributors']:
                self.write_person_construct(handler, u'contributor', contributor)
            for category in item['categories']:
                self.write_category_construct(handler, category)
            for link in item['links']:
                self.write_link_construct(handler, link)
            if item.get('summary'):
                self.write_text_construct(handler, u'summary', item['summary'])
            if item.get('content'):
                self.write_content(handler, item['content'])

            handler.endElement(u'entry')


    def validate(self):

        def validate_text_construct(obj):
            if isinstance(obj, tuple):
                if obj[0] not in ['text', 'html', 'xhtml']:
                    return False
            # @@@ no validation is done that 'html' text constructs are valid HTML
            # @@@ no validation is done that 'xhtml' text constructs are well-formed XML or valid XHTML

            return True

        if not validate_text_construct(self.feed['title']):
            raise ValidationError('feed title has invalid type')
        if self.feed.get('subtitle'):
            if not validate_text_construct(self.feed['subtitle']):
                raise ValidationError('feed subtitle has invalid type')
        if self.feed.get('rights'):
            if not validate_text_construct(self.feed['rights']):
                raise ValidationError('feed rights has invalid type')

        alternate_links = {}
        for link in self.feed.get('links'):
            if link.get('rel') == 'alternate' or link.get('rel') == None:
                key = (link.get('type'), link.get('hreflang'))
                if key in alternate_links:
                    raise ValidationError('alternate links must have unique type/hreflang')
                alternate_links[key] = link

        if self.feed.get('authors'):
            feed_author = True
        else:
            feed_author = False

        for item in self.items:
            if not feed_author and not item.get('authors'):
                if item.get('source') and item['source'].get('authors'):
                    pass
                else:
                    raise ValidationError('if no feed author, all entries must have author (possibly in source)')

            if not validate_text_construct(item['title']):
                raise ValidationError('entry title has invalid type')
            if item.get('rights'):
                if not validate_text_construct(item['rights']):
                    raise ValidationError('entry rights has invalid type')
            if item.get('summary'):
                if not validate_text_construct(item['summary']):
                    raise ValidationError('entry summary has invalid type')
            source = item.get('source')
            if source:
                if source.get('title'):
                    if not validate_text_construct(source['title']):
                        raise ValidationError('source title has invalid type')
                if source.get('subtitle'):
                    if not validate_text_construct(source['subtitle']):
                        raise ValidationError('source subtitle has invalid type')
                if source.get('rights'):
                    if not validate_text_construct(source['rights']):
                        raise ValidationError('source rights has invalid type')

            alternate_links = {}
            for link in item.get('links'):
                if link.get('rel') == 'alternate' or link.get('rel') == None:
                    key = (link.get('type'), link.get('hreflang'))
                    if key in alternate_links:
                        raise ValidationError('alternate links must have unique type/hreflang')
                    alternate_links[key] = link

            if not item.get('content'):
                if not alternate_links:
                    raise ValidationError('if no content, entry must have alternate link')

            if item.get('content') and isinstance(item.get('content'), tuple):
                content_type = item.get('content')[0].get('type')
                if item.get('content')[0].get('src'):
                    if item.get('content')[1]:
                        raise ValidationError('content with src should be empty')
                    if not item.get('summary'):
                        raise ValidationError('content with src requires a summary too')
                    if content_type in ['text', 'html', 'xhtml']:
                        raise ValidationError('content with src cannot have type of text, html or xhtml')
                if content_type:
                    if '/' in content_type and \
                        not content_type.startswith('text/') and \
                        not content_type.endswith('/xml') and not content_type.endswith('+xml') and \
                        not content_type in ['application/xml-external-parsed-entity', 'application/xml-dtd']:
                        # @@@ check content is Base64
                        if not item.get('summary'):
                            raise ValidationError('content in Base64 requires a summary too')
                    if content_type not in ['text', 'html', 'xhtml'] and '/' not in content_type:
                        raise ValidationError('content type does not appear to be valid')

                    # @@@ no validation is done that 'html' text constructs are valid HTML
                    # @@@ no validation is done that 'xhtml' text constructs are well-formed XML or valid XHTML

                    return

        return