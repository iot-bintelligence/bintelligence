import './NotificationItem.css'

function NotificationItem({isExpired, statusText, date, time}) {

  let notificationClass = "notificationItemContainer"
  if (isExpired) {
    notificationClass += " expired"
  }

  return(
    <div className={notificationClass}>
      <div className='timeSection'>
        <div className='timeText'>{time}</div>
        <div className='timeText'>{date}</div>
      </div>

      <div className='textSection'>
        <div className='divider'></div>
        <p className='statusText'>{statusText}</p>
      </div>
      
    </div>
  )
}

export default NotificationItem;