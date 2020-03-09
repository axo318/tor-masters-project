class Debug:
    def show(self, *msg):
        intro = str(self.__class__.__name__)
        final = '['+intro+']:'
        print(final, *msg)
