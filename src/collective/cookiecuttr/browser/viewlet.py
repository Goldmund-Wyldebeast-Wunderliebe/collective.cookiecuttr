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
        try:
            self.settings = getUtility(IRegistry).forInterface(ICookieCuttrSettings)
        except:
            self.settings = None

    def update(self):
        pass

    def available(self):
        return self.settings and self.settings.cookiecuttr_enabled

    def render(self):
        if self.available():

            cuttr_dict = {}
            if self.settings.cookiecuttr_text:
                cuttr_dict['cookieAnalyticsMessage'] = str(self.settings.cookiecuttr_text)

            if self.settings.cookiecuttr_accept_button:
                cuttr_dict['cookieAcceptButtonText'] = str(self.settings.cookiecuttr_accept_button)
            if self.settings.cookiecuttr_decline_button:
                cuttr_dict['cookieDeclineButtonText'] = str(self.settings.cookiecuttr_decline_button,)
                cuttr_dict['cookieDeclineButton'] = 'true'


            if self.settings.cookiecuttr_what_are_they_url and self.settings.cookiecuttr_what_are_they_text:
                cuttr_dict['cookieWhatAreTheyLink'] = str(self.settings.cookiecuttr_what_are_they_url)
                cuttr_dict['cookieWhatAreLinkText'] = str(self.settings.cookiecuttr_what_are_they_text)
            else:
                cuttr_dict['cookieWhatAreTheyLink'] = 'false'
                cuttr_dict['cookieWhatAreLinkText'] = ''


            snippet = safe_unicode(js_template % str(cuttr_dict) )
            return snippet
        return ""


class CookieCuttrAwareAnalyticsViewlet(AnalyticsViewlet):

    def render(self):
        # Retrieve settings from registry
        settings = getUtility(IRegistry).forInterface(ICookieCuttrSettings)
        available = settings and settings.cookiecuttr_enabled

        # Render if CookieCuttr is 'Not available' or Cookies were accepted
        if not available or self.request.cookies.get('cc_cookie_accept',None):
            return super(CookieCuttrAwareAnalyticsViewlet, self).render()

        return ""   

js_template = """
<script type="text/javascript">

    (function($) {
        $(document).ready(function () {
            if($.cookieCuttr)
                $.cookieCuttr(%s);
        });
    })(jQuery);
</script>

"""
