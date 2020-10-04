from django import forms

from rest.iglink.models import InstagramAPISettings


class IGApiForm(forms.ModelForm):
    """
    Form directive for admin.
    """
    ig_username = forms.CharField()

    class Meta:
        model = InstagramAPISettings
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IGApiForm, self).__init__(*args, **kwargs)
        self.fields['ig_username'].required = True
