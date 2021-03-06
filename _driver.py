"""LiveJournal Content Export Driver
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from frozendict import frozendict as _frozendict
from pytsite import lang as _lang, util as _util, logger as _logger, html as _html
from plugins import widget as _widget, content_export as _content_export, livejournal as _livejournal


class _SettingsWidget(_widget.Abstract):
    """LiveJournal content_export Settings Widget.
     """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-content-export-lj-settings'
        self._username = kwargs.get('username', '')
        self._password = kwargs.get('password', '')
        self._lj_like = kwargs.get('lj_like', 'fb,tw,go,vk,lj')
        self._js_modules.append('content-export-livejournal-widget-settings')

    def _get_element(self, **kwargs) -> _html.Element:
        """Get HTML element of the widget.

        :param **kwargs:
        """
        wrapper = _html.TagLessElement()

        wrapper.append(_widget.input.Text(
            uid='{}[username]'.format(self._uid),
            label=_lang.t('content_export_livejournal@username'),
            required=True,
            value=self._username,
        ).renderable())

        wrapper.append(_widget.input.Password(
            uid='{}[password]'.format(self._uid),
            label=_lang.t('content_export_livejournal@password'),
            required=True,
            value=self._password,
        ).renderable())

        wrapper.append(_widget.input.Text(
            uid='{}[lj_like]'.format(self._uid),
            label=_lang.t('content_export_livejournal@lj_like_buttons'),
            help=_lang.t('content_export_livejournal@lj_like_buttons_help'),
            value=self._lj_like,
        ).renderable())

        wrapper.append(_widget.input.Hidden(
            uid='title',
            name='{}[title]'.format(self._uid),
            required=True,
            value=self._title,
        ).renderable())

        return wrapper


class Driver(_content_export.AbstractDriver):
    """LiveJournal content_export Driver.
    """

    def get_name(self) -> str:
        """Get system name of the driver.
        """
        return 'lj'

    def get_description(self) -> str:
        """Get human readable description of the driver.
        """
        return 'content_export_livejournal@livejournal'

    def get_options_description(self, driver_options: _frozendict) -> str:
        """Get human readable driver options.
        """
        return driver_options.get('username')

    def get_settings_widget(self, driver_opts: _frozendict, form_url: str) -> _widget.Abstract:
        """Add widgets to the settings form of the driver.
        """
        return _SettingsWidget(
            uid='driver_opts',
            username=driver_opts.get('username'),
            password=driver_opts.get('password'),
            lj_like=driver_opts.get('lj_like', 'fb,tw,go,vk,lj'),
        )

    def export(self, entity, exporter):
        """Performs export.

        :type entity: plugins.content._model.Content
        :type exporter: plugins.content_export._model.ContentExport
        """
        try:
            _logger.info("Export started. '{}'".format(entity.title))

            tags = exporter.add_tags

            if entity.has_field('tags'):
                tags += tuple([tag.title for tag in entity.f_get('tags')])

            opts = exporter.driver_opts

            msg = ''
            if entity.has_field('images') and entity.images:
                img_url = entity.images[0].get_url(width=1024)
                msg += '<p><a href="{}"><img src="{}" title="{}"></a></p>'. \
                    format(entity.url, img_url, _util.escape_html(entity.title))

            msg += '<p>{}: <a href="{}">{}</a></p>'.format(
                _lang.t('content_export_livejournal@source', language=entity.language), entity.url, entity.url)
            if entity.has_field('description'):
                msg += '<p>{}</p>'.format(entity.f_get('description'))
            msg += '<lj-cut>'
            msg_body = entity.f_get('body', process_tags=True, responsive_images=False, images_width=1200)
            msg_body = msg_body.replace('\r', '').replace('\n', '')
            msg += _util.trim_str(msg_body, 64000, True)
            msg += '</lj-cut>'
            if opts['lj_like']:
                msg += '<lj-like buttons="{}">'.format(opts['lj_like'])

            s = _livejournal.Session(opts['username'], opts['password'])
            pub_time = entity.f_get('publish_time') if entity.has_field('publish_time') else entity.created

            r = s.post_event(entity.title[:255], msg, tags, pub_time)

            _logger.info("Export finished. '{}'. LJ response: {}".format(entity.title, r))

        except Exception as e:
            raise _content_export.error.ExportError(e)
