from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename="users",
    datasource="users",
    attributes=['name', 'sid', 'home', 'domain', 'hostname'],
    timestamp=None
)
class WindowsUser(AbstractExportableItem):
    pass
