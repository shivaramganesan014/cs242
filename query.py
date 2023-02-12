
import logging, sys
logging.disable(sys.maxsize)

import json

import lucene
import os
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity
import sys
import os


def sort_by_score(json):
    try:
        return int(json['score'])
    except:
        return 0


def retrieve(storedir, query, k):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    parser = QueryParser('Body', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, k).scoreDocs
    
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "title": doc.get("Title"),
            "url": doc.get("Url")
        })
    # print("Total matches :: ", len(topkdocs))
    # print(topkdocs)
    return topkdocs


query = sys.argv[1]
k = 10
if(len(sys.argv) > 2):
    k = int(sys.argv[2])

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

index_dir = "/home/cs242/project/index_dir/"
file_names = os.listdir(index_dir)
# print(file_names)

total_list = []

for name in file_names:
    topK = retrieve(index_dir+name, query, k)    
    topK.sort(key=sort_by_score, reverse=True)
    total_list += topK[0:3]

total_list.sort(key=sort_by_score, reverse=True)
print("Total matches from collection :: ", len(total_list))
print(total_list)




