import sys
from matplotlib import pyplot as plt
import urllib
import numpy as np
import xml.etree.ElementTree
from PyQt5.QtWidgets import *

from multiprocessing import Pool

# extract a list of resolution information from xml
def queryresolution(result):
    resolutionlist=[]
    url = 'http://www.rcsb.org/pdb/rest/describePDB?structureId={}'.format(','.join(result.split('\n')).strip(','))
    req = urllib.request.Request(url)
    f = urllib.request.urlopen(req)
    result = f.read().decode("utf-8")
    et=xml.etree.ElementTree.fromstring(result)
    for child in et:
        try:
            resolutionlist.append(child.attrib['resolution'])
        except:
            pass
    return resolutionlist

# represent an advanced search as xml
def queryPDB(year):
    queryText = """
<?xml version="1.0" encoding="UTF-8"?>
<orgPdbCompositeQuery version="1.0">
 <queryRefinement>
  <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.ExpTypeQuery</queryType>
    <description>Experimental Method is ELECTRON MICROSCOPY</description>
    <mvStructure.expMethod.value>ELECTRON MICROSCOPY</mvStructure.expMethod.value>
  </orgPdbQuery>
 </queryRefinement>
 <queryRefinement>
   <orgPdbQuery>
    <version>head</version>
    <queryType>org.pdb.query.simple.ReleaseDateQuery</queryType>
    <database_PDB_rev.date.comparator>between</database_PDB_rev.date.comparator>
    <database_PDB_rev.date.min>{}</database_PDB_rev.date.min>
    <database_PDB_rev.date.max>{}</database_PDB_rev.date.max>
    <database_PDB_rev.mod_type.comparator><![CDATA[<]]></database_PDB_rev.mod_type.comparator>
    <database_PDB_rev.mod_type.value>1</database_PDB_rev.mod_type.value>
  </orgPdbQuery>
 </queryRefinement>
</orgPdbCompositeQuery>
""".format(str(year)+"-01-01",str(year)+"-12-31")
    return queryText

# Main function to plot the # of structures vs year
def YearlyGrowthofStructuresSolvedByElectronMicroscopy(start,end):
    pdbcount=[]
    pdbcounttotal=[]
    p=Pool(4)
    result=p.map(querywebyear,range(start,end+1))
    p.close()
    for i in range(end-start+1):
        pdbcount.append(result[i].count('\n'))
        pdbcounttotal.append(sum(pdbcount))

    fig, ax = plt.subplots()
    ind = np.arange(end-start+1)
    b1=ax.bar(ind+0.2, pdbcount, color='green',align='center',width=0.4)
    b2=ax.bar(ind-0.2,pdbcounttotal,color='blue',align='center',width=0.4)

    ax.set_xticklabels(np.arange(start,end+1))
    ax.set_xticks(ind)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number")
    ax.set_title('Structures Solved By Electron Microscopy')
    ax.legend((b1[0],b2[0]),("Yearly","Total"),loc=2)
    plt.show()
# query PDB for the Yearly growth,used in multiprocessing
def querywebyear(i):
    url = 'http://www.rcsb.org/pdb/rest/search'
    req = urllib.request.Request(url, data=queryPDB(i).encode("UTF-8"))
    f = urllib.request.urlopen(req)
    result = f.read().decode("utf-8")
    return result
# Main function to plot the # of structures vs year vs resolution
def YearlyGrowthofStructuresSolvedByElectronMicroscopyVsRes(start,end,low,high):
    p=Pool(4)
    result=p.map(querywebyear,range(start,end+1))
    p.close()
    res=[]
    for i in result:
        c=np.asarray(queryresolution(i),dtype='float')
        res.append((c<low).sum())
        res.append(((c>=low)&(c<high)).sum())
        res.append((c>=high).sum())
    fig, ax = plt.subplots()
    ind = np.arange(end-start+1)
    years=len(ind)
    b1=ax.bar(ind-0.2, res[::3], color='red',align='center',width = 0.2)
    b2=ax.bar(ind, res[1::3], color='yellow',align='center',width = 0.2)
    b3=ax.bar(ind+0.2, res[2::3], color='blue',align='center',width = 0.2)
    ax.set_xticklabels(np.arange(start,end+1))
    ax.set_xticks(ind)
    ax.set_xlabel('Year')
    ax.set_ylabel('Numbers')
    ax.legend((b1[0],b2[0],b3[0]),('<{}A'.format(low),'{}~{}A'.format(low,high),'>{}A'.format(high)),loc=2)
    ax.set_title('Number of structures vs Resolution')
    plt.show()

#GUI
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PDB EM search tool'
        #self.left = 100
        #self.top = 100
        #self.width = 640
        #self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        # Create textbox
        self.textbox1 = QLineEdit()
        label1=QLabel("From year")
        label2=QLabel("to")
        self.textbox2 = QLineEdit()
        self.button1 = QPushButton('plot', self)
        labellayout1=QHBoxLayout()
        labellayout1.addWidget(label1)
        labellayout1.addWidget(self.textbox1)
        labellayout1.addWidget(label2)
        labellayout1.addWidget(self.textbox2)
        labellayout1.addWidget(self.button1)

        self.button1.clicked.connect(self.on_click1)

        label3=QLabel("1.Plot yearly growth")
        label4=QLabel("2.Plot yearly growth vs resolution")

        self.textbox3 = QLineEdit()
        # self.textbox3.setMaxLength(10)
        label5=QLabel("0 ~")
        label6=QLabel("~")
        label7=QLabel("~ inf.")
        self.textbox4 = QLineEdit()
        self.button2 = QPushButton('plot', self)
        self.statusbar = QStatusBar()
        # self.statusbar.showMessage("Plotting......")
        # self.textbox5 = QLineEdit()
        # self.button2 = QPushButton('plot', self)
        labellayout2=QHBoxLayout()
        labellayout2.addWidget(label5)
        labellayout2.addWidget(self.textbox3)
        # labellayout3=QHBoxLayout()
        labellayout2.addWidget(label6)

        labellayout2.addWidget(self.textbox4)
        labellayout2.addWidget(label7)
        labellayout2.addWidget(self.button2)
        labellayout2.addStretch(1)

        self.button2.clicked.connect(self.on_click2)


        # labellayout3.addWidget(self.textbox5)

        mainlayout=QGridLayout()
        mainlayout.addWidget(label3,0,0)
        mainlayout.addLayout(labellayout1,1,0)
        mainlayout.addWidget(label4,2,0)
        mainlayout.addLayout(labellayout2,3,0)
        mainlayout.addWidget(self.statusbar,4,0)

        self.setLayout(mainlayout)
        self.resize(480,160)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show()

    def on_click1(self):
        try:
            textboxValue1 = self.textbox1.text()
            textboxValue2 = self.textbox2.text()

            if 1997<=int(textboxValue1)<=int(textboxValue2)<=2017:
                self.statusbar.showMessage("Plotting......Please wait until plot window show up!")
                YearlyGrowthofStructuresSolvedByElectronMicroscopy(int(textboxValue1),int(textboxValue2))
                self.statusbar.clearMessage()
            else:
                QMessageBox.warning(self, 'Wrong Time Period', "Please input correct year! ", QMessageBox.Ok)
                self.textbox1.setText("")
                self.textbox2.setText("")
        except:
            QMessageBox.warning(self, 'Empty', "Please input correct year! ", QMessageBox.Ok)
    def on_click2(self):

        try:
            textboxValue1 = self.textbox1.text()
            textboxValue2 = self.textbox2.text()
            textboxValue3 = self.textbox3.text()
            textboxValue4 = self.textbox4.text()
            if 1997<=int(textboxValue1)<=int(textboxValue2)<=2017:
                if 0<int(textboxValue3)<int(textboxValue4):
                    self.statusbar.showMessage("Plotting......Please wait until plot window show up!")
                    YearlyGrowthofStructuresSolvedByElectronMicroscopyVsRes(int(textboxValue1),int(textboxValue2),int(textboxValue3),int(textboxValue4))
                    self.statusbar.clearMessage()
                else:
                    QMessageBox.warning(self, 'Wrong cutoff!', "Please input again! ", QMessageBox.Ok)
                    self.textbox3.setText("")
                    self.textbox4.setText("")
            else:
                QMessageBox.warning(self, 'Wrong Time Period', "Please input correct year! ", QMessageBox.Ok)
                self.textbox1.setText("")
                self.textbox2.setText("")
        except:
            QMessageBox.warning(self, 'Empty', "Please fill in all textbox! ", QMessageBox.Ok)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
