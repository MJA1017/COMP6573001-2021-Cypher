import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

fo = open("grade.txt","r")
l1 = fo.readlines()
print(l1)

for idx,val in enumerate(l1):
    l1[idx]=val[:-1]
for idx,val in enumerate(l1):
    l1[idx]=val.split(" ")

print(l1)

server = smtplib.SMTP('smtp.gmail.com',port=587)
server.starttls()
server.login("ccpervasive@gmail.com","cypherpervasive")

for i in l1:
    fromaddr = "ccpervasive@gmail.com"             #enter your email address
    toaddr = i[1]

    msg=MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Passing Letter"

    body="Hello {0} ,\nof class {1} , roll no.{2}\nYour grade is {3}".format(i[0],i[3],i[2],i[-1])
    msg.attach(MIMEText(body,'plain'))

    text=msg.as_string()
    server.sendmail(fromaddr,toaddr,text)

server.quit()