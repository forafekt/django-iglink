from django.db import models
from django.utils.translation import ugettext_lazy as _


class InstagramAPISettings(models.Model):
    """
    Input Instagram username from interface dynamically.
    """
    ig_username = models.CharField(max_length=30, default='', blank=True, null=True,
                                   verbose_name=_('Instagram username'))
    objects = models.Manager()

    class Meta:
        """
        Admin Meta
        """
        verbose_name = _("IG LINK")
        verbose_name_plural = _("IG LINK SETTINGS")

    def __str__(self):
        return self.ig_username
