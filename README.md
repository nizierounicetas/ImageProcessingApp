# ImageProcessingApp
A GUI application, developed in Python, that processes chosen images with nonlinear filters based on ordinal statistics(maximum filter, mimimum filter, median filter) and contrast enhancement techniques(linear contrast and histogram equalization). Developed as part of the third laboratory work on the discipline Computer Graphics.

![image](https://user-images.githubusercontent.com/79499100/229625644-0c6adaa9-4c02-4c75-a7a5-28b2f09e00aa.png)

## build and run
- To run with Python interpreter open CMD in root project folder and run: ```python main.py``` (make sure that the interpreter is added to the environment variables)
- To build and run executable file you need:
  - install <b>pyinstaller</b>: ```pip install pyinstaller```
  - open CMD in root folder and run: ```pyinstaller --windowed -F --add-data "pics/image.ico;pics" --icon=pics/image.ico -d bootloader main.py --name image_processing --onefile``` in Windows or ```pyinstaller --windowed -F --add-data "pics/image.ico:pics" --icon=pics/image.ico -d bootloader main.py --name image_processing --onefile``` in Unix systems
  - after that you can find one-file executable <b>image_processing</b> in <b>dist</b> folder and excecute it.
  
  You can also find executable <b>image_processing</b> in <b>Release</b>.
  
  
