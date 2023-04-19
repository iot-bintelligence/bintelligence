import './MyBins.css'
import Bin from '../My Bins/Bin'

function MyBins() {
  return (
    <div className="binContainer">
      <h1>Mine komprimatorer</h1>
      <div className="mybins">
        <Bin name={"Roverud sykehjem"} fillDegree={74} estimate={"16 timer"}/>
        <Bin name={"Langeland sykehjem"} fillDegree={34} estimate={"3 dager"}/>
      </div>
        
    </div>
  )
}

export default MyBins;