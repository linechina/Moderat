from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
from libs.language import Translate

# Multi Lang
translate = Translate()
_ = lambda _word: translate.word(_word)

class moderatRightClickMenu:
    def __init__(self, moderat):
        self.moderat = moderat

        self.moderat.clientsTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.moderat.connect(self.moderat.clientsTable, SIGNAL('customContextMenuRequested(const QPoint&)'),
                             self.online_clients_menu)

        self.moderat.offlineClientsTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.moderat.connect(self.moderat.offlineClientsTable, SIGNAL('customContextMenuRequested(const QPoint&)'),
                             self.offline_clients_menu)

        self.moderat.moderatorsTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.moderat.connect(self.moderat.moderatorsTable, SIGNAL('customContextMenuRequested(const QPoint&)'),
                             self.moderators_menu)

    def online_clients_menu(self, point):
        self.moderat.emenu = QMenu(self.moderat)

        if self.moderat.clientsTable.currentRow() >= 0:
            self.moderat.emenu.addAction(QIcon(':/icons/assets/log_viewer.png'), _('VIEWER_WINDOW_TITLE'),
                                         lambda: self.moderat.execute_module(module='logviewer'))
            self.moderat.emenu.addAction(QIcon(':/icons/assets/other_settings.png'), _('LOG_SETTINGS_TITLE'),
                                         self.moderat.set_logs_settings)
            self.moderat.emenu.addSeparator()
            self.moderat.emenu.addAction(QIcon(':/icons/assets/set_alias.png'), _('SET_ALIAS'),
                                         self.moderat.set_alias)
            self.moderat.emenu.addAction(QIcon(':/icons/assets/update_source.png'), _('RELOAD_CLIENT'),
                                         self.moderat.update_source)
            self.moderat.emenu.addSeparator()
            self.moderat.emenu.addAction(QIcon(':/icons/assets/remote_shell.png'), _('MSHELL_TITLE'),
                                         lambda: self.moderat.execute_module(module='shell'))
            self.moderat.emenu.addAction(QIcon(':/icons/assets/remote_explorer.png'), _('MEXPLORER_TITLE'),
                                         lambda: self.moderat.execute_module(module='explorer'))
            self.moderat.emenu.addAction(QIcon(':/icons/assets/remote_scripting.png'), _('MSCRIPTING_TITLE'),
                                         lambda: self.moderat.execute_module(module='scripting'))
            self.moderat.emenu.addAction(QIcon(':/icons/assets/desktop.png'), _('MDESKTOP_TITLE'),
                                         lambda: self.moderat.execute_module(module='desktop'))
            self.moderat.emenu.addAction(QIcon(':/icons/assets/webcam.png'), _('MWEBCAM_TITLE'),
                                         lambda: self.moderat.execute_module(module='webcam'))

            if self.moderat.privs == 1:
                self.moderat.emenu.addSeparator()
                self.moderat.emenu.addAction(QIcon(':/icons/assets/set_moderator.png'), _('SET_MODERATOR_TITLE'),
                                             self.moderat.set_moderator)

        self.moderat.emenu.exec_(self.moderat.clientsTable.mapToGlobal(point))

    def offline_clients_menu(self, point):
        self.moderat.emenu = QMenu(self.moderat)
        if self.moderat.offlineClientsTable.currentRow() >= 0:
            self.moderat.emenu.addAction(QIcon(':/icons/assets/log_viewer.png'), _('VIEWER_WINDOW_TITLE'),
                                         lambda: self.moderat.execute_module(module='logviewer'))
            self.moderat.emenu.addAction(QIcon(':/icons/assets/set_alias.png'), _('SET_ALIAS'),
                                         self.moderat.set_alias)
            self.moderat.emenu.addAction(QIcon(':/icons/assets/trash.png'), _('REMOVE_CLIENT'),
                                         self.moderat.remove_client)
        self.moderat.emenu.exec_(self.moderat.offlineClientsTable.mapToGlobal(point))

    def moderators_menu(self, point):
        self.moderat.emenu = QMenu(self.moderat)
        if self.moderat.moderatorsTable.currentRow() >= 0:
            self.moderat.emenu.addAction(QIcon(':/icons/assets/add_moderator.png'), _('MODERATOR_ADD_MDOERATOR'),
                                         self.moderat.create_moderator)
            self.moderat.emenu.addAction(QIcon(':/icons/assets/password.png'), _('MODERATOR_CHANGE_PASSWORD'),
                                         self.moderat.change_moderator_password)
            self.moderat.emenu.addAction(QIcon(':/icons/assets/privileges.png'), _('MODERATOR_CHANGE_GROUP'),
                                         self.moderat.change_moderator_privilege)
            self.moderat.emenu.addAction(QIcon(':/icons/assets/trash.png'), _('MODERATOR_REMOVE'),
                                         self.moderat.remove_moderator)
        self.moderat.emenu.exec_(self.moderat.moderatorsTable.mapToGlobal(point))