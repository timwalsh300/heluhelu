from django import forms
    
class SearchForm(forms.Form):
    keywords = forms.CharField()

    def clean_keywords(self):
        data = self.cleaned_data['keywords']
        return data
