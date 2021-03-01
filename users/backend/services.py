from ..models import CustomUser
import logging

lgr = logging.getLogger(__name__)

from base.servicebase import ServiceBase


class CustomUserService(ServiceBase):
	"""
	Service for SystemService CRUD
	"""
	manager = CustomUser.objects

	def create(self, username, email, password, **kwargs):
		"""
		This method creates an entry with the given kwargs as for the given manager.
		@param username: username for the user.
		@param email: email of the user.
		@param password: password or the user.
		@param kwargs: key=>value methods to pass to the create method.
		@return: Created object or None on error.
		"""
		try:
			if 'pk' in kwargs and self.manager.get(pk = kwargs.get('pk', '')):
				return self.manager.get(pk = kwargs.get('pk', ''))  # Returned Object.
			if self.manager is not None:
				return self.manager.create_user(username, email, password, **kwargs)
		except Exception as e:
			lgr.exception('%sService create exception: %s' % (self.manager.model.__name__, e))
		return None
