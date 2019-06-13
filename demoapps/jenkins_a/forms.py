from django import forms


def config_xml_valid(value):
    if value.name[-3:]!= 'xml':
        raise forms.ValidationError("配置文件格式不正确，not xml")


class JobConfForm(forms.Form):
    name = forms.CharField(label='项目名称',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    config_xml = forms.FileField(label='配置文件', validators=[config_xml_valid])
