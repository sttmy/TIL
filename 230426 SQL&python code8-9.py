# p401

from tkinter import *
root = Tk()
root.geometry("200x250")
upFrame =Frame(root)
upFrame.pack()
downFrame = Frame(root)
downFrame.pack()
editBox = Entry(upFrame, width=10)    # 입력이 되는 화면 구성
editBox.pack(padx=20, pady=20)
listBox = Listbox(downFrame, bg='yellow')
listBox.pack()
listBox.insert(END, "하나")   # END: 들어가는 위치, 하나씩 집어넣음
listBox.insert(END, "둘")
listBox.insert(END, "셋")
root.mainloop()