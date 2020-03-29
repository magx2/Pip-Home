from PipHome.PipFrame import PipFrame


class PipTab(PipFrame):
    def __init__(self, notebook, config, **kw):
        super().__init__(notebook, config, **kw)
        self.notebook = notebook
