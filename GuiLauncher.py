import os
import os.path
import csv
import io
import appJar
import tkinter.font as tkFont
import TemplateFillerFromCsv

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
			TemplateFillerFromCsv.writeFileFromCsvAndTemplate(csvFilePath, stringFormat, exportFilePath, replacements, delimiter)
			return
		app.button(u"Create filled file", createFileFromCsvButtonPressed)
	return

if __name__ == '__main__':
	mainGui()





