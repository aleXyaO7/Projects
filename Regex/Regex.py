import sys; args = sys.argv[1:]
t = int(args[0])-30
s = [
    r"/^0$|^10[01]$/",
    r"/^[01]*$/",
    r"/0$/",
    r"/\w*[aeiou]\w*[aeiou]\w*/i",
    r"/^1[01]*0$|^0$/",
    r"/^[01]*110[01]*$/",
    r"/^.{2,4}$/s",
    r"/^\d{3} *-? *\d\d *-? *\d{4}$/",
    r"/^.*?d\w*/mi",
    r"/^[01]?$|^0[01]*0$|^1[01]*1$/",
    
    r"/^[x.o]{64}$/i",
    r"/^[xo]*\.[xo]*$/i",
    r"/^(x+o*)?\.|\.(o*x+)?$/i",
    r"/^.(..)*$/s",
    r"/^(1?0|11)([01]{2})*$/",
    r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
    r"/^(1?0)*1*$/",
    r"/^\b[bc]*a?[bc]*$/",
    r"/^(b|c|a[bc]*a)+$/",
    r"/^(2[02]*|(1[02]*){2})+$/",

    r"/\w*(\w)\w*\1\w*/i",
    r"/\w*(\w)\w*(\1\w*){3}/i",
    r"/^([01])([01]*\1)?$/",
    r"/\b(?=\w*cat)\w{6}\b/i",
    r"/\b(?=\w*ing)(?=\w*bri)\w{5,9}\b/i",
    r"/\b(?!\w*cat)\w{6}\b/i",
    r"/\b((\w)(?!\w*\2))+\b/i",
    r"/^0*(1(?!0011)0*)*$/",
    r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
    r"/^0*(1(?!.1)0*)*$/",

    r"/^(0(?!10)|1)*$/",
    r"/^(0(?!10)|1(?!01))*$/",
    r"/^([01])([01]*\1)?$/",
    r"/\b(?!\w*(\w)\w*\1\b)\w+/i",
    r"/(?=\w*(\w)\w*((\w)\w*(\1\w*\3|\3\w*\1)|\1\w*(\w)\w*\5))\w*/i",
    r"/\b((\w)(?!\w*\2))*(\w)(((\w)(?!\w*\6))*\3){2,}((\w)(?!\w*\8))*\b/i",
    r"/\b(?!\w*([aeiou])\w*\1\w*)(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)\w+\b/i",
    r"/^(?=0*((10*){2})*$)[01]([01]{2})*$/",
    r"/^(?=(1(((00|11)*01){2}|(00|11)*10))?(00|11|(01|10)((00|11)*\7){2}|01(00|11)*10|10(00|11)*01)*$)(?!0.+)[01]+/",
    r"//",

    r"/(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u)^[a-z]*$/m",
    r"/(?=(.*[aeiou]){5})(?!(.*[aeiou]){6})^[a-z]*$/m",
    r"/(?=.*[^aeiou\n]w[^aeiou]{2})^[a-z]*$/m",  
    r"/^((?=(.)(.)(.))(?=.*\4\3\2$)[a-z]*|aa?)$/m",
    r"/(?=.*(bt|tb))(?!.*(b|t).*\2)^[a-z]*$/m",
    r"/^([a-z])+\1[a-z]*$/m",
    r"/^(?=.*(.)(.*\1){5})[a-z]*$/m",
    r"/^(?=.*((.)\2){3})[a-z]*$/m",
    r"/^(?=(.*[^aeiou\n]){13})[a-z]*$/m",
    r"/^(([a-z])(?!.*\2.*\2))*$/m",
]
if t < len(s):
    print(s[t])
#Alexander Yao, Period 4, 2023