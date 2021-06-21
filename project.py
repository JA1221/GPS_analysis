import tkinter as tk
import os
import math
from tkinter.constants import COMMAND, LAST
from typing import Text
from PIL import ImageTk, Image
from tkinter import messagebox
import windnd
from tkinter import filedialog
from functools import partial
import joblib
x = 800
y = 475

fileNames = list()
# GPSData = list()
colorDic = dict()
totalSatPos = list()
root = tk.Tk()
canvas = tk.Canvas(root, bg='#FFFFFF')
menu = tk.Menu(root)
allSatData = dict()
totalSatAvgData = list()
circle = list()
menu1 = tk.Menu(menu)
countList = list()
TInfo = list()
info = list()
houseImg = ImageTk.PhotoImage(Image.open('house.png'))
houseList = list()
showHouse = tk.BooleanVar()
showHouse.set(True)
Gfilepath = ''

def colorDictInit():
    for i in range(0, 21):
        colorDic[i] = [255, i*12, 0]
    for i in range(21, 41):
        colorDic[i] = [255-(i-21)*12, 255, 0]
    for i in range(41, 61):
        colorDic[i] = [0, 255, (i-41)*12]
    for i in range(61, 81):
        colorDic[i] = [0, 255-(i-61)*12, 255]
    for i in range(81, 101):
        colorDic[i] = [(i-81)*12, 0, 255]


def tkwin():
    rootInit()
    menuInit()
    # set canvas bacnground
    imgpath = 'sky.png'
    img = Image.open(imgpath)
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(x, y, image=photo)
    canvas.pack(expand=tk.YES, fill=tk.BOTH)
    initCanvas()
    drawColorChart()

    root.mainloop()


def rootInit():
    root.geometry('1600x950')
    root.title('Final Projecct')
    root.resizable(False, False)
    root.config(menu=menu)
    windnd.hook_dropfiles(root, func=draggedFile)


def menuInit():
    menu.add_cascade(label="選擇GPS DATA", command=selectFile, font=('Consolus'))
    menu.add_cascade(label='Satellite History', menu=menu1)
    menu.add_cascade(label="顯示/隱藏建築物", command=changeHouseVisible, font=('Consolus'))


def initCanvas():
    canvas.bind("<Button-1>", click)
    canvas.config(highlightthickness=0)
    # 800 450+25
    for i in range(16):  # draw line
        length = 450
        angle = i*22.5
        sin, cos = cal(angle)
        canvas.create_line(x, y, x+450*sin, y+450*cos, width=1, fill='#8E8E8E')
    canvas.create_oval(798, 473, 802, 477, fill='#000000')
    for i in range(0, 10):  # num of circle
        r = i*50
        canvas.create_oval(x-r, y-r,
                           x+r, y+r, width=2, outline='#8E8E8E')

    # NSWE
    canvas.create_text(x, y-450, text='N',
                       font=('Time New Roman', 30), fill='#FFE153')
    canvas.create_text(x, y+450, text='S',
                       font=('Time New Roman', 30), fill='#FFE153')
    canvas.create_text(x-450, y, text='W',
                       font=('Time New Roman', 30), fill='#FFE153')
    canvas.create_text(x+450, y, text='E',
                       font=('Time New Roman', 30), fill='#FFE153')
    for i in range(1,9):
        canvas.create_text(x, y-i*50, text = str(90-i*10)+'°',
                       font=('Time New Roman', 20), fill='#FFA042')


def draw(canvas, data):
    sin, cos = cal(data[2])
    length = (90-int(data[1])) * 5
    snr = 99-int(data[3])
    color = ''
    for i in range(0, 3):
        color += format(colorDic[snr][i], 'x').zfill(2)
    # print(color)

    color = '#' + color
    centralX = x+length*sin
    centralY = y+length*cos
    c = canvas.create_oval(centralX-15, centralY-15,
                           centralX+15, centralY+15, fill=color, outline=color)
    t = canvas.create_text(centralX, centralY,
                           text=data[0], fill='#FFFFFF', font=('Consolas', 20))
    totalSatPos.append([data[0], centralX, centralY])

    circle.append(c)
    circle.append(t)

    
def drawHouse(canvas, data):
    sin, cos = cal(data[2])
    length = (90-int(data[1])) * 5

    if isCovered(data)[0] and showHouse.get():
        centralX = x+length/2*sin
        centralY = y+length/2*cos
        h = canvas.create_image(centralX, centralY, image=houseImg)
        houseList.append(h)

def changeHouseVisible():
    showHouse.set(not showHouse.get())
    if(Gfilepath != ''):
        run(Gfilepath)

def dis(x1, y1, x2, y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


def cal(angle):
    angle = int(angle)
    pi = math.pi
    r = math.radians(angle)

    sin = math.sin(r)
    cos = math.cos(r)
    return sin, cos


def click(a):
    for i in totalSatPos:
        if dis(i[1], i[2], a.x, a.y) < 15:
            ss = ''
            ss += 'Satellite Num: '
            ss += i[0]
            for j in totalSatAvgData:
                if i[0] == j[0]:
                    print(j)
                    print(isCovered(j)[1])
                    # print(countList[int(j[0])])
                    nosig = int(countList[int(j[0])][1]) - int(countList[int(j[0])][2])
                    ss = ss+ '\nData amount: ' + countList[int(j[0])][1] + \
                        '\nNo signal count: ' + str(nosig) + \
                        '\nAvreage Elevation: ' + \
                        str(j[1]) + '\nAvreage Azimuth: ' + \
                        str(j[2]) + '°\nAvreage SNR: ' + str(j[3]) +\
                        '\n' + isCovered(j)[1]
            tk.messagebox.showinfo(title='Satellite Details', message=ss)
            # show the satelite all data
    else:
        # remove the data window
        pass
    # clean()


def drawColorChart():
    r = 200
    x1 = 1500
    x2 = 1550
    canvas.create_text((x1+x2)/2, r-15, text="SNR",
                       font=('Consolas', 16), fill='#FFFFFF')
    canvas.create_text(x2+20, r+5, text="99",
                       font=('Consolas', 14), fill='#FFFFFF')
    canvas.create_text(x2+20, r+5*51, text="50",
                       font=('Consolas', 14), fill='#FFFFFF')
    canvas.create_text(x2+20, r+5*100, text="0",
                       font=('Consolas', 14), fill='#FFFFFF')
    for i in range(0, 100):
        color = ''
        for j in range(0, 3):
            color += format(colorDic[i][j], 'x').zfill(2)
        # print(color)
        color = '#' + color
        canvas.create_rectangle(x1, r, x2, r+5, fill=color, outline=color)
        r += 5

def drawInfo(canvas, date, time, location):
    x = canvas.create_text(118, 30, text=date,justify=tk.RIGHT,
                       font=('Consolas', 20), fill='#FFFFFF')
    y = canvas.create_text(110, 60, text=time,justify=tk.RIGHT,
                       font=('Consolas', 20), fill='#FFFFFF')
    z = canvas.create_text(200, 90, text=location,justify=tk.RIGHT,
                       font=('Consolas', 20), fill='#FFFFFF')

    info.append(x)
    info.append(y)
    info.append(z)


def draggedFile(files):
    filepath = files[0].decode('big5')
    global Gfilepath
    Gfilepath = filepath
    run(filepath)


def selectFile():
    try:
        filepath = filedialog.askopenfilename(
            initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        global Gfilepath
        Gfilepath = filepath
        run(filepath)
    except:
        return


def clean():
    fileNames.clear()
    totalSatPos.clear()
    totalSatAvgData.clear()
    for i in circle:
        canvas.delete(i)
    circle.clear()
    
    for i in info:
        canvas.delete(i)
    info.clear()
    for i in houseList:
        canvas.delete(i)
    houseList.clear()

def run(filepath):
    clean()
    f = open(filepath, 'r')
    try:
        data = f.read().split('\n')
        f.close()
    except:
        errorMsg()
        return

    try:
        GSVdata = process_NMEA(data)
        GSVdata = merge_NMEA(GSVdata)[0]
    except:
        errorMsg()
        return

    # for 邵同學
    f2 = open(filepath, 'r')
    data2 = f2.read().split('\n')
    f2.close()
    GPRMC = getGPRMC(data2)
    TInfo.append([getTime(GPRMC[0]),getDate(GPRMC[0]),getTime(GPRMC[-1]),getDate(GPRMC[-1])])
    time = getTime(GPRMC[0])
    date = getDate(GPRMC[0])
    location = getLocation(GPRMC[0])
    # print(GPRMC)
    # print(time)
    # print(date)
    # print(location)

    for i in GSVdata:
        totalSatAvgData.append(i)
    # print(totalSatAvgData)
    for i in totalSatAvgData:
        drawHouse(canvas, i)
    for i in totalSatAvgData:
        draw(canvas, i)

    drawInfo(canvas, time, date, location)
    resetSatHisMenu()


def resetSatHisMenu():
    menu1.delete(0, tk.END)
    for i in totalSatAvgData:
        s = 'satellite '
        s += str(i[0])
        menu1.add_command(label=s, command=partial(detailWin, str(i[0])))


def detailWin(i):
    s = ''
    print(TInfo[0][0])
    s = s + 'satellite ' + str(i) + '\n'
    s = s + 'Observation time: '  +\
        '\nStart: '  + str(TInfo[0][1]) + ' , ' + str(TInfo[0][0]) +  \
        '\nEnd: '+ str(TInfo[0][3]) + ' , ' + str(TInfo[0][2]) 
    s = s +  '\nElevation    Azimuth      SNR\n'
    oneSatData = allSatData[i]
    for j in oneSatData:
        s = s + '      ' + str(j[0])+'°            '+str(j[1]) + \
            '             '+str(j[2])+'\n'
    # print(s)
    tk.messagebox.showinfo(title='Satellite Info', message=s)


def errorMsg():
    msg = 'Please give correct GPS data'
    tk.messagebox.showinfo(title='Satellite Info', message=msg)
    pass


def process_NMEA(data):
    # save $GPGSV
    for i in reversed(range(len(data))):
        if data[i][:6] != '$GPGSV':
            del data[i]

    # split ',' and '*'
    # remove len error data
    for i in reversed(range(len(data))):
        data[i] = data[i].split('*')[0]
        data[i] = data[i].split(',')[4:]
        dataLen = len(data[i])

        if dataLen % 4 > 0 or dataLen > 16:
            # print('Error data:' + str(data[i]))
            del data[i]

    # Store individual data for each satellite
    tmp = []
    for line in data:
        for i in range(int(len(line)/4)):
            tmp.append(line[i*4:(i+1)*4])

    # remove data that is not a number
    for i in reversed(range(len(tmp))):
        for s in tmp[i]:
            if (s != '') and (not s.isdigit()):  # item error
                # print('Data that is not a number:' + str(tmp[i]))
                del tmp[i]

    # SNR = '' -> SNR = '0'
    for i in reversed(range(len(tmp))):
        for j in range(len(tmp[i])):
            if tmp[i][j] == '':
                tmp[i][j] = '0'

    # Remove out-of-range data
    for i in reversed(range(len(tmp))):
        error = False

        if not int(tmp[i][0]) in range(1, 33):  # satellite ID
            error = True
        if not int(tmp[i][1]) in range(0, 91):  # Elevation
            error = True
        if not int(tmp[i][2]) in range(0, 360):  # Azimuth
            error = True
        if not int(tmp[i][3]) in range(0, 100):  # SNR
            error = True

        if error:
            # print('Out-of-range data:' + str(tmp[i]))
            del tmp[i]
            continue

    for oneData in tmp:
        if oneData[0] in allSatData:
            allSatData[oneData[0]].append([oneData[1], oneData[2], oneData[3]])
        else:
            allSatData[oneData[0]] = [[oneData[1], oneData[2], oneData[3]]]

    return tmp  # [ID, Elevation, Azimuth, SNR]


def merge_NMEA(data):
    import numpy as np
    # [Elevation, Azimuth, SNR, count, availableCount]
    array = [[0, 0, 0, 0, 0] for i in range(33)]

    # sum
    for x in data:
        index = int(x[0])
        a = np.array(array[index])
        if int(x[3]) > 0:
            b = np.array([int(x[1]), int(x[2]), int(x[3]), 1, 1])
        else:
            b = np.array([0, 0, 0, 1, 0])
        array[index] = list(a + b)

    # avg
    tmp = []
    
    for i in range(33):
        sate = array[i]
        count = sate[3]
        avlCount = sate[4]

        # avg avlData
        if avlCount != 0:
            tmp.append([str(i)] + [str(int(sate[j] / avlCount))
                       for j in range(3)])
        # save SNR 0
        if avlCount == 0 and count != 0:
            for x in data:
                if(int(x[0]) == i):
                    tmp.append(x[:3] + [0])
                    break
        # save count
        if countList != 0:
            countList.append([str(i), str(count), str(avlCount)])

    for i in tmp:
        i[0] = (str(i[0])).zfill(2)
        i[1] = (str(i[1])).zfill(2)
        i[2] = (str(i[2])).zfill(3)
        i[3] = (str(i[3])).zfill(2)
    # print(countList)
    return tmp, countList


def getGPRMC(data):
    # save available $GPRMC
    for i in reversed(range(len(data))):
        if data[i][:6] != '$GPRMC' or data[i].split(',')[2] != 'A' or len(data[i].split(',')) != 13:
            del data[i]

    for i in reversed(range(len(data))):
        data[i] = data[i].split(',')
        data[i] = data[i][1:2] + data[i][3:7] + \
            data[i][9:10]  # [Time, Lat, N/S, Lng, E/W, Date]
        data[i][0] = data[i][0][:-3]
        error = False

        if len(data[i][0]) != 6:  # Time
            error = True
        if not int(float(data[i][1])/100) in range(0, 90):  # latitude
            error = True
        if not (data[i][2] == 'N' or data[i][2] == 'S'):  # N/S
            error = True
        if not int(float(data[i][3])/100) in range(0, 180):  # longitude
            error = True
        if not(data[i][4] == 'E' or data[i][4] == 'W'):  # E/W
            error = True
        if len(data[i][5]) != 6:  # Date
            error = True

        if error:
            # print('Error data:' + str(data[i]))
            del data[i]

    # for x in data:
    #     print(x)
    return data


def getTime(data):
    data = data[0]
    h = int(data[:2]) + 8
    m = int(data[2:4])
    s = int(data[4:6])

    m += int(h/24)
    h %= 24

    return str(h % 13).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2) + (' AM' if h <= 12 else ' PM')


def getDate(data):
    data = data[5]
    d = data[:2]
    m = data[2:4]
    y = '20' + data[4:6]

    return y + '/' + m + '/' + d


def getLocation(data):
    lat = str(float(data[1])/100).split('.')
    lng = str(float(data[3])/100).split('.')

    lat = lat[0] + '°' + lat[1][:2] + '\'' + lat[1][2:4] + '\"' + data[2]
    lng = lng[0] + '°' + lng[1][:2] + '\'' + lng[1][2:4] + '\"' + data[4]

    return lat + ' ' + lng


def getSatelliteDistance(degree):
    import math
    a = 1
    b = -12734*math.cos(math.radians(90 + degree))
    c = -665266800

    return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)

def getSatelliteDistance(degree):
    import math
    a = 1
    b = -12734*math.cos(math.radians(90 + degree))
    c = -665266800

    return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)

def isCovered(sData):
    degree = int(sData[1])
    SNR = int(sData[3])
    distance = getSatelliteDistance(degree)

    sData = [[distance, SNR]]
    clf = joblib.load('./model.pkl') # load model
    wantPredict = clf.predict(sData)

    # print(wantPredict)
    if wantPredict == [1]:
        print('Covered by buildings.')
        return True,'This satellite is covered by buildings.'
    elif wantPredict == [0]:
        print('Not Covered by buildings.')
        return False, 'This Satellite is not Covered by buildings.'

isCovered(['02', '65', '064', '18']) 

def main():
    colorDictInit()
    tkwin()


main()
