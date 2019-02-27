import os
import os.path
import csv
import io
import argparse

def csvToStringFormat(csvFilePath, stringFormat, outputStream, delimiter = u'auto'):
    # formattedString = ''
    # delimiter = u';'
    # delimiter = u','
    with open (csvFilePath, 'r') as f:
        if delimiter == u"auto":
            dialect = csv.Sniffer().sniff(f.readline()) #### detect delimiters
            f.seek(0)
            delimiter = dialect.delimiter
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            # print(stringFormat)
            # print(dict(row))
            # formattedString += stringFormat.format(**dict(row))
            #TODO : add check to do that only when using sql syntax
            for key, value in row.items():
                row[key] = value.replace("'","''")
            print(stringFormat.format(**dict(row)), file=outputStream)
    # return formattedString
    return

def getHeaderListFromCsv(csvFilePath, delimiter = u'auto'):
    headerList = list()
    return headerList

def writeFileFromCsvAndTemplate(csvFilePath, stringFormat, sqlFilePath, replacements=(), delimiter = u'auto'):
    outputStream = io.StringIO('')
    csvToStringFormat(csvFilePath, stringFormat, outputStream, delimiter)
    outputString = outputStream.getvalue()
    outputStream.close();
    # print(outputString)
    for replacementCouple in replacements:
        # print(replacementCouple)
        # print(replacementCouple[0])
        # print(replacementCouple[1])
        outputString = outputString.replace(replacementCouple[0], replacementCouple[1])
    with open (sqlFilePath, 'w') as f:
        f.write(outputString)

sqlKeywords = (u"ADD",u"EXTERNAL",u"PROCEDURE",u"ALL",u"FETCH",u"PUBLIC",u"ALTER",u"FILE",u"RAISERROR",u"AND",u"FILLFACTOR",u"READ",u"ANY",u"FOR",u"READTEXT",u"AS",u"FOREIGN",u"RECONFIGURE",u"ASC",u"FREETEXT",u"REFERENCES",u"AUTHORIZATION",u"FREETEXTTABLE",u"REPLICATION",u"BACKUP",u"FROM",u"RESTORE",u"BEGIN",u"FULL",u"RESTRICT",u"BETWEEN",u"FUNCTION",u"RETURN",u"BREAK",u"GOTO",u"REVERT",u"BROWSE",u"GRANT",u"REVOKE",u"BULK",u"GROUP",u"RIGHT",u"BY",u"HAVING",u"ROLLBACK",u"CASCADE",u"HOLDLOCK",u"ROWCOUNT",u"CASE",u"IDENTITY",u"ROWGUIDCOL",u"CHECK",u"IDENTITY_INSERT",u"RULE",u"CHECKPOINT",u"IDENTITYCOL",u"SAVE",u"CLOSE",u"IF",u"SCHEMA",u"CLUSTERED",u"IN",u"SECURITYAUDIT",u"COALESCE",u"INDEX",u"SELECT",u"COLLATE",u"INNER",u"SEMANTICKEYPHRASETABLE",u"COLUMN",u"INSERT",u"SEMANTICSIMILARITYDETAILSTABLE",u"COMMIT",u"INTERSECT",u"SEMANTICSIMILARITYTABLE",u"COMPUTE",u"INTO",u"SESSION_USER",u"CONSTRAINT",u"IS",u"SET",u"CONTAINS",u"JOIN",u"SETUSER",u"CONTAINSTABLE",u"KEY",u"SHUTDOWN",u"CONTINUE",u"KILL",u"SOME",u"CONVERT",u"LEFT",u"STATISTICS",u"CREATE",u"LIKE",u"SYSTEM_USER",u"CROSS",u"LINENO",u"TABLE",u"CURRENT",u"LOAD",u"TABLESAMPLE",u"CURRENT_DATE",u"MERGE",u"TEXTSIZE",u"CURRENT_TIME",u"NATIONAL",u"THEN",u"CURRENT_TIMESTAMP",u"NOCHECK",u"TO",u"CURRENT_USER",u"NONCLUSTERED",u"TOP",u"CURSOR",u"NOT",u"TRAN",u"DATABASE",u"NULL",u"TRANSACTION",u"DBCC",u"NULLIF",u"TRIGGER",u"DEALLOCATE",u"OF",u"TRUNCATE",u"DECLARE",u"OFF",u"TRY_CONVERT",u"DEFAULT",u"OFFSETS",u"TSEQUAL",u"DELETE",u"ON",u"UNION",u"DENY",u"OPEN",u"UNIQUE",u"DESC",u"OPENDATASOURCE",u"UNPIVOT",u"DISK",u"OPENQUERY",u"UPDATE",u"DISTINCT",u"OPENROWSET",u"UPDATETEXT",u"DISTRIBUTED",u"OPENXML",u"USE",u"DOUBLE",u"OPTION",u"USER",u"DROP",u"OR",u"VALUES",u"DUMP",u"ORDER",u"VARYING",u"ELSE",u"OUTER",u"VIEW",u"END",u"OVER",u"WAITFOR",u"ERRLVL",u"PERCENT",u"WHEN",u"ESCAPE",u"PIVOT",u"WHERE",u"EXCEPT",u"PLAN",u"WHILE",u"EXEC",u"PRECISION",u"WITH",u"EXECUTE",u"PRIMARY",u"WITHIN GROUP",u"EXISTS",u"PRINT",u"WRITETEXT",u"EXIT",u"PROC")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Produit un fichier sql à partir du contenu d'un fichier csv.")
    parser.add_argument(u'csvFilePath', type=str, help="Fichier csv contenant les données.")
    parser.add_argument(u'tplSql', type=argparse.FileType('r'), help="Fichier sql template à utiliser pour la création du fichier sql de sortie.")
    parser.add_argument(u'output', type=argparse.FileType('w'), help="Chemin du fichier sql produit.")
    args = parser.parse_args()
    templateString = args.tplSql.read()
    csvToStringFormat(csvFilePath=args.csvFilePath, stringFormat=templateString, outputStream=args.output)

