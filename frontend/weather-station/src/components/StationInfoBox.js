import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';


function StationInfoBox(props) {
  return (
    <Row>
      <Col>
        <div className="stationInfoBox">
          <h4 style={{color: "#3581cc"}}>Station information</h4>
          <div className="lead">
            <Row>
              <Col lg="2" md="2">Last update:</Col><Col>{props.data.lastWeaterPointDate}</Col>
            </Row>
          </div>
        </div>
      </Col>
    </Row>
  );
}
  
export default StationInfoBox;
