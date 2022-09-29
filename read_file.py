## reading the data from whatsapp report
import pandas as pd
import numpy as np
import regex as re
import datetime
import calendar
import matplotlib.pyplot as plt



date =[]
time =[]
name=[]
subject = []


with open("WhatsApp Chat with Former 7 shuttlers.txt", encoding="utf-8") as fp:
    while True:
        line = fp.readline()
        
        if not line:
            print('EOF')
            break
        data = line
        pattern = "(\d{2}/\d{2}/\d{4})"
        temp = re.findall(pattern, data)
        if len(temp)!=0 :
            date.append("".join(temp))

            pattern = "(\d{2}:\d{2})"
            time.append("".join(re.findall(pattern, data)))
            
            pattern = ".*- (\.*\s*.*): "
            name.append("".join(re.findall(pattern, data)))

            pattern = ": (.*)"
            subject.append("".join(re.findall(pattern, data)))

        
        else:
            subject[-1] = subject[-1]+"".join(data)

        


df = pd.DataFrame(list(zip(date,time,name,subject)),columns=['date','time','name','subject'] )

df.to_csv("output.csv")


for pos,data in enumerate(df['date']):
    df.loc[pos,['dayofweek']] = calendar.day_name[datetime.datetime.strptime(data, "%d/%m/%Y").weekday()]


for pos,data in enumerate(df['subject']):
    for c in data:
        df.loc[pos,['memes']] = np.where(ord(c) < 128,0,1)
    df.loc[pos, ['youtube_share']] = np.where('youtube' in data, 1, 0)
    df.loc[pos, ['contact_file_attachment']] = np.where('attached)' in data, 1, 0)
    df.loc[pos, ['images']] = np.where('Media omitted' in data, 1, 0)
   
    


df1 = df[df['name']!='']


print(df1['dayofweek'].value_counts().keys())
print(df1['dayofweek'].value_counts().values)
plt.bar(df1['dayofweek'].value_counts().keys(),df1['dayofweek'].value_counts().values)
plt.xticks(rotation='vertical')
plt.xlabel("Days of week including weekends")
plt.ylabel("No of Messages")
plt.title(" No of Messages sent on each day")
plt.show()

df2 = df1.copy()

post_array = []

for pos,data in enumerate(df1['name']):
    if ":" in data:
        post_array.append(data)
        
        
        
print(post_array)

for i in post_array:
    df1 = df1[df1['name']!=i]

df3 = df1.copy()

print(df3['name'].value_counts())

print(df1['name'].value_counts().keys())
print(df1['name'].value_counts().values)
plt.bar(df1['name'].value_counts().keys(),df1['name'].value_counts().values)
plt.xticks(rotation='vertical')
plt.xlabel("Members")
plt.ylabel("No of Messages")
plt.title(" No of Messages sent by members")
plt.show()


crosstb = pd.crosstab(df1.name, df1.images)
crosstb.plot.bar()
plt.show()


crosstb = pd.crosstab(df1.name, df1.contact_file_attachment)
crosstb.plot.bar()
plt.show()

crosstb = pd.crosstab(df1.name, df1.memes)
crosstb.plot.bar()
plt.show()

crosstb = pd.crosstab(df1.name, df1.youtube_share)
crosstb.plot.bar()
plt.show()

