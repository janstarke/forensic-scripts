from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename="users",
    attributes=['name', 'sid', 'home', 'domain', 'hostname'],
    timestamp=None
)
class WindowsUser(AbstractExportableItem):
    def __init__(self, t: Target):
        super(WindowsUser, self).__init__([u for u in t.users()])
