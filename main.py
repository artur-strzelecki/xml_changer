from dearpygui.core import *
from dearpygui.simple import *
import os
from xml_changer import xml_changer


class Main:
    def __init__(self):
        self.subfolders = []  # variable with path subfolders
        with window("App"):
            set_theme("Cherry")
            set_main_window_size(660, 700)
            set_main_window_title("XML Changer")
            add_button("Select XML file", callback=self.file_picker, width=150)
            add_same_line()
            add_input_text("##filepath", source="filepath", hint="XML file path", width=350)
            add_same_line()
            add_text("ErrorFile", default_value="XML file not find", color=[237, 69, 103], show=False)
            add_spacing(count=10, name="spacing1")
            add_button("Select folder", callback=self.directory_picker, width=150)
            add_same_line()
            add_input_text("##dirspath", source="dirspath", hint="Folders to change", width=350)
            add_same_line()
            add_text("ErrorPath", default_value="Path not exists", color=[237, 69, 103], show=False)
            add_spacing(count=10, name="spacing1")
            add_button("Select EXE", callback=self.exe_picker, width=150)
            add_same_line()
            add_input_text("##exepath", source="exepath", width=350)
            add_same_line()
            add_spacing(count=20, name="spacing3")
            add_button("Subfolders", callback=self.find_all_subfolers, width=150, height=30)
            add_same_line()
            add_button("Change", callback=self.change, width=150, height=30)
            add_spacing(count=5, name="spacing4")
            start_dearpygui(primary_window="App")

    ''' XML FILE PICKER'''
    def file_picker(self, sender, data):
        open_file_dialog(callback=self.apply_selected_file, extensions=".xml")

    def apply_selected_file(self, sender, data):
        log_debug(data)
        directory = data[0]
        file = data[1]
        set_value("filepath", f"{directory}\\{file}")

    ''' exe picker '''
    def exe_picker(self, sender, data):
        open_file_dialog(callback=self.apply_selected_exe, extensions=".exe")

    def apply_selected_exe(self, sender, data):
        log_debug(data)
        directory = data[0]
        file = data[1]
        set_value("exepath", f"{directory}\\{file}")

    ''' DIR PICKER '''
    def directory_picker(self, sender, data):
        select_directory_dialog(callback=self.apply_selected_directory)

    def apply_selected_directory(self, sender, data):
        log_debug(data)
        directory = data[0]
        folder = data[1]
        set_value("dirspath", f"{directory}\\{folder}")

    ''' find subfolders to path'''
    def find_all_subfolers(self):
        # delete checkbox if exists
        for folder_path in self.subfolders:
            delete_item(os.path.basename(folder_path))

        self.subfolders = []  # clear list
        if does_item_exist("Subfolders_group"):
            delete_item("Subfolders_group")  # delete group

        path = get_value("dirspath")
        configure_item("ErrorPath", show=False)

        # check exists path
        if not os.path.exists(path):
            configure_item("ErrorPath", show=True)
            return

        self.subfolders = [f.path for f in os.scandir(path) if f.is_dir()]  # find all folders in path

        with group("Subfolders_group", parent="App"):
            for folder_path in self.subfolders:
                add_checkbox(os.path.basename(folder_path), default_value=True)  # add folder name to checkbox

    def change(self):
        subfolders_to_change = []
        """ check exists xml file """
        xml_file_path = get_value("filepath")
        configure_item("ErrorFile", show=False)
        if not os.path.isfile(xml_file_path):
            configure_item("ErrorFile", show=True)
            return

        """ check exists exe file """
        exe_path = get_value("exepath")
        exe_exists = True
        if not os.path.isfile(exe_path):
            exe_exists = False

        """ check exists checkbox with path dir"""
        if len(self.subfolders) == 0:
            # delete exists window
            if does_item_exist("Error"):
                delete_item("Error")

            with window("Error", width=200, height=100):
                add_text("Please pick a subfolders!")

            return

        for folder_path in self.subfolders:
            if get_value(os.path.basename(folder_path)) is True:  # get value from checkbox from subfolders button
                subfolders_to_change.append(folder_path)

        if len(subfolders_to_change) > 0:
            # add success window
            if does_item_exist("Success"):
                delete_item("Success")

            with window("Success", width=300, height=100):
                # add progress bar
                add_progress_bar("ProgressBar", default_value=0)
                count = len(subfolders_to_change)
                i = 0
                # change xml in checked subfolders
                for folder_path in subfolders_to_change:
                    i += 1
                    progress_value = i/count
                    xml_changer(xml_file_path, exe_exists, exe_path, folder_path)
                    set_value("ProgressBar", progress_value)

                # delete progress bar and add
                delete_item("ProgressBar")
                add_text("Successful changed XML files! ")

            # clear values
            set_value("filepath", "")
            set_value("dirspath", "")
            set_value("exepath", "")

            for folder_path in self.subfolders:
                delete_item(os.path.basename(folder_path))

            self.subfolders = []


app = Main()





