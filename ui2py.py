import os

'''
【脚本功能】：自动将.ui文件同步转化更新为.py文件

1、遍历ui_files中所有.ui文件
检查该.ui文件是否已经生成相应的.py文件
    若没有相应的.py，则生成.py
    若已经存在，则对比.ui和.py的文件【修改时间】
        若.ui修改时间 新于 .py修改时间，则执行命令更新.py
        否则 .ui修改时间 不新于 .py修改时间，则忽略此.py的更新

'''


def updateUi2Py(__pyuic_exe_path, __ui_files_path):
    fileList = os.listdir(__ui_files_path)

    # 字典（哈希表）—— [ui文件名 : py文件名]
    ui_py_hash = {}

    # 统计所有.ui文件，并记录下来
    for file_name in fileList:
        if file_name.endswith('.ui'):
            ui_py_hash[file_name] = ''

    # 统计所有的.py文件，如果有对应的.ui文件，就加到哈希表中
    for file_name in fileList:
        if file_name.endswith('.py'):
            # 获取文件名（无后缀）
            file_name_without_suffix = os.path.splitext(file_name)[0]
            # 将.py文件加到哈希表的对应.ui中去
            ui_file_name = file_name_without_suffix[:-3] + '.ui'
            if ui_file_name in ui_py_hash:
                ui_py_hash[ui_file_name] = str(file_name_without_suffix + '.py')

    # 至此，已经统计完所有的[ui文件名 : py文件名]

    for ui_py_item in ui_py_hash.items():
        # 取ui绝对路径名
        ui_file_full_path = __ui_files_path + '\\' + ui_py_item[0]
        py_file_full_path = __ui_files_path + '\\' + ui_py_item[1]

        # 取ui文件名（不带后缀）
        file_name_without_suffix = os.path.splitext(ui_py_item[0])[0]

        # 若【没有相应的.py】 或 【ui文件已经发生更新】则运行pyuic命令更新.py
        if ui_py_item[1] == '' or os.path.getmtime(ui_file_full_path) > os.path.getmtime(py_file_full_path):
            cmds = list()

            # d:
            cmds.append(__pyuic_exe_path[0].lower() + ':')

            # cd D:\\ProgramData\\Miniconda3\\envs\pytorch37\\Scripts
            cmds.append('cd ' + os.path.dirname(os.path.abspath(__pyuic_exe_path)))

            # pyuic5 xxx.ui -o xxx_ui.py
            cmds.append('pyuic5 ' + __ui_files_path + '\\' + ui_py_item[0] \
                        + ' -o ' + __ui_files_path + '\\' + file_name_without_suffix + '_ui.py')

            # 执行以上的命令组合
            print(' && '.join(cmds))
            os.system(' && '.join(cmds))


    # 先更新.ui自动转.py文件
ui_files_path = 'C:\\Users\\jeffe\\Desktop\\pyqtproject\\ui_files'
pyuic_exe_path = 'D:\\Anocanda3\\Scripts\\pyuic5.exe'
updateUi2Py(pyuic_exe_path, ui_files_path)

# 后续再导入ui文件，确保_ui.py文件是最新的
