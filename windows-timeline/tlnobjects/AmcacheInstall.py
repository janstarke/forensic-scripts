from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename = "amcache_install",
    attributes=["last_insert", "last_removal", "info_origin"],
    timestamp="last_removal"
)
class AmcacheInstall(AbstractExportableItem):
    def __init__(self, t: Target):
        super(AmcacheInstall, self).__init__([u for u in t.amcache_install()])
