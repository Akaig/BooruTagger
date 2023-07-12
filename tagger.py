import sys
import os
import configparser
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtCore import Qt, QStringListModel
from Widgets.previewImage import Preview
from Widgets.previewTags import PreviewTags
from Widgets.Hotkeys import Hotkeys

form_class = uic.loadUiType("Ui/tagger.ui")[0]

class Tagger(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        with open('list.tag', encoding="utf8") as f:
            tags = [x.strip() for x in f]

        string_list_model = QStringListModel()
        string_list_model.setStringList(tags)
        completer = QtWidgets.QCompleter()
        completer.setModel(string_list_model)
        completer.setMaxVisibleItems(5)
        self.image_tag_table.set_completer(completer)
        self.all_images_tags_list.set_completer(completer)
        del(tags)

        self.images_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.open_template_action.triggered.connect(self.open_template)
        self.save_template_action.triggered.connect(self.save_template)
        self.hotkeys_action.triggered.connect(self.handle_hotkeys)
        self.show_preview_action.toggled.connect(self.on_preview_toggled)
        self.show_tag_count_action.toggled.connect(self.on_preview_tag_toggled)
        self.images_list.currentItemChanged.connect(self.update_preview)
        self.addToAllButton.clicked.connect(self.save_all)
        self.removeFromAllButton.clicked.connect(self.remove_all_tags)

        down_shortcut = QtWidgets.QShortcut(QKeySequence("PgDown"), self)
        up_shortcut = QtWidgets.QShortcut(QKeySequence("PgUp"), self)
        down_shortcut.activated.connect(self.select_next)
        up_shortcut.activated.connect(self.select_prev)

        self.insert_shortcut = QtWidgets.QShortcut(self)
        self.delete_shortcut = QtWidgets.QShortcut(self)
        self.copy_shortcut = QtWidgets.QShortcut(self)
        self.insert_below_shortcut = QtWidgets.QShortcut(self)
        self.save_shortcut = QtWidgets.QShortcut(self)
        self.insert_shortcut.activated.connect(self.add_row)
        self.delete_shortcut.activated.connect(self.remove_row)
        self.copy_shortcut.activated.connect(self.add_to_image_tags)
        self.insert_below_shortcut.activated.connect(self.add_row_below_current)
        self.save_shortcut.activated.connect(self.save_individual)

        self.setupHotkeys()
        self.preview = None
        self.preview_tags = None

    def setupHotkeys(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        hotkey = config["hotkeys"]

        self.save_shortcut.setKey(QKeySequence(hotkey["save"]))
        self.delete_shortcut.setKey(QKeySequence(hotkey["delete"]))
        self.copy_shortcut.setKey(QKeySequence(hotkey["add tag to table"]))
        self.insert_shortcut.setKey(QKeySequence(hotkey["add new row"]))
        self.insert_below_shortcut.setKey(QKeySequence(hotkey["add new row below"]))

    def open_template(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        template = QtWidgets.QFileDialog.getOpenFileName(self, "Select a Template", options=options, filter="Template (*.tagger)")
        if template[0]:
            with open(template[0]) as f:
                tags = [x.rstrip() for x in f]
            self.all_images_tags_list.clear()
            self.all_images_tags_list.setRowCount(0)
            for tag in tags:
                row = self.all_images_tags_list.rowCount()
                self.all_images_tags_list.insertRow(row)
                self.all_images_tags_list.setItem(row, 0, QtWidgets.QTableWidgetItem(tag))

    def save_template(self):
        all_tags = self.get_all_tags_table_data()
        template_name = QtWidgets.QFileDialog.getSaveFileName(self, "Save Template", filter="Template (*.tagger)")
        if template_name[0]:
            with open(template_name[0], "w") as f:
                f.write("\n".join(all_tags))
        
    def remove_all_tags(self):
        files = []
        for i in range(self.images_list.count()):
            files.append(f"{self.images_list.item(i).data(Qt.UserRole).rsplit('.', 1)[0]}.txt")
        current_row = self.images_list.currentRow()
        if self.allBelowCheckBox.isChecked():
            files = files[current_row:]
        if self.allAboveCheckBox.isChecked():
            files = files[:current_row+1]
        
        self.remove_from_all(files)

    def save_all(self):
        files = []
        for i in range(self.images_list.count()):
            files.append(f"{self.images_list.item(i).data(Qt.UserRole).rsplit('.', 1)[0]}.txt")
        self.save_unique_tags(files)
        
    def save_unique_tags(self, files_path):
        for file_path in files_path:
            unique_tags = set()
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    for line in file:
                        tags = line.split(",")
                        for tag in tags:
                            tag = tag.strip()
                            if tag != "":
                                unique_tags.add(tag)
            tags = self.get_all_tags_table_data()
            for tag in tags:
                unique_tags.add(tag)

            with open(file_path, "w") as fOut:
                sorted_tags = list(unique_tags)
                sorted_tags.sort()
                fOut.write(", ".join(sorted_tags))

    def add_to_image_tags(self):
        row = self.image_tag_table.rowCount()
        item = self.all_images_tags_list.item(self.all_images_tags_list.currentRow(), 0)
        if item is not None:
            self.image_tag_table.insertRow(row)
            self.image_tag_table.setItem(row, 0, QtWidgets.QTableWidgetItem(item.text()))

    def update_preview(self, current, previous):
        try:
            if current != previous:
                file_path = current.data(Qt.UserRole)
                tag_file_path = f"{file_path.rsplit('.', 1)[0]}.txt"
                if self.show_preview_action.isChecked():
                    if current:
                        if self.preview:
                            self.preview.set_image(file_path)
                        else:
                            self.preview = Preview(file_path, self.show_preview_action)
                            self.preview.show()

                if os.path.isfile(tag_file_path):
                    self.image_tag_table.clear()
                    self.image_tag_table.setRowCount(0)
                    with open(tag_file_path) as f:
                        for line in f:
                            tags = line.split(",")
                            for tag in tags:
                                row = self.image_tag_table.rowCount()
                                self.image_tag_table.insertRow(row)
                                self.image_tag_table.setItem(row, 0, QtWidgets.QTableWidgetItem(tag.strip()))
                else:
                    self.image_tag_table.clear()
                    self.image_tag_table.setRowCount(1)
        except AttributeError:
            pass

    def select_next(self):
        current_row = self.images_list.currentRow()
        next_row = current_row + 1
        if next_row < self.images_list.count():
            self.images_list.setCurrentRow(next_row)

    def select_prev(self):
        current_row = self.images_list.currentRow()
        prev_row = current_row - 1
        if prev_row >= 0:
            self.images_list.setCurrentRow(prev_row)

    def add_row(self):
        if self.image_tag_table == QtWidgets.QApplication.focusWidget():
            self.image_tag_table.insertRow(self.image_tag_table.rowCount())
        elif self.all_images_tags_list == QtWidgets.QApplication.focusWidget():
            self.all_images_tags_list.insertRow(self.all_images_tags_list.rowCount())

    def add_row_below_current(self):
        if self.image_tag_table == QtWidgets.QApplication.focusWidget():
            selected_row = self.image_tag_table.currentRow()
            self.image_tag_table.insertRow(selected_row + 1)
        elif self.all_images_tags_list == QtWidgets.QApplication.focusWidget():
            selected_row = self.all_images_tags_list.currentRow()
            self.all_images_tags_list.insertRow(selected_row + 1)

    def remove_row(self):
        if self.image_tag_table == QtWidgets.QApplication.focusWidget():
            self.image_tag_table.removeRow(self.image_tag_table.currentRow())
        elif self.all_images_tags_list == QtWidgets.QApplication.focusWidget():
            self.all_images_tags_list.removeRow(self.all_images_tags_list.currentRow())

    def save_individual(self):
        if self.images_list.count() > 0:
            unique_tags = set()
            selected_item = self.images_list.currentItem()
            file_path = selected_item.data(Qt.UserRole)
            tag_file_path = f"{file_path.rsplit('.', 1)[0]}.txt"
            data = self.get_table_data()
            for tag in data:
                unique_tags.add(tag)

            sorted_tags = list(unique_tags)
            sorted_tags.sort()
            with open(tag_file_path, "w") as f:
                f.write(", ".join(sorted_tags))

    def remove_from_all(self, files_path):
        tag_to_remove = self.tagToRemoveLineEdit.text()
        for file_path in files_path:
            if os.path.isfile(file_path):
                unique_tags = set()
                with open(file_path, 'r') as file:
                    for line in file:
                        tags = line.split(",")
                        for tag in tags:
                            tag = tag.strip()
                            if tag != tag_to_remove:
                                if tag != "":
                                    unique_tags.add(tag)

            sorted_tags = list(unique_tags)
            sorted_tags.sort()
            with open(file_path, "w") as f:
                f.write(", ".join(sorted_tags))

    def get_table_data(self):
        data = []
        for row in range(self.image_tag_table.rowCount()):
            for column in range(self.image_tag_table.columnCount()):
                item = self.image_tag_table.item(row, column)
                if item is not None:
                    data.append(item.text())
                else:
                    data.append('')
        return data

    def get_all_tags_table_data(self):
        data = []
        for row in range(self.all_images_tags_list.rowCount()):
            for column in range(self.all_images_tags_list.columnCount()):
                item = self.all_images_tags_list.item(row, column)
                if item is not None:
                    data.append(item.text())
                else:
                    data.append('')
        return data
 
    def on_preview_toggled(self, checked):
        if checked:
            if self.preview is None:
                selected_item = self.images_list.currentItem()
                if selected_item:
                    file_path = selected_item.data(Qt.UserRole)
                    self.preview = Preview(file_path, self.show_preview_action)
                    self.preview.show()
        else:
            if self.preview:
                self.preview.hide()
                self.preview.deleteLater()
                self.preview = None
    
    def on_preview_tag_toggled(self, checked):
        if checked:
            if self.preview_tags is None:
                tags = []
                files = []
                for i in range(self.images_list.count()):
                    files.append(f"{self.images_list.item(i).data(Qt.UserRole).rsplit('.', 1)[0]}.txt")
                if files:
                    for f in files:
                        if os.path.isfile(f):
                            with open(f) as fIn:
                                for x in fIn:
                                    if "---" in x:
                                        tags.extend([y.strip() for y in x.split("---")])
                                    else:
                                        tags.extend([y.strip() for y in x.split(",")])
                total = {item:tags.count(item) for item in tags}
                sorted_total = dict(sorted(total.items(), key=lambda x:x[1], reverse=True))
                self.preview_tags = PreviewTags(sorted_total, self.show_tag_count_action)
                self.preview_tags.show()

        else:
            if self.preview_tags:
                #self.preview.hide()
                #self.preview.deleteLater()
                #self.preview = None
                self.preview_tags.hide()
                self.preview_tags.deleteLater()
                self.preview_tags = None

    def on_item_double_clicked(self):
        if not self.show_preview_action.isChecked():
            self.show_preview_action.setChecked(True)

    def open_folder(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a Folder", options=options)
        if folder:
            self.images_list.clear()
            for file_name in os.listdir(folder):
                if file_name.endswith(".jpg") or file_name.endswith(".png") or file_name.endswith(".jpeg"):
                    pixmap = QPixmap(os.path.join(folder, file_name)).scaled(150, 150, Qt.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    label = QtWidgets.QLabel()
                    label.setPixmap(pixmap)
                    item = QtWidgets.QListWidgetItem(self.images_list)
                    item.setSizeHint(label.sizeHint())
                    self.images_list.addItem(item)
                    self.images_list.setItemWidget(item, label)
                    item.setData(Qt.UserRole, os.path.join(folder, file_name))
    
    def open_folder_debug(self):
        folder = r"path/to/folder"
        if folder:
            self.images_list.clear()
            for file_name in os.listdir(folder):
                if file_name.endswith(".jpg") or file_name.endswith(".png") or file_name.endswith(".jpeg"):
                    pixmap = QPixmap(os.path.join(folder, file_name)).scaled(150, 150, Qt.KeepAspectRatio)
                    label = QtWidgets.QLabel()
                    label.setPixmap(pixmap)
                    item = QtWidgets.QListWidgetItem(self.images_list)
                    item.setSizeHint(label.sizeHint())
                    self.images_list.addItem(item)
                    self.images_list.setItemWidget(item, label)
                    item.setData(Qt.UserRole, os.path.join(folder, file_name))

    def handle_hotkeys(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.hotkeys = Hotkeys(config, self.setupHotkeys)
        self.hotkeys.show()

    def closeEvent(self, event):
        app.quit()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    form = Tagger()
    form.show()
    sys.exit(app.exec_())