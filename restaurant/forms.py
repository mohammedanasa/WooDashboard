from django import forms
from restaurant.models import *



class CategoryModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class ModifierModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class ModifierGroupModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = {'name','product',} 



class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2','placeholder':'Product Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'min-h-100px mb-2 ql-container ql-snow form-control'}),required=False)
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control mb-2','placeholder':'Product Price'}))
    category = CategoryModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select mb-2', 'data-placeholder':'Select an option','data-control':'select2'}),
        required=False
    )
    modifiergroup = ModifierGroupModelMultipleChoiceField(
        queryset=ModifierGroup.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select mb-2', 'data-placeholder':'Select an option','data-control':'select2'}),
        required=False
    )
    photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'type':'file','accept':".png, .jpg, .jpeg"}),required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price','category','modifiergroup','photo','is_active']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2','placeholder':'Category Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'min-h-200px mb-2 form-control','id':'kt_ecommerce_add_category_description'}),required=False)
    photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'type':'file','accept':".png, .jpg, .jpeg"}),required=False)
    class Meta:
        model = Category
        fields = ['name', 'description','photo']



class ModifierGroupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2','placeholder':'Modifier Group Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'min-h-200px mb-2 form-control','id':'kt_ecommerce_add_category_description'}),required=False)
    modifier = ModifierModelMultipleChoiceField(
        queryset=Modifier.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check form-check-inline mb-2','id':'inlineCheckbox1','type':'checkbox'}),
        required=True,
    )
    class Meta:
        model = ModifierGroup
        fields = ['name', 'description','modifier',]

class ModifierForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2','placeholder':'Modifier Name'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control mb-2','placeholder':'Modifier Price'}))
    modifiergroup = ModifierGroupModelMultipleChoiceField(
        queryset=ModifierGroup.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select mb-2', 'data-placeholder':'Select an option','data-control':'select2'}),
        required=False
    )
    
    class Meta:
        model = Modifier
        fields = ['name', 'price','modifiergroup',]

class MenuForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2','placeholder':'Menu Name'}))
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'min-h-200px mb-2 form-control'}),required=False)
    
    class Meta:
        model = Menu
        fields = ['name', 'description', 'category', 'is_active']

    
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['firstaddress', 'street', 'city', 'state', 'zip_code']
