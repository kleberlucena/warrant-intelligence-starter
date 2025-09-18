# dashboard/views.py
from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy
import pandas as pd

from .forms import ImportCSVForm
from warrants.services.importer import import_from_dataframe
from django.views.generic import TemplateView, View, ListView
from django.http import HttpResponse
from people.models import Person

class HomeView(TemplateView):
    template_name = "dashboard/home.html"
    extra_context = {"page_title": "Dashboard – WIS"}

class HealthcheckView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("ok")

class MapView(TemplateView):
    template_name = "dashboard/map.html"
    extra_context = {"page_title": "Mapa de Mandados"}

class PeopleListView(ListView):
    model = Person
    template_name = "dashboard/people_list.html"
    context_object_name = "people"
    paginate_by = 20


###### IMPORTAÇÃO ####

class ImportDataView(FormView):
    template_name = "dashboard/import.html"
    form_class = ImportCSVForm
    success_url = reverse_lazy("dashboard:importar")

    def form_valid(self, form):
        f = form.cleaned_data["file"]
        sep = form.cleaned_data["sep"]
        encoding = form.cleaned_data["encoding"]
        dry_run = form.cleaned_data["dry_run"]
        preview_rows = form.cleaned_data["preview_rows"]

        try:
            # lê o CSV diretamente do arquivo enviado (InMemoryUploadedFile)
            df = pd.read_csv(f, sep=sep, encoding=encoding)
        except Exception as e:
            messages.error(self.request, f"Erro lendo CSV: {e}")
            return self.form_invalid(form)

        # gera preview
        preview = df.head(preview_rows).to_dict(orient="records") if preview_rows else []

        # executa import (dry_run opcional)
        try:
            summary = import_from_dataframe(df, dry_run=dry_run)
        except Exception as e:
            messages.error(self.request, f"Erro na importação: {e}")
            return self.form_invalid(form)

        # guarda dados no context via session (ou use extra_context)
        self.request.session["import_preview"] = preview
        self.request.session["import_summary"] = summary

        if dry_run:
            messages.info(self.request, "Simulação concluída. Nenhum dado foi gravado.")
        else:
            messages.success(self.request, "Importação concluída com sucesso.")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Importar dados (CSV)"
        ctx["preview"] = self.request.session.pop("import_preview", None)
        ctx["summary"] = self.request.session.pop("import_summary", None)
        return ctx