import Tkinter as tk
from PIL import Image, ImageTk

import requests
import cStringIO
import praw

def resize(im):
	while (im.size[0]>600 or im.size[1]>600):
		x=int(im.size[0]/1.2)
		y=int(im.size[1]/1.2)
		im = im.resize((x,y))
		print x,y
	return im

class App:

	def __init__(self,master,submissions):
		frame = tk.Frame(master)
		frame.pack()
		
		self.button = tk.Button(frame, text="Quit",fg="red", command=frame.quit)
		self.button.pack()
		self.submissions = submissions
		
		self.submission = next(submissions)
		image = self.get_image()
		self.title = self.submission.title
		
		self.MainImage = tk.Canvas(frame, width=600, height=600)
		self.MainImage.pack()
		tk.tki = ImageTk.PhotoImage(image)
		self.MainImage.create_image(300,300,image=tk.tki)

		self.InputBox = tk.Entry(frame,width=50)
		self.InputBox.pack()
		self.InputBox.focus_set()
		
		self.Submit = tk.Button(frame,text="Submit",command=lambda:self.submit(self.title))
		self.Submit.pack()
		
		self.Next = tk.Button(frame,text="Next",command=lambda:self.generate())
		self.Next.pack()
		
		self.Answer = tk.Button(frame,text="Answer",command=lambda:self.answer())
		self.Answer.pack()
	
	def generate(self):
		
		self.submission = next(self.submissions)
		image = self.get_image()
		self.title = self.submission.title
		self.InputBox.delete(0,tk.END)
		
		print self.title
		
		tk.tki = ImageTk.PhotoImage(image)
		self.MainImage.create_image(300,300,image=tk.tki)
		self.MainImage.pack()
		
		self.InputBox.focus_set()

	def submit(self,title):
		s= self.InputBox.get()
		
		if s in title:
			self.InputBox.delete(0,tk.END)
			self.InputBox.insert(0,"correct")
		else:
			self.InputBox.delete(0,tk.END)
			self.InputBox.insert(0,"incorrect")
			
	def get_image(self):
		loop=1
		while loop:
			print self.submission.url
		
			if 'i.imgur' in self.submission.url:
				r = requests.get(self.submission.url)
				i=Image.open(cStringIO.StringIO(r.content))
				i = resize(i)
				loop=0
			else:
				self.submission = next(self.submissions)
		return i
		
	def answer(self):
		self.InputBox.delete(0,tk.END)
		self.InputBox.insert(0,self.title)
					
root = tk.Tk()

user_agent=("test program by /u/MMPSteez")
r = praw.Reddit(user_agent=user_agent)
submissions = r.get_subreddit('cityporn').get_new(limit=200)

app = App(root,submissions)
root.mainloop()
