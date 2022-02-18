import random
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


#继承QDockWidget类，提供了一种叫做工具面板，它可以是被锁在QMainWindow窗口内部或者是作为顶级窗口悬浮在桌面上
class PyMaxDockWidget(QtWidgets.QDockWidget):
    #传入构造函数参数
    #新式类的写法：super(子类，self).__init__(参数1，参数2，....)
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)#继承父类的构造函数
        self.setWindowFlags(QtCore.Qt.Tool)#将某一子窗口设置为最顶层窗口
        self.setWindowTitle('技术中心_3D组综合工具v1.0')
        self.creat_widgets()
        self.creat_layout()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)#关闭窗口时删掉实例化的类

    def RotatePivotOnly(self, obj, rotation):
        rotValInv = rt.inverse(rt.r2q(rotation))
        with pymxs.animate(False):
            obj.rotation *= rotValInv
            obj.objectoffsetpos *= rotValInv
            obj.objectoffsetrot *= rotValInv

    def select_path(self):
        directory = os.path.dirname(self.path_line.text())
        if not os.path.exists(directory):
            directory = ''
        output_path = QtWidgets.QFileDialog.getExistingDirectory(dir=directory)
        output_path = output_path
        self.path_line.setText(output_path)

    def export_fbx_unity_envir(self):
        rt.execute("fn r2q r = (return r as quat)")
        old_path = self.path_line.text()
        new_path = old_path + '/'
        name = self.name_line.text()

        obj = rt.selection
        rotation = rt.EulerAngles(90, 0, 0)
        if (len(rt.selection)):
            for x in obj:
                mulity_name = "SM_" + x.Name
                posx = rt.getProperty(x,"pos.x")
                posy = rt.getProperty(x,"pos.y")
                posz = rt.getProperty(x,"pos.z")
                rt.setProperty(x, "pos.x", 0.0)
                rt.setProperty(x, "pos.y", 0.0)
                rt.setProperty(x, "pos.z", 0.0)
                self.RotatePivotOnly(x, rotation)
                rt.select(x)
                rt.exportFile(new_path + mulity_name, rt.name('noPrompt'), selectedOnly=True, using=rt.FBXEXP)
                rt.ResetXForm(x)
                rt.convertToPoly(x)
                rt.setProperty(x, "pos.x", posx)
                rt.setProperty(x, "pos.y", posy)
                rt.setProperty(x, "pos.z", posz)

        else:
            rt.messageBox("没有选择物体")

        rt.redrawViews()


    def export_fbx_unity_character(self):
        old_path = self.path_line.text()
        new_path = old_path + '/'
        name = self.name_line.text()

        obj = rt.selection
        rotation = rt.EulerAngles(90, 0, 0)
        rt.execute("fn r2q r = (return r as quat)")
        for x in obj:
            x.pivot = rt.Point3(0, 0, 0)
            self.RotatePivotOnly(x, rotation)

        if(len(rt.selection)):
            if(name != ""):
                rt.exportFile(new_path + name, rt.name('noPrompt'), selectedOnly=True, using=rt.FBXEXP)
            else:rt.messageBox("请输入导出的物体的名字")
        else:
            rt.messageBox("没有选择物体")

    def export_obj(self):
        objpath = self.path_line.text()
        obj_new_path = objpath + '/'
        obj_name = self.name_line.text()

        if(len(rt.selection)):
            rt.exportFile(obj_new_path + obj_name, rt.name('noPrompt'), selectedOnly=True, using=rt.ObjExp)
        else:
            rt.messageBox("没有选择物体")

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

    def one_material(self):
        with pymxs.undo(True):
            a = rt.selection
            m = rt.ai_Standard_Surface()
            for x in a:
                x.material = m
            rt.redrawViews()  # 视图更新

        return

    def mulity_material(self):
        with pymxs.undo(True):
            a = rt.selection
            for x in a:
                m = rt.ai_Standard_Surface()
                m.name = "M_" + x.name
                m.base_color = rt.color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                m.specular = 0.0
                x.material = m
            rt.redrawViews()  # 视图更新
        return

    def clear_material(self):
        with pymxs.undo(True):
            for obj in rt.selection:
                obj.material = rt.undefined
            rt.redrawViews()

    def clear_materialColor(self):
        with pymxs.undo(True):
            for obj in rt.selection:
                obj.material.base_color = rt.color(150,150,150)
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
        rt.setCommandPanelTaskMode(rt.name('create'))
        rt.setCommandPanelTaskMode(rt.name('modify'))
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

    def creat_widgets(self):
        self.lab_maxfile = QtWidgets.QLabel("MaxFile(文件)")
        self.but_open_maxfile = QtWidgets.QPushButton("打开项目文件夹")
        self.but_open_maxfile.clicked.connect(self.open_maxfile_dir)

        self.but_save_backup = QtWidgets.QPushButton('同目录保存备份(_backup.max)')
        self.but_save_backup.clicked.connect(self.save_backup)

        self.but_save_select_maxfile = QtWidgets.QPushButton("保存选中模型为(_select.max)")
        self.but_save_select_maxfile.clicked.connect(self.save_select)

        self.but_open_vertexpaint = QtWidgets.QPushButton('打开顶点绘画')
        self.but_open_vertexpaint.clicked.connect(self.add_vertexpaint_mod)

        self.lab_vertexcolor = QtWidgets.QLabel("VeterColor(顶点绘画)")
        self.radioZ = QtWidgets.QRadioButton('光照结果')
        self.radioZ.toggled.connect(self.show_channle_shader)

        self.radioR = QtWidgets.QRadioButton('R通道')
        self.radioR.toggled.connect(self.show_channle_r)

        self.radioG = QtWidgets.QRadioButton('G通道')
        self.radioG.toggled.connect(self.show_channle_g)

        self.radioB = QtWidgets.QRadioButton('B通道')
        self.radioB.toggled.connect(self.show_channle_b)

        self.radioA = QtWidgets.QRadioButton('A通道')
        self.radioA.toggled.connect(self.show_channle_a)

        self.label_Creat = QtWidgets.QLabel("CreatMaya(Maya模式创建)")
        self.plane_btn = QtWidgets.QPushButton("plane")
        self.plane_btn.clicked.connect(self.creat_plane)

        self.but_creat_box = QtWidgets.QPushButton("box")
        self.but_creat_box.clicked.connect(self.creat_box)

        self.but_creat_sphere = QtWidgets.QPushButton("sphere")
        self.but_creat_sphere.clicked.connect(self.creat_sphere)

        self.but_creat_cylinder = QtWidgets.QPushButton("cylinder")
        self.but_creat_cylinder.clicked.connect(self.creat_cylinder)

        #mesh-物体
        self.poly_label = QtWidgets.QLabel("Mesh(物体)")
        self.editpoly_btn = QtWidgets.QPushButton("Editable_poly(塌陷)")
        self.editpoly_btn.clicked.connect(self.make_editpoly)

        self.resert_btn = QtWidgets.QPushButton("Resert_xform(重置变换)")
        self.resert_btn.clicked.connect(self.resert)

        self.bt_cenceterObj = QtWidgets.QPushButton("坐标轴---》物体中心")
        self.bt_cenceterObj.clicked.connect(self.cencter_select)

        self.bt_world = QtWidgets.QPushButton("物体---》世界中心")
        self.bt_world.clicked.connect(self.world_select)

        #Modeling-建模
        self.label_m = QtWidgets.QLabel("Modeling(建模)")

        self.remove_btn = QtWidgets.QPushButton("Remove")
        self.remove_btn.clicked.connect(self.remove)

        self.cut_btn = QtWidgets.QPushButton("Cut")
        self.cut_btn.clicked.connect(self.cut)

        self.inset_btn = QtWidgets.QPushButton("inset")
        self.inset_btn.clicked.connect(self.inset)

        self.Bevel_btn = QtWidgets.QPushButton("bevel")
        self.Bevel_btn.clicked.connect(self.bevel)

        self.SwiftLoop_btn = QtWidgets.QPushButton("EdgeLoop")
        self.SwiftLoop_btn.clicked.connect(self.swiftloop)

        self.TargetWeld_btn = QtWidgets.QPushButton("targetweld")
        self.TargetWeld_btn.clicked.connect(self.targetweld)

        self.smoothing_lb = QtWidgets.QLabel("Smoothing(光滑组)")

        self.smoothing_btn = QtWidgets.QPushButton("一键光滑组")
        self.smoothing_btn.clicked.connect(self.smmothing)

        self.smoothing_plane_btn = QtWidgets.QPushButton("打平面+光滑组")
        self.smoothing_plane_btn.clicked.connect(self.smmothing_makeplane)

        #Material-材质
        self.label_material = QtWidgets.QLabel("Material(材质)")
        self.but_oneMaterial = QtWidgets.QPushButton("单一材质")
        self.but_oneMaterial.clicked.connect(self.one_material)

        self.but_mulity_material = QtWidgets.QPushButton("复合材质(M_name)")
        self.but_mulity_material.clicked.connect(self.mulity_material)

        self.but_clearn_material = QtWidgets.QPushButton("清除材质")
        self.but_clearn_material.clicked.connect(self.clear_material)

        self.but_clearn_material_diffuse = QtWidgets.QPushButton("清除材质颜色")
        self.but_clearn_material_diffuse.clicked.connect(self.clear_materialColor)

        self.label2 = QtWidgets.QLabel("UV")

        self.uv_btn = QtWidgets.QPushButton("open UV")
        self.uv_btn.clicked.connect(self.open_uv)

        self.label_bake = QtWidgets.QLabel("Bake(烘培)")

        self.bt_bake = QtWidgets.QPushButton('烘培')
        self.bt_bake.clicked.connect(self.bake)

        self.label3 = QtWidgets.QLabel("Export(导出)")

        self.fbxsetting_btn = QtWidgets.QPushButton("FBX输出设置........")
        self.fbxsetting_btn.clicked.connect(self.fbx_setting)

        self.selectpath_btn = QtWidgets.QPushButton("选择路径........")
        self.selectpath_btn.clicked.connect(self.select_path)

        self.path_line = QtWidgets.QLineEdit()
        self.name_line = QtWidgets.QLineEdit()

        self.btn_export_character = QtWidgets.QPushButton("Unity-单FBX-角色(Y上)")
        self.btn_export_character.clicked.connect(self.export_fbx_unity_character)

        self.btn_export_env = QtWidgets.QPushButton("Unity-批量FBX-场景(Y上)")
        self.btn_export_env.clicked.connect(self.export_fbx_unity_envir)


        self.export_btn2 = QtWidgets.QPushButton("导出OBJ")
        self.export_btn2.clicked.connect(self.export_obj)

        self.label_import = QtWidgets.QLabel("Import(导入)")

        self.bt_import = QtWidgets.QPushButton('导入')
        self.bt_import.clicked.connect(self.import_fast)

        self.label_layer = QtWidgets.QLabel("Layer(图层)")

        self.bt_high = QtWidgets.QPushButton('High_layer')
        self.bt_high.clicked.connect(self.layer_high)

        self.bt_low = QtWidgets.QPushButton('low_layer')
        self.bt_low.clicked.connect(self.layer_low)

        self.del_low = QtWidgets.QPushButton('clean empty layer')
        self.del_low.clicked.connect(self.detel_layer)

    def creat_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.lab_maxfile)
        self.main_layout.addWidget(self.but_open_maxfile)
        self.main_layout.addWidget(self.but_save_backup)
        self.main_layout.addWidget(self.but_save_select_maxfile)
        self.main_layout.addWidget(self.lab_vertexcolor)
        self.main_layout.addWidget(self.radioZ)

        self.qhbox_rgba = QtWidgets.QHBoxLayout()
        self.qhbox_rgba.addWidget(self.radioR)
        self.qhbox_rgba.addWidget(self.radioG)
        self.qhbox_rgba.addWidget(self.radioB)
        self.qhbox_rgba.addWidget(self.radioA)
        self.main_layout.addLayout(self.qhbox_rgba)

        self.main_layout.addWidget(self.but_open_vertexpaint)

        self.main_layout.addWidget(self.label_Creat)
        self.plane_layout = QtWidgets.QHBoxLayout()
        self.plane_layout.addWidget(self.plane_btn)
        self.plane_layout.addWidget(self.but_creat_box)
        self.main_layout.addLayout(self.plane_layout)

        self.sphere_layout = QtWidgets.QHBoxLayout()
        self.sphere_layout.addWidget(self.but_creat_sphere)
        self.sphere_layout.addWidget(self.but_creat_cylinder)
        self.main_layout.addLayout(self.sphere_layout)

        self.main_layout.addWidget(self.poly_label)
        self.main_layout.addWidget(self.editpoly_btn)
        self.main_layout.addWidget(self.resert_btn)
        self.main_layout.addWidget(self.bt_cenceterObj)
        self.main_layout.addWidget(self.bt_world)

        self.main_layout.addWidget(self.label_m)
        self.qhbox_modeling_a = QtWidgets.QGridLayout()
        self.qhbox_modeling_a.addWidget(self.remove_btn,0,0)
        self.qhbox_modeling_a.addWidget(self.cut_btn,0,1)
        self.qhbox_modeling_a.addWidget(self.inset_btn,1,0)
        self.qhbox_modeling_a.addWidget(self.Bevel_btn,1,1)
        self.qhbox_modeling_a.addWidget(self.SwiftLoop_btn,2,0)
        self.qhbox_modeling_a.addWidget(self.TargetWeld_btn,2,1)
        self.main_layout.addLayout(self.qhbox_modeling_a)

        self.main_layout.addWidget(self.smoothing_lb)
        self.main_layout.addWidget(self.smoothing_btn)
        self.main_layout.addWidget(self.smoothing_plane_btn)
        self.main_layout.addWidget(self.label_material)

        self.material_hbox_a = QtWidgets.QHBoxLayout()
        self.material_hbox_a.addWidget(self.but_oneMaterial)
        self.material_hbox_a.addWidget(self.but_mulity_material)
        self.main_layout.addLayout(self.material_hbox_a)

        self.material_hbox_b = QtWidgets.QHBoxLayout()
        self.material_hbox_b.addWidget(self.but_clearn_material)
        self.material_hbox_b.addWidget(self.but_clearn_material_diffuse)
        self.main_layout.addLayout(self.material_hbox_b)

        self.main_layout.addWidget(self.label2)
        self.main_layout.addWidget(self.uv_btn)
        self.main_layout.addWidget(self.label_bake)
        self.main_layout.addWidget(self.bt_bake)
        self.main_layout.addWidget(self.label3)
        self.main_layout.addWidget(self.fbxsetting_btn)

        self.main_layout2 = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.selectpath_btn)
        self.main_layout2.addWidget(self.path_line)
        self.main_layout2.addWidget(self.name_line)

        self.main_layout2.setStretch(0, 3)
        self.main_layout2.setStretch(1, 1)

        self.main_layout.addLayout(self.main_layout2)
        self.main_layout.addWidget(self.btn_export_character)
        self.main_layout.addWidget(self.btn_export_env)
        self.main_layout.addWidget(self.export_btn2)
        self.main_layout.addWidget(self.label_import)
        self.main_layout.addWidget(self.bt_import)
        self.main_layout.addWidget(self.label_layer)

        self.layerscence_layout = QtWidgets.QHBoxLayout()
        self.layerscence_layout.addWidget(self.bt_high)
        self.layerscence_layout.addWidget(self.bt_low)
        self.main_layout.addLayout(self.layerscence_layout)

        self.main_layout.addWidget(self.del_low)

        #创建Qwidget顶层类，将布局添加到对象
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.main_layout)
        self.setWidget(self.widget)
        self.resize(300, 600)


if __name__ == '__main__':
    try:
        w.close()
        w.deleteLater()

    except:
        pass
    main_window = qtmax.GetQMaxMainWindow()
    w = PyMaxDockWidget(parent=main_window)
    w.setFloating(True)
    w.setStyleSheet("QLabel { background-color: rgba(53,94,189,1) }")
    w.setStyleSheet("QLabel {font-size:18 px}")

    w.show()