#  _  __         _          ___       _               ___ _           _
# | |/ /_ _ __ _| |_ ___ __/ __| __ _| |___ _ __  ___| _ \ |_  _ __ _(_)_ _
# | ' <| '_/ _` |  _/ _ (_-<__ \/ _` | / _ \ '  \/ -_)  _/ | || / _` | | ' \
# |_|\_\_| \__,_|\__\___/__/___/\__,_|_\___/_|_|_\___|_| |_|\_,_\__, |_|_||_|
#                                                               |___/
# License: BSD License ; see LICENSE
#
# Main authors: Philipp Bucher (https://github.com/philbucher)
#

"""
This is the file that is detected by salome in order to load the plugin
Do not rename or move this file!
Check "salome_pluginsmanager.py" for more information
"""

def InitializePlugin(context):
    """Main function for initializing / opening the plugin
    This is called each time the user opens the KratosMultiphysics plugin in Salome
    """

    ### for development/debugging
    reinitialize_every_time = False # default value: False # CONFIG

    # python imports
    import logging
    logger = logging.getLogger(__name__)

    # plugin imports
    from kratos_salome_plugin.gui.plugin_controller import PluginController
    import kratos_salome_plugin.gui.active_window as active_window
    import kratos_salome_plugin.version as plugin_version
    from kratos_salome_plugin import salome_utilities
    from kratos_salome_plugin.reload_modules import ReloadModules

    # salome imports
    import qtsalome

    # qt imports
    from PyQt5.QtWidgets import QMessageBox

    ### initializing the plugin ###
    logger.info("")
    logger.info("Starting to initialize plugin")

    # logging configuration
    logger.info('Reinitialize Plugin every time: %s', reinitialize_every_time)

    if reinitialize_every_time:
        ReloadModules()

    global VERSION_CHECKS_PERFORMED
    if 'VERSION_CHECKS_PERFORMED' not in globals():
        # doing the version check only once per session and not every time the plugin is reopened
        VERSION_CHECKS_PERFORMED = 1
        # check version of py-qt
        expected_qt_version = 5
        if not qtsalome.QT_SALOME_VERSION == expected_qt_version:
            logger.warning('The version of PyQt has changed, from %d to %d!', expected_qt_version, qtsalome.QT_SALOME_VERSION)

        # check if version of salome is among the checked versions
        salome_versions = salome_utilities.GetVersions()
        if salome_versions not in plugin_version.TESTED_SALOME_VERSIONS:
            msg  = 'This Plugin is not tested with this version of Salome ({}.{}.{}).\n'.format(*salome_versions)
            msg += 'The tested versions are:'
            for v in plugin_version.TESTED_SALOME_VERSIONS:
                msg += '\n    {}.{}.{}'.format(*v)
            QMessageBox.warning(None, 'Untested Salome Version', msg)

    global PLUGIN_CONTROLLER
    if 'PLUGIN_CONTROLLER' not in globals() or reinitialize_every_time:
        # initialize only once the PluginController
        PLUGIN_CONTROLLER = PluginController()

    active_window.ACTIVE_WINDOW.ShowOnTop()

    logger.info("Successfully initialized plugin")

### Registering the Plugin in Salome ###

fct_args = [
    'Kratos Multiphysics',
    'Starting the plugin for Kratos Multiphysics',
]

from salome_pluginsmanager import AddFunction
import kratos_salome_plugin.salome_utilities as salome_utils
from kratos_salome_plugin.utilities import GetAbsPathInPlugin

if salome_utils.GetVersions() >= [9,3,0]:
    fct_args.append(InitializePlugin)
    from PyQt5.QtGui import QIcon
    icon_file = GetAbsPathInPlugin("misc","kratos_logo.png")
    fct_args.append(QIcon(icon_file))
else:
    def ShowMessageUnSupportedVersion(dummy):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(None, 'Unsupported version', 'This Plugin only works for Salome version 9.3 and newer!')
    fct_args.append(ShowMessageUnSupportedVersion)

AddFunction(*fct_args)
