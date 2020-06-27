import cv2
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import filedialog,Text
from PIL import Image,ImageTk
import pytesseract
from pytesseract import Output
import tkinter.messagebox

counter = 0
points = []
original = np.zeros((),np.uint8)

# Function definitions
def img_open():
    global original,img
    filename = filedialog.askopenfilename(initialdir = '/Users/NidhiDedhia/', title = 'Select an Image', filetypes = (('JPG','*.jpg'),('All files','*.*')))
    original = cv2.imread(filename)
    img = np.copy(original)
    cv2.namedWindow('Frame')
    cv2.imshow('Frame', original)


def auto_crop():
    global warped,img
    img_gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img_gray, (5,5), 0)
    ret,thresh = cv2.threshold(blur, 190, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5))
    canny = cv2.Canny(thresh,55,200)
    contours,hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    max_contour = contours[max_index]
    perimeter = cv2.arcLength(max_contour, True)
    ROI = cv2.approxPolyDP(max_contour, 0.01 * perimeter, True)
    if len(ROI) == 4:
        p1 = np.array([ROI[1],ROI[0],ROI[2],ROI[3]],np.float32)
        p2 = np.array([(0,0),(600,0),(0,500),(600,500)],np.float32)
        perspective = cv2.getPerspectiveTransform(p1, p2)
        warped = cv2.warpPerspective(original, perspective, (600,500))
        cv2.imshow('Auto Crop', warped)
    img = np.copy(warped)


def manual_crop():
    def click(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x,y))
            copy = np.copy(original)
            cv2.circle(copy, (x,y), 10, (100,38,255),-1)
            cv2.imshow('Frame', copy)
            if len(points) == 4:
                warp()
    def warp():
        global transformed,img
        pts_1 = np.array([points[0], points[1], points[2], points[3]],np.float32)
        pts_2 = np.array([(0, 0), (600, 0), (0, 500), (600, 500)],np.float32)
        perspective = cv2.getPerspectiveTransform(pts_1,pts_2)
        transformed = cv2.warpPerspective(original, perspective, (600,500))
        img = np.copy(transformed)
        cv2.imshow('Manual Crop',transformed)
    cv2.namedWindow('Manual Crop')
    cv2.setMouseCallback('Frame',click)
    

def rotate_clockwise():
    global img
    rot_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow('Rotate', rot_img)
    img = np.copy(rot_img)


def rotate_anticlockwise():
    global img
    rot_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imshow('Rotate', rot_img)
    img = np.copy(rot_img)


def show_original():
    global img
    cv2.imshow('Original', original)
    img = original


def ocr():
    global text,img
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(img_gray, 180, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh,lang= 'eng')
    data = pytesseract.image_to_data(thresh,output_type= Output.DICT)
    no_word = len(data['text'])
    for i in range(no_word):
        if int(data['conf'][i]) > 50:
            x,y,w,h = data['left'][i],data['top'][i],data['width'][i],data['height'][i]
            cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,255,0),1)
            cv2.imshow('OCR',thresh)
            cv2.waitKey(200)
    img = np.copy(thresh)


def show_text():
    global text_frame
    text_frame = Text(textbox, bg = '#e8ebe9')
    text_frame.insert('1.0',text)
    text_frame.pack()


def save_text():
    text_file = open("text.txt", "w")
    n = text_file.write(text)
    text_file.close()
    tk.messagebox.showinfo(title = 'Save Text', message = 'Text file saved')


def save_image():
    global img,counter
    cv2.imwrite('IMG_'+str(counter)+'.jpg', img)
    counter+=1
    tk.messagebox.showinfo(title = 'Save Image', message = 'Image Saved')


def close():
    global text
    msg = tk.messagebox.askquestion(title = 'Close Windows', message = 'This will close all the windows. Are you sure?')
    if msg == 'yes':
        text_frame.delete('1.0',END)
        cv2.destroyAllWindows()



# GUI
root = tk.Tk()
root.title('Imager')

canvas = tk.Canvas(root,height = 700,width = 700,bg = "powder blue")
canvas.pack()

frame = tk.Frame(canvas,bg = "white")
frame.place(relx = 0.48, rely = 0.02, relheight = 0.78, relwidth = 0.5)

textbox = tk.Frame(frame,bg = "#e8ebe9")
textbox.place(relx = 0.10,rely = 0.15,relwidth = 0.8,relheight = 0.65)

label = tk.Label(frame, text = 'Recognized Text', font = ('Times New Roman', '20'), bg = 'white')
label.place(relx = 0.5, rely = 0.09, anchor = 'center')


#Buttons
img_open_btn = tk.Button(canvas, text = 'Open Image', fg = '#2e6bdb', bg ='white', font = ('Sans serif','12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = img_open)
img_open_btn.place(relx = 0.09, rely = 0.07, relwidth = 0.30)

autocrop_btn = tk.Button(canvas, text = 'Auto Crop', fg = '#2e6bdb', bg ='white',font = ('Sans serif','12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = auto_crop)
autocrop_btn.place(relx = 0.05, rely = 0.18, relwidth = 0.18)

manualcrop_btn = tk.Button(canvas, text = 'Manual Crop', fg = '#2e6bdb', bg ='white',font = ('Sans serif','12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = manual_crop)
manualcrop_btn.place(relx = 0.25, rely = 0.18, relwidth = 0.18)

ocr_btn = tk.Button(canvas, text = 'OCR', fg = '#2e6bdb', bg ='white',font = ('Sans serif', '12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = ocr)
ocr_btn.place(relx = 0.09, rely = 0.29, relwidth = 0.30)

show_text_btn = tk.Button(canvas, text = 'Show Text', fg = '#2e6bdb', bg ='white',font = ('Sans serif', '12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = show_text)
show_text_btn.place(relx = 0.09, rely = 0.40, relwidth = 0.30)

clkwise = PhotoImage(file = r"icons/clockwise.png")
sample1 = clkwise.subsample(9,9)
rotate_clk_btn = tk.Button(canvas, text = '  Rotate Clockwise', image = sample1, compound = 'left', fg = '#2e6bdb', bg ='white',font = ('Sans serif','12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = rotate_clockwise)
rotate_clk_btn.place(relx = 0.09, rely = 0.51, relwidth = 0.30)

anticlkwise = PhotoImage(file = r"icons/anticlockwise.png")
sample2 = anticlkwise.subsample(9,9)
rotate_anticlk_btn = tk.Button(canvas, text = '  Rotate Anticlockwise', image = sample2, compound = 'left', fg = '#2e6bdb', bg ='white',font = ('Sans serif','12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = rotate_anticlockwise)
rotate_anticlk_btn.place(relx = 0.09, rely = 0.62, relwidth = 0.30)

save_to_txt = tk.Button(frame, text = 'Save as .txt file', fg = '#2e6bdb', bg ='white',font = ('Sans serif', '12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = save_text)
save_to_txt.place(relx = 0.38, rely = 0.85, relwidth = 0.50)

show_original_img_btn = tk.Button(canvas, text = 'Show Original', fg = '#2e6bdb', bg ='white',font = ('Sans serif', '12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = show_original)
show_original_img_btn.place(relx = 0.09, rely = 0.73, relwidth = 0.30)

save_img_btn = tk.Button(canvas, text = 'Save Image', fg = '#2e6bdb', bg ='white',font = ('Sans serif', '12','bold'),padx = 0, pady = 3, cursor = 'hand2',command = save_image)
save_img_btn.place(relx = 0.52, rely = 0.83, relwidth = 0.42)

close_btn = tk.Button(canvas, text = 'Close', fg = '#db422e', bg ='white',font = ('Sans serif', '12','bold'),padx = 3, pady = 3, cursor = 'hand2', command = close)
close_btn.place(relx = 0.52, rely = 0.9, relwidth = 0.42)

root.mainloop()