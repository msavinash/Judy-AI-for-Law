from sklearn.feature_extraction.text import TfidfVectorizer
import os


THRESHOLD = 0.5
LAW_WORDS = "LawWords.txt"

docs = []
INP_PATH = "dataset2"
for i in os.listdir(INP_PATH):
    print(i)
    tmpdocs = os.listdir(os.path.join(INP_PATH, i))
    # print(tmpdocs)
    for j in tmpdocs:
        if "para" in j:
            with open(os.path.join(INP_PATH, i, j)) as f:
                tmptxt = f.read()
            docs.append(tmptxt)

vectorizer = TfidfVectorizer()
vectorizer.fit(docs)

with open(LAW_WORDS) as f:
    lawWords = f.readlines()

caseFiles = None
with open("caseDetails.txt") as f:
    casefacts = f.readlines()
l = []
for casefact in casefacts:
    casefact = casefact.strip("\n")
    print(i)
    tmpCaseFact = []
    for word in casefact.split(" "):
        x = vectorizer.transform([word])
        value = x.sum()
        if word in lawWords or value > THRESHOLD:
            tmpCaseFact.append(word)
    l.append(" ".join(tmpCaseFact))
# l.sort(reverse=True)
l = list(map(lambda x:x+"\n", l))
with open("summarizedCaseDetails.txt", "w") as f:
    f.writelines(l)
