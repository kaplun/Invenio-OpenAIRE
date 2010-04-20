# ./invenio/raw/mets.py
# PyXB bindings for NamespaceModule
# NSM:37b18ba845b72418ee8d15dde7fb53950cd4055d
# Generated 2010-04-20 10:20:01.606257 by PyXB version 1.1.1
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:82dd8ab0-4c55-11df-a1bb-0016d3115fae')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
from invenio import _xlink

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.loc.gov/METS/', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a Python instance."""
    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace.fallbackNamespace(), location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, _fallback_namespace=default_namespace)


# Atomic SimpleTypeDefinition
class STD_ANON_1 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_1._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_1, enum_prefix=None)
STD_ANON_1.BYTE = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'BYTE')
STD_ANON_1.IDREF = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'IDREF')
STD_ANON_1.SMIL = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'SMIL')
STD_ANON_1.MIDI = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'MIDI')
STD_ANON_1.SMPTE_25 = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-25')
STD_ANON_1.SMPTE_24 = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-24')
STD_ANON_1.SMPTE_DF30 = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-DF30')
STD_ANON_1.SMPTE_NDF30 = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-NDF30')
STD_ANON_1.SMPTE_DF29_97 = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-DF29.97')
STD_ANON_1.SMPTE_NDF29_97 = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-NDF29.97')
STD_ANON_1.TIME = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'TIME')
STD_ANON_1.TCF = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'TCF')
STD_ANON_1.XPTR = STD_ANON_1._CF_enumeration.addEnumeration(unicode_value=u'XPTR')
STD_ANON_1._InitializeFacetMap(STD_ANON_1._CF_enumeration)

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class URIs (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.anyURI."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'URIs')
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.anyURI
URIs._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'URIs', URIs)

# Atomic SimpleTypeDefinition
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.RECT = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'RECT')
STD_ANON_2.CIRCLE = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'CIRCLE')
STD_ANON_2.POLY = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'POLY')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_3 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_3, enum_prefix=None)
STD_ANON_3.BYTE = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'BYTE')
STD_ANON_3.SMIL = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'SMIL')
STD_ANON_3.MIDI = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'MIDI')
STD_ANON_3.SMPTE_25 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-25')
STD_ANON_3.SMPTE_24 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-24')
STD_ANON_3.SMPTE_DF30 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-DF30')
STD_ANON_3.SMPTE_NDF30 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-NDF30')
STD_ANON_3.SMPTE_DF29_97 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-DF29.97')
STD_ANON_3.SMPTE_NDF29_97 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'SMPTE-NDF29.97')
STD_ANON_3.TIME = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'TIME')
STD_ANON_3.TCF = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'TCF')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_4 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_4, enum_prefix=None)
STD_ANON_4.ordered = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'ordered')
STD_ANON_4.unordered = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'unordered')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_5 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_5._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_5, enum_prefix=None)
STD_ANON_5.ARK = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'ARK')
STD_ANON_5.URN = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'URN')
STD_ANON_5.URL = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'URL')
STD_ANON_5.PURL = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'PURL')
STD_ANON_5.HANDLE = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'HANDLE')
STD_ANON_5.DOI = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'DOI')
STD_ANON_5.OTHER = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'OTHER')
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_6 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_6._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_6, enum_prefix=None)
STD_ANON_6.BYTE = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'BYTE')
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_7 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_7._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_7, enum_prefix=None)
STD_ANON_7.Adler_32 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'Adler-32')
STD_ANON_7.CRC32 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'CRC32')
STD_ANON_7.HAVAL = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'HAVAL')
STD_ANON_7.MD5 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'MD5')
STD_ANON_7.MNP = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'MNP')
STD_ANON_7.SHA_1 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'SHA-1')
STD_ANON_7.SHA_256 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'SHA-256')
STD_ANON_7.SHA_384 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'SHA-384')
STD_ANON_7.SHA_512 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'SHA-512')
STD_ANON_7.TIGER = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'TIGER')
STD_ANON_7.WHIRLPOOL = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'WHIRLPOOL')
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_8 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_8._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_8, enum_prefix=None)
STD_ANON_8.BYTE = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'BYTE')
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_9 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_9._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_9, enum_prefix=None)
STD_ANON_9.MARC = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'MARC')
STD_ANON_9.MODS = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'MODS')
STD_ANON_9.EAD = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'EAD')
STD_ANON_9.DC = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'DC')
STD_ANON_9.NISOIMG = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'NISOIMG')
STD_ANON_9.LC_AV = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'LC-AV')
STD_ANON_9.VRA = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'VRA')
STD_ANON_9.TEIHDR = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'TEIHDR')
STD_ANON_9.DDI = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'DDI')
STD_ANON_9.FGDC = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'FGDC')
STD_ANON_9.LOM = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'LOM')
STD_ANON_9.PREMIS = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'PREMIS')
STD_ANON_9.PREMISOBJECT = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'PREMIS:OBJECT')
STD_ANON_9.PREMISAGENT = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'PREMIS:AGENT')
STD_ANON_9.PREMISRIGHTS = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'PREMIS:RIGHTS')
STD_ANON_9.PREMISEVENT = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'PREMIS:EVENT')
STD_ANON_9.TEXTMD = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'TEXTMD')
STD_ANON_9.METSRIGHTS = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'METSRIGHTS')
STD_ANON_9.ISO_191152003_NAP = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'ISO 19115:2003 NAP')
STD_ANON_9.OTHER = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'OTHER')
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_10 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_10._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_10, enum_prefix=None)
STD_ANON_10.decompression = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'decompression')
STD_ANON_10.decryption = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'decryption')
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_11 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_11._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_11, enum_prefix=None)
STD_ANON_11.INDIVIDUAL = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'INDIVIDUAL')
STD_ANON_11.ORGANIZATION = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'ORGANIZATION')
STD_ANON_11.OTHER = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'OTHER')
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_12 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_12._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_12, enum_prefix=None)
STD_ANON_12.CREATOR = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'CREATOR')
STD_ANON_12.EDITOR = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'EDITOR')
STD_ANON_12.ARCHIVIST = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'ARCHIVIST')
STD_ANON_12.PRESERVATION = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'PRESERVATION')
STD_ANON_12.DISSEMINATOR = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'DISSEMINATOR')
STD_ANON_12.CUSTODIAN = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'CUSTODIAN')
STD_ANON_12.IPOWNER = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'IPOWNER')
STD_ANON_12.OTHER = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'OTHER')
STD_ANON_12._InitializeFacetMap(STD_ANON_12._CF_enumeration)

# Complex type areaType with content type EMPTY
class areaType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'areaType')
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute BEGIN uses Python identifier BEGIN
    __BEGIN = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'BEGIN'), 'BEGIN', '__httpwww_loc_govMETS_areaType_BEGIN', pyxb.binding.datatypes.string)

    BEGIN = property(__BEGIN.value, __BEGIN.set, None, u'BEGIN (string/O): An attribute that specifies the point in the content file where the relevant section of content begins. It can be used in conjunction with either the END attribute or the EXTENT attribute as a means of defining the relevant portion of the referenced file precisely. It can only be interpreted meaningfully in conjunction with the BETYPE or EXTTYPE, which specify the kind of beginning/ending point values or beginning/extent values that are being used. The BEGIN attribute can be used with or without a companion END or EXTENT element. In this case, the end of the content file is assumed to be the end point.\n\t\t\t\t')


    # Attribute END uses Python identifier END
    __END = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'END'), 'END', '__httpwww_loc_govMETS_areaType_END', pyxb.binding.datatypes.string)

    END = property(__END.value, __END.set, None, u'END (string/O): An attribute that specifies the point in the content file where the relevant section of content ends. It can only be interpreted meaningfully in conjunction with the BETYPE, which specifies the kind of ending point values being used. Typically the END attribute would only appear in conjunction with a BEGIN element.\n\t\t\t\t')


    # Attribute BETYPE uses Python identifier BETYPE
    __BETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'BETYPE'), 'BETYPE', '__httpwww_loc_govMETS_areaType_BETYPE', STD_ANON_1)

    BETYPE = property(__BETYPE.value, __BETYPE.set, None, u'BETYPE: Begin/End Type.\n\t\t\t\t\tBETYPE (string/O): An attribute that specifies the kind of BEGIN and/or END values that are being used. For example, if BYTE is specified, then the BEGIN and END point values represent the byte offsets into a file. If IDREF is specified, then the BEGIN element specifies the ID value that identifies the element in a structured text file where the relevant section of the file begins; and the END value (if present) would specify the ID value that identifies the element with which the relevant section of the file ends. Must be one of the following values: \nBYTE\nIDREF\nSMIL\nMIDI\nSMPTE-25\nSMPTE-24\nSMPTE-DF30\nSMPTE-NDF30\nSMPTE-DF29.97\nSMPTE-NDF29.97\nTIME\nTCF\nXPTR\n\t\t\t\t')


    # Attribute COORDS uses Python identifier COORDS
    __COORDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'COORDS'), 'COORDS', '__httpwww_loc_govMETS_areaType_COORDS', pyxb.binding.datatypes.string)

    COORDS = property(__COORDS.value, __COORDS.set, None, u'COORDS (string/O): Specifies the coordinates in an image map for the shape of the pertinent area as specified in the SHAPE attribute. While technically optional, SHAPE and COORDS must both appear together to define the relevant area of image content. COORDS should be used in conjunction with SHAPE in the manner defined for the COORDs and SHAPE attributes on an HTML4 <area> element. COORDS must be a comma delimited string of integer value pairs representing coordinates (plus radius in the case of CIRCLE) within an image map. Number of coordinates pairs depends on shape: RECT: x1, y1, x2, y2; CIRC: x1, y1; POLY: x1, y1, x2, y2, x3, y3 . . .\n\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_areaType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute EXTENT uses Python identifier EXTENT
    __EXTENT = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'EXTENT'), 'EXTENT', '__httpwww_loc_govMETS_areaType_EXTENT', pyxb.binding.datatypes.string)

    EXTENT = property(__EXTENT.value, __EXTENT.set, None, u'EXTENT (string/O): An attribute that specifies the extent of the relevant section of the content file. Can only be interpreted meaningfully in conjunction with the EXTTYPE which specifies the kind of value that is being used. Typically the EXTENT attribute would only appear in conjunction with a BEGIN element and would not be used if the BEGIN point represents an IDREF.\n\t\t\t\t')


    # Attribute EXTTYPE uses Python identifier EXTTYPE
    __EXTTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'EXTTYPE'), 'EXTTYPE', '__httpwww_loc_govMETS_areaType_EXTTYPE', STD_ANON_3)

    EXTTYPE = property(__EXTTYPE.value, __EXTTYPE.set, None, u'EXTTYPE (string/O): An attribute that specifies the kind of EXTENT values that are being used. For example if BYTE is specified then EXTENT would represent a byte count. If TIME is specified the EXTENT would represent a duration of time. EXTTYPE must be one of the following values: \nBYTE\nSMIL\nMIDI\nSMPTE-25\nSMPTE-24\nSMPTE-DF30\nSMPTE-NDF30\nSMPTE-DF29.97\nSMPTE-NDF29.97\nTIME\nTCF.\n\t\t\t\t')


    # Attribute SHAPE uses Python identifier SHAPE
    __SHAPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SHAPE'), 'SHAPE', '__httpwww_loc_govMETS_areaType_SHAPE', STD_ANON_2)

    SHAPE = property(__SHAPE.value, __SHAPE.set, None, u'SHAPE (string/O): An attribute that can be used as in HTML to define the shape of the relevant area within the content file pointed to by the <area> element. Typically this would be used with image content (still image or video frame) when only a portion of an integal image map pertains. If SHAPE is specified then COORDS must also be present. SHAPE should be used in conjunction with COORDS in the manner defined for the shape and coords attributes on an HTML4 <area> element. SHAPE must contain one of the following values: \nRECT \nCIRCLE\nPOLY\n\t\t\t\t')


    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ADMID'), 'ADMID', '__httpwww_loc_govMETS_areaType_ADMID', pyxb.binding.datatypes.IDREFS)

    ADMID = property(__ADMID.value, __ADMID.set, None, u'ADMID (IDREFS/O): Contains the ID attribute values identifying the <rightsMD>, <sourceMD>, <techMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain or link to administrative metadata pertaining to the content represented by the <area> element. Typically the <area> ADMID attribute would be used to identify the <rightsMD> element or elements that pertain to the <area>, but it could be used anytime there was a need to link an <area> with pertinent administrative metadata. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer\n\t\t\t\t')


    # Attribute CONTENTIDS uses Python identifier CONTENTIDS
    __CONTENTIDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CONTENTIDS'), 'CONTENTIDS', '__httpwww_loc_govMETS_areaType_CONTENTIDS', URIs)

    CONTENTIDS = property(__CONTENTIDS.value, __CONTENTIDS.set, None, u'CONTENTIDS (URI/O): Content IDs for the content represented by the <area> (equivalent to DIDL DII or Digital Item Identifier, a unique external ID).\n\t\t\t\t')


    # Attribute FILEID uses Python identifier FILEID
    __FILEID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'FILEID'), 'FILEID', '__httpwww_loc_govMETS_areaType_FILEID', pyxb.binding.datatypes.IDREF, required=True)

    FILEID = property(__FILEID.value, __FILEID.set, None, u'FILEID (IDREF/R): An attribute which provides the XML ID value that identifies the <file> element in the <fileSec> that then points to and/or contains the digital content represented by the <area> element. It must contain an ID value represented in an ID attribute associated with a <file> element in the <fileSec> element in the same METS document.\n\t\t\t\t')


    _ElementMap = {

    }
    _AttributeMap = {
        __BEGIN.name() : __BEGIN,
        __END.name() : __END,
        __BETYPE.name() : __BETYPE,
        __COORDS.name() : __COORDS,
        __ID.name() : __ID,
        __EXTENT.name() : __EXTENT,
        __EXTTYPE.name() : __EXTTYPE,
        __SHAPE.name() : __SHAPE,
        __ADMID.name() : __ADMID,
        __CONTENTIDS.name() : __CONTENTIDS,
        __FILEID.name() : __FILEID
    }
Namespace.addCategoryObject('typeBinding', u'areaType', areaType)


# Complex type behaviorSecType with content type ELEMENT_ONLY
class behaviorSecType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'behaviorSecType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}behaviorSec uses Python identifier behaviorSec
    __behaviorSec = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'behaviorSec'), 'behaviorSec', '__httpwww_loc_govMETS_behaviorSecType_httpwww_loc_govMETSbehaviorSec', True)


    behaviorSec = property(__behaviorSec.value, __behaviorSec.set, None, None)


    # Element {http://www.loc.gov/METS/}behavior uses Python identifier behavior
    __behavior = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'behavior'), 'behavior', '__httpwww_loc_govMETS_behaviorSecType_httpwww_loc_govMETSbehavior', True)


    behavior = property(__behavior.value, __behavior.set, None, u'\n\t\t\t\t\t\tA behavior element <behavior> can be used to associate executable behaviors with content in the METS document. This element has an interface definition <interfaceDef> element that represents an abstract definition of a set of behaviors represented by a particular behavior. A <behavior> element also has a behavior mechanism <mechanism> element, a module of executable code that implements and runs the behavior defined abstractly by the interface definition.\n\t\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_behaviorSecType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CREATED'), 'CREATED', '__httpwww_loc_govMETS_behaviorSecType_CREATED', pyxb.binding.datatypes.dateTime)

    CREATED = property(__CREATED.value, __CREATED.set, None, u'CREATED (dateTime/O): Specifies the date and time of creation for the <behaviorSec>\n\t\t\t\t')


    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__httpwww_loc_govMETS_behaviorSecType_LABEL', pyxb.binding.datatypes.string)

    LABEL = property(__LABEL.value, __LABEL.set, None, u'LABEL (string/O): A text description of the behavior section.\n\t\t\t\t')


    _ElementMap = {
        __behaviorSec.name() : __behaviorSec,
        __behavior.name() : __behavior
    }
    _AttributeMap = {
        __ID.name() : __ID,
        __CREATED.name() : __CREATED,
        __LABEL.name() : __LABEL
    }
Namespace.addCategoryObject('typeBinding', u'behaviorSecType', behaviorSecType)


# Complex type CTD_ANON_1 with content type SIMPLE
class CTD_ANON_1 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string

    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_1_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t\t\t\t')


    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TYPE'), 'TYPE', '__httpwww_loc_govMETS_CTD_ANON_1_TYPE', pyxb.binding.datatypes.string)

    TYPE = property(__TYPE.value, __TYPE.set, None, u'TYPE (string/O): A description of the identifier type.\n\t\t\t\t\t\t\t\t\t\t\t\t')


    _ElementMap = {

    }
    _AttributeMap = {
        __ID.name() : __ID,
        __TYPE.name() : __TYPE
    }



# Complex type divType with content type ELEMENT_ONLY
class divType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'divType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}div uses Python identifier div
    __div = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'div'), 'div', '__httpwww_loc_govMETS_divType_httpwww_loc_govMETSdiv', True)


    div = property(__div.value, __div.set, None, None)


    # Element {http://www.loc.gov/METS/}mptr uses Python identifier mptr
    __mptr = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'mptr'), 'mptr', '__httpwww_loc_govMETS_divType_httpwww_loc_govMETSmptr', True)


    mptr = property(__mptr.value, __mptr.set, None, u' \n\t\t\t\t\t\tLike the <fptr> element, the METS pointer element <mptr> represents digital content that manifests its parent <div> element. Unlike the <fptr>, which either directly or indirectly points to content represented in the <fileSec> of the parent METS document, the <mptr> element points to content represented by an external METS document. Thus, this element allows multiple discrete and separate METS documents to be organized at a higher level by a separate METS document. For example, METS documents representing the individual issues in the series of a journal could be grouped together and organized by a higher level METS document that represents the entire journal series. Each of the <div> elements in the <structMap> of the METS document representing the journal series would point to a METS document representing an issue.  It would do so via a child <mptr> element. Thus the <mptr> element gives METS users considerable flexibility in managing the depth of the <structMap> hierarchy of individual METS documents. The <mptr> element points to an external METS document by means of an xlink:href attribute and associated XLink attributes. \t\t\t\t\t\t\t\t\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}fptr uses Python identifier fptr
    __fptr = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'fptr'), 'fptr', '__httpwww_loc_govMETS_divType_httpwww_loc_govMETSfptr', True)


    fptr = property(__fptr.value, __fptr.set, None, u'\n\t\t\t\t\t\tThe <fptr> or file pointer element represents digital content that manifests its parent <div> element. The content represented by an <fptr> element must consist of integral files or parts of files that are represented by <file> elements in the <fileSec>. Via its FILEID attribute,  an <fptr> may point directly to a single integral <file> element that manifests a structural division. However, an <fptr> element may also govern an <area> element,  a <par>, or  a <seq>  which in turn would point to the relevant file or files. A child <area> element can point to part of a <file> that manifests a division, while the <par> and <seq> elements can point to multiple files or parts of files that together manifest a division. More than one <fptr> element can be associated with a <div> element. Typically sibling <fptr> elements represent alternative versions, or manifestations, of the same content\n\t\t\t\t\t')


    # Attribute CONTENTIDS uses Python identifier CONTENTIDS
    __CONTENTIDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CONTENTIDS'), 'CONTENTIDS', '__httpwww_loc_govMETS_divType_CONTENTIDS', URIs)

    CONTENTIDS = property(__CONTENTIDS.value, __CONTENTIDS.set, None, u'CONTENTIDS (URI/O): Content IDs for the content represented by the <div> (equivalent to DIDL DII or Digital Item Identifier, a unique external ID).\n\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'label'), 'label', '__httpwww_loc_govMETS_divType_httpwww_w3_org1999xlinklabel', pyxb.binding.datatypes.string)

    label = property(__label.value, __label.set, None, None)


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_divType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute ORDER uses Python identifier ORDER
    __ORDER = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ORDER'), 'ORDER', '__httpwww_loc_govMETS_divType_ORDER', pyxb.binding.datatypes.integer)

    ORDER = property(__ORDER.value, __ORDER.set, None, u"ORDER (integer/O): A representation of the div's order among its siblings (e.g., its absolute, numeric sequence). For an example, and clarification of the distinction between ORDER and ORDERLABEL, see the description of the ORDERLABEL attribute.\n\t\t\t\t")


    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ADMID'), 'ADMID', '__httpwww_loc_govMETS_divType_ADMID', pyxb.binding.datatypes.IDREFS)

    ADMID = property(__ADMID.value, __ADMID.set, None, u'ADMID (IDREFS/O): Contains the ID attribute values identifying the <rightsMD>, <sourceMD>, <techMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain or link to administrative metadata pertaining to the structural division represented by the <div> element. Typically the <div> ADMID attribute would be used to identify the <rightsMD> element or elements that pertain to the <div>, but it could be used anytime there was a need to link a <div> with pertinent administrative metadata. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__httpwww_loc_govMETS_divType_LABEL', pyxb.binding.datatypes.string)

    LABEL = property(__LABEL.value, __LABEL.set, None, u'LABEL (string/O): An attribute used, for example, to identify a <div> to an end user viewing the document. Thus a hierarchical arrangement of the <div> LABEL values could provide a table of contents to the digital content represented by a METS document and facilitate the users\u2019 navigation of the digital object. Note that a <div> LABEL should be specific to its level in the structural map. In the case of a book with chapters, the book <div> LABEL should have the book title and the chapter <div>; LABELs should have the individual chapter titles, rather than having the chapter <div> LABELs combine both book title and chapter title . For further of the distinction between LABEL and ORDERLABEL see the description of the ORDERLABEL attribute.\n\t\t\t\t')


    # Attribute ORDERLABEL uses Python identifier ORDERLABEL
    __ORDERLABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ORDERLABEL'), 'ORDERLABEL', '__httpwww_loc_govMETS_divType_ORDERLABEL', pyxb.binding.datatypes.string)

    ORDERLABEL = property(__ORDERLABEL.value, __ORDERLABEL.set, None, u"ORDERLABEL (string/O): A representation of the div's order among its siblings (e.g., \u201cxii\u201d), or of any non-integer native numbering system. It is presumed that this value will still be machine actionable (e.g., it would support \u2018go to page ___\u2019 function), and it should not be used as a replacement/substitute for the LABEL attribute. To understand the differences between ORDER, ORDERLABEL and LABEL, imagine a text with 10 roman numbered pages followed by 10 arabic numbered pages. Page iii would have an ORDER of \u201c3\u201d, an ORDERLABEL of \u201ciii\u201d and a LABEL of \u201cPage iii\u201d, while page 3 would have an ORDER of \u201c13\u201d, an ORDERLABEL of \u201c3\u201d and a LABEL of \u201cPage 3\u201d.\n\t\t\t\t")


    # Attribute DMDID uses Python identifier DMDID
    __DMDID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'DMDID'), 'DMDID', '__httpwww_loc_govMETS_divType_DMDID', pyxb.binding.datatypes.IDREFS)

    DMDID = property(__DMDID.value, __DMDID.set, None, u'DMDID (IDREFS/O): Contains the ID attribute values identifying the <dmdSec>, elements in the METS document that contain or link to descriptive metadata pertaining to the structural division represented by the current <div> element.  For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TYPE'), 'TYPE', '__httpwww_loc_govMETS_divType_TYPE', pyxb.binding.datatypes.string)

    TYPE = property(__TYPE.value, __TYPE.set, None, u'TYPE (string/O): An attribute that specifies the type of structural division that the <div> element represents. Possible <div> TYPE attribute values include: chapter, article, page, track, segment, section etc. METS places no constraints on the possible TYPE values. Suggestions for controlled vocabularies for TYPE may be found on the METS website.\n\t\t\t\t')


    _ElementMap = {
        __div.name() : __div,
        __mptr.name() : __mptr,
        __fptr.name() : __fptr
    }
    _AttributeMap = {
        __CONTENTIDS.name() : __CONTENTIDS,
        __label.name() : __label,
        __ID.name() : __ID,
        __ORDER.name() : __ORDER,
        __ADMID.name() : __ADMID,
        __LABEL.name() : __LABEL,
        __ORDERLABEL.name() : __ORDERLABEL,
        __DMDID.name() : __DMDID,
        __TYPE.name() : __TYPE
    }
Namespace.addCategoryObject('typeBinding', u'divType', divType)


# Complex type CTD_ANON_2 with content type SIMPLE
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string

    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_2_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t\t\t\t')


    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TYPE'), 'TYPE', '__httpwww_loc_govMETS_CTD_ANON_2_TYPE', pyxb.binding.datatypes.string)

    TYPE = property(__TYPE.value, __TYPE.set, None, u'TYPE (string/O): A description of the identifier type (e.g., OCLC record number, LCCN, etc.).\n\t\t\t\t\t\t\t\t\t\t\t\t')


    _ElementMap = {

    }
    _AttributeMap = {
        __ID.name() : __ID,
        __TYPE.name() : __TYPE
    }



# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}smLocatorLink uses Python identifier smLocatorLink
    __smLocatorLink = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'smLocatorLink'), 'smLocatorLink', '__httpwww_loc_govMETS_CTD_ANON_3_httpwww_loc_govMETSsmLocatorLink', True)


    smLocatorLink = property(__smLocatorLink.value, __smLocatorLink.set, None, u'\n\t\t\t\t\t\t\t\t\tThe structMap locator link element <smLocatorLink> is of xlink:type "locator".  It provides a means of identifying a <div> element that will participate in one or more of the links specified by means of <smArcLink> elements within the same <smLinkGrp>. The participating <div> element that is represented by the <smLocatorLink> is identified by means of a URI in the associate xlink:href attribute.  The lowest level of this xlink:href URI value should be a fragment identifier that references the ID value that identifies the relevant <div> element.  For example, "xlink:href=\'#div20\'" where "div20" is the ID value that identifies the pertinent <div> in the current METS document. Although not required by the xlink specification, an <smLocatorLink> element will typically include an xlink:label attribute in this context, as the <smArcLink> elements will reference these labels to establish the from and to sides of each arc link.\n\t\t\t\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}smArcLink uses Python identifier smArcLink
    __smArcLink = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'smArcLink'), 'smArcLink', '__httpwww_loc_govMETS_CTD_ANON_3_httpwww_loc_govMETSsmArcLink', True)


    smArcLink = property(__smArcLink.value, __smArcLink.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_3_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)

    role = property(__role.value, __role.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_3_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'extended')

    type = property(__type.value, __type.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_3_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)

    title = property(__title.value, __title.set, None, None)


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_3_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, None)


    # Attribute ARCLINKORDER uses Python identifier ARCLINKORDER
    __ARCLINKORDER = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ARCLINKORDER'), 'ARCLINKORDER', '__httpwww_loc_govMETS_CTD_ANON_3_ARCLINKORDER', STD_ANON_4, unicode_default=u'unordered')

    ARCLINKORDER = property(__ARCLINKORDER.value, __ARCLINKORDER.set, None, u'ARCLINKORDER (enumerated string/O): ARCLINKORDER is used to indicate whether the order of the smArcLink elements aggregated by the smLinkGrp element is significant. If the order is significant, then a value of "ordered" should be supplied.  Value defaults to "unordered" Note that the ARLINKORDER attribute has no xlink specified meaning.')


    _ElementMap = {
        __smLocatorLink.name() : __smLocatorLink,
        __smArcLink.name() : __smArcLink
    }
    _AttributeMap = {
        __role.name() : __role,
        __type.name() : __type,
        __title.name() : __title,
        __ID.name() : __ID,
        __ARCLINKORDER.name() : __ARCLINKORDER
    }



# Complex type CTD_ANON_4 with content type EMPTY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_4_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)

    role = property(__role.value, __role.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)

    title = property(__title.value, __title.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)

    href = property(__href.value, __href.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)

    arcrole = property(__arcrole.value, __arcrole.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinkshow', _xlink.STD_ANON_1)

    show = property(__show.value, __show.set, None, None)


    # Attribute CONTENTIDS uses Python identifier CONTENTIDS
    __CONTENTIDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CONTENTIDS'), 'CONTENTIDS', '__httpwww_loc_govMETS_CTD_ANON_4_CONTENTIDS', URIs)

    CONTENTIDS = property(__CONTENTIDS.value, __CONTENTIDS.set, None, u'CONTENTIDS (URI/O): Content IDs for the content represented by the <mptr> (equivalent to DIDL DII or Digital Item Identifier, a unique external ID).\n\t\t\t\t            ')


    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinkactuate', _xlink.STD_ANON_2)

    actuate = property(__actuate.value, __actuate.set, None, None)


    # Attribute LOCTYPE uses Python identifier LOCTYPE
    __LOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LOCTYPE'), 'LOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_4_LOCTYPE', STD_ANON_5, required=True)

    LOCTYPE = property(__LOCTYPE.value, __LOCTYPE.set, None, u'LOCTYPE (string/R): Specifies the locator type used in the xlink:href attribute. Valid values for LOCTYPE are: \n\t\t\t\t\tARK\n\t\t\t\t\tURN\n\t\t\t\t\tURL\n\t\t\t\t\tPURL\n\t\t\t\t\tHANDLE\n\t\t\t\t\tDOI\n\t\t\t\t\tOTHER\n\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')

    type = property(__type.value, __type.set, None, None)


    # Attribute OTHERLOCTYPE uses Python identifier OTHERLOCTYPE
    __OTHERLOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OTHERLOCTYPE'), 'OTHERLOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_4_OTHERLOCTYPE', pyxb.binding.datatypes.string)

    OTHERLOCTYPE = property(__OTHERLOCTYPE.value, __OTHERLOCTYPE.set, None, u'OTHERLOCTYPE (string/O): Specifies the locator type when the value OTHER is used in the LOCTYPE attribute. Although optional, it is strongly recommended when OTHER is used.\n\t\t\t\t')


    _ElementMap = {

    }
    _AttributeMap = {
        __ID.name() : __ID,
        __role.name() : __role,
        __title.name() : __title,
        __href.name() : __href,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __CONTENTIDS.name() : __CONTENTIDS,
        __actuate.name() : __actuate,
        __LOCTYPE.name() : __LOCTYPE,
        __type.name() : __type,
        __OTHERLOCTYPE.name() : __OTHERLOCTYPE
    }



# Complex type CTD_ANON_5 with content type EMPTY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_5_httpwww_w3_org1999xlinkshow', _xlink.STD_ANON_1)

    show = property(__show.value, __show.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_5_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')

    type = property(__type.value, __type.set, None, None)


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_5_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_5_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)

    role = property(__role.value, __role.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_5_httpwww_w3_org1999xlinkactuate', _xlink.STD_ANON_2)

    actuate = property(__actuate.value, __actuate.set, None, None)


    # Attribute OTHERLOCTYPE uses Python identifier OTHERLOCTYPE
    __OTHERLOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OTHERLOCTYPE'), 'OTHERLOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_5_OTHERLOCTYPE', pyxb.binding.datatypes.string)

    OTHERLOCTYPE = property(__OTHERLOCTYPE.value, __OTHERLOCTYPE.set, None, u'OTHERLOCTYPE (string/O): Specifies the locator type when the value OTHER is used in the LOCTYPE attribute. Although optional, it is strongly recommended when OTHER is used.\n\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_5_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)

    title = property(__title.value, __title.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_5_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)

    arcrole = property(__arcrole.value, __arcrole.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_loc_govMETS_CTD_ANON_5_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)

    href = property(__href.value, __href.set, None, None)


    # Attribute USE uses Python identifier USE
    __USE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'USE'), 'USE', '__httpwww_loc_govMETS_CTD_ANON_5_USE', pyxb.binding.datatypes.string)

    USE = property(__USE.value, __USE.set, None, u'USE (string/O): A tagging attribute to indicate the intended use of the specific copy of the file  represented by the <FLocat> element (e.g., service master, archive master). A USE attribute can be expressed at the<fileGrp> level, the <file> level, the <FLocat> level and/or the <FContent> level.  A USE attribute value at the <fileGrp> level should pertain to all of the files in the <fileGrp>.  A USE attribute at the <file> level should pertain to all copies of the file as represented by subsidiary <FLocat> and/or <FContent> elements.  A USE attribute at the <FLocat> or <FContent> level pertains to the particular copy of the file that is either referenced (<FLocat>) or wrapped (<FContent>).\n\t\t\t\t\t\t\t')


    # Attribute LOCTYPE uses Python identifier LOCTYPE
    __LOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LOCTYPE'), 'LOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_5_LOCTYPE', STD_ANON_5, required=True)

    LOCTYPE = property(__LOCTYPE.value, __LOCTYPE.set, None, u'LOCTYPE (string/R): Specifies the locator type used in the xlink:href attribute. Valid values for LOCTYPE are: \n\t\t\t\t\tARK\n\t\t\t\t\tURN\n\t\t\t\t\tURL\n\t\t\t\t\tPURL\n\t\t\t\t\tHANDLE\n\t\t\t\t\tDOI\n\t\t\t\t\tOTHER\n\t\t\t\t')


    _ElementMap = {

    }
    _AttributeMap = {
        __show.name() : __show,
        __type.name() : __type,
        __ID.name() : __ID,
        __role.name() : __role,
        __actuate.name() : __actuate,
        __OTHERLOCTYPE.name() : __OTHERLOCTYPE,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __href.name() : __href,
        __USE.name() : __USE,
        __LOCTYPE.name() : __LOCTYPE
    }



# Complex type objectType with content type EMPTY
class objectType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'objectType')
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkactuate', _xlink.STD_ANON_2)

    actuate = property(__actuate.value, __actuate.set, None, None)


    # Attribute LOCTYPE uses Python identifier LOCTYPE
    __LOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LOCTYPE'), 'LOCTYPE', '__httpwww_loc_govMETS_objectType_LOCTYPE', STD_ANON_5, required=True)

    LOCTYPE = property(__LOCTYPE.value, __LOCTYPE.set, None, u'LOCTYPE (string/R): Specifies the locator type used in the xlink:href attribute. Valid values for LOCTYPE are: \n\t\t\t\t\tARK\n\t\t\t\t\tURN\n\t\t\t\t\tURL\n\t\t\t\t\tPURL\n\t\t\t\t\tHANDLE\n\t\t\t\t\tDOI\n\t\t\t\t\tOTHER\n\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)

    href = property(__href.value, __href.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')

    type = property(__type.value, __type.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkshow', _xlink.STD_ANON_1)

    show = property(__show.value, __show.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)

    title = property(__title.value, __title.set, None, None)


    # Attribute OTHERLOCTYPE uses Python identifier OTHERLOCTYPE
    __OTHERLOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OTHERLOCTYPE'), 'OTHERLOCTYPE', '__httpwww_loc_govMETS_objectType_OTHERLOCTYPE', pyxb.binding.datatypes.string)

    OTHERLOCTYPE = property(__OTHERLOCTYPE.value, __OTHERLOCTYPE.set, None, u'OTHERLOCTYPE (string/O): Specifies the locator type when the value OTHER is used in the LOCTYPE attribute. Although optional, it is strongly recommended when OTHER is used.\n\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)

    role = property(__role.value, __role.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)

    arcrole = property(__arcrole.value, __arcrole.set, None, None)


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_objectType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__httpwww_loc_govMETS_objectType_LABEL', pyxb.binding.datatypes.string)

    LABEL = property(__LABEL.value, __LABEL.set, None, u'LABEL (string/O): A text description of the entity represented.\n\t\t\t\t')


    _ElementMap = {

    }
    _AttributeMap = {
        __actuate.name() : __actuate,
        __LOCTYPE.name() : __LOCTYPE,
        __href.name() : __href,
        __type.name() : __type,
        __show.name() : __show,
        __title.name() : __title,
        __OTHERLOCTYPE.name() : __OTHERLOCTYPE,
        __role.name() : __role,
        __arcrole.name() : __arcrole,
        __ID.name() : __ID,
        __LABEL.name() : __LABEL
    }
Namespace.addCategoryObject('typeBinding', u'objectType', objectType)


# Complex type CTD_ANON_6 with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True

    _ElementMap = {

    }
    _AttributeMap = {

    }



# Complex type CTD_ANON_7 with content type EMPTY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_loc_govMETS_CTD_ANON_7_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI, required=True)

    href = property(__href.value, __href.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_7_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)

    role = property(__role.value, __role.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_7_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'locator')

    type = property(__type.value, __type.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'label'), 'label', '__httpwww_loc_govMETS_CTD_ANON_7_httpwww_w3_org1999xlinklabel', pyxb.binding.datatypes.string)

    label = property(__label.value, __label.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_7_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)

    title = property(__title.value, __title.set, None, None)


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_7_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.')


    _ElementMap = {

    }
    _AttributeMap = {
        __href.name() : __href,
        __role.name() : __role,
        __type.name() : __type,
        __label.name() : __label,
        __title.name() : __title,
        __ID.name() : __ID
    }



# Complex type mdSecType with content type ELEMENT_ONLY
class mdSecType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'mdSecType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}mdRef uses Python identifier mdRef
    __mdRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'mdRef'), 'mdRef', '__httpwww_loc_govMETS_mdSecType_httpwww_loc_govMETSmdRef', False)


    mdRef = property(__mdRef.value, __mdRef.set, None, u'\n\t\t\t\t\t\tThe metadata reference element <mdRef> element is a generic element used throughout the METS schema to provide a pointer to metadata which resides outside the METS document.  NB: <mdRef> is an empty element.  The location of the metadata must be recorded in the xlink:href attribute, supplemented by the XPTR attribute as needed.\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}mdWrap uses Python identifier mdWrap
    __mdWrap = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'mdWrap'), 'mdWrap', '__httpwww_loc_govMETS_mdSecType_httpwww_loc_govMETSmdWrap', False)


    mdWrap = property(__mdWrap.value, __mdWrap.set, None, u' \n\t\t\t\t\t\tA metadata wrapper element <mdWrap> provides a wrapper around metadata embedded within a METS document. The element is repeatable. Such metadata can be in one of two forms: 1) XML-encoded metadata, with the XML-encoding identifying itself as belonging to a namespace other than the METS document namespace. 2) Any arbitrary binary or textual form, PROVIDED that the metadata is Base64 encoded and wrapped in a <binData> element within the internal descriptive metadata element.\n\t\t\t\t\t')


    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ADMID'), 'ADMID', '__httpwww_loc_govMETS_mdSecType_ADMID', pyxb.binding.datatypes.IDREFS)

    ADMID = property(__ADMID.value, __ADMID.set, None, u'ADMID (IDREFS/O): Contains the ID attribute values of the <digiprovMD>, <techMD>, <sourceMD> and/or <rightsMD> elements within the <amdSec> of the METS document that contain administrative metadata pertaining to the current mdSecType element. Typically used in this context to reference preservation metadata (digiprovMD) which applies to the current metadata. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute GROUPID uses Python identifier GROUPID
    __GROUPID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'GROUPID'), 'GROUPID', '__httpwww_loc_govMETS_mdSecType_GROUPID', pyxb.binding.datatypes.string)

    GROUPID = property(__GROUPID.value, __GROUPID.set, None, u'GROUPID (string/O): This identifier is used to indicate that different metadata sections may be considered as part of a group. Two metadata sections with the same GROUPID value are to be considered part of the same group. For example this facility might be used to group changed versions of the same metadata if previous versions are maintained in a file for tracking purposes.\n\t\t\t\t')


    # Attribute STATUS uses Python identifier STATUS
    __STATUS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'STATUS'), 'STATUS', '__httpwww_loc_govMETS_mdSecType_STATUS', pyxb.binding.datatypes.string)

    STATUS = property(__STATUS.value, __STATUS.set, None, u'STATUS (string/O): Indicates the status of this metadata (e.g., superseded, current, etc.).\n\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_mdSecType_ID', pyxb.binding.datatypes.ID, required=True)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/R): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. The ID attribute on the <dmdSec>, <techMD>, <sourceMD>, <rightsMD> and <digiprovMD> elements (which are all of mdSecType) is required, and its value should be referenced from one or more DMDID attributes (when the ID identifies a <dmdSec> element) or ADMID attributes (when the ID identifies a <techMD>, <sourceMD>, <rightsMD> or <digiprovMD> element) that are associated with other elements in the METS document. The following elements support references to a <dmdSec> via a DMDID attribute: <file>, <stream>, <div>.  The following elements support references to <techMD>, <sourceMD>, <rightsMD> and <digiprovMD> elements via an ADMID attribute: <metsHdr>, <dmdSec>, <techMD>, <sourceMD>, <rightsMD>, <digiprovMD>, <fileGrp>, <file>, <stream>, <div>, <area>, <behavior>. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CREATED'), 'CREATED', '__httpwww_loc_govMETS_mdSecType_CREATED', pyxb.binding.datatypes.dateTime)

    CREATED = property(__CREATED.value, __CREATED.set, None, u'CREATED (dateTime/O): Specifies the date and time of creation for the metadata.\n\t\t\t\t')


    _ElementMap = {
        __mdRef.name() : __mdRef,
        __mdWrap.name() : __mdWrap
    }
    _AttributeMap = {
        __ADMID.name() : __ADMID,
        __GROUPID.name() : __GROUPID,
        __STATUS.name() : __STATUS,
        __ID.name() : __ID,
        __CREATED.name() : __CREATED
    }
Namespace.addCategoryObject('typeBinding', u'mdSecType', mdSecType)


# Complex type amdSecType with content type ELEMENT_ONLY
class amdSecType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'amdSecType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}techMD uses Python identifier techMD
    __techMD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'techMD'), 'techMD', '__httpwww_loc_govMETS_amdSecType_httpwww_loc_govMETStechMD', True)


    techMD = property(__techMD.value, __techMD.set, None, u' \n\t\t\t\t\t\tA technical metadata element <techMD> records technical metadata about a component of the METS object, such as a digital content file. The <techMD> element conforms to same generic datatype as the <dmdSec>, <rightsMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes.  A technical metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <techMD> elements; and technical metadata can be associated with any METS element that supports an ADMID attribute. Technical metadata can be expressed according to many current technical description standards (such as MIX and textMD) or a locally produced XML schema.\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}digiprovMD uses Python identifier digiprovMD
    __digiprovMD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'digiprovMD'), 'digiprovMD', '__httpwww_loc_govMETS_amdSecType_httpwww_loc_govMETSdigiprovMD', True)


    digiprovMD = property(__digiprovMD.value, __digiprovMD.set, None, u'\n\t\t\t\t\t\tA digital provenance metadata element <digiprovMD> can be used to record any preservation-related actions taken on the various files which comprise a digital object (e.g., those subsequent to the initial digitization of the files such as transformation or migrations) or, in the case of born digital materials, the files\u2019 creation. In short, digital provenance should be used to record information that allows both archival/library staff and scholars to understand what modifications have been made to a digital object and/or its constituent parts during its life cycle. This information can then be used to judge how those processes might have altered or corrupted the object\u2019s ability to accurately represent the original item. One might, for example, record master derivative relationships and the process by which those derivations have been created. Or the <digiprovMD> element could contain information regarding the migration/transformation of a file from its original digitization (e.g., OCR, TEI, etc.,)to its current incarnation as a digital object (e.g., JPEG2000). The <digiprovMD> element conforms to same generic datatype as the <dmdSec>,  <techMD>, <rightsMD>, and <sourceMD> elements, and supports the same sub-elements and attributes. A digital provenance metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <digiprovMD> elements; and digital provenance metadata can be associated with any METS element that supports an ADMID attribute. Digital provenance metadata can be expressed according to current digital provenance description standards (such as PREMIS) or a locally produced XML schema.\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}rightsMD uses Python identifier rightsMD
    __rightsMD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'rightsMD'), 'rightsMD', '__httpwww_loc_govMETS_amdSecType_httpwww_loc_govMETSrightsMD', True)


    rightsMD = property(__rightsMD.value, __rightsMD.set, None, u'\n\t\t\t\t\t\tAn intellectual property rights metadata element <rightsMD> records information about copyright and licensing pertaining to a component of the METS object. The <rightsMD> element conforms to same generic datatype as the <dmdSec>, <techMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes. A rights metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <rightsMD> elements; and rights metadata can be associated with any METS element that supports an ADMID attribute. Rights metadata can be expressed according current rights description standards (such as CopyrightMD and rightsDeclarationMD) or a locally produced XML schema.\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}sourceMD uses Python identifier sourceMD
    __sourceMD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'sourceMD'), 'sourceMD', '__httpwww_loc_govMETS_amdSecType_httpwww_loc_govMETSsourceMD', True)


    sourceMD = property(__sourceMD.value, __sourceMD.set, None, u'\n\t\t\t\t\t\tA source metadata element <sourceMD> records descriptive and administrative metadata about the source format or media of a component of the METS object such as a digital content file. It is often used for discovery, data administration or preservation of the digital object. The <sourceMD> element conforms to same generic datatype as the <dmdSec>, <techMD>, <rightsMD>,  and <digiprovMD> elements, and supports the same sub-elements and attributes.  A source metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <sourceMD> elements; and source metadata can be associated with any METS element that supports an ADMID attribute. Source metadata can be expressed according to current source description standards (such as PREMIS) or a locally produced XML schema.\n\t\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_amdSecType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    _ElementMap = {
        __techMD.name() : __techMD,
        __digiprovMD.name() : __digiprovMD,
        __rightsMD.name() : __rightsMD,
        __sourceMD.name() : __sourceMD
    }
    _AttributeMap = {
        __ID.name() : __ID
    }
Namespace.addCategoryObject('typeBinding', u'amdSecType', amdSecType)


# Complex type CTD_ANON_8 with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}fileGrp uses Python identifier fileGrp
    __fileGrp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'), 'fileGrp', '__httpwww_loc_govMETS_CTD_ANON_8_httpwww_loc_govMETSfileGrp', True)


    fileGrp = property(__fileGrp.value, __fileGrp.set, None, u' \n\t\t\t\t\t\t\t\t\tA sequence of file group elements <fileGrp> can be used group the digital files comprising the content of a METS object either into a flat arrangement or, because each file group element can itself contain one or more  file group elements,  into a nested (hierarchical) arrangement. In the case where the content files are images of different formats and resolutions, for example, one could group the image content files by format and create a separate <fileGrp> for each image format/resolution such as:\n-- one <fileGrp> for the thumbnails of the images\n-- one <fileGrp> for the higher resolution JPEGs of the image \n-- one <fileGrp> for the master archival TIFFs of the images \nFor a text resource with a variety of content file types one might group the content files at the highest level by type,  and then use the <fileGrp> element\u2019s nesting capabilities to subdivide a <fileGrp> by format within the type, such as:\n-- one <fileGrp> for all of the page images with nested <fileGrp> elements for each image format/resolution (tiff, jpeg, gif)\n-- one <fileGrp> for a PDF version of all the pages of the document \n-- one <fileGrp> for  a TEI encoded XML version of the entire document or each of its pages.\nA <fileGrp> may contain zero or more <fileGrp> elements and or <file> elements.\t\t\t\t\t\n\t\t\t\t\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_8_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    _ElementMap = {
        __fileGrp.name() : __fileGrp
    }
    _AttributeMap = {
        __ID.name() : __ID
    }



# Complex type fileGrpType with content type ELEMENT_ONLY
class fileGrpType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'fileGrpType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}file uses Python identifier file
    __file = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'file'), 'file', '__httpwww_loc_govMETS_fileGrpType_httpwww_loc_govMETSfile', True)


    file = property(__file.value, __file.set, None, u'\n\t\t\t\t\t\tThe file element <file> provides access to the content files for the digital object being described by the METS document. A <file> element may contain one or more <FLocat> elements which provide pointers to a content file and/or a <FContent> element which wraps an encoded version of the file. Embedding files using <FContent> can be a valuable feature for exchanging digital objects between repositories or for archiving versions of digital objects for off-site storage. All <FLocat> and <FContent> elements should identify and/or contain identical copies of a single file. The <file> element is recursive, thus allowing sub-files or component files of a larger file to be listed in the inventory. Alternatively, by using the <stream> element, a smaller component of a file or of a related file can be placed within a <file> element. Finally, by using the <transformFile> element, it is possible to include within a <file> element a different version of a file that has undergone a transformation for some reason, such as format migration.\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}fileGrp uses Python identifier fileGrp
    __fileGrp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'), 'fileGrp', '__httpwww_loc_govMETS_fileGrpType_httpwww_loc_govMETSfileGrp', True)


    fileGrp = property(__fileGrp.value, __fileGrp.set, None, None)


    # Attribute USE uses Python identifier USE
    __USE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'USE'), 'USE', '__httpwww_loc_govMETS_fileGrpType_USE', pyxb.binding.datatypes.string)

    USE = property(__USE.value, __USE.set, None, u'USE (string/O): A tagging attribute to indicate the intended use of files within this file group (e.g., master, reference, thumbnails for image files). A USE attribute can be expressed at the<fileGrp> level, the <file> level, the <FLocat> level and/or the <FContent> level.  A USE attribute value at the <fileGrp> level should pertain to all of the files in the <fileGrp>.  A USE attribute at the <file> level should pertain to all copies of the file as represented by subsidiary <FLocat> and/or <FContent> elements.  A USE attribute at the <FLocat> or <FContent> level pertains to the particular copy of the file that is either referenced (<FLocat>) or wrapped (<FContent>). \n\t\t\t\t')


    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ADMID'), 'ADMID', '__httpwww_loc_govMETS_fileGrpType_ADMID', pyxb.binding.datatypes.IDREFS)

    ADMID = property(__ADMID.value, __ADMID.set, None, u'ADMID (IDREF/O): Contains the ID attribute values of the <techMD>, <sourceMD>, <rightsMD> and/or <digiprovMD> elements within the <amdSec> of the METS document applicable to all of the files in a particular file group. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_fileGrpType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute VERSDATE uses Python identifier VERSDATE
    __VERSDATE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'VERSDATE'), 'VERSDATE', '__httpwww_loc_govMETS_fileGrpType_VERSDATE', pyxb.binding.datatypes.dateTime)

    VERSDATE = property(__VERSDATE.value, __VERSDATE.set, None, u'VERSDATE (dateTime/O): An optional dateTime attribute specifying the date this version/fileGrp of the digital object was created.\n\t\t\t\t')


    _ElementMap = {
        __file.name() : __file,
        __fileGrp.name() : __fileGrp
    }
    _AttributeMap = {
        __USE.name() : __USE,
        __ADMID.name() : __ADMID,
        __ID.name() : __ID,
        __VERSDATE.name() : __VERSDATE
    }
Namespace.addCategoryObject('typeBinding', u'fileGrpType', fileGrpType)


# Complex type CTD_ANON_9 with content type ELEMENT_ONLY
class CTD_ANON_9 (fileGrpType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is fileGrpType

    # Element file ({http://www.loc.gov/METS/}file) inherited from {http://www.loc.gov/METS/}fileGrpType

    # Element fileGrp ({http://www.loc.gov/METS/}fileGrp) inherited from {http://www.loc.gov/METS/}fileGrpType

    # Attribute VERSDATE inherited from {http://www.loc.gov/METS/}fileGrpType

    # Attribute ID inherited from {http://www.loc.gov/METS/}fileGrpType

    # Attribute USE inherited from {http://www.loc.gov/METS/}fileGrpType

    # Attribute ADMID inherited from {http://www.loc.gov/METS/}fileGrpType

    _ElementMap = fileGrpType._ElementMap.copy()
    _ElementMap.update({

    })
    _AttributeMap = fileGrpType._AttributeMap.copy()
    _AttributeMap.update({

    })



# Complex type metsType with content type ELEMENT_ONLY
class metsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'metsType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}behaviorSec uses Python identifier behaviorSec
    __behaviorSec = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'behaviorSec'), 'behaviorSec', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSbehaviorSec', True)


    behaviorSec = property(__behaviorSec.value, __behaviorSec.set, None, u'\n\t\t\t\t\t\tA behavior section element <behaviorSec> associates executable behaviors with content in the METS document by means of a repeatable behavior <behavior> element. This element has an interface definition <interfaceDef> element that represents an abstract definition of the set of behaviors represented by a particular behavior section. A <behavior> element also has a <mechanism> element which is used to point to a module of executable code that implements and runs the behavior defined by the interface definition. The <behaviorSec> element, which is repeatable as well as nestable, can be used to group individual behaviors within the structure of the METS document. Such grouping can be useful for organizing families of behaviors together or to indicate other relationships between particular behaviors.')


    # Element {http://www.loc.gov/METS/}structLink uses Python identifier structLink
    __structLink = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'structLink'), 'structLink', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSstructLink', False)


    structLink = property(__structLink.value, __structLink.set, None, u' \n\t\t\t\t\t\tThe structural link section element <structLink> allows for the specification of hyperlinks between the different components of a METS structure that are delineated in a structural map. This element is a container for a single, repeatable element, <smLink> which indicates a hyperlink between two nodes in the structural map. The <structLink> section in the METS document is identified using its XML ID attributes.\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}structMap uses Python identifier structMap
    __structMap = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'structMap'), 'structMap', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSstructMap', True)


    structMap = property(__structMap.value, __structMap.set, None, u' \n\t\t\t\t\t\tThe structural map section <structMap> is the heart of a METS document. It provides a means for organizing the digital content represented by the <file> elements in the <fileSec> of the METS document into a coherent hierarchical structure. Such a hierarchical structure can be presented to users to facilitate their comprehension and navigation of the digital content. It can further be applied to any purpose requiring an understanding of the structural relationship of the content files or parts of the content files. The organization may be specified to any level of granularity (intellectual and or physical) that is desired. Since the <structMap> element is repeatable, more than one organization can be applied to the digital content represented by the METS document.  The hierarchical structure specified by a <structMap> is encoded as a tree of nested <div> elements. A <div> element may directly point to content via child file pointer <fptr> elements (if the content is represented in the <fileSec<) or child METS pointer <mptr> elements (if the content is represented by an external METS document). The <fptr> element may point to a single whole <file> element that manifests its parent <div<, or to part of a <file> that manifests its <div<. It can also point to multiple files or parts of files that must be played/displayed either in sequence or in parallel to reveal its structural division. In addition to providing a means for organizing content, the <structMap> provides a mechanism for linking content at any hierarchical level with relevant descriptive and administrative metadata.\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}dmdSec uses Python identifier dmdSec
    __dmdSec = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dmdSec'), 'dmdSec', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSdmdSec', True)


    dmdSec = property(__dmdSec.value, __dmdSec.set, None, u'\n\t\t\t\t\t\tA descriptive metadata section <dmdSec> records descriptive metadata pertaining to the METS object as a whole or one of its components. The <dmdSec> element conforms to same generic datatype as the <techMD>, <rightsMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes. A descriptive metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <dmdSec> elements; and descriptive metadata can be associated with any METS element that supports a DMDID attribute.  Descriptive metadata can be expressed according to many current description standards (i.e., MARC, MODS, Dublin Core, TEI Header, EAD, VRA, FGDC, DDI) or a locally produced XML schema. \n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}metsHdr uses Python identifier metsHdr
    __metsHdr = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'metsHdr'), 'metsHdr', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSmetsHdr', False)


    metsHdr = property(__metsHdr.value, __metsHdr.set, None, u' \n\t\t\t\t\tThe mets header element <metsHdr> captures metadata about the METS document itself, not the digital object the METS document encodes. Although it records a more limited set of metadata, it is very similar in function and purpose to the headers employed in other schema such as the Text Encoding Initiative (TEI) or in the Encoded Archival Description (EAD).\n\t\t\t')


    # Element {http://www.loc.gov/METS/}amdSec uses Python identifier amdSec
    __amdSec = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'amdSec'), 'amdSec', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSamdSec', True)


    amdSec = property(__amdSec.value, __amdSec.set, None, u' \n\t\t\t\t\t\tThe administrative metadata section <amdSec> contains the administrative metadata pertaining to the digital object, its components and any original source material from which the digital object is derived. The <amdSec> is separated into four sub-sections that accommodate technical metadata (techMD), intellectual property rights (rightsMD), analog/digital source metadata (sourceMD), and digital provenance metadata (digiprovMD). Each of these subsections can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both. Multiple instances of the <amdSec> element can occur within a METS document and multiple instances of its subsections can occur in one <amdSec> element. This allows considerable flexibility in the structuring of the administrative metadata. METS does not define a vocabulary or syntax for encoding administrative metadata. Administrative metadata can be expressed within the amdSec sub-elements according to many current community defined standards, or locally produced XML schemas. ')


    # Element {http://www.loc.gov/METS/}fileSec uses Python identifier fileSec
    __fileSec = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'fileSec'), 'fileSec', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSfileSec', False)


    fileSec = property(__fileSec.value, __fileSec.set, None, u' \n\t\t\t\t\t\tThe overall purpose of the content file section element <fileSec> is to provide an inventory of and the location for the content files that comprise the digital object being described in the METS document.\n\t\t\t\t\t')


    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TYPE'), 'TYPE', '__httpwww_loc_govMETS_metsType_TYPE', pyxb.binding.datatypes.string)

    TYPE = property(__TYPE.value, __TYPE.set, None, u'TYPE (string/O): Specifies the class or type of the object, e.g.: book, journal, stereograph, dataset, video, etc.\n\t\t\t\t')


    # Attribute OBJID uses Python identifier OBJID
    __OBJID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OBJID'), 'OBJID', '__httpwww_loc_govMETS_metsType_OBJID', pyxb.binding.datatypes.string)

    OBJID = property(__OBJID.value, __OBJID.set, None, u'OBJID (string/O): Is the primary identifier assigned to the METS object as a whole. Although this attribute is not required, it is strongly recommended. This identifier is used to tag the entire METS object to external systems, in contrast with the ID identifier.\n\t\t\t\t')


    # Attribute PROFILE uses Python identifier PROFILE
    __PROFILE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'PROFILE'), 'PROFILE', '__httpwww_loc_govMETS_metsType_PROFILE', pyxb.binding.datatypes.string)

    PROFILE = property(__PROFILE.value, __PROFILE.set, None, u'PROFILE (string/O): Indicates to which of the registered profile(s) the METS document conforms. For additional information about PROFILES see Chapter 5 of the METS Primer.\n\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_metsType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__httpwww_loc_govMETS_metsType_LABEL', pyxb.binding.datatypes.string)

    LABEL = property(__LABEL.value, __LABEL.set, None, u'LABEL (string/O): Is a simple title string used to identify the object/entity being described in the METS document for the user.\n\t\t\t\t')


    _ElementMap = {
        __behaviorSec.name() : __behaviorSec,
        __structLink.name() : __structLink,
        __structMap.name() : __structMap,
        __dmdSec.name() : __dmdSec,
        __metsHdr.name() : __metsHdr,
        __amdSec.name() : __amdSec,
        __fileSec.name() : __fileSec
    }
    _AttributeMap = {
        __TYPE.name() : __TYPE,
        __OBJID.name() : __OBJID,
        __PROFILE.name() : __PROFILE,
        __ID.name() : __ID,
        __LABEL.name() : __LABEL
    }
Namespace.addCategoryObject('typeBinding', u'metsType', metsType)


# Complex type CTD_ANON_10 with content type ELEMENT_ONLY
class CTD_ANON_10 (metsType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is metsType

    # Element behaviorSec ({http://www.loc.gov/METS/}behaviorSec) inherited from {http://www.loc.gov/METS/}metsType

    # Element structLink ({http://www.loc.gov/METS/}structLink) inherited from {http://www.loc.gov/METS/}metsType

    # Element structMap ({http://www.loc.gov/METS/}structMap) inherited from {http://www.loc.gov/METS/}metsType

    # Element dmdSec ({http://www.loc.gov/METS/}dmdSec) inherited from {http://www.loc.gov/METS/}metsType

    # Element metsHdr ({http://www.loc.gov/METS/}metsHdr) inherited from {http://www.loc.gov/METS/}metsType

    # Element amdSec ({http://www.loc.gov/METS/}amdSec) inherited from {http://www.loc.gov/METS/}metsType

    # Element fileSec ({http://www.loc.gov/METS/}fileSec) inherited from {http://www.loc.gov/METS/}metsType

    # Attribute TYPE inherited from {http://www.loc.gov/METS/}metsType

    # Attribute ID inherited from {http://www.loc.gov/METS/}metsType

    # Attribute LABEL inherited from {http://www.loc.gov/METS/}metsType

    # Attribute PROFILE inherited from {http://www.loc.gov/METS/}metsType

    # Attribute OBJID inherited from {http://www.loc.gov/METS/}metsType

    _ElementMap = metsType._ElementMap.copy()
    _ElementMap.update({

    })
    _AttributeMap = metsType._AttributeMap.copy()
    _AttributeMap.update({

    })



# Complex type CTD_ANON_11 with content type ELEMENT_ONLY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True

    _ElementMap = {

    }
    _AttributeMap = {

    }



# Complex type structLinkType with content type ELEMENT_ONLY
class structLinkType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'structLinkType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}smLinkGrp uses Python identifier smLinkGrp
    __smLinkGrp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'smLinkGrp'), 'smLinkGrp', '__httpwww_loc_govMETS_structLinkType_httpwww_loc_govMETSsmLinkGrp', True)


    smLinkGrp = property(__smLinkGrp.value, __smLinkGrp.set, None, u'\n\t\t\t\t\t\tThe structMap link group element <smLinkGrp> provides an implementation of xlink:extendLink, and provides xlink compliant mechanisms for establishing xlink:arcLink type links between 2 or more <div> elements in <structMap> element(s) occurring within the same METS document or different METS documents.  The smLinkGrp could be used as an alternative to the <smLink> element to establish a one-to-one link between <div> elements in the same METS document in a fully xlink compliant manner.  However, it can also be used to establish one-to-many or many-to-many links between <div> elements. For example, if a METS document contains two <structMap> elements, one of which represents a purely logical structure and one of which represents a purely physical structure, the <smLinkGrp> element would provide a means of mapping a <div> representing a logical entity (for example, a newspaper article) with multiple <div> elements in the physical <structMap> representing the physical areas that  together comprise the logical entity (for example, the <div> elements representing the page areas that together comprise the newspaper article).\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}smLink uses Python identifier smLink
    __smLink = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'smLink'), 'smLink', '__httpwww_loc_govMETS_structLinkType_httpwww_loc_govMETSsmLink', True)


    smLink = property(__smLink.value, __smLink.set, None, u' \n\t\t\t\t\t\tThe Structural Map Link element <smLink> identifies a hyperlink between two nodes in the structural map. You would use <smLink>, for instance, to note the existence of hypertext links between web pages, if you wished to record those links within METS. NOTE: <smLink> is an empty element. The location of the <smLink> element to which the <smLink> element is pointing MUST be stored in the xlink:href attribute.\n\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_structLinkType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    _ElementMap = {
        __smLinkGrp.name() : __smLinkGrp,
        __smLink.name() : __smLink
    }
    _AttributeMap = {
        __ID.name() : __ID
    }
Namespace.addCategoryObject('typeBinding', u'structLinkType', structLinkType)


# Complex type CTD_ANON_12 with content type ELEMENT_ONLY
class CTD_ANON_12 (structLinkType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is structLinkType

    # Element smLinkGrp ({http://www.loc.gov/METS/}smLinkGrp) inherited from {http://www.loc.gov/METS/}structLinkType

    # Element smLink ({http://www.loc.gov/METS/}smLink) inherited from {http://www.loc.gov/METS/}structLinkType

    # Attribute ID inherited from {http://www.loc.gov/METS/}structLinkType

    _ElementMap = structLinkType._ElementMap.copy()
    _ElementMap.update({

    })
    _AttributeMap = structLinkType._AttributeMap.copy()
    _AttributeMap.update({

    })



# Complex type fileType with content type ELEMENT_ONLY
class fileType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'fileType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}transformFile uses Python identifier transformFile
    __transformFile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'transformFile'), 'transformFile', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETStransformFile', True)


    transformFile = property(__transformFile.value, __transformFile.set, None, u'\n\t\t\t\t\t\tThe transform file element <transformFile> provides a means to access any subsidiary files listed below a <file> element by indicating the steps required to "unpack" or transform the subsidiary files. This element is repeatable and might provide a link to a <behavior> in the <behaviorSec> that performs the transformation.')


    # Element {http://www.loc.gov/METS/}FContent uses Python identifier FContent
    __FContent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FContent'), 'FContent', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETSFContent', False)


    FContent = property(__FContent.value, __FContent.set, None, u'\n\t\t\t\t\t\tThe file content element <FContent> is used to identify a content file contained internally within a METS document. The content file must be either Base64 encoded and contained within the subsidiary <binData> wrapper element, or consist of XML information and be contained within the subsidiary <xmlData> wrapper element.\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}stream uses Python identifier stream
    __stream = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'stream'), 'stream', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETSstream', True)


    stream = property(__stream.value, __stream.set, None, u' \n\t\t\t\t\t\tA component byte stream element <stream> may be composed of one or more subsidiary streams. An MPEG4 file, for example, might contain separate audio and video streams, each of which is associated with technical metadata. The repeatable <stream> element provides a mechanism to record the existence of separate data streams within a particular file, and the opportunity to associate <dmdSec> and <amdSec> with those subsidiary data streams if desired. ')


    # Element {http://www.loc.gov/METS/}FLocat uses Python identifier FLocat
    __FLocat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FLocat'), 'FLocat', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETSFLocat', True)


    FLocat = property(__FLocat.value, __FLocat.set, None, u' \n\t\t\t\t\t\tThe file location element <FLocat> provides a pointer to the location of a content file. It uses the XLink reference syntax to provide linking information indicating the actual location of the content file, along with other attributes specifying additional linking information. NOTE: <FLocat> is an empty element. The location of the resource pointed to MUST be stored in the xlink:href attribute.\n\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}file uses Python identifier file
    __file = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'file'), 'file', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETSfile', True)


    file = property(__file.value, __file.set, None, None)


    # Attribute CHECKSUMTYPE uses Python identifier CHECKSUMTYPE
    __CHECKSUMTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CHECKSUMTYPE'), 'CHECKSUMTYPE', '__httpwww_loc_govMETS_fileType_CHECKSUMTYPE', STD_ANON_7)

    CHECKSUMTYPE = property(__CHECKSUMTYPE.value, __CHECKSUMTYPE.set, None, u'CHECKSUMTYPE (enumerated string/O): Specifies the checksum algorithm used to produce the value contained in the CHECKSUM attribute.  CHECKSUMTYPE must contain one of the following values:\n\t\t\t\t\tAdler-32\n\t\t\t\t\tCRC32\n\t\t\t\t\tHAVAL\n\t\t\t\t\tMD5\n\t\t\t\t\tMNP\n\t\t\t\t\tSHA-1\n\t\t\t\t\tSHA-256\n\t\t\t\t\tSHA-384\n\t\t\t\t\tSHA-512\n\t\t\t\t\tTIGER\n\t\t\t\t\tWHIRLPOOL\n\t\t\t\t')


    # Attribute BETYPE uses Python identifier BETYPE
    __BETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'BETYPE'), 'BETYPE', '__httpwww_loc_govMETS_fileType_BETYPE', STD_ANON_6)

    BETYPE = property(__BETYPE.value, __BETYPE.set, None, u'BETYPE: Begin/End Type.\n\t\t\t\t\tBETYPE (string/O): An attribute that specifies the kind of BEGIN and/or END values that are being used. Currently BYTE is the only valid value that can be used in conjunction with nested <file> or <stream> elements. \n\t\t\t\t')


    # Attribute CHECKSUM uses Python identifier CHECKSUM
    __CHECKSUM = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CHECKSUM'), 'CHECKSUM', '__httpwww_loc_govMETS_fileType_CHECKSUM', pyxb.binding.datatypes.string)

    CHECKSUM = property(__CHECKSUM.value, __CHECKSUM.set, None, u'CHECKSUM (string/O): Provides a checksum value for the associated file or wrapped content.\n\t\t\t\t')


    # Attribute OWNERID uses Python identifier OWNERID
    __OWNERID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OWNERID'), 'OWNERID', '__httpwww_loc_govMETS_fileType_OWNERID', pyxb.binding.datatypes.string)

    OWNERID = property(__OWNERID.value, __OWNERID.set, None, u'OWNERID (string/O): A unique identifier assigned to the file by its owner.  This may be a URI which differs from the URI used to retrieve the file.\n\t\t\t\t')


    # Attribute BEGIN uses Python identifier BEGIN
    __BEGIN = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'BEGIN'), 'BEGIN', '__httpwww_loc_govMETS_fileType_BEGIN', pyxb.binding.datatypes.string)

    BEGIN = property(__BEGIN.value, __BEGIN.set, None, u'BEGIN (string/O): An attribute that specifies the point in the parent <file> where the current <file> begins.  When used in conjunction with a <file> element, this attribute is only meaningful when this element is nested, and its parent <file> element represents a container file. It can be used in conjunction with the END attribute as a means of defining the location of the current file within its parent file. However, the BEGIN attribute can be used with or without a companion END attribute. When no END attribute is specified, the end of the parent file is assumed also to be the end point of the current file. The BEGIN and END attributes can only be interpreted meaningfully in conjunction with a BETYPE attribute, which specifies the kind of beginning/ending point values that are being used. \n\t\t\t\t')


    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ADMID'), 'ADMID', '__httpwww_loc_govMETS_fileType_ADMID', pyxb.binding.datatypes.IDREFS)

    ADMID = property(__ADMID.value, __ADMID.set, None, u'ADMID (IDREFS/O): Contains the ID attribute values of the <techMD>, <sourceMD>, <rightsMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain administrative metadata pertaining to the file. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CREATED'), 'CREATED', '__httpwww_loc_govMETS_fileType_CREATED', pyxb.binding.datatypes.dateTime)

    CREATED = property(__CREATED.value, __CREATED.set, None, u'CREATED (dateTime/O): Specifies the date and time of creation for the associated file or wrapped content.\n\t\t\t\t')


    # Attribute DMDID uses Python identifier DMDID
    __DMDID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'DMDID'), 'DMDID', '__httpwww_loc_govMETS_fileType_DMDID', pyxb.binding.datatypes.IDREFS)

    DMDID = property(__DMDID.value, __DMDID.set, None, u'DMDID (IDREFS/O): Contains the ID attribute values identifying the <dmdSec>, elements in the METS document that contain or link to descriptive metadata pertaining to the content file represented by the current <file> element.  For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute GROUPID uses Python identifier GROUPID
    __GROUPID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'GROUPID'), 'GROUPID', '__httpwww_loc_govMETS_fileType_GROUPID', pyxb.binding.datatypes.string)

    GROUPID = property(__GROUPID.value, __GROUPID.set, None, u'GROUPID (string/O): An identifier that establishes a correspondence between this file and files in other file groups. Typically, this will be used to associate a master file in one file group with the derivative files made from it in other file groups.\n\t\t\t\t')


    # Attribute MIMETYPE uses Python identifier MIMETYPE
    __MIMETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'MIMETYPE'), 'MIMETYPE', '__httpwww_loc_govMETS_fileType_MIMETYPE', pyxb.binding.datatypes.string)

    MIMETYPE = property(__MIMETYPE.value, __MIMETYPE.set, None, u'MIMETYPE (string/O): The IANA MIME media type for the associated file or wrapped content. Some values for this attribute can be found on the IANA website.\n\t\t\t\t')


    # Attribute USE uses Python identifier USE
    __USE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'USE'), 'USE', '__httpwww_loc_govMETS_fileType_USE', pyxb.binding.datatypes.string)

    USE = property(__USE.value, __USE.set, None, u'USE (string/O): A tagging attribute to indicate the intended use of all copies of the file aggregated by the <file> element (e.g., master, reference, thumbnails for image files). A USE attribute can be expressed at the<fileGrp> level, the <file> level, the <FLocat> level and/or the <FContent> level.  A USE attribute value at the <fileGrp> level should pertain to all of the files in the <fileGrp>.  A USE attribute at the <file> level should pertain to all copies of the file as represented by subsidiary <FLocat> and/or <FContent> elements.  A USE attribute at the <FLocat> or <FContent> level pertains to the particular copy of the file that is either referenced (<FLocat>) or wrapped (<FContent>).\n\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_fileType_ID', pyxb.binding.datatypes.ID, required=True)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/R): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. Typically, the ID attribute value on a <file> element would be referenced from one or more FILEID attributes (which are of type IDREF) on <fptr>and/or <area> elements within the <structMap>.  Such references establish links between  structural divisions (<div> elements) and the specific content files or parts of content files that manifest them. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute SIZE uses Python identifier SIZE
    __SIZE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SIZE'), 'SIZE', '__httpwww_loc_govMETS_fileType_SIZE', pyxb.binding.datatypes.long)

    SIZE = property(__SIZE.value, __SIZE.set, None, u'SIZE (long/O): Specifies the size in bytes of the associated file or wrapped content.\n\t\t\t\t')


    # Attribute END uses Python identifier END
    __END = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'END'), 'END', '__httpwww_loc_govMETS_fileType_END', pyxb.binding.datatypes.string)

    END = property(__END.value, __END.set, None, u'END (string/O): An attribute that specifies the point in the parent <file> where the current, nested <file> ends. It can only be interpreted meaningfully in conjunction with the BETYPE, which specifies the kind of ending point values being used. Typically the END attribute would only appear in conjunction with a BEGIN attribute.\n\t\t\t\t')


    # Attribute SEQ uses Python identifier SEQ
    __SEQ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SEQ'), 'SEQ', '__httpwww_loc_govMETS_fileType_SEQ', pyxb.binding.datatypes.int)

    SEQ = property(__SEQ.value, __SEQ.set, None, u'SEQ (integer/O): Indicates the sequence of this <file> relative to the others in its <fileGrp>.\n\t\t\t\t')


    _ElementMap = {
        __transformFile.name() : __transformFile,
        __FContent.name() : __FContent,
        __stream.name() : __stream,
        __FLocat.name() : __FLocat,
        __file.name() : __file
    }
    _AttributeMap = {
        __CHECKSUMTYPE.name() : __CHECKSUMTYPE,
        __BETYPE.name() : __BETYPE,
        __CHECKSUM.name() : __CHECKSUM,
        __OWNERID.name() : __OWNERID,
        __BEGIN.name() : __BEGIN,
        __ADMID.name() : __ADMID,
        __CREATED.name() : __CREATED,
        __DMDID.name() : __DMDID,
        __GROUPID.name() : __GROUPID,
        __MIMETYPE.name() : __MIMETYPE,
        __USE.name() : __USE,
        __ID.name() : __ID,
        __SIZE.name() : __SIZE,
        __END.name() : __END,
        __SEQ.name() : __SEQ
    }
Namespace.addCategoryObject('typeBinding', u'fileType', fileType)


# Complex type behaviorType with content type ELEMENT_ONLY
class behaviorType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'behaviorType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}interfaceDef uses Python identifier interfaceDef
    __interfaceDef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'interfaceDef'), 'interfaceDef', '__httpwww_loc_govMETS_behaviorType_httpwww_loc_govMETSinterfaceDef', False)


    interfaceDef = property(__interfaceDef.value, __interfaceDef.set, None, u'\n\t\t\t\t\t\tThe interface definition <interfaceDef> element contains a pointer to an abstract definition of a single behavior or a set of related behaviors that are associated with the content of a METS object. The interface definition object to which the <interfaceDef> element points using xlink:href could be another digital object, or some other entity, such as a text file which describes the interface or a Web Services Description Language (WSDL) file. Ideally, an interface definition object contains metadata that describes a set of behaviors or methods. It may also contain files that describe the intended usage of the behaviors, and possibly files that represent different expressions of the interface definition.\t\t\n\t\t\t')


    # Element {http://www.loc.gov/METS/}mechanism uses Python identifier mechanism
    __mechanism = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'mechanism'), 'mechanism', '__httpwww_loc_govMETS_behaviorType_httpwww_loc_govMETSmechanism', False)


    mechanism = property(__mechanism.value, __mechanism.set, None, u' \n\t\t\t\t\tA mechanism element <mechanism> contains a pointer to an executable code module that implements a set of behaviors defined by an interface definition. The <mechanism> element will be a pointer to another object (a mechanism object). A mechanism object could be another METS object, or some other entity (e.g., a WSDL file). A mechanism object should contain executable code, pointers to executable code, or specifications for binding to network services (e.g., web services).\n\t\t\t\t\t')


    # Attribute GROUPID uses Python identifier GROUPID
    __GROUPID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'GROUPID'), 'GROUPID', '__httpwww_loc_govMETS_behaviorType_GROUPID', pyxb.binding.datatypes.string)

    GROUPID = property(__GROUPID.value, __GROUPID.set, None, u'GROUPID (string/O): An identifier that establishes a correspondence between the given behavior and other behaviors, typically used to facilitate versions of behaviors.\n\t\t\t\t')


    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ADMID'), 'ADMID', '__httpwww_loc_govMETS_behaviorType_ADMID', pyxb.binding.datatypes.IDREFS)

    ADMID = property(__ADMID.value, __ADMID.set, None, u'ADMID (IDREFS/O): An optional attribute listing the XML ID values of administrative metadata sections within the METS document pertaining to this behavior.\n\t\t\t\t')


    # Attribute BTYPE uses Python identifier BTYPE
    __BTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'BTYPE'), 'BTYPE', '__httpwww_loc_govMETS_behaviorType_BTYPE', pyxb.binding.datatypes.string)

    BTYPE = property(__BTYPE.value, __BTYPE.set, None, u'BTYPE (string/O): The behavior type provides a means of categorizing the related behavior.')


    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CREATED'), 'CREATED', '__httpwww_loc_govMETS_behaviorType_CREATED', pyxb.binding.datatypes.dateTime)

    CREATED = property(__CREATED.value, __CREATED.set, None, u'CREATED (dateTime/O): The dateTime of creation for the behavior. \n\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_behaviorType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. In the case of a <behavior> element that applies to a <transformFile> element, the ID value must be present and would be referenced from the transformFile/@TRANSFORMBEHAVIOR attribute. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute STRUCTID uses Python identifier STRUCTID
    __STRUCTID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'STRUCTID'), 'STRUCTID', '__httpwww_loc_govMETS_behaviorType_STRUCTID', pyxb.binding.datatypes.IDREFS)

    STRUCTID = property(__STRUCTID.value, __STRUCTID.set, None, u'STRUCTID (IDREFS/O): An XML IDREFS attribute used to link a <behavior>  to one or more <div> elements within a <structMap> in the METS document. The content to which the STRUCTID points is considered input to the executable behavior mechanism defined for the behavior.  If the <behavior> applies to one or more <div> elements, then the STRUCTID attribute must be present.\n\t\t\t\t')


    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__httpwww_loc_govMETS_behaviorType_LABEL', pyxb.binding.datatypes.string)

    LABEL = property(__LABEL.value, __LABEL.set, None, u'LABEL (string/O): A text description of the behavior.  \n\t\t\t\t')


    _ElementMap = {
        __interfaceDef.name() : __interfaceDef,
        __mechanism.name() : __mechanism
    }
    _AttributeMap = {
        __GROUPID.name() : __GROUPID,
        __ADMID.name() : __ADMID,
        __BTYPE.name() : __BTYPE,
        __CREATED.name() : __CREATED,
        __ID.name() : __ID,
        __STRUCTID.name() : __STRUCTID,
        __LABEL.name() : __LABEL
    }
Namespace.addCategoryObject('typeBinding', u'behaviorType', behaviorType)


# Complex type CTD_ANON_13 with content type EMPTY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute BETYPE uses Python identifier BETYPE
    __BETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'BETYPE'), 'BETYPE', '__httpwww_loc_govMETS_CTD_ANON_13_BETYPE', STD_ANON_8)

    BETYPE = property(__BETYPE.value, __BETYPE.set, None, u'BETYPE: Begin/End Type.\n\t\t\t\t\t\t\t\t\t\tBETYPE (string/O): An attribute that specifies the kind of BEGIN and/or END values that are being used. Currently BYTE is the only valid value that can be used in conjunction with nested <file> or <stream> elements. \n\t\t\t\t\t\t\t\t\t')


    # Attribute DMDID uses Python identifier DMDID
    __DMDID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'DMDID'), 'DMDID', '__httpwww_loc_govMETS_CTD_ANON_13_DMDID', pyxb.binding.datatypes.IDREFS)

    DMDID = property(__DMDID.value, __DMDID.set, None, u'DMDID (IDREFS/O): Contains the ID attribute values identifying the <dmdSec>, elements in the METS document that contain or link to descriptive metadata pertaining to the content file stream represented by the current <stream> element.  For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_13_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t')


    # Attribute streamType uses Python identifier streamType
    __streamType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'streamType'), 'streamType', '__httpwww_loc_govMETS_CTD_ANON_13_streamType', pyxb.binding.datatypes.string)

    streamType = property(__streamType.value, __streamType.set, None, u'streamType (string/O): The IANA MIME media type for the bytestream.')


    # Attribute END uses Python identifier END
    __END = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'END'), 'END', '__httpwww_loc_govMETS_CTD_ANON_13_END', pyxb.binding.datatypes.string)

    END = property(__END.value, __END.set, None, u'END (string/O): An attribute that specifies the point in the parent <file> where the <stream> ends. It can only be interpreted meaningfully in conjunction with the BETYPE, which specifies the kind of ending point values being used. Typically the END attribute would only appear in conjunction with a BEGIN attribute.\n\t\t\t\t\t\t\t\t\t')


    # Attribute OWNERID uses Python identifier OWNERID
    __OWNERID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OWNERID'), 'OWNERID', '__httpwww_loc_govMETS_CTD_ANON_13_OWNERID', pyxb.binding.datatypes.string)

    OWNERID = property(__OWNERID.value, __OWNERID.set, None, u'OWNERID (string/O): Used to provide a unique identifier (which could include a URI) assigned to the file. This identifier may differ from the URI used to retrieve the file.\n\t\t\t\t\t\t\t\t\t')


    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ADMID'), 'ADMID', '__httpwww_loc_govMETS_CTD_ANON_13_ADMID', pyxb.binding.datatypes.IDREFS)

    ADMID = property(__ADMID.value, __ADMID.set, None, u'ADMID (IDREFS/O): Contains the ID attribute values of the <techMD>, <sourceMD>, <rightsMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain administrative metadata pertaining to the bytestream. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t')


    # Attribute BEGIN uses Python identifier BEGIN
    __BEGIN = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'BEGIN'), 'BEGIN', '__httpwww_loc_govMETS_CTD_ANON_13_BEGIN', pyxb.binding.datatypes.string)

    BEGIN = property(__BEGIN.value, __BEGIN.set, None, u'BEGIN (string/O): An attribute that specifies the point in the parent <file> where the current <stream> begins. It can be used in conjunction with the END attribute as a means of defining the location of the stream within its parent file. However, the BEGIN attribute can be used with or without a companion END attribute. When no END attribute is specified, the end of the parent file is assumed also to be the end point of the stream. The BEGIN and END attributes can only be interpreted meaningfully in conjunction with a BETYPE attribute, which specifies the kind of beginning/ending point values that are being used. \n\t\t\t\t\t\t\t\t\t')


    _ElementMap = {

    }
    _AttributeMap = {
        __BETYPE.name() : __BETYPE,
        __DMDID.name() : __DMDID,
        __ID.name() : __ID,
        __streamType.name() : __streamType,
        __END.name() : __END,
        __OWNERID.name() : __OWNERID,
        __ADMID.name() : __ADMID,
        __BEGIN.name() : __BEGIN
    }



# Complex type CTD_ANON_14 with content type ELEMENT_ONLY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}xmlData uses Python identifier xmlData
    __xmlData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'xmlData'), 'xmlData', '__httpwww_loc_govMETS_CTD_ANON_14_httpwww_loc_govMETSxmlData', False)


    xmlData = property(__xmlData.value, __xmlData.set, None, u'\n\t\t\t\t\t\t\t\t\tAn xml data wrapper element <xmlData> is used to contain  an XML encoded file. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> element is set to \u201clax\u201d. Therefore, if the source schema and its location are identified by means of an xsi:schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element.\n\t\t\t\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}binData uses Python identifier binData
    __binData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'binData'), 'binData', '__httpwww_loc_govMETS_CTD_ANON_14_httpwww_loc_govMETSbinData', False)


    binData = property(__binData.value, __binData.set, None, u'\n\t\t\t\t\t\t\t\t\tA binary data wrapper element <binData> is used to contain a Base64 encoded file.\n\t\t\t\t\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_14_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    # Attribute USE uses Python identifier USE
    __USE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'USE'), 'USE', '__httpwww_loc_govMETS_CTD_ANON_14_USE', pyxb.binding.datatypes.string)

    USE = property(__USE.value, __USE.set, None, u'USE (string/O): A tagging attribute to indicate the intended use of the specific copy of the file represented by the <FContent> element (e.g., service master, archive master). A USE attribute can be expressed at the<fileGrp> level, the <file> level, the <FLocat> level and/or the <FContent> level.  A USE attribute value at the <fileGrp> level should pertain to all of the files in the <fileGrp>.  A USE attribute at the <file> level should pertain to all copies of the file as represented by subsidiary <FLocat> and/or <FContent> elements.  A USE attribute at the <FLocat> or <FContent> level pertains to the particular copy of the file that is either referenced (<FLocat>) or wrapped (<FContent>).\n\t\t\t\t\t\t\t')


    _ElementMap = {
        __xmlData.name() : __xmlData,
        __binData.name() : __binData
    }
    _AttributeMap = {
        __ID.name() : __ID,
        __USE.name() : __USE
    }



# Complex type CTD_ANON_15 with content type EMPTY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_w3_org1999xlinkshow', _xlink.STD_ANON_1)

    show = property(__show.value, __show.set, None, None)


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_15_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_w3_org1999xlinkactuate', _xlink.STD_ANON_2)

    actuate = property(__actuate.value, __actuate.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}from uses Python identifier from_
    __from = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'from'), 'from_', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_w3_org1999xlinkfrom', pyxb.binding.datatypes.string, required=True)

    from_ = property(__from.value, __from.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)

    title = property(__title.value, __title.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}to uses Python identifier to
    __to = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'to'), 'to', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_w3_org1999xlinkto', pyxb.binding.datatypes.string, required=True)

    to = property(__to.value, __to.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)

    arcrole = property(__arcrole.value, __arcrole.set, None, None)


    _ElementMap = {

    }
    _AttributeMap = {
        __show.name() : __show,
        __ID.name() : __ID,
        __actuate.name() : __actuate,
        __from.name() : __from,
        __title.name() : __title,
        __to.name() : __to,
        __arcrole.name() : __arcrole
    }



# Complex type CTD_ANON_16 with content type ELEMENT_ONLY
class CTD_ANON_16 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}metsDocumentID uses Python identifier metsDocumentID
    __metsDocumentID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'metsDocumentID'), 'metsDocumentID', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_loc_govMETSmetsDocumentID', False)


    metsDocumentID = property(__metsDocumentID.value, __metsDocumentID.set, None, u'    \n\t\t\t\t\t\t\t\t\tThe metsDocument identifier element <metsDocumentID> allows a unique identifier to be assigned to the METS document itself.  This may be different from the OBJID attribute value in the root <mets> element, which uniquely identifies the entire digital object represented by the METS document.\n\t\t\t\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}agent uses Python identifier agent
    __agent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'agent'), 'agent', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_loc_govMETSagent', True)


    agent = property(__agent.value, __agent.set, None, u'agent: \n\t\t\t\t\t\t\t\tThe agent element <agent> provides for various parties and their roles with respect to the METS record to be documented.  \n\t\t\t\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}altRecordID uses Python identifier altRecordID
    __altRecordID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'altRecordID'), 'altRecordID', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_loc_govMETSaltRecordID', True)


    altRecordID = property(__altRecordID.value, __altRecordID.set, None, u'    \n\t\t\t\t\t\t\t\t\tThe alternative record identifier element <altRecordID> allows one to use alternative record identifier values for the digital object represented by the METS document; the primary record identifier is stored in the OBJID attribute in the root <mets> element.\n\t\t\t\t\t\t\t\t')


    # Attribute RECORDSTATUS uses Python identifier RECORDSTATUS
    __RECORDSTATUS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'RECORDSTATUS'), 'RECORDSTATUS', '__httpwww_loc_govMETS_CTD_ANON_16_RECORDSTATUS', pyxb.binding.datatypes.string)

    RECORDSTATUS = property(__RECORDSTATUS.value, __RECORDSTATUS.set, None, u'RECORDSTATUS (string/O): Specifies the status of the METS document. It is used for internal processing purposes.\n\t\t\t\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_16_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ADMID'), 'ADMID', '__httpwww_loc_govMETS_CTD_ANON_16_ADMID', pyxb.binding.datatypes.IDREFS)

    ADMID = property(__ADMID.value, __ADMID.set, None, u'ADMID (IDREFS/O): Contains the ID attribute values of the <techMD>, <sourceMD>, <rightsMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain administrative metadata pertaining to the METS document itself.  For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    # Attribute CREATEDATE uses Python identifier CREATEDATE
    __CREATEDATE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CREATEDATE'), 'CREATEDATE', '__httpwww_loc_govMETS_CTD_ANON_16_CREATEDATE', pyxb.binding.datatypes.dateTime)

    CREATEDATE = property(__CREATEDATE.value, __CREATEDATE.set, None, u'CREATEDATE (dateTime/O): Records the date/time the METS document was created.\n\t\t\t\t\t\t\t')


    # Attribute LASTMODDATE uses Python identifier LASTMODDATE
    __LASTMODDATE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LASTMODDATE'), 'LASTMODDATE', '__httpwww_loc_govMETS_CTD_ANON_16_LASTMODDATE', pyxb.binding.datatypes.dateTime)

    LASTMODDATE = property(__LASTMODDATE.value, __LASTMODDATE.set, None, u'LASTMODDATE (dateTime/O): Is used to indicate the date/time the METS document was last modified.\n\t\t\t\t\t\t\t')


    _ElementMap = {
        __metsDocumentID.name() : __metsDocumentID,
        __agent.name() : __agent,
        __altRecordID.name() : __altRecordID
    }
    _AttributeMap = {
        __RECORDSTATUS.name() : __RECORDSTATUS,
        __ID.name() : __ID,
        __ADMID.name() : __ADMID,
        __CREATEDATE.name() : __CREATEDATE,
        __LASTMODDATE.name() : __LASTMODDATE
    }



# Complex type seqType with content type ELEMENT_ONLY
class seqType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'seqType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}par uses Python identifier par
    __par = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'par'), 'par', '__httpwww_loc_govMETS_seqType_httpwww_loc_govMETSpar', True)


    par = property(__par.value, __par.set, None, None)


    # Element {http://www.loc.gov/METS/}area uses Python identifier area
    __area = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'area'), 'area', '__httpwww_loc_govMETS_seqType_httpwww_loc_govMETSarea', True)


    area = property(__area.value, __area.set, None, None)


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_seqType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    _ElementMap = {
        __par.name() : __par,
        __area.name() : __area
    }
    _AttributeMap = {
        __ID.name() : __ID
    }
Namespace.addCategoryObject('typeBinding', u'seqType', seqType)


# Complex type CTD_ANON_17 with content type EMPTY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_17_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.')


    # Attribute ARCTYPE uses Python identifier ARCTYPE
    __ARCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ARCTYPE'), 'ARCTYPE', '__httpwww_loc_govMETS_CTD_ANON_17_ARCTYPE', pyxb.binding.datatypes.string)

    ARCTYPE = property(__ARCTYPE.value, __ARCTYPE.set, None, u'ARCTYPE (string/O):The ARCTYPE attribute provides a means of specifying the relationship between the <div> elements participating in the arc link, and hence the purpose or role of the link.  While it can be considered analogous to the xlink:arcrole attribute, its type is a simple string, rather than anyURI.  ARCTYPE has no xlink specified meaning, and the xlink:arcrole attribute should be used instead of or in addition to the ARCTYPE attribute when full xlink compliance is desired with respect to specifying the role or purpose of the arc link. \n\t\t\t\t\t\t\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkshow', _xlink.STD_ANON_1)

    show = property(__show.value, __show.set, None, None)


    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ADMID'), 'ADMID', '__httpwww_loc_govMETS_CTD_ANON_17_ADMID', pyxb.binding.datatypes.IDREFS)

    ADMID = property(__ADMID.value, __ADMID.set, None, u'ADMID (IDREFS/O): Contains the ID attribute values identifying the <sourceMD>, <techMD>, <digiprovMD> and/or <rightsMD> elements within the <amdSec> of the METS document that contain or link to administrative metadata pertaining to <smArcLink>. Typically the <smArcLink> ADMID attribute would be used to identify one or more <sourceMD> and/or <techMD> elements that refine or clarify the relationship between the xlink:from and xlink:to sides of the arc. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkactuate', _xlink.STD_ANON_2)

    actuate = property(__actuate.value, __actuate.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}from uses Python identifier from_
    __from = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'from'), 'from_', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkfrom', pyxb.binding.datatypes.string)

    from_ = property(__from.value, __from.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}to uses Python identifier to
    __to = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'to'), 'to', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkto', pyxb.binding.datatypes.string)

    to = property(__to.value, __to.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)

    title = property(__title.value, __title.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'arc')

    type = property(__type.value, __type.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)

    arcrole = property(__arcrole.value, __arcrole.set, None, None)


    _ElementMap = {

    }
    _AttributeMap = {
        __ID.name() : __ID,
        __ARCTYPE.name() : __ARCTYPE,
        __show.name() : __show,
        __ADMID.name() : __ADMID,
        __actuate.name() : __actuate,
        __from.name() : __from,
        __to.name() : __to,
        __title.name() : __title,
        __type.name() : __type,
        __arcrole.name() : __arcrole
    }



# Complex type CTD_ANON_18 with content type EMPTY
class CTD_ANON_18 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute OTHERMDTYPE uses Python identifier OTHERMDTYPE
    __OTHERMDTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OTHERMDTYPE'), 'OTHERMDTYPE', '__httpwww_loc_govMETS_CTD_ANON_18_OTHERMDTYPE', pyxb.binding.datatypes.string)

    OTHERMDTYPE = property(__OTHERMDTYPE.value, __OTHERMDTYPE.set, None, u'OTHERMDTYPE (string/O): Specifies the form of metadata in use when the value OTHER is indicated in the MDTYPE attribute.\n\t\t\t\t')


    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CREATED'), 'CREATED', '__httpwww_loc_govMETS_CTD_ANON_18_CREATED', pyxb.binding.datatypes.dateTime)

    CREATED = property(__CREATED.value, __CREATED.set, None, u'CREATED (dateTime/O): Specifies the date and time of creation for the associated file or wrapped content.\n\t\t\t\t')


    # Attribute MDTYPEVERSION uses Python identifier MDTYPEVERSION
    __MDTYPEVERSION = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'MDTYPEVERSION'), 'MDTYPEVERSION', '__httpwww_loc_govMETS_CTD_ANON_18_MDTYPEVERSION', pyxb.binding.datatypes.string)

    MDTYPEVERSION = property(__MDTYPEVERSION.value, __MDTYPEVERSION.set, None, u'MDTYPEVERSION(string/O): Provides a means for recording the version of the type of metadata (as recorded in the MDTYPE or OTHERMDTYPE attribute) that is being used.  This may represent the version of the underlying data dictionary or metadata model rather than a schema version. ')


    # Attribute CHECKSUM uses Python identifier CHECKSUM
    __CHECKSUM = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CHECKSUM'), 'CHECKSUM', '__httpwww_loc_govMETS_CTD_ANON_18_CHECKSUM', pyxb.binding.datatypes.string)

    CHECKSUM = property(__CHECKSUM.value, __CHECKSUM.set, None, u'CHECKSUM (string/O): Provides a checksum value for the associated file or wrapped content.\n\t\t\t\t')


    # Attribute XPTR uses Python identifier XPTR
    __XPTR = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'XPTR'), 'XPTR', '__httpwww_loc_govMETS_CTD_ANON_18_XPTR', pyxb.binding.datatypes.string)

    XPTR = property(__XPTR.value, __XPTR.set, None, u'XPTR (string/O): Locates the point within a file to which the <mdRef> element refers, if applicable.\n\t\t\t\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_loc_govMETS_CTD_ANON_18_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)

    href = property(__href.value, __href.set, None, None)


    # Attribute CHECKSUMTYPE uses Python identifier CHECKSUMTYPE
    __CHECKSUMTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CHECKSUMTYPE'), 'CHECKSUMTYPE', '__httpwww_loc_govMETS_CTD_ANON_18_CHECKSUMTYPE', STD_ANON_7)

    CHECKSUMTYPE = property(__CHECKSUMTYPE.value, __CHECKSUMTYPE.set, None, u'CHECKSUMTYPE (enumerated string/O): Specifies the checksum algorithm used to produce the value contained in the CHECKSUM attribute.  CHECKSUMTYPE must contain one of the following values:\n\t\t\t\t\tAdler-32\n\t\t\t\t\tCRC32\n\t\t\t\t\tHAVAL\n\t\t\t\t\tMD5\n\t\t\t\t\tMNP\n\t\t\t\t\tSHA-1\n\t\t\t\t\tSHA-256\n\t\t\t\t\tSHA-384\n\t\t\t\t\tSHA-512\n\t\t\t\t\tTIGER\n\t\t\t\t\tWHIRLPOOL\n\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_18_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)

    role = property(__role.value, __role.set, None, None)


    # Attribute LOCTYPE uses Python identifier LOCTYPE
    __LOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LOCTYPE'), 'LOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_18_LOCTYPE', STD_ANON_5, required=True)

    LOCTYPE = property(__LOCTYPE.value, __LOCTYPE.set, None, u'LOCTYPE (string/R): Specifies the locator type used in the xlink:href attribute. Valid values for LOCTYPE are: \n\t\t\t\t\tARK\n\t\t\t\t\tURN\n\t\t\t\t\tURL\n\t\t\t\t\tPURL\n\t\t\t\t\tHANDLE\n\t\t\t\t\tDOI\n\t\t\t\t\tOTHER\n\t\t\t\t')


    # Attribute OTHERLOCTYPE uses Python identifier OTHERLOCTYPE
    __OTHERLOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OTHERLOCTYPE'), 'OTHERLOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_18_OTHERLOCTYPE', pyxb.binding.datatypes.string)

    OTHERLOCTYPE = property(__OTHERLOCTYPE.value, __OTHERLOCTYPE.set, None, u'OTHERLOCTYPE (string/O): Specifies the locator type when the value OTHER is used in the LOCTYPE attribute. Although optional, it is strongly recommended when OTHER is used.\n\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_18_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')

    type = property(__type.value, __type.set, None, None)


    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_18_httpwww_w3_org1999xlinkshow', _xlink.STD_ANON_1)

    show = property(__show.value, __show.set, None, None)


    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__httpwww_loc_govMETS_CTD_ANON_18_LABEL', pyxb.binding.datatypes.string)

    LABEL = property(__LABEL.value, __LABEL.set, None, u'LABEL (string/O): Provides a label to display to the viewer of the METS document that identifies the associated metadata.\n\t\t\t\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_18_httpwww_w3_org1999xlinkactuate', _xlink.STD_ANON_2)

    actuate = property(__actuate.value, __actuate.set, None, None)


    # Attribute MIMETYPE uses Python identifier MIMETYPE
    __MIMETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'MIMETYPE'), 'MIMETYPE', '__httpwww_loc_govMETS_CTD_ANON_18_MIMETYPE', pyxb.binding.datatypes.string)

    MIMETYPE = property(__MIMETYPE.value, __MIMETYPE.set, None, u'MIMETYPE (string/O): The IANA MIME media type for the associated file or wrapped content. Some values for this attribute can be found on the IANA website.\n\t\t\t\t')


    # Attribute MDTYPE uses Python identifier MDTYPE
    __MDTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'MDTYPE'), 'MDTYPE', '__httpwww_loc_govMETS_CTD_ANON_18_MDTYPE', STD_ANON_9, required=True)

    MDTYPE = property(__MDTYPE.value, __MDTYPE.set, None, u'MDTYPE (string/R): Is used to indicate the type of the associated metadata. It must have one of the following values:\nMARC: any form of MARC record\nMODS: metadata in the Library of Congress MODS format\nEAD: Encoded Archival Description finding aid\nDC: Dublin Core\nNISOIMG: NISO Technical Metadata for Digital Still Images\nLC-AV: technical metadata specified in the Library of Congress A/V prototyping project\nVRA: Visual Resources Association Core\nTEIHDR: Text Encoding Initiative Header\nDDI: Data Documentation Initiative\nFGDC: Federal Geographic Data Committee metadata\nLOM: Learning Object Model\nPREMIS:  PREservation Metadata: Implementation Strategies\nPREMIS:OBJECT: PREMIS Object entiry\nPREMIS:AGENT: PREMIS Agent entity\nPREMIS:RIGHTS: PREMIS Rights entity\nPREMIS:EVENT: PREMIS Event entity\nTEXTMD: textMD Technical metadata for text\nMETSRIGHTS: Rights Declaration Schema\nISO 19115:2003 NAP: North American Profile of ISO 19115:2003 descriptive metadata\nOTHER: metadata in a format not specified above\n\t\t\t\t')


    # Attribute SIZE uses Python identifier SIZE
    __SIZE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SIZE'), 'SIZE', '__httpwww_loc_govMETS_CTD_ANON_18_SIZE', pyxb.binding.datatypes.long)

    SIZE = property(__SIZE.value, __SIZE.set, None, u'SIZE (long/O): Specifies the size in bytes of the associated file or wrapped content.\n\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_18_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)

    title = property(__title.value, __title.set, None, None)


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_18_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_18_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)

    arcrole = property(__arcrole.value, __arcrole.set, None, None)


    _ElementMap = {

    }
    _AttributeMap = {
        __OTHERMDTYPE.name() : __OTHERMDTYPE,
        __CREATED.name() : __CREATED,
        __MDTYPEVERSION.name() : __MDTYPEVERSION,
        __CHECKSUM.name() : __CHECKSUM,
        __XPTR.name() : __XPTR,
        __href.name() : __href,
        __CHECKSUMTYPE.name() : __CHECKSUMTYPE,
        __role.name() : __role,
        __LOCTYPE.name() : __LOCTYPE,
        __OTHERLOCTYPE.name() : __OTHERLOCTYPE,
        __type.name() : __type,
        __show.name() : __show,
        __LABEL.name() : __LABEL,
        __actuate.name() : __actuate,
        __MIMETYPE.name() : __MIMETYPE,
        __MDTYPE.name() : __MDTYPE,
        __SIZE.name() : __SIZE,
        __title.name() : __title,
        __ID.name() : __ID,
        __arcrole.name() : __arcrole
    }



# Complex type parType with content type ELEMENT_ONLY
class parType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'parType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}seq uses Python identifier seq
    __seq = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'seq'), 'seq', '__httpwww_loc_govMETS_parType_httpwww_loc_govMETSseq', True)


    seq = property(__seq.value, __seq.set, None, None)


    # Element {http://www.loc.gov/METS/}area uses Python identifier area
    __area = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'area'), 'area', '__httpwww_loc_govMETS_parType_httpwww_loc_govMETSarea', True)


    area = property(__area.value, __area.set, None, None)


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_parType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    _ElementMap = {
        __seq.name() : __seq,
        __area.name() : __area
    }
    _AttributeMap = {
        __ID.name() : __ID
    }
Namespace.addCategoryObject('typeBinding', u'parType', parType)


# Complex type CTD_ANON_19 with content type EMPTY
class CTD_ANON_19 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute TRANSFORMBEHAVIOR uses Python identifier TRANSFORMBEHAVIOR
    __TRANSFORMBEHAVIOR = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TRANSFORMBEHAVIOR'), 'TRANSFORMBEHAVIOR', '__httpwww_loc_govMETS_CTD_ANON_19_TRANSFORMBEHAVIOR', pyxb.binding.datatypes.IDREF)

    TRANSFORMBEHAVIOR = property(__TRANSFORMBEHAVIOR.value, __TRANSFORMBEHAVIOR.set, None, u'TRANSFORMBEHAVIOR (string/O): An IDREF to a behavior element for this transformation.')


    # Attribute TRANSFORMKEY uses Python identifier TRANSFORMKEY
    __TRANSFORMKEY = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TRANSFORMKEY'), 'TRANSFORMKEY', '__httpwww_loc_govMETS_CTD_ANON_19_TRANSFORMKEY', pyxb.binding.datatypes.string)

    TRANSFORMKEY = property(__TRANSFORMKEY.value, __TRANSFORMKEY.set, None, u'TRANSFORMKEY (string/O): A key to be used with the transform algorithm for accessing the file\u2019s contents.')


    # Attribute TRANSFORMORDER uses Python identifier TRANSFORMORDER
    __TRANSFORMORDER = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TRANSFORMORDER'), 'TRANSFORMORDER', '__httpwww_loc_govMETS_CTD_ANON_19_TRANSFORMORDER', pyxb.binding.datatypes.positiveInteger, required=True)

    TRANSFORMORDER = property(__TRANSFORMORDER.value, __TRANSFORMORDER.set, None, u'TRANSFORMORDER (postive-integer/R): The order in which the instructions must be followed in order to unpack or transform the container file.')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_19_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t')


    # Attribute TRANSFORMTYPE uses Python identifier TRANSFORMTYPE
    __TRANSFORMTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TRANSFORMTYPE'), 'TRANSFORMTYPE', '__httpwww_loc_govMETS_CTD_ANON_19_TRANSFORMTYPE', STD_ANON_10, required=True)

    TRANSFORMTYPE = property(__TRANSFORMTYPE.value, __TRANSFORMTYPE.set, None, u'TRANSFORMTYPE (string/R): Is used to indicate the type of transformation needed to render content of a file accessible. This may include unpacking a file into subsidiary files/streams. The controlled value constraints for this XML string include \u201cdecompression\u201d and \u201cdecryption\u201d. Decompression is defined as the action of reversing data compression, i.e., the process of encoding information using fewer bits than an unencoded representation would use by means of specific encoding schemas. Decryption is defined as the process of restoring data that has been obscured to make it unreadable without special knowledge (encrypted data) to its original form. ')


    # Attribute TRANSFORMALGORITHM uses Python identifier TRANSFORMALGORITHM
    __TRANSFORMALGORITHM = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TRANSFORMALGORITHM'), 'TRANSFORMALGORITHM', '__httpwww_loc_govMETS_CTD_ANON_19_TRANSFORMALGORITHM', pyxb.binding.datatypes.string, required=True)

    TRANSFORMALGORITHM = property(__TRANSFORMALGORITHM.value, __TRANSFORMALGORITHM.set, None, u'TRANSFORM-ALGORITHM (string/R): Specifies the decompression or decryption routine used to access the contents of the file. Algorithms for compression can be either loss-less or lossy.')


    _ElementMap = {

    }
    _AttributeMap = {
        __TRANSFORMBEHAVIOR.name() : __TRANSFORMBEHAVIOR,
        __TRANSFORMKEY.name() : __TRANSFORMKEY,
        __TRANSFORMORDER.name() : __TRANSFORMORDER,
        __ID.name() : __ID,
        __TRANSFORMTYPE.name() : __TRANSFORMTYPE,
        __TRANSFORMALGORITHM.name() : __TRANSFORMALGORITHM
    }



# Complex type CTD_ANON_20 with content type ELEMENT_ONLY
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_loc_govMETS_CTD_ANON_20_httpwww_loc_govMETSname', False)


    name = property(__name.value, __name.set, None, u' \n\t\t\t\t\t\t\t\t\t\t\tThe element <name> can be used to record the full name of the document agent.\n\t\t\t\t\t\t\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}note uses Python identifier note
    __note = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'note'), 'note', '__httpwww_loc_govMETS_CTD_ANON_20_httpwww_loc_govMETSnote', True)


    note = property(__note.value, __note.set, None, u" \n\t\t\t\t\t\t\t\t\t\t\tThe <note> element can be used to record any additional information regarding the agent's activities with respect to the METS document.\n\t\t\t\t\t\t\t\t\t\t\t")


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_20_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t\t')


    # Attribute OTHERROLE uses Python identifier OTHERROLE
    __OTHERROLE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OTHERROLE'), 'OTHERROLE', '__httpwww_loc_govMETS_CTD_ANON_20_OTHERROLE', pyxb.binding.datatypes.string)

    OTHERROLE = property(__OTHERROLE.value, __OTHERROLE.set, None, u'OTHERROLE (string/O): Denotes a role not contained in the allowed values set if OTHER is indicated in the ROLE attribute.\n\t\t\t\t\t\t\t\t\t\t')


    # Attribute ROLE uses Python identifier ROLE
    __ROLE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ROLE'), 'ROLE', '__httpwww_loc_govMETS_CTD_ANON_20_ROLE', STD_ANON_12, required=True)

    ROLE = property(__ROLE.value, __ROLE.set, None, u'ROLE (string/R): Specifies the function of the agent with respect to the METS record. The allowed values are:\nCREATOR: The person(s) or institution(s) responsible for the METS document.\nEDITOR: The person(s) or institution(s) that prepares the metadata for encoding.\nARCHIVIST: The person(s) or institution(s) responsible for the document/collection.\nPRESERVATION: The person(s) or institution(s) responsible for preservation functions.\nDISSEMINATOR: The person(s) or institution(s) responsible for dissemination functions.\nCUSTODIAN: The person(s) or institution(s) charged with the oversight of a document/collection.\nIPOWNER: Intellectual Property Owner: The person(s) or institution holding copyright, trade or service marks or other intellectual property rights for the object.\nOTHER: Use OTHER if none of the preceding values pertains and clarify the type and location specifier being used in the OTHERROLE attribute (see below).\n\t\t\t\t\t\t\t\t\t\t')


    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TYPE'), 'TYPE', '__httpwww_loc_govMETS_CTD_ANON_20_TYPE', STD_ANON_11)

    TYPE = property(__TYPE.value, __TYPE.set, None, u'TYPE (string/O): is used to specify the type of AGENT. It must be one of the following values:\nINDIVIDUAL: Use if an individual has served as the agent.\nORGANIZATION: Use if an institution, corporate body, association, non-profit enterprise, government, religious body, etc. has served as the agent.\nOTHER: Use OTHER if none of the preceding values pertain and clarify the type of agent specifier being used in the OTHERTYPE attribute\n\t\t\t\t\t\t\t\t\t\t')


    # Attribute OTHERTYPE uses Python identifier OTHERTYPE
    __OTHERTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OTHERTYPE'), 'OTHERTYPE', '__httpwww_loc_govMETS_CTD_ANON_20_OTHERTYPE', pyxb.binding.datatypes.string)

    OTHERTYPE = property(__OTHERTYPE.value, __OTHERTYPE.set, None, u'OTHERTYPE (string/O): Specifies the type of agent when the value OTHER is indicated in the TYPE attribute.\n\t\t\t\t\t\t\t\t\t\t')


    _ElementMap = {
        __name.name() : __name,
        __note.name() : __note
    }
    _AttributeMap = {
        __ID.name() : __ID,
        __OTHERROLE.name() : __OTHERROLE,
        __ROLE.name() : __ROLE,
        __TYPE.name() : __TYPE,
        __OTHERTYPE.name() : __OTHERTYPE
    }



# Complex type structMapType with content type ELEMENT_ONLY
class structMapType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'structMapType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}div uses Python identifier div
    __div = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'div'), 'div', '__httpwww_loc_govMETS_structMapType_httpwww_loc_govMETSdiv', False)


    div = property(__div.value, __div.set, None, u" \n\t\t\t\t\t\tThe structural divisions of the hierarchical organization provided by a <structMap> are represented by division <div> elements, which can be nested to any depth. Each <div> element can represent either an intellectual (logical) division or a physical division. Every <div> node in the structural map hierarchy may be connected (via subsidiary <mptr> or <fptr> elements) to content files which represent that div's portion of the whole document. \n\t\t\t\t\t")


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_structMapType_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')


    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'TYPE'), 'TYPE', '__httpwww_loc_govMETS_structMapType_TYPE', pyxb.binding.datatypes.string)

    TYPE = property(__TYPE.value, __TYPE.set, None, u'TYPE (string/O): Identifies the type of structure represented by the <structMap>. For example, a <structMap> that represented a purely logical or intellectual structure could be assigned a TYPE value of \u201clogical\u201d whereas a <structMap> that represented a purely physical structure could be assigned a TYPE value of \u201cphysical\u201d. However, the METS schema neither defines nor requires a common vocabulary for this attribute. A METS profile, however, may well constrain the values for the <structMap> TYPE.\n\t\t\t\t')


    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__httpwww_loc_govMETS_structMapType_LABEL', pyxb.binding.datatypes.string)

    LABEL = property(__LABEL.value, __LABEL.set, None, u'LABEL (string/O): Describes the <structMap> to viewers of the METS document. This would be useful primarily where more than one <structMap> is provided for a single object. A descriptive LABEL value, in that case, could clarify to users the purpose of each of the available structMaps.\n\t\t\t\t')


    _ElementMap = {
        __div.name() : __div
    }
    _AttributeMap = {
        __ID.name() : __ID,
        __TYPE.name() : __TYPE,
        __LABEL.name() : __LABEL
    }
Namespace.addCategoryObject('typeBinding', u'structMapType', structMapType)


# Complex type CTD_ANON_21 with content type ELEMENT_ONLY
class CTD_ANON_21 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}xmlData uses Python identifier xmlData
    __xmlData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'xmlData'), 'xmlData', '__httpwww_loc_govMETS_CTD_ANON_21_httpwww_loc_govMETSxmlData', False)


    xmlData = property(__xmlData.value, __xmlData.set, None, u'\n\t\t\t\t\t\t\t\t\tThe xml data wrapper element <xmlData> is used to contain XML encoded metadata. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> is set to \u201clax\u201d. Therefore, if the source schema and its location are identified by means of an XML schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element. \t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}binData uses Python identifier binData
    __binData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'binData'), 'binData', '__httpwww_loc_govMETS_CTD_ANON_21_httpwww_loc_govMETSbinData', False)


    binData = property(__binData.value, __binData.set, None, u' \n\t\t\t\t\t\t\t\t\tThe binary data wrapper element <binData> is used to contain Base64 encoded metadata.\t\t\t\t\t\t\t\t\t\t\t\t')


    # Attribute MIMETYPE uses Python identifier MIMETYPE
    __MIMETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'MIMETYPE'), 'MIMETYPE', '__httpwww_loc_govMETS_CTD_ANON_21_MIMETYPE', pyxb.binding.datatypes.string)

    MIMETYPE = property(__MIMETYPE.value, __MIMETYPE.set, None, u'MIMETYPE (string/O): The IANA MIME media type for the associated file or wrapped content. Some values for this attribute can be found on the IANA website.\n\t\t\t\t')


    # Attribute OTHERMDTYPE uses Python identifier OTHERMDTYPE
    __OTHERMDTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'OTHERMDTYPE'), 'OTHERMDTYPE', '__httpwww_loc_govMETS_CTD_ANON_21_OTHERMDTYPE', pyxb.binding.datatypes.string)

    OTHERMDTYPE = property(__OTHERMDTYPE.value, __OTHERMDTYPE.set, None, u'OTHERMDTYPE (string/O): Specifies the form of metadata in use when the value OTHER is indicated in the MDTYPE attribute.\n\t\t\t\t')


    # Attribute CHECKSUMTYPE uses Python identifier CHECKSUMTYPE
    __CHECKSUMTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CHECKSUMTYPE'), 'CHECKSUMTYPE', '__httpwww_loc_govMETS_CTD_ANON_21_CHECKSUMTYPE', STD_ANON_7)

    CHECKSUMTYPE = property(__CHECKSUMTYPE.value, __CHECKSUMTYPE.set, None, u'CHECKSUMTYPE (enumerated string/O): Specifies the checksum algorithm used to produce the value contained in the CHECKSUM attribute.  CHECKSUMTYPE must contain one of the following values:\n\t\t\t\t\tAdler-32\n\t\t\t\t\tCRC32\n\t\t\t\t\tHAVAL\n\t\t\t\t\tMD5\n\t\t\t\t\tMNP\n\t\t\t\t\tSHA-1\n\t\t\t\t\tSHA-256\n\t\t\t\t\tSHA-384\n\t\t\t\t\tSHA-512\n\t\t\t\t\tTIGER\n\t\t\t\t\tWHIRLPOOL\n\t\t\t\t')


    # Attribute SIZE uses Python identifier SIZE
    __SIZE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SIZE'), 'SIZE', '__httpwww_loc_govMETS_CTD_ANON_21_SIZE', pyxb.binding.datatypes.long)

    SIZE = property(__SIZE.value, __SIZE.set, None, u'SIZE (long/O): Specifies the size in bytes of the associated file or wrapped content.\n\t\t\t\t')


    # Attribute MDTYPE uses Python identifier MDTYPE
    __MDTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'MDTYPE'), 'MDTYPE', '__httpwww_loc_govMETS_CTD_ANON_21_MDTYPE', STD_ANON_9, required=True)

    MDTYPE = property(__MDTYPE.value, __MDTYPE.set, None, u'MDTYPE (string/R): Is used to indicate the type of the associated metadata. It must have one of the following values:\nMARC: any form of MARC record\nMODS: metadata in the Library of Congress MODS format\nEAD: Encoded Archival Description finding aid\nDC: Dublin Core\nNISOIMG: NISO Technical Metadata for Digital Still Images\nLC-AV: technical metadata specified in the Library of Congress A/V prototyping project\nVRA: Visual Resources Association Core\nTEIHDR: Text Encoding Initiative Header\nDDI: Data Documentation Initiative\nFGDC: Federal Geographic Data Committee metadata\nLOM: Learning Object Model\nPREMIS:  PREservation Metadata: Implementation Strategies\nPREMIS:OBJECT: PREMIS Object entiry\nPREMIS:AGENT: PREMIS Agent entity\nPREMIS:RIGHTS: PREMIS Rights entity\nPREMIS:EVENT: PREMIS Event entity\nTEXTMD: textMD Technical metadata for text\nMETSRIGHTS: Rights Declaration Schema\nISO 19115:2003 NAP: North American Profile of ISO 19115:2003 descriptive metadata\nOTHER: metadata in a format not specified above\n\t\t\t\t')


    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CREATED'), 'CREATED', '__httpwww_loc_govMETS_CTD_ANON_21_CREATED', pyxb.binding.datatypes.dateTime)

    CREATED = property(__CREATED.value, __CREATED.set, None, u'CREATED (dateTime/O): Specifies the date and time of creation for the associated file or wrapped content.\n\t\t\t\t')


    # Attribute CHECKSUM uses Python identifier CHECKSUM
    __CHECKSUM = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CHECKSUM'), 'CHECKSUM', '__httpwww_loc_govMETS_CTD_ANON_21_CHECKSUM', pyxb.binding.datatypes.string)

    CHECKSUM = property(__CHECKSUM.value, __CHECKSUM.set, None, u'CHECKSUM (string/O): Provides a checksum value for the associated file or wrapped content.\n\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_21_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    # Attribute MDTYPEVERSION uses Python identifier MDTYPEVERSION
    __MDTYPEVERSION = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'MDTYPEVERSION'), 'MDTYPEVERSION', '__httpwww_loc_govMETS_CTD_ANON_21_MDTYPEVERSION', pyxb.binding.datatypes.string)

    MDTYPEVERSION = property(__MDTYPEVERSION.value, __MDTYPEVERSION.set, None, u'MDTYPEVERSION(string/O): Provides a means for recording the version of the type of metadata (as recorded in the MDTYPE or OTHERMDTYPE attribute) that is being used.  This may represent the version of the underlying data dictionary or metadata model rather than a schema version. ')


    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__httpwww_loc_govMETS_CTD_ANON_21_LABEL', pyxb.binding.datatypes.string)

    LABEL = property(__LABEL.value, __LABEL.set, None, u'LABEL: an optional string attribute providing a label to display to the viewer of the METS document identifying the metadata.\n\t\t\t\t\t\t\t')


    _ElementMap = {
        __xmlData.name() : __xmlData,
        __binData.name() : __binData
    }
    _AttributeMap = {
        __MIMETYPE.name() : __MIMETYPE,
        __OTHERMDTYPE.name() : __OTHERMDTYPE,
        __CHECKSUMTYPE.name() : __CHECKSUMTYPE,
        __SIZE.name() : __SIZE,
        __MDTYPE.name() : __MDTYPE,
        __CREATED.name() : __CREATED,
        __CHECKSUM.name() : __CHECKSUM,
        __ID.name() : __ID,
        __MDTYPEVERSION.name() : __MDTYPEVERSION,
        __LABEL.name() : __LABEL
    }



# Complex type CTD_ANON_22 with content type ELEMENT_ONLY
class CTD_ANON_22 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://www.loc.gov/METS/}seq uses Python identifier seq
    __seq = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'seq'), 'seq', '__httpwww_loc_govMETS_CTD_ANON_22_httpwww_loc_govMETSseq', False)


    seq = property(__seq.value, __seq.set, None, u'  \n\t\t\t\t\t\t\t\t\tThe sequence of files element <seq> aggregates pointers to files,  parts of files and/or parallel sets of files or parts of files  that must be played or displayed sequentially to manifest a block of digital content. This might be the case, for example, if the parent <div> element represented a logical division, such as a diary entry, that spanned multiple pages of a diary and, hence, multiple page image files. In this case, a <seq> element would aggregate multiple, sequentially arranged <area> elements, each of which pointed to one of the image files that must be presented sequentially to manifest the entire diary entry. If the diary entry started in the middle of a page, then the first <area> element (representing the page on which the diary entry starts) might be further qualified, via its SHAPE and COORDS attributes, to specify the specific, pertinent area of the associated image file.\n\t\t\t\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}area uses Python identifier area
    __area = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'area'), 'area', '__httpwww_loc_govMETS_CTD_ANON_22_httpwww_loc_govMETSarea', False)


    area = property(__area.value, __area.set, None, u' \n\t\t\t\t\t\t\t\t\tThe area element <area> typically points to content consisting of just a portion or area of a file represented by a <file> element in the <fileSec>. In some contexts, however, the <area> element can also point to content represented by an integral file. A single <area> element would appear as the direct child of a <fptr> element when only a portion of a <file>, rather than an integral <file>, manifested the digital content represented by the <fptr>. Multiple <area> elements would appear as the direct children of a <par> element or a <seq> element when multiple files or parts of files manifested the digital content represented by an <fptr> element. When used in the context of a <par> or <seq> element an <area> element can point either to an integral file or to a segment of a file as necessary.\n\t\t\t\t\t\t\t\t')


    # Element {http://www.loc.gov/METS/}par uses Python identifier par
    __par = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'par'), 'par', '__httpwww_loc_govMETS_CTD_ANON_22_httpwww_loc_govMETSpar', False)


    par = property(__par.value, __par.set, None, u' \n\t\t\t\t\t\t\t\t\tThe <par> or parallel files element aggregates pointers to files, parts of files, and/or sequences of files or parts of files that must be played or displayed simultaneously to manifest a block of digital content represented by an <fptr> element. This might be the case, for example, with multi-media content, where a still image might have an accompanying audio track that comments on the still image. In this case, a <par> element would aggregate two <area> elements, one of which pointed to the image file and one of which pointed to the audio file that must be played in conjunction with the image. The <area> element associated with the image could be further qualified with SHAPE and COORDS attributes if only a portion of the image file was pertinent and the <area> element associated with the audio file could be further qualified with BETYPE, BEGIN, EXTTYPE, and EXTENT attributes if only a portion of the associated audio file should be played in conjunction with the image.\n\t\t\t\t\t\t\t\t')


    # Attribute FILEID uses Python identifier FILEID
    __FILEID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'FILEID'), 'FILEID', '__httpwww_loc_govMETS_CTD_ANON_22_FILEID', pyxb.binding.datatypes.IDREF)

    FILEID = property(__FILEID.value, __FILEID.set, None, u'FILEID (IDREF/O): An optional attribute that provides the XML ID identifying the <file> element that links to and/or contains the digital content represented by the <fptr>. A <fptr> element should only have a FILEID attribute value if it does not have a child <area>, <par> or <seq> element. If it has a child element, then the responsibility for pointing to the relevant content falls to this child element or its descendants.\n\t\t\t\t\t\t\t')


    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_22_ID', pyxb.binding.datatypes.ID)

    ID = property(__ID.value, __ID.set, None, u'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')


    # Attribute CONTENTIDS uses Python identifier CONTENTIDS
    __CONTENTIDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'CONTENTIDS'), 'CONTENTIDS', '__httpwww_loc_govMETS_CTD_ANON_22_CONTENTIDS', URIs)

    CONTENTIDS = property(__CONTENTIDS.value, __CONTENTIDS.set, None, u'CONTENTIDS (URI/O): Content IDs for the content represented by the <fptr> (equivalent to DIDL DII or Digital Item Identifier, a unique external ID).\n\t\t\t\t            ')


    _ElementMap = {
        __seq.name() : __seq,
        __area.name() : __area,
        __par.name() : __par
    }
    _AttributeMap = {
        __FILEID.name() : __FILEID,
        __ID.name() : __ID,
        __CONTENTIDS.name() : __CONTENTIDS
    }



mets = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'mets'), CTD_ANON_10, documentation=u'METS: Metadata Encoding and Transmission Standard.\n\t\t\t\tMETS is intended to provide a standardized XML format for transmission of complex digital library objects between systems.  As such, it can be seen as filling a role similar to that defined for the Submission Information Package (SIP), Archival Information Package (AIP) and Dissemination Information Package (DIP) in the Reference Model for an Open Archival Information System. The root element <mets> establishes the container for the information being stored and/or transmitted by the standard.\n\t\t\t')
Namespace.addCategoryObject('elementBinding', mets.name().localName(), mets)



behaviorSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'behaviorSec'), behaviorSecType, scope=behaviorSecType))

behaviorSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'behavior'), behaviorType, scope=behaviorSecType, documentation=u'\n\t\t\t\t\t\tA behavior element <behavior> can be used to associate executable behaviors with content in the METS document. This element has an interface definition <interfaceDef> element that represents an abstract definition of a set of behaviors represented by a particular behavior. A <behavior> element also has a behavior mechanism <mechanism> element, a module of executable code that implements and runs the behavior defined abstractly by the interface definition.\n\t\t\t\t\t'))
behaviorSecType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=behaviorSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'behaviorSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=behaviorSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'behavior'))),
    ])
})



divType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'div'), divType, scope=divType))

divType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'mptr'), CTD_ANON_4, scope=divType, documentation=u' \n\t\t\t\t\t\tLike the <fptr> element, the METS pointer element <mptr> represents digital content that manifests its parent <div> element. Unlike the <fptr>, which either directly or indirectly points to content represented in the <fileSec> of the parent METS document, the <mptr> element points to content represented by an external METS document. Thus, this element allows multiple discrete and separate METS documents to be organized at a higher level by a separate METS document. For example, METS documents representing the individual issues in the series of a journal could be grouped together and organized by a higher level METS document that represents the entire journal series. Each of the <div> elements in the <structMap> of the METS document representing the journal series would point to a METS document representing an issue.  It would do so via a child <mptr> element. Thus the <mptr> element gives METS users considerable flexibility in managing the depth of the <structMap> hierarchy of individual METS documents. The <mptr> element points to an external METS document by means of an xlink:href attribute and associated XLink attributes. \t\t\t\t\t\t\t\t\n\t\t\t\t\t'))

divType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'fptr'), CTD_ANON_22, scope=divType, documentation=u'\n\t\t\t\t\t\tThe <fptr> or file pointer element represents digital content that manifests its parent <div> element. The content represented by an <fptr> element must consist of integral files or parts of files that are represented by <file> elements in the <fileSec>. Via its FILEID attribute,  an <fptr> may point directly to a single integral <file> element that manifests a structural division. However, an <fptr> element may also govern an <area> element,  a <par>, or  a <seq>  which in turn would point to the relevant file or files. A child <area> element can point to part of a <file> that manifests a division, while the <par> and <seq> elements can point to multiple files or parts of files that together manifest a division. More than one <fptr> element can be associated with a <div> element. Typically sibling <fptr> elements represent alternative versions, or manifestations, of the same content\n\t\t\t\t\t'))
divType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=divType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mptr'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=divType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'div'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=divType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fptr'))),
    ])
})



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'smLocatorLink'), CTD_ANON_7, scope=CTD_ANON_3, documentation=u'\n\t\t\t\t\t\t\t\t\tThe structMap locator link element <smLocatorLink> is of xlink:type "locator".  It provides a means of identifying a <div> element that will participate in one or more of the links specified by means of <smArcLink> elements within the same <smLinkGrp>. The participating <div> element that is represented by the <smLocatorLink> is identified by means of a URI in the associate xlink:href attribute.  The lowest level of this xlink:href URI value should be a fragment identifier that references the ID value that identifies the relevant <div> element.  For example, "xlink:href=\'#div20\'" where "div20" is the ID value that identifies the pertinent <div> in the current METS document. Although not required by the xlink specification, an <smLocatorLink> element will typically include an xlink:label attribute in this context, as the <smArcLink> elements will reference these labels to establish the from and to sides of each arc link.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'smArcLink'), CTD_ANON_17, scope=CTD_ANON_3))
CTD_ANON_3._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLocatorLink'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLocatorLink'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smArcLink'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLocatorLink'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smArcLink'))),
    ])
})


CTD_ANON_6._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)),
    ])
})



mdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'mdRef'), CTD_ANON_18, scope=mdSecType, documentation=u'\n\t\t\t\t\t\tThe metadata reference element <mdRef> element is a generic element used throughout the METS schema to provide a pointer to metadata which resides outside the METS document.  NB: <mdRef> is an empty element.  The location of the metadata must be recorded in the xlink:href attribute, supplemented by the XPTR attribute as needed.\n\t\t\t\t\t'))

mdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'mdWrap'), CTD_ANON_21, scope=mdSecType, documentation=u' \n\t\t\t\t\t\tA metadata wrapper element <mdWrap> provides a wrapper around metadata embedded within a METS document. The element is repeatable. Such metadata can be in one of two forms: 1) XML-encoded metadata, with the XML-encoding identifying itself as belonging to a namespace other than the METS document namespace. 2) Any arbitrary binary or textual form, PROVIDED that the metadata is Base64 encoded and wrapped in a <binData> element within the internal descriptive metadata element.\n\t\t\t\t\t'))
mdSecType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=mdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mdRef'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
mdSecType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=mdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mdWrap'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(mdSecType._ContentModel_1, False),
    pyxb.binding.content.ModelGroupAllAlternative(mdSecType._ContentModel_2, False),
])
mdSecType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



amdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'techMD'), mdSecType, scope=amdSecType, documentation=u' \n\t\t\t\t\t\tA technical metadata element <techMD> records technical metadata about a component of the METS object, such as a digital content file. The <techMD> element conforms to same generic datatype as the <dmdSec>, <rightsMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes.  A technical metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <techMD> elements; and technical metadata can be associated with any METS element that supports an ADMID attribute. Technical metadata can be expressed according to many current technical description standards (such as MIX and textMD) or a locally produced XML schema.\n\t\t\t\t\t'))

amdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'digiprovMD'), mdSecType, scope=amdSecType, documentation=u'\n\t\t\t\t\t\tA digital provenance metadata element <digiprovMD> can be used to record any preservation-related actions taken on the various files which comprise a digital object (e.g., those subsequent to the initial digitization of the files such as transformation or migrations) or, in the case of born digital materials, the files\u2019 creation. In short, digital provenance should be used to record information that allows both archival/library staff and scholars to understand what modifications have been made to a digital object and/or its constituent parts during its life cycle. This information can then be used to judge how those processes might have altered or corrupted the object\u2019s ability to accurately represent the original item. One might, for example, record master derivative relationships and the process by which those derivations have been created. Or the <digiprovMD> element could contain information regarding the migration/transformation of a file from its original digitization (e.g., OCR, TEI, etc.,)to its current incarnation as a digital object (e.g., JPEG2000). The <digiprovMD> element conforms to same generic datatype as the <dmdSec>,  <techMD>, <rightsMD>, and <sourceMD> elements, and supports the same sub-elements and attributes. A digital provenance metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <digiprovMD> elements; and digital provenance metadata can be associated with any METS element that supports an ADMID attribute. Digital provenance metadata can be expressed according to current digital provenance description standards (such as PREMIS) or a locally produced XML schema.\n\t\t\t\t\t'))

amdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'rightsMD'), mdSecType, scope=amdSecType, documentation=u'\n\t\t\t\t\t\tAn intellectual property rights metadata element <rightsMD> records information about copyright and licensing pertaining to a component of the METS object. The <rightsMD> element conforms to same generic datatype as the <dmdSec>, <techMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes. A rights metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <rightsMD> elements; and rights metadata can be associated with any METS element that supports an ADMID attribute. Rights metadata can be expressed according current rights description standards (such as CopyrightMD and rightsDeclarationMD) or a locally produced XML schema.\n\t\t\t\t\t'))

amdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'sourceMD'), mdSecType, scope=amdSecType, documentation=u'\n\t\t\t\t\t\tA source metadata element <sourceMD> records descriptive and administrative metadata about the source format or media of a component of the METS object such as a digital content file. It is often used for discovery, data administration or preservation of the digital object. The <sourceMD> element conforms to same generic datatype as the <dmdSec>, <techMD>, <rightsMD>,  and <digiprovMD> elements, and supports the same sub-elements and attributes.  A source metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <sourceMD> elements; and source metadata can be associated with any METS element that supports an ADMID attribute. Source metadata can be expressed according to current source description standards (such as PREMIS) or a locally produced XML schema.\n\t\t\t\t\t'))
amdSecType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=amdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'techMD'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=amdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'rightsMD'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=amdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'digiprovMD'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=amdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'sourceMD'))),
    ])
})



CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'), CTD_ANON_9, scope=CTD_ANON_8, documentation=u' \n\t\t\t\t\t\t\t\t\tA sequence of file group elements <fileGrp> can be used group the digital files comprising the content of a METS object either into a flat arrangement or, because each file group element can itself contain one or more  file group elements,  into a nested (hierarchical) arrangement. In the case where the content files are images of different formats and resolutions, for example, one could group the image content files by format and create a separate <fileGrp> for each image format/resolution such as:\n-- one <fileGrp> for the thumbnails of the images\n-- one <fileGrp> for the higher resolution JPEGs of the image \n-- one <fileGrp> for the master archival TIFFs of the images \nFor a text resource with a variety of content file types one might group the content files at the highest level by type,  and then use the <fileGrp> element\u2019s nesting capabilities to subdivide a <fileGrp> by format within the type, such as:\n-- one <fileGrp> for all of the page images with nested <fileGrp> elements for each image format/resolution (tiff, jpeg, gif)\n-- one <fileGrp> for a PDF version of all the pages of the document \n-- one <fileGrp> for  a TEI encoded XML version of the entire document or each of its pages.\nA <fileGrp> may contain zero or more <fileGrp> elements and or <file> elements.\t\t\t\t\t\n\t\t\t\t\t\t\t\t'))
CTD_ANON_8._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'))),
    ])
})



fileGrpType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'file'), fileType, scope=fileGrpType, documentation=u'\n\t\t\t\t\t\tThe file element <file> provides access to the content files for the digital object being described by the METS document. A <file> element may contain one or more <FLocat> elements which provide pointers to a content file and/or a <FContent> element which wraps an encoded version of the file. Embedding files using <FContent> can be a valuable feature for exchanging digital objects between repositories or for archiving versions of digital objects for off-site storage. All <FLocat> and <FContent> elements should identify and/or contain identical copies of a single file. The <file> element is recursive, thus allowing sub-files or component files of a larger file to be listed in the inventory. Alternatively, by using the <stream> element, a smaller component of a file or of a related file can be placed within a <file> element. Finally, by using the <transformFile> element, it is possible to include within a <file> element a different version of a file that has undergone a transformation for some reason, such as format migration.\n\t\t\t\t\t'))

fileGrpType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'), fileGrpType, scope=fileGrpType))
fileGrpType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=fileGrpType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=fileGrpType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'file'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=fileGrpType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=fileGrpType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'file'))),
    ])
})


CTD_ANON_9._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'file'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileGrp'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'file'))),
    ])
})



metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'behaviorSec'), behaviorSecType, scope=metsType, documentation=u'\n\t\t\t\t\t\tA behavior section element <behaviorSec> associates executable behaviors with content in the METS document by means of a repeatable behavior <behavior> element. This element has an interface definition <interfaceDef> element that represents an abstract definition of the set of behaviors represented by a particular behavior section. A <behavior> element also has a <mechanism> element which is used to point to a module of executable code that implements and runs the behavior defined by the interface definition. The <behaviorSec> element, which is repeatable as well as nestable, can be used to group individual behaviors within the structure of the METS document. Such grouping can be useful for organizing families of behaviors together or to indicate other relationships between particular behaviors.'))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'structLink'), CTD_ANON_12, scope=metsType, documentation=u' \n\t\t\t\t\t\tThe structural link section element <structLink> allows for the specification of hyperlinks between the different components of a METS structure that are delineated in a structural map. This element is a container for a single, repeatable element, <smLink> which indicates a hyperlink between two nodes in the structural map. The <structLink> section in the METS document is identified using its XML ID attributes.\n\t\t\t\t\t'))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'structMap'), structMapType, scope=metsType, documentation=u' \n\t\t\t\t\t\tThe structural map section <structMap> is the heart of a METS document. It provides a means for organizing the digital content represented by the <file> elements in the <fileSec> of the METS document into a coherent hierarchical structure. Such a hierarchical structure can be presented to users to facilitate their comprehension and navigation of the digital content. It can further be applied to any purpose requiring an understanding of the structural relationship of the content files or parts of the content files. The organization may be specified to any level of granularity (intellectual and or physical) that is desired. Since the <structMap> element is repeatable, more than one organization can be applied to the digital content represented by the METS document.  The hierarchical structure specified by a <structMap> is encoded as a tree of nested <div> elements. A <div> element may directly point to content via child file pointer <fptr> elements (if the content is represented in the <fileSec<) or child METS pointer <mptr> elements (if the content is represented by an external METS document). The <fptr> element may point to a single whole <file> element that manifests its parent <div<, or to part of a <file> that manifests its <div<. It can also point to multiple files or parts of files that must be played/displayed either in sequence or in parallel to reveal its structural division. In addition to providing a means for organizing content, the <structMap> provides a mechanism for linking content at any hierarchical level with relevant descriptive and administrative metadata.\n\t\t\t\t\t'))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dmdSec'), mdSecType, scope=metsType, documentation=u'\n\t\t\t\t\t\tA descriptive metadata section <dmdSec> records descriptive metadata pertaining to the METS object as a whole or one of its components. The <dmdSec> element conforms to same generic datatype as the <techMD>, <rightsMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes. A descriptive metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <dmdSec> elements; and descriptive metadata can be associated with any METS element that supports a DMDID attribute.  Descriptive metadata can be expressed according to many current description standards (i.e., MARC, MODS, Dublin Core, TEI Header, EAD, VRA, FGDC, DDI) or a locally produced XML schema. \n\t\t\t\t\t'))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'metsHdr'), CTD_ANON_16, scope=metsType, documentation=u' \n\t\t\t\t\tThe mets header element <metsHdr> captures metadata about the METS document itself, not the digital object the METS document encodes. Although it records a more limited set of metadata, it is very similar in function and purpose to the headers employed in other schema such as the Text Encoding Initiative (TEI) or in the Encoded Archival Description (EAD).\n\t\t\t'))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'amdSec'), amdSecType, scope=metsType, documentation=u' \n\t\t\t\t\t\tThe administrative metadata section <amdSec> contains the administrative metadata pertaining to the digital object, its components and any original source material from which the digital object is derived. The <amdSec> is separated into four sub-sections that accommodate technical metadata (techMD), intellectual property rights (rightsMD), analog/digital source metadata (sourceMD), and digital provenance metadata (digiprovMD). Each of these subsections can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both. Multiple instances of the <amdSec> element can occur within a METS document and multiple instances of its subsections can occur in one <amdSec> element. This allows considerable flexibility in the structuring of the administrative metadata. METS does not define a vocabulary or syntax for encoding administrative metadata. Administrative metadata can be expressed within the amdSec sub-elements according to many current community defined standards, or locally produced XML schemas. '))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'fileSec'), CTD_ANON_8, scope=metsType, documentation=u' \n\t\t\t\t\t\tThe overall purpose of the content file section element <fileSec> is to provide an inventory of and the location for the content files that comprise the digital object being described in the METS document.\n\t\t\t\t\t'))
metsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'amdSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'metsHdr'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dmdSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structMap'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileSec'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'behaviorSec'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'behaviorSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structLink'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structMap'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structMap'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'amdSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dmdSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structMap'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileSec'))),
    ])
})


CTD_ANON_10._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'amdSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'metsHdr'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dmdSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structMap'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileSec'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'behaviorSec'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'behaviorSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structLink'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structMap'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structMap'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'amdSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dmdSec'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'structMap'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fileSec'))),
    ])
})


CTD_ANON_11._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)),
    ])
})



structLinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'smLinkGrp'), CTD_ANON_3, scope=structLinkType, documentation=u'\n\t\t\t\t\t\tThe structMap link group element <smLinkGrp> provides an implementation of xlink:extendLink, and provides xlink compliant mechanisms for establishing xlink:arcLink type links between 2 or more <div> elements in <structMap> element(s) occurring within the same METS document or different METS documents.  The smLinkGrp could be used as an alternative to the <smLink> element to establish a one-to-one link between <div> elements in the same METS document in a fully xlink compliant manner.  However, it can also be used to establish one-to-many or many-to-many links between <div> elements. For example, if a METS document contains two <structMap> elements, one of which represents a purely logical structure and one of which represents a purely physical structure, the <smLinkGrp> element would provide a means of mapping a <div> representing a logical entity (for example, a newspaper article) with multiple <div> elements in the physical <structMap> representing the physical areas that  together comprise the logical entity (for example, the <div> elements representing the page areas that together comprise the newspaper article).\n\t\t\t\t\t'))

structLinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'smLink'), CTD_ANON_15, scope=structLinkType, documentation=u' \n\t\t\t\t\t\tThe Structural Map Link element <smLink> identifies a hyperlink between two nodes in the structural map. You would use <smLink>, for instance, to note the existence of hypertext links between web pages, if you wished to record those links within METS. NOTE: <smLink> is an empty element. The location of the <smLink> element to which the <smLink> element is pointing MUST be stored in the xlink:href attribute.\n\t\t\t\t'))
structLinkType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=structLinkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLinkGrp'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=structLinkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLink'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=structLinkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLinkGrp'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=structLinkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLink'))),
    ])
})


CTD_ANON_12._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLinkGrp'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLink'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLinkGrp'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'smLink'))),
    ])
})



fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'transformFile'), CTD_ANON_19, scope=fileType, documentation=u'\n\t\t\t\t\t\tThe transform file element <transformFile> provides a means to access any subsidiary files listed below a <file> element by indicating the steps required to "unpack" or transform the subsidiary files. This element is repeatable and might provide a link to a <behavior> in the <behaviorSec> that performs the transformation.'))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FContent'), CTD_ANON_14, scope=fileType, documentation=u'\n\t\t\t\t\t\tThe file content element <FContent> is used to identify a content file contained internally within a METS document. The content file must be either Base64 encoded and contained within the subsidiary <binData> wrapper element, or consist of XML information and be contained within the subsidiary <xmlData> wrapper element.\n\t\t\t\t\t'))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'stream'), CTD_ANON_13, scope=fileType, documentation=u' \n\t\t\t\t\t\tA component byte stream element <stream> may be composed of one or more subsidiary streams. An MPEG4 file, for example, might contain separate audio and video streams, each of which is associated with technical metadata. The repeatable <stream> element provides a mechanism to record the existence of separate data streams within a particular file, and the opportunity to associate <dmdSec> and <amdSec> with those subsidiary data streams if desired. '))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FLocat'), CTD_ANON_5, scope=fileType, documentation=u' \n\t\t\t\t\t\tThe file location element <FLocat> provides a pointer to the location of a content file. It uses the XLink reference syntax to provide linking information indicating the actual location of the content file, along with other attributes specifying additional linking information. NOTE: <FLocat> is an empty element. The location of the resource pointed to MUST be stored in the xlink:href attribute.\n\t\t\t\t\t'))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'file'), fileType, scope=fileType))
fileType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'stream'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'file'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FContent'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FLocat'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'transformFile'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'transformFile'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'file'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'stream'))),
    ])
})



behaviorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'interfaceDef'), objectType, scope=behaviorType, documentation=u'\n\t\t\t\t\t\tThe interface definition <interfaceDef> element contains a pointer to an abstract definition of a single behavior or a set of related behaviors that are associated with the content of a METS object. The interface definition object to which the <interfaceDef> element points using xlink:href could be another digital object, or some other entity, such as a text file which describes the interface or a Web Services Description Language (WSDL) file. Ideally, an interface definition object contains metadata that describes a set of behaviors or methods. It may also contain files that describe the intended usage of the behaviors, and possibly files that represent different expressions of the interface definition.\t\t\n\t\t\t'))

behaviorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'mechanism'), objectType, scope=behaviorType, documentation=u' \n\t\t\t\t\tA mechanism element <mechanism> contains a pointer to an executable code module that implements a set of behaviors defined by an interface definition. The <mechanism> element will be a pointer to another object (a mechanism object). A mechanism object could be another METS object, or some other entity (e.g., a WSDL file). A mechanism object should contain executable code, pointers to executable code, or specifications for binding to network services (e.g., web services).\n\t\t\t\t\t'))
behaviorType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=behaviorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'interfaceDef'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=behaviorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mechanism'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=behaviorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mechanism'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'xmlData'), CTD_ANON_11, scope=CTD_ANON_14, documentation=u'\n\t\t\t\t\t\t\t\t\tAn xml data wrapper element <xmlData> is used to contain  an XML encoded file. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> element is set to \u201clax\u201d. Therefore, if the source schema and its location are identified by means of an xsi:schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'binData'), pyxb.binding.datatypes.base64Binary, scope=CTD_ANON_14, documentation=u'\n\t\t\t\t\t\t\t\t\tA binary data wrapper element <binData> is used to contain a Base64 encoded file.\n\t\t\t\t\t\t\t\t'))
CTD_ANON_14._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'xmlData'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'binData'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'metsDocumentID'), CTD_ANON_1, scope=CTD_ANON_16, documentation=u'    \n\t\t\t\t\t\t\t\t\tThe metsDocument identifier element <metsDocumentID> allows a unique identifier to be assigned to the METS document itself.  This may be different from the OBJID attribute value in the root <mets> element, which uniquely identifies the entire digital object represented by the METS document.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'agent'), CTD_ANON_20, scope=CTD_ANON_16, documentation=u'agent: \n\t\t\t\t\t\t\t\tThe agent element <agent> provides for various parties and their roles with respect to the METS record to be documented.  \n\t\t\t\t\t\t\t\t'))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'altRecordID'), CTD_ANON_2, scope=CTD_ANON_16, documentation=u'    \n\t\t\t\t\t\t\t\t\tThe alternative record identifier element <altRecordID> allows one to use alternative record identifier values for the digital object represented by the METS document; the primary record identifier is stored in the OBJID attribute in the root <mets> element.\n\t\t\t\t\t\t\t\t'))
CTD_ANON_16._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'agent'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'altRecordID'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'metsDocumentID'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



seqType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'par'), parType, scope=seqType))

seqType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'area'), areaType, scope=seqType))
seqType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=seqType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'par'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=seqType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'area'))),
    ])
})



parType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'seq'), seqType, scope=parType))

parType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'area'), areaType, scope=parType))
parType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=parType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'seq'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=parType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'area'))),
    ])
})



CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), pyxb.binding.datatypes.string, scope=CTD_ANON_20, documentation=u' \n\t\t\t\t\t\t\t\t\t\t\tThe element <name> can be used to record the full name of the document agent.\n\t\t\t\t\t\t\t\t\t\t\t'))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'note'), pyxb.binding.datatypes.string, scope=CTD_ANON_20, documentation=u" \n\t\t\t\t\t\t\t\t\t\t\tThe <note> element can be used to record any additional information regarding the agent's activities with respect to the METS document.\n\t\t\t\t\t\t\t\t\t\t\t"))
CTD_ANON_20._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'note'))),
    ])
})



structMapType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'div'), divType, scope=structMapType, documentation=u" \n\t\t\t\t\t\tThe structural divisions of the hierarchical organization provided by a <structMap> are represented by division <div> elements, which can be nested to any depth. Each <div> element can represent either an intellectual (logical) division or a physical division. Every <div> node in the structural map hierarchy may be connected (via subsidiary <mptr> or <fptr> elements) to content files which represent that div's portion of the whole document. \n\t\t\t\t\t"))
structMapType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=structMapType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'div'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



CTD_ANON_21._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'xmlData'), CTD_ANON_6, scope=CTD_ANON_21, documentation=u'\n\t\t\t\t\t\t\t\t\tThe xml data wrapper element <xmlData> is used to contain XML encoded metadata. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> is set to \u201clax\u201d. Therefore, if the source schema and its location are identified by means of an XML schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element. \t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t'))

CTD_ANON_21._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'binData'), pyxb.binding.datatypes.base64Binary, scope=CTD_ANON_21, documentation=u' \n\t\t\t\t\t\t\t\t\tThe binary data wrapper element <binData> is used to contain Base64 encoded metadata.\t\t\t\t\t\t\t\t\t\t\t\t'))
CTD_ANON_21._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_21._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'xmlData'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_21._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'binData'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'seq'), seqType, scope=CTD_ANON_22, documentation=u'  \n\t\t\t\t\t\t\t\t\tThe sequence of files element <seq> aggregates pointers to files,  parts of files and/or parallel sets of files or parts of files  that must be played or displayed sequentially to manifest a block of digital content. This might be the case, for example, if the parent <div> element represented a logical division, such as a diary entry, that spanned multiple pages of a diary and, hence, multiple page image files. In this case, a <seq> element would aggregate multiple, sequentially arranged <area> elements, each of which pointed to one of the image files that must be presented sequentially to manifest the entire diary entry. If the diary entry started in the middle of a page, then the first <area> element (representing the page on which the diary entry starts) might be further qualified, via its SHAPE and COORDS attributes, to specify the specific, pertinent area of the associated image file.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'area'), areaType, scope=CTD_ANON_22, documentation=u' \n\t\t\t\t\t\t\t\t\tThe area element <area> typically points to content consisting of just a portion or area of a file represented by a <file> element in the <fileSec>. In some contexts, however, the <area> element can also point to content represented by an integral file. A single <area> element would appear as the direct child of a <fptr> element when only a portion of a <file>, rather than an integral <file>, manifested the digital content represented by the <fptr>. Multiple <area> elements would appear as the direct children of a <par> element or a <seq> element when multiple files or parts of files manifested the digital content represented by an <fptr> element. When used in the context of a <par> or <seq> element an <area> element can point either to an integral file or to a segment of a file as necessary.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'par'), parType, scope=CTD_ANON_22, documentation=u' \n\t\t\t\t\t\t\t\t\tThe <par> or parallel files element aggregates pointers to files, parts of files, and/or sequences of files or parts of files that must be played or displayed simultaneously to manifest a block of digital content represented by an <fptr> element. This might be the case, for example, with multi-media content, where a still image might have an accompanying audio track that comments on the still image. In this case, a <par> element would aggregate two <area> elements, one of which pointed to the image file and one of which pointed to the audio file that must be played in conjunction with the image. The <area> element associated with the image could be further qualified with SHAPE and COORDS attributes if only a portion of the image file was pertinent and the <area> element associated with the audio file could be further qualified with BETYPE, BEGIN, EXTTYPE, and EXTENT attributes if only a portion of the associated audio file should be played in conjunction with the image.\n\t\t\t\t\t\t\t\t'))
CTD_ANON_22._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'par'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'area'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'seq'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
