from django import forms
from django.forms import ModelForm
from .models import Customer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CustomerForm(ModelForm):
    
    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', '更新 / 作成'))

class ModelManageForm(forms.Form):
    model_type = [
        ("customer", "得意先"),
        ("product", "商品"),
        ("deliv_dest", "納品先"),
        ("product_per_customer", "得意先別商品"),
    ]
    
    manage = [
        ("up", "取込"),
        ("down", "出力"),
    ]
    
    model_name = forms.ChoiceField(
        label='管理するマスタ', 
        choices = model_type
    )

    up_or_down = forms.ChoiceField(
        label='取込 or 出力', 
        choices = manage
    )

    data = forms.FileField(
        label='取込データ' 
    )

