class UserNotFollowing(Exception):
    def __init__(self, unfollowed_user_id: str):
        super().__init__(
            f"User with id {unfollowed_user_id} can not be unfollowed, becouse is not followed."
        )
