import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import WorldMap, { WorldElement } from "./world-map/world-map";
import Legend from "./legend/legend";
import styled from "styled-components";

const socket = io.connect("http://127.0.0.1:5000/world_map");

function subscribe(callback: any) {
  socket.on("json", (data: string) => callback(JSON.parse(data)));
}

function App() {
  const [worldElements, setWorldElements] = useState([]);
  useEffect(() => subscribe((worldElements: []) => setWorldElements(worldElements)), []);

  return (
    <Container>
      <WorldMap worldElements={worldElements} elementNameMapping={elementNameMapping} />
      {Legend(elementNameMapping, worldElements.map((worldElement: WorldElement) => worldElement.element_name))}
    </Container>
  );
}

const Container = styled.div`
  display: flex;
  heigth: 98vh;
`

const elementNameMapping = new Map([
  ["Food", "#28f75c"],
  ["SlowMonster", "#ff2e2e"],
  ["FastMonster", "#f59042"]
]);

export default App;
