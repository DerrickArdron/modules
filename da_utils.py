import re

def fix_apostrophe(value):
    if "'" in value:
        value = value.replace("'","''")
    return(value)

def createTable(db, tableName, index, *cols):
    stmt = "DROP TABLE IF EXISTS " + tableName + ";"
    db.query(stmt)
    db.commit()

    stmt = "create table if not exists \"" + tableName + "\" (%s)" % ",".join(cols)
    stmt = "create table " + tableName + " (%s)" % ",".join(cols)
    stmt = stmt[:-1] + ',' + index+')'
    # for debugging the next 3 lines write the stmt to a text file

    with open("createTable.txt","w") as txtFile:
        txtFile.write(stmt)
        txtFile.close()
    # now execute the stmt
    db.query(stmt)
    db.commit()
    print('added', tableName)


def dataAdder(db,caller, table, keyVal, **other):
    #print('~26 da_utils keyVal =', keyVal,'Key Length', len(keyVal))
    #print('~26 da_utils other =',other)
    otherKeyList = list(other.keys())
    otherValueList = list(other.values())
    insertList = " (" + str(otherKeyList)[1:-1].replace("'","") + ") VALUES ("+ str(otherValueList)[1:-1] + ")"
    n = 0
    updateList = ''
    while n < len(otherKeyList):
        # wrap any year (4 numerics) in a string for SQL Update below
        unknown = str((otherValueList[n]))
        p = re.compile('\d{4')
        m = p.match(unknown)
        if m:
            unknown = m.group()
        else:
            unknown = "'" + unknown + "'"


        updateList = updateList + otherKeyList[n] + ' = ' + unknown + ", "
        n += 1
    updateList = updateList[:-2]
    if len(keyVal) > 0:
        # is there a row corresponding to the keval in the database
        stmt = "SELECT * from " + table +' where ' + keyVal
        c = db.cursor()
        c.execute(stmt)
        itemString = str(c.fetchone())
    else:
        itemString = 'NONE'
    if itemString.upper() == 'NONE':
        # there is no row in the database with that primary key so INSERT
        stmt = 'INSERT INTO ' + table + insertList
        stmtCopy = stmt
        #print('da_utils Insert stmt =', stmt)
        try:
            db.query(stmt)
            db.commit()
        except Exception as e:
            print('Caller', caller,'Insert Exception:', e)
            print('Stmt',stmtCopy)

        except TypeError as e:
            print('Caller', caller,'OperationalError:', e)
            print('Stmt',stmtCopy)

        '''
        except ErrorCode as e:
            print('Caller', caller,'OperationalError:', e)
            pass
        '''

    else:
        # there is a row in the database with that primary key so UPDATE
        stmt = 'UPDATE ' + table + '\nSET '+ updateList +'\n WHERE ' + keyVal
        # print('~66 da_utils stmt =',stmt)
        stmtCopy = stmt
        try:
            db.query(stmt)
            db.commit()
        except Exception as e:
            print('Caller', caller,'Update Exception:', e)
            print('Stmt',stmtCopy)

        except TypeError as e:
            print('Caller', caller,'Update TypeError:', e)
            print('Stmt',stmtCopy)



def makeSrch(keyColumns, keyValues):
    n = 0
    rtnStr =''
    while n < len(keyColumns):
        if n > 0:
            rtnStr = rtnStr[:-1] + " and "
        if str(type(keyValues[n])) == "<class 'int'>":
            keyValue = str(keyValues[n])
        else:
            keyValue = "'" + keyValues[n] + "'"
        rtnStr = rtnStr + keyColumns[n] + ' = ' +keyValue + "'"
        n += 1
    return rtnStr[:-1]


def makeDataDict(database, table, db, dataTuple):
    stmt = "SELECT Column_Name FROM \
    INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + database + \
    "'and TABLE_NAME = '" + table + "';"
    stmtCopy = stmt
    c = db.cursor()
    c.execute(stmt)
    hdrTuple = c.fetchall()
    rowStr = ''
    n= 0
    dataDict = {}
    for row in hdrTuple:
        rowStr = stringStripper(row)
        dataDict[rowStr] = dataTuple[n]
        n += 1
    return dataDict

def stringStripper(input):
    input = str(input)
    input = input.replace('(','',100)
    input = input.replace(')','',100)
    input = input.replace(',','',100)
    input = input.replace("'",'',100)
    return input


