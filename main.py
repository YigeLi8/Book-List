'''
main file
'''


def bookListFileConversion():
    #Format of the library files
    # <book name>#<number of copies>#<restricted>

    #blOpen -> Open the booklist.txt
    blOpen = open("booklist.txt", "r")
    #bookList -> Array of booklist
    bookList = []

    s = blOpen.readline()
    s = s.rstrip("\n")

    while s != "":

      a = s.split("#")
      bookList.append(a)
      s = blOpen.readline()
      s = s.rstrip("\n")

    print(bookList)
    return bookList


def libraryLogFileConversion():

    #llOpen -> Open the librarylog.txt
    llOpen = open("librarylog-1.txt", "r")
    #libraryLog -> Array of library log
    libraryLog = []

    s = llOpen.readline()
    s = s.rstrip("\n")

    while s != "":

      a = s.split("#")
      libraryLog.append(a)
      s = llOpen.readline()
      s = s.rstrip("\n")

    print(libraryLog)
    return libraryLog

bookListFileConversion()
libraryLogFileConversion()