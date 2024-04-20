import os, sys
import struct
import shutil
from PIL import Image

orignal_path ="D:/隐写/yuan.bmp"
copy_path1 = "D:/隐写/隐写后图片/head.bmp"
copy_path2 = "D:/隐写/隐写后图片/eof.bmp"
copy_path3 = "D:/隐写/隐写后图片/data.bmp"
fsize = os.path.getsize(orignal_path)
fmax = open('D:/隐写/隐写信息/max.txt', 'r')
datamax = fmax.read()
fmin = open('D:/隐写/隐写信息/min.txt', 'r')
datamin = fmin.read()

def bmp_info(f):
    unpackbuf = struct.unpack('<ccIIIIIIHH', f)
    if (unpackbuf[0] != b'B' or unpackbuf[1] != b'M'):
        return None
    else:
        return {
            'bfSize': unpackbuf[2],#4字节整数：表示位图大小
            'bfRserverd': unpackbuf[3],#4字节整数：保留位，始终为0
            'bfOffBits': unpackbuf[4],#4字节整数：实际图像的偏移量
            'biSize': unpackbuf[5],#4字节整数：Header所需的字节数
            'biWidth': unpackbuf[6],#4字节整数：图像宽度
            'biHeight': unpackbuf[7], #4字节整数：图像高度
            'biPlames':unpackbuf[8],# #一个2字节整数：颜色平面数，始终为1
            'biBitCount': unpackbuf[9]#一个2字节整数：比特数/像素。
        }

# 头文件冗余隐写：修改文件头中的保留字段隐藏信息
def header_stegano():
    shutil.copy(orignal_path, copy_path1)#复制文件从src到dst。
    with open(copy_path1, 'r+b') as sfr: #已读写二进制模式打开文件
        str = input('请输入需要隐写的信息:  ')
        sfr.seek(0x0006)#用于移动文件读取指针到指定位置。地址偏移，即保留位的四字节
        sfr.write(str.encode())# 以 encoding 指定的编码格式编码字符串
        sfr.close()
        print("信息隐写成功")
    Operation()

# 头文件分析
def header_analysis():
    with open(copy_path1, 'rb') as afr:
        afr.seek(0x0006)
        ReserverData = afr.read(4)#读取4字节的数据
        if (ReserverData != 0x0000):
            print("分析成功")
            print("头文件隐写的信息是: ",ReserverData.decode())
        f = open('D:/隐写实验一/隐写信息/头部隐写.txt', mode='w')  # 打开文件，若文件不存在系统自动创建。
        f.write(ReserverData.decode())#以 encoding 指定的编码格式解码字符串
        f.close()
    Operation()

#尾部追加隐写
def eof_stegano():
    shutil.copy(orignal_path, copy_path2)
    with open(copy_path2, 'r+b') as sfr:
        sfr.seek(0, 2)
        print("1.数据量较大（>25%） 2.数据量较小（<1%） ")
        flag = eval(input("请选择: "))#执行选择的命令,并返回表达式的值
        print("")
        if flag == 1:
            sfr.write(datamax.encode())#写入 max的文件内容
            sfr.close()
            print("隐写成功，请查看隐写后图片的文件夹")
            Operation()
        elif flag == 2:
            sfr.write(datamin.encode())#写入 min 文件内容
            sfr.close()
            print("隐写成功，请查看隐写后图片的文件夹")
            Operation()
        else:
            print("请重新输入：")
            Steganography()

#尾部分析
def eof_analysis():
    with open(copy_path2, 'rb') as afr:
        im = Image.open(copy_path2)  # 返回一个Image对象
        print("------------------------------")
        print('bfwidth：%d, bfheight：%d ' % (im.size[0], im.size[1]))
        size = len(afr.read())
        print("图片实际大小为 {} byte".format(size))
        print("------------------------------")
        flag = eval(input("请输入位深度:"))#24位位图 和 8位位图选项
        orignalBytesphoto = 0
        # 24位图，一个像素点占3个字节 14位文件头，40位信息头，无调色板
        if flag == 24:
            orignalBytesphoto = im.size[0] * im.size[1] * 3 + 14 + 40
        # 8位位图，一个像素点占1个字节 14位文件头，40位信息头，有颜色表，每个颜色表结构体是4字节，无调色板
        elif flag == 8:
            orignalBytesphoto = im.size[0] * im.size[1] + 14 + 40 + 256 * 4
        else:
            print("请重新输入：")
        afr.seek(fsize)
        ReserverData = afr.read(size - orignalBytesphoto)#保留信息，通过判断源文件和隐写后的图片大小对比
        if (ReserverData != 0x0000):#差不为0 则隐写过
            print("隐写分析成功")  # 判断是否被隐写
            f = open('D:/隐写实验一/隐写信息/尾部隐藏.txt', mode='w')  # 打开文件，若文件不存在系统自动创建。
            f.write(ReserverData.decode())
            f.close()
        else:
            print("该图片没有被隐写!")
        Operation()

#数据区的直接覆盖隐写
def bmp_data():
    shutil.copy(orignal_path, copy_path3) #文件复制
    with open(copy_path3, 'r+b') as sfr:
        sfr.seek(0x0054)     #到指定的位置
        print("1.数据量较大（>25%） 2.数据量较小（<1%） ")
        flag = eval(input("请选择: "))
        print("")
        if flag == 1:
            sfr.write(datamax.encode())#写入 datamax内容
            sfr.close()
            print("隐写成功，请查看隐写后图片的文件夹")
            Operation()
        elif flag == 2:
            sfr.write(datamin.encode()) #写入 datamin内容
            sfr.close()
            print("隐写成功，请查看隐写后图片的文件夹")
            Operation()
        else:
            print("请重新输入：")
            Steganography()

#数据分析  指针移动到偏移位置读取字节的信息长度
def bmp_data_analysis():
    with open(copy_path3, 'rb') as afr:
        afr.seek(0x0054)    #移动到指定位置
        ReserverData = afr.read(len(datamax))  #max文件内容
        if (ReserverData != 0x0000):
            print("信息隐写成功")
            f = open('D:/隐写实验一/隐写信息/数据区隐写.txt', mode='w')  # 打开文件，若文件不存在系统自动创建。
            f.write(ReserverData.decode())  #写入内容到 hidden_data 文件中
            f.close()
            Operation()

def Steganography():
    print("__________________________________")
    print("1.头文件冗余部分的隐写 　 　      |")
    print("2.文件尾部追加隐写    　         |")
    print("3.数据区直接覆盖的隐写 　　　      |")
    print("4.退出             　 　　      |")
    print("|_________________________________|")
    flag = eval(input("请输入要进行的操作: "))
    print("")
    if flag == 1:
        header_stegano()
    elif flag == 2:
        eof_stegano()
    elif flag == 3:
        bmp_data()
    elif flag == 4:
        Operation()
    else:
        print("请重新输入: ")
        Steganography()

def Analysis():
    print("_______________________________________________")
    print("|1.头文件冗余部分的分析  |")
    print("|2.文件尾部追加分析     |")
    print("|3.数据区直接覆盖的分析  |")
    print("|4.退出               |")
    print("_________________________________________________|")
    flag = eval(input("请输入要进行的操作: "))

    print("")
    if flag == 1:
        header_analysis()
    elif flag == 2:
        eof_analysis()
    elif flag == 3:
        bmp_data_analysis()
    elif flag == 4:
        Operation()
    else:
        print("请重新输入: ")
        Analysis()

def Operation():
    print("_________________________")
    print("|1.隐写        |")
    print("|2.分析        |")
    print("|3.退出        |")
    print("|_______________________|")
    flag = eval(input("请输入要进行的操作: "))
    print("")
    if flag == 1:
        Steganography()
    elif flag == 2:
        Analysis()
    elif flag == 3:
        sys.exit()
    else:
        print("请重新输入: ")
        Operation()

if __name__ == '__main__':
    Operation()