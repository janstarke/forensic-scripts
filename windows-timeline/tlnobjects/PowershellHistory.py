from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename="powershell_history.csv",
    datasource="powershell_history",
    attributes=["last_insert", "last_removal", "info_origin"],
    timestamp="last_removal"
)
class PowershellHistory(AbstractExportableItem):
    pass
