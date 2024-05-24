import threading
import time
import requests
import Game.GameThread
from Game import ClientThread
from Game.ClientThread import State


class MatchmakingThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = []
        self.is_alive = True

    def run(self):
        while self.is_alive:
            if len(self.queue) >= 2:
                tmpP1: ClientThread.ClientThread = self.queue[0]
                tmpP2: ClientThread.ClientThread = self.queue[1]
                if tmpP1.state == State.QUEUE and tmpP2.state == State.QUEUE:
                    player1: ClientThread.ClientThread = self.queue.pop(0)
                    player2: ClientThread.ClientThread = self.queue.pop(0)
                    player1.state = State.PLAY
                    player2.state = State.PLAY
                    Game.GameThread.GameThread(player1, player2).start()
                time.sleep(1)

    def add_to_queue(self, player: ClientThread.ClientThread):
        print(f"Adding player {player.uuid} to queue")
        player.uuid = self.clean_uuid(player.uuid)
        self.queue.append(player)
        self.order_queue()

    def clean_uuid(self, uuid):
        if isinstance(uuid, bytes):
            uuid = uuid.decode('utf-8')
        clean_uuid = uuid.strip("b'").split("\\x")[0]
        clean_uuid = clean_uuid.split("\\")[0]
        clean_uuid = clean_uuid.replace("'", "").strip()
        return clean_uuid

    def get_rank_by_uuid(self, uuid):
        try:
            response = requests.get(f'http://localhost:5000/rank/{uuid}')
            if response.status_code == 200:
                rank_data = response.json()
                return rank_data['value']
            else:
                print(f"Failed to get rank for uuid {uuid}: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error during request to get rank: {e}")
            return None

    def order_queue(self):
        # Initialiser les listes pour les paires et les utilisateurs sans paires
        pairs = []
        unpaired_users = []
        paired_users = set()

        # Itérer sur la liste des utilisateurs sans les trier préalablement
        for i, queue in enumerate(self.queue):
            # Ignorer les utilisateurs déjà appariés
            if queue in paired_users:
                continue

            # Initialiser la paire comme non trouvée pour cet utilisateur
            pair_found = False
            closest_diff = float('inf')
            closest_user = None

            # Essayer de trouver la paire la plus proche pour cet utilisateur
            for j in range(i + 1, len(self.queue)):
                if self.queue[j] not in paired_users:
                    user_rank = self.get_rank_by_uuid(queue.uuid)
                    potential_pair_rank = self.get_rank_by_uuid(self.queue[j].uuid)

                    # Calculer la différence de rang
                    diff = abs(user_rank - potential_pair_rank)

                    # Trouver la paire la plus proche sans dépasser 500 points de différence
                    if diff <= 500 and diff < closest_diff:
                        closest_diff = diff
                        closest_user = self.queue[j]

            # Vérifier si une paire a été trouvée
            if closest_user is not None:
                pairs.append((queue, closest_user))
                paired_users.add(queue)
                paired_users.add(closest_user)
                pair_found = True

            # Si aucun pair n'a été trouvé pour cet utilisateur, l'ajouter aux utilisateurs sans paires
            if not pair_found:
                unpaired_users.append(queue)

        return pairs, unpaired_users

    def update_rank(self, uuid):
        # Nettoyer l'UUID avant utilisation
        uuid = self.clean_uuid(uuid)

        # Vérifier si l'utilisateur existe dans la table user via l'API
        user_exists = self.check_user_exists_api(uuid)

        if not user_exists:
            raise ValueError("User does not exist")

        # Vérifier si l'utilisateur a une entrée dans la table rank via l'API
        user_rank = self.get_rank_by_uuid_api(uuid)

        if user_rank is None:
            # Insérer une nouvelle entrée avec une valeur de 500 si aucune entrée n'existe
            self.create_rank_entry_api(uuid, 500)
        else:
            print(f"User {uuid} already has a rank entry.")

    # Méthode pour vérifier si l'utilisateur existe via l'API
    def check_user_exists_api(self, uuid):
        response = requests.get(f"http://localhost:5000/users/uuid/{uuid}")
        return response.status_code == 200

    # Méthode pour obtenir le rang de l'utilisateur par UUID via l'API
    def get_rank_by_uuid_api(self, uuid):
        response = requests.get(f"http://localhost:5000/ranks/{uuid}")
        if response.status_code == 200:
            return response.json().get('value')
        return None

    # Méthode pour créer une nouvelle entrée de rang via l'API
    def create_rank_entry_api(self, uuid, value):
        payload = {
            'uuid_player': uuid,
            'value': value
        }
        response = requests.post("http://localhost:5000/rank", json=payload)
        if response.status_code == 200:
            print(f"New rank entry created for user {uuid} with value {value}")
        else:
            raise Exception(f"Failed to create rank entry for user {uuid}: {response.text}")
