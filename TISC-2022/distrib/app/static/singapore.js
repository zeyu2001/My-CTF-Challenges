(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['exports', 'echarts'], factory);
    } else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {
        factory(exports, require('echarts'));
    } else {
        factory({}, root.echarts);
    }
}(this, function(exports, echarts) {
    var log = function(msg) {
        if (typeof console !== 'undefined') {
            console && console.error && console.error(msg);
        }
    };
    if (!echarts) {
        log('ECharts is not Loaded');
        return;
    }
    if (!echarts.registerMap) {
        log('ECharts Map is not loaded');
        return;
    }
    echarts.registerMap('Singapore', {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {
                "name": "Central Singapore"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": ["@@dbFVa\\\\`JXGfTrPHPOX@TXhNbU@ISWSiA[_@GcLkZUMMAqJMAIWQOJMKY@OGYFL\\WDYNDb"],
                "encodeOffsets": [
                    [106287, 1337]
                ]
            }
        }, {
            "type": "Feature",
            "properties": {
                "name": "North East Singapore"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": ["@@B\\TjTX\\LjcN[VMbCTJFQacFM]QYBGSM@iQ[^GVMAMNDX"],
                "encodeOffsets": [
                    [106370, 1403]
                ]
            }
        }, {
            "type": "Feature",
            "properties": {
                "name": "North West Singapore"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": ["@@TV|hbFTElW\\kCUSWW@OPOGSqHeIW[_b[EUcaaP]V@RVFO|WrA~NRBT"],
                "encodeOffsets": [
                    [106253, 1473]
                ]
            }
        }, {
            "type": "Feature",
            "properties": {
                "name": "South East Singapore"
            },
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    ["@@CWNMNBHU\\]jRN@HTZA^RENbdERBLVBZGTiJDfSAMSgBe[CQGaN[A­]mOeYEBINBrNNYVKlHd`@"],
                    ["@@]DITJVbaCZ|NXIVOJQKmuUetKH"],
                    ["@@WPUJPPjS\\DlEAMWCKI[EQN"]
                ],
                "encodeOffsets": [
                    [
                        [106370, 1403]
                    ],
                    [
                        [106526, 1441]
                    ],
                    [
                        [106446, 1441]
                    ]
                ]
            }
        }, {
            "type": "Feature",
            "properties": {
                "name": "South West Singapore"
            },
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    ["@@ZH@SYL"],
                    ["@@]VRFTKjGUW[P"],
                    ["@@TJLU_L"],
                    ["@@XB@SKEKX"],
                    ["@@T@diaSOAeQCRQPJ{[UONBVYtxfXBW]XDV^JA"],
                    ["@@ASMQB}XqP{UE@Q^UbOCaZMXCK[MESRSaMHP^QNMYiZLJZMFJoZuNCGcFyMOM{xCG^uSMCQaOKULYSAE`JHKVZhELj´r@ZRLNddLd^b@POXIZB"]
                ],
                "encodeOffsets": [
                    [
                        [106316, 1291]
                    ],
                    [
                        [106316, 1277]
                    ],
                    [
                        [106201, 1238]
                    ],
                    [
                        [106260, 1238]
                    ],
                    [
                        [106201, 1323]
                    ],
                    [
                        [106253, 1473]
                    ]
                ]
            }
        }],
        "UTF8Encoding": true
    });
}));