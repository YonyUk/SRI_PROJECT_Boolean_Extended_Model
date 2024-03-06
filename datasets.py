import json
import PyPDF2 as pdf
from os import listdir,getcwd,system
from math import log10
from utils import splitBy

"""
This module contains diferent retrieval information models for documents
"""

# globals variables definitions
global CONFIG

CONFIG = {}

class DataSet:
    """
    This class defines a dataset of documents
    """
    _files = None

    def __init__(self,path=None):
        if not path == None:
            self._files = listdir(path)
            pass
        else:
            self._files = listdir(getcwd())
            pass
        
        temp = []
        for i in range(len(self._files)):
            if CONFIG['files_to_omit'].count(self._files[i]) == 0:
                temp.append(self._files[i])
                pass
            pass
        
        self._files = temp
        pass
    
    pass

class TfIdfDataSet(DataSet):
    
    """
    This clas defines a dataset which's documents are tokenized and stored in a matrix M, the components are the
    tf-idf normalized values for each token of a document, the tokens are the words contained in that document
    """
    
    _docs_tf = {}
    _idfs = {}
    _documents = []
    _max_idf = 0
    
    def __init__(self,path=None):
        super().__init__(path)
        for file in self._files:
            
            if CONFIG['files_to_omit'].count(file) > 0:
                continue
            try:
                self._documents.append(self._tokenize(file))
                pass
            except Exception:
                print(f'No se pudo leer el fichero {file}')
                pass
            pass
        self._index_documents()
        system('clear')
        pass
    
    def _tokenize(self,document):
        """
        split the document's content and returns a list with the words inside
        """
        print(f'loading document {document}')
        i = document.split('.')
        extension = i[len(i) - 1]
        content = []        
        if extension == 'pdf':
            pdfFileObj = open(document,'rb')
            pdfReader = pdf.PdfFileReader(pdfFileObj)
            for i in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(i)
                text = pageObj.extractText().lower()
                content = content.__add__(splitBy(text,CONFIG['characters_to_omit']))
                pass
            pass
        else:
            reader = open(document,'r')
            content = splitBy(reader.read().lower(),CONFIG['characters_to_omit'])
            reader.close()
            pass
        print(f'document {document} loaded')
        return content

    def _index_documents(self):
        """
        computes the tf-idf values of all documents
        """
        
        document_number = 0
        for document in self._documents:
            system('clear')
            print(f'\rprocessing file {self._files[document_number]}')
            max_tf = 0
            doc = {}
            
            for word in document:
                # si es la primera vez que vemos la palabra dentro del documento
                if list(doc.keys()).count(word) == 0:
                    # la marcamos como vista una vez
                    doc[word] = document.count(word)
                    # si tambien es la primera vez que la vemos en todo el dataset
                    if list(self._idfs.keys()).count(word) == 0:
                        # la marcamos como vista por primera vez en el dataset
                        self._idfs[word] = 1
                        pass
                    pass
                
                if doc[word] > max_tf:
                    max_tf = doc[word]
                    pass
                
                pass
            
            self._docs_tf[document_number] = doc,max_tf
            document_number += 1
            
            pass
        
        # ahora computamos el idf de cada termino
        for word in self._idfs.keys():
            self._idfs[word] = log10(len(self._documents)/self._idfs[word])
            if self._idfs[word] > self._max_idf:
                self._max_idf = self._idfs[word]
                pass
            pass
                
        pass
    
    def _getTf_Idf(self,word,document):
        """
        returns the tf-idf value normalized for the given value in this dataset in the given document
        document is a number
        """
        
        if list(self._idfs.keys()).count(word) == 0: return 0
        
        doc_info = self._docs_tf[document]
        
        if list(doc_info[0].keys()).count(word) == 0: return 0
        
        tf_normalized = doc_info[0][word]/doc_info[1]
        idf_normalized = self._idfs[word]/self._max_idf
        
        return tf_normalized*idf_normalized
    
    def GetWeight(self,word,document):
        id_document = self._files.index(document)
        return self._getTf_Idf(word,id_document)
    
    def GetWeightVector(self,word):
        vector = []
        for document in self._files:
            vector.append(self.GetWeight(word,document))
            pass
        
        return vector
    
    pass

# load the configuration file
with open('config.json','r') as f:
    config = json.load(f)
    for key in config.keys():
        CONFIG[key] = config[key]
        pass
    pass
