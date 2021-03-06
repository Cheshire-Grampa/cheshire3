# Version 1.0b1

from cheshire3.session import Session
from cheshire3.configParser import C3Object

class Server(C3Object):
    """A Server object is a collection point for other objects, and an
    initial entry into the system for requests from a
    ProtocolHandler. A server might know about several Databases,
    RecordStores and so forth, but its main function is to check
    whether the request should be accepted or not and create an
    environment in which the request can be processed. It will likely
    have access to a UserStore database which maintains authentication
    and authorisation information. The exact nature of this
    information is not defined, allowing many possible backend
    implementations. Servers are the top level of configuration for
    the system and hence their constructor requires the path to a
    local XML configuration file, however from then on configuration
    information may be retrieved from other locations such as a remote
    datastore to enable distributed environments to maintain
    synchronicity."""

    databases = {}
    authStore = None
    resultSetStore = None
    queryStore = None

    def __init__(self, session, configFile="serverConfig.xml"):
        """The constructer takes a Session object and a file path to
        the configuration file to be parsed and processed.
        """
        raise(NotImplementedError)



class Database(C3Object):
    """A Database is a collection of Records and Indexes. It is
    responsable for maintaining and allowing access to its components,
    as well as metadata associated with the collections. It must be
    able to interpret a request, splitting it amongst its known
    resources and then recombine the values into a single response."""
    indexes = {}
    protocolMaps = {}
    recordStore = None

    def add_record(self, session, rec):
        """Ensure that a record is registered with the database.  This
        function does not ensure persistence of the record, not index
        it, just perform registration"""
        raise(NotImplementedError)

    def remove_record(self, session, rec):
        """Unregister the record."""
        raise(NotImplementedError)

    def index_record(self, session, rec):
        """Sends the record to all indexes registered with the database to be indexes"""
        raise(NotImplementedError)

    def unindex_record(self, session, rec):
        """Sends the record to all indexes registered with the database to be removed/unindexed"""
        raise(NotImplementedError)


    def begin_indexing(self, session):
        """Perform tasks before records are to be indexed"""
        raise(NotImplementedError)

    def commit_indexing(self, session):
        """Perform tasks after records have been sent to indexes.  For
        example, commit any temporary data to IndexStores"""
        raise(NotImplementedError)

    def reindex(self, session):
        """ Reindex all records registered with the database"""
        raise(NotImplementedError)


    def scan(self, session, clause, nTerms, direction=">="):
        """Given a CQL query (single searchClause), resolve the index
        and return a section of the term list"""
        raise(NotImplementedError)

    def search(self, session, query):
        """ Given a CQL query, perform the query and return a resultSet"""
        raise(NotImplementedError)

    def sort(self, session, resultSets, sortKeys):
        """ Take one or more resultSets and sort/merge by sortKeys """
        raise(NotImplementedError)


    def commit_metadata(self, session):
        """Ensure persistence of database metadata"""
        raise(NotImplementedError)

    def accumulate_metadata(self, session, obj):
        """ """
        raise(NotImplementedError)


class Index(C3Object):
    """An Index is an object which defines an access point into
    records and is responsable for extracting that information from
    them. It can then store the information extracted in an
    IndexStore. The entry point can be defined using one or more XPath
    expressions, and the extraction process can be defined using a
    workflow chain of standard objects. These chains must start with
    an Extractor, but from there might then include PreParsers,
    Parsers, Transformers, Normalizers and even other Indexes.  The
    index can also be the last object in a regular Workflow, so long
    as an XPath object is used to find the data in the record
    immediately before an Extractor."""
    indexStore = None

    def begin_indexing(self, session):
        """ Perform tasks before indexing any records """
        raise(NotImplementedError)

    def commit_indexing(self, session):
        """ Perform tasks after records have been indexed """
        raise(NotImplementedError)

    def index_record(self, session, rec):
        """ Accept a record to index.  If begin indexing has been
        called, the index might not commit any data until
        commit_indexing is called.  If it is not in batch mode, then
        index_record will also commit the terms to the indexStore."""
        raise(NotImplementedError)

    def delete_record(self, session, rec):
        """ Delete all the terms of the given record from the indexes.
        Does this by extracting the terms from the record, finding and
        removing them. Hence the record must be the same as the one
        that was indexed."""
        raise(NotImplementedError)

    def store_terms(self, session, data, rec):
        raise(NotImplementedError)

    def extract_data(self, session, rec):
        raise(NotImplementedError)

    def fetch_term(self, session, term, summary, prox):
        raise(NotImplementedError)

    def fetch_termById(self, session, termId):
        raise(NotImplementedError)

    def fetch_termList(self, session, term, nTerms, relation, end, summary):
        raise(NotImplementedError)

    def fetch_vector(self, session, rec, summary):
        raise(NotImplementedError)

    def fetch_proxVector(self, session, rec, elemId=-1):
        raise(NotImplementedError)

    def fetch_summary(self, session):
        raise(NotImplementedError)

    def fetch_termFrequencies(self, session, mType, start, nTerms, direction):
        raise(NotImplementedError)

    def clear(self, session):
        raise(NotImplementedError)
    
    def scan(self, session, clause, nTerms, direction=">="):
        """Produce an ordered term list with document frequencies and total occurences """
        raise(NotImplementedError)

    def search(self, session, clause, db):
        """Search this particular index given a CQL clause, return a resultSet object"""
        raise(NotImplementedError)

    def sort(self, session, rset):
        """Sort a result set based on the values extracted according to this index."""
        raise(NotImplementedError)


    def serialize_term(self, session, termId, data, nRecs=0, nOccs=0):
        """Callback from IndexStore to serialise list of terms and
        document references to be stored"""
        raise(NotImplementedError)

    def deserialize_term(self, session, data, nRecs=-1, prox=1):
        """Callback from IndexStore to take serialised data and
        produce list of terms and document references."""
        raise(NotImplementedError)

    def merge_term(self, session, currentData, newData, op="replace", nRecs=0, nOccs=0):
        """Callback from IndexStore to take two sets of terms and merge them together."""
        raise(NotImplementedError)

    def construct_resultSetItem(self, session, term, rsiType=""):
        """Take a single item, as stored in this Index, and produce a ResultSetItem representation."""
        raise(NotImplementedError)

    def construct_resultSet(self, session, terms, queryHash={}):
        """Take a list of terms and produce an appropriate ResultSet object."""
        raise(NotImplementedError)

    def calc_sectionOffsets(self, session, start, nRecs, dataLen=0):
        raise(NotImplementedError)



class Selector(C3Object):
    """A Selector is a simple wrapper around an XPath or other means of selecting data from a parsed structure in a Record"""
    def process_record(self, session, record):
        """Process the given record and return the results."""
        raise(NotImplementedError)


# Takes some data, returns a list of extracted values
class Extractor(C3Object):
    """An Extractor is a processing object called by an Index with the
    value of an evaluated XPath expression or with a string. Example
    normalizers might extract keywords from an element or the entire
    contents thereof as a single string. Extractors must also be used
    on the query terms to apply the same keyword processing rules, for
    example."""
    def process_string(self, session, data):
        """Process a raw string, eg from an attribute value or the query."""
        raise(NotImplementedError)
    def process_node(self, session, data):
        """Process a DOM node."""
        raise(NotImplementedError)
    def process_eventList(self, session, data):
        """Process a list of SAX events serialised in C3 internal format."""
        raise(NotImplementedError)
    def process_xpathResult(self, session, data):
        """Process the result of an XPath expression. Convenience
        function to wrap the other process_* functions and do type
        checking."""
        raise(NotImplementedError)

class Tokenizer(C3Object):
    u"""A Tokenizer takes a string of language and processes it to produce an ordered list of tokens.
    
    String is commonly in hash, as per output from Extractor"""

    def process_string(self, session, data):
        raise NotImplementedError
    def process_hash(self, session, data):
        raise NotImplementedError

class TokenMerger(C3Object):
    u"""A TokenMerger takes an ordered list of tokens (i.e. as produced by a Tokenizer) and merges them into a hash.
    This might involve merging multiple tokens per key, while maintaining frequency, proximity information etc."""

    def process_string(self, session, data):
        raise NotImplementedError
    def process_hash(self, session, data):
        raise NotImplementedError


# Takes a string, returns a list of normalised values
class Normalizer(C3Object):
    """Normalizer objects are chained after Extractors in order to
    transform the data from the record or query. A Normalizer might
    standardise case, perform stemming or transform a date into
    ISO8601 format. Normalizers are also needed to transform the terms
    in a request into the same format as the term in the Index. For
    example a date index might be searched using a free text date and
    that would need to be parsed into the normalized form in order to
    compare it with the stored data."""
    
    def process_string(self, session, data):
        """Process a string into an alternative form."""
        raise(NotImplementedError)

    def process_hash(self, session, data):
        """Process a hash of values into alternative forms."""
        raise(NotImplementedError)

# Takes raw data, returns one or more Documents

class DocumentFactory(C3Object):
    """ Object Docs """
    def load(self, session, data, cache=None, format=None, tagName=None, codec=""):
        """Load documents into the document factory from data.  (XXX More to come)"""
        raise(NotImplementedError)

    def get_document(self, session, n=-1):
        raise(NotImplementedError)

    def register_stream(self, session, format, cls):
        """ Register an implementation of a DocumentStream (cls) against a name for the format parameter (format)"""
        raise(NotImplementedError)

class QueryFactory(C3Object):
    pass

    

# Takes a Document, returns a Record
class Parser(C3Object):
    """Normally a simple wrapper around an XML parser, these objects
    can be viewed as Record Factories. They take a Document containing
    some XML and produce the equivalent Record."""
    def process_document(self, session, doc):
        """Take a Document, parse it and return a Record object."""
        raise(NotImplementedError)

# Takes a Document, returns a Document
class PreParser(C3Object):
    """A PreParser takes a Document and creates a second one. For
    example, the input document might consist solely of a URL. The
    output would be a Document with the data that the PreParser has
    fetched from that address. This functionality allows for work flow
    chains to be strung together in many ways, and perhaps in ways
    which the original implemention had not foreseen."""
    inMimeType = ""
    outMimeType = ""

    def process_document(self, session, doc):
        """Take a Document, transform it and return a new Document object."""
        raise(NotImplementedError)


# Takes a Record, returns a Document
class Transformer(C3Object):
    """A Transformer is the opposite of a Parser. It takes a Record
    and produces a Document. In many cases this can be handled by an
    XSLT implementation but other instances might include one that
    returns a binary file based on the information in the
    record. Transformers might be used in an indexing chain, but are
    more likely to be used to render a record in a format or schema
    requested by the end user."""
    def process_record(self, session, rec):
        """Take a Record, transform it and return a new Document object."""
        raise(NotImplementedError)


# Users instantiated out of AuthStore like any other configured object
class User(C3Object):
    """An object representing a user of the system to allow for
    convenient access to properties such as username, password and
    rights metadata."""

    username = ''
    password = ''
    rights = []
    email = ''
    realName = ''
    flags = []

    def has_flag(self, session, flag, object=None):
        """Check whether or not the user has the specified flag.  This
        flag may be set regarding a particular object, for example
        write access to a particular store."""
        raise(NotImplementedError)


class ProtocolMap(C3Object):
    """Protocol maps map from an incoming query type to internal indexes based on some specification."""
    protocol = ""
    def resolve_index(self, session, data):
        """Given a query, resolve it and return the index object to be used."""
        raise(NotImplementedError)
    

# --- Store APIs ---

# Not an object store, we just look after terms and indexes
class IndexStore(C3Object):
    """A persistent storage mechanism for extracted terms."""

    def begin_indexing(self, session, index):
        """Perform tasks as required before indexing begins, for example setting batch files."""
        raise(NotImplementedError)
    def commit_indexing(self, session, index):
        """Commit the data to disk from the indexing process."""
        raise(NotImplementedError)
    def commit_centralIndexing(self, session, index, filePath):
        """Commit the data to disk from the indexing process, called automatically unless in distributed mode."""
        raise(NotImplementedError)


    def contains_index(self, session, index):
        """Does the IndexStore currently store the given Index."""
        raise(NotImplementedError)
    def create_index(self, session, index):
        """Create an index in the store."""
        raise(NotImplementedError)
    def clean_index(self, session, index):
        """Remove all the terms from an index, but keep the specification."""
        raise(NotImplementedError)
    def delete_index(self, session, index):
        """Completely delete an index from the store."""
        raise(NotImplementedError)


    def delete_terms(self, session, index, terms, rec=None):
        """Delete the given terms from an index, optionally only for a particular record."""
        raise(NotImplementedError)
    def store_terms(self, session, index, terms, rec):
        """Store terms in the index for a given record."""
        raise(NotImplementedError)

    def create_term(self, session, index, termId, resultSet):
        raise(NotImplementedError)

    def fetch_term(self, session, index, term, summary=0, prox=0):
        """Fetch a single term."""
        raise(NotImplementedError)

    def fetch_termById(self, session, index, termId):
        raise(NotImplementedError)

    def fetch_termList(self, session, index, term, nTerms=0, relation="", end="", summary=0, reverse=0):
        """Fetch a list of terms for an index.
        numReq:  How many terms are wanted.
        relation: Which order to scan through the index.
        end: A point to end at (eg between A and B)
        summary: Only return frequency info, not the pointers to matching records.
        reverse: Use the reversed index if available (eg 'xedni' not 'index').
        """
        raise(NotImplementedError)
    def fetch_sortValue(self, session, index, item):
        """Fetch a stored data value for the given record."""
        raise(NotImplementedError)


    def fetch_vector(self, session, index, rec, summary=0):
        raise(NotImplementedError)

    def fetch_proxVector(self, session, index, rec, elemId=-1):
        raise(NotImplementedError)

    def fetch_summary(self, session, index):
        raise(NotImplementedError)

    def fetch_termFrequencies(self, session, index, mType, start, nTerms, direction):
        raise(NotImplementedError)


    def construct_resultSetItem(self, session, recId, recStoreId, nOccs, rsiType):
        raise(NotImplementedError)


# Store configured objects
class ObjectStore(C3Object):
    """An interface to a persistent storage mechanism for configured Cheshire3 objects."""
    def create_object(self, session, obj=None):
        """Given a Cheshire3 object, create a serialised form of it in the database.
        Note:  You should use create_record() as per RecordStore to create an object from a configuration.
        """
        raise(NotImplementedError)
    def delete_object(self, session, id):
        """Delete an object."""
        raise(NotImplementedError)
    def fetch_object(self, session, id):
        """Fetch an object."""
        raise(NotImplementedError)
    def store_object(self, session, obj):
        """Store an object, potentially overwriting an existing copy."""
        raise(NotImplementedError)

# Store CQL queries
class QueryStore(ObjectStore):
    """An interface to persistent storage for Queries."""
    def create_query(self, session, query=None):
        """Create a new query in the store."""
        raise(NotImplementedError)
    def delete_query(self, session, id):
        """Delete a query from the store."""
        raise(NotImplementedError)
    def fetch_query(self, session, id):
        """Fetch a query from the store."""
        raise(NotImplementedError)
    def store_query(self, session, query):
        """Store a query, potentially overwriting an existing copy."""
        raise(NotImplementedError)


# Store records
class RecordStore(ObjectStore):
    """A persistent storage mechanism for Records. It allows such
    operations as create, update, fetch and delete. It also allows
    fast retrieval of important record metadata, for use with
    computing relevance ranking for example."""

    def create_record(self, session, rec=None):
        """Create a record and assign it a new identifier."""
        raise(NotImplementedError)
    def replace_record(self, session, rec):
        """Permissions checking hook for store_record if the record does not already exist."""
        raise(NotImplementedError)
    def store_record(self, session, rec, transformer=None):
        """Store an existing record. It must already have an identifier assigned to it."""
        raise(NotImplementedError)
    def fetch_record(self, session, id, parser=None):
        """Return the record with the given identifier."""
        raise(NotImplementedError)
    def delete_record(self, session, id):
        """Delete the record with the given identifier from storage."""
        raise(NotImplementedError)
    def fetch_recordMetadata(self, session, id, mType):
        """Return the size of the record, according to its metadata."""
        raise(NotImplementedError)

# Store documents
class DocumentStore(ObjectStore):
    """An interface to a persistent storage mechanism for Documents and their associated metadata."""
    def create_document(self, session, doc=None):
        raise(NotImplementedError)
    def delete_document(self, session, id):
        raise(NotImplementedError)
    def fetch_document(self, session, id):
        raise(NotImplementedError)
    def store_document(self, session, doc):
        raise(NotImplementedError)

# And store result sets
class ResultSetStore(ObjectStore):
    """A persistent storage mechanism for result sets."""
    def create_resultSet(self, session, rset=None):
        raise(NotImplementedError)
    def delete_resultSet(self, session, id):
        raise(NotImplementedError)
    def fetch_resultSet(self, session, id):
        raise(NotImplementedError)
    def store_resultSet(self, session, rset):
        raise(NotImplementedError)


# --- Code Instantiated Objects ---

class Document:
    """A Document is the raw data which will become a record. It may
    be processed into a Record by a Parser, or into another Document
    type by a PreParser. Documents might be stored in a DocumentStore,
    if necessary, but can generally be discarded. Documents may be
    anything from a JPG file, to an unparsed XML file, to a string
    containing a URL. This allows for future compatability with new
    formats, as they may be incorporated into the system by
    implementing a Document type and a PreParser."""
    id = -1
    documentStore = ""
    text = ""
    mimeType = ""
    processHistory = []
    parent = ('','',-1)

    def __init__(self, data, creator="", history=[], mimeType="", parent=None, filename="", tagName="", byteCount=0, byteOffset=0, wordCount=0):
        """The constructer takes the data which should be used to
        construct the document. This is implementation dependant. It
        also optionally may take a creator object, process history
        information and a mimetype.  The parent option is for
        documents which have been extracted from another document, for
        example pages from a book."""
        raise(NotImplementedError)
    def get_raw(self, session):
        """Return the raw data associated with this document."""
        raise(NotImplementedError)


class ResultSet:
    """A collection of records, typically created as the result of a search on a database."""
    termid = -1
    totalOccs = 0
    totalRecs = 0
    id = ""
    expires = ""
    index = None
    queryTerm = ""
    queryFreq = 0
    queryPositions = []
    relevancy = 0
    maxWeight = 0
    minWeight = 0

    def combine(self, session, others, clause):
        raise(NotImplementedError)
    def retrieve(self, session, req):
        raise(NotImplementedError)
    def sort(self, session, req):
        raise(NotImplementedError)

class ResultSetItem(object):
    """An object representing a pointer to a Record, with result set specific metadata.""" 
    id = 0
    recordStore = ""
    occurences = 0


class Record:
    """Records in the system are stored in an XML form. Attached to
    the record is various configurable metadata, such as the time it
    was inserted into the database and by which user. Records are
    stored in a RecordStore database and retrieved via a persistent
    and unique document identifier. The record data may be retrieved
    as a list of SAX events, as regularised XML or as a DOM tree."""
    tagName = ''
    status = ''
    baseUri = ''
    history = []
    rights = []
    recordStore = None
    elementHash = {}
    resultSetItem = None

    wordCount = -1
    byteCount = -1
    metadata = {}

    parent = ('', None, 0)
    processHistory = []

    dom = None
    xml = ""
    sax = []

    def __init__(self, data, xml="", docId=None, wordCount=0, byteCount=0):
        raise(NotImplementedError)
    
    def __repr__(self):
            if self.recordStore is not None:
                return "%s/%s" % (self.recordStore, self.id)            
            else:
                return "%s-%s" % (str(self.__class__).split('.')[-1], self.id)

    def get_dom(self, session):
        """Return the DOM document node for the record."""
        raise(NotImplementedError)
    def get_sax(self, session):
        """Return the list of SAX events for the record, serialised according to the internal C3 format."""
        raise(NotImplementedError)
    def get_xml(self, session):
        """Return the XML for the record as a serialised string."""
        raise(NotImplementedError)

    def process_xpath(self, session, xpath, maps={}):
        """Process the given xpath (either string or compiled), perhaps with some supplied namespace mappings."""
        raise(NotImplementedError)

    def fetch_vector(self, session, index, summary=False):
        raise(NotImplementedError)


class Workflow(C3Object):
    """A workflow is similar to the process chain concept of an index,
    but behaves at a more global level. It will allow the
    configuration of a workflow using Cheshire3 objects and simple
    code to be defined and executed for input objects. For example,
    one might define a common workflow pattern of PreParsers, a Parser
    and then indexing routines in the XML configuration, and then run
    each document in a documentFactory through it.  This allows users
    who are not familiar with Python, but who are familiar with XML
    and the Cheshire3 design to implement tasks as required by
    changing only configuration files. It thus also allows a user to
    configure personal workflows in a Cheshire3 system which they
    don't have permission to modify."""
    code = ""

    def process(self, session, *args, **kw):
        """Executes the code as constructed from the XML configuration
        on the given object. The return value is the last object to be
        produced by the execution.  This function is automatically
        written and compiled when the object is instantiated."""
        raise(NotImplementedError)


class Logger(C3Object):
    def log(self, session, *args, **kw):
        raise(NotImplementedError)
    
