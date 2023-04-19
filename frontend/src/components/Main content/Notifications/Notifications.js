import './Notifications.css'
import NotificationItem from './NotificationItem';

function Notifications() {
  return(
    <div className="notificationsContainer">
      <h1>Varslinger</h1>

      <div className='notificationsBox'>
        <div className='currentNotifications'>
          <p className='notificationsSectionHeadline'>Denne uken</p>
          <NotificationItem isExpired={false} statusText={"Roverud komprimator er full."} date={"19.04.23"} time={"12:33"}/>
          <NotificationItem isExpired={true} statusText={"Langeland ikke tømt på 9 timer."} date={"14.04.23"} time={"18:13"}/>
        </div>

        <div className='pastNotifications'>
          <p className='notificationsSectionHeadline'>Tidligere</p>
          <NotificationItem isExpired={false} statusText={"Roverud komprimator er full."} date={"15.04.23"} time={"16:49"}/>
          <NotificationItem isExpired={false} statusText={"Langeland komprimator er full."} date={"14.04.23"} time={"09:13"}/>
        </div>
      </div>
    </div>
  )
}

export default Notifications;