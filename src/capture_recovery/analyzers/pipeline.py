class AnalyzerPipeline:

    def __init__(self, analyzers):

        self.analyzers = analyzers

    def run(self, reader, report):

        for analyzer in self.analyzers:

            reader.seek(0)

            analyzer.run(reader, report)