
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


def create_index(data, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    for key, value in data.items():
        if(key == "reddit"):
            titleType = FieldType() #title/ question
            titleType.setStored(True)
            titleType.setTokenized(True)
            titleType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

            scoreType = FieldType()
            scoreType.setStored(True)
            scoreType.setTokenized(False)

            urlType = FieldType()
            urlType.setStored(True)
            urlType.setTokenized(False)

            bodyType = FieldType()
            bodyType.setStored(True)
            bodyType.setTokenized(True)
            bodyType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

            commentType = FieldType()
            commentType.setStored(True)
            commentType.setTokenized(True)
            commentType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

            for d in value:
                title = d["title"]
                score = d["score"]
                url = d["url"]
                body = d['body']
                all_comments = ";".join(d["comments"])
                doc = Document()
                doc.add(Field('Title', str(title), titleType))
                doc.add(Field('Score', str(score), scoreType))
                doc.add(Field('Url', str(url), urlType))
                doc.add(Field('Body', str(body), bodyType))
                doc.add(Field('Comments', str(all_comments), commentType))

                writer.addDocument(doc)
        elif(key == "wikihow"):
            titleType = FieldType() #title/ question
            titleType.setStored(True)
            titleType.setTokenized(True)
            titleType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

            urlType = FieldType()
            urlType.setStored(True)
            urlType.setTokenized(False)

            bodyType = FieldType()
            bodyType.setStored(True)
            bodyType.setTokenized(True)
            bodyType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
            for d in value:
                title = d["title"]
                url = d["url"]
                body = d["intro_text"]

                doc = Document()
                doc.add(Field('Title', str(title), titleType))
                doc.add(Field('Url', str(url), urlType))
                doc.add(Field('Body', str(body), bodyType))

                writer.addDocument(doc)
        elif(key == "stackoverflow"):
            titleType = FieldType() #title/ question
            titleType.setStored(True)
            titleType.setTokenized(True)
            titleType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

            urlType = FieldType()
            urlType.setStored(True)
            urlType.setTokenized(False)

            bodyType = FieldType()
            bodyType.setStored(True)
            bodyType.setTokenized(True)
            bodyType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

            answerType = FieldType()
            answerType.setStored(True)
            answerType.setTokenized(True)
            answerType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)


            for d in value:
                question = d["question"]

                title = question["title"]
                score = question["vote"]
                url = question["link"]
                body = question['description']
                question_comments = ";".join(question["comments"])
                answers = d["answer"]
                ans_body = ""
                max_score = 0
                for ans in answers:
                    if ans["answer_type"] == "accepted":
                        ans_body = ans["description"] + ";".join(ans["comments"])
                        break
                    else:
                        score = int(ans["vote"])
                        if score > max_score:
                            max_score = score
                            ans_body = ans["description"] + ";".join(ans["comments"])
                        

                doc = Document()
                if ans_body:
                    doc.add(Field("Answer", str(ans_body), answerType))
                doc.add(Field('Title', str(title), titleType))
                doc.add(Field('Score', str(score), scoreType))
                doc.add(Field('Url', str(url), urlType))
                doc.add(Field('Body', str(body), bodyType))
                writer.addDocument(doc)
        else:
            titleType = FieldType() #title/ question
            titleType.setStored(True)
            titleType.setTokenized(True)
            titleType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

            urlType = FieldType()
            urlType.setStored(True)
            urlType.setTokenized(False)

            bodyType = FieldType()
            bodyType.setStored(True)
            bodyType.setTokenized(True)
            bodyType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

            for d in value:

                for inner_value in d.values():
                    title = inner_value["Title"]
                    url = "https://en.wikipedia.org/wiki/"+title
                    body = inner_value["Content"]
                    doc = Document()
                    doc.add(Field('Title', str(title), titleType))
                    doc.add(Field('Url', str(url), urlType))
                    doc.add(Field('Body', str(body), bodyType))
                    writer.addDocument(doc)

    writer.close()


lucene.initVM(vmargs=['-Djava.awt.headless=true'])

file_dir = "/home/cs242/ir_combined_data/"
index_dir = "/home/cs242/project/ir_indexing/"
file_names = os.listdir(file_dir)
data = []
# for name in file_names:
file_name = "/home/cs242/test_dir/shiva.jsonl"
with open(file_name) as f:
    try:
    	data = json.load(f)
    except Exception as e:
        try:
            data = json.loads(f)
        except:
            print("Exception in Exception")
        print(e)
        print("___________________")
    create_index(data, index_dir)
