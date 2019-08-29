import React, { useState, useEffect, Fragment } from "react";
import styled from "styled-components";
import io from "socket.io-client";

const socket = io.connect("http://127.0.0.1:5000/world_map");

function subscribe(callback: any) {
  socket.on("json", (data: string) => callback(JSON.parse(data)));
}

interface WorldElement {
  element_name: string;
  position: number[];
}

const WorldMap: React.FC = () => {
  return (
    <Container>
      <WorldMapGrid />
    </Container>
  );
};

function WorldMapGrid() {
  const [worldElements, setWorldElements] = useState([]);
  useEffect(() => subscribe((worldElements: []) => setWorldElements(worldElements)), []);

  let possible_cells = [<RedCell />, <GreenCell />];
  let index = 0;
  let element_name_mapping = new Map();
  worldElements.forEach((element: WorldElement) => {
    if (!element_name_mapping.has(element.element_name)) {
      element_name_mapping.set(element.element_name, possible_cells[index++]);
    }
  });

  return <Fragment>{generateGrid(worldElements, element_name_mapping)}</Fragment>;
}

const generateGrid = (
  worldElements: WorldElement[],
  element_name_mapping: Map<string, JSX.Element>
) => {
  const positions: number[][] = worldElements.map(
    (element: WorldElement) => element.position
  );
  const width: number = calculateWorldDimension(positions, 0);
  const height: number = calculateWorldDimension(positions, 1);

  const cells: JSX.Element[] = buildCells(
    worldElements,
    element_name_mapping,
    width,
    height
  );
  return buildRows(cells, width, height);
};

const calculateWorldDimension = (positions: number[][], dimension: number) => {
  return Math.max(...positions.map(position => position[dimension]), 39) + 1;
};

const buildCells = (
  worldElements: WorldElement[],
  element_name_mapping: Map<string, JSX.Element>,
  width: number,
  height: number
) => {
  let cells: JSX.Element[] = Array(width * height).fill(<BlankCell />);
  worldElements.forEach(
    (element: WorldElement) =>
      (cells[calculateIndex(element.position, width)] = getElement(
        element.element_name,
        element_name_mapping
      ))
  );
  return cells.map((cell: JSX.Element, index: number) => ({ ...cell, key: index }));
};

const calculateIndex = (position: number[], width: number) => {
  return position[1] * width + position[0];
};

const getElement = (
  element_name: string,
  element_name_mapping: Map<string, JSX.Element>
): JSX.Element => {
  const element: JSX.Element | undefined = element_name_mapping.get(element_name);
  return element === undefined ? <BlankCell /> : element;
};

const buildRows = (cells: JSX.Element[], width: number, height: number) => {
  let rows: JSX.Element[][] = [];
  for (let index: number = 0; index < height; index++) {
    rows.push(cells.slice(index * width, (index + 1) * width));
  }
  return rows.map((row, index) => <Row key={index}>{row}</Row>);
};

const Container = styled.div`
  display: flex;
  flex-direction: column;
  width: 90vw;
  height: 90vh;
`;

const Row = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  flex: 1;
`;

const BlankCell = styled.div`
  border-radius: 50%;
  flex: 1;
`;

const RedCell = styled.div`
  border-radius: 50%;
  background-color: #ff2e2e;
  flex: 1;
`;

const GreenCell = styled.div`
  border-radius: 50%;
  background-color: #28f75c;
  flex: 1;
`;

export default WorldMap;
