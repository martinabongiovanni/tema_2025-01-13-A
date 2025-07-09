import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_localization(self):
        localizations = self._model.get_all_localization()
        for localization in localizations:
            self._view.dd_localization.options.append(ft.dropdown.Option(localization))

    def handle_graph(self, e):
        try:
            localization = self._view.dd_localization.value
            if localization is None:
                self._view.create_alert("Attenzione! Selezionare un tipo di localization.")
                return

            nNodes, nEdges = self._model.build_graph(localization)

            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Creato grafo con {nNodes} nodi e {nEdges} archi."))
            for edge in self._model.get_info_edges():
                self._view.txt_result.controls.append(ft.Text(f"{edge[0]} <-> {edge[1]}: peso {edge[2]}"))
        finally:
            if self._view.dd_localization.value is not None:
                self._view.dd_localization.disabled = True
                self._view.btn_graph.disabled = True
                self._view.btn_analizza_grafo.disabled = False
                self._view.btn_path.disabled = False
                self._view.update_page()

    def analyze_graph(self, e):
        try:
            lista_all_componenti = self._model.get_componente_connessa()

            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Le componenti connesse sono:"))
            for lista in lista_all_componenti:
                self._view.txt_result.controls.append(ft.Text(f"{str(lista)} | dimensione componente: {len(lista)}"))
        finally:
            self._view.btn_analizza_grafo.disabled = True
            self._view.btn_path.disabled = False
            self._view.update_page()

    def handle_path(self, e):
        try:
            best_path = self._model.get_longest_path()

            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"la sequenza di cromosomi di lunghezza massima è:"))
            for element in best_path:
                self._view.txt_result.controls.append(ft.Text(f"{element.Chromosome}"))
        finally:
            self._view.btn_path.disabled = True
            self._view.update_page()

