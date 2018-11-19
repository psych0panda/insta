import json
from time import sleep


class Bot:

    def __init__(self,
                 logger: object,
                 api: object,
                 pk: object='',
                 username: object='',
                 rank_token: object='',
                 query: object='')-> object:
        self.logger = logger
        self.api = api
        self.pk = pk
        self.username = username
        self.query = query
        self.rank_token = rank_token
        self.my_followers_pk = []

    def top_tags_pk(self)-> list:
        output_list = []
        top_tags_pk = []
        results = self.api.top_search(self.query)
        output_list.extend(results.get('users', []))
        for i in output_list:
            pk = i.get('user')
            top_tags_pk.append(pk.get('pk'))
        return top_tags_pk

    def get_tag_followers_pk(self)-> list:
        users_list = []
        tag_followers_pk = []
        for i in self.top_tags_pk():
            followers = self.api.user_followers(i, self.rank_token)
            users_list.extend(followers.get('users', []))
            next_max_id = followers.get('next_max_id')
            while next_max_id:
                followers = self.api.user_followers(i, self.rank_token, max_id=next_max_id)
                users_list.extend(followers.get('users', []))
                if len(users_list) >= 600:
                    break
                next_max_id = followers.get('next_max_id')
        for i in users_list:
            tag_followers_pk.append(i.get('pk'))
        return tag_followers_pk

    def my_followers(self)-> list:
        my_followers = []
        results = self.api.user_following(self.api.authenticated_user_id, self.rank_token)
        my_followers.extend(results.get('users', []))
        self.logger.debug("Queue size u following ", len(my_followers))
        if len(my_followers) >= 7500:
            self.logger.debug("Maximum queue size u following ")
            for follower in my_followers:
                sleep(120)
                self.api.friendships_destroy(follower.get('pk'))
                self.logger.debug("Destroy friendships with user ", follower.get('pk'))
        else:
            for follower in my_followers:
                self.my_followers_pk.append(follower.get('pk'))
            return self.my_followers_pk

    def friend_request(self)-> None:
        targets = self.get_tag_followers_pk()
        for target in targets:
            if target in self.my_followers_pk:
                self.logger.debug('You are already friends with this user')
                continue
            else:
                sleep(120)
                self.api.friendships_create(target)
                self.logger.debug('Subscription to user')

