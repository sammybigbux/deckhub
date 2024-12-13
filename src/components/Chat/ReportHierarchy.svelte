<script>
  import * as d3 from "d3";
  import { onMount } from "svelte";

  export let scope = "strong"; // Scope can be "strong" or "weak"

  export let hierarchy = {
    "Section 1": {
      "Concept 1": ["Term 1", "Term 2"],
      "Concept 2": ["Term 3", "Term 4"],
    },
    "Section 2": {
      "Concept 3": ["Term 5", "Term 6"],
      "Concept 4": ["Term 7", "Term 8"],
    },
  };

  const layout_dict = 
    {
    "auto_scaling_dynamic_response_question": {
        "Dynamic Response": [
            "Predictive Scaling",
            "Scaling Cooldown",
            "Step Scaling"
        ],
        "? 1": [
            "? 2",
            "? 3"
        ]
    },
    "auto_scaling_monitoring_question": {
        "Monitoring and Metrics": [
            "CPU Utilization",
            "Custom Metrics",
            "Network In/Out"
        ],
        "? 4": [
            "? 5",
            "? 6"
        ],
        "? 7": [
            "? 8",
            "? 9",
            "? 10"
        ]
    },
    "cloudformation_costexplorer_question": {
        "AWS Cost Explorer and Anomaly Detection": [
            "AWS Cost Explorer",
            "AWS Cost Anomaly Detection",
            "? 12"
        ],
        "CloudFormation Use Case": [
            "CloudFormation",
            "? 11"
        ],
        "? 13": [
            "? 14",
        ]
    },
    "multi_account_management_question": {
        "Billing Consolidation and Cost Savings": [
            "Consolidated Billing",
            "Aggregated Usage",
            "Savings Plans"
        ],
        "Managing Multiple AWS Accounts": [
            "AWS Organizations",
            "Management Account",
            "Member Account",
            "? 100"
        ],
        "Organizing Accounts Using OUs": [
            "Organizational Units (OUs)",
        ]
    },
    "scp_security_compliance_question": {
        "Applying SCPs for Security and Compliance": [
            "Service Control Policies (SCPs)",
            "? 16",
            "? 17"
        ],
        "? 18": [
            "? 19",
            "? 20"
        ]
    },
    "cloudshell_command_execution_question": {
        "Cloud Shell Availability": ["? 21", "? 22"],
        "Command Execution in Cloud Shell": ["? 23", "? 24"]
    },
    "database_selection_and_replication_question": {
        "Comparing RDBMS and NoSQL": [
            "RDBMS",
            "NoSQL",
            "? 25"
        ],
        "Selecting the Right Database for Workloads": [
            "OLTP",
            "OLAP"
        ]
    },
    "edge_functions_use_case_question": {
        "CloudFront Functions vs. Lambda@Edge": [
            "Lambda@Edge",
            "? 26"
        ],
        "Request and Response Modification": [
            "Origin Request",
            "Viewer Response",
            "? 27"
        ]
    },
    "edge_logic_execution_question": {
        "Executing Logic at the Edge": [
            "Lambda@Edge",
            "Origin Request",
            "Origin Response",
            "Viewer Request",
            "Viewer Response"
        ],
        "? 28": [
            "? 29",
            "? 30"
        ]
    },
    "sagemaker_rekognition_question": {
        "Rekognition Use Case": [
            "Rekognition",
            "? 31"
        ],
        "SageMaker Use Case": [
            "SageMaker",
            "? 32"
        ]
    }
}




  let selectedSection = null;
  let strongAreasVisible = true;

  function getButtonClass() {
      return scope === "strong" ? "variant-filled-primary" : "variant-filled-tertiary";
  }

  function convertToCapitalizedWords(inputString) {
        const dictionary = {
            "cloudformation_costexplorer_question": "CloudFormation CostExplorer Question",
            "multi_account_management_question": "Multi-Account Management Question",
            "sagemaker_rekognition_question": "SageMaker Rekognition Question",
            "cloudshell_command_execution_question": "CloudShell Command Execution Question",
            "scp_security_compliance_question": "SCP Security Compliance Question"
        };

        // Check if the input string exists in the dictionary
        if (dictionary[inputString]) {
            return dictionary[inputString];
        }

        // Default behavior if no dictionary match
        return inputString
            .split('_') // Split the string into an array of words using the underscore as a delimiter
            .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
            .reduce((result, word, index) => {
                // Add a newline after the third word
                if (index === 3) {
                    return result + '\n' + word;
                }
                return result + (result ? ' ' : '') + word;
            }, ''); // Join the words together, handling the newline after the 3rd word
    }


  function getNodeFill(d) {
      if (d.id.includes("?")) {
          return "#444"; // Question mark nodes (always yellow)
      }
      return scope === "strong" ? "#007bff" : "#6864f4"; // Primary for strong, tertiary purple for weak
  }

  function modifyHierarchy(hierarchy) {
    for (const key in hierarchy) {
        hierarchy[key] = layout_dict[key];
    }
    return hierarchy;
  }



  hierarchy = modifyHierarchy(hierarchy);
  console.log("Modified Hierarchy:", hierarchy);

  function transformDataForSection(section, concepts) {
    const nodes = [];
    const links = [];
    const sectionNode = { id: section, group: "section" };
    nodes.push(sectionNode);

    Object.entries(concepts).forEach(([concept, terms]) => {
      const conceptNode = { id: concept, group: "concept" };
      nodes.push(conceptNode);
      links.push({ source: sectionNode.id, target: conceptNode.id });

      terms.forEach((term) => {
        const termNode = { id: term, group: "term" };
        nodes.push(termNode);
        links.push({ source: conceptNode.id, target: termNode.id });
      });
    });

    return { nodes, links };
  }

  function handleSectionClick(section) {
    selectedSection = section;
    const graphData = transformDataForSection(section, hierarchy[section]);
    d3.select("#my_dataviz").selectAll("*").remove();
    createGraph(graphData);
  }

  function createGraph(graph) {
    const container = document.getElementById("my_dataviz");
    const { width, height } = container.getBoundingClientRect();
    const padding = 50;

    const svg = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", `0 0 ${width} ${height - 50}`);

    // Define the arrowhead marker within your existing SVG
    svg.append("defs")
        .append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", "0 -5 10 10") // Defines the coordinate system for the marker
        .attr("refX", 10) // Position of the arrowhead on the end of the line
        .attr("refY", 0)
        .attr("markerWidth", 6) // Size of the marker
        .attr("markerHeight", 6)
        .attr("orient", "auto") // Orient to follow the line
        .append("path")
        .attr("d", "M0,-5L10,0L0,5") // The arrowhead shape
        .attr("fill", "white"); // Arrowhead color

    const tooltip = d3.select("#my_dataviz")
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("background", "#333")
        .style("color", "#fff")
        .style("padding", "5px 10px")
        .style("border-radius", "4px")
        .style("font-size", "12px")
        .style("pointer-events", "none")
        .style("opacity", 0);

    // Create links with directional arrows
    const link = svg
        .selectAll("line")
        .data(graph.links)
        .enter()
        .append("line")
        .attr("stroke", "#aaa")
        .attr("stroke-width", 2)
        .attr("marker", "url(#arrowhead)"); // Attach the arrowhead

    const node = svg
        .selectAll("g")
        .data(graph.nodes)
        .enter()
        .append("g");

    // Function to calculate the width of the text
    function getTextWidth(text, font) {
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        context.font = font || "12px Arial";
        return context.measureText(text).width;
    }

    // Append rectangles
    node.append("rect")
        .attr("rx", 10) // Rounded corners
        .attr("ry", 10)
        .attr("width", (d) => {
            if (d.id.includes("?")) {
                // Calculate the width for the word "Undiscovered"
                const undiscoveredTextWidth = getTextWidth("Undiscovered", "15px Arial") + 30; // Increased padding
                return Math.max(undiscoveredTextWidth, d.group === "section" ? 150 : d.group === "concept" ? 120 : 90);
            }
            const defaultWidth = d.group === "section" ? 150 : d.group === "concept" ? 120 : 90;
            const textWidth = getTextWidth(d.id, "15px Arial"); // Calculate text width
            return Math.max(defaultWidth, textWidth + 30); // Increased padding
        })
        .attr("height", (d) => {
            if (d.group === "section") return 60;
            if (d.group === "concept") return 50;
            return 40;
        })
        .attr("x", (d) => {
            const width = d.id.includes("?")
                ? Math.max(getTextWidth("Undiscovered", "15px Arial") + 30, d.group === "section" ? 150 : d.group === "concept" ? 120 : 90)
                : Math.max(getTextWidth(d.id, "15px Arial") + 30, d.group === "section" ? 150 : d.group === "concept" ? 120 : 90);
            return -(width / 2); // Center horizontally
        })
        .attr("y", (d) => -((d.group === "section" ? 60 : d.group === "concept" ? 50 : 40) / 2))
        .style("fill", getNodeFill)
        .style("stroke", "white")
        .style("stroke-width", 2);

    node.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", "0.35em")
        .style("font-size", "15px")
        .style("fill", "white")
        .style("pointer-events", "none")
        .style("font-weight", "bold")
        .selectAll("tspan")
        .data((d) => {
            if (d.id.includes("?")) {
                // If d.id contains "?", set text to "Undiscovered"
                return ["Undiscovered"];
            }

            // Get the capitalized words
            const words = convertToCapitalizedWords(d.id).split(' ');

            // If more than 3 words, split into two lines
            if (words.length > 3) {
                return [
                    words.slice(0, 3).join(' '), // First three words
                    words.slice(3).join(' '),   // Remaining words
                ];
            }

            // If 3 or fewer words, return as a single line
            return [words.join(' ')];
        })
        .enter()
        .append("tspan")
        .attr("x", 0) // Center align text
        .attr("dy", (d, i) => (i === 0 ? 0 : "1.2em")) // Add line spacing for subsequent lines
        .text((line) => line);

    const simulation = d3.forceSimulation(graph.nodes)
        .force("link", d3.forceLink(graph.links).id((d) => d.id).distance(160))
        .force("charge", d3.forceManyBody().strength(-1250))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .on("tick", ticked);

    function ticked() {
        link
            .attr("x1", (d) => Math.max(padding, Math.min(width - padding, d.source.x)))
            .attr("y1", (d) => Math.max(padding, Math.min(height - padding, d.source.y)))
            .attr("x2", (d) => Math.max(padding, Math.min(width - padding, d.target.x)))
            .attr("y2", (d) => Math.max(padding, Math.min(height - padding, d.target.y)));

        node.attr("transform", (d) => {
            d.x = Math.max(padding, Math.min(width - padding, d.x));
            d.y = Math.max(padding, Math.min(height - padding, d.y));
            return `translate(${d.x}, ${d.y})`;
        });
    }
}



</script>

<div class="flex flex-col items-center h-screen">
  <div class="w-full text-center transition-transform duration-500" style="transform: translateY({strongAreasVisible ? 0 : -100}px);">
    <h2 class="text-base lg:text-xl font-medium mb-4 pt-5">
      {#if scope === "strong"}
        Select a question to see how your answer shapes a personalized learning path.<br />
        <span class="text-primary-500">Blue</span> nodes show ideas our model thinks you're more familiar with.
      {:else}
        Select a question to see how your answer shapes a personalized learning path.<br />
        <span class="text-tertiary-500">Purple</span> nodes show ideas our model thinks you need to work on.
      {/if}
    </h2>
    <div class="flex flex-wrap justify-center gap-4">
        {#each Object.keys(hierarchy) as section}
          <button
            class="button {getButtonClass()} w-auto px-4 py-2"
            on:click={() => handleSectionClick(section)}
          >
            {convertToCapitalizedWords(section)}
          </button>
        {/each}
    </div>
  </div>
  <div id="my_dataviz" class="flex-grow w-full"></div>
</div>

<style>
#my_dataviz {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  overflow: hidden;
}

svg {
    border: 1px solid #ccc;
}

circle {
    stroke: #fff;
    stroke-width: 2px;
}

text {
    font: 12px sans-serif;
    pointer-events: none;
}

button {
    font-size: 16px;
    cursor: pointer;
}

.button.variant-filled-primary {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.button.variant-filled-primary:hover {
    background-color: #0056b3;
}

.button.variant-filled-tertiary {
    color: white;
    border: none;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.button.variant-filled-tertiary:hover {
    background-color: #9304f2;
}

.section-header {
  border-bottom: 2px solid white; /* White line under the text */
  padding-bottom: 0.5rem; /* Space between text and border */
}
</style>
