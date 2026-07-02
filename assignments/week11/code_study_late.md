(please read this in "code" seciton on github"


The code I've decided to study is https://github.com/geekcomputers/Python/blob/master/Image-watermarker/app.py
It's an application to put in watermarks on images.
We start off with some imported libraries. As I looked them up these seem to help with a lot of different stuff. :

customtkinter: this builds the actual window you see on screen, with buttons and boxes. I might come back to this for my own use later on for the project.
filedialog: this is the little pop-up window that says "pick a file from your computer." Like when you click "Upload Photo" and a window opens showing your folders.
CTkMessagebox: this makes small pop-up alert boxes, like error or etc.
Image and ImageTk: these seem to be for opening and showing pictures.
Watermark:this comes from a different file the programmer made themselves.
pyglet: a tool that helps load special fancy fonts that aren't already on your computer.
colorchooser: this allows you to choose color


Then the variables are defined.
We have stuff like img, logo,color_code to store different things into memory.

load_image() lets us pick a pic from the computer into the app.
move_logo() lets us drag the watermark with the mouse.
move_text does the same thing with text.
the rest are similar to these, then comes save_image which saves where everything has been put and saves them into one image.

Overall, this file with about 300 hundred lines basically builds up the ui as far as I understood. It's building a lot of frames and buttons and defining borders and errors. Another file (watermark.py) is the actual thing that commands to stamp the mark onto the image.
Most of the pop-up stuff like the file picker and color picker come from the imported libraries, so they're not coded from scratch. 
This eases my brain a bit because I am also keeping an eye around for codes that I can take example of for my final project.

A part where I decided to look in more closely is the drag and drop part. I found how it works interesting.

It happens to first follow the mouse's location, then makes the logo follow it.

new_x = e.x and new_y = e.y logs the mouse position.
And image_canvas.coords(logo, new_x, new_y) tells it to move the logo to mouse position.
These seem to be possible with the help of customtkinter. This one might come in handy for me later on.

Finally defining borders for the mouse to go is appearently also a problem. So the author's fix is pretty simple, I could understand this without looking it up.

pythonif new_x < 0:
    new_x = 0
elif new_x + label_width > canvas_width:
    new_x = canvas_width - label_width    ... 

SO its saying that if the logo tries to go past the left edge (below 0), put it back to 0. SAme thing with right. Mouse can go anywhere but logo just snaps back into place.
Same rules follow up after this with up and down as well.
