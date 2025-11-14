import logging, time

from django.db.models.signals 	import post_save
from django.template.loader 	import render_to_string
from django.core.mail 			import send_mail
from django.dispatch 			import receiver

from requests import HTTPError, status_codes

from business.models.singletons import BusinessConfig
from feedback_requests.config 	import TELEGRAM_SEND_NOTIFICATIONS
from feedback_requests.models 	import FeedbackRequest
from core.models.general 		import TelegramSendingChannel


_logger = logging.getLogger(__name__)


@receiver(post_save, sender = FeedbackRequest)
def send_new_request_notification_into_telegram(sender, instance: FeedbackRequest, created, **kwargs):
	if not created:
		return

	specialization = TelegramSendingChannel.Specialization.NEW_REQUEST_NOTIFICATIONS
	channel = TelegramSendingChannel.get_by_specialization(specialization)

	if not channel:
		return

	message = render_to_string(
		TELEGRAM_SEND_NOTIFICATIONS.TG_MESSAGE_TEMPLATE_NAME,
		{'request': instance}
	)

	error_message: str = ""
	for _ in range(0, TELEGRAM_SEND_NOTIFICATIONS.ATTEMPTS_COUNT):
		# Эта функция будет выполнятся в отдельном потоке, так что всё путём
		success, ex = channel.try_send_message(message, raise_for_status = True)

		if success:
			instance.mark_as_seen()
			_logger.debug(f"Успешно отправил уведомление о новой заявке в телеграмм.")
			return

		error_message = str(ex)
		# Ошибка статуса (raise_for_status())
		if isinstance(ex, HTTPError):
			error_message = f"{ex.response.status_code}: {ex.response.json()['description']}"

			status_code: int = ex.response.status_code
			status_group = status_code // 100

			code_allow_retry = lambda code: code in TELEGRAM_SEND_NOTIFICATIONS.RETRY_ATTEMPT_HTTP_CODES
			if not any(map(code_allow_retry, (status_group, status_code))):
				_logger.debug(
					f'Это HTTPError и кода ошибки нет в списке для прекращения попыток отправить сообщение')
				break

			TOO_MANY_REQUESTS = 429
			if status_code == TOO_MANY_REQUESTS:
				pause_time = TELEGRAM_SEND_NOTIFICATIONS.SLEEP_TIME_ON_TOO_MANY_REQUESTS

				_logger.debug(f"Это Too Many Requests, ухожу в \"спячку\" на {pause_time}.")
				time.sleep(pause_time)

	# Все ошибки будут обработаны тут
	_logger.error(f"Не смог отправить уведомление о создании новой заявки в телеграм: {error_message}")

@receiver(post_save, sender = FeedbackRequest)
def send_new_request_notification_by_telegram(sender, instance: FeedbackRequest, created, **kwargs):
	if not created:
		return
	if not BusinessConfig.get_solo().debug_email_sending_enabled:
		return
	# Делалось второпях
	message = f"""
Новая заявка!
Заявитель: {instance.requestener_name}
Номер телефона: {instance.phone_number}
""".lstrip()

	if instance.email:
		message += f"Почта: {instance.email}\n"

	if instance.comment:
		message += f"Комментарий:\n{instance.comment}\n"

	# TODO: Сделать через regex
	to: list[str] = BusinessConfig.get_solo().new_feedback_requests_receiver_emails.replace(' ', '').replace('\n', '').replace('\t', '').split(',')
	if send_mail(
		subject=f'Новая заявка от: {instance.created_at.strftime('%d/%m/%Y, %H:%M:%S')}',
		message=message,
		from_email='noreply@mysite.com',
		recipient_list = to,
	) > 0: instance.mark_as_seen()
