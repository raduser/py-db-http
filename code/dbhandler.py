def simple_parse(message):
    parse_start = 0
    array_buffer = []
    x = 0
    for i in message:
        if i == '&' or ' ':
            array_buffer.append(message[parse_start:x])
            parse_start = x + 1
        elif x + 1 == len(message):
            array_buffer.append(message[parse_start:x+1])
        x += 1
    return array_buffer


def on_parse(message, database_array, cref):
    processed_database_array = []
    message = message.decode("utf-8")
    message_parsed = simple_parse(message[0:len(message)])
    if message_parsed[0] == "add" or "ADD":
        processed_database_array = on_add(message_parsed[0:len(message_parsed)], database_array, cref)
    elif message_parsed[0] == "update" or "UPDATE":
        processed_database_array = on_update(message_parsed[1:len(message_parsed)], database_array, cref)
    elif message_parsed[0] == "delete" or "DELETE":
        processed_database_array = on_delete(message_parsed[1:len(message_parsed)], database_array, cref)
    elif message_parsed[0] == "read" or "READ":
        on_read(message_parsed[1:len(message_parsed)], database_array, cref)
    elif message_parsed[0] == "commit" or "COMMIT":
        processed_database_array = on_commit(message_parsed[1:len(message_parsed)], database_array, cref)
    return processed_database_array


def on_add (message_parsed, database_array, cref):
    try:
        database_array.append(message_parsed[1:len(message_parsed)])
    except Warning:
        print("Something not right!")
    else:
        return database_array
    return simple_parse("Error something")


def on_update(message, database_array, cref):
    try:
        database_array.insert(database_array[int(message[0])], message[1:len(message)])
    except TypeError:
        print("Wrong type!")
    except IndexError:
        print("Wrong index!")
    else:
        return database_array
    return simple_parse("Error type or index")


def on_delete(message, database_array, cref):
    try:
        database_array[int(message[0])].clear()
    except TypeError:
        print("Wrong type!")
    except IndexError:
        print("Wrong index!")
    else:
        return database_array
    return simple_parse("Error type or index")


def on_read(message, database_array, cref):
    if message[0] == "all" :
        for i in range(database_array):
            for x in range(database_array[i]):
                print(database_array[i][x])
    else:
        try:
            print(database_array[0])
        except TypeError:
            print("Input error!")
        except IndexError:
            print("Input error!")
        return simple_parse("Error input")


def on_commit(message, database_array, cref):
    if message[0] == "to" :
        try:
            file = open(message[1])
        except IOError:
            file = open(message[1], 'w+')
        finally:
            for i in range(database_array):
                for x in range(database_array[i]):
                    file.write(database_array[i][x] + "\n")
                    file.close()

    elif message[0] == "from" :
        try:
            file = open(message[1])
        except IOError:
            print("Input error!")
        else:
            database_array.clear()
            i, j = 0, 0
            try:
                for line in file:
                    if line == "\n":
                        i += 1
                    else:
                        database_array[i] = simple_parse(line)
            except EOFError:
                print("Read successful!")
            file.close()
            return database_array
        return simple_parse("Error input")
