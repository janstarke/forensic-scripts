from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename="amcache_install",
    datasource="amcache_install",
    attributes=["last_insert", "last_removal", "info_origin"],
    timestamp="last_removal"
)
class AmcacheInstall(AbstractExportableItem):
    pass
