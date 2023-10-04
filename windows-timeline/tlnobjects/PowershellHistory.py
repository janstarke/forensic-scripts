from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename="powershell_history.csv",
    datasource="powershell_history",
    attributes=["mtime", "command", "username", "user_id", "source"],
    timestamp="mtime"
)
class PowershellHistory(AbstractExportableItem):
    pass
