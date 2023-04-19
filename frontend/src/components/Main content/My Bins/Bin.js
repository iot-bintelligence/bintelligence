import "./Bin.css"
import binImage from '../../../images/binImage.png'

function Bin() {
    return (
        <div className="binItemContainer">
            <p className="binTitle">Roverud sykehjem</p>
            <img className="binImage" src={binImage}></img>
        </div>
    )
}

export default Bin