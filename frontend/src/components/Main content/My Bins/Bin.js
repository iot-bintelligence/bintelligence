import "./Bin.css"
import binImage from '../../../images/binImage.png'
import clock from '../../../images/clock.png'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowRight } from '@fortawesome/free-solid-svg-icons'



function Bin({ name, fillDegree, estimate }) {
    return (
        <div className="binItemContainer">
            <p className="binTitle">{name}</p>
            <img className="binImage" src={binImage}></img>

            <div className="estimateSection">
                <div className="estimateItem">
                    <p className="estimateItemHeadline">Fyllingsgrad</p>
                    <div className="estimateRectangle">
                        <p className="whiteText">{fillDegree}</p>
                    </div>
                </div>
                <div className="estimateItem">
                    <p className="estimateItemHeadline">Estimat</p>
                    <div className="estimateRectangle">
                        <img className="clockImage" src={clock}></img>
                        <p className="whiteText">{estimate}</p>
                    </div>
                </div>
            </div>

            <div className="emptyButton">Registrer tømming<FontAwesomeIcon icon={faArrowRight} className="icon"/></div>
        </div>
    )
}

export default Bin