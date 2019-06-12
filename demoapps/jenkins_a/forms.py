from django import forms


def config_xml_valid(value):
    pass


class JobConfForm(forms.Form):
    name = forms.CharField(label='项目名称')
    config_xml = forms.FileField(label='配置', validators=[config_xml_valid])
