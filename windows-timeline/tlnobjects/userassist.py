import csv

from dissect.target import Target
from dissect.target.plugins.os.windows.regf import userassist

ATT_HOSTNAME = "hostname"
ATT_DOMAIN = "domain"
ATT_TIMESTAMP = "ts"
ATT_PATH = "path"
ATT_NUMBER_OF_EXECUTIONS = "number_of_executions"
ATT_APPLICATION_FOCUS_COUNT = "application_focus_count"
ATT_REGF_HIVE_PATH = "regf_hive_path"
ATT_USER_ID = "user_id"
ATT_USERNAME = "username"


class UserAssist:
    def __init__(self, t: Target):
        self.__entries = [u for u in t.userassist()]

    def to_csv(self, dst_file):
        self.__entries.sort(key=lambda entry: entry.__getattribute__(ATT_TIMESTAMP))
        writer = csv.DictWriter(dst_file, fieldnames=[
            ATT_TIMESTAMP,
            ATT_USERNAME,
            ATT_PATH,
            ATT_DOMAIN,
            ATT_HOSTNAME,
            ATT_USER_ID,
            ATT_NUMBER_OF_EXECUTIONS,
            ATT_APPLICATION_FOCUS_COUNT
        ])

        for entry in self.__entries:
            writer.writerow(
                {
                    ATT_TIMESTAMP: entry.__getattribute__(ATT_TIMESTAMP),
                    ATT_USERNAME: entry.__getattribute__(ATT_USERNAME),
                    ATT_PATH: entry.__getattribute__(ATT_PATH),
                    ATT_DOMAIN: entry.__getattribute__(ATT_DOMAIN),
                    ATT_HOSTNAME: entry.__getattribute__(ATT_HOSTNAME),
                    ATT_USER_ID: entry.__getattribute__(ATT_USER_ID),
                    ATT_NUMBER_OF_EXECUTIONS: entry.__getattribute__(ATT_NUMBER_OF_EXECUTIONS),
                    ATT_APPLICATION_FOCUS_COUNT: entry.__getattribute__(ATT_APPLICATION_FOCUS_COUNT)
                }
            )
