import React from 'react';
import styled from 'styled-components';

const App: React.FC = () => {
  return (
    <Container>
      {generateCellGrid(100, 100)}
    </Container>
  );
}

const generateCellGrid = (width: number, height: number) => {
  const rows: Array<JSX.Element> = new Array(height);
  for(let i: number = 0; i < height; i++) {
    rows.push(<Row key={i}>{generateCells(width)}</Row>);
  }
  return rows
}

const generateCells = (width: number) => {
  const cells: Array<JSX.Element> = new Array(width)
  for(let i: number = 0; i < width; i++) {
    cells.push(<Cells key={i}></Cells>);
  }
  return cells;
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  width: 80vw;
  height: 80vh;
`;

const Row = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  flex: 1;
`;

const Cells = styled.div`
  border-style: solid;
  border-width: 1px;
  flex: 1;
`;

export default App;
