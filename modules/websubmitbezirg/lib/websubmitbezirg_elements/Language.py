class Language(VerticalPanel):
    def load(self):
        l = Label("Language:")
        c = ListBox()
        c.addItem("English")
        c.addItem("French")
        f = FileUpload()
        self.add(l)
        self.add(c)
        self.add(f)
