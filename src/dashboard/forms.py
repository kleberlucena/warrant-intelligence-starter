# dashboard/forms.py
from django import forms

class ImportCSVForm(forms.Form):
    file = forms.FileField(
        label="Arquivo CSV",
        help_text="Use um CSV com cabeçalho: national_id,name,mother_name,birth_date,number,status,issued_at,court,lat,lon"
    )
    sep = forms.CharField(label="Separador", initial=",", max_length=3)
    encoding = forms.CharField(label="Encoding", initial="utf-8", max_length=32)
    dry_run = forms.BooleanField(label="Apenas simular (não gravar)", required=False)
    preview_rows = forms.IntegerField(label="Pré-visualizar (linhas)", initial=10, min_value=0, max_value=100)
