from exporter.abstracts import Exporter


class TXTExporter(Exporter):
    def export(self, content: str, **kwargs):
        with open(self.path, 'w') as file:
            file.write(content)

    @property
    def extension(self):
        return 'txt'
