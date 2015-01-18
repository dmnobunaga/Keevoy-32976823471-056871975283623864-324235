$(function(){
    /* Moment */
    moment.locale('ru');
    /* reportrange */
    if($("#reportrange").length > 0){   
        $("#reportrange").daterangepicker({                    
            ranges: {
               'Сегодня': [moment(), moment()],
               'Вчера': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
               'За 7 дней': [moment().subtract(6, 'days'), moment()],
               'За 30 дней': [moment().subtract(29, 'days'), moment()],
               'Этот месяц': [moment().startOf('month'), moment().endOf('month')],
               'Предыдущий Месяц': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            },
            opens: 'left',
            buttonClasses: ['btn btn-default'],
            applyClass: 'btn-small btn-primary',
            cancelClass: 'btn-small',
            format: 'MM.DD.YYYY',
            separator: ' to ',
            startDate: moment().subtract('days', 29),
            endDate: moment()            
          },function(start, end) {
              $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        });
        
        $("#reportrange span").html(moment().subtract('days', 29).format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));
    }
    /* end reportrange */

    /* Donut dashboard chart */
    Morris.Donut({
        element: 'dashboard-donut-1',
        data: [
            {label: "Новые", value: 2513},
            {label: "Вернувшиеся", value: 764},
            {label: "Клиенты", value: 311}
        ],
        colors: ['#33414E', '#3FBAE4', '#FEA223'],
        resize: true
    });
    /* END Donut dashboard chart */
    
    /* Bar dashboard chart */
    Morris.Bar({
        element: 'dashboard-bar-1',
        data: [
            { y: 'Oct 10', a: 75, b: 35 },
            { y: 'Oct 11', a: 64, b: 26 },
            { y: 'Oct 12', a: 78, b: 39 },
            { y: 'Oct 13', a: 82, b: 34 },
            { y: 'Oct 14', a: 86, b: 39 },
            { y: 'Oct 15', a: 94, b: 40 },
            { y: 'Oct 16', a: 96, b: 41 }
        ],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Покупатели', 'Посетители'],
        barColors: ['#33414E', '#3FBAE4'],
        gridTextSize: '10px',
        hideHover: true,
        resize: true,
        gridLineColor: '#E5E5E5'
    });
    /* END Bar dashboard chart */
    
    /* Line dashboard chart */
    Morris.Line({
      element: 'dashboard-line-1',
      data: [
        { y: '2015-06-01', a: 1,b: 40},
        { y: '2015-07-01', a: 1,b: 60},
        { y: '2015-08-01', a: 1,b: 70},
        { y: '2015-09-01', a: 2,b: 240},
        { y: '2015-10-01', a: 2,b: 250},
        { y: '2015-11-01', a: 4,b: 460},
        { y: '2015-12-01', a: 6,b: 720},
        { y: '2016-01-01', a: 3,b: 920}
      ],
      xkey: 'y',
      ykeys: ['a','b'],
      labels: ['Кампании','Продажи'],
      resize: true,
      xLabels: 'day',
      gridTextSize: '10px',
      lineColors: ['#3FBAE4','#33414E'],
      gridLineColor: '#E5E5E5'
    });   
    /* EMD Line dashboard chart */
    
    /* Vector Map */

    jQuery('#dashboard-map-sales').vectorMap(
        {
            map: 'russia_en',
            backgroundColor: '#fff',
            color: '#eee',
            hoverOpacity: 0.7,
            selectedColor: '#999999',
            enableZoom: true,
            showTooltip: true,
            scaleColors: ['#C8EEFF', '#006491'],
            values: {'mc':'75','le':'20','cl':'3','or':'1','pe':'1','kr':'0.1','sh':'0.1','sa':'0.7'},
            normalizeFunction: 'polynomial'
        });
    /* END Vector Map */


    /* Rickshaw dashboard chart */
    var seriesData = [ [], [] ];
    var random = new Rickshaw.Fixtures.RandomData(1000);

    for(var i = 0; i < 100; i++) {
        random.addData(seriesData);
    }

    var rdc = new Rickshaw.Graph( {
        element: document.getElementById("dashboard-chart"),
        renderer: 'area',
        width: $("#dashboard-chart").width(),
        height: 250,
        series: [{color: "#33414E",data: seriesData[0],name: 'Новых'},
            {color: "#3FBAE4",data: seriesData[1],name: 'Вернулось'}]
    } );

    rdc.render();

    var legend = new Rickshaw.Graph.Legend({graph: rdc, element: document.getElementById('dashboard-legend')});
    var shelving = new Rickshaw.Graph.Behavior.Series.Toggle({graph: rdc,legend: legend});
    var order = new Rickshaw.Graph.Behavior.Series.Order({graph: rdc,legend: legend});
    var highlight = new Rickshaw.Graph.Behavior.Series.Highlight( {graph: rdc,legend: legend} );

    var rdc_resize = function() {
        rdc.configure({
            width: $("#dashboard-chart").width(),
            height: $("#dashboard-chart").height()
        });
        rdc.render();
    };

    var hoverDetail = new Rickshaw.Graph.HoverDetail({graph: rdc});

    window.addEventListener('resize', rdc_resize);

    rdc_resize();
    /* END Rickshaw dashboard chart */

    $(".x-navigation-minimize").on("click",function(){
        setTimeout(function(){
            rdc_resize();
        },200);    
    });
    
    
});

