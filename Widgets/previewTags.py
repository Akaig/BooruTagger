from PyQt5 import QtWidgets, uic

preview_tags_class = uic.loadUiType("Ui/previewTags.ui")[0]
class PreviewTags(QtWidgets.QDialog, preview_tags_class):
    def __init__(self, sorted_tags, show_tag_action):
        super().__init__()
        self.setupUi(self)
        self.show_tag_action = show_tag_action
        self.sorted_tags = sorted_tags
        self.show_tag_action.triggered.connect(self.handle_show_tag_action)
        self.exportButton.clicked.connect(self.exportTags)
        self.move(0,0)
        self.populate_table()
        self.rejected.connect(self.close_tag_window)

    def close_tag_window(self):
        self.show_tag_action.setChecked(False)

    def handle_show_tag_action(self, checked):
        if not checked:
            self.close()

    def populate_table(self):
        self.tags_table.clear()
        for k in self.sorted_tags.keys():
            row = self.tags_table.rowCount()
            self.tags_table.insertRow(row)
            self.tags_table.setItem(row, 0, QtWidgets.QTableWidgetItem(k))
            self.tags_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(self.sorted_tags[k])))

    def exportTags(self):
        with open("exported tags.txt", "w") as fOut:
            for key in self.sorted_tags:
                fOut.write("%s,%s\n"%(key,self.sorted_tags[key]))