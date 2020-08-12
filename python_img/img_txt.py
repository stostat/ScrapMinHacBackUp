from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
import re 


PDF_file = "filename.pdf"

# Almacenar todas las páginas del PDF en una variable
pages = convert_from_path(PDF_file, 500) 
  
# contador para el numero de paginas 
image_counter = 1
  
# loop que itera sobre el total de paginas 
for page in pages: 
  
    filename = "page_"+str(image_counter)+".jpg"
       
    page.save(filename, 'JPEG') 
   
    image_counter = image_counter + 1


# var que obtiene el total de o numero de imgs 
filelimit = image_counter-1
  
# output .txt 
outfile = "out_text.txt"
  
f = open(outfile, "a") 
  
# iteramos sobre el total de num pages 
for i in range(1, filelimit + 1): 
    #se genera los jpgs
    filename = "page_"+str(i)+".jpg"
          
    # usamos pytesserct 
    text = str(((pytesseract.image_to_string(Image.open(filename))))) 
  
    text = text.replace('-\n', '')     
  
    # escribimos en el file 
    f.write(text) 
  
# cerramos el archivo 
f.close()
