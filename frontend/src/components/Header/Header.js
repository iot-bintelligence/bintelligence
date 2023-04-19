import './Header.css'
import logo from '../../images/logo.png'
import profilePicture from '../../images/profilePicture.png'


function Header() {
    return (
        <div className="headerContainer">
            
            <div className="logoSection">
                <img className='logo' src={logo} />
            </div>

            <div className="profileSection">
                <h3 className="profileText">Hei, Erik!</h3>
                <img className="profilePicture" src={profilePicture} />
            </div>

        </div>
    )
}

export default Header;