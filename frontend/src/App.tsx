import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import WorldMap, { WorldElement } from "./world-map/world-map";
import Legend from "./stats/legend";
import styled from "styled-components";
import PopulationChart from "./stats/population-chart";
import symbolicateStackTrace from "react-native/Libraries/Core/Devtools/symbolicateStackTrace";

const socket = io.connect("http://192.168.0.196:5000/simulation");

function subscribe(callback: any) {
  socket.on("json", (data: string) => callback(JSON.parse(data)));
}

const resetSimulation = () => {
  socket.emit("stop")
  socket.emit("start")
}

function App() {
  const [worldElements, setWorldElements] = useState([]);
  useEffect(() => subscribe((worldElements: []) => setWorldElements(worldElements)), []);

  return (
    <Container>
      <WorldMap worldElements={worldElements} elementNameMapping={elementNameMapping} />
      <Stats>
        {Legend(
          elementNameMapping,
          worldElements.map((worldElement: WorldElement) => worldElement.element_name)
        )}
        <PopulationChart
          elementNameMapping={elementNameMapping}
          worldElementsName={worldElements
            .map((worldElement: WorldElement) => worldElement.element_name)
            .filter((elementName: string) => elementName !== "Food")}
        />
        <PopulationChart
          elementNameMapping={elementNameMapping}
          worldElementsName={worldElements
            .map((worldElement: WorldElement) => worldElement.element_name)
            .filter((elementName: string) => elementName === "Food")}
        />
        <button onClick={resetSimulation}>Reset</button>
      </Stats>
    </Container>
  );
}

const Stats = styled.div`
  display: flex;
  flex: 1;
  height: auto;
  flex-direction: column;
  justify-content: center;
  background-color: #777777;
`;

const Container = styled.div`
  display: flex;
  height: 85vh;
`;

const elementNameMapping = new Map([
  ["Food", "#28f75c"],
  ["SlowMonster", "#ff0000"],
  ["FastMonster", "#0080ff"]
]);

export default App;
