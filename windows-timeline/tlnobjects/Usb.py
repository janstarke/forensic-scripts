from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename = "usb",
    attributes=["last_insert", "last_removal", "info_origin"],
    timestamp="last_removal"
)
class Usb(AbstractExportableItem):
    def __init__(self, t: Target):
        super(Usb, self).__init__([u for u in t.usb()])
