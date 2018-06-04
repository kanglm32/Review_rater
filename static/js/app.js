/* data route */
var url = '/barchart';


var select = document.querySelector('#selectModel');
var probabilities = " ";
var C_probs = " ";
d3.select('#selectModel')
  .on("change", function(){

      console.log('TEST')
      var sect = document.getElementById('selectModel')
      var section = sect.options[sect.selectedIndex].value;
      console.log(section);

       if (section == 'Deviations View'){
        console.log('Deviations View')
        Plotly.d3.json(url, function(error, response) {
          console.log(response);
          
      
          var trace3 = {
            type: 'bar',
            x: response.deviations_x,
            y: response.deviations_y,
            
            marker: {
              color: "#98abc5"
            }
          };
      
          var data2 = [trace3];
      
          var layout = {
            title: 'Deviation of Accuracy',
            xaxis:{
              title: "Rating Deviations"
            },
            yaxis:{
              title:"Count of Deviations"
            },
            
          };
      
          Plotly.newPlot('plot', data2, layout);
        });
      }

      if (section == 'Ratings View'){
        console.log('Ratings View')
        Plotly.d3.json(url, function(error, response) {
          console.log(response);
          
         var trace1 = {
            type: 'bar',
            x: response.human_rating_x,
            y: response.human_rating_y,
            
            marker: {
              color: "#8a89a6"
            },
            name: "Human Rating"
          };
      
          var trace2 = {
            type: 'bar',
            x: response.machine_rating_x,
            y: response.machine_rating_y,
            
            marker: {
              color: "#ff8c00"
            },
            name: "Machine Rating"
          };
      
          var data = [trace1, trace2];
      
          var layout = {
            title: 'Machine vs Human Ratings',
            xaxis:{
              title: "Rating"
            },
            yaxis:{
              title:"Count of Ratings"
            },
            
          };
      
          Plotly.newPlot('plot', data, layout);
        });
      }})