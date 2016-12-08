from PyQt4 import QtGui,QtCore
from w import ui_nupdf
from pdfrw import PdfReader, PdfWriter
import os

win = None
outfile = None
last = ""

class func_data:
	def open_files():
		listWidget = win.pdfList
		global last
		a = QtGui.QFileDialog.getOpenFileNames(
			win, "Open Files", last, "Pdf files (*.pdf)")

		if a:
			last= os.path.dirname(a[0])
			listWidget.addItems(a)
	
	def current_list():
		try:
			current_item = win.pdfList.currentIndex().row()
			return current_item
		except:
			return -1


	def remove_item():
		l = win.pdfList
		current_item = func_data.current_list()
		if current_item!=-1:
			l.takeItem(current_item)

	def move_up():
		current_item = func_data.current_list()
		if current_item>0:
			l = win.pdfList
			item = l.item(current_item-1).text()
			l.takeItem(current_item-1)
			l.insertItem(current_item,item)
	
	def move_down():
		total = win.pdfList.count()-1
		current_item = func_data.current_list()
		if current_item!=-1 and current_item<total:
			l = win.pdfList
			item = l.item(current_item+1).text()
			l.item(current_item+1).setText(l.item(current_item).text())
			l.item(current_item).setText(item)
			l.setCurrentRow(current_item+1)

	def outfile_select():
		global last,outfile
		out = QtGui.QFileDialog.getSaveFileName(
			win, "Save File", last, "Pdf files (*.pdf)")

		if out:
			outfile = out
			last= os.path.dirname(outfile)
			win.outLine.setText(outfile)


	def merge_pdf():
		if outfile:
			total_pages = 0
			pdf_files = []
			file_count = win.pdfList.count()

			for i in range(file_count):
				try:

					pdf_files.append( PdfReader( win.pdfList.item(i).text() ) )
					total_pages = total_pages+pdf_files[-1].numPages
				except:
					pass
			
			done_pages = 0

			pdf_writer = PdfWriter()

			for i in pdf_files:
				win.pdfProgress.setValue(done_pages//total_pages)
				QtCore.QCoreApplication.processEvents()
				for j in range( i.numPages ):
					pdf_writer.addpage(i.getPage(j))
					done_pages = done_pages+1

			win.pdfProgress.setValue(100)
			pdf_writer.write(outfile)
			
		else:
			QtGui.QMessageBox.information(win, "Information", "No Output File Selected.",QtGui.QMessageBox.Ok)

	def about_func():
		QtGui.QMessageBox.information(win, "Information", "Application By:\nWaryam\n\nAcknowledgements:\nIcons from flaticon.com\nDesigned By: Pixel Buddha,\nDesigned By: Vectors Market",QtGui.QMessageBox.Ok)


app =QtGui.QApplication([])
mainWindow = ui_nupdf()
win = mainWindow

#Function Definitions

mainWindow.actionPdf.triggered.connect(func_data.open_files)
mainWindow.actionRemove.triggered.connect(lambda:func_data.remove_item())
mainWindow.actionUp.triggered.connect(func_data.move_up)
mainWindow.actionDown.triggered.connect(func_data.move_down)
mainWindow.outButton.clicked.connect(func_data.outfile_select)
mainWindow.mergeButton.clicked.connect(func_data.merge_pdf)
mainWindow.actionAbout.triggered.connect(func_data.about_func)

mainWindow.show()
app.exec_()