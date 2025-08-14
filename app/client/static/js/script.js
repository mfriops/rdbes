function beautify(name){

    if (name.indexOf('_') > -1) {

        var beautify = name.replace(/_/g,' ');
        beautify = beautify.charAt(0).toUpperCase() + beautify.slice(1);

        for (let i = 0; i < name.length-1; i++) {
            if (name.charAt(i) == '_') {
                beautify = beautify.substring(0,i+1) + beautify.charAt(i+1).toUpperCase() + beautify.substring(i+2,name.length);
            }
        }
    } else {

        var beautify = name.charAt(0).toUpperCase() + name.slice(1);

        for (let i = name.length-1; i >= 0; i--) {
            if (name.charAt(i) == name.charAt(i).toUpperCase()) {
                beautify = beautify.substring(0,i) + ' ' + beautify.substring(i,2*name.length);
            }
        }
    }
    return beautify;
}
