import PythonMagick
import os

'''
Convert pdf to png at 300 dpi
Requires the input, output paths as well as the input file (with extension)
Returns png using the original file name but droppign the ".pdf"
@ Chris 27/02/15
'''

path="O:/Documents/temp/img_to_convert"
inst="Map_difference_fig.pdf"
file="%s/%s" %(path, inst)

opath="O:/Documents/temp/good_imgs"
ofile=os.path.splitext(inst)
ofile="%s.png" %(ofile)

img = PythonMagick.Image()
img.density("300")
img.read(file)
img.write(ofile)