import docx2txt
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import re
# Extracting text from DOCX
def doctotext(m):
    temp = docx2txt.process(m)
    resume_text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = ' '.join(resume_text)
    return (text)
    
#Extracting text from PDF
def pdftotext(m):
    # pdf file object
    # you can find find the pdf file with complete code in below
    pdfFileObj = open(m, 'rb')

    # pdf reader object
    pdfFileReader = PdfFileReader(pdfFileObj)

    # number of pages in pdf
    num_pages = pdfFileReader.numPages

    currentPageNumber = 0
    text = ''

    # Loop in all the pdf pages.
    while(currentPageNumber < num_pages ):

        # Get the specified pdf page object.
        pdfPage = pdfFileReader.getPage(currentPageNumber)
        # Get pdf page text.
        text = text + pdfPage.extractText()

        # Process next page.
        currentPageNumber += 1
    return (text)

#main function
if __name__ == '__main__': 

    FilePath = 'AI.pdf'
    FilePath.lower().endswith(('.png', '.docx'))
    if FilePath.endswith('.docx'):
      textinput = doctotext(FilePath) 
    elif FilePath.endswith('.pdf'):
      textinput = pdftotext('Sample.pdf')
    else:
      print("File not support")
import spacy
import en_core_web_sm
from spacy.matcher import Matcher

# load pre-trained model
nlp = en_core_web_sm.load()

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

#Extract Name
def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', [pattern])
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text
# print('Name: ',extract_name(textinput))

#Extract email
def extract_email(text):
    '''
    Helper function to extract email id from text
    :param text: plain text extracted from resume file
    '''
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

# print('Email: ',extract_email(textinput))

#Extract Phone Number

def extract_mobile_number(text):
    '''
    Helper function to extract mobile number from text
    :param text: plain text extracted from resume file
    :return: string of extracted mobile numbers
    '''
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number

# print('Email: ',extract_mobile_number(textinput))

import re
from nltk.corpus import stopwords

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'M.B.A', 'MBA', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSLC', 'SSC' 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [str(sent).strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index]
                
                

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'((\d{}))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education
# print('Qualification: ',extract_education(textinput))


#Extracting experience
EXPERIENCE = [
            'DEVELOPER',
            'SCIENTIST',
        ]


def extract_roles(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [str(sent).strip() for sent in nlp_text.sents]

    exp = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EXPERIENCE and tex not in STOPWORDS:
                exp[tex] = text + nlp_text[index]
                
                

    # Extract year
    experience = []
    for key in exp.keys():
        year = re.findall(r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)|Apr(?:il)|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\D\d{4}|Present|present)', exp[key])
        if year:
            experience.append((key, ''.join(year[0] + '-' +year[1])))
        else:
            experience.append(key)
    return experience

# print('Experience: ',extract_roles(textinput))


import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')

#Extracting skills

def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
  
    
    # extract values
    skills = ['JavaScript','SQL']
    # print(skills)
    skillset = []
    
    # check for one-grams (example: python)
    for token in tokens:
        if token in skills:
            skillset.append(token)
    return skillset
# print ('Skills',extract_skills(textinput))



#Extract entities


RESUME_SECTIONS = [
                    'accomplishments',
                    'experience',
                    'education',
                    'interests',
                    'projects',
                    'professional experience',
                    'publications',
                    'skills',
                ]


def extract_entity_sections(text):
    # print("Inside function")
    '''
    Helper function to extract all the raw text from sections of resume
    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(RESUME_SECTIONS)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in RESUME_SECTIONS:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)
    
    return entities

# print ('entities',extract_entity_sections(textinput))

import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')
from collections import Counter

def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
  
    
    # extract values
    skills = ['JavaScript','SQL','Python','DataScience','HTML','Data Visualization','Django']
    #print(skills)
    skillset = []
    
    # check for one-grams (example: python)
    for token in tokens:
        if token in skills:
            skillset.append(token)
    return skillset
# print ('Skills',extract_skills(textinput))
# print('Ocuurances',Counter(extract_skills(textinput)))

import pdfplumber
import re
pdf = pdfplumber.open('Sample.pdf')
all_text=''
for pdf_page in pdf.pages:
    single_page_text = pdf_page.extract_text()
    all_text = all_text + '\n' + single_page_text
textList=all_text.split("\n")
sectionLookup =['Experience','Education','Skills','Courses and Certificates']
flag=0
sectionIndex={}
keyOrder=[]
sectionContent={}
for i in textList:
    if i.strip() in sectionLookup:
        flag=1
        sectionIndex[str(i.strip())]=textList.index(i)
        keyOrder.append(i.strip())       
for j in range(len(keyOrder)):
    if j==len(keyOrder)-1:
        # print("----",j)
        content=[]
        for i in range(sectionIndex[keyOrder[j]], len(textList)):
            content.append(textList[i].strip())
        sectionContent[keyOrder[j]]=content
    else:
        # print("----",j)
        content=[]
        for i in range(sectionIndex[keyOrder[j]], sectionIndex[keyOrder[j+1]]):
            content.append(textList[i].strip())
        sectionContent[keyOrder[j]]=content
# print(sectionContent['Experience'])

rolesLookup=['Python Developer','Data Scientist']

experienceSection=sectionContent['Experience']
# print(type(experienceSection))
rolesSectionIndex={}
roleskeyOrder=[]
rolessectionContent={}
rolesSection={}
for i in experienceSection:
    if i.strip() in rolesLookup:
        rolesSectionIndex[str(i.strip())]=experienceSection.index(i)
        roleskeyOrder.append(i.strip())  
for j in range(len(roleskeyOrder)):
    if j==len(roleskeyOrder)-1:
        # print("----",j)
        content=[]
        for i in range(rolesSectionIndex[roleskeyOrder[j]], len(experienceSection)):
            content.append(experienceSection[i].strip())
        rolessectionContent[roleskeyOrder[j]]=content
    else:
        # print("----",j)
        content=[]
        for i in range(rolesSectionIndex[roleskeyOrder[j]], rolesSectionIndex[roleskeyOrder[j+1]]):
            content.append(experienceSection[i].strip())
        rolessectionContent[roleskeyOrder[j]]=content           
# print(rolessectionContent)
experince={}
for role,desc in rolessectionContent.items():
    # print(role,"----",desc)
    exp=re.findall(r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)|Apr(?:il)|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\D\d{4}|Present|present)',str(desc))
    # print(role,"-",exp)
    experince[role]=exp
def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele+","
    
    # return string
    return str1
import pandas as pd

name=extract_name(textinput)
phone=extract_mobile_number(textinput)
email=extract_email(textinput)
qualification=listToString(extract_education(textinput))
skills=listToString(extract_skills(textinput))
sectios=extract_entity_sections(textinput)
frequency=Counter(extract_skills(textinput))
outputjson={
    "name":[name],
    "phone":[phone],
    "email":[email],
    "qualification":[qualification],
    "skills":[skills],
    "frequency":[frequency],
    "experince":[experince]
}

df = pd.DataFrame(outputjson)
print(df)
df.to_csv('out_new.csv',index=False)  
