# print("Hello New World!")
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
for role,desc in rolessectionContent.items():
    # print(role,"----",desc)
    exp=re.findall(r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)|Apr(?:il)|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\D\d{4}|Present|present)',str(desc))
    print(role,"-",exp)







