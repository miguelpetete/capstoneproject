class UserServicies:
    def is_registered(self, user_id: int) -> bool:
        """
        Verify if an user is registered in the db.

        :param user_id-> id of the user that identifies it.

        :return -> True if user is registered. False if don't.
        """

    def has_jobs(self, user_id: int) -> [int]:
        """
        Verify if an user is registered in the db and has offers

        :param user_id-> id of the user that identifies it.

        :return -> Empty if the user doesn't have any job offers. A list of
        the jobs that has aplied.
        """
