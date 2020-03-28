from PipHome.PipFrame import PipFrame


class PipTab(PipFrame):
    def __init__(self, notebook, **kw):
        super().__init__(notebook, **kw)
        self.notebook = notebook
