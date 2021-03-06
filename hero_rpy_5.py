"""
Added a store. The hero can now buy a tonic or a sword. A tonic will add 2 to the hero's health wherease a sword will add 2 power.
"""
import random
import time

class Character(object):
    def __init__(self):
        self.name = '<undefined>'
        self.health = 10
        self.power = 5
        self.coins = 20

    def alive(self):
        return self.health > 0

    def attack(self, enemy):
        if not self.alive():
            return
        print "%s attacks %s" % (self.name, enemy.name)
        enemy.receive_damage(self.power)
        if not enemy.alive():
            self.coins += enemy.bounty
            print "%s collected %d bounty for killing %s" % (self.name,enemy.bounty,enemy.name)
        time.sleep(1.5)

    def receive_damage(self, points):
        self.health -= points
        print "%s received %d damage." % (self.name, points)
        if self.health <= 0:
            print "%s is dead." % self.name

    def print_status(self):
        print "%s has %d health and %d power." % (self.name, self.health, self.power)

class Hero(Character):
    def __init__(self):
        self.name = 'hero'
        self.health = 10
        self.power = 5
        self.coins = 20
        self.armour = 0
        self.armour_counter = 0
        self.bounty = 2
        self.evade = 0
        self.tonic_points = 0
        self.swap_power = False
        # self.evade_prob

    def restore(self):
        self.health = 10
        print "Hero's health is restored to %d!" % self.health
        time.sleep(1)

    def buy(self, item):
        self.coins -= item.cost
        item.apply(hero)

    def receive_damage(self, points):
        if self.evade > 0:
            if random.random() >= ((self.evade * 5)/100):
                if self.armour:
                    self.armour_counter -= 1
                if random.random() > .2:
                    super(Hero,self).receive_damage(points - self.armour)
                    print "%d Point being passed to receive_damage" % (points - self.armour)
                    print "Armounr Counter : %d" % self.armour_counter
                else:
                    double_damage = ((2 * points) - self.armour)
                    super(Hero,self).receive_damage(double_damage)
                    print "%d Point being passed to receive_damage" % (points - self.armour)
                    print "Armounr Counter : %d" % self.armour_counter
            else:
                return
                if self.armour_counter == 0:
                    self.armour_counter = 3
                    self.armour = 0

class Goblin(Character):
    def __init__(self):
        self.name = 'goblin'
        self.health = 6
        self.power = 2
        self.bounty = 3
        self.coins = 0

class Medic(Character):
    def __init__(self):
        self.name = 'medic'
        self.health = 7
        self.power = 3
        self.bounty = 5
        self.coins = 0

    def receive_damage(self, points):
        super(Medic,self).receive_damage(points)
        if random.random() < .2:
            self.health += 2

class Shadow(Character):
    def __init__(self):
        self.name = "shadow"
        self.health = 1
        self.power = 5
        self.bounty = 5
        self.coins = 0


    def receive_damage(self, points):
        if random.random() < 0.1:
            super(Shadow, self).receive_damage(points)
        else:
            return

class Zombie(Character):
    def __init__(self):
        self.name = "zombie"
        self.health = 10
        self.power = 2
        self.bounty = 25
        self.coins = 0


    def alive(self):
        return True

    def receive_damage(self, points):
        self.health -= points
        print "%s received %d damage." % (self.name, points)


class Wizard(Character):
    def __init__(self):
        self.name = 'wizard'
        self.health = 8
        self.power = 1
        self.bounty = 9
        self.coins = 0


    def attack(self, enemy):
        swap_power = random.random() > 0.5
        if swap_power:
            print "%s swaps power with %s during attack" % (self.name, enemy.name)
            self.power, enemy.power = enemy.power, self.power
        super(Wizard, self).attack(enemy)
        if swap_power:
            self.power, enemy.power = enemy.power, self.power

class Battle(object):
    def do_battle(self, hero, enemy):
        print "====================="
        print "Hero faces the %s" % enemy.name
        print "====================="
        while hero.alive() and enemy.alive():
            hero.print_status()
            enemy.print_status()
            time.sleep(1.5)
            print "-----------------------"
            print "What do you want to do?"
            print "1. fight %s" % enemy.name
            print "2. do nothing"
            print "3. flee"
            if hero.tonic_points:
                print "4. Add my tonic points from the weaponry."
            if hero.swap_power:
                print "5. Swap powers with the enemy."
            print "> ",
            input = int(raw_input())
            if input == 1:
                hero.attack(enemy)
            elif input == 2:
                pass
            elif input == 3:
                print "Goodbye."
                exit(0)
            elif input == 4:
                hero.health += hero.tonic_points
                hero.tonic_points = 0
            elif input == 5:
                temp_power = enemy.power
                enemy.power = hero.power
                hero.power = temp_power
                hero.swap_power = False
                print "%s and %s powers are swapped to %d and %d respectively" % (hero.name,enemy.name,hero.power,enemy.power)
            else:
                print "Invalid input %r" % input
                continue
            if input != 4 and input != 5:
                enemy.attack(hero)
        if hero.alive():
            hero.power = enemy.power
            print "You defeated the %s" % enemy.name
            return True
        else:
            print "YOU LOSE!"
            return False

class Tonic(object):
    cost = 5
    name = 'tonic'

    def apply(self, character):
        choice = raw_input("Do you want to use tonic now? (Y or N) : ").upper()
        if choice == 'Y':
            character.health += 2
            print "%s's health increased to %d." % (character.name, character.health)
        else:
            print "Tonic is stored in his weaponry"
            hero.tonic_points += 2

class SuperTonic(object):
    cost = 10
    name = 'supertonic'

    def apply(self, character):
        character.health += 10
        print "%s's health increased to %d." % (character.name, character.health)


class Sword(object):
    cost = 10
    name = 'sword'

    def apply(self, hero):
        hero.power += 2
        print "%s's power increased to %d." % (hero.name, hero.power)

class Armour(object):
    cost = 6
    name = "armour"

    def apply(self, hero):
        hero.armour = 2
        hero.armour_counter = 3
        print "%s's armour increased to %d." % (hero.name, hero.armour)

class Evade(object):
    cost = 15
    name = "evade"

    def apply(self, hero):
        if hero.evade >= 18:
            hero.evade = 18
            print "%s's evade cannot increse more than 90%" % hero.name
        else:
            hero.evade += 2
            print "%s's evade increased to %d." % (hero.name, hero.evade)

class SwapPower(object):
    cost = 15
    name = "swap_power"

    def apply(self, character):
        print "Swap Power is stored in his weaponry"
        character.swap_power = True


class Store(object):
    items = [Tonic, SuperTonic, Armour, Sword, Evade, SwapPower]
    def do_shopping(self, hero):
        while True:
            print "====================="
            print "Welcome to the store!"
            print "====================="
            print "You have %d coins." % hero.coins
            print "What do you want to do?"
            for i in xrange(len(Store.items)):
                item = Store.items[i]
                print "%d. buy %s (%d)" % (i + 1, item.name, item.cost)
            print "9. leave"
            input = int(raw_input("> "))
            if input == 9:
                break
            else:
                ItemToBuy = Store.items[input - 1]
                item = ItemToBuy()
                if hero.coins >= item.cost:
                    hero.buy(item)
                else:
                    print "You have insufficient funds to buy this item. Go rob a bank."    
hero = Hero()
enemies = [Goblin(), Shadow(), Wizard(),Zombie()]
battle_engine = Battle()
shopping_engine = Store()

for enemy in enemies:
    hero_won = battle_engine.do_battle(hero, enemy)
    if not hero_won:
        print "YOU LOSE!"
        exit(0)
    shopping_engine.do_shopping(hero)
print "YOU WIN!"
