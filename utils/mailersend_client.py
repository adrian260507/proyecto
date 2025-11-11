# utils/mailersend_client.py
from flask import current_app
from mailersend import emails
import base64
import logging

class MailerSendClient:
    def __init__(self):
        self.api_key = current_app.config.get("MAILERSEND_API_KEY")
        self.sender_email = current_app.config.get("MAIL_DEFAULT_SENDER")
        self.sender_name = current_app.config.get("MAIL_DEFAULT_SENDER_NAME", "Connexa Sistema")
        
    def send_email(self, subject, recipients, html_content=None, text_content=None, attachments=None):
        """
        Envía un email usando la API de MailerSend
        """
        try:
            if not self.api_key:
                current_app.logger.error("❌ MailerSend API key no configurada")
                return False
            
            # Inicializar el cliente de MailerSend
            mailer = emails.NewEmail(self.api_key)
            
            # Configurar remitente
            mailer.set_mail_from(
                {
                    "name": self.sender_name,
                    "email": self.sender_email,
                }
            )
            
            # Configurar destinatarios
            recipient_list = []
            for recipient in recipients:
                recipient_list.append({
                    "name": recipient.get('name', 'Usuario'),
                    "email": recipient['email']
                })
            
            mailer.set_mail_to(recipient_list)
            
            # Configurar asunto
            mailer.set_subject(subject)
            
            # Configurar contenido HTML
            if html_content:
                mailer.set_html_content(html_content)
            
            # Configurar contenido de texto plano
            if text_content:
                mailer.set_plaintext_content(text_content)
            elif html_content:
                # Generar texto plano básico desde HTML si no se proporciona
                text_content = self._html_to_plain_text(html_content)
                mailer.set_plaintext_content(text_content)
            
            # Configurar adjuntos si los hay
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
            
            # Enviar el email
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
        """
        Convierte HTML a texto plano básico
        """
        import re
        # Eliminar etiquetas HTML
        text = re.sub(r'<[^>]+>', '', html_content)
        # Reemplazar entidades HTML
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
        # Colapsar espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

# Instancia global del cliente
mailersend_client = MailerSendClient()
