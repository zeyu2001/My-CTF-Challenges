for (let charCode = 0; charCode < 65536; charCode++) {
    const char = String.fromCharCode(charCode);
    
    if (char.toLowerCase().length > 1) {
        console.log(char, charCode);
    }
}