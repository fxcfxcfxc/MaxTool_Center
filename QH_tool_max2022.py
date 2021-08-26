from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import qtmax
from pymxs import runtime as rt

import os

def make_editpoly():
    rt.convertToPoly(rt.selection)

    return


def make_material():
    a = rt.selection
    m = rt.standardMaterial()
    for x in a :
        x.material = m

    return 



def clear_material():

    for obj in rt.selection:
        obj.material = rt.undefined


def open_uv():
    a = rt.selection
    uv = rt.Unwrap_UVW()
    for x in a :
        rt.addModifier(x,uv)

    uv.edit()
    
        







class PyMaxDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('启虹游戏工具盒')
        self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def select_path(self):
        directory = os.path.dirname(self.selectpath_btn.text())
        if not os.path.exists(directory):
                directory = ''

        
        output_path = QtWidgets.QFileDialog.getExistingDirectory(dir=directory)

        output_path =  output_path +"\\"+"12"+".fbx"

        self.selectpath_btn.setText(output_path)

    def export_fbx (self):

        path = self.selectpath_btn.text()

        rt.exportFile(path,rt.name('noPrompt'),selectedOnly=True,using=rt.FBXEXP)

    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("多边形")
        main_layout.addWidget(label)

        editpoly_btn = QtWidgets.QPushButton("塌陷并转换为Editpoly")
        editpoly_btn.clicked.connect(make_editpoly)
        main_layout.addWidget(editpoly_btn)

        #
        label_m = QtWidgets.QLabel("材质")
        main_layout.addWidget(label_m)

        material_btn = QtWidgets.QPushButton("快速赋予材质")
        material_btn.clicked.connect(make_material)
        main_layout.addWidget(material_btn)

        materialclear_btn = QtWidgets.QPushButton("清除选择物体材质")
        materialclear_btn.clicked.connect(clear_material)
        main_layout.addWidget(materialclear_btn)
        #
        label2 = QtWidgets.QLabel("修改器")
        main_layout.addWidget(label2)

        uv_btn = QtWidgets.QPushButton("UV")
        uv_btn.clicked.connect(open_uv)
        main_layout.addWidget(uv_btn)
        #
        label3 = QtWidgets.QLabel("导出")
        main_layout.addWidget(label3)


        #
        self.selectpath_btn = QtWidgets.QPushButton("........")
        self.selectpath_btn.clicked.connect(self.select_path)
        main_layout.addWidget(self.selectpath_btn)

        self.selectpath_btn = QtWidgets.QLineEdit()
        main_layout.addWidget(self.selectpath_btn)

        export_btn = QtWidgets.QPushButton("导出选择")
        export_btn.clicked.connect(self.export_fbx)
        main_layout.addWidget(export_btn)


        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setWidget(widget)
        self.resize(250, 200)

def main():
    
    main_window = qtmax.GetQMaxMainWindow()
    w = PyMaxDockWidget(parent=main_window)
    w.setFloating(True)
    w.show()

if __name__ == '__main__':
    main()