import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import WorldMap, { WorldElement } from "./world-map/world-map";
import Legend from "./stats/legend";
import styled from "styled-components";
import PopulationChart from "./stats/population-chart";

const socket = io.connect("http://192.168.0.196:5000/world_map");

function subscribe(callback: any) {
  socket.on("json", (data: string) => callback(JSON.parse(data)));
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
      </Stats>
    </Container>
  );
}

const Stats = styled.div`
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: flex-start;
`;

const Container = styled.div`
  display: flex;
  heigth: 85vh;
`;

const elementNameMapping = new Map([
  ["Food", "#28f75c"],
  ["SlowMonster", "#ff0000"],
  ["FastMonster", "#0080ff"]
]);

export default App;
