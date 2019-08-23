# ImageToALTOXML
Convert Multiple Images to Multiple ALTo XML Files, Text files, JSON File

Requirements:
============
  1. python 3
  2. Anaconda 3 software (Not mendatory)
     I suggest anaconda 3. Because, It has all the necessary packeges installed in it.
     So, you don't need to install them individually by yourself.
     To know more, visit - https://docs.anaconda.com/anaconda/
  3. Tesseract-OCR 4.1 or greater, visit - https://github.com/UB-Mannheim/tesseract/wiki
  
Installation:
=============
  Python:
  ------
  1. Download or install python3 (I used python 3.7.3) or anaconda3
  2. Add the location of installed folder to the environment path variable (control panel -> System & Security -> System -> 
     Advanced system settings -> Environment variables -> click on PATH -> Edit it by Adding that path (copied) in 'PATH')
     
  Tesseract-OCR:
  -------------
  1. Download and install it from - https://github.com/UB-Mannheim/tesseract/wiki
  2. Add the location of installed folder 'Tesseract-OCR' & 'tessdata' to system path or environment variable
     (paths in my system are - C:\Program Files\Tesseract-OCR
                               C:\Program Files\Tesseract-OCR\tessdata)
  3. An extra thing you need to do. That is after setting environment variable, create a new variable by clicking on 'New'
     (like - control panel -> System & Security -> System -> Advanced system settings -> Environment variables -> Click 'New' Under
     'System variables' -> Name it 'TESSDATA_PREFIX' and give the value C:\Program Files\Tesseract-OCR\tessdata)
     
  Packages:
  ---------
  1. Open CMD (Command Prompt)
  2. download & unzip project from https://github.com/Yadab-Sd/ImageToALTOXML/
  3. type in cmd, "cd <project folder location>
  4. now write "pip instll -r requirements.txt" and press enter to install necessary all packages for this project
     (To install package individually, write - pip install <package_name> ) 
     (You will find all package names with correct syntex from https://pypi.org/)
  
  
  Now, Run main.py by-
  **********************************************************************
  python main.py --input_dir input/ --output_dir output/
  **********************************************************************
  
  - here, input/ and output/ are the input and output locations
  - put all the pictures need to convert text all of them in a single file
  - you can use input/folder1/ or input/folder2/
                               
