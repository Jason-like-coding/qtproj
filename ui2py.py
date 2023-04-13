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


class Ui2Py:
    ui_files_path = 'ui_files'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ui_files_path = os.path.join(current_dir, ui_files_path)

    pyuic_exe_path = 'pyuic5'
    # 遍历环境变量 PATH 中的路径
    for path in os.environ['PATH'].split(os.pathsep):
        found = False
        for ext in os.environ['PATHEXT'].split(os.pathsep) if 'PATHEXT' in os.environ else ['']:
            # 拼接路径和命令名称
            full_path = os.path.join(path, pyuic_exe_path + ext)
            if os.path.exists(full_path) and os.access(path, os.X_OK):
                # 获取所在目录
                dir_path = os.path.dirname(full_path)
                print(f'找到 {pyuic_exe_path} 的执行目录为：{dir_path}')
                pyuic_exe_path = os.path.join(dir_path, pyuic_exe_path + ext.lower())
                found = True
                break
        if found:
            break
    else:
        raise FileNotFoundError(
            f'找不到名为 {pyuic_exe_path} 的命令, 请检查环境变量 PATH 中是否包含了该命令的执行目录')

    @classmethod
    def update_ui(cls):
        # 先更新.ui自动转.py文件
        fileList = os.listdir(cls.ui_files_path)

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
            ui_file_full_path = os.path.join(cls.ui_files_path, ui_py_item[0])
            py_file_full_path = os.path.join(cls.ui_files_path, ui_py_item[1])

            # 取ui文件名（不带后缀）
            file_name_without_suffix = os.path.splitext(ui_py_item[0])[0]
            py_file_name = file_name_without_suffix + '_ui.py'

            if ui_py_item[1] != '' and os.path.getmtime(ui_file_full_path) <= os.path.getmtime(py_file_full_path):
                print(f"{py_file_name} already exists and up-to-date")
                continue

            # 若【没有相应的.py】 或 【ui文件已经发生更新】则运行pyuic命令更新.py
            # pyuic5 xxx.ui -o xxx_ui.py
            cmd = (cls.pyuic_exe_path + ' ' + ui_file_full_path + ' -o ' +
                   os.path.join(cls.ui_files_path, py_file_name))

            # 执行以上的命令组合
            print(cmd)
            os.system(cmd)
            print(f"update {py_file_name} success")


if __name__ == '__main__':
    Ui2Py.update_ui()
