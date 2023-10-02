from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename = "powershell_history.csv",
    attributes=["last_insert", "last_removal", "info_origin"],
    timestamp="last_removal"
)
class PowershellHistory(AbstractExportableItem):
    def __init__(self, t: Target):
        super(PowershellHistory, self).__init__([u for u in t.powershell_history()])
