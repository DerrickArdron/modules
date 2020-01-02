import csv, sqlite3

def _get_col_datatypes(fin):
    dr = csv.DictReader(fin) # comma is default delimiter
    fieldTypes = {} # a
    for entry in dr:
        fieldsLeft = [f for f in dr.fieldnames if f not in fieldTypes.keys()]
        if not fieldsLeft: break # We're done
        for field in fieldsLeft:
            data = entry[field]
        # Need data to decide
        if len(data) == 0:
            #continue
            fieldTypes[field] = "TEXT"

        if data.isdigit():
            fieldTypes[field] = "INTEGER"
        else:
            fieldTypes[field] = "TEXT"
    # TODO: Currently there's no support for DATE in sqllite

    if len(fieldsLeft) > 0:
        raise Exception("Failed to find all the columns data types - Maybe some are empty?")

    return fieldTypes


def escapingGenerator(f):
    for line in f:
        yield line.encode("ascii", "xmlcharrefreplace").decode("ascii")


def csvToDb(csvFile,dbFile,tablename, outputToFile = False):

    with open(csvFile,mode='r', encoding="ISO-8859-1") as fin:
        dt = _get_col_datatypes(fin)

        fin.seek(0)

        reader = csv.DictReader(fin)

        # Keep the order of the columns name just as in the CSV
        fields = reader.fieldnames
        cols = []

        # Set field and type
        for f in fields:
            cols.append("\"%s\" %s" % (f, 'TEXT'))
            #cols.append("\"%s\" %s" % (f, dt[f]))

        # Generate create table statement:
        stmt = "create table if not exists \"" + tablename + "\" (%s)" % ",".join(cols)
        with open("csvToDb.txt","w") as txtFile:
            txtFile.write(stmt)
            txtFile.close()
        con = sqlite3.connect(dbFile)
        cur = con.cursor()
        cur.execute(stmt)
        con.commit()

        stmt = "DELETE from " +tablename
        cur.execute(stmt)

        fin.seek(0)


        reader = csv.reader(escapingGenerator(fin))
        reader.__next__()


        # Generate insert statement:
        stmt = "INSERT INTO \"" + tablename + "\" VALUES(%s);" % ','.join('?' * len(cols))

        cur.executemany(stmt, reader)
        con.commit()
        con.close()

def createTable(dbFile, tableName, primaryKey, *cols):
    con = sqlite3.connect(dbFile)
    cur = con.cursor()

    stmt = 'Drop TABLE IF EXISTS "'+ tableName +'"'
    cur.execute(stmt)
    con.commit()

    stmt = "create table if not exists \"" + tableName + "\" (%s)" % ",".join(cols)
    stmt = stmt[:-1]
    stmt = stmt + ', CONSTRAINT compoundPK PRIMARY KEY (' +primaryKey +'))'
    with open("createTable.txt","w") as txtFile:
        txtFile.write(stmt)
        txtFile.close()
    cur.execute(stmt)
    con.commit()

    '''
    stmt = "DELETE from " +tableName
    cur.execute(stmt)
    con.commit()
    con.close()
    '''


def dataAdder(caller,dbFile, table, **other):
    # print('~112',caller, dbFile, table, pKeyName, pKey, other)
    con = sqlite3.connect(dbFile)
    cur = con.cursor()
    keyStr = ''
    valueStr = ''
    valueList = []
    for key in other:
        keyStr = keyStr + ', '+ key
        valueList.append(str(other[key]))
    for item in valueList:
        valueStr = valueStr + '\''+item +'\','
    valueStr = valueStr[:-1]
    '''
    stmt = 'SELECT "GlRef" from Output where "GlRef" = \'' + pKey +"'"
    cur.execute(stmt)
    con.commit()
    itemString = str(cur.fetchone())
    if itemString.upper() == 'NONE':
    '''
    stmt = 'INSERT INTO ' +table+'\nVALUES ('+ valueStr + ')'
    '''
    else:
        subStmt = ""
        for key in other:
            value = "{value}".format(value = other[key])
            if "'" in value:
                value = value.replace("'","''")
            subStmt = subStmt + key + ' = \'' + value +'\','
        subStmt = subStmt[:-1]
        stmt = 'UPDATE Output\nSET '+subStmt +'\nWHERE GlRef = \'' + pKey +'\''
    #print('stmt ~138', stmt)
    '''
    cur.execute(stmt)
    con.commit()

def output(dbFile, table, fileName):
    con = sqlite3.connect(dbFile)
    cur = con.cursor()
    cur.execute('select * from '+ table)
    colnames = cur.description
    headers =[]
    for row in colnames:
        headers.append(row[0])
        # print(headers)
    with open(fileName, 'w', newline = '') as outCSV:
        outWriter = csv.writer(outCSV)
        outWriter.writerow(headers)
        stmt = 'SELECT * FROM ' + table
        cur.execute(stmt)
        rows = cur.fetchall()
        for row in rows:
            outWriter.writerow(row)
        outCSV.close()
        
def fix_apostrophe(value):
    if "'" in value:                   
        value = value.replace("'","''")
    return(value)