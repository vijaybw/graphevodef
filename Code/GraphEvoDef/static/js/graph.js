   /*!
    * Copyright 2019 - present Rakan Alanazi
    * https://github.com/RakanAlanazi
    *
    * Date: 2020-09-07
    */
   var parts = window.location.pathname.toString().split('/');
   var project = parts[parts.length - 2]
   console.log('project: ' + project)
   var versionselected = ''
   var base_url = "/graph/" + project
   var base_graph_url = base_url
   var state = parts[parts.length - 1]
   console.log('state: ' + state)

   var network = null;
   var graphData = null
   var options = null

   var highlightActive = false;
   var nodes = new vis.DataSet();
   var edgeSet = new vis.DataSet();
   var first = 0

   $(document).ready(function() {

        document.querySelector('#selectedversion').addEventListener('change', versiongraph);
        //Load this for the first time.
        if(first == 0)
        {
            first = 1
            versiongraph()
        }
   });

    function versiongraph()
    {
        versionselected = $('#selectedversion option:selected').val()

         if (versionselected.length > 0) {
            base_graph_url = base_url + '/' + versionselected
             console.log('stx:' + state)
            //state = 'Loaded'
            console.log('verurlnext:' + versionselected)
            console.log('url:' + base_graph_url)
             deselectNode();
           $.ajax({
               type: "GET",
               cache: false,
               dataType: "json",
               url: base_graph_url,

               success: function(data) {

                  network = null;
                  graphData = null
                  options = null

                   nodes = new vis.DataSet();
                   edgeSet = new vis.DataSet();


                   nodes.add(Object.values(data.nodes))
                   edgeSet.add(Object.values(data.edges))
                    console.log('stx1:' + state)
                   if (state === 'True') {

                       options = {
                           height: Math.round($(window).height() * 1) + 'px',
                           		layout: {
                                improvedLayout: false
                            },
                           // nodes: {
                           //   shapeProperties: {
                           //     interpolation: false    // 'true' for intensive zooming
                            //  }
                          //  },
                           // physics: {
                           //     stabilization: false
                           // },
                           interaction: {
                               keyboard: true,
                               hover: false
                           },
                         //  groups: {
                          //     red: {color:{background:'red'}},
                           //    blue: {color:{background:'blue'}},
                           //    lightblue: {color:{background:'lightblue'}},
                           //    lightred: {color:{background:'orange'}}
                          // }
                       };
                    // alert(options);
                   } else {
                       options = {
                           height: Math.round($(window).height() * 1) + 'px',
                           		layout: {
                                improvedLayout: false
                            },
                           //nodes: {
                           //   shapeProperties: {
                           //     interpolation: false    // 'true' for intensive zooming
                           //   }
                           // },
                            physics: {
                                enabled: false,
                               
                          },
                           interaction: {
                               keyboard: true,
                               hover: false
                           },
                         //  groups: {
                         //      red: {color:{background:'red'}},
                          //     blue: {color:{background:'blue'}},
                           //    lightblue: {color:{background:'lightblue'}},
                            //   lightred: {color:{background:'orange'}}
                           //}
                       };

                       // alert(options);
                   }
                   graphData = {
                       nodes: nodes,
                       edges: edgeSet
                   }
                   var myDiv = document.getElementById("mynetwork");
                   draw(graphData, myDiv)

               }

           });
            }
    }

  

   function draw(graphData, Div) {

       network = new vis.Network(Div, graphData, options);

       allNodes = nodes.get({
           returnType: "Object"
       });
       allEdges = edgeSet.get({
           returnType: "Object"
       });

       //bkpAllNodes = nodes.get({
       //    returnType: "Object"
       //});
       //bkpAllEdges = edgeSet.get({
       //    returnType: "Object"
       //});

       loadingProgress(network)
       navigation(network)
       document.querySelector('#search').addEventListener('input', nodeSearch);


       network.on("selectNode", function(params) {
           setTimeout(function() {
               selectNode(nodes.get(params.nodes[0]));
           }, 1);
       });

       network.on("deselectNode", function(params) {
           deselectNode();
       });

       network.on("click", neighbourhoodHighlight);

   }

   function loadingProgress(network) {

       network.on("stabilizationProgress", function(params) {
           document.title = 'Graph | ' + Math.round(params.iterations / params.total * 100) + "%";

       });

       network.on("stabilizationIterationsDone", function(params) {
           network.storePositions();
           console.log("saved data")


           network.setOptions({
               height: Math.round($(window).height() * 1) + 'px',
                    layout: {
                    improvedLayout: false
                },
                nodes: {
                  shapeProperties: {
                    interpolation: false    // 'true' for intensive zooming
                  }
                },
                  // physics:{
                  //   stabilization:false
                  //  },
               interaction: {
                   keyboard: true,
                   hover: false
               },
           });
           document.title = "Graph | loaded "
           var nz = nodes.get({
               returnType: "Object"
           });
           var ez = edgeSet.get({
               returnType: "Object"
           });
           var graphData = {
               nodes: nz,
               edges: ez
           }

           $.ajax({
               type: "POST",
               dataType: "json",
               contentType: "application/json",
               url: base_graph_url,
               data: JSON.stringify(graphData),
               context: this,

               success: function(data) {

               }

           });


       });


   }

   function navigation(network) {

       document.querySelector('#zoomin').addEventListener('click', function() {
           network.moveTo({
               'scale': network.getScale() * 2,
               animation: {
                   duration: 300
               }
           });
       });

       document.querySelector('#zoomout').addEventListener('click', function() {
           network.moveTo({
               'scale': network.getScale() * 0.5,
               animation: {
                   duration: 300
               }
           });
       });

       document.querySelector('#zoomfit').addEventListener('click', function() {
           network.fit({
               animation: {
                   duration: 300
               }
           });
       });


   }

   function deselectNode() {
       document.querySelector('#nodeCard').className = "card animated zoomOut";
       deselectTimeout = setTimeout(function() {
           document.getElementById("nodeCard").style.display = "none";

       }, 1);
   }

   function selectNode(node) {
       document.getElementById("nodeCard").style.display = "block";
       document.querySelector('#nodeCard').className = "card animated zoomIn";

       if(node.title.toString().includes(":"))
       {
           var nodeClass = node.title.toString().split(":")[0];
           var nodeFunction = node.title.toString().split(":")[1];

           document.getElementById("nodeClass").innerHTML = nodeClass;
           document.getElementById("nodeFunction").innerHTML = nodeFunction;

           var myStringArrayLabels = ["DEFECT_CNT","PORTRAIT","WMC","DIT","NOC","CBO","RFC","LCOM","Ca","Ce","NPM","LCOM3","LOC","DAM","MOA","MFA","CAM","IC","CBM","AMC","AVG_CC","MAX_CC","NEWONE"];
           var myStringArrayValues = [node.DEFECT_CNT,node.PORTRAIT,node.WMC,node.DIT,node.NOC,node.CBO,node.RFC,node.LCOM,node.Ca,node.Ce,node.NPM,node.LCOM3,node.LOC,node.DAM,node.MOA,node.MFA,node.CAM,node.IC,node.CBM,node.AMC,node.AVG_CC,node.MAX_CC,node.NEWONE];
            var arrayLength = myStringArrayLabels.length;
            var myString = "<table class=\"table\"><tbody>";

            for (var i = 0; i < arrayLength; i++) {

                  myString += "<tr>";
                  myString += "<th scope=\"row\">" + myStringArrayLabels[i] + "</th>";
                  myString += "<td id='td"+i+"'>" + myStringArrayValues[i] + "</td>";
                  myString += "</tr>";
            }

            myString += "</tbody></table>";
            document.getElementById('functionKpiTable').innerHTML = myString;

       }
       else
       {
           document.getElementById("nodeClass").innerHTML = node.label;
       }
   }

  
   function neighbourhoodHighlight(params) {
    // if something is selected:
    if (params.nodes.length > 0) {
      highlightActive = true;
      var i,j;
      var selectedNode = params.nodes[0];
      var degrees = 2;

      // mark all nodes as hard to read.
      for (var nodeId in allNodes) {
        allNodes[nodeId].color = 'rgba(200,200,200,0.5)';
        if (allNodes[nodeId].hiddenLabel === undefined) {
          allNodes[nodeId].hiddenLabel = allNodes[nodeId].label;
          allNodes[nodeId].label = undefined;
        }
      }

    //  for (var edgeId in allEdges) {

  //      allEdges[edgeId].color = 'rgba(200,200,200,0.5)';
     
//}
      var connectedNodes = network.getConnectedNodes(selectedNode);
      var allConnectedNodes = [];

      // get the second degree nodes
      for (i = 1; i < degrees; i++) {
        for (j = 0; j < connectedNodes.length; j++) {
          allConnectedNodes = allConnectedNodes.concat(network.getConnectedNodes(connectedNodes[j]));
        }
      }

      // all second degree nodes get a different color and their label back
      for (i = 0; i < allConnectedNodes.length; i++) {
        allNodes[allConnectedNodes[i]].color = 'rgba(150,150,150,0.75)';
        if (allNodes[allConnectedNodes[i]].hiddenLabel !== undefined) {
          allNodes[allConnectedNodes[i]].label = allNodes[allConnectedNodes[i]].hiddenLabel;
          allNodes[allConnectedNodes[i]].hiddenLabel = undefined;
        }
      }

      // all first degree nodes get their own color and their label back
      for (i = 0; i < connectedNodes.length; i++) {
        allNodes[connectedNodes[i]].color = undefined;
        if (allNodes[connectedNodes[i]].hiddenLabel !== undefined) {
          allNodes[connectedNodes[i]].label = allNodes[connectedNodes[i]].hiddenLabel;
          allNodes[connectedNodes[i]].hiddenLabel = undefined;
        }
      }

      // the main node gets its own color and its label back.
      allNodes[selectedNode].color = undefined;
      if (allNodes[selectedNode].hiddenLabel !== undefined) {
        allNodes[selectedNode].label = allNodes[selectedNode].hiddenLabel;
        allNodes[selectedNode].hiddenLabel = undefined;
      }
    }
    else if (highlightActive === true) {
      // reset all nodes
      for (var nodeId in allNodes) {
        allNodes[nodeId].color = undefined;
        if (allNodes[nodeId].hiddenLabel !== undefined) {
          allNodes[nodeId].label = allNodes[nodeId].hiddenLabel;
          allNodes[nodeId].hiddenLabel = undefined;
        }
      }
     /// for (var edgeId in allEdges) {
    //     allEdges[edgeId].color = null;
       
    //  }
      highlightActive = false
    }

    var updateArray = [];
    for (nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
         
   // var updateArrayEdges = [];
    //for (edgeId in allEdges) {
    //if (allEdges.hasOwnProperty(edgeId)) {
    //updateArrayEdges.push(allEdges[edgeId]);
  ////  }
   // }
    //edgeSet.update(updateArrayEdges);
    nodes.update(updateArray);
  }


   function nodeSearch() {
    //if (highlightActive === true) {
     //   // reset all nodes
      //  for (var nodeIdx in allNodes) {
      //      allNodes[nodeIdx].color = undefined;
      //      if (allNodes[nodeIdx].hiddenLabel !== undefined) {
       //         allNodes[nodeIdx].label = allNodes[nodeIdx].hiddenLabel;
       //         allNodes[nodeIdx].hiddenLabel = undefined;
       //     }
       // }
       // highlightActive = false;
   // }       
    let nodeId = document.getElementById("search").value;
       for (let node of nodes.get()) {
          if (node.id == nodeId) {
             network.selectNodes([ node.id ]);
             selectNode(node);
                  
            network.focus(node.id, {
                scale : Math.log(nodes.length/2),
                //locked : false,
                animation : {duration : 300}
             });
          }
       }
   
    }