
class CustomType(object):
    pass

class ImageShow(CustomType):

    def __init__(self,imname,ret) -> None:
        self.imname = imname
        self.ret = ret


    def json(self):
        return {
            'type':"imshow",
            "imname":self.imname,
            "repr":self.imname,
            "if_show":True
        }

class PrintShow(CustomType):

    def __init__(self,reinput) -> None:
        self.show = str(reinput)
        self.ret = reinput


    def json(self):
        return {
            'type':"print",
            "show":self.show,
            "repr":self.show,
            "if_show":True
        }