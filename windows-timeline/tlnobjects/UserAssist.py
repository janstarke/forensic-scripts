from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename="userassist",
    datasource="userassist",
    attributes=["ts",
                "username",
                "path",
                "hostname",
                "domain",
                "number_of_executions",
                "application_focus_count",
                "regf_hive_path",
                "user_id"],
    timestamp="ts"
)
class UserAssist(AbstractExportableItem):
    pass
