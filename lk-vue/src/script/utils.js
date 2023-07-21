function _add_zero(oriTime) {
    return oriTime = oriTime.length === 2 ? oriTime : "0" + oriTime
}


function timeFormatConvert(timeInt) {
    const date = new Date(timeInt);
    const year = date.getFullYear().toString()
    let month = (date.getMonth() + 1).toString()
    let day = date.getDate().toString()
    let hours = date.getHours().toString()
    let minutes = date.getMinutes().toString()
    let seconds = date.getSeconds().toString()

    month = _add_zero(month)
    day = _add_zero(day)
    hours = _add_zero(hours)
    minutes = _add_zero(minutes)
    seconds = _add_zero(seconds)


    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

function getFileOriName(absName, mode){
    if (mode === "suffix"){
        return absName.slice(absName.lastIndexOf('.') + 1)
    }
    else if (mode === "name"){
        return absName.split("/").pop()
    }
}

function sizeFormat(s){
    let allUnit = ["bytes", "Kb", "Mb", "Gb"]
    let index = 0
    let unit = allUnit[index]

    while (true){
        if (s < 1024 || index === 4){break}
        s = s / 1024
        index ++
        unit = allUnit[index]
    }
    s = s.toFixed(4)
    return s + " " + unit
}

function convertToStringArray(str) {
    str = str.slice(1, -1);
    return str.split(',').map(function (element) {
        return element.trim().replace(/^"(.*)"$/, '$1');
    })
}


export {
    timeFormatConvert,
    getFileOriName,
    sizeFormat,
    convertToStringArray
}