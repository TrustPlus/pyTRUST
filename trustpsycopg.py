import psycopg2
import psycopg2.extras

class TableManagement:
    """__TableManagement__
           This class manipulates a PostGres Database and implements a template designed for 
           SECIM. 
           <img src="/home/setafur/src/SECIM/secimtools/LIMS/secimlims/images/secimDBClassDiagram.png" alt="DB Model" title="SECIM Database" height="600px"></img>
           \f[ 
                   \includegraphics[height=8in]{/home/setafur/src/SECIM/secimtools/LIMS/secimlims/images/secimDBClassDiagram}
           \f]
           The mehods defined here in are written to reflect initialization of the database 
           for use with the SECIM requirements defined in the SECIM metadata spreadsheets 
           derived from UCSD. These methods include the following:

    __Private Constructors__:
    Constuctors only available within the _TableManagement_ class.
           - _init_: Class constructor.
               - Opens connection and cursor to the PostGres Database. Two types of
                   cursors are provided; dictionary cursor, and tuple cursor.
                   Counters | DB Params
                   ---------| -------
                   projectCount    | conn
                   studyCount      | authDict
                   nmrCount        | cur
                   msiCount        | dictcur
                   massSpecCount   | dbData
    
           - _createTable_: Table constructor.

           - _addTableColumns_: Column constructor.

    __Public Constructors__:
    Constuctors available to methods calling the _TableManagement_ class.
           - _createProjectTable_
           - _createStudyTable_
           - _createNMRTable_
           - _addNMRTableColumns_

    __Private Destructors__:
    Destructors available only within the _TableManagement_ class.
           - _addNMRTableColumns_
           - _dropTableColumns_
           - _del_

    __Public Destructors__:
    Destructors available to methods calling the _TableManagement_ class.
               - _dropProjectTable_
               - _dropStudyTable_
               - _dropNMRTable_
               - _dropNMRTableColumns_

    __Private Getters__:
    Getters available only within the _TableManagement_ class.
           - _getTableColumns_
           - _getAllTableData_
           - _getSequentialTableRowData_

    __Public Getters__:
    Getters available to methods calling the _TableManagement_ class.
           - _getTables_
           - _getTablePrivileges_
           - _getProjectColumns_
           - _getStudyColumns_
           - _getNMRColumns_
           - _getAllNMRTableData_
           - _getSequentialNMRTableRows_

    __Private Setters__:
    Setters available only within the _TableManagement_ class.
           - _insertValueIntoTable_
           - _updateValueInTable_

    __Public Setters__:
    Setters available to methods calling the _TableManagement_ class.
           - _insertValueIntoNMRTable_
           - _updateNMRTableValues_"""
    #Initialize all table counts.

    ##Counter of Project tables.
    projectCount = 0
    ##Counter of Study Tables
    studyCount = 0
    ##Counter of NMR Tables.
    nmrCount = 0
    ##Counter of MSI Tables
    msiCount = 0
    ##Counter of Mass Spec. tables.
    massSpecCount = 0
    
    ## Connection to database. Provides Dictionary and Tuple cursors.
    conn = []   
    ## Dictionary with all the authentication parameters provided to conn.
    authDict = {}   
    ## Tuple cursor. Provides access to execution and fetching in database.
    cur = []    
    ## Dictionary cursor. Provides access to exec. & fetch. in database.
    dictcur = {}
    ## List of data fetched from cur or dictcur.
    dbData = []

#Constructors
    #Private
    def __init__(self, mode, authString):
        """__init__ :
               This method initializes the TableManagement Class. This __init__ method 
                primarily conducts simple checks to ensure that the method instantiating
            the class has the appropriate permissions in the database it is trying to 
            access.
            
               @param mode: Mode with which to open the class.
            
            @param authString: Authentication providing all the credentials required to
                access the database at the given level of priviliages
                   required by the requested mode.
               
               This method provides the connection, self.conn, cursor, self.cur,
                dictionary cursor, self.dictcur, and authentication parameters, 
                   self.authDict required by all the remaining methods of this class, 
    
                   eg. 
                   dbname='<DB>' user='<user>' host='<host>' port='<port>' password='<pass>'"""

        authDict = authString.split(' ')
        authDict = dict([i.split('=') for i in authDict])
        #self.authDict = {key.strip('\''): item.strip('\'') for key,item in authDict.items()}
        
        for key,item in authDict.items():
            self.authDict.update({key.strip('\''): item.strip('\'')})
        
        #print 'Connection config:'
        #print authDict
        self.conn = psycopg2.connect(authString)
        self.cur = self.conn.cursor()
        self.dictcur =  self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        #Define login profile, connection, and cursor based on mode.
        self.mode = mode
        if self.mode == 'r':
            print 'Trying to connect to database in read mode.'
            #Check current user priviliges on the currently connected.
            execString = "select * from database_privs('"+self.authDict['user']+"');"
            self.cur.execute(execString)
            priv_test = self.cur.fetchall()
            #print priv_test
            #Test Priviliges in current database.
            for i in priv_test:
                if i[1]==self.authDict['dbname']:
                    print 'DB priv: ', i
                    if 'CREATE' in i[2]:
                        print 'User:', self.authDict['user'], ' - Incorrect priviliges.'
                        print 'Disconnecting and exiting.' 
                        self.cur.close()
                        self.conn.close()
                        exit(1)
                    else:
                        print 'User', self.authDict['user'], 'successfuly connected.'
        elif self.mode == 'rw':
            print 'Trying to connect to database in read/write mode.'
            #Check current user priviliges on the currently connected.
            execString = "select * from database_privs('"+self.authDict['user']+"');"
            self.cur.execute(execString)
            priv_test = self.cur.fetchall()
            #print priv_test
            #Test Priviliges in current database.
            for i in priv_test:
                if i[1]==self.authDict['dbname']:
                    print 'DB priv: ', i
                    if 'CREATE' not in i[2]:
                        print 'User:', self.authDict['user'], ' - Incorrect priviliges.'
                        print 'Disconnecting and exiting.'
                        self.cur.close()
                        self.conn.close()
                        exit(1)
                    else:
                        print 'User', self.authDict['user'], 'successfuly connected.'
        else:
            print 'Do not recognize connection mode. Please select r/rw.'
            print 'Disconnecting and exiting.'
            self.cur.close()
            self.conn.close()
            exit(1)

    def __createTable(self,tableName, tableColumns):
        if self.mode == 'rw':
            executeString = "CREATE TABLE " + tableName + " (" +tableColumns + ");"
            self.cur.execute(executeString)
            self.conn.commit()
        else:
            print 'Could not write table. Wrong permisions.'

    def _addTableColumns(self,tableName,columnNameList):
        #TODO Sergio to ADD permissions check for table in which column is being created.
        for i in columnNameList:
            executeString="ALTER TABLE "+tableName+" ADD COLUMN "+i+" text;"
            self.cur.execute(executeString)
            self.conn.commit()

#Destructors
    #Private
    def __dropTable(self,tableName):
        if self.mode == 'rw':
            executeString = "DROP TABLE " + tableName+";"
            self.cur.execute(executeString)
            self.conn.commit()
        else:
            print 'Could not drop table. Wrong permisions.'

    def _dropTableColumns(self,tableName,columnNameList):
        #TODO Sergio to ADD permissions check for table in which column is being created.
        for i in columnNameList:
            executeString="ALTER TABLE "+tableName+" DROP COLUMN "+i+";"
            self.cur.execute(executeString)
            self.conn.commit()

#Getters
    #Private
    def _getTableColumns(self, tableName):
        self.cur.execute('SELECT * FROM '+tableName+';')
        columnNames = [i[0] for i in self.cur.description]
        return columnNames

    def _getAllTableData(self,tableName):
        self.dictcur.execute('SELECT * FROM '+tableName+';')
        allTableData = self.dictcur.fetchall()
        return allTableData

    def _getSequentialTableRowData(self,tableName,rows):
        self.dictcur.execute('SELECT * FROM '+tableName+';')
        tableRowData = []
        tableRowData = [tableRowData.append(self.dictcur.fetchone()) for i in range(rows[0], rows[1])]
        return tableRowData

    #Public
    def getTables(self):
        execString = "SELECT table_name FROM information_schema.tables\
                      WHERE table_schema = 'public'"
        self.cur.execute(execString)
        result = self.cur.fetchall()
        badChars = "(){}<>',"
        tables = []
        for table in result:
            table = str(table)
            for c in badChars: table = table.replace(c, "")
            tables.append(table)
        return tables

    def getTablePrivileges(self,tableName):
        execString = "SELECT * FROM table_privs('"+self.authDict['user']+"');"
        self.dictcur.execute(execString)
        privTest = self.dictcur.fetchall()
        for i in privTest:
            testTableName = list(tableName)
            if i['relname']==testTableName[0]:
                return i
            else:
                print 'Table',testTableName,'not found.'
                return 0

#Setters
    #Private
    def _insertValueIntoTable(self,tableName,columnList,itemList):
        columnParams = []
        for i in columnList:
            columnParams.append('%s')
        columnParams = ', '.join(columnParams)
        columnList = ','.join(columnList)
        executeString = "INSERT INTO "+tableName+" ("+columnList+") VALUES ("+columnParams+")"
        self.cur.executemany(executeString, itemList)
        self.conn.commit()

    def _updateValueInTable(self,tableName,ids,columns,items):
        updateValues = []
        pgsql_return_values = []
        for item in items:
            updateValue = []
            for entry in zip(columns,item):
                #print entry
                updateString = entry[0]+' = '+"'{0}'".format(entry[1])
                updateValue.append(updateString)
            updateValues.append(updateValue)
        columns = ', '.join(columns)
        for (value_id,values) in zip(ids,updateValues):
            values = ', '.join(values)
            value_id = str(value_id)
            executeString = "UPDATE "+tableName+" SET "+values+" WHERE ID = "+value_id+ \
                " RETURNING id, "+columns+";"
            #print executeString
            self.cur.execute(executeString)
            self.conn.commit()
            #pgsql_return_values.append(self.cur.fetchall())
        #return pgsql_return_values
