import React from "react";
import styled from "styled-components";

interface WorldMapProps {
  worldElements: WorldElement[];
  elementNameMapping: Map<string, string>;
}

export interface WorldElement {
  element_name: string;
  position: number[];
}

function WorldMap(props: WorldMapProps) {
  return <Container>{generateGrid(props.worldElements, props.elementNameMapping)}</Container>;
}

const generateGrid = (
  worldElements: WorldElement[],
  elementNameMapping: Map<string, string>
) => {
  const positions: number[][] = worldElements.map(
    (element: WorldElement) => element.position
  );
  const width: number = calculateWorldDimension(positions, 0);
  const height: number = calculateWorldDimension(positions, 1);

  const cells: JSX.Element[] = buildCells(
    worldElements,
    elementNameMapping,
    width,
    height
  );
  return buildRows(cells, width, height);
};

const calculateWorldDimension = (positions: number[][], dimension: number) => {
  return Math.max(...positions.map(position => position[dimension]), 49) + 1;
};

const buildCells = (
  worldElements: WorldElement[],
  elementNameMapping: Map<string, string>,
  width: number,
  height: number
) => {
  let cells: JSX.Element[] = Array(width * height).fill(<BlankCell />);
  worldElements.forEach(
    (element: WorldElement) =>
      (cells[calculateIndex(element.position, width)] = getElement(
        element.element_name,
        elementNameMapping
      ))
  );
  return cells.map((cell: JSX.Element, index: number) => ({ ...cell, key: index }));
};

const calculateIndex = (position: number[], width: number) => {
  return position[1] * width + position[0];
};

const getElement = (
  element_name: string,
  elementNameMapping: Map<string, string>
): JSX.Element => {
  const element: JSX.Element | undefined = <Cell color={elementNameMapping.get(element_name)}/>;
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
  height: 85vh;
  flex: 10;
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

const Cell = styled.div`
  border-radius: 50%;
  background-color: ${props => props.color};
  flex: 1;
`;

export default WorldMap;
