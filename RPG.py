import random
import time
import sys

class Item:
    def __init__(self, name, effect, value):
        self.name = name
        self.effect = effect
        self.value = value

class Character:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.max_health = 100
        self.health = 100
        self.max_mana = 50
        self.mana = 50
        self.attack = 10
        self.defense = 5
        self.exp = 0
        self.coins = 50
        self.critical_chance = 0.2  # 20% chance for critical hit

    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.attack += 5
        self.defense += 2
        print(f"{self.name} leveled up! Level: {self.level}")
        print(f"Health: {self.health}, Mana: {self.mana}, Attack: {self.attack}, Defense: {self.defense}")

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level_up()

    def gain_coins(self, amount):
        self.coins += amount
        print(f"You gained {amount} coins. Total: {self.coins} coins")

class Monster:
    def __init__(self, name, health, attack, defense, exp_reward, coin_reward):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.coin_reward = coin_reward
        self.critical_chance = 0.15  # 15% chance for critical hit

def calculate_damage(attacker, defender):
    if random.random() < attacker.critical_chance:
        critical_damage = max(0, attacker.attack * 2 - defender.defense)  # Double damage for critical hit
        print("Critical Hit!")
        return critical_damage
    else:
        normal_damage = max(0, attacker.attack - defender.defense)
        return normal_damage

def loading_animation():
    print("Loading", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()  # New line after loading animation

def battle(player, monster):
    print(f"A wild {monster.name} appears!")
    while player.health > 0 and monster.health > 0:
        print(f"\n{player.name} HP: {player.health}/{player.max_health} | Mana: {player.mana}/{player.max_mana}")
        print(f"{monster.name} HP: {monster.health}")
        action = input("Do you want to (A)ttack or (R)un? ").lower()
        if action == 'a':
            if player.mana >= 5:  # Memeriksa apakah cukup mana untuk menyerang
                damage = calculate_damage(player, monster)
                monster.health -= damage
                player.mana -= 5  # Mengurangi mana saat menyerang
                print(f"You attacked {monster.name} for {damage} damage.")
                print(f"Mana decreased to {player.mana}/{player.max_mana}.")
                if monster.health <= 0:
                    print(f"You defeated {monster.name}!")
                    player.gain_exp(monster.exp_reward)
                    player.gain_coins(monster.coin_reward)
                    loading_animation()  # Menambahkan loading sebelum kembali ke menu
                    return True

                # Monster attacks player
                damage = calculate_damage(monster, player)
                player.health -= damage
                print(f"{monster.name} attacked you for {damage} damage.")
                if player.health <= 0:
                    print("You have been defeated!")
                    loading_animation()  # Menambahkan loading sebelum game over
                    return False
            else:
                print("Not enough mana to attack!")
        elif action == 'r':
            if random.random() < 0.5:
                print("You successfully ran away!")
                loading_animation()  # Menambahkan loading sebelum kembali ke menu
                return True
            else:
                print("You failed to run away!")
                # Monster attacks player
                damage = calculate_damage(monster, player)
                player.health -= damage
                print(f"{monster.name} attacked you for {damage} damage.")
        else:
            print("Invalid action. Please choose A or R.")

def shop(player):
    items = [
        Item("Health Potion", "Restores 50 HP", 20),
        Item("Mana Potion", "Restores 30 Mana", 15),
        Item("Attack Boost", "Increases attack by 5", 30),
        Item("Defense Boost", "Increases defense by 3", 25)
    ]

    while True:
        print("\n==== SHOP ====")
        print(f"Your coins: {player.coins}")
        for i, item in enumerate(items):
            print(f"{i+1}. {item.name} - {item.value} coins")
        print("0. Exit shop")

        choice = input("Enter the number of the item you want to buy (0 to exit): ")
        if choice == '0':
            break
        try:
            item = items[int(choice) - 1]
            if player.coins >= item.value:
                player.coins -= item.value
                if item.name == "Health Potion":
                    player.health = min(player.max_health, player.health + 50)
                    print(f"You used {item.name}. Health restored to {player.health}")
                elif item.name == "Mana Potion":
                    player.mana = min(player.max_mana, player.mana + 30)
                    print(f"You used {item.name}. Mana restored to {player.mana}")
                elif item.name == "Attack Boost":
                    player.attack += 5
                    print(f"You used {item.name}. Attack increased to {player.attack}")
                elif item.name == "Defense Boost":
                    player.defense += 3
                    print(f"You used {item.name}. Defense increased to {player.defense}")
                loading_animation()  # Menambahkan loading setelah membeli item
            else:
                print("Not enough coins!")
        except (ValueError, IndexError):
            print("Invalid choice!")

def main():
    print("Welcome to the RPG Game!")
    player_name = input("Enter your character's name: ")
    player = Character(player_name)

    monsters = [
        Monster("Wild Pikachu", health=30, attack=8, defense=2, exp_reward=20, coin_reward=10),
        Monster("Wild Bulbasaur", health=40, attack=7, defense=3, exp_reward=25, coin_reward=15),
        Monster("Wild Charmander", health=35, attack=9, defense=1, exp_reward=22, coin_reward=12)
    ]

    while player.health > 0:
        print("\n==== MAIN MENU ====")
        print(f"1. Explore")
        print(f"2. Visit Shop")
        print(f"3. Check Status")
        print(f"4. Rest (Restore Mana)")
        print(f"5. Quit Game")

        choice = input("What would you like to do? ")

        if choice == '1':
            monster = random.choice(monsters)
            battle_result = battle(player, monster)
            if not battle_result:
                break
        elif choice == '2':
            shop(player)
        elif choice == '3':
            print(f"\n==== {player.name}'s Status ====")
            print(f"Level: {player.level}")
            print(f"Health: {player.health}/{player.max_health}")
            print(f"Mana: {player.mana}/{player.max_mana}")
            print(f"Attack: {player.attack}")
            print(f"Defense: {player.defense}")
            print(f"EXP: {player.exp}/{player.level * 100}")
            print(f"Coins: {player.coins}")
            loading_animation()  # Menambahkan loading setelah mengecek status
        elif choice == '4':
            mana_restored = min(player.max_mana - player.mana, 20)
            player.mana += mana_restored
            print(f"You rested and restored {mana_restored} Mana. Current Mana: {player.mana}/{player.max_mana}")
            loading_animation()  # Menambahkan loading setelah istirahat
        elif choice == '5':
            print("Thank you for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

    print("Game Over!")

if __name__ == "__main__":
    main()
