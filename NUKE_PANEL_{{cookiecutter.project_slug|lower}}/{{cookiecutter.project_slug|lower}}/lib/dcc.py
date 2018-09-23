from ..extern.Qt import QtWidgets  # pylint: disable=E0611
from ..extern.Qt import QtCore     # pylint: disable=E0611
from ..extern.Qt import QtCompat

__all__ = ["_maya_delete_ui","_nuke_delete_ui","_maya_main_window","_nuke_main_window","_nuke_set_zero_margins"]
# ----------------------------------------------------------------------
# Environment detection
# ----------------------------------------------------------------------

try:
    import maya.cmds as cmds
    MAYA = True
except ImportError:
    MAYA = False

try:
    import nuke
    import nukescripts
    NUKE = True
except ImportError:
    NUKE = False

STANDALONE = False
if not MAYA and not NUKE:
    STANDALONE = True

# ----------------------------------------------------------------------
# DCC application helper functions
# ----------------------------------------------------------------------


def _maya_delete_ui(winobj, wintitle):
    """Delete existing UI in Maya"""
    if cmds.window(winobj, q=True, exists=True):
        cmds.deleteUI(winobj)  # Delete window
    if cmds.dockControl('MayaWindow|' + wintitle, q=True, ex=True):
        cmds.deleteUI('MayaWindow|' + wintitle)  # Delete docked window


def _nuke_delete_ui(winobj):
    """Delete existing UI in Nuke"""
    for obj in QtWidgets.QApplication.allWidgets():
        if obj.objectName() == winobj:
            obj.deleteLater()


def _maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


def _nuke_main_window():
    """Returns Nuke's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        if (obj.inherits('QMainWindow') and
                obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
            return obj
    else:
        raise RuntimeError('Could not find DockMainWindow instance')


def _nuke_set_zero_margins(widget_object):
    """Remove Nuke margins when docked UI

    .. _More info:
        https://gist.github.com/maty974/4739917
    """
    try:
        if widget_object:
            target_widgets = set()
            target_widgets.add(widget_object.parentWidget().parentWidget())
            target_widgets.add(widget_object.parentWidget().parentWidget().parentWidget().parentWidget())

            for widget_layout in target_widgets:
                widget_layout.layout().setContentsMargins(0, 0, 0, 0)
    except:
        pass