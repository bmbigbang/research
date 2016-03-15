import csv,numpy
pixel=[17,41];pixel2=[10,10];fname='as0000'
fin1=[];temp1=[];arr1=[];arr2=[];arr3=[];temp2=[];temp3=[];fin2=[];fin3=[]
arr4=[];arr5=[];arr6=[]
for i in range(241):
    if len(str(i))==2:
        l='0'+str(i)
    if len(str(i))==1:
        l='00'+str(i)
    if len(str(i))>=3:
        l=str(i)
    l1=fname+'_I'+l+'.txt'
    l2=fname+'_X'+l+'.txt'
    l3=fname+'_Y'+l+'.txt'
    f1 = open(l1, 'rb')
    f2 = open(l2, 'rb')
    f3 = open(l3, 'rb')
    spamreader1 = csv.reader(f1, delimiter='\t', quotechar='|')
    spamreader2 = csv.reader(f2, delimiter='\t', quotechar='|')
    spamreader3 = csv.reader(f3, delimiter='\t', quotechar='|')
    for row in spamreader1:
        tempo=[]
        for entry in row:
            tempo.append(entry)
        temp1.append(tempo)
    fin1.append(temp1)
    for row in spamreader2:
        tempo=[]
        for entry in row:
            tempo.append(entry)
        temp2.append(tempo)
    fin2.append(temp2)
    for row in spamreader3:
        tempo=[]
        for entry in row:
            tempo.append(entry)
        temp3.append(tempo)
    fin3.append(temp3)
    temp1=[];temp2=[];temp3=[]
f1.close();f2.close();f3.close()
for j in fin1:
    arr1.append(j[pixel[0]][pixel[1]])
for j in fin2:
    arr2.append(j[pixel[0]][pixel[1]])
for j in fin3:
    arr3.append(j[pixel[0]][pixel[1]])
for j in fin1:
    arr4.append(j[pixel2[0]][pixel2[1]])
for j in fin2:
    arr5.append(j[pixel2[0]][pixel2[1]])
for j in fin3:
    arr6.append(j[pixel2[0]][pixel2[1]])
fl = open('correlation.csv', 'w')
csv.register_dialect('unixpwd', delimiter=',',lineterminator='\r')
writer = csv.writer(fl,dialect='unixpwd')
arra=[];FF1=[];FF2=[]
for i in range(len(arr1)):
    X=float(arr2[i]);Y=float(arr3[i]);I=float(arr1[i])
    X2=float(arr5[i]);Y2=float(arr6[i]);I2=float(arr4[i])
    R=(X**2+Y**2)**0.5
    R2=(X2**2+Y2**2)**0.5
    if I==0:
        F='inf'
    else:
        F=R/I
    if I2==0:
        F2='inf'
    else:
        F2=R/I
    arra.append([I,I2,R,R2])
    FF1.append(F);FF2.append(F2)
SS=numpy.convolve(FF1,FF2,"same")
for i in range(len(arr1)):
    if i==0:
        writer.writerow(['I1', 'I2', 'R1','R2', 'Correlation'])
    arra[i].append(SS[i])
    writer.writerow(arra[i])
fl.close()
