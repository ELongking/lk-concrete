function _add_zero(oriTime){
    return oriTime = oriTime.length === 2 ? oriTime: "0" + oriTime
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


export {
    timeFormatConvert
}