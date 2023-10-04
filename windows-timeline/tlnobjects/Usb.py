from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename="usb",
    datasource="usb",
    attributes=["last_insert", "last_removal", "info_origin"],
    timestamp="last_removal"
)
class Usb(AbstractExportableItem):
    pass
