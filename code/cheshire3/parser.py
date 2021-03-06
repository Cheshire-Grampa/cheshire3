
import re
import cStringIO
import StringIO

from xml.sax import ContentHandler, make_parser, ErrorHandler
from xml.sax import parseString as saxParseString
from xml.sax import InputSource as SaxInput
from xml.sax.saxutils import escape
from xml.dom.minidom import parseString as domParseString

from cheshire3.configParser import C3Object
from cheshire3.baseObjects import Parser
from cheshire3.record import SaxRecord, SaxContentHandler, MinidomRecord
from cheshire3.record import LxmlRecord
from cheshire3.utils import flattenTexts, elementType, nonTextToken

# utility function to update data on record from document

class BaseParser(Parser):
    def _copyData(self, doc, rec):
        rec.filename = doc.filename
        rec.tagName = doc.tagName
        rec.processHistory = doc.processHistory
        rec.processHistory.append(self.id)
        if doc.documentStore:
            rec.parent = ('document', doc.documentStore, doc.id)
        elif doc.parent:
            rec.parent = doc.parent


class MinidomParser(BaseParser):
    """ Use default Python Minidom implementation to parse document """

    def process_document(self, session, doc):
        xml = doc.get_raw(session)
        dom = domParseString(xml)
        rec = MinidomRecord(dom, xml)
        self._copyData(doc, rec)
        return rec


class SaxParser(BaseParser):
    """ Default SAX based parser. Creates SaxRecord """

    _possibleSettings = {'namespaces' : {'docs' : "Enable namespace processing in SAX"},
                         'stripWhitespace' : {'docs' : "Strip additional whitespace when processing."},
			 'attrHash' : {'docs' : "Tag/Attribute combinations to include in hash."}
			 }

    def __init__(self, session, config, parent):
        Parser.__init__(self, session, config, parent)
        self.parser = make_parser()
        self.errorHandler = ErrorHandler()
        self.parser.setErrorHandler(self.errorHandler)
        self.inputSource = SaxInput()
        ch = SaxContentHandler()
        self.contentHandler  = ch
        self.parser.setContentHandler(ch)
        self.keepError = 1

        if (self.get_setting(session, 'namespaces')):
            self.parser.setFeature('http://xml.org/sax/features/namespaces', 1)
        p = self.get_setting(session, 'attrHash')
        if (p):
            l = p.split()
            for i in l:
                (a,b) = i.split("@")
                try:
                    ch.hashAttributesNames[a].append(b)
                except:
                    ch.hashAttributesNames[a] = [b]
        if self.get_setting(session, 'stripWhitespace'):
            ch.stripWS = 1

    def process_document(self, session, doc):

        xml = doc.get_raw(session)        
        self.inputSource.setByteStream(cStringIO.StringIO(xml))        
        ch = self.contentHandler
        ch.reinit()
        try:
            self.parser.parse(self.inputSource)
        except:
            # Splat.  Reset self and reraise
            if self.keepError:
                # Work out path
                path = []
                for l in ch.pathLines:
                    line = ch.currentText[l]
                    elemName = line[2:line.index('{')-1]
                    path.append("%s[@SAXID='%s']" % (elemName, l))
                self.errorPath = '/'.join(path)
            else:
                ch.reinit()
                
            raise        
        rec = SaxRecord(ch.currentText, xml, wordCount=ch.recordWordCount)
        rec.elementHash = ch.elementHash
        rec.byteCount = len(xml)
        self._copyData(doc, rec)
        ch.reinit()
        return rec


class StoredSaxParser(BaseParser):

    def process_document(self, session, doc):
        data = doc.get_raw(session)
        data = unicode(data, 'utf-8')
        sax = data.split(nonTextToken)
        if sax[-1][0] == "9":
            line = sax.pop()
            elemHash = pickle.loads(str(line[2:]))
        else:
            elemHash = {}
        rec = SaxRecord(sax)
        rec.elementHash = elemHash
        return rec


try:
    
    from lxml import etree
    
except ImportError:
    
    # Define empty classes
    class LxmlParser(Parser):
        """ lxml based Parser.  Creates LxmlRecords """
        pass
    
    class LxmlSchemaParser(Parser):
        pass
    
    
    class LxmlRelaxNGParser(Parser):
        pass


    class LxmlHtmlParser(BaseParser):
        """ lxml based parser for HTML documents """
        pass
    
else:
    
    class LxmlParser(BaseParser):
        """ lxml based Parser.  Creates LxmlRecords """
        
        _possibleSettings = {'validateDTD': {'docs': "Validate to DTD while parsing (if a DTD was referenced by the Document.)", 'type' : int, 'options' : "0|1"},
                             'allowNetwork': {'docs': "Allow network access to look up external documents (DTDs etc.)", 'type' : int, 'options' : "0|1"}
                             }
        
        def __init__(self, session, config, parent):
            BaseParser.__init__(self, session ,config, parent)
            dtdVal = bool(self.get_setting(session, 'validateDTD', 0))
            noNetwork = not self.get_setting(session, 'allowNetwork', 0)
            self.parser = etree.XMLParser(dtd_validation=dtdVal, no_network=noNetwork)
        
        def process_document(self, session, doc):
            # input must be string or stream
            data = doc.get_raw(session)
            try:
                et = etree.parse(StringIO.StringIO(data), self.parser)
            except AssertionError:
                data = data.decode('utf8')
                et = etree.parse(StringIO.StringIO(data), self.parser)
            rec = LxmlRecord(et)
            rec.byteCount = len(data)
            self._copyData(doc, rec)
            return rec


    class LxmlSchemaParser(Parser):
        pass
    
    
    class LxmlRelaxNGParser(Parser):
        pass


    class LxmlHtmlParser(BaseParser):
        """ lxml based parser for HTML documents """

        def __init__(self, session, config, parent):
            BaseParser.__init__(self, session ,config, parent)
            self.parser = etree.HTMLParser()

        def process_document(self, session, doc):
            data = doc.get_raw(session)
            et = etree.parse(StringIO.StringIO(data), self.parser)
            rec = LxmlRecord(et)
            rec.byteCount = len(data)
            self._copyData(doc, rec)
            return rec


class PassThroughParser(BaseParser):
    """ Copy the data from a document (eg list of sax events or a dom tree) into an appropriate record object """

    def process_document(self, session, doc):
        # Simply copy data into a record of appropriate type
        data = doc.get_raw(session)
        if (typeof(data) == types.ListType):
            rec = SaxRecord(data)
        else:
            rec = DomRecord(data)
        self._copyData(doc, rec)
        return rec


# Copy
from record import MarcRecord
class MarcParser(BaseParser):
    """ Creates MarcRecords which fake the Record API for Marc """
    def process_document(self, session, doc):
        return MarcRecord(doc)

