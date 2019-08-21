import os
import shutil
import xml.dom.minidom

languagesCount = {"nonEnglish": 0}

def newLanguageDir(language):
    os.mkdir("C:/Users/Thiag/Documents/britishDatasetDocuments/" + language)

# Windows only
def copyTxtFile(xmlFileName, language):
    txtFileName = xmlFileName[:-3] + "txt"
    sourceFile = "C:/Users/Thiag/Documents/CORPUS_TXT/" + txtFileName
    targetDir = "C:/Users/Thiag/Documents/britishDatasetDocuments/" + language
    try:
        shutil.copy(sourceFile, targetDir)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())

if __name__ == "__main__":
    newLanguageDir("nonEnglish")

    for fileName in os.listdir("C:/Users/Thiag/Documents/CORPUS_UTF-8"):
        if fileName[-3:] != "xml": continue

        doc = xml.dom.minidom.parse("C:/Users/Thiag/Documents/CORPUS_UTF-8/" + fileName)
        pTags = doc.getElementsByTagName("p")
        for tag in pTags:
            if tag.getAttribute("n") == "first language":
                language = tag.firstChild.nodeValue
                if language not in languagesCount:
                    languagesCount[language] = 0
                    newLanguageDir(language)
                languagesCount[language] += 1
                copyTxtFile(fileName, language)

                if language != "English":
                    languagesCount["nonEnglish"] += 1
                    copyTxtFile(fileName, "nonEnglish")

    for lang in  sorted(languagesCount, key = languagesCount.get, reverse = True):
        print(str(lang) + ": " + str(languagesCount[lang]))
    