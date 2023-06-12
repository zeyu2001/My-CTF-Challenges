# SEETF 2023

Here are the challenges I made for SEETF 2023, the inaugural CTF held by [Social Engineering Experts](https://ctftime.org/team/151372).

| Challenge                                           | Summary                                                                              | Category | Solves |
|-----------------------------------------------------|--------------------------------------------------------------------------------------|----------|--------|
| Shellcode As A Service                              | 6 bytes of shellcode, only open and read syscalls allowed                            | Pwn      |        |
| Express JavaScript Security                         | RCE through unrestricted options on latest version of EJS                            | Web      | test   |
| PlantUML                                            | 0day URL whitelist bypass to SSRF and local file read in latest version of PlantUML  | Web      |        |
| Sourceful Guessless Web                             | Making use of ini_set PHP directives to control assert callback and read local files | Web      |        |
| Star Cereal Episode 4: The Revenge of the Breakfast | 0day in serialize-javascript library + CSP bypass through www.youtube.com JSONP      | Web      |        |
| Mandatory Notes Challenge                           | Navigation XS-Leak challenge using Chrome's max URL length and long URL fragments    | Web      |        |
| Wasmabism                                           | WASM exploitation: buffer overflow to overwriting function pointers and XSS          | Web      |        |
| ezXXE                                               | A bunch of XXE regex bypasses                                                        | Web      |        |
| Now You C Me                                        | Custom HTTP server vulnerable to integer overflow, leading to client-side desync     | Web      |        |
| readonly                                            | Command injection in PEARcmd without needing a writeable filesystem                  | Web      |        |