import requests
from bs4 import BeautifulSoup
import re
import pickle
import sys
import os

BASE_URL = "https://indiankanoon.org"
PAGES = BASE_URL + "/search/?formInput=murder%20%20doctypes%3A%20highcourts&pagenum="	# 0 based
# DATABASE = []
DATASET_PATH = "dataset"
COUNT = 0

documents = []



def getDocsLinks(api):
	global documents
	try:
		resp = requests.get(api)
		print("Got page")
		data = resp.content
		soup = BeautifulSoup(data, 'html5lib')
		middleElement = soup.find('div', attrs={'class':'results_middle'})
		results = middleElement.findAll('a', attrs={'class':'cite_tag', 'href':re.compile(r'/doc')})
		for i in results:
			documents.append(i["href"])
	except requests.exceptions.SSLError:
		print("Skipping page due to SSL Error")


def addToDataset(document):
	global COUNT
	# print(DATASET_PATH, str(document['doc_id']))
	docId = document["doc_id"].split("/")[2]
	filePath = os.path.join(DATASET_PATH, docId)
	# print(filePath)
	os.makedirs(filePath)
	with open(os.path.join(filePath, docId+"_paragraphs.txt"), "w") as f:
		data = "::::".join(document["paragraphs"])
		f.write(data)
	with open(os.path.join(filePath, docId+"_blockquotes.txt"), "w") as f:
		data = "::::".join(document["blockquotes"])
		f.write(data)
	with open(os.path.join(filePath, docId+"_meta.txt"), "w") as f:
		# print(type(document["source"])
		data = document["title"].decode_contents()+"\n"+document["source"].decode_contents()
		f.write(data)
	COUNT += 1




def getDocument(docId):
	api = BASE_URL+docId
	try:
		resp = requests.get(api)
		print("Got doc")
		data = resp.content
		soup = BeautifulSoup(data, 'html5lib')
		# print(soup.prettify())
		judgments = soup.find('div', attrs={'class':'judgments'})
		document = {}
		# print(judgments)
		document['doc_id'] = docId
		document['title'] = judgments.find('div', attrs={"class":"doc_title"})
		document['source'] = judgments.find('div', attrs={"class":"docsource_main"})
		paragraphs = judgments.findAll('p', attrs={"id":re.compile(r'p')})
		blockquotes = judgments.findAll('blockquote')
		document['paragraphs'] = []
		document['blockquotes'] = []
		# print(paragraphs[0].decode_contents())
		for i in paragraphs:
			document['paragraphs'].append(i.decode_contents())
		for i in blockquotes:
			document['blockquotes'].append(i.decode_contents())
		addToDataset(document)
		# DATABASE.append(d)
	except requests.exceptions.SSLError:
		print("skipping", docId)


def getAllDocuments():
	global documents
	for i in documents:
		try:
			getDocument(i)
		except Exception as e:
			print("ERROR:", e)


def getPages(n):
	for i in range(n):
		getDocsLinks(PAGES+str(i))
	getAllDocuments()



if __name__=="__main__":
	try:
		os.mkdir("dataset")
	except FileExistsError:
		pass
	getPages(3)
	print("Fetched", COUNT, "documents")
	# sys.setrecursionlimit(10000)
	# with open("docs.pkl", "wb") as f:
	# 	pickle.dump(DATABASE, f)
