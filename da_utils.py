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
    print('da_utils ~40 otherValueList = ',otherKeyList)
    otherValueList = list(other.values())
    print('da_utils ~42 otherValueList = ',otherValueList)
    insertList = " (" + str(otherKeyList)[1:-1].replace("'","") + ") VALUES ("+ str(otherValueList)[1:-1] + ")"
    print('da_utils ~44 insertList = ',insertList)
    n = 0
    updateList = ''
    while n < len(otherKeyList):
        unknown = str((otherValueList[n]))
        p = re.compile('\d{4')
        m = p.match(unknown)
        print('da_utils ~51 p=',m)
        if m:
            unknown = m.group()
        else:
            unknown = "'" + unknown + "'"
        print('da_utils ~46 unkown =', unknown)
        updateList = updateList + otherKeyList[n] + ' = ' + unknown +", "
        n+= 1
    updateList = updateList[:-2]
    print('da_utils ~55 updateList =', updateList)
    stmt = "SELECT * from " + table +' where ' + keyVal
    c = db.cursor()
    c.execute(stmt)
    itemString = str(c.fetchone())
    if itemString.upper() == 'NONE':
        stmt = 'INSERT INTO ' + table + insertList
        print('da_utils ~59 da_utils',stmt)
        try:
            db.query(stmt)
            db.commit()
        except Exception as e:
            print('da_utils  ~62',e)
        pass
    else:
        stmt = 'UPDATE ' + table + '\nSET '+ updateList +'\n WHERE ' + keyVal
        print('~66 da_utils',stmt)
        db.query(stmt)
        db.commit()

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
    print(rtnStr)
    return rtnStr[:-1]
