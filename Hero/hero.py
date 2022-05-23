from time import sleep


class Hero:
    def __init__(self, n, h, a):
        self.name = n
        self.health = h
        self.armor = a

    def print(self):
        print("Здоров'я: ", self.health)
        print("Броня: ", self.armor)


class Warrior(Hero):
    def hello(self):
        print('На коні з\'явився ВОЇН за іменем ', self.name)
        self.print()
        sleep(3)

    def attack(self, enemy):
        print('\nУдар! ВОЇН ' + self.name + "б'є мечем з силою 30 ворога " + enemy.name)
        sleep(2)
        enemy.armor -= 30
        if enemy.health < 0:
            enemy.health += enemy.armor
            enemy.armor = 0
        print('Страшний удар підкосив ' + enemy.name + " його броня становить = " + str(enemy.armor) + ", а здоров'я = " + str(enemy.health) + '\n')
        sleep(2)


class Magician(Hero):
    def hello(self):
        print('З телепорту вистрибнув МАГ за іменем ', self.name)
        self.print()
        sleep(3)

    def attack(self, enemy):
        print('\nЗакляття! МАГ ' + self.name + "зачарував з ураженням 40 ворога " + enemy.name)
        sleep(2)
        enemy.armor -= 40
        if enemy.health < 0:
            enemy.health += enemy.armor
            enemy.armor = 0
        print('Страшний удар підкосив ' + enemy.name + " його броня становить = " + str(enemy.armor) + ", а здоров'я = " + str(enemy.health) + '\n')
        sleep(2)


w = Warrior('Richard', 100, 50)
m = Magician('Gandelf', 50, 30)
w.hello()
m.hello()
w.attack(m)