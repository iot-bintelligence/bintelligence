import './MyBins.css'
import Bin from '../My Bins/Bin'

function MyBins() {
  return (
    <div className="binContainer">
      <h1>Mine komprimatorer</h1>
      <div className="mybins">
        <Bin />
        <Bin />
      </div>
        
    </div>
  )
}

export default MyBins;