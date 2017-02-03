
# coding: utf-8

# In[4]:

from matplotlib import pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog


# In[65]:


class Application(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self)
        self.grid()
        self.createWidgets()
        self.centerwindow()
#         self.plotsomething()
    def findfilename(self):
        self.filename=filedialog.askopenfilename(title = "Select file")
        lines=np.loadtxt(self.filename).transpose()
        plt.plot(lines[0],lines[1],'-*')
        plt.show()
    def createWidgets(self):
        self.findbutton= tk.Button(self,text='select file',command=self.findfilename)
        self.findbutton.pack(fill='both', expand='yes')
#         self.findbutton.grid(row=1,column=1)
        self.tt=tk.Text(self,wrap='word')
        self.tt.insert('1.0',"1.click the button above\n2.choose a file(e.g.two_column.txt)\n3.plot window will show separately")
        self.tt.pack(fill='both',expand='yes')
#         self.tt.grid(row=2,column=1)

    def centerwindow(self):
        w = 200 
        h = 200 
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        
app = Application()
app.title('Zhouw_hw7')
app.mainloop()


# In[ ]:



