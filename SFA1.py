#import libraries
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from tkinter import filedialog
from radiospectra.sources import CallistoSpectrogram
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np 
from scipy.optimize import curve_fit
from sympy import *
from tkinter import messagebox
from pathlib import Path
import os

root = tk.Tk()
root.title('Solar Flare Analizer (II and III)')
canvas = tk.Canvas(root, width=560, height=80)
canvas.grid(columnspan=6, rowspan=6)

#logo
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=42)



#instructions00 = tk.Label(root, text="Collaborate with", fg = "Green", font=("Arial",12) , justify=LEFT)
#instructions00.grid(columnspan=2, column=1, row=44)

instructions01 = tk.Label(root, text="USJ & UOC", fg = "Red", font=("Arial",12) , justify=LEFT)
instructions01.grid(columnspan=1, column=1, row=44)

#instructions
instructions1 = tk.Label(root, text="Select a FITS file or fits.gz file on your computer", font=("Raleway",12) , justify=LEFT)
instructions1.grid(columnspan=3, column=0, row=1)

instructions11 = tk.Label(root, text="Frequency Spectrum -->", font=("Raleway",10), justify=LEFT)
instructions11.grid(columnspan=3, column=0, row=6)

instructions12 = tk.Label(root, text="Intensity colour Rescaled -->", font=("Raleway",10), justify=LEFT)
instructions12.grid(columnspan=3, column=0, row=8)

instructions2 = tk.Label(root, text="Enter the frequency channel number", font=("Raleway",10), justify=LEFT)
instructions2.grid(columnspan=3, column=0, row=11)

instructions3 = tk.Label(root, text="Maximum Intencity frquency plot -->", font=("Raleway",10), justify=LEFT)
instructions3.grid(columnspan=3, column=0, row=17)

instructions4 = tk.Label(root, text="Mhzs^(-1)", font=("Raleway",12), justify=LEFT)
instructions4.grid(column=2, row=35)

instructions5 = tk.Label(root, text="Drift rate", font=("Raleway",12), justify=LEFT)
instructions5.grid(column=0, row=35)

instructions5 = tk.Label(root, text="Model -->", font=("Raleway",12), justify=LEFT)
instructions5.grid(column=0, row=37)

instructions51 = tk.Label(root, text="R^2 -->", font=("Raleway",12), justify=LEFT)
instructions51.grid(column=0, row=39)

instructions6 = tk.Label(root, text="Fine crop", font=("Raleway",12), justify=LEFT)
instructions6.grid(column=1, row=25)

def open_file():
        browse_text.set("loading...")
        global filename
        filename = filedialog.askopenfilename()
        #filename = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[("fits file", "*")])
        entry1.insert(0, filename)
        browse_text.set("Browse")
        return print(filename)

#Open the image of the radio burst        
def im1():
    img1_text.set("Loading...") 
    global image
    image = CallistoSpectrogram.read(filename)
    plot1 = image.plot()
    plt.show()
    #img1 = plt.savefig("image1.JPG",dpi=1200)
    img1_text.set("IMG1") 

#Colour corrected radio burst    
def im2():
    img2_text.set("Loading...") 
    global image
    image = CallistoSpectrogram.read(filename)
    nobg = image.subtract_bg()
    nobg.plot(cmap=cm.jet,vmin=-17) 
    plt.ylabel("Frequency [MHz]")
    plt.xlabel("Time [UT]")
    #plt.axis('off')
    #plt.title("Bleien low frequncy antenna")
    #plt.savefig("image2.JPG",dpi=1200)
    #img2 = plt.savefig("image2.JPG",dpi=1200)
    plt.show()
    img2_text.set("IMG2")    

#Channel number input
inputtxt = tk.StringVar()
def chan():
    global Input1
    global freq_x
    global time_x
    freq_x = len(image.freq_axis)
    time_x = len(image.time_axis)
    Input1 = inputtxt.get()
    n=int(Input1)
    spectrum = image[n,:] # Single Lightcurve at channel 145
    plt.plot(spectrum,linewidth=2.0)
    #print(len(spectrum))
    plt.ylabel('Intensity')
    plt.xlabel('Units of time [Equals 1/4 seconds]')
    plt.title('Lightcurve for each frequency channel')
    plt.axis([0, time_x, 0, freq_x])
    plt.grid(True)
    plt.plot()
    #plt.savefig("image3.JPG",dpi=1200)
    plt.show()
    
def maxin():
    #read channals one by one and find the maximum intensity points or each channel
    freq_x = len(image.freq_axis) 
    l= list()
    for i in range(0,freq_x):
        max1=np.array(max(image[i,:]))
        #print(max1)
        p=np.where(image[i,:] == max1)
        p0=p[0][0]
        l.append(p0)
    global points
    global points1
    global frequencies
    global ffr
    global ffr1
    points = np.array(l)
    points1 = np.flip(points)
    frequencies = image.freq_axis
    ffr = np.array(frequencies)
    ffr1=np.flip(ffr)
    ###################################################################
    #plot the maximum intensity points with the frequency
    plt.scatter(points,ffr,color='blue')
    plt.ylabel("Frequency [MHz]")
    plt.xlabel("Units of time [Equals 1/4 seconds]")
    plt.title("Highest intensity points of the frequencies")
    #plt.savefig("image4.JPG",dpi=1200)
    plt.show()

inputtxt1 = tk.StringVar()
inputtxt2 = tk.StringVar()
inputtxt3 = tk.StringVar()
inputtxt4 = tk.StringVar()
def crop():
    global Input2
    global Input3
    global Input4
    global Input5
    Input2 = inputtxt1.get()
    Input3 = inputtxt2.get()
    Input4 = inputtxt3.get()
    Input5 = inputtxt4.get()
   
    ##crop the the area that contains the solar flare
    t1=int(Input2)
    t2=int(Input3)
    f1=int(Input4)
    f2=int(Input5)
    global ffrq
    global pointsq
    ffr[ffr<f1]=0
    ffr[ffr>f2]=0
    ffrq=ffr.astype('float')
    ffrq[ffrq==0]=np.nan
    points[points<t1]=0
    points[points>t2]=0
    pointsq=points.astype('float')
    pointsq[pointsq==0]=np.nan

    plt.scatter(pointsq,ffrq,color='green',label="Highest inensity points of each channel")
    plt.ylabel("Frequency [MHz]")
    plt.xlabel("Units of time [Equals 1/4 seconds]")
    plt.show()
###########################################################
inputtxt11 = tk.StringVar()
inputtxt21 = tk.StringVar()
inputtxt31= tk.StringVar()
inputtxt41 = tk.StringVar()
def crop1():
    global Input21
    global Input31
    global Input41
    global Input51
    global ffrq
    global pointsq
    Input21 = inputtxt11.get()
    Input31 = inputtxt21.get()
    Input41 = inputtxt31.get()
    Input51 = inputtxt41.get()
   
    ##crop the the area that contains the solar flare
    tt1=int(Input21)
    tt2=int(Input31)
    ff1=int(Input41)
    ff2=int(Input51)
    
    ffrq[np.isnan(ffrq)]=0
    ind = np.where((ffrq>ff1) & (ffrq<ff2))
    points[np.isnan(pointsq)]=0
    ind = ind[0]
    mm = list()
    for i in ind:
        poi = pointsq[i]
        mm.append(poi)
    poi1 = np.array(mm)
    poi1 = poi1[(poi1<tt2) & (poi1>tt1)]
    for i in poi1:
        pointsq[points==i]=0
    pointsq=pointsq.astype('float')
    pointsq[pointsq==0]=np.nan
    ffrq=ffrq.astype('float')
    ffrq[ffrq==0]=np.nan    
    
    
    
    plt.scatter(pointsq,ffrq,color='red',label="Highest inensity points of each channel")
    plt.ylabel("Frequency [MHz]")
    plt.xlabel("Units of time [Equals 1/4 seconds]")
    plt.title("Highest inensity points of each channel")
    #plt.savefig("image15.JPG",dpi=1200)
    plt.show()
    
    


def type2():
        
    if  len(pointsq) > len(ffrq):
        #root.withdrew()
        #messagebox.showerror("Error","Error!! Please crop properly")
        print("yes")
    else: 
        # remember here graph axix are diveded by 1000 and 1000 respectively
        plt.scatter((pointsq),(ffrq),color='green',label="Highest inensity points of each channel")
        plt.ylabel("Frequency [MHz]")
        plt.xlabel("Units of time [Equals 1/4 seconds]")
        #plt.show()
        ##################################################################
        #drop the corresponding np.nan values in a 2D array
        global pointsq12
        global ffrq12
        pointsq12 = pointsq
        ffrq12 = ffrq
        pointsq12 = pointsq12
        ffrq12 = ffrq12
        tr1=np.transpose((pointsq12,ffrq12))
        newlist = tr1[~np.isnan(tr1).any(axis=1),:]
        ##################################################################
        sortedlst=newlist[newlist[:,0].argsort()]
    
        #####################################################################
        #####################################################################
    
        arr1,arr2=np.split(sortedlst,2,axis=1)
        l1= list()
        for i in range(0,len(arr1)):
            p1=arr1[i][0]
            l1.append(p1)
        x1 = np.array(l1) #"x1" is the time
        #x2 = np.linspace(t1,t2,len(x1))
    
        l2=list()
        for i in range(0,len(arr2)):
            p2=arr2[i][0]
            l2.append(p2)
        y1 = np.array(l2) #"y1" is the frequencies
        ####################################################################
        #print(x1)
        dupli = list()
        for i in l1:
            if l1.count(i)>1:
                if i not in dupli:
                    dupli.append(i)
        duplicatelist = np.array(dupli) 
        reindex = list()
        for j in range(0,len(duplicatelist)):
            list2 = [i for i in range(len(l1)) if l1[i]== duplicatelist[j]]
            reindex.append(list2)
        g1 = list()
        g2 = list()
        for i in reindex:
            g2.append(len(i))
            for j in range(0,len(i)):
                y11 = y1[i[j]]
                g1.append(y11)
        #print(g2)   
        d=list()
        d1=1
        for i in g2:
            d1 = d1 + i
            d.append(d1)
        d.insert(0,0)
        #print(d)
        r = list()
        for i in range(0,len(d)-1):
            if i < len(d):
                r.append(g1[d[i]:d[i+1]-1])
        #print(len(r))
        av = list()
        for i in range(0,len(r)):
            av.append(sum(r[i]) / len(r[i]))
        ave=np.array(av)
        #print(av)
        #print(dupli)
        #print(reindex)
        #print(av[1])
        finaly = list()
        for i in range(0,len(reindex)):
            y1[reindex[i]] = av[i]
        y1f = np.array(y1)
        #print(y1f)
        resx1 =list()
        for i in x1:
            if i not in resx1:
                resx1.append(i)
        #print(resx1)
        #*resx1,_ = resx1 
        xx=np.array(resx1)
        xxn = xx
        #print(len(xxn))
        #print(resx1)
        resy1 =list()
        for i in y1f:
            if i not in resy1:
                resy1.append(i)
        yy=np.array(resy1)
        yyn = yy
        #print(len(yyn))
        #print(len(resy1))
        #################################################################
        # the x and y axises are divided by 1000 and 1000 respectively
    
        #plt.scatter(xxn,yyn,color='black',label="average")
        #plt.xlabel("Time (Seconds)")
        #plt.ylabel("Frequency (MHz)")
        #plt.title("Average frequency graph")
        #plt.show()
    
        # if you wanna plot average frequency plot please remove above hashtags
    
        ##################################################################
        def exp1(x,a0,b,a1):#input x in seconds
            return a0 * np.exp((b+x)/x) + a1
        #constant define. This should be in the program
        #fit the data
        #Curve_fit
        ##################################################################
        #p0 are the initial guesses
        popt, pcov = curve_fit(exp1,xxn,yyn,p0=[1,1,1],maxfev=50000)
        perr = np.sqrt(np.diag(pcov))
        ##################################################################
        #Plot the function
        exp1_fuc=exp1(xxn,popt[0],popt[1],popt[2])
        #print(linear_fuc[0])
        plt.plot(xxn,exp1_fuc,label="Model")
        plt.ylabel("Frequency [MHz]")
        plt.xlabel("Units of time [Equals 1/4 seconds]")
        plt.title("The solar rdio burst and modeled line")
        plt.legend()
        #plt.savefig("image16.JPG",dpi=1200)
        plt.show()
    
        #print("The drift rate of the solar radio burst is ", popt[0] , " Mhzs^(-1)")
        ##################################################################
        #create the 1st derivation graph
        aa0=popt[0]
        bb0=popt[1]
        aa1=popt[2]
       
        x = symbols('x')
        mod= aa0 * exp((bb0+x)/x) + aa1
       
        der=mod.diff(x)
        der1 = lambdify(x,der)
        h = list()
        for i in xxn:
            df = der1(i)
            h.append(df)
        h1=np.array(h)
        
        
        plt.scatter(xxn,h1*4,color='black',label="drift rates")
        plt.ylabel("Drift rates (MHz/S)")
        plt.title("Drifte rates of the type II burst")
        plt.xlabel("Units of time [Equals 1/4 seconds]")
        ##############################################################
       
        plt.plot(xxn,h1*4,color='yellow')
        plt.ylabel("Drift rate [MHz/S]")
        plt.xlabel("Units of time [Equals 1/4 seconds]")
        plt.title("Drift rates")
        plt.legend()
        #plt.savefig("image17.JPG",dpi=1200)
        plt.show()
    
        av1=sum(h1)/len(h1)
        entry7.insert(0, av1*4)
        entry8.insert(0,mod)
        print("The drift rate of the type II solar radio burst is", av1," MHzs^(-1)")
        
        ffrqq1= yyn
        ffrqq1[np.isnan(ffrqq1)]=0
        ffrqq1 = ffrqq1[ffrqq1 != 0]
        ffrqq1 = ffrqq1[:len(exp1_fuc)]
        
        co_m = np.corrcoef(ffrqq1,exp1_fuc)
        coor = co_m[0,1]
        cof = coor**2
        entry10.insert(0,str(cof))
        


def type3():
    #drop the corresponding np.nan values in a 2D array
    tr=np.transpose((pointsq,ffrq))
    newlist = tr[~np.isnan(tr).any(axis=1),:]
    arr1,arr2=np.split(newlist,2,axis=1)
    l1= list()
    for i in range(0,len(arr1)):
        p1=arr1[i][0]
        l1.append(p1)
    x1 = np.array(l1) #"x1" is the time
    l2=list()
    for i in range(0,len(arr2)):
        p2=arr2[i][0]
        l2.append(p2)
    y1 = np.array(l2) #"y1" is the frequencies
    ##################################################################

    def lin(x,b,a0):#input x in seconds
        return b*x+a0
    #constant define. This should be in the program
    #fit the data
    #Curve_fit
    ##################################################################
    popt, pcov = curve_fit(lin,x1,y1)
    perr = np.sqrt(np.diag(pcov))
    ##################################################################
    #Plot the function
    linear_fuc=lin(x1,popt[0],popt[1])
    #print(linear_fuc[0])
    plt.scatter(pointsq,ffrq,color='green',label="Highest inensity points of each channel")
    plt.ylabel("Frequency [MHz]")
    plt.xlabel("Units of time [Equals 1/4 seconds]")
    #plt.show()
    plt.plot(x1,linear_fuc,label="Model")
    plt.ylabel("Frequency [MHz]")
    plt.xlabel("Units of time [Equals 1/4 seconds]")
    plt.title("The solar rdio burst and modeled line")
    plt.legend()
    #plt.savefig("image6.JPG",dpi=1200)
    plt.show()
    
    y8=StringVar(print("The drift rate of the solar radio burst is ", popt[0] , " Mhzs^(-1)"))
    entry7.insert(0, popt[0]*4)
    entry8.insert(0,(popt[0]*4,"*x +",popt[1]))
    
    ffrqq= ffrq
    ffrqq[np.isnan(ffrqq)]=0
    ffrqq = ffrqq[ffrqq != 0]
    ffrqq = ffrqq[:len(linear_fuc)]
    
    co_m = np.corrcoef(ffrqq,linear_fuc)
    coor = co_m[0,1]
    cof = coor**2
    entry10.insert(0,str(cof))
    

def save():
    ffrq[np.isnan(ffrq)]=0
    n_ffrq = np.where(ffrq==0)
    n_ffrq = n_ffrq[0]
    pointsq[np.isnan(pointsq)]=0
    n_poi = np.where(pointsq==0)
    n_poi = n_poi[0]
    bmty = np.concatenate((n_poi,n_ffrq))
    com = np.transpose((pointsq,ffrq)).tolist()
    bmty = np.unique(np.array(bmty)).tolist()
    for i in sorted(bmty,reverse = True):
        del com[i]
    com1 = np.array(com)
    wtf1, wtf2 = zip(*com1)
    fg = Path(filename)
    fg1 = os.path.basename(fg)
    fgp1 = os.path.dirname(fg)
    namefg1 = "%s.txt" % fg1
    join = os.path.join(fgp1,namefg1)
    
    sav = open(join,"w")
    sav.write("Solar Burst : " + str(fg1))
    sav.write("\nTime(1/4 Seconds) vs Frequency(MHz) : " "\n" + str(com1))
    sav.write("\nTime(1/4 Seconds): " "\n" + str(wtf1))
    sav.write("\nFrequency(MHz): " "\n" + str(wtf2))
    sav.close()

def clear1():
    entry1.delete('0',tk.END)
    entry2.delete('0',tk.END)
    entry3.delete('0',tk.END)
    entry4.delete('0',tk.END)
    entry5.delete('0',tk.END)
    entry6.delete('0',tk.END)
    entry7.delete('0',tk.END)
    entry8.delete('0',tk.END)
    entry10.delete('0',tk.END)
    entry31.delete('0',tk.END)
    entry41.delete('0',tk.END)
    entry51.delete('0',tk.END)
    entry61.delete('0',tk.END)

#entry1
entry1= Entry(root, width =55)
entry1.grid(column=1, row=2)

#entry2 channel number
entry2= Entry(root,textvariable=inputtxt,font="Raleway", width =7)
entry2.grid(column=1, row=13)

#crop
entry3= Entry(root,textvariable=inputtxt1,font="Raleway", width =7)
entry3.grid(column=1, row=21)
lbl1=Label(root, text="Time Start")
lbl1.grid(column=0, row=21)

entry4= Entry(root,textvariable=inputtxt2,font="Raleway", width =7)
entry4.grid(column=1, row=22)
lbl2=Label(root, text="Time End")
lbl2.grid(column=0, row=22)

entry5= Entry(root,textvariable=inputtxt3,font="Raleway", width =7)
entry5.grid(column=1, row=23)
lbl3=Label(root, text="Frequency Start")
lbl3.grid(column=0, row=23)

entry6= Entry(root,textvariable=inputtxt4,font="Raleway", width =7)
entry6.grid(column=1, row=24)
lbl4=Label(root, text="Frequency End")
lbl4.grid(column=0, row=24)

#crop1
entry31= Entry(root,textvariable=inputtxt11,font="Raleway", width =7)
entry31.grid(column=1, row=26)
lbl11=Label(root, text="Time Start")
lbl11.grid(column=0, row=26)

entry41= Entry(root,textvariable=inputtxt21,font="Raleway", width =7)
entry41.grid(column=1, row=28)
lbl21=Label(root, text="Time End")
lbl21.grid(column=0, row=28)

entry51= Entry(root,textvariable=inputtxt31,font="Raleway", width =7)
entry51.grid(column=1, row=30)
lbl31=Label(root, text="Frequency Start")
lbl31.grid(column=0, row=30)

entry61= Entry(root,textvariable=inputtxt41,font="Raleway", width =7)
entry61.grid(column=1, row=32)
lbl41=Label(root, text="Frequency End")
lbl41.grid(column=0, row=32)


#entry results
entry7=Entry(root,font="Raleway", width =35)
entry7.grid(column=1, row=35)

#entry results1
entry8=Entry(root,font="Raleway", width =35)
entry8.grid(column=1, row=37)

#entry r2 score
entry10=Entry(root,font="Raleway", width =15)
entry10.grid(column=1, row=39)


#browse button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda:open_file(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
browse_text.set("Browse")
browse_btn.grid(column=2, row=2)

#imgg1 button
img1_text = tk.StringVar()
img1_btn = tk.Button(root, textvariable=img1_text, command=lambda:im1(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
img1_text.set("IMG1")
img1_btn.grid(column=2, row=6)

#imgg2 button
img2_text = tk.StringVar()
img2_btn = tk.Button(root, textvariable=img2_text, command=lambda:im2(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
img2_text.set("IMG2")
img2_btn.grid(column=2, row=8)

#imge3 button
img3_text = tk.StringVar()
img3_btn = tk.Button(root, textvariable=img3_text, command=lambda:chan(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
img3_text.set("Submit")
img3_btn.grid(column=2, row=13)

#imge4 button
img4_text = tk.StringVar()
img4_btn = tk.Button(root, textvariable=img4_text, command=lambda:maxin(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
img4_text.set("IMG3")
img4_btn.grid(column=2, row=17)

#Crop button
img5_text = tk.StringVar()
img5_btn = tk.Button(root, textvariable=img5_text, command=lambda:crop(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
img5_text.set("Crop")
img5_btn.grid(column=2, row=22)

#Crop1 button
img51_text = tk.StringVar()
img51_btn = tk.Button(root, textvariable=img51_text, command=lambda:crop1(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
img51_text.set("F.Crop")
img51_btn.grid(column=2, row=23)

#TypeIII button
img6_text = tk.StringVar()
img6_btn = tk.Button(root, textvariable=img6_text, command=lambda:type3(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
img6_text.set("Type III")
img6_btn.grid(column=2, row=25)

#Save button
savb = tk.StringVar()
savbb = tk.Button(root, textvariable=savb, command=lambda:save(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
savb.set("Save")
savbb.grid(column=2, row=30)

#TypeII button
img7_text = tk.StringVar()
img7_btn = tk.Button(root, textvariable=img7_text, command=lambda:type2(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
img7_text.set("Type II")
img7_btn.grid(column=2, row=24)


#Clear button
img56_text = tk.StringVar()
img56_btn = tk.Button(root, textvariable=img56_text, command=lambda:clear1(), font="Raleway", bg="#20bebe", fg="white", height=1, width=7)
img56_text.set("Clear All")
img56_btn.grid(column=2, row=32)



canvas = tk.Canvas(root, width=600, height=350)
canvas.grid(columnspan=3)

root.mainloop()
