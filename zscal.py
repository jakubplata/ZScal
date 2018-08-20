# -*- coding: utf-8 -*-

import random
from dzialki import Dzialka
from PySide.QtGui import *
from PySide.QtCore import *
from main_window import Ui_MainWindow
import sys


VERSION = '0.1'
HELPTEXT = """
ZScal - wersja: %s

Autor: Jakub Plata
"""

TEKSTY = ["Rozciągam granicę...", "Przekopuję graniczniki...",
          "Poprawiam dzienniki...", "Poziomuję butel... yyy libelkę",
          "Naciągam pomiary...", "Centruję instrument...", "Szukam wizury...",
          "Szkicuję..."]


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.assignWidgets()

        self.show()

    def assignWidgets(self):
        self.actionOpen.triggered.connect(self.set_infile_path)
        self.actionSave.triggered.connect(self.set_outfile_path)
        self.actionExit.triggered.connect(self.close_application)
        self.actionO_programie.triggered.connect(self.about)

        self.change_infile_btn.clicked.connect(self.set_infile_path)
        self.change_outfile_btn.clicked.connect(self.set_outfile_path)
        self.zaokr_btn.clicked.connect(self.zaok_file)

    def set_infile_path(self):
        self.winscal_file, _ = QFileDialog.getOpenFileName(self,
                                                          'Wybierz plik', '.')
        self.infile_path.setText(self.winscal_file)

    def set_outfile_path(self):
        self.zaokscal_file, _ = QFileDialog.getSaveFileName(self,
                                                           'Zapisz plik', '.')
        self.outfile_path.setText(self.zaokscal_file)

    def about(self):
        QMessageBox.information(self, 'O programie', HELPTEXT % VERSION)

    def close_application(self):
        choice = QMessageBox.question(self, 'Koniec?',
                                      'Porzucasz mnie?',
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    ###########################################################################
    # SCAL METHODS
    ###########################################################################

    def txt(self):
        return TEKSTY[random.randint(0, len(TEKSTY)-1)]

    def zaok_file(self):
        try:
            self.read_file()
            errors_info = self.write_file()
        except (FileNotFoundError, AttributeError):
            self.statusBar().clearMessage()
            QMessageBox.critical(self, 'Błąd!!!', 'Nie wybrano plików!')
        else:
            info_text = """Działki z zerową powierzchnią: %s
Rozbieżności w powierzchni: %s
            """ % errors_info
            QMessageBox.information(self, 'Gotowe!', info_text)


    def read_file(self):
        self.statusBar().showMessage('Wczytuję dane...')
        with open(self.winscal_file, 'r') as infile:
            self.dzialki = []
            data = [row.strip().split() for row in infile.readlines()]
            index = 0
            progress = QProgressDialog(self.txt(), 'Anuluj',
                                       0, len(data)+1)
            progress.setWindowModality(Qt.WindowModal)
            progress.setWindowTitle("Czekaj...")
            for n, r in enumerate(data):
                progress.setValue(n)
                if r == ['**']:
                    nr, pow = data[index][0:2]  # index omija ewntualnie pozostawione uwagi w pliku
                    kon = {'kontury': data[index + 1:n]}
                    self.dzialki.append(Dzialka(nr, pow,
                                                self.kasujzero_box.isChecked(),
                                                self.powrozb_box.isChecked(),
                                                **kon))
                    index = n + 1
        infile.close()
        self.statusBar().clearMessage()

    def write_file(self):
        self.statusBar().showMessage('Zapisuję dane...')
        with open(self.zaokscal_file, 'w') as outfile:
            progress = QProgressDialog(self.txt(), 'Anuluj',
                                       0, len(self.dzialki) + 1)
            progress.setWindowModality(Qt.WindowModal)
            progress.setWindowTitle("Czekaj...")
            pow_errors = 0
            zero_errors = 0
            for nr, d in enumerate(self.dzialki):
                progress.setValue(nr)
                txt, zc, pc = d.text_to_write()
                outfile.writelines(txt)
                pow_errors += pc
                zero_errors += zc
        outfile.close()
        self.statusBar().clearMessage()
        return zero_errors, pow_errors

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Plastique')
    translator = QTranslator(app)
    locale = QLocale.system().name()
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator.load('qt_%s' % locale, path)
    app.installTranslator(translator)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )