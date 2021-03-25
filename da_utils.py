
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


def dataAdder(db,caller, table, **other):
    keyList = list(other.keys())
    valueList = list(other.values())
    stmt = 'INSERT INTO ' + table + ' ' "(" + str(keyList)[1:-1].replace("'","") + ") VALUES ("+ str(valueList)[1:-1] + ")"
    try:
        db.query(stmt)
        db.commit()
    except Exception as e:
        print(e)
        pass
    else:
        pass
    finally:
        pass
