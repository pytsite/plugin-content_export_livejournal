"""PytSite LiveJournal Content Export Driver
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from pytsite import lang
    from plugins import content_export, assetman
    from . import _driver

    # Resources
    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.js_module('content-export-livejournal-widget-settings',
                       __name__ + '@js/content-export-livejournal-widget-settings')
    assetman.t_js(__name__)

    # Content export driver
    content_export.register_driver(_driver.Driver())
