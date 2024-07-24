from django import forms

class FileUploadForm(forms.Form):
    # setFile = forms.FileField(label='Drop .set file', widget=forms.ClearableFileInput(attrs={'accept': '.set'}))
    fifFile = forms.FileField(label='Drop .fdt file', widget=forms.ClearableFileInput(attrs={'accept': '.fif'}))
