import os
from dotenv import load_dotenv

"""
Collection of Email Structures. ForgotPassword Links Format and Order Invoice Format.
"""

load_dotenv()


def forgotPasswordFormat(email, reset_code):
    """
    Structure for Forgot Password Reset Link.
    Parameters
    ----------------------------------------------------------
    reset_code: str - Token to reset Password
    email: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: str - Mail Body
    """
    DB_URL = os.environ.get('LOCAL_DATABASE_URL')
    subject = "Hello User"
    recipient = email
    message = """
        <!DOCTYPE html>
        <html>
        <title>Reset Password</title>
        <body>
        <h3>Hello, {0:}</h3>
        <p>Password Reset Request has been received by Someone.</p>
        <p>Visit Below Link to Reset Your Password<br><u>{2}/{1}</u></p>
        <p>If you did not requested, You can ignore this mail!<p>
        </body>
        </html>
        """.format(email, reset_code, DB_URL)
    return subject, recipient, message
