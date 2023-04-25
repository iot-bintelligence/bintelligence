import './Content.css'
import MyBins from '../Main content/My Bins/MyBins';
import Notifications from './Notifications/Notifications';
import Settings from './Settings/Settings';


function Content() {
    return (
        <div className="contentContainer">
            <MyBins className="binContainer"/>
            <Notifications className="notificationsContainer"/>
            <Settings className="settingsContainer"/>
        </div>
    )
}

export default Content;