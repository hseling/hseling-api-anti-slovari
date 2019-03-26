import boilerplate


def process_data(file):
    """Split all files contents and then combine unique words into resulting file.
    """
    # result = set()
    #
    # for _, contents in data_to_process.items():
    #     if isinstance(contents, bytes):
    #         text = contents.decode('utf-8')
    #     else:
    #         text = contents
    #     result |= set([word + "!!!" for word in text.split()])
    #
    # if result:
    #     yield None, '\n'.join(sorted(list(result)))
    conn = boilerplate.get_mysql_connection()
    cur = conn.cursor()
    print(file)
    name = file[:-4]
    print(name)
    cur.execute("SELECT table_name from information_schema.tables where \
        table_schema = 'hse-api-database' and table_name = '%s'", name)
    resp = cur.fetchone()
    print(resp)
    try:
        text = boilerplate.get_file(file).decode('utf-8')
        if name == 'main':
            f = [tuple(x.split(';')) for x in text.split('\n')]
        else:
            f = [tuple(x.split(',')[1:]) for x in text.split('\n')]
        print(f[:5])
        cur.execute("CREATE TABLE `hse-api-database`.{} \
            (word varchar(300), lemma varchar(300), morphs varchar(300), categories varchar(100))".format(name))
        for tup in f:
            try:
                cur.execute("INSERT INTO `hse-api-database`.{}(word,lemma,morphs,categories)\
                    VALUES(%s, %s, %s, %s)".format(name), tup)
                # print("INSERT INTO `hse-api-database`.{}(word,lemma,morphs,categories)\
                #     VALUES(%s, %s, %s, %s)".format(name))
            except:
                print(tup)
                raise
        conn.commit()
        return name, text
    except:
        pass
