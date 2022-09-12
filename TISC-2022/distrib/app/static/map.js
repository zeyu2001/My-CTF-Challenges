const make_map = (cityname, dom_id) => {
    chart = echarts.init(document.getElementById(dom_id));
    let option = {
        backgroundColor: "#000",
        series: [
            {
                "mapType": "Singapore",
                "data": [
                    { name: 'Central Singapore', value: 2 },
                    { name: 'North East Singapore', value: 1 },
                    { name: 'North West Singapore', value: 2 },
                    { name: 'South East Singapore', value: 0 },
                    { name: 'South West Singapore', value: 1 },
                ],
                "name": "",
                "symbol": "circle",
                "type": "map",
                "roam": false,
                "label": {
                  "textStyle": {
                    "color": "#fff"
                  },
                  "color": "#fff",
                  "show": false
                },
                "itemStyle": {
                  "areaColor": "#323c48",
                  "borderColor": "#111",
                  "textStyle": {
                    "color": "#fff"
                  },
                  "borderWidth": 0.5
                },
                "emphasis": {
                  "itemStyle": {
                    "areaColor": "#323c48",
                    "textStyle": {
                      "color": "#fff"
                    }
                  },
                  "label": {
                    "show": true,
                    "color": "#fff"
                  }
                },
                "map": "Singapore",
                "z": 2,
                "coordinateSystem": "geo",
                "left": "center",
                "top": "center",
                "aspectScale": null,
                "showLegendSymbol": true,
                "boundingCoords": null,
                "center": null,
                "zoom": 1,
                "scaleLimit": null,
                "selectedMode": true,
                "select": {
                  "label": {
                    "show": true,
                    "color": "#fff"
                  },
                  "itemStyle": {
                    "color": "#323c48"
                  }
                },
            }
        ],
        visualMap: {
            left: 'right',
            min: 0,
            max: 2,
            inRange: {
                color: [
                    '#031BBB',
                    '#FFA500',
                    '#DC143C'
                ]
            },
            text: ['Fully Compromised', 'Partially Compromised', 'Neutral'],
            calculable: true
        }
    };
    chart.setOption(option);
}

make_map('Singapore', 'map-container');