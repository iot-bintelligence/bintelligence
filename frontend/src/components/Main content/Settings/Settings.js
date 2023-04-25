import './Settings.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFloppyDisk } from '@fortawesome/free-solid-svg-icons'

function Settings() {
  return(
    <div className="settingsContainer">
      <h1>Innstillinger</h1>

      <div className='settingsBox'>
        <div className='notifTypeSection'>
          <p className='notifText'>Varslingstype</p>
          <div className='smsRadio'>
            <input type="radio" id="sms" name="contact-method" value="sms"></input>
            <label for="sms">SMS</label>
          </div>

          <div>
            <input type="radio" id="email" name="contact-method" value="email"></input>
            <label for="email">Email</label>
          </div>

          <div>
            <input className='inputField' type="text" id="fname" name="fname" placeholder='SMS/Email'></input>
          </div>
        </div>
        <div className='chooseDegreeSection'>
          <p className='degreeText'>Velg fyllingsgrad for varsel</p>
          <input type="range" min="1" max="100" value="50" className="slider" id="myRange"></input>
        </div>


        <div className='saveButton'><FontAwesomeIcon icon={faFloppyDisk} className='icon'/> Lagre </div>
        
      </div>
    </div>
  )
}

export default Settings;