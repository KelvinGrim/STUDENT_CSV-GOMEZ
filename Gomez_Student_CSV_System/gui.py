import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QComboBox, QMessageBox, QMenu, QDialog, QFormLayout,
    QHeaderView, QFrame, QShortcut
)
from PyQt5.QtCore import Qt
import main


 #========================================#
class AddDialog(QDialog):
    def __init__(self, title, fields, data=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumWidth(400)

        self.inputs = {}
        layout = QFormLayout(self)
        layout.setSpacing(12)

        for i, field in enumerate(fields):
            le = QLineEdit()
            le.setMinimumHeight(32)
            le.setSizePolicy(le.sizePolicy().horizontalPolicy(),
                             le.sizePolicy().Expanding)

            if data:
                le.setText(data[i])

            self.inputs[field] = le
            layout.addRow(field, le)

        btns = QHBoxLayout()

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)
        layout.addRow(btns)

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

    def get_data(self):
        return [w.text().strip() for w in self.inputs.values()]


 #========================================#
class ViewDialog(QDialog):
    def __init__(self, title, headers, data):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(800, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.right_click)

        for r, row in enumerate(data):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(value))

        header = self.table.horizontalHeader()

        if len(headers) == 3:
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        else:
            header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

    def right_click(self, pos):
        row = self.table.currentRow()
        if row < 0:
            return

        menu = QMenu()

        edit = menu.addAction("Edit")
        delete = menu.addAction("Delete")

        action = menu.exec_(self.table.mapToGlobal(pos))

        if action == edit:
            self.edit_row(row)

        elif action == delete:
            if QMessageBox.question(self, "Confirm", "Delete this entry?") == QMessageBox.Yes:
                self.delete_row(row)

    def delete_row(self, row):
        title = self.windowTitle()

        if "College" in title:
            rows = main.read_csv("colleges.csv")
            rows.pop(row)
            main.write_csv("colleges.csv", rows)

        elif "Program" in title:
            rows = main.read_csv("programs.csv")
            rows.pop(row)
            main.write_csv("programs.csv", rows)

        self.table.removeRow(row)

    def edit_row(self, row):
        title = self.windowTitle()

        if "College" in title:
            file = "colleges.csv"
            fields = ["Code", "Name"]

        elif "Program" in title:
            file = "programs.csv"
            fields = ["Code", "Name", "College"]

        else:
            return

        data = main.read_csv(file)

        dlg = AddDialog("Edit Entry", fields, data[row])

        if dlg.exec_():
            new_data = dlg.get_data()
            data[row] = new_data
            main.write_csv(file, data)

            for c, v in enumerate(new_data):
                self.table.setItem(row, c, QTableWidgetItem(v))


 #========================================#
class StudentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student CSV System")
        self.setFixedSize(1200, 900)
        self.edit_id = None
        self.init_ui()

    def init_ui(self):
        root = QHBoxLayout(self)
        root.setSpacing(20)

 #========================================#
        left = QVBoxLayout()
        left.setSpacing(14)

        self.menu_btn = QPushButton("Menu")
        self.menu_btn.setFixedSize(70, 30)
        left.addWidget(self.menu_btn)


        input_card = QFrame()
        input_layout = QVBoxLayout(input_card)
        input_layout.setSpacing(10)

        self.id = QLineEdit()
        self.id.setPlaceholderText("0000-0000")
        self.fn = QLineEdit()
        self.ln = QLineEdit()
        self.program = QLineEdit()
        self.year = QLineEdit()

        self.gender = QComboBox()
        self.gender.addItem("Select Gender")
        self.gender.addItems(["Male", "Female", "Non-binary"])
        self.gender.model().item(0).setEnabled(False)

        fields = [
            ("Student ID", self.id),
            ("First Name", self.fn),
            ("Last Name", self.ln),
            ("Program Code", self.program),
            ("Year", self.year),
        ]

        for lbl, w in fields:
            label = QLabel(lbl)
            label.setMinimumHeight(20)

            w.setMinimumHeight(28)

            input_layout.addWidget(label)
            input_layout.addWidget(w)
            
        self.add_btn = QPushButton("Add Student")
        self.add_btn.setMinimumHeight(28)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumHeight(28)

        input_layout.addSpacing(10)
        input_layout.addWidget(self.gender)
        input_layout.addWidget(self.add_btn)
        input_layout.addWidget(self.cancel_btn)

        left.addWidget(input_card)


        details_card = QFrame()
        details_layout = QVBoxLayout(details_card)
        details_layout.setSpacing(6)

        title = QLabel("Student Details")
        title.setStyleSheet("font-weight:bold; font-size:14px;")
        details_layout.addWidget(title)

        self.details = {}

        for label in ["ID", "First Name", "Last Name", "Program", "Year", "Gender"]:
            lbl = QLabel(f"{label}: ")
            self.details[label] = lbl
            details_layout.addWidget(lbl)

        left.addWidget(details_card)
        left.addStretch()

 #========================================#
        right = QVBoxLayout()
        right.setSpacing(10)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search students...")

        self.table = QTableWidget()
        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            ["ID", "First Name", "Last Name", "Program", "Year", "Gender"]
        )
        
        self.table.horizontalHeader().setMinimumHeight(50)
        self.table.verticalHeader().setDefaultSectionSize(28) 
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.table_menu)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        v_header = self.table.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.Fixed)
        v_header.setDefaultSectionSize(36)      
        right.addWidget(self.search)
        right.addWidget(self.table)

        root.addLayout(left, 1)
        root.addLayout(right, 2)

        # SIGNALS
        self.search.textChanged.connect(self.load_students)
        self.add_btn.clicked.connect(self.add_or_update)
        self.cancel_btn.clicked.connect(self.cancel_edit)
        self.menu_btn.clicked.connect(self.open_menu)
        self.table.itemSelectionChanged.connect(self.show_details)

        QShortcut("Return", self, activated=self.add_or_update)
        QShortcut("Escape", self, activated=self.cancel_edit)

        self.apply_style()
        self.load_students()

 #========================================#
    def apply_style(self):
        self.setStyleSheet("""
        /* Only style containers — DO NOT override text colors */

        QFrame {
            background: white;
            border: 1px solid #D0D0D0;
            border-radius: 8px;
            padding: 8px;
        }

        QLineEdit, QComboBox {
            padding: 4px;
            border: 1px solid #BEBEBE;
            border-radius: 4px;
        }

        QPushButton {
            padding: 6px;
            border-radius: 6px;
            border: 1px solid #BEBEBE;
            background: #EAEAEA;
        }

        QPushButton:hover {
            background: #DCDCDC;
        }

        QPushButton[text="Add Student"],
        QPushButton[text="Update Student"] {
            background: #2F6FD6;
            color: white;
            font-weight: bold;
        }

        QTableWidget {
            border: 1px solid #D0D0D0;
            background: white;
            gridline-color: #E5E5E5;
        }

        QHeaderView::section {
            background: #E6E6E6;
            padding: 6px;
            border: 1px solid #C8C8C8;
            font-weight: bold;
        }
        """)
 #========================================#
    def open_menu(self):
        menu = QMenu(self)

        add_college = menu.addAction("Add College")
        add_program = menu.addAction("Add Program")
        view_colleges = menu.addAction("View Colleges")
        view_programs = menu.addAction("View Programs")

        action = menu.exec_(self.menu_btn.mapToGlobal(self.menu_btn.rect().bottomLeft()))

        if action == add_college:
            dlg = AddDialog("Add College", ["Code", "Name"])
            if dlg.exec_():
                main.add_college(dlg.get_data())

        elif action == add_program:
            dlg = AddDialog("Add Program", ["Code", "Name", "College Code"])
            if dlg.exec_():
                main.add_program(dlg.get_data())

        elif action == view_colleges:
            ViewDialog("Colleges List", ["Code", "Name"], main.read_csv("colleges.csv")).exec_()

        elif action == view_programs:
            ViewDialog("Programs List", ["Code", "Name", "College"], main.read_csv("programs.csv")).exec_()

 #========================================#
    def table_menu(self, pos):
        row = self.table.rowAt(pos.y())

        menu = QMenu(self)

        if row >= 0:
            edit = menu.addAction("Edit Student")
            delete = menu.addAction("Delete Student")
        else:
            refresh = menu.addAction("Refresh")

        action = menu.exec_(self.table.viewport().mapToGlobal(pos))

        if row >= 0:
            student_id = self.table.item(row, 0).text()
            real_index = self.get_real_index(student_id)

            if action == edit:
                self.edit_student(row)

            elif action == delete:
                if QMessageBox.question(self, "Confirm", "Delete this student?") == QMessageBox.Yes:
                    main.delete_student(real_index)
                    self.load_students()

        else:
            if action == refresh:
                self.load_students()

    def load_students(self):
        text = self.search.text().lower()
        data = main.read_csv("students.csv")

        filtered = [r for r in data if text in " ".join(r).lower()]

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(filtered))

        for r, row in enumerate(filtered):
            for c, v in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(v))

        self.table.setSortingEnabled(True)

    def edit_student(self, row):
        self.edit_id = self.table.item(row, 0).text()

        self.id.setText(self.table.item(row, 0).text())
        self.fn.setText(self.table.item(row, 1).text())
        self.ln.setText(self.table.item(row, 2).text())
        self.program.setText(self.table.item(row, 3).text())
        self.year.setText(self.table.item(row, 4).text())

        gender = self.table.item(row, 5).text()
        index = self.gender.findText(gender)
        if index >= 0:
            self.gender.setCurrentIndex(index)

        self.add_btn.setText("Update Student")



    def add_or_update(self):
        data = [
            self.id.text(),
            self.fn.text(),
            self.ln.text(),
            self.program.text(),
            self.year.text(),
            self.gender.currentText()
        ]


        if self.edit_id is None:
            ok, msg = main.add_student(data)


        else:
            idx = self.get_real_index(self.edit_id)


            if idx is None:
                QMessageBox.warning(
                    self,
                    "Update Failed",
                    "Student no longer exists."
                )


                self.clear_inputs()
                self.edit_id = None
                self.add_btn.setText("Add Student")
                self.load_students()
                return

            ok, msg = main.update_student(idx, data)


        if not ok:
            QMessageBox.warning(self, "Error", msg)
            return


        self.clear_inputs()
        self.edit_id = None
        self.add_btn.setText("Add Student")
        self.load_students()
        
    def cancel_edit(self):
            self.clear_inputs()
            self.edit_id = None
            self.add_btn.setText("Add Student")

    def clear_inputs(self):
        for w in [self.id, self.fn, self.ln, self.program, self.year]:
            w.clear()
        self.gender.setCurrentIndex(0)

    def show_details(self):
        row = self.table.currentRow()
        headers = ["ID", "First Name", "Last Name", "Program", "Year", "Gender"]

        if row < 0:
            for key in headers:
                self.details[key].setText(f"{key}: ")
            return

        for i, key in enumerate(headers):
            item = self.table.item(row, i)
            self.details[key].setText(f"{key}: {item.text() if item else ''}")

    def get_real_index(self, student_id):
        data = main.read_csv("students.csv")
        for i, row in enumerate(data):
            if row[0] == student_id:
                return i
        return None



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StudentApp()
    win.show()
    sys.exit(app.exec_())

