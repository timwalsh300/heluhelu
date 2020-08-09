from django import forms
    
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
