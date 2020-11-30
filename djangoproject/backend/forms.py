from django import forms

class CreateForm(forms.Form):
    username = forms.CharField(label='Desired username')
    password1 = forms.CharField(label='Enter a password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Re-enter the password', widget=forms.PasswordInput)
    email = forms.CharField(label='Your email address')

    def clean_username(self):
        data = self.cleaned_data['username']
        return data
    def clean_password1(self):
        data = self.cleaned_data['password1']
        return data
    def clean_password2(self):
        data = self.cleaned_data['password2']
        return data
    def clean_email(self):
        data = self.cleaned_data['email']
        return data
    
class SearchForm(forms.Form):
    keywords = forms.CharField()

    def clean_keywords(self):
        data = self.cleaned_data['keywords']
        return data

class AddBooksForm(forms.Form):
    select_result_0 = forms.BooleanField(required=False)
    select_result_1 = forms.BooleanField(required=False)
    select_result_2 = forms.BooleanField(required=False)
    select_result_3 = forms.BooleanField(required=False)
    select_result_4 = forms.BooleanField(required=False)
    select_result_5 = forms.BooleanField(required=False)
    select_result_6 = forms.BooleanField(required=False)
    select_result_7 = forms.BooleanField(required=False)
    select_result_8 = forms.BooleanField(required=False)
    select_result_9 = forms.BooleanField(required=False)
