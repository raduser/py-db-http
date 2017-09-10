def simple_parse(message):
    parse_start = 0
    buffarray = []
    for i in range(len(message)):
         if message[i] == " ":
            buffarray.append(message[parse_start:i])
            parse_start = i
         elif i == len(message):
             buffarray.append(message[parse_start:len(message)])
    return buffarray


def on_parse(message, dbarray, cref):
    message_parsed = simple_parse(message)
    if(message[0] == "add"):
        dbarrayb = on_add(message_parsed[1:len(message_parsed)], dbarray, cref)
        if dbarrayb != 0:
            dbarray = dbarrayb
    elif(message[0] == "update"):
        dbarrayb = on_update(message_parsed[1:len(message_parsed)], dbarray, cref)
        if dbarrayb != 0:
            dbarray = dbarrayb
    elif(message[0] == "delete"):
        dbarrayb = on_delete(message_parsed[1:len(message_parsed)], dbarray, cref)
        if dbarrayb != 0:
            dbarray = dbarrayb
    elif(message[0] == "read"):
        on_read(message_parsed[1:len(message_parsed)], dbarray, cref)
    elif(message[0] == "commit"):
        dbarrayb = on_commit(message_parsed[1:len(message_parsed)], dbarray, cref)
        if dbarrayb != 0:
            dbarray = dbarrayb
    return dbarray


def on_add (message_parsed, dbarray, cref):
    try:
        dbarray.append(message_parsed)
    except Warning:
        cref.wfile.write("Something no right!".encode("utf-8"))
    else:
        return dbarray
    return 0


def on_update(message, dbarray, cref):
    try:
        dbarray.insert(dbarray[int(message[0])], message[1:len(message)])
    except TypeError:
        cref.wfile.write("Wrong type!".encode("utf-8"))
    except IndexError:
        cref.wfile.write("Wrong index!".encode("utf-8"))
    else:
        return dbarray
    return 0


def on_delete(message, dbarray, cref):
    try:
        dbarray[int(message[0])].clear()
    except TypeError:
        cref.wfile.write("Wrong type!".encode("utf-8"))
    except IndexError:
        cref.wfile.write("Wrong index!".encode("utf-8"))
    else:
        return dbarray

def on_read(message, dbarray, cref):
    if(message[0] == "all"):
        for i in range(dbarray):
            for x in range(dbarray[i]):
                cref.wfile.write(dbarray[i][x].encode("utf-8"))
    else:
        try:
            cref.wfile.write(dbarray[int(message[0])].encode("utf-8"))
        except TypeError:
            cref.wfile.write("Wrong type!".encode("utf-8"))
        except IndexError:
            cref.wfile.write("Wrong index!".encode("utf-8"))


def on_commit(message, dbarray, cref):
    if(message[0] == "to"):
        try:
            file = open(message[1])
        except IOError:
            file = open(message[1], 'w+')
        finally:
            for i in range(dbarray):
                for x in range(dbarray[i]):
                    file.write(dbarray[i][x] + "\n")
                    file.close()
    elif(message[0] == "from"):
        try:
            file = open(message[1])
        except IOError:
            cref.wfile.write("Wrong filename!".encode("utf-8"))
        else:
            dbarray.clear()
            i, j = 0, 0
            try:
                for line in file:
                    if line == "\n":
                        i += 1
                    else:
                        dbarray[i] = simple_parse(line)
            except EOFError:
                cref.wfile.write("File was read!".encode("utf-8"))
            file.close()
            return dbarray


def on_sort(message, dbarray, cref):
    print(1)