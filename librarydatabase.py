import math

#Collaborators: Yige Li, Grace Kang, Adan Zurek, Alexander Teo

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

#modify these values to find if it can be borrowed
restrict_day = -1
student_can_borrow = "Piotr"
student_can_borrow_book = "Dragon reborn"
student_can_borrow_for_days = 3

total_days = 0
total_amount_fines = 0
paid_fines = 0

num_books = {}
book_added_db = {}
for book in book_list:
    if book[0] not in num_books:
        num_books[book[0]] = int(book[1])
    if book[0] not in book_added_db:
        book_added_db[book[0]] = 0

book_restrictions = {}
for book in book_list:
    if book[0] not in book_restrictions:
        book_restrictions[book[0]] = book[2]

borrowed_db = {}
fines_db = {}
borrowed_books_db = {}
actually_borrowed_db = {}


borrowed_time_books = {}
for entry in library_log:
    if len(entry) > 1:
        # real entry
        action = entry[0]
        day = entry[1]
        if restrict_day != -1:
            if restrict_day == int(day):
                if student_can_borrow in fines_db:
                    if fines_db[student_can_borrow] > 0:
                        print(student_can_borrow + " cannot borrow.")
                        break
                if student_can_borrow_book in borrowed_books_db:
                    if borrowed_books_db[student_can_borrow_book] <= num_books[student_can_borrow_book]:
                        print(student_can_borrow + " cannot borrow.")
                        break
                if student_can_borrow_book in book_restrictions:
                    if book_restrictions[student_can_borrow_book] == 'TRUE':
                        if student_can_borrow_for_days > 7:
                            print(student_can_borrow + " cannot borrow.")
                            break
                    else:
                        if student_can_borrow_for_days > 28:
                            print(student_can_borrow + " cannot borrow.")
                            break
                else:

                    if student_can_borrow_for_days > 28:
                        print(student_can_borrow + " cannot borrow.")
                        break
                if student_can_borrow != "":
                    print(student_can_borrow + " can borrow.")
                break
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
            if book_restrictions[book_name] == 'TRUE':
                timeAllowed = 7

            remove_index = -1
            if student_name in borrowed_db:
                for i in range(len(borrowed_db[student_name])):
                    book = borrowed_db[student_name][i]
                    if book[0] == book_name:
                        if int(day) - book[1] > timeAllowed and timeAllowed == 7:
                            if student_name not in fines_db:
                                fines_db[student_name] = 0
                            fines_db[student_name] += 5*(int(day) - (book[1]+timeAllowed))
                        elif int(day) - book[1] > timeAllowed and timeAllowed == 28:
                            if student_name not in fines_db:
                                fines_db[student_name] = 0
                            fines_db[student_name] += 1*(int(day) - (book[1]+timeAllowed))
                        borrowed_books_db[book_name] -= 1
                    if book_name not in actually_borrowed_db:
                        actually_borrowed_db[book_name] = int(day) - book[1]
                    else:
                        actually_borrowed_db[book_name] += int(day) - book[1]
                    remove_index = i
                    break
                if remove_index != -1:
                    borrowed_db[student_name].pop(remove_index)



        elif action == 'A':
            # Adding
            book_name = entry[2]
            if book_name not in num_books:
                num_books[book_name] = 1
            else:
                num_books[book_name] += 1
            if book_name not in book_restrictions:
                book_restrictions[book_name] = False
            if book_name not in book_added_db:
                book_added_db[book_name] = int(day)

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
        total_days = int(entry[0])

for entry in borrowed_db:
    if len(borrowed_db[entry]) > 0:
        if len(borrowed_db[entry][0]) > 0:
            if borrowed_db[entry][0][0] in actually_borrowed_db:
                actually_borrowed_db[borrowed_db[entry][0][0]] += (total_days - int(borrowed_db[entry][0][1]))

most_borrowed_with_usage = {}



def find_most_borrowed():
    for i in actually_borrowed_db:
        print("{}: {}".format(i, actually_borrowed_db[i]))
        most_borrowed_with_usage[i] = [actually_borrowed_db[i]]


def find_borrow_ratios():
    for i in borrowed_time_books:
        if i in actually_borrowed_db:
            print(i + str(": ") + str(math.floor(100*float(actually_borrowed_db[i])/float(num_books[i]*total_days))))
            if i in most_borrowed_with_usage:
                most_borrowed_with_usage[i].append(math.floor(100*float(actually_borrowed_db[i])/float(num_books[i]*total_days)))

def find_usage_ratios():
    for i in borrowed_time_books:
        if i in actually_borrowed_db:
            print(i + str(": ") + str(math.floor(100*float(actually_borrowed_db[i]+1)/float((num_books[i]*(total_days - book_added_db[i]))))))
            if i in most_borrowed_with_usage:
                most_borrowed_with_usage[i].append(math.floor(100*float(actually_borrowed_db[i])/float(actually_borrowed_db[i] + num_books[i]*total_days)))



def show_fines():
    for fine in fines_db:
        print(fine, fines_db[fine])

if restrict_day == -1:
    find_most_borrowed()
    print("="*50)
    print("="*50)
    find_borrow_ratios()
    print("="*50)
    print("="*50)
    find_usage_ratios()
    print("="*50)
    print("="*50)
    show_fines()
