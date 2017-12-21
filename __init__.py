"""PytSite LiveJournal Content Export Driver
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _register_assetman_resources():
    from plugins import assetman

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.js_module('content-export-livejournal-widget-settings',
                           __name__ + '@js/content-export-livejournal-widget-settings')
        assetman.t_js(__name__)

    return assetman


def plugin_install():
    _register_assetman_resources().build(__name__)


def plugin_load_uwsgi():
    from pytsite import lang
    from plugins import content_export
    from . import _driver

    # Resources
    lang.register_package(__name__)
    _register_assetman_resources()

    # Content export driver
    content_export.register_driver(_driver.Driver())
