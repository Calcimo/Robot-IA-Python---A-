from Classes.City import City
from Classes.Case import Case
from Classes.Building import Building
from Classes.Task import Task
from Classes.Robot import Robot
from Classes.Team import Team
from time import *
from tkinter import *
from tkinter import tix

#clear popup
def cleanup(e, er, top):
    global value
    global valuer
    value=e.get()
    value = int(value)
    if value < 12 or value > 50:
    	print("Size must be between 12 and 50, your size : ", value)
    	cleanup(e, er, top)
    valuer=er.get()
    valuer=int(valuer)
    if valuer < 1 or valuer > 4:
    	print("Number of robots must be between 1 and 4, your number : ", valuer)
    	cleanup(e, er, top)
    top.destroy()

#popup
def popup(b):
    top=Toplevel(fenetre)
    l=Label(top,text="Choose a size for your city (between 12 and 50) ")
    l.pack()
    e=Entry(top)
    e.pack()
    l=Label(top,text="How many robots do you want in each team (between 1 and 4) ")
    l.pack()
    er=Entry(top)
    er.pack()
    be=Button(top,text='Ok',command=lambda:cleanup(e, er, top))
    be.pack()
    b["state"] = "disabled" 
    fenetre.wait_window(top)
    b["state"] = "normal"

#move
def move_start(event):
    canvas.scan_mark(event.x, event.y)
def move_move(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

#windows zoom
def zoomer(event):
	if (event.delta > 0):
		canvas.scale("all", event.x, event.y, 2, 2)
		testCity.mult *= 2
	elif (event.delta < 0):
		if (testCity.mult > 1):
			canvas.scale("all", event.x, event.y, 0.5, 0.5)
			testCity.mult *= 0.5
		elif (testCity.mult == 1):
			print("You can't zoom out anymore")
	testCity.refreshGenerate(canvas)
	canvas.configure(scrollregion = canvas.bbox("all"))

fenetre = tix.Tk()
fenetre.geometry("1200x700")
canvas = Canvas(fenetre, width=30*20, height=30*20)
testCity = 0
#bouton=Button(fenetre, text="Commancer la génération", command=fenetre.quit)
#bouton.pack()
def callback(b):
	global testCity
	try:
		testCity.reload = 1
	except:
		pass
	try:
		for i in range(len(testCity.teams)):
			for j in range(len(testCity.teams[i].robots)):
				testCity.teams[i].robots[j].meter.destroy()
	except:
		pass
	for Widget in fenetre.winfo_children():
		#print("suppression: ", Widget)
		Widget.pack_forget()
	b = Button(fenetre, text="Generate a random map", command=lambda:callback(b), background="white", activebackground ="black", activeforeground="white", font='Helvetica 12 bold')
	b.pack()
	try:
		del testCity
	except:
		pass
	popup(b)
	testCity = City(value,value, canvas,fenetre, valuer)
	canvas.pack()

	canvas.scale("all", 0, 0, 2, 2)
	testCity.mult *= 2
	testCity.refreshGenerate(canvas)
	canvas.configure(scrollregion = canvas.bbox("all"))

	#ba = Button(fenetre, text="YA UN ROBOT", command=lambda:testCity.addRobot(canvas, testCity.deplacement(canvas, fenetre)))
	ba = Button(fenetre, text="Let's go !", command=lambda:[testCity.lemouv(canvas, fenetre)], background="white", activebackground ="black", activeforeground="white", font='Helvetica 12 bold')
	ba.pack()
	ba.place(x=140,y=20)
b = Button(fenetre, text="Generate a random map", command=lambda:callback(b), background="white", activebackground ="black", activeforeground="white", font='Helvetica 12 bold')
b.pack()

# This is what enables using the mouse:
canvas.bind("<ButtonPress-1>", move_start)
canvas.bind("<B1-Motion>", move_move)

#windows scroll
canvas.bind("<MouseWheel>",zoomer)
fenetre.mainloop()