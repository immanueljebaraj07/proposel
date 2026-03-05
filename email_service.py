import smtplib
from email.mime.text import MIMEText

# Function to send email notifications

def send_email_notification(to_email, subject, body):
    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login credentials for sending the email
        server.login('your_email@gmail.com', 'your_password')

        # Create the email
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'your_email@gmail.com'
        msg['To'] = to_email

        # Send the email
        server.sendmail('your_email@gmail.com', to_email, msg.as_string())
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print(f'An error occurred: {e}')  

# Example usage of the function

# Notify seller when product quantity is reduced
send_email_notification('Jeevaperumal1128@gmail.com', 'Product Quantity Reduced', 'The quantity of the product has been reduced in the grocery proposal system.')

# Notify anonymous buyer
send_email_notification('buyer@example.com', 'Product Quantity Reduced', 'Please note that the quantity of a product you were interested in has been reduced in the grocery proposal system.')