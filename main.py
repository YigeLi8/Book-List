import math

def bookListFileConversion():
    #Format of the library files
    # <book name>#<number of copies>#<restricted>

    #blOpen -> Open the booklist.txt
    blOpen = open("booklist-2.txt", "r")
    #bookList -> Array of booklist
    bookList = []

    s = blOpen.readline()
    s = s.rstrip("\n")

    while s != "":

      a = s.split("#")
      bookList.append(a)
      s = blOpen.readline()
      s = s.rstrip("\n")

    return bookList


def libraryLogFileConversion():

    #llOpen -> Open the librarylog.txt
    llOpen = open("librarylog-3.txt", "r")
    #libraryLog -> Array of library log
    libraryLog = []

    s = llOpen.readline()
    s = s.rstrip("\n")

    while s != "":

      a = s.split("#")
      libraryLog.append(a)
      s = llOpen.readline()
      s = s.rstrip("\n")

    return libraryLog


book_list = bookListFileConversion()
library_log = libraryLogFileConversion()

total_amount_fines = 0
paid_fines = 0

num_books = {}
for book in book_list:
    if book[0] not in num_books:
        num_books[book[0]] = int(book[1])

book_restrictions = {}
for book in book_list:
    if book[0] not in book_restrictions:
        book_restrictions[book[0]] = book[2]

borrowed_db = {}
fines_db = {}
borrowed_books_db = {}

borrowed_time_books = {}
for entry in library_log:
    if len(entry) > 1:
        # real entry
        action = entry[0]
        day = entry[1]
        if action == 'B':
            # Borrowing
            student_name = entry[2]
            book_name = entry[3]
            days_borrowed_for = entry[4]
            if book_name in borrowed_books_db:
                if borrowed_books_db[book_name] <= num_books[book_name]:
                    if student_name not in borrowed_db:
                        borrowed_db[student_name] = []
                    if student_name in fines_db:
                        if fines_db[student_name] == 0:
                            borrowed_db[student_name].append([book_name, int(day)])
                            borrowed_books_db[book_name] += 1
                            if book_name not in borrowed_time_books:
                                borrowed_time_books[book_name] = int(days_borrowed_for)
                            else:
                                borrowed_time_books[book_name] += int(days_borrowed_for)
                    else:
                        borrowed_db[student_name].append([book_name, int(day)])
                        borrowed_books_db[book_name] += 1
                        if book_name not in borrowed_time_books:
                            borrowed_time_books[book_name] = int(days_borrowed_for)
                        else:
                            borrowed_time_books[book_name] += int(days_borrowed_for)
            else:


                if student_name not in borrowed_db:
                    borrowed_db[student_name] = []
                if student_name in fines_db:
                    if fines_db[student_name] == 0:
                        borrowed_db[student_name].append([book_name, int(day)])
                        borrowed_books_db[book_name] = 1
                        if book_name not in borrowed_time_books:
                            borrowed_time_books[book_name] = int(days_borrowed_for)
                        else:
                            borrowed_time_books[book_name] += int(days_borrowed_for)
                else:
                    borrowed_db[student_name].append([book_name, int(day)])
                    borrowed_books_db[book_name] = 1
                    if book_name not in borrowed_time_books:
                        borrowed_time_books[book_name] = int(days_borrowed_for)
                    else:
                        borrowed_time_books[book_name] += int(days_borrowed_for)

        elif action == 'R':
            # Returning
            student_name = entry[2]
            book_name = entry[3]
            timeAllowed = 28
            if book_restrictions[book_name]:
                timeAllowed = 7

            if student_name in borrowed_db:
                for book in borrowed_db[student_name]:
                    if book[0] == book_name:
                        if int(day) - book[1] > timeAllowed and timeAllowed == 7:
                            if student_name not in fines_db:
                                fines_db[student_name] = 0
                            fines_db[student_name] += 5*(int(day) - book[1])
                        elif int(day) - book[1] > timeAllowed and timeAllowed == 28:
                            if student_name not in fines_db:
                                fines_db[student_name] = 0
                            fines_db[student_name] += 1*(int(day) - book[1])


        elif action == 'A':
            # Adding
            book_name = entry[2]
            if book_name not in num_books:
                num_books[book_name] = 1
            else:
                num_books[book_name] += 1
            if book_name not in book_restrictions:
                book_restrictions[book_name] = False

        elif action == 'P':
            # Paying Fine
            student_name = entry[2]
            amount_paid = entry[3]
            paid_fines += int(amount_paid)
            if student_name in fines_db:
                fines_db[student_name] -= int(amount_paid)
        else:
            print("ERROR: Invalid Action")
            print(entry)
    elif len(entry) == 1:
        # current day
        current_day = int(entry[0])


def find_most_borrowed():
    borrowed_time_books_sorted = sorted(borrowed_time_books, key=borrowed_time_books.get, reverse=True)
    for i in borrowed_time_books_sorted:
        print("{}: {}".format(i, borrowed_time_books[i]))


def find_borrow_ratios():
    for i in borrowed_time_books:
        print(i, borrowed_time_books[i], num_books[i])
        print(math.floor(100*num_books[i]/float(borrowed_time_books[i])))


# find_most_borrowed()
print("="*50)
print("="*50)
# find_borrow_ratios()

print(fines_db)