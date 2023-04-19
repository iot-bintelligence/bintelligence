import './Footer.css'
import telenor from '../../images/telenor.png'

function Footer() {
  return(
    <div className='footerContainer'>
      <div className="promotionSection">
        <h2 className='promotionText'>Tjeneste levert av Telenor</h2>
        <img className='telenorLogo' src={telenor}></img>
      </div>
    </div>
  )
}

export default Footer;