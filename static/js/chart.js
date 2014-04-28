function execute(){
  $.ajax({
  url: "/api/hour?start=3day",
  type: "GET",
  dataType: 'json',
  success: function(json){
    data = reOrder(json);
    console.log(data['datetime'][data['datetime'].length-1]);
    $("#now").text(data['datetime'][data['datetime'].length-1]);
    $(function (){
      $('#container1').highcharts({
        chart: { zoomType: 'x' },
        title: { text: '温度と紫外線' },
        xAxis: {
          type: 'datetime',
          tickInterval: 6 * 3600 * 1000,
          tickWidth: 0,
          gridLineWidth: 1
        },
        yAxis: [{
          title: { text: '温度(°C)' },
          max: 40,
          min: -10,
          plotLines:[{
            value: 0,
            width: 1,
            color: '#808080'
          }]
        },{
          title: { text: 'UV Index' },
          max: 20,
          min: 0,
          opposite: true,
          plotLines:[{
            value: 0,
            width: 1,
            color: '#808080'
          }]
        }],
        tooltip: {
          shared: true,
          crosshairs: true
        },
        series: [{
          type: 'spline',
          tooltip: { valueSuffix: '°C' },
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: '屋外温度',
          color: "#ffd700",
          data: data['outtemp']
        },{
          type: 'spline',
          tooltip: { valueSuffix: '°C' },
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: '室内温度',
          color: "#4169e1",
          data: data['intemp']
        },{
          type: 'spline',
          tooltip: { valueSuffix: '°C' },
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: '結露温度',
          data: data['dewpoint']
        },{
          type: 'column',
          yAxis: 1,
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: 'UV Index',
          color: "#ff0000",
          data: data['UV']
        }]
      });
      $('#container2').highcharts({
        chart: { zoomType: 'x' },
        title: { text: '湿度と降水量' },
        xAxis: {
          type: 'datetime',
          tickInterval: 6 * 3600 * 1000,
          tickWidth: 0,
          gridLineWidth: 1
        },
        yAxis: [{
          title: { text: '湿度(%)' },
          max: 100,
          min: 0,
          maxPadding: 0,
          minPadding: 0,
          plotLines:[{
            value: 0,
            width: 1,
            color: '#808080'
          }]
        },{
          title: { text: '降水量(mm)' },
          opposite: true,
          max: 100,
          min: 0
        }],
        tooltip: {
          shared: true,
          crosshairs: true
        },
        series: [{
          type: 'spline',
          tooltip: { valueSuffix: '%' },
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: '屋外湿度',
          color: "#ffd700",
          data: data['outhumidity']
        },{
          type: 'spline',
          tooltip: { valueSuffix: '%' },
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: '室内湿度',
          color: "#4169e1",
          data: data['inhumidity']
        },{
          type: 'column',
          yAxis: 1,
          tooltip: { valueSuffix: 'mm' },
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: '降水量',
          data: data['dayrain']
        }]
      });
      $('#container3').highcharts({
        chart: { zoomType: 'x' },
        title: { text: '風速・風向' },
        xAxis: {
          type: 'datetime',
          tickInterval: 6 * 3600 * 1000,
          tickWidth: 0,
          gridLineWidth: 1
        },
        yAxis:[{
          title: { text: '風速(m/s)' },
          max: 40,
          min: 0,
          plotLines:[{
            value: 0,
            width: 1,
            color: '#808080'
          }]
        },{
          title: { text: '風向(°)' },
          opposite: true,
          max: 360,
          min: 0
        }],
        tooltip: {
          shared: true,
          crosshairs: true
        },
        series: [{
          type: 'column',
          yAxis: 1,
          tooltip: { valueSuffix: '°' },
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: '風向',
          pointPadding: 0.5,
          data: data['winddir']
        },{
          type: 'line',
          tooltip: { valueSuffix: 'm/s' },
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: '平均風速',
          data: data['windspeed']
        },{
          type: 'line',
          tooltip: { valueSuffix: 'm/s' },
          pointStart: Date.parse(data['datetime'][0]),
          pointInterval: 60 * 60 * 1000,
          name: '瞬間最大風速',
          data: data['windgust']
        }],
      });
    });
  }
  });
}

function reOrder(data){
  var newData = new Object();
  for(var i = 0;i < data.length; i++ ){
    for(var k in data[i]){
      if(newData[k] != undefined){
        newData[k].push(data[i][k]);
      }else{
        newData[k] = new Array();
        newData[k].push(data[i][k]);
      }
    }
  }
  console.log(newData);
  return newData;
}
