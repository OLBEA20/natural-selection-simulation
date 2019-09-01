import React, { Fragment, useEffect, useState } from "react";
import io from "socket.io-client";
import WorldMap from "./world-map/world-map";
import Legend from "./legend/legend";

const socket = io.connect("http://127.0.0.1:5000/world_map");

function subscribe(callback: any) {
  socket.on("json", (data: string) => callback(JSON.parse(data)));
}

function App() {
  const [worldElements, setWorldElements] = useState([]);
  useEffect(() => subscribe((worldElements: []) => setWorldElements(worldElements)), []);

  return (
    <Fragment>
      <WorldMap worldElements={worldElements} elementNameMapping={elementNameMapping} />
      {Legend(elementNameMapping)}
    </Fragment>
  );
}

const elementNameMapping = new Map([
  ["Food", "#28f75c"],
  ["SlowMonster", "#ff2e2e"],
  ["FastMonster", "#f59042"]
]);

export default App;
