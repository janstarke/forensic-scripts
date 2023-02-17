# forensics
Collection of useful forensic scripts

| Topic | Tool | Task |
|-|-|-|
|LNK-Files | `lnk2bodyfile.py` | creates a bodyfile line from an LNK file. This tool can read multiple LNK files at once and thus can create of timeline of file accesses |
|Outlook | `ost2bodyfile.py` | creates a bodyfile from an OST file (creation, modification and access of mails and other items) |
|Outlook | `ostcat.py` | prints the contents of an item stored in an OST file. Use the item id to select the item |
|Outlook | `ostgrep.py` | grep in an OST file using regular expressions. This scripts greps in the contents of mails, but currently not in the subject. As a result, subject and mail id are being displayed. |