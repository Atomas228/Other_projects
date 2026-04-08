from tkinter import *
from tkinter import filedialog, font
from tkmacosx import Button
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pillow_heif
#colors and fonts
background = '#EEEEEE'
text_fg = '#777C6D'
btn = '#CBCBCB'
btn_txt = '#777C6D'
font_main = ("Arial", 20, "bold")
font_small = ("Arial",17,"bold")
font_smallest = ("Arial", 15, "bold")

window = Tk()
window.title("Image watermarker")
window.minsize(width=300, height=300)
window.config(bg=background)
image_label = Label(window)
max_width = 700
original_img = None

class Watermark():
    def __init__(self):
        super().__init__()
        #default values for the watermark
        self.alpha = 255
        self.wtm_x = 100
        self.wtm_y = 100
        self.final_img = None
        self.boldornot = ""
        self.italicornot = ""
        self.bold_state = IntVar()
        self.italic_state = IntVar()
        self.fontstyle = "Arial"
    def action(self):
        #opens up the image and takes it to the 1st column
        #with all the buttons and other things to other columns on the right
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        pillow_heif.register_heif_opener()
        if file_path:
            img = Image.open(file_path)
            #remove the first label and button
            missing_img.place_forget()
            add_img_btn.place_forget()
            #resize the window accordingly to the image size
            #but width of the image not bigger than 700px
            if img.width > max_width:
                ratio = max_width/img.width
                new_width = max_width
                new_height = int(img.height * ratio)
                img = img.resize((new_width,new_height))
            else:
                new_width, new_height = img.width, img.height
            #puts the image on the 1st column
            tk_img = ImageTk.PhotoImage(img)
            self.original_img = img
            image_label.config(image=tk_img)
            image_label.image = tk_img
            image_label.grid(row=0,column=0,rowspan=11, sticky="n", padx=(0,30))
            #puts the text and other scales, spinboxes and texts on the other columns
            text_pointing = Label(text="Click on the image\nwhere you want to put the watermark", bg=background, bd=0)
            text_pointing.config(fg=text_fg, font=("Arial", 17))
            text_pointing.grid(row=0,column=1, columnspan=3, pady=(20,0))
            text_label = Label(text="Text to watermark", bg=background, bd=0)
            text_label.config(fg=text_fg, font=font_main)
            text_label.grid(row=1,column=1, columnspan=3, pady=(10,0))
            self.text = Text(height=2, width=20, bg=btn, highlightthickness=1, highlightbackground=btn_txt)
            self.text.config(font=font_small)
            self.text.grid(row=2,column=1, columnspan=3, pady=(0,20))
            self.scale = Scale(from_=1, to=100, bg=btn, command=self.transparency_scale)
            self.scale.grid(row=4,column=1, pady=(0,20))
            self.scale.config(font=font_small)
            scale_label = Label(text="Transparency", bg=background, bd=0)
            scale_label.config(fg=text_fg, font=font_main)
            scale_label.grid(row=3,column=1,pady=(20,0))
            self.text_size = Scale(from_=5, to=150, bg=btn)
            self.text_size.grid(row=4,column=3,pady=(0,20))
            self.text_size.config(font=font_small)
            size_label = Label(text="Size", bg=background, bd=0)
            size_label.config(fg=text_fg, font=font_main)
            size_label.grid(row=3,column=3,pady=(20,0))
            #rgb values for the watermark color
            color_label = Label(text="Color (RGB)", bg=background, bd=0)
            color_label.config(fg=text_fg, font=font_main)
            color_label.grid(row=5,column=1,columnspan=3, pady=(20,0))
            r_label = Label(text="R", bg=background, bd=0)
            r_label.config(fg=text_fg, font=font_smallest)
            r_label.grid(row=6,column=1)
            self.r_spinbox = Spinbox(from_=0, to=255, width=4, bg=btn, highlightbackground=background)
            self.r_spinbox.grid(row=7, column=1, padx=20)
            self.r_spinbox.config(font=font_small)
            g_label = Label(text="G", bg=background, bd=0)
            g_label.config(fg=text_fg, font=font_smallest)
            g_label.grid(row=6,column=2)
            self.g_spinbox = Spinbox(from_=0, to=255, width=4, bg=btn, highlightbackground=background)
            self.g_spinbox.grid(row=7, column=2, padx=20)
            self.g_spinbox.config(font=font_small)
            b_label = Label(text="B", bg=background, bd=0)
            b_label.config(fg=text_fg, font=font_smallest)
            b_label.grid(row=6,column=3)
            self.b_spinbox = Spinbox(from_=0, to=255, width=4, bg=btn, highlightbackground=background)
            self.b_spinbox.grid(row=7, column=3, padx=20)
            self.b_spinbox.config(font=font_small)
            #checkbutton for text being bold or/and italic
            boldcheckbutton = Checkbutton(text="Bold", variable=self.bold_state, fg=text_fg, bg=background)
            boldcheckbutton.grid(row=8, column=1, pady=(20,0))
            boldcheckbutton.config(font=font_small)
            italiccheckbutton = Checkbutton(text="Italic", variable=self.italic_state, fg=text_fg, bg=background)
            italiccheckbutton.grid(row=8, column=3, pady=(20,0))
            italiccheckbutton.config(font=("Arial",17,"italic"))
            #listbox for all the available fonts in the font family
            listbox_label = Label(text="Font Style", bg=background, bd=0)
            listbox_label.config(fg=text_fg, font=font_main)
            listbox_label.grid(row=8,column=2, pady=(20,0))
            self.listbox = Listbox(height=4)
            #check the working fonts and make them into a list
            fonts = list(self.working_fonts())
            #for every font that is working insert it into the listbox
            for item in fonts:
                self.listbox.insert(fonts.index(item), item)
            self.listbox.config(font=font_smallest, fg=text_fg, bg=btn)
            self.listbox.grid(row=9, column=2, pady=(0,10), padx=10)
            #button to watermark the image
            wtm_btn = Button(text="Watermark", command=self.watermark, bg=btn, borderless = True)
            wtm_btn.config(fg=btn_txt, font=font_small)
            wtm_btn.grid(row=10,column=1, pady=20)
            #button to save the image
            img_save = Button(text="Save Image", command = self.image_saver, bg=btn, borderless = True)
            img_save.config(fg=btn_txt, font=font_small)
            img_save.grid(row=10,column=3, pady=20)
            #update the information of the window and check if the height of the picture is smaller
            # than the height of the other columns and make the window to the height of the
            # other columns
            window.update_idletasks()
            if window.winfo_reqheight() > new_height:
                new_height = window.winfo_reqheight()
            window.geometry(f"{new_width+550}x{new_height}")
    #check the working fonts and append them to a list that is returned
    def working_fonts(self):
        font_dir = "/System/Library/Fonts/Supplemental/"
        good_fonts = []
        for f in font.families():
            try:
                ImageFont.truetype(f"{font_dir}{f}.ttf", 1)
                good_fonts.append(f)
            except OSError:
                pass
        return good_fonts
    
    #watermarking procedure
    def watermark(self):
        #if no image is there then do nothing
        if self.original_img is None:
            return
        #get the text in the right format
        wtm_text = self.text.get("1.0", "end-1c")
        #if no watermark text is there then do nothing
        if not wtm_text:
            return
        #if bold is checked then change the string bold value to have Bold
        if self.bold_state.get() == 1:
            self.boldornot = " Bold"
        #else is added to make the value change when the checkbox is unchecked again
        else:
            self.boldornot = ""
        # same as with the comment before but with italic
        if self.italic_state.get() == 1:
            self.italicornot = " Italic"
        else:
            self.italicornot = ""

        #if there is any value marked in the listbox
        # then set the fontstyle to the value from the listbox
        if self.listbox.curselection():
            self.fontstyle = self.listbox.get(self.listbox.curselection())

        #use a copy of the image instead of the original one
        watermarked_img = self.original_img.copy()
        base = watermarked_img.convert("RGBA")
        txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        try:
            #try to use the font with the current values of bold and italic,
            # but if this font doesnt support the bold or italic then use without them
            font = ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{self.fontstyle}{self.boldornot}{self.italicornot}.ttf",self.text_size.get())
            bbox = draw.textbbox((0, 0), wtm_text, font=font)
        except OSError:
            font = ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{self.fontstyle}.ttf",self.text_size.get())
            bbox = draw.textbbox((0, 0), wtm_text, font=font)
        #check the text width and height to make the picture appear
        # in the center where the click happened exactly
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = self.wtm_x - text_width // 2
        y = self.wtm_y - text_height // 2
        #draw the text where the click happened and use rgb colors and font
        draw.text((x,y),wtm_text,fill=(int(self.r_spinbox.get()),int(self.g_spinbox.get()),int(self.b_spinbox.get()),self.alpha), font=font)
        #try to combine the drawed watermark and the image together into one image
        combined = Image.alpha_composite(base,txt_layer)
        self.final_img = combined.convert("RGB")
        tk_img = ImageTk.PhotoImage(self.final_img)
        #put the edited image into the window on the 1st column
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.bind("<Button-1>", self.set_position)
        image_label.grid(row=0,column=0,rowspan=11, sticky="n", padx=(0,30))
    #returns the value for transparency
    def transparency_scale(self,value):
        self.alpha = int(255-(255*(int(value)/100)))
    #returns the x and y values of the clicked cursor
    def set_position(self, event):
        self.wtm_x = event.x
        self.wtm_y = event.y

    #asks how to save and saves the image
    def image_saver(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Image files", "*.png *.jpg *.jpeg")],
            title="Image save")
        if file_path:
            self.final_img.save(file_path)

watermark = Watermark()
#first text
missing_img = Label(text="Image is missing", bg=background, bd=0)
missing_img.config(fg=text_fg, font=font_main)
missing_img.place(relx=0.5, rely=0.25, anchor="center")

#add image button
add_img_btn = Button(text="Add an Image", command=watermark.action, bg=btn, borderless = True)
add_img_btn.config(fg=btn_txt, font=font_small)
add_img_btn.place(relx=0.5,rely=0.5, anchor="center")

window.mainloop()