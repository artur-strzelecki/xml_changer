from xml_diff import xml_diff
import os
import fnmatch
import shutil
from datetime import datetime
from lxml import etree


def xml_changer(main_xml_path, exe_exists, exe_path, folder_path):
    pattern = 'config.xml'  # pattern to find a xml in all folders in path

    # find config.xml in subfolders
    file_xml_path = []  # list with path files xml
    for file in os.scandir(folder_path):
        if fnmatch.fnmatch(file.name, pattern):
            file_xml_path.append(file.path)

    # if we find a file fits to pattern copy it to new filder and change name to config_current_date
    if len(file_xml_path) > 0:

        # create a folder with old version config.xml
        config_old_folder = folder_path + '\\config_old_version'
        if not os.path.exists(config_old_folder):
            os.makedirs(config_old_folder)

        # copy exe file
        if exe_exists is True:
            exe_new = folder_path + '\\' + os.path.basename(exe_path)
            shutil.copy(exe_path, exe_new)

        # copy files to new folder with new name and delete current file
        for xml in file_xml_path:
            new_xml_name = 'config' + datetime.today().strftime('%Y%m%d') + '.xml'
            xml_new = config_old_folder + '\\' + new_xml_name

            # dont check exists file because overwrites old version of this specific file name
            shutil.copy(xml, xml_new)

            new_xml_tree = xml_diff(xml, main_xml_path)
            # remove current file xml
            os.remove(xml)

            if new_xml_tree is not None:
                et = etree.ElementTree(new_xml_tree)
                # add new config.xml with current folder
                with open(xml, 'wb') as f:
                    et.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)
