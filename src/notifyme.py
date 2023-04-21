from notifypy import Notify

# Notifies the score
def notifyMe(scoreCard):
    notification = Notify()
    notification.title = "live-score-notifier"
    notification.message = scoreCard
    notification.icon = "img/ipl.jpg"
    notification.send()
        
