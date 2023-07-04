import * as XLSX from "xlsx";

async function readExcel(file){
    let res;
    try {
        res = await readXlsx(file);
        return res
    } catch (error) {
        console.log("Error reading Excel file:", error);
    }
}


function readXlsx(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        let excelRes;
        reader.onload = (e) => {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, {type: 'array'});
            const worksheet = workbook.Sheets[workbook.SheetNames[0]];

            let headers = []
            try {
                for (const cellAddress in worksheet) {
                    if (cellAddress[cellAddress.length - 1] === "1") {
                        headers.push(worksheet[cellAddress].v)
                    }
                }
                excelRes = {headers: headers, flag: true, msg: ""}
            } catch (e) {
                excelRes = {headers: headers, flag: false, msg: e.toString()}
            }
            resolve(excelRes)
        };

        reader.onerror = (e) => {
            reject(e);
        };
        reader.readAsArrayBuffer(file.raw);
    })
}


export {
    readExcel
}
