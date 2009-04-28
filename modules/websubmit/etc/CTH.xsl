<?xml version="1.0" encoding="UTF-8"?>
<!-- $Id: CTH.xsl,v 1.2 2007/08/14 12:36:17 diane Exp $

     This file is part of CDS Invenio.
     Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.

     CDS Invenio is free software; you can redistribute it and/or
     modify it under the terms of the GNU General Public License as
     published by the Free Software Foundation; either version 2 of the
     License, or (at your option) any later version.

     CDS Invenio is distributed in the hope that it will be useful, but
     WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
     General Public License for more details.  

     You should have received a copy of the GNU General Public License
     along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
     59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
-->
<!--
<name>CTH</name>
<description>Generate the marc xml for CERN thesis</description>
-->

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:fn="http://cdsweb.cern.ch/websubmit/fn"
exclude-result-prefixes="fn">
<xsl:output method="xml" encoding="UTF-8"/>

<xsl:template match="/record">
  <!--The ouput is encapsulated into a <record></record>-->
  <xsl:element name="record"> 
    <!--Main apply-template for child nodes:
        All the nodes must have a "template match" statement(possibly an empty one) 
        otherwise xslt display them using one of the default built-in template 
        (e.g for text node it display the content). Alternatively we can specify 
        in the main apply-template(just below) which nodes must not be considered as their 
        values are accessed trough other templates.-->
    <xsl:apply-templates select="node()[not(self::WSE_university) and not(self::WSE_subtitle)and not(self::WSE_place)and not(self::WSE_publisher) and not (self::WSE_diploma)]">
    </xsl:apply-templates>
    <!--Static tags (don't depend on field's values)-->
    <xsl:call-template name="datafield_with_one_subfield">
      <xsl:with-param name="tag" select="'041'"/>
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value" select="'eng'"/>
    </xsl:call-template>
    <xsl:call-template name="datafield_with_one_subfield">
      <xsl:with-param name="tag" select="'595'"/>
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value" select="'CERN EDS'"/>
    </xsl:call-template>
    <xsl:call-template name="datafield_with_one_subfield">
      <xsl:with-param name="tag" select="'690'"/>
      <xsl:with-param name="ind1" select="'C'"/>
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value" select="'CERN'"/>
    </xsl:call-template>
    <xsl:call-template name="datafield_with_one_subfield">
      <xsl:with-param name="tag" select="'690'"/>
      <xsl:with-param name="ind1" select="'C'"/>
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value" select="'PROVISIONALTHESIS'"/>
    </xsl:call-template>
    <xsl:call-template name="static_tag_916"/>
    <xsl:call-template name="datafield_with_one_subfield">
      <xsl:with-param name="tag" select="'960'"/>
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value" select="'29'"/>
    </xsl:call-template>
    <xsl:call-template name="datafield_with_one_subfield">
      <xsl:with-param name="tag" select="'963'"/>
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value" select="'PUBLIC'"/>
    </xsl:call-template>
    <!--xsl:call-template name="datafield_with_one_subfield">
      <xsl:with-param name="tag" select="'859'"/>
      <xsl:with-param name="code" select="'f'"/>
      <xsl:with-param name="value" select="fn:read_file('/home/berkovits/SuE')"/>
    </xsl:call-template-->
  </xsl:element>
</xsl:template>

<xsl:template match="WSE_abstract[value!='']">
  <xsl:call-template name="datafield_with_one_subfield">
    <xsl:with-param name="tag" select="'520'"/>
    <xsl:with-param name="code" select="'a'"/>
    <xsl:with-param name="value"><xsl:value-of select="./value"/></xsl:with-param> 
  </xsl:call-template>
</xsl:template>

<xsl:template match="WSE_other_rep[value!='']">
  <xsl:for-each select="./value">
    <xsl:sort select="@id" order="ascending"/>
    <xsl:if test="position()=1">
      <xsl:call-template name="datafield_with_one_subfield">
        <xsl:with-param name="tag" select="'690'"/>
        <xsl:with-param name="ind1" select="'C'"/>
        <xsl:with-param name="code" select="'a'"/>
        <xsl:with-param name="value" select="'REPORT'"/>
      </xsl:call-template>
    </xsl:if>
    <xsl:call-template name="datafield_with_one_subfield">
      <xsl:with-param name="tag" select="'088'"/>
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value"><xsl:value-of select="."/></xsl:with-param> 
    </xsl:call-template>
  </xsl:for-each>
</xsl:template>

<xsl:template match="WSE_authors/value[@id='1']"> 
  <xsl:element name="datafield">
    <xsl:attribute name="tag"><xsl:value-of select="'100'"/></xsl:attribute>
    <xsl:attribute name="ind1"><xsl:value-of select="''"/></xsl:attribute>
    <xsl:attribute name="ind2"><xsl:value-of select="''"/></xsl:attribute>
    <xsl:call-template name="subfield">
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value"><xsl:value-of select="./surname"/>, <xsl:value-of select="./forename"/></xsl:with-param> 
    </xsl:call-template>
    <xsl:call-template name="subfield">
      <xsl:with-param name="code" select="'u'"/>
      <xsl:with-param name="value" select="./affiliation"/>
    </xsl:call-template>
  </xsl:element>
</xsl:template>

<xsl:template match="WSE_authors/value[@id>'1']"> 
  <xsl:for-each select=".">
    <xsl:element name="datafield">
      <xsl:attribute name="tag"><xsl:value-of select="'700'"/></xsl:attribute>
      <xsl:attribute name="ind1"><xsl:value-of select="''"/></xsl:attribute>
      <xsl:attribute name="ind2"><xsl:value-of select="''"/></xsl:attribute>
      <xsl:call-template name="subfield">
        <xsl:with-param name="code" select="'a'"/>
        <xsl:with-param name="value"><xsl:value-of select="./surname"/>, <xsl:value-of select="./forename"/></xsl:with-param> 
      </xsl:call-template>
      <xsl:call-template name="subfield">
        <xsl:with-param name="code" select="'u'"/>
        <xsl:with-param name="value" select="./affiliation"/>
      </xsl:call-template>
    </xsl:element>
  </xsl:for-each>
</xsl:template>

<xsl:template match="WSE_supervisors[value!='']"> 
  <xsl:for-each select="./value">
    <xsl:element name="datafield">
      <xsl:attribute name="tag"><xsl:value-of select="'700'"/></xsl:attribute>
      <xsl:attribute name="ind1"><xsl:value-of select="''"/></xsl:attribute>
      <xsl:attribute name="ind2"><xsl:value-of select="''"/></xsl:attribute>
      <xsl:call-template name="subfield">
        <xsl:with-param name="code" select="'a'"/>
        <xsl:with-param name="value"><xsl:value-of select="./surname"/>, <xsl:value-of select="./forename"/></xsl:with-param> 
      </xsl:call-template>
      <xsl:call-template name="subfield">
        <xsl:with-param name="code" select="'e'"/>
        <xsl:with-param name="value" select="'dir.'"/>
      </xsl:call-template>
    </xsl:element>
  </xsl:for-each> 
</xsl:template>

<xsl:template match="WSE_title[value!='']"> 
  <xsl:element name="datafield">
    <xsl:attribute name="tag"><xsl:value-of select="'245'"/></xsl:attribute>
    <xsl:attribute name="ind1"><xsl:value-of select="''"/></xsl:attribute>
    <xsl:attribute name="ind2"><xsl:value-of select="''"/></xsl:attribute>
    <xsl:call-template name="subfield">
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value"><xsl:value-of select="."/></xsl:with-param> 
    </xsl:call-template>
    <xsl:call-template name="subfield">
      <xsl:with-param name="code" select="'b'"/>
      <xsl:with-param name="value"><xsl:value-of select="../WSE_subtitle/value"/></xsl:with-param> 
    </xsl:call-template>
  </xsl:element>
</xsl:template>

<xsl:template match="WSE_date"> 
 <xsl:element name="datafield">
   <xsl:attribute name="tag"><xsl:value-of select="'269'"/></xsl:attribute>
   <xsl:attribute name="ind1"><xsl:value-of select="''"/></xsl:attribute>
   <xsl:attribute name="ind2"><xsl:value-of select="''"/></xsl:attribute>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'c'"/>
     <xsl:with-param name="value"><xsl:value-of select="./value/y"/></xsl:with-param> 
   </xsl:call-template>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'a'"/>
     <xsl:with-param name="value"><xsl:value-of select="../WSE_place/value"/></xsl:with-param> 
   </xsl:call-template>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'b'"/>
     <xsl:with-param name="value"><xsl:value-of select="../WSE_publisher/value"/></xsl:with-param> 
   </xsl:call-template>
 </xsl:element>
 <xsl:call-template name="datafield_with_one_subfield">
    <xsl:with-param name="tag" select="'500'"/>
    <xsl:with-param name="code" select="'a'"/>
    <xsl:with-param name="value">
      <xsl:value-of select="'Presented on '"/>
      <xsl:value-of select="./value/d"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="fn:look_up_KB(./value/m, '/usr/local/invenio/etc/bibconvert/KB/Month.KB', '8')"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="./value/y"/>
    </xsl:with-param>
  </xsl:call-template>
  <xsl:element name="datafield">
   <xsl:attribute name="tag"><xsl:value-of select="'502'"/></xsl:attribute>
   <xsl:attribute name="ind1"><xsl:value-of select="''"/></xsl:attribute>
   <xsl:attribute name="ind2"><xsl:value-of select="''"/></xsl:attribute>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'c'"/>
     <xsl:with-param name="value"><xsl:value-of select="./value/y"/></xsl:with-param> 
   </xsl:call-template>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'a'"/>
     <xsl:with-param name="value"><xsl:value-of select="../WSE_diploma/value"/></xsl:with-param> 
   </xsl:call-template>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'b'"/>
     <xsl:with-param name="value"><xsl:value-of select="../WSE_university/value"/></xsl:with-param> 
   </xsl:call-template>
 </xsl:element>
</xsl:template>

<xsl:template match="WSE_pages"> 
 <xsl:element name="datafield">
   <xsl:attribute name="tag"><xsl:value-of select="'300'"/></xsl:attribute>
   <xsl:attribute name="ind1"><xsl:value-of select="''"/></xsl:attribute>
   <xsl:attribute name="ind2"><xsl:value-of select="''"/></xsl:attribute>
   <xsl:choose>
     <xsl:when test="./value!=''">
       <xsl:call-template name="subfield">
         <xsl:with-param name="code" select="'a'"/>
         <xsl:with-param name="value"><xsl:value-of select="./value"/>p</xsl:with-param> 
       </xsl:call-template>
     </xsl:when>
     <xsl:otherwise>
      <xsl:call-template name="subfield">
         <xsl:with-param name="code" select="'a'"/>
         <xsl:with-param name="value" select="'mult. p'"/>
      </xsl:call-template>
     </xsl:otherwise>
   </xsl:choose>
 </xsl:element>
</xsl:template>

<xsl:template match="WSE_experiment[value='ALEPH']"> 
  <xsl:call-template name="datafield_with_one_subfield">
    <xsl:with-param name="tag" select="'490'"/>
    <xsl:with-param name="code" select="'a'"/>
    <xsl:with-param name="value" select="'ALEPH Theses'"/>
  </xsl:call-template>
</xsl:template>

<xsl:template match="WSE_main[value!='']"> 
  <xsl:call-template name="datafield_with_one_subfield">
    <xsl:with-param name="tag" select="'FFT'"/>
    <xsl:with-param name="ind1" select="''"/>
    <xsl:with-param name="code" select="'a'"/>
    <xsl:with-param name="value" select="./value"/>
  </xsl:call-template>
</xsl:template>

<xsl:template match="WSE_experiment[value!='']"> 
  <xsl:element name="datafield">
    <xsl:attribute name="tag"><xsl:value-of select="'693'"/></xsl:attribute>
    <xsl:attribute name="ind1"><xsl:value-of select="''"/></xsl:attribute>
    <xsl:attribute name="ind2"><xsl:value-of select="''"/></xsl:attribute>
    <xsl:call-template name="subfield">
      <xsl:with-param name="code" select="'a'"/>
      <xsl:with-param name="value">
      <xsl:value-of select="fn:look_up_KB(., '/usr/local/invenio/etc/bibconvert/KB/SISUC-693e---693a.kb', '2')"/>
    </xsl:with-param>
    </xsl:call-template>
     <xsl:call-template name="subfield">
      <xsl:with-param name="code" select="'e'"/>
      <xsl:with-param name="value" select="."/>
  </xsl:call-template>
  </xsl:element>
</xsl:template>

<xsl:template match="WSE_Subject[value!='']"> 
 <xsl:element name="datafield">
   <xsl:attribute name="tag"><xsl:value-of select="'650'"/></xsl:attribute>
   <xsl:attribute name="ind1"><xsl:value-of select="'1'"/></xsl:attribute>
   <xsl:attribute name="ind2"><xsl:value-of select="'7'"/></xsl:attribute>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'a'"/>
     <xsl:with-param name="value"><xsl:value-of select="./value"/></xsl:with-param> 
   </xsl:call-template>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'2'"/>
     <xsl:with-param name="value" select="'SzGeCERN'"/>
   </xsl:call-template>
 </xsl:element>
</xsl:template>

<xsl:template match="WSE_CernDepartements[value!='']"> 
  <xsl:call-template name="datafield_with_one_subfield">
    <xsl:with-param name="tag" select="'710'"/>
    <xsl:with-param name="code" select="'5'"/>
    <xsl:with-param name="value"><xsl:value-of select="./value"/></xsl:with-param> 
  </xsl:call-template>
</xsl:template>


<!--Common functions-->

<!--Marc 21 datafield with one subfield-->
<xsl:template name="datafield_with_one_subfield">
 <xsl:param name="tag"/>
 <xsl:param name="ind1"/>
 <xsl:param name="ind2"/>
 <xsl:param name="code"/>
 <xsl:param name="value"/>
 <xsl:element name="datafield">
   <xsl:attribute name="tag"><xsl:value-of select="$tag"/></xsl:attribute>
   <xsl:attribute name="ind1"><xsl:value-of select="$ind1"/></xsl:attribute>
   <xsl:attribute name="ind2"><xsl:value-of select="$ind2"/></xsl:attribute>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="$code"/>
     <xsl:with-param name="value" select="$value"/>
   </xsl:call-template>
 </xsl:element>
</xsl:template>

<!--Datafield for tag 916-->
<xsl:template name="static_tag_916">
 <xsl:element name="datafield">
   <xsl:attribute name="tag"><xsl:value-of select="'916'"/></xsl:attribute>
   <xsl:attribute name="ind1"><xsl:value-of select="''"/></xsl:attribute>
   <xsl:attribute name="ind2"><xsl:value-of select="''"/></xsl:attribute>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'s'"/>
     <xsl:with-param name="value" select="'n'"/>
   </xsl:call-template>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'w'"/>
     <xsl:with-param name="value">
       <xsl:value-of select="fn:current_date('%Y%U')"/>
     </xsl:with-param>
   </xsl:call-template>
   <xsl:call-template name="subfield">
     <xsl:with-param name="code" select="'y'"/>
     <xsl:with-param name="value">
       <xsl:value-of select="'a'"/>
       <xsl:value-of select="fn:current_date('%Y')"/>
     </xsl:with-param>
   </xsl:call-template>
 </xsl:element>
</xsl:template>

<!--Marc 21 subfield-->
<xsl:template name="subfield">
 <xsl:param name="code"/>
 <xsl:param name="value"/>
 <xsl:if test="$value!=''">
   <xsl:element name="subfield">
     <xsl:attribute name="code"><xsl:value-of select="$code"/></xsl:attribute>
     <xsl:value-of select="$value"/>
   </xsl:element>
 </xsl:if>
</xsl:template>
</xsl:stylesheet>

