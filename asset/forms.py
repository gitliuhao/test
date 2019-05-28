from django import forms

from asset.models import Asset


class AssetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class']="form-control"

    class Meta:
        model = Asset
        fields = "__all__"
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     '': forms.TextInput(attrs={'class': 'form-control'}),
        # }