import azure.functions as func
import logging
import os 
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, HtmlContent
import psycopg2


def send_email(receiver_email, subject, body):
    print(f"Sending email to {receiver_email} ...")
    mail_content = Mail(
        from_email="minhhieuvu9497@gmail.com",
        to_emails=receiver_email,
        subject=subject,
        plain_text_content=body,
        html_content=HtmlContent(body)
    )

    sendgrid_client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    return sendgrid_client.send(mail_content)


def main(msg: func.ServiceBusMessage):
    db_connection = None
    print("DEBUGGGGGGING")
    id_noti = msg.get_body()
    print(id_noti)
    notification_id = int(id_noti.decode('utf-8'))
    print("Triggered notification: " + str(notification_id))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    try:
        # TODO: Get connection to database
        db_connection = psycopg2.connect(os.environ.get("SQLALCHEMY_DATABASE_URI"))
        cursor = db_connection.cursor()

        # Get notification message and subject from database
        cursor.execute("SELECT message, subject FROM notification WHERE id = %s", (notification_id,))
        notification = cursor.fetchone()
        if not notification:
            logging.error('can not find notification id %s', notification_id)
            return
        message, subject = notification

        # Get attendees email and name
        cursor.execute("SELECT email, first_name FROM attendee")
        attendees = cursor.fetchall()

        # Loop through each attendee and send an email with a personalized subject
        for email, first_name in attendees:
            personalized_subject = f"{subject} - {first_name}"
            print(personalized_subject)
            send_email(email, personalized_subject, message)

        # Update the notification table by setting the completed date and updating the status
        completed_date = datetime.now()
        status = f"Notified {len(attendees)} attendees"
        cursor.execute(
            "UPDATE notification SET status = %s, completed_date = %s WHERE id = %s",
            (status, completed_date, notification_id)
        )
        db_connection.commit()
        logging.info("Execute send notification")

    except Exception as error:
        with open("/Users/hieuvuminh/Downloads/web/nd081-c3-Migrating-Non-Native-Cloud-Applications-project-starter/function/ServiceBusQueueTrigger/log.txt", "w") as file:
            file.write(str(error))
        logging.error(error)

    finally:
        if db_connection is not None:
            db_connection.close()
        logging.info("Close send notification")
