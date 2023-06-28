import * as XLSX from "xlsx";

function readXlsx(file) {
    const reader = new FileReader();
    let res = {}
    reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];

        let headers = []
        try {
            for (const cellAddress in worksheet) {
                if (cellAddress[0] === "A") {
                    headers.push(worksheet[cellAddress].v)
                }
            }
            res = {headers: headers, flag: true, msg: ""}
        } catch (e) {
            res =  {headers: headers, flag: false, msg: e.toString()}
        }
    };

    reader.readAsArrayBuffer(file.raw);
    return res
}


export {
    readXlsx
}
