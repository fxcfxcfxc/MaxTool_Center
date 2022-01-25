
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import qtmax
from pymxs import runtime as rt
import os
import pymxs
'''
开发环境：
    max2022版本以上，使用自己的包开头必须将项目目录添加到环境变量中
    pymxs+pyside2
'''

class PyMaxDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('模型组工具')
        self.initUI()
        #self.creat_widgets()
        #self.creat_layout()
        #self.creat_connect()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)



    def select_path(self):
        directory = os.path.dirname(self.path_line.text())
        if not os.path.exists(directory):
            directory = ''
        output_path = QtWidgets.QFileDialog.getExistingDirectory(dir=directory)
        output_path = output_path
        self.path_line.setText(output_path)

    def export_fbx(self):
        old_path = self.path_line.text()
        new_path = old_path + '/'
        name = self.name_line.text()
        rt.exportFile(new_path + name, rt.name('noPrompt'), selectedOnly=True, using=rt.FBXEXP)

    def export_obj(self):
        path = self.path_line.text()
        name = self.name_line.text()
        rt.exportFile(path + name, rt.name('noPrompt'), selectedOnly=True, using=rt.ObjExp)

    def import_fast(self):
        rt.execute('max file import')

    def cencter_select(self):
        with pymxs.undo(True):
            rt.CenterPivot(rt.selection)

    def world_select(self):
        with pymxs.undo(True):
            s = rt.selection
            for x in s:
                rt.setProperty(x, "pos.x", 0.0)
                rt.setProperty(x, "pos.y", 0.0)
                rt.setProperty(x, "pos.z", 0.0)
            rt.redrawViews()

    def bake(self):

        rt.execute('actionMan.executeAction 1858480148 "23214332"')

    def smmothing(self):
        with pymxs.undo(True):
            rt.execute('$.EditablePoly.ConvertSelection #Face #Edge')
            rt.execute('$.EditablePoly.makeSmoothEdges 1')
            rt.execute('$.EditablePoly.ConvertSelectionToBorder #Face #Edge')
            rt.execute('$.EditablePoly.makeHardEdges 1')

        # pymxs metond
        # getDollarSel = getattr(rt, '%getDollarSel')
        # rt.polyop.getFaceSelection(getDollarSel())
        # getDollarSel().makeSmoothEdges(1)
        # getDollarSel().convertSelectionToBorder(rt.name('Face'),rt.name('Edge'))
        # getDollarSel().makeHardEdges(1)

    def smmothing_makeplane(self):
        with pymxs.undo(True):
            rt.execute('$.EditablePoly.ConvertSelection #Face #Edge')
            rt.execute('$.EditablePoly.makeSmoothEdges 1')
            rt.execute('$.EditablePoly.ConvertSelectionToBorder #Face #Edge')
            rt.execute('$.EditablePoly.makeHardEdges 1')
            rt.execute('$.EditablePoly.makePlanar #Face')

    def remove(self):
        with pymxs.undo(True):
            rt.execute('$.EditablePoly.Remove ()')

    def make_editpoly(self):
        rt.convertToPoly(rt.selection)
        return

    def layer_high(self):
        with pymxs.undo(True):
            rt.execute('a = LayerManager.newLayer()')
            rt.execute('a.current = true')
            rt.execute('a.addnodes $')
            rt.execute('a.setname "high"')

    def layer_low(self):
        with pymxs.undo(True):
            rt.execute('a = LayerManager.newLayer()')
            rt.execute('a.current = true')
            rt.execute('a.addnodes $')
            rt.execute('a.setname "low"')

    def resert(self):
        a = rt.selection
        for x in a:
            rt.ResetXForm(x)
            rt.convertToPoly(x)

    def creat_plane(self):
        with pymxs.undo(True):
            a = rt.plane()
            a.lengthsegs = 1
            a.widthsegs = 1
            rt.redrawViews()

    def creat_box(self):
        with pymxs.undo(True):
            a = rt.box()
            rt.redrawViews()

    def creat_cylinder(self):
        with pymxs.undo(True):
            a = rt.cylinder()
            a.sides = 12
            rt.redrawViews()

    def creat_sphere(self):
        with pymxs.undo(True):
            a = rt.sphere()
            a.segs = 12
            rt.redrawViews()

    def detel_layer(self):
        a = rt.LayerManager.count
        list = []
        for x in range(a):
            layer = rt.LayerManager.getLayer(x)
            if layer.canDelete():
                list.append(layer.name)

        for x in list:
            rt.LayerManager.deleteLayerByName(x)

    def cut(self):
        with pymxs.undo(True):
            if list(rt.selection) == []:
                print("0")
            else:
                rt.setCommandPanelTaskMode(rt.name('modify'))
                rt.execute('macros.run "Ribbon - Modeling" "CutsCut"')

    def inset(self):
        with pymxs.undo(True):
            rt.execute('macros.run "Ribbon - Modeling" "EPoly_Inset"')

    def bevel(self):
        with pymxs.undo(True):
            rt.execute('macros.run "Ribbon - Modeling" "EPoly_Bevel"')

    def swiftloop(self):
        with pymxs.undo(True):
            rt.execute('macros.run "PolyTools" "swiftloop"')

    def targetweld(self):
        with pymxs.undo(True):
            rt.execute('macros.run "Editable Polygon Object" "EPoly_TargetWeld"')

    def collapse(self):
        with pymxs.undo(True):
            rt.execute('macros.run "Ribbon - Modeling" "GeometryCollapse"')

    def make_material(self):
        with pymxs.undo(True):
            a = rt.selection
            m = rt.ai_Standard_Surface()
            for x in a:
                x.material = m
            rt.redrawViews()  # 视图更新

        return

    def layer_material(self):
        with pymxs.undo(True):
            a = rt.selection
            for x in a:
                m = rt.ai_Standard_Surface()
                m.name = x.name
                x.material = m
            rt.redrawViews()  # 视图更新
        return

    def clear_material(self):
        with pymxs.undo(True):
            for obj in rt.selection:
                obj.material = rt.undefined
            rt.redrawViews()

    def open_uv(self):
        a = rt.selection
        uv = rt.Unwrap_UVW()
        for x in a:
            rt.addModifier(x, uv)

        rt.setCommandPanelTaskMode(rt.name('create'))
        rt.setCommandPanelTaskMode(rt.name('modify'))
        uv.edit()

    def add_vertexpaint_mod(self):
        a = rt.selection
        uv = rt.VertexPaint()
        for x in a:
            rt.addModifier(x, uv)
        rt.redrawViews()

    def fbx_setting(self):
        rt.OpenFbxSetting()

    def show_channle_r(self):
        with pymxs.undo(True):
            for obj in rt.selection:
                obj.material.k_test = 1.0
            v = rt.VertexPaintTool()
            v.paintColor = rt.color(255, 0, 0)
            rt.redrawViews()

    def show_channle_g(self):
        with pymxs.undo(True):
            for obj in rt.selection:
                obj.material.k_test = 2.0

            v = rt.VertexPaintTool()
            v.paintColor = rt.color(0, 255, 0)
            rt.redrawViews()

    def show_channle_b(self):
        with pymxs.undo(True):
            for obj in rt.selection:
                obj.material.k_test = 3.0
            v = rt.VertexPaintTool()
            v.paintColor = rt.color(0, 0, 255)
            rt.redrawViews()
            rt.redrawViews()

    def show_channle_a(self):
        with pymxs.undo(True):
            for obj in rt.selection:
                obj.material.k_test = 4.0
            rt.redrawViews()

    def show_channle_shader(self):
        with pymxs.undo(True):
            for obj in rt.selection:
                obj.material.k_test = 0.0
            rt.redrawViews()

    def save_select(self):
        maxfile_name = rt.maxFileName
        maxfile_path = rt.maxFilePath
        print(maxfile_path + maxfile_name)
        select_maxfile = maxfile_name.replace('.max', '')  # replace方法来进行字符串的删除
        rt.saveNodes(rt.selection,maxfile_path + select_maxfile + "_select.max")
        os.startfile(maxfile_path)


    def save_backup(self):
        maxfile_name = rt.maxFileName
        maxfile_path = rt.maxFilePath
        print(maxfile_path+maxfile_name)
        backup_maxfile = maxfile_name.replace('.max','') #replace方法来进行字符串的删除
        rt.saveMaxFile(maxfile_path + backup_maxfile + "_backup.max",useNewFile = False)#传入参数false来防止max保存

    def open_maxfile_dir(self):
        maxfile_path = rt.maxFilePath
        os.startfile(maxfile_path)




    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout()

        open_maxfile_but = QtWidgets.QPushButton("打开项目文件夹")
        open_maxfile_but.clicked.connect(self.open_maxfile_dir)
        main_layout.addWidget(open_maxfile_but)

        save_backup_but = QtWidgets.QPushButton('同目录保存备份_backup.max')
        save_backup_but.clicked.connect(self.save_backup)
        main_layout.addWidget(save_backup_but)

        save_select_maxfile_but = QtWidgets.QPushButton("保存选中模型为_select.max")
        save_select_maxfile_but.clicked.connect(self.save_select)
        main_layout.addWidget(save_select_maxfile_but)

        vertexpaint2 = QtWidgets.QPushButton('vertexpaint打开顶点绘画')
        vertexpaint2.clicked.connect(self.add_vertexpaint_mod)
        main_layout.addWidget(vertexpaint2)

        radioZ = QtWidgets.QRadioButton('光照结果')
        radioZ.toggled.connect(self.show_channle_shader)
        main_layout.addWidget(radioZ)

        radioR = QtWidgets.QRadioButton('R通道')
        radioR.toggled.connect(self.show_channle_r)
        main_layout.addWidget(radioR)

        radioG = QtWidgets.QRadioButton('G通道')
        radioG.toggled.connect(self.show_channle_g)
        main_layout.addWidget(radioG)

        radioB = QtWidgets.QRadioButton('B通道')
        radioB.toggled.connect(self.show_channle_b)
        main_layout.addWidget(radioB)

        radioA = QtWidgets.QRadioButton('A通道')
        radioA.toggled.connect(self.show_channle_a)
        main_layout.addWidget(radioA)

        label_Creat = QtWidgets.QLabel("Creat-创建基本体Maya模式")
        main_layout.addWidget(label_Creat)
        #
        plane_layout = QtWidgets.QHBoxLayout()
        plane_btn = QtWidgets.QPushButton("plane")
        plane_btn.clicked.connect(self.creat_plane)
        plane_layout.addWidget(plane_btn)

        box_btn = QtWidgets.QPushButton("box")
        box_btn.clicked.connect(self.creat_box)
        plane_layout.addWidget(box_btn)

        main_layout.addLayout(plane_layout)
        #
        sphere_layout = QtWidgets.QHBoxLayout()
        sphere_btn = QtWidgets.QPushButton("sphere")
        sphere_btn.clicked.connect(self.creat_sphere)
        sphere_layout.addWidget(sphere_btn)

        cylinder_btn = QtWidgets.QPushButton("cylinder")
        cylinder_btn.clicked.connect(self.creat_cylinder)
        sphere_layout.addWidget(cylinder_btn)

        main_layout.addLayout(sphere_layout)
        #
        label = QtWidgets.QLabel("Mesh-物体")
        main_layout.addWidget(label)

        editpoly_btn = QtWidgets.QPushButton("Editablepoly")
        editpoly_btn.clicked.connect(self.make_editpoly)
        main_layout.addWidget(editpoly_btn)

        resert_btn = QtWidgets.QPushButton("Resert xform")
        resert_btn.clicked.connect(self.resert)
        main_layout.addWidget(resert_btn)

        label_m = QtWidgets.QLabel("Modeling-建模")
        main_layout.addWidget(label_m)

        remove_btn = QtWidgets.QPushButton("Remove")
        remove_btn.clicked.connect(self.remove)
        main_layout.addWidget(remove_btn)

        cut_btn = QtWidgets.QPushButton("Cut")
        cut_btn.clicked.connect(self.cut)
        main_layout.addWidget(cut_btn)

        inset_btn = QtWidgets.QPushButton("inset")
        inset_btn.clicked.connect(self.inset)
        main_layout.addWidget(inset_btn)

        Bevel_btn = QtWidgets.QPushButton("bevel")
        Bevel_btn.clicked.connect(self.bevel)
        main_layout.addWidget(Bevel_btn)

        SwiftLoop_btn = QtWidgets.QPushButton("EdgeLoop")
        SwiftLoop_btn.clicked.connect(self.swiftloop)
        main_layout.addWidget(SwiftLoop_btn)

        TargetWeld_btn = QtWidgets.QPushButton("targetweld")
        TargetWeld_btn.clicked.connect(self.targetweld)
        main_layout.addWidget(TargetWeld_btn)

        Collapse_btn = QtWidgets.QPushButton("collapse")
        Collapse_btn.clicked.connect(self.collapse)
        main_layout.addWidget(Collapse_btn)

        Tr_label = QtWidgets.QLabel("Pivot-轴")
        main_layout.addWidget(Tr_label)

        bt_cenceterObj = QtWidgets.QPushButton(" To Center")
        bt_cenceterObj.clicked.connect(self.cencter_select)
        main_layout.addWidget(bt_cenceterObj)

        bt_world = QtWidgets.QPushButton("To world[0,0,0]")
        bt_world.clicked.connect(self.world_select)
        main_layout.addWidget(bt_world)

        smoothing_lb = QtWidgets.QLabel("Smoothing-光滑组")
        main_layout.addWidget(smoothing_lb)

        smoothing_btn = QtWidgets.QPushButton("一键光滑组")
        smoothing_btn.clicked.connect(self.smmothing)
        main_layout.addWidget(smoothing_btn)

        smoothing_plane_btn = QtWidgets.QPushButton("打平面+光滑组")
        smoothing_plane_btn.clicked.connect(self.smmothing_makeplane)
        main_layout.addWidget(smoothing_plane_btn)

        #
        label_m = QtWidgets.QLabel("Material-材质")
        main_layout.addWidget(label_m)

        material_btn = QtWidgets.QPushButton("统一材质")
        material_btn.clicked.connect(self.make_material)
        main_layout.addWidget(material_btn)

        layermaterial_btn = QtWidgets.QPushButton("多个材质(自动匹配物体名称)")
        layermaterial_btn.clicked.connect(self.layer_material)
        main_layout.addWidget(layermaterial_btn)

        materialclear_btn = QtWidgets.QPushButton("清除选择物体材质")
        materialclear_btn.clicked.connect(self.clear_material)
        main_layout.addWidget(materialclear_btn)
        #
        label2 = QtWidgets.QLabel("Modifter-修改器")
        main_layout.addWidget(label2)

        uv_btn = QtWidgets.QPushButton("UV")
        uv_btn.clicked.connect(self.open_uv)
        main_layout.addWidget(uv_btn)

        label_bake = QtWidgets.QLabel("Bake-烘培")
        main_layout.addWidget(label_bake)

        bt_bake = QtWidgets.QPushButton('烘培')
        bt_bake.clicked.connect(self.bake)
        main_layout.addWidget(bt_bake)
        #
        label3 = QtWidgets.QLabel("Export-导出")
        main_layout.addWidget(label3)

        self.fbxsetting_btn = QtWidgets.QPushButton("FBX输出设置........")
        self.fbxsetting_btn.clicked.connect(self.fbx_setting)
        main_layout.addWidget(self.fbxsetting_btn)
        #
        self.main_layout2 = QtWidgets.QHBoxLayout()
        self.selectpath_btn = QtWidgets.QPushButton("选择路径........")
        self.selectpath_btn.clicked.connect(self.select_path)
        main_layout.addWidget(self.selectpath_btn)
        #
        self.path_line = QtWidgets.QLineEdit()
        self.main_layout2.addWidget(self.path_line)
        self.name_line = QtWidgets.QLineEdit()
        self.main_layout2.addWidget(self.name_line)
        #
        self.main_layout2.setStretch(0, 3)
        self.main_layout2.setStretch(1, 1)

        main_layout.addLayout(self.main_layout2)

        export_btn = QtWidgets.QPushButton("导出FBX")
        export_btn.clicked.connect(self.export_fbx)
        main_layout.addWidget(export_btn)
        export_btn2 = QtWidgets.QPushButton("导出OBJ")
        export_btn2.clicked.connect(self.export_obj)
        main_layout.addWidget(export_btn2)

        label_import = QtWidgets.QLabel("Import-导入")
        main_layout.addWidget(label_import)

        bt_import = QtWidgets.QPushButton('导入')
        bt_import.clicked.connect(self.import_fast)
        main_layout.addWidget(bt_import)

        label_layer = QtWidgets.QLabel("Layer-图层")
        main_layout.addWidget(label_layer)

        layerscence_layout = QtWidgets.QHBoxLayout()
        bt_high = QtWidgets.QPushButton('High_layer')
        bt_high.clicked.connect(self.layer_high)
        layerscence_layout.addWidget(bt_high)

        bt_low = QtWidgets.QPushButton('low_layer')
        bt_low.clicked.connect(self.layer_low)
        layerscence_layout.addWidget(bt_low)

        main_layout.addLayout(layerscence_layout)

        del_low = QtWidgets.QPushButton('clean empty layer')
        del_low.clicked.connect(self.detel_layer)
        main_layout.addWidget(del_low)

        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setWidget(widget)
        self.resize(250, 600)


def main():
    main_window = qtmax.GetQMaxMainWindow()
    w = PyMaxDockWidget(parent=main_window)
    w.setFloating(True)
    w.show()


if __name__ == '__main__':
    main()