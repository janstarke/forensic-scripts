from dissect.target import Target
from utils.ExportableItem import ExportableItem, AbstractExportableItem


@ExportableItem(
    filename="amcache_install",
    datasource="amcache_install",
    attributes=["start_time", "stop_time", "created", "modified", "access", "create", "filename", "longname", "path", "digests", "link_date"],
    timestamp="start_time"
)
class AmcacheInstall(AbstractExportableItem):
    pass
