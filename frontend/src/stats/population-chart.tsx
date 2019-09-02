import React from "react";
import { AreaSeries, XYPlot, XAxis, YAxis } from "react-vis";
import styled from "styled-components";


interface PopulationChartProps {
  elementNameMapping: Map<string, string>;
  worldElementsName: string[];
}

class PopulationChart extends React.Component<PopulationChartProps, any> {
  elementsCount: Map<string, number[]>;
  constructor(props: PopulationChartProps) {
    super(props);
    this.elementsCount = new Map<string, number[]>();
  }

  updateElementsCount = (
    elementNameMapping: Map<string, string>,
    worldElementsName: string[]
  ) => {
    elementNameMapping.forEach((_: string, elementName: string) =>
      this.updateElement(elementName, worldElementsName)
    );
  };

  updateElement = (elementName: string, worldElementsName: string[]) => {
    const elementCount = worldElementsName.filter((name: string) => name === elementName)
      .length;
    let elementCounts = this.elementsCount.get(elementName);
    elementCounts = elementCounts !== undefined ? elementCounts : [];
    elementCounts.push(elementCount);
    this.elementsCount.set(elementName, elementCounts);
  };

  generateSeries = (elementNameMapping: Map<string, string>) => {
    let series: JSX.Element[] = [];
    elementNameMapping.forEach((color: string, elementName: string) =>
      series.push(
        <AreaSeries
          key={elementName}
          color={color}
          opacity={0.5}
          data={this.getElementCounts(elementName).map((count: number, index: number) => ({
            x: index,
            y: count
          }))}
        />
      )
    );
    return series;
  };

  getElementCounts = (elementName: string) => {
    const elementCounts = this.elementsCount.get(elementName);
    return elementCounts !== undefined ? elementCounts : [];
  };

  render() {
    this.updateElementsCount(this.props.elementNameMapping, this.props.worldElementsName);
    return (
      <Container>
        <XYPlot width={200} height={150}>
          <XAxis/>
          <YAxis/>
          {this.generateSeries(this.props.elementNameMapping)}
        </XYPlot>
      </Container>
    );
  }
}

const Container = styled.div`
  flex: 1;
`;

export default PopulationChart;
