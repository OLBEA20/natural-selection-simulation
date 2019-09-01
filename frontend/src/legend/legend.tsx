import React, { Fragment } from "react";
import styled from "styled-components";

function Legend(elementNameMapping: Map<string, string>) {
  let elements: JSX.Element[] = [];
  elementNameMapping.forEach((value: string, key: string) =>
    elements.push(legendElement(key, value))
  );
  return <Fragment>{elements}</Fragment>;
}

function legendElement(key: string, value: string) {
  return (
    <LegendElement key={key}>
      <LegendText>{key}</LegendText> <LegendPictogram key={key} color={value}/>
    </LegendElement>
  );
}

const LegendElement = styled.span`
  display: flex;
  height: 10px;
  width: 200px;
`
const LegendText = styled.h6`
  margin: 0px;
  flex: 1;
`
const LegendPictogram = styled.div`
  background-color: ${props => props.color}
  flex: 1
`
export default Legend