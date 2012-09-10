from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import safe_unicode

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.cookiecuttr.interfaces import ICookieCuttrSettings
from plone.app.layout.analytics.view import AnalyticsViewlet

class CookieCuttrViewlet(BrowserView):
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(CookieCuttrViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.settings = getUtility(IRegistry).forInterface(ICookieCuttrSettings)

    def update(self):
        pass

    def available(self):
        return self.settings.cookiecuttr_enabled

    def render(self):
        if self.available():
            snippet = safe_unicode(js_template % (self.settings.cookiecuttr_text,
                                                  self.settings.cookiecuttr_accept_button,
                                                  self.settings.cookiecuttr_decline_button,
                                                  self.settings.cookiecuttr_what_are_they_url,
                                                  self.settings.cookiecuttr_what_are_they_text,
                                                  ))
            return snippet
        return ""


class CookieCuttrAwareAnalyticsViewlet(AnalyticsViewlet):

    def render(self):
        if self.request.cookies.get('cc_cookie_accept',None):
            return super(CookieCuttrAwareAnalyticsViewlet, self).render()
        else:
            return ""



js_template = """
<script type="text/javascript">

    (function($) {
        $(document).ready(function () {
            $.cookieCuttr({cookieAnalyticsMessage: "%s",
                           cookieAcceptButtonText: "%s",
                           cookieDeclineButtonText: "%s",
                           cookieWhatAreTheyLink: false,
                           cookieDeclineButton: true,
                           cookieWhatAreTheyLink: "%s",
                           cookieWhatAreLinkText: "%s"});
        })
    })(jQuery);
</script>

"""
