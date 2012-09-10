from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.cookiecuttr')


class ICookieCuttr(Interface):
    """This interface is registered in profiles/default/browserlayer.xml,
    and is referenced in the 'layer' option of various browser resources.
    When the product is installed, this marker interface will be applied
    to every request, allowing layer-specific customisation.
    """


class ICookieCuttrSettings(Interface):
    """Global CookieCuttr settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    cookiecuttr_enabled = schema.Bool(title=_(u"Enable CookieCuttr"),
                                  description=_(u"help_cookiecuttr_enable",
                                                default=u"Toggle this to enable"
                                                " loading of the CookieCuttr"
                                                " plugin."),
                                  required=False,
                                  default=False,)

    cookiecuttr_text = schema.TextLine(title=_(u"Text to show your visitor"),
                                       description=_(u"", default=u""),
                                       required=False,
                                       default=u"")

    cookiecuttr_accept_button = schema.TextLine(title=_(u"Text to show in the Accept button"),
                                       description=_(u"", default=u""),
                                       required=False,
                                       default=_(u"Accept"))

    cookiecuttr_decline_button = schema.TextLine(title=_(u"Text to show in the Decline button"),
                                       description=_(u"", default=u""),
                                       required=False,
                                       default=_(u"Decline"))
    cookiecuttr_what_are_they_url= schema.TextLine(title=_(u"URL to a site explaining what cookies are"),
                                       description=_(u"", default=u""),
                                       required=False,
                                       default=_(u"http://"))

    cookiecuttr_what_are_they_text= schema.TextLine(title=_(u"Text to show in What Are Cookies URL"),
                                       description=_(u"", default=u""),
                                       required=False,
                                       default=_(u"What are cookies?"))

