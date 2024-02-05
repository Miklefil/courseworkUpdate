# from django.conf import settings
# from django.core.mail import send_mail
# from django.utils import timezone
#
# from mailings.models import Log, Client
#
# x = 25
# def send_emails():
#     print(timezone.now().time())
#
#     clients = Client.objects.all()
#
#     for client in clients:
#         # Assuming each client has a related message and setting
#         message = client.messages.latest('id')
#         setting = client.settings.latest('id')
#
#         periodicity = setting.periodicity
#         start_date = setting.start_date
#         days_passed = (timezone.now().date() - start_date).days
#
#         if periodicity == 'daily':
#             send_e_mail(client, message, setting)
#             print("day")
#
#         elif periodicity == 'weekly':
#             if days_passed % 7 == 0:
#                 send_e_mail(client, message, setting)
#                 print("week")
#
#         elif periodicity == 'monthly':
#             if days_passed % 30 == 0:
#                 send_e_mail(client, message, setting)
#                 print("month")
#
#
# def send_e_mail(client, selected_message, selected_settings):
#     subject = selected_message.subject
#     body = selected_message.body
#
#     send_mail(
#         f"{subject}",
#         f"{body}",
#         settings.EMAIL_HOST_USER,
#         [client.email]
#     )
#     log_entry = Log.objects.create(
#         client=client,
#         status="finished",
#         server_response="Email sent successfully",
#         email_subject=subject,
#         email_body=body
#     )
