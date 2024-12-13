import random
import time
import sys


# Utility Functions
def slow_print(text, delay=0.05):
    """Prints text character by character with a delay."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def slow_input(prompt, delay=0.025):
    """Prints a prompt with a delay and returns the user input."""
    slow_print(prompt, delay)
    return input()


# Classes
class Player:
    def __init__(self, name, race, weapon):
        self.name = name.capitalize()
        self.race = race.capitalize()
        self.weapon = weapon.capitalize()
        self.health = Player.health_by_race(self.race)
        self.base_damage = Player.default_damage_by_weapon(self.weapon)
        self.damage = self.calculate_damage()

    @staticmethod
    def health_by_race(race):
        """Returns health based on race."""
        health_values = {
            "Human": 100,
            "Elf": 75,
            "Orc": 125
        }
        return health_values.get(race, 100)

    @staticmethod
    def default_damage_by_weapon(weapon):
        """Returns base damage based on weapon."""
        damage_values = {
            "Sword": 10,
            "Axe": 15,
            "Bow": 8
        }
        return damage_values.get(weapon, 10)

    def calculate_damage(self):
        """Calculates total damage based on race and weapon bonuses."""
        race_weapon_bonus = {
            "Human": {"Sword": 2, "Axe": 0, "Bow": -1},
            "Elf": {"Sword": -1, "Axe": -2, "Bow": 3},
            "Orc": {"Sword": 1, "Axe": 3, "Bow": -2}
        }
        return self.base_damage + race_weapon_bonus[self.race][self.weapon]


class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage


def generate_enemy(area):
    """Generates a new enemy for the given area."""
    enemies = {
        "City": [Enemy("Rat", 10, 2), Enemy("Wolf", 20, 5)],
        "Forest": [Enemy("Rat", 10, 2), Enemy("Snake", 15, 3)],
        "Cave": [Enemy("Snake", 15, 3), Enemy("Wolf", 20, 5)],
        "Field": [Enemy("Snake", 15, 3)],
        "Bandit Village": [Enemy("Wolf", 20, 5)],
        "Mountain": [Enemy("Wolf", 20, 5)],
        "Second Level of Cave": [Enemy("Snake", 15, 3), Enemy("Wolf", 20, 5)]
    }
    if area in enemies:
        return random.choice(enemies[area])
    return None


# Combat Function
def combat(player, enemy):
    """Handles combat between the player and an enemy."""
    slow_print(f"A wild {enemy.name} appears!")

    race_weapon_miss_chance = {
        "Human": {"Sword": 5, "Axe": 20, "Bow": 10},
        "Elf": {"Sword": 10, "Axe": 15, "Bow": 5},
        "Orc": {"Sword": 10, "Axe": 5, "Bow": 20}
    }
    race_dodge_chance = {
        "Human": 10,
        "Elf": 20,
        "Orc": 5
    }

    player_miss_chance = race_weapon_miss_chance[player.race][player.weapon]
    player_dodge_chance = race_dodge_chance[player.race]
    enemy_miss_chance = 20
    enemy_dodge_chance = 15

    while player.health > 0 and enemy.health > 0:
        # Player attacks
        if random.randint(1, 100) <= player_miss_chance:
            slow_print("You missed your attack!")
        elif random.randint(1, 100) <= enemy_dodge_chance:
            slow_print(f"The {enemy.name} dodged your attack!")
        else:
            player_damage = random.randint(player.damage - 2, player.damage + 2)
            enemy.health -= player_damage
            slow_print(f"You hit the {enemy.name} for {player_damage} damage. {enemy.name} has {max(0, enemy.health)} health left.")

        if enemy.health <= 0:
            slow_print(f"You defeated the {enemy.name}!")
            return "Victory"

        # Enemy attacks
        if random.randint(1, 100) <= enemy_miss_chance:
            slow_print(f"The {enemy.name} missed its attack!")
        elif random.randint(1, 100) <= player_dodge_chance:
            slow_print("You dodged the attack!")
        else:
            enemy_damage = random.randint(enemy.damage - 2, enemy.damage + 2)
            player.health -= enemy_damage
            slow_print(f"The {enemy.name} hits you for {enemy_damage} damage. You have {max(0, player.health)} health left.")

        if player.health <= 0:
            slow_print(f"You were defeated by the {enemy.name}. Game over.")
            return "Game Over"


# Navigation Function
def navigate(player, current_area):
    """Handles navigation based on the player's current location."""
    areas = {
        "Human Village": ["City", "Forest", "Cave"],
        "Elf Village": ["City", "Forest", "Cave"],
        "Orc Village": ["City", "Forest", "Cave"],
        "City": ["Forest", "Field", "Bandit Village", player.race + " Village"],
        "Forest": ["City", "Cave", "Mountain", player.race + " Village"],
        "Cave": ["Second Level of Cave", "Forest", player.race + " Village"],
        "Second Level of Cave": ["Cave", "Forest"],
        "Field": ["City"],
        "Bandit Village": ["City"],
        "Mountain": ["Forest"]
    }

    while True:
        slow_print(f"You are currently in {current_area}.")
        slow_print(f"From here, you can go to: {', '.join(areas[current_area])}.")
        next_area = slow_input("Where do you want to go? ").title()
        if next_area in areas[current_area]:
            return next_area
        slow_print("Invalid choice. Please choose a valid area.")


# Health Restoration
def restore_health(player):
    """Restores the player's health to its maximum based on their race."""
    player.health = Player.health_by_race(player.race)
    slow_print(f"You have returned to the {player.race} Village and restored your health to {player.health}.")


# Game Initialization Functions
def choose_race():
    """Prompts the player to choose a race."""
    valid_races = ["Human", "Elf", "Orc"]
    while True:
        race = slow_input("Pick your race: Human, Elf, or Orc: ").capitalize()
        if race in valid_races:
            return race
        slow_print("Invalid choice. Please pick Human, Elf, or Orc.")


def choose_weapon():
    """Prompts the player to choose a weapon."""
    valid_weapons = ["Sword", "Axe", "Bow"]
    while True:
        weapon = slow_input("Pick your weapon: Sword, Axe, or Bow: ").capitalize()
        if weapon in valid_weapons:
            return weapon
        slow_print("Invalid choice. Please pick Sword, Axe, or Bow.")


# Main Game Logic
def main():
    slow_print("Welcome to the game!")
    name = slow_input("What is your name? ")

    # Choose race and weapon
    race = choose_race()
    weapon = choose_weapon()

    # Determine starting village
    starting_village = f"{race} Village"

    # Create player instance
    player = Player(name, race, weapon)

    # Display player stats
    slow_print(f"{player.name}, the {player.race}, has picked a {player.weapon}.")
    slow_print(f"You start with {player.health} health.")
    slow_print(f"Your weapon's base damage is {player.base_damage}.")
    slow_print(f"With your {player.race} bonus, your total damage is {player.damage}.")

    # Starting area
    current_area = starting_village

    # Main game loop
    while True:
        if current_area not in ["Human Village", "Elf Village", "Orc Village"]:
            enemy = generate_enemy(current_area)
            if enemy:
                result = combat(player, enemy)
                if result == "Game Over":
                    break
                slow_print(f"After defeating the {enemy.name}, you continue your journey.")
        elif current_area in ["Human Village", "Elf Village", "Orc Village"]:
            slow_print(f"You are in the {current_area}. Resting here restores your health.")
            restore_health(player)

        current_area = navigate(player, current_area)


# Run the game
if __name__ == "__main__":
    main()
