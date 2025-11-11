# utils/mailersend_client.py
from flask import current_app
from mailersend import emails
import base64
import logging

class MailerSendClient:
    def __init__(self, app=None):
        self.api_key = None
        self.sender_email = None
        self.sender_name = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Inicializa el cliente usando la configuración de Flask."""
        self.api_key = app.config.get("MAILERSEND_API_KEY")
        self.sender_email = app.config.get("MAIL_DEFAULT_SENDER")
        self.sender_name = app.config.get("MAIL_DEFAULT_SENDER_NAME", "Connexa Sistema")

        if not self.api_key:
            app.logger.warning("⚠️ MAILERSEND_API_KEY no configurada")
        else:
            app.logger.info("📧 MailerSendClient inicializado correctamente")

    def send_email(self, subject, recipients, html_content=None, text_content=None, attachments=None):
        """Envía un email usando MailerSend."""
        try:
            if not self.api_key:
                current_app.logger.error("❌ MailerSend API key no configurada")
                return False

            mailer = emails.NewEmail(self.api_key)

            mailer.set_mail_from({
                "name": self.sender_name,
                "email": self.sender_email,
            })

            recipient_list = [{"name": r.get('name', 'Usuario'), "email": r['email']} for r in recipients]
            mailer.set_mail_to(recipient_list)
            mailer.set_subject(subject)

            if html_content:
                mailer.set_html_content(html_content)

            if text_content:
                mailer.set_plaintext_content(text_content)
            elif html_content:
                text_content = self._html_to_plain_text(html_content)
                mailer.set_plaintext_content(text_content)

            if attachments:
                attachment_list = []
                for attachment in attachments:
                    if isinstance(attachment, dict) and 'data' in attachment:
                        encoded_data = base64.b64encode(attachment['data']).decode('utf-8')
                        attachment_list.append({
                            "content": encoded_data,
                            "filename": attachment.get('filename', 'attachment'),
                            "type": attachment.get('content_type', 'application/octet-stream')
                        })
                mailer.set_attachments(attachment_list)

            response = mailer.send()

            if response and response.status_code == 202:
                current_app.logger.info(f"✅ Email enviado exitosamente a {recipients}")
                return True
            else:
                current_app.logger.error(f"❌ Error enviando email: {response.status_code if response else 'No response'}")
                return False

        except Exception as e:
            current_app.logger.error(f"💥 Error en MailerSend: {str(e)}")
            return False

    def _html_to_plain_text(self, html_content):
        import re
        text = re.sub(r'<[^>]+>', '', html_content)
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

# 👇 Instancia global, sin inicializar todavía
mailersend_client = MailerSendClient()

