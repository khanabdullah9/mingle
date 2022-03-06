from xml.dom import ValidationErr
from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password',
        'class':'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name','email','username','password']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']="Enter first name"
        self.fields['first_name'].widget.attrs['class']="form-control"

        self.fields['last_name'].widget.attrs['placeholder']="Enter last name"
        self.fields['last_name'].widget.attrs['class']="form-control"

        self.fields['email'].widget.attrs['placeholder']="Enter email"
        self.fields['email'].widget.attrs['class']="form-control"
        
        self.fields['username'].widget.attrs['class']="form-control"
        self.fields['username'].widget.attrs['placeholder']="Enter username"

    def clean(self):
        cleaned_data= super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')

        if password!=confirm_password:
            raise forms.ValidationError("Password and confirm password do not match!")

        for i in username:
            if i=='"' or i=="'" or i=="%" or i=="^" or i=="&" or i=="(" or i==")" or i=="-" or i=="+" or i=="=" or i=="~" or i=="`" or i=="<" or i==">":
                raise forms.ValidationError("Valid symbols for mingle username '!','@','#','$','.','|','_'")
