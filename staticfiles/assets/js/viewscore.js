var x = ["Q1", "Q2", "Q3", "Q4", "Q", 
            "Q6", "Q7", "Q8", "Q9", "Q10"
        ];
var y = [10,20,30,40,50,60,70,80,90];

Plotly.plot('graph', [{
    x: x,
    y: y,
    type: 'bar'
}], 
{
  
}, 
{
    modeBarButtons: [[{
        name: 'June',
        click: function() {
          Plotly.relayout('graph',
            'xaxis.range', 
            [
              new Date(2015, 05, 1).getTime(),
              new Date(2015, 05, 31).getTime()
            ]
          );
        }
      }, {
        name: 'Q2',
        click: function() {
          Plotly.relayout('graph',
            'xaxis.range', 
            [
              new Date(2015, 06, 1).getTime(),
              new Date(2015, 06, 31).getTime()
            ]
          );
        }
      }
    ]]
}
);