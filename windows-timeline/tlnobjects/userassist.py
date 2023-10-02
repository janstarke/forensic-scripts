from dissect.target import Target
from .exportable_item import ExportableItem, AbstractExportableItem


@ExportableItem(
    attributes=["ts", "hostname", "domain", "path", "number_of_executions", "application_focus_count", "regf_hive_path",
                "user_id", "username"],
    sort_by="ts"
)
class UserAssist(AbstractExportableItem):
    def __init__(self, t: Target):
        super(UserAssist, self).__init__([u for u in t.userassist()])

