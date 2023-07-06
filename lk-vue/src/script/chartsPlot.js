import * as echarts from "echarts"


function doBoxPlot(itemInfo) {
    const option = {
        title: {
            text: 'Boxplot -> ' + itemInfo.fileName,
            left: "center"
        },
        xAxis: {
            type: 'category',
            data: itemInfo.cols
        },
        yAxis: {
            type: 'value',
            splitArea: {
                show: true
            }
        },
        series: [
            {
                name: "boxplot",
                type: "boxplot",
                data: itemInfo.allData
            }
        ]
    }
    return option
}

function doHeatmapPlot(itemInfo) {
    const option = {
        title: {
            text: 'Heatmap -> ' + itemInfo.fileName,
            left: "center"
        },
        visualMap: {
            min: 0,
            max: 10,
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '15%'
        },
        xAxis: {
            type: "category",
            data: itemInfo.cols
        },
        yAxis: {
            type: "category",
            data: itemInfo.cols
        },
        series: [
            {
                type: "heatmap",
                data: itemInfo.allData,
                label: {show: true},
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ],
    }
    return option
}


export {
    doBoxPlot,
    doHeatmapPlot
}