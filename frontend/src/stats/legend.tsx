import React from "react";
import styled from "styled-components";

function Legend(elementNameMapping: Map<string, string>, worldElementsName: string[]) {
  let elements: JSX.Element[] = [];
  elementNameMapping.forEach((value: string, key: string) =>
    elements.push(legendElement(key, value, worldElementsName.filter((name: string) => name === key).length)
  ));
  return <Container>{elements}</Container>;
}

function legendElement(key: string, value: string, element_count: number) {
  return (
    <LegendElement key={key}>
      <LegendText>{key}</LegendText> <LegendPictogram key={key} color={value}/> <LegendText>{element_count}</LegendText>
    </LegendElement>
  );
}

const Container = styled.div`
  flex: auto;
  border-style: solid;
  border-width: 2px;
  border-color: #333333;
  background-color: #444444;
`

const LegendElement = styled.span`
  display: flex;
  height: 10px;
  width: 200px;
  margin: 8px;
`
const LegendText = styled.h6`
  padding-left: 8px;
  margin: 0px;
  flex: 1;
`
const LegendPictogram = styled.div`
  background-color: ${props => props.color};
  flex: 1;
  margin-left: 4px;
`
export default Legend