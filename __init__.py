"""PytSite LiveJournal Content Export Driver
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from plugins import assetman

    assetman.register_package(__name__)
    assetman.js_module('content-export-livejournal-widget-settings',
                       __name__ + '@js/content-export-livejournal-widget-settings')
    assetman.t_js(__name__)


def plugin_install():
    from plugins import assetman

    assetman.build(__name__)


def plugin_load_uwsgi():
    from pytsite import lang
    from plugins import content_export
    from . import _driver

    # Resources
    lang.register_package(__name__)

    # Content export driver
    content_export.register_driver(_driver.Driver())
