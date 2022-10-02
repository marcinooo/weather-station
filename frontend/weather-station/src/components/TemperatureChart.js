import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  Tooltip, CartesianGrid } from 'recharts';


function TemperatureChart(props) {
  const temperatureRange = [0, Math.max(...props.data.map(o => parseInt(o.temperature))) + 3];
  return (
    <Row>
      <Col>
      <h2 className="display-6">Temperature</h2>
      <div className="line-chart-wrapper">
      <ResponsiveContainer width='100%' height={400}>
        <LineChart
          width={600} height={400} data={props.data}
          margin={{ top: 40, right: 40, bottom: 35, left: 20 }}
        >
          <CartesianGrid stroke="#eee" strokeDasharray="5 5"/>
          <XAxis dataKey="date" label={{value: "hours", dy: 32}} angle={-35} textAnchor="end"/>
          <YAxis label={{ value: 'temperature [°C]', angle: -90,  dx: -10}} domain={temperatureRange} scale="linear"/>
          <Tooltip
            wrapperStyle={{
              borderColor: 'white',
              boxShadow: '2px 2px 3px 0px rgb(204, 204, 204)',
            }}
            contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.8)' }}
            labelStyle={{ fontWeight: 'bold', color: '#666666' }}
          />
          <Line type="monotone" dataKey="temperature" stroke="#82ca9d" />
        </LineChart>
        </ResponsiveContainer>
      </div>
      </Col>
    </Row>
  );
}
  
export default TemperatureChart;
