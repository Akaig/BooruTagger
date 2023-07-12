from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QKeySequence

hotkeys_ui = uic.loadUiType("Ui/hotkeys.ui")[0]
class Hotkeys(QtWidgets.QDialog, hotkeys_ui):
    def __init__(self, config, setupHotkeys):
        super().__init__()
        self.setupUi(self)
        self.config = config
        self.setupHotkeys = setupHotkeys

        self.save_button.clicked.connect(self.saveHotkeys)
        self.populateHotkeys()

    def populateHotkeys(self):
        
        hotkey_boxes = [
            self.save_keysequence,
            self.del_keysequence,
            self.add_new_keysequence,
            self.add_new_below_keysequence,
            self.add_tag_keysequence,
        ]

        hotkeys = self.config["hotkeys"]

        for hotkey_box, config_value in zip(hotkey_boxes, hotkeys):
            hotkey_box.setKeySequence(QKeySequence.fromString(hotkeys[config_value]))

    def saveHotkeys(self):
        hotkey_boxes = [
            self.save_keysequence,
            self.del_keysequence,
            self.add_new_keysequence,
            self.add_new_below_keysequence,
            self.add_tag_keysequence,
        ]
        
        hotkeys = self.config["hotkeys"]

        for hotkey_box, config_value in zip(hotkey_boxes, hotkeys):
            hotkeys[config_value] = hotkey_box.keySequence().toString(QKeySequence.SequenceFormat.NativeText)
        with open("config.ini", "w") as f:
            self.config.write(f)

        self.setupHotkeys()