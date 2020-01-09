
from django import forms
from django.forms import ModelForm, inlineformset_factory
from crispy_forms.helper import FormHelper
from .models import Estimate_header, Estimate_detail
from django.core.exceptions import ObjectDoesNotExist
from io import TextIOWrapper
import csv



class ModelManageForm(forms.Form):
    model_type = [
        ("estimate_detail", "見積詳細"),
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


class ModelFormWithFormSetMixin:

    def __init__(self, *args, **kwargs):
        super(ModelFormWithFormSetMixin, self).__init__(*args, **kwargs)
        self.fields['customer'].label = False
        self.fields['created_date'].label = False
        self.fields['valid_date'].label = False
        self.fields['sls_prn'].label = False
        self.fields['sls_rep'].label = False
        self.fields['remarks_1'].label = False
        self.fields['remarks_2'].label = False
        self.fields['remarks_3'].label = False
        self.fields['remarks_4'].label = False
        self.fields['estimate_state'].label = False
        self.fields['customer_name'].label = False
        self.fields['wholesale_rate'].label = False
        self.fields['internal_remarks'].label = False

        self.helper = FormHelper()
        self.formset = self.formset_class(
            instance=self.instance,
            data=self.data if self.is_bound else None,
        )
        for formset in self.formset.forms:
            formset.fields['product'].label = False
            formset.fields['selling_price_new'].label = False
            formset.fields['wholesale_price_new'].label = False
            formset.fields['wholesale_rate'].label = False
            formset.fields['remarks'].label = False

        # self.formset.forms.fields['selling_price_new'].label = False

    def is_valid(self):
        return super(ModelFormWithFormSetMixin, self).is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        saved_instance = super(ModelFormWithFormSetMixin, self).save(commit)
        self.formset.save(commit)
        return saved_instance


class Estimate_detailForm(ModelForm):
    
    class Meta:
        model = Estimate_detail
        fields = ['estmt_no','product','selling_price_new',
        'wholesale_price_new','wholesale_rate','remarks']

    # def __init__(self, *args, **kwargs):
        # super(self).__init__(*args, **kwargs)
        # self.fields['selling_price_new'].label = False

Estimate_detailFormSet = inlineformset_factory(
        parent_model = Estimate_header, 
        model = Estimate_detail, 
        form = Estimate_detailForm,
        extra=5, 
        )

class Estimate_headerForm(ModelFormWithFormSetMixin, ModelForm):

    # 追加
    formset_class = Estimate_detailFormSet 

    class Meta:
        model = Estimate_header
        fields = '__all__'



class EstimateEditForm(forms.Form):

    form_class = inlineformset_factory(
            Estimate_header, 
            Estimate_detail, 
            fields = (
                'product', 
                'estimate_price',
                ),
            extra=3,
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        super(EstimateEditForm, self).__init__(*args, **kwargs)

