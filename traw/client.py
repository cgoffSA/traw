from . import const
from . import models
from .api import API
from .utils import dispatchmethod


class Client(object):
    """ The Client class is the primary access point for the Testrail API

    The intended way to use this class is:

    .. code-block:: python

        import traw
        testrail = traw.Client(username='username',
                               user_api_key='api_key',
                               url='url')

    Authentication credentials will be pulled in the following order:
     - TRAW Client instantiation
       - traw.Client(username='<username>', user_api_key='<api_key>', url='<url>')
       - (optional) You may substitute `password` for `user_api_key`
     - Environmental variables
       - TRAW_USERNAME=<username>
       - TRAW_USER_API_KEY=<api_key>
       - TRAW_URL=<url>
       - (optional) You may substitude `TRAW_PASSWORD` for `TRAW_USER_API_KEY`
     - A configuration file in the user's home directory (~/.traw_config)
       - [TRAW]
         username = <username>
         user_api_key = <user_api_key>
         url = <url>
       - (optional) You may substitute `password = <password>` for `user_api_key`

    If both a user api key and a user password are provided, the api key will be used
    """
    def __init__(self, **credentials):
        """ Initialize the TRAW instance """
        self._api = API(**credentials)

    # POST generics
    @dispatchmethod
    def add(self, obj):
        # Not directly implemented. TypeError is raised if called directly
        pass  # pragma: no cover

    @dispatchmethod
    def close(self, obj):
        # Not directly implemented. TypeError is raised if called directly
        pass  # pragma: no cover

    @dispatchmethod
    def delete(self, obj):
        # Not directly implemented. TypeError is raised if called directly
        pass  # pragma: no cover

    @dispatchmethod
    def update(self, obj):
        # Not directly implemented. TypeError is raised if called directly
        pass  # pragma: no cover

    # Case type related methods
    def case_types(self):
        """ Returns the generator of case types

        :yields: models.CaseType Objects

        """
        for case_type in self._api.case_types():
            yield models.CaseType(self, case_type)

    # Priorities related methods
    def priorities(self):
        """ Returns the generator of Priorities

        :yields: models.Priority Objects
        """
        for priority in self._api.priorities():
            yield models.Priority(self, priority)

    # Project related methods
    @dispatchmethod
    def project(self):
        """ Return a Project instance
            `client.project()` returns a new Project instance (no API call)
            `client.project(1234)` returns a Project instance with an id or 1234
        """
        return models.Project(self)

    @project.register(int)
    def _project_by_id(self, project_id):
        """ Do not call directly
            Returns project with ``project_id``
        """
        return models.Project(self, self._api.project_by_id(project_id))

    def projects(self, active_only=False, completed_only=False):
        """ Returns the generator of available projects

        Leaving both active_only and completed_only will return all projects

        :param active_only: Only include currently active projects in list
        :param completed_only: Only include completed projects in list

        :yields: models.Project Objects
        """
        if active_only is True and completed_only is True:
            raise TypeError('Either `active_only` or `completed_only` can be '
                            'set, but not both')

        elif active_only is True or completed_only is True:
            is_completed = 1 if completed_only else 0
        else:
            is_completed = None

        for project in self._api.projects(is_completed):
            yield models.Project(self, project)

    # Status related methods
    def statuses(self):
        """ Returns the generator of statuses

        :yields: models.Status Objects
        """
        for status in self._api.statuses():
            yield models.Status(self, status)

    # Template related methods
    @dispatchmethod
    def templates(self):
        """ Return template instances for the given project object or project ID

        :param project: models.Project object for a project that exists in TestRail
        :param int: Project ID for a project that exists in TestRail

        :yields: models.Template objects
        """
        raise NotImplementedError(const.NOTIMP.format("models.Project or int"))

    @templates.register(int)
    def _templates_by_project_id(self, project_id):
        for template in self._api.templates(project_id):
            yield models.Template(self, template)

    @templates.register(models.Project)
    def _templates_by_project(self, project):
        for template in self._api.templates(project.id):
            yield models.Template(self, template)

    # User related methods
    @dispatchmethod
    def user(self):
        """ Return a User instance
            `client.user()` returns a new User instance (no API call)
            `client.user(1234)` returns a User instance with an ID of 1234
            `client.user('user@email.com')` returns a User instance
                with an email of user@email.com
        """
        return models.User(self)

    @user.register(str)
    def _user_by_email(self, email):
        """ Do not call directly
            Returns user associated with ``email``
        """
        if '@' not in email:
            raise ValueError('"email" must be a string that includes an "@" sym')

        return models.User(self, self._api.user_by_email(email))

    @user.register(int)
    def _user_by_id(self, user_id):
        """ Do not call directly
            Returns user with ``user_id``
        """
        return models.User(self, self._api.user_by_id(user_id))

    def users(self):
        """ Returns the generator of available Users

        :yields: models.User Objects
        """
        for user in self._api.users():
            yield models.User(self, user)
