import os
import pathlib

from fpdf import FPDF

from exporter.abstracts import Exporter

HERE = pathlib.Path(__file__).parent


class PDFExporter(Exporter):
    def export(self, content: str, **kwargs):
        font_size = kwargs.get('font_size', 12)
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('Onuava', '', os.path.join(HERE, '../assets/fonts/onuava__.ttf'), uni=True)
        pdf.set_font('Onuava', size=font_size)
        pdf.multi_cell(0, 10, content)
        pdf.output(self.path, 'F')

    @property
    def extension(self):
        return 'pdf'
