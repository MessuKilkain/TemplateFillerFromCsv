import os
import os.path
import csv
import io
import appJar
import tkinter.font as tkFont


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

def highlightSyntax(app, widgetName):
	tkText = app.getTextAreaWidget(widgetName)
	for tag in tkText.tag_names():
		tkText.tag_remove(tag, u"1.0", u"end")
	# for w in (u'SELECT', u'select'):
		# app.tagTextAreaPattern(widgetName, u"keyword", w)
	# app.tagTextAreaPattern(widgetName, u"template_valid", u"\{[^{}]+\}", regexp=True)
	app.tagTextAreaPattern(widgetName, u"template_valid", u"ADD/i", regexp=True)

def mainGui():
	with appJar.gui("Rename episodes", font={'size':12}) as app:
		app.setLogLevel(u'DEBUG')
		app.entry(u"csvFilePath", label=u"Csv path", kind='file', default=u'-- CSV file to use --')
		app.optionBox(u"csvSeparator", [u"auto",u",",u";"], label=u"CSV Separator")
		app.optionBox(u"templateLanguage", [u"normal text",u"sql"], label=u"Template language")
		def highlightSyntaxOnChange(widgetName):
			highlightSyntax(app, widgetName)
			return
		# Main template
		app.text(u"stringMainTemplate", focus=True, change=highlightSyntaxOnChange)
		app.checkBox(title=u'remplacement_EmptyByNull', name=u'\'\' by NULL')
		app.checkBox(title=u'remplacement_EqualNullByIsNull', name=u'= NULL by IS NULL')
		boldFont = tkFont.Font(font=app.getTextAreaWidget(u"stringMainTemplate")[u'font'])
		boldFont.configure(weight=u"bold")
		app.tagTextArea(u"stringMainTemplate", u"keyword", foreground=u"blue", font=boldFont)
		app.tagTextArea(u"stringMainTemplate", u"template_valid", foreground=u"green")
		app.entry(u"exportFilePath", label=u"New file path", kind='file', default=u'-- New file path --')
		def createFileFromCsvButtonPressed(widgetName):
			csvFilePath = app.getEntry(u'csvFilePath')
			exportFilePath = app.getEntry(u'exportFilePath')
			stringFormat = app.getTextArea(u'stringMainTemplate')
			if not csvFilePath:
				# csvFilePath should be defined
				app.errorBox(u'Error', u'Csv file path should be defined.')
				return
			if not os.path.isfile(csvFilePath):
				# csvFilePath should be a path to a file
				app.errorBox(u'Error', u'Csv file path should be a path to a directory.')
				return
			if not exportFilePath:
				newExportFilePath = app.saveBox(title=u"New file path", fileName=None, dirName=None, fileExt=None, fileTypes=None, asFile=None, parent=None)
				app.debug(u"newExportFilePath : %s",newExportFilePath)
				app.setEntry(u'exportFilePath',newExportFilePath)
				exportFilePath = newExportFilePath
			if not exportFilePath:
				# exportFilePath should be defined
				app.errorBox(u'Error', u'New file path should be a defined.')
				return
			if os.path.exists(exportFilePath):
				# exportFilePath already exists
				if not os.path.isfile(exportFilePath):
					# exportFilePath is not a file
					app.errorBox(u'Error', u'New file path should be a path to a file.')
					return
				if not app.yesNoBox(u"Overwrite warning", u"The file at path "+exportFilePath+u' already exists. Are you sure you want to overwrite it?'):
					return
			delimiter = app.getOptionBox(u"csvSeparator")
			# TODO : fill replacements list
			replacements = list()
			if app.getCheckBox(u"remplacement_EmptyByNull"):
				replacements.append(('\'\'','NULL'))
			if app.getCheckBox(u"remplacement_EqualNullByIsNull"):
				replacements.append((' = NULL',' IS NULL'))
			writeFileFromCsvAndTemplate(csvFilePath, stringFormat, exportFilePath, replacements, delimiter)
			return
		app.button(u"Create filled file", createFileFromCsvButtonPressed)
	return

if __name__ == '__main__':
	mainGui()





