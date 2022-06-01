from ast import Pass
import json
import sys
import time
from math import ceil

import vk_api

import settings
from interfaces.IGraph import IGraph
from interfaces.ILink import ILink
from interfaces.INode import INode
from settings import CHUNK_SIZE

try:
    from local_settings import LOGIN, PASSWORD
except ImportError:
    print("Local settings not found.")

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def log_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_social_graph(vk, user_list: list):
    graph = IGraph([], [])
    visited = set()

    def get_start_users(start_users: list):
        users, id_erros = vk_api.vk_request_one_param_pool(
            vk,
            'users.get',
            key='user_ids',
            values=start_users,
            default_values={'fields': 'photo'}
        )

        if id_erros:
            log_error("Error in [get start_users]")
            log_error(id_erros)

        for user in users:
            user_info = users[user][0]
            user_id = user_info['id']
            user_photo = user_info['photo']
            user_node = INode(user_id, {'photo': user_photo})
            graph.add_node(user_node)

    def get_deep_friends(user_ids: list):
        chunk_amount = ceil(len(user_ids) / CHUNK_SIZE)
        for chunk in range(chunk_amount):
            deep_friends, errors = vk_api.vk_request_one_param_pool(
                vk,
                'friends.get',
                key='user_id',
                values=user_ids[chunk * CHUNK_SIZE: (chunk + 1) * CHUNK_SIZE],
                default_values={"fields": "photo"}
            )

            if errors:
                log_error("Error in [get_deep_friends]")
                log_error(errors)

            for user_id, response in deep_friends.items():
                friends = response['items']
                for friend in friends:
                    friend_node = INode(
                        friend['id'], {'photo': friend['photo']})
                    link = ILink(user_id, friend['id'])
                    graph.add_node(friend_node)
                    graph.add_link(link)
                    visited.add(user_id)

    get_start_users(user_list)

    for _ in range(settings.DEPTH):
        ids = [node.id for node in graph.nodes if not node.id in visited]
        get_deep_friends(ids)

    return graph


def main():
    start_users = None
    # Args check
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith('-'):
            arg_info = arg.split('=')
            if arg_info[0] == '-input' or arg_info[0] == '-i':
                settings.INPUT_FILE = arg_info[1]
            elif arg_info[0] == '-users' or arg_info[0] == '-u':
                start_users = arg_info[1].split(',')
            elif arg_info[0] == '-output' or arg_info[0] == '-o':
                settings.OUTPUT_FILE = arg_info[1]
            elif arg_info[0] == '-depth' or arg_info[0] == '-d':
                settings.DEPTH = int(arg_info[1])
    # Args check end
    if not start_users:
        with open(settings.INPUT_FILE, "r") as file:
            data = file.read().strip()
            start_users = json.loads(data)
    if not start_users:
        print("Start users is empty.")
        return
    if not settings.OUTPUT_FILE:
        settings.OUTPUT_FILE = '_'.join(map(str, start_users)) + '.out'


    vk_session = vk_api.VkApi(LOGIN, PASSWORD, captcha_handler=captcha_handler)
    try:
        vk_session.auth()
        vk = vk_session.get_api()
    except vk_api.AuthError as error_msg:
        log_error("vk_api.AuthError", error_msg)
        return

    graph = get_social_graph(vk, start_users)
    with open(settings.OUTPUT_FILE, "w") as file:
        file.write(graph.toJSON())


if __name__ == "__main__":
    t1 = time.time()
    main()
    print("Time elapsed", time.time() - t1)
