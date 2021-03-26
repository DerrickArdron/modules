
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


def valType(inPut):
    if str(type(inPut)) == "<class 'int'>":
        rtnVal = str(inPut)
    else:
        rtnVal = "'" + inPut + "'"
    return rtnVal


def dataAdder(db,caller, table, keyVal, **other):
    '''
    pKeyList = list(pKey.keys())
    pKeyValues = list(pKey.values())

    n = 0
    pKeyStr =''
    while n < len(pKey):
        if n > 0:
            pKeyStr = pKeyStr + ', '
        pKeyStr = pKeyStr +pKeyList[n] +' = ' + valType(pKeyValues[n])
        print('~39', pKeyStr)
        n += 1
    #pKeyStr = pKeyStr + ')'
    '''

    otherKeyList = list(other.keys())
    otherValueList = list(other.values())
    keyValueList = " (" + str(otherKeyList)[1:-1].replace("'","") + ") VALUES ("+ str(otherValueList)[1:-1] + ")"
    n = 0
    updateList = ''
    while n < len(otherKeyList):
        updateList = updateList + otherKeyList[n] + ' = ' + valType(otherValueList[n]) +", "
        n+= 1
    updateList = updateList[:-2]
    print('~55 ', updateList)
    stmt = "SELECT * from " + table +' where ' + keyVal
    c = db.cursor()
    c.execute(stmt)
    itemString = str(c.fetchone())
    if itemString.upper() == 'NONE':
        stmt = 'INSERT INTO ' + table + keyValueList
        try:
            db.query(stmt)
            db.commit()
        except Exception as e:
            print(e)
        pass
    else:
        stmt = 'UPDATE ' + table + '\nSET '+ updateList +'\n WHERE ' + keyVal
        print('~64 da_utils',stmt)
        db.query(stmt)
        db.commit()
