import sys 
import os
import random
import pandas as pd
from time import sleep
global enemy
global level

#Start game
os.system('clear')
print('_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_')
print('_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_')
print('_-_-_-_-_Welcome to DUNGEON OF GREED_-_-_-_-_')
print('_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_')
print('_-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-__-_-_-_-_')
print('')
print('')
sleep(1)

# adding some comment

#$str,defense,agi,intel,hitchance,critchance,critmulti
night_elf = [8,10,5,10,80,10,1.5]
shadow_assasin = [2,10,15,10,90,10,1.5]
blood_priest = [6,6,3,10,85,10,1.5]
level = 1
room = ''
monsterlist = pd.read_csv('dog_monsters_v1.csv') #importing all the monsters of the game
wealth_list = pd.read_csv('dog_wealth_v1.csv') #importing all wealth drops of the game

class Hero:
	def __init__(self,name,strength,defense,agility,intel,hit_chance,crit_chance,crit_multi): #, hit_chance, crit_chance, crit_multi, defense, intel, agility, looting, greed)
		self.name = name
		self.strength = strength
		self.hp = 100 + self.strength
		self.health = self.hp
		self.damage = strength * 0.5 + 5
		self.agility = agility
		self.hit_chance = hit_chance
		self.crit_chance = crit_chance + self.agility
		self.defense = defense
		self.intel = intel
		self.agility = agility
		self.crit_multi = crit_multi
		self.greed = 1
		self.weapon = []
		self.weapon_wielded = []
		self.gear = []
		self.gear_wielded = []
		self.wealth = []
		self.pots = {'small': 1, 'medium': 0, 'large': 0}

	def levelup(self):
		self.strength +=1
		self.agility +=1
		self.intel += 1
		self.hp += 10


#function for name and player setup
def herosetup():
	t1 = 'What is your ancient name?' + '\n'
	for character in t1:
		sys.stdout.write(character)
		sys.stdout.flush()
		sleep(0.05)

	playername = input(str('->'))

#assigning the hero class based on user input
	t2 = 'Choose from any of the below roles for today!' + '\n'
	for character in t2:
		sys.stdout.write(character)
		sys.stdout.flush()
		sleep(0.03)

	print('Press 1 to play as NIGHT ELF')
	print('Press 2 to play as SHADOW ASSASSIN')
	print('Press 3 to play as BLOOD PRIEST')
	print('\n')

	playerhero = 0
	while playerhero == 0:
		playerhero = input(str('->'))
		if playerhero == '1':
			char_class = ('Night elf')
			#Create the hero object
			hero = Hero(playername,8,10,5,10,80,10,1.5)
			print(hero.name + ' the ' + 'Night elf has entered the game')
	

		elif playerhero == '2':
			char_class = ('Shadow assasin')
			hero = Hero(playername,2,10,15,10,90,10,1.5)
			print(hero.name + ' the ' + 'Shadow assasin has entered the game')
			

		elif playerhero == '3':
			char_class = ('Blood priest')
			hero = Hero(playername,6,6,3,10,85,10,1.5)
			print(hero.name + ' the ' + 'blood priest has entered the game')
			
		else:
			print('Please choose from the available roles!' + '\n')
			playerhero = 0
	return hero, char_class

#This function let's the play choose which room to enter
junction_history = ['1','2','3'] #handler to prevent room re-enter abuse. This should be reset after level clear. 

def junction():
	t3 = ('Which room would you to enter?' + '\n')
	for character in t3:
		sys.stdout.write(character)
		sys.stdout.flush()
		sleep(0.03)
	while len(junction_history) > 0:
		if '1' in junction_history:
			print('Press 1 to enter the Battle Room')
		if '2' in junction_history:
			print('Press 2 to enter the Trap Room')
		if '3' in junction_history:
			print('Press 3 to enter the Aeon Chamber')
		room_choice = input('->')
		if room_choice == '1':
			junction_history.pop(0)
			battleroom()
			break
		elif room_choice == '2':
			junction_history.pop(1)
			break
			#call trap room function
		elif room_choice == '3':
			junction_history.pop(2)
			break
			#call Aeon chamber function
		else:
			print('You walk into a wall and hurt yourself...' + '\n')
			hero.health -=1
			#handle death possibility

#prints status of the hero 
def status(): #need to expand this to include potions, inventory, wealth, current greed level etc
	print(hero.name + ' the ' + char_class)
	print('HP:' + str(hero.health) +'/' +str(hero.hp))
	print('Current Level {}'.format(level))
	print(room)


def battleroom():
	room = 'Battle Room'
	t4 ='You enter a dim cave and hear something sinister stir in the shadows...'
	for character in t4:
		sys.stdout.write(character)
		sys.stdout.flush()
		sleep(0.02)
	enemy = monster_spawn() #stored the return value (class object) of the function in a new variale to be reused in fight function
	print('\n'+ 'You encounter some dangerous looking ' + enemy.name)
	battle_choices(hero,enemy)


def monster_spawn():
	monster_options = monsterlist.loc[monsterlist['Level'] == level] #Makes a dataframe of monsters in current level from main dataframe
	monster_random = random.randint(0,(len(monster_options) - 1)) #Generates a random number to pick the monster
	monster_data = monster_options.iloc[monster_random] #Generates a dataframe of the chosen monster
	monster = Monster(monster_data) #creates the monster object
	return monster

def battle_choices(hero,enemy):
	print('1. Attack' + '\n' + '2. Flee' + '\n' + '3. Potion' + '\n' + 'Your Turn!' + '\n') #make functions for 2 and 3 
	battle_action = input(str('->')) #validate input for incorrect options
	if battle_action == '1':
		fight(hero,enemy)
	elif battle_action == '2':
		flee(hero,enemy) #attemps to flee the battle room 
	elif battle_action == '3':
		potion(hero,enemy) #allows hero to consume potions
	else:
		print('Please s2elect a valid input...')	
		battle_choices(hero,enemy)

def fight(hero, enemy):
	if 1 ==1: #useless line kept for faulty indentation
		initiative = random.randint(1,101) + hero.agility
		status()
		print('\n' + '\n' + '--------battle-------')
		print(enemy.name + ' health: ' +str(enemy.health) +'/' + str(enemy.hp) + '\n' )
		if initiative > 50:
			hero_hit = random.randint(1,101)
			if hero_hit < (hero.hit_chance - enemy.defense): #factors if the hit is successful based on hit chance and monster defense
				crit_proc = crit_check()
				attack_damage = int(random.randint(int(0.8 * hero.damage), int((hero.damage) * crit_proc)))
				print('You hit for {} damage'.format(attack_damage))
				enemy.health -= attack_damage
			else:
				print('You swing wildly and miss...')
			enemy_hit = random.randint(1,101)
			if enemy_hit < (enemy.hit_chance - hero.defense): #factors if the hit is successful based on hit chance and hero defense
				crit_enemy = crit_monster_check(enemy) #should have been a common function in parent class
				enemy_damage = int(random.randint(int(0.8 * enemy.damage), int((enemy.damage) * crit_enemy)))
				print('You take {} damage'.format(enemy_damage) + '\n')
				hero.health -= enemy_damage
			else:
				print('You successfully dodge the attack' + '\n')
		else:
			enemy_hit = random.randint(1,101)
			if enemy_hit < (enemy.hit_chance - hero.defense): #factors if the hit is successful based on hit chance and hero defense
				crit_enemy = crit_monster_check(enemy) #should have been a common function in parent class
				enemy_damage = int(random.randint(int(0.8 * enemy.damage), int((enemy.damage) * crit_enemy)))
				print('You take {} damage'.format(enemy_damage) + '\n') 
				hero.health -= enemy_damage
			else:
				print('You successfully dodge the attack' + '\n')
			hero_hit = random.randint(1,101)
			if hero_hit < (hero.hit_chance - enemy.defense): #factors if the hit is successful based on hit chance and monster defense
				crit_proc = crit_check()
				attack_damage = int(random.randint(int(0.8 * hero.damage), int((hero.damage) * crit_proc)))
				print('You hit for {} damage'.format(attack_damage) +'\n')
				enemy.health -= attack_damage
			else:
				print('You swing wildly and miss...' + '\n')
		if hero.health <= 0:
			death() #handles death
		elif enemy.health <= 0:
			battle_room_success() #code a common function for clearing battle room that levels you up, drops loot, resets room handler, takes you to next level
		else:
			battle_choices(hero,enemy)

def battle_room_success():
	global level 
	t5 = ('You have cleared level ' +str(level) + '!')
	for character in t5:
		sys.stdout.write(character)
		sys.stdout.flush()
		sleep(0.02)
	print('Your greed bonus has increased')
	print(' ')
	input('Press any key to continue...')
	status()
	hero.greed += 0.1
	print('Greed bonus:' + hero.greed)
	wealth_drop() #pending
	#potion_drop create a potion drop function which drops heals across rooms based on room type and level
	#level_handler() #Create a function that progresses the game across levels 1-5
	#inventory allow player to change inventory
	
def wealth_drop(): #complete this
	global level
	

def death():
	os.system('clear')
	print('  =   =  ====  =  =   ===  =  ===  ===') 
	print('  =====  =  =  =  =   = =  =  ===  = =')
	print('      =  =  =  =  =   = =  =  =    = =')
	print('      =  ====  ====   ===  =  ===  ===') 
	print('')
	print(hero.name + ' the ' + char_class)
	print('Died at level {}'.format(level)) 
	print('Score = ' + str(hero.wealth))

def crit_check():
	if random.randint(1,101) < hero.crit_chance:
		print('You unleash a critical strike')
		return hero.crit_multi
	else:
		return 1

def crit_monster_check(enemy): #combine all crit functions in parent class during refactorization
	if random.randint(1,101) < enemy.crit_chance:
		print('The {} attack you with a critical strike'.format(enemy.name))
		return enemy.crit_multi
	else:
		return 1

def potion(hero,enemy):
	while  hero.pots['small'] > 0 or hero.pots['medium'] > 0 or hero.pots['large'] > 0:
		print('Your Potions:')
		print('1. Small - ' +str(hero.pots['small']))
		print('2. Medium - ' +str(hero.pots['medium']))
		print('3. Large - ' +str(hero.pots['large']))
		consume_pot = input(str('-->' + '\n'))

		if consume_pot == '1':
			if hero.pots['small'] > 0:
				hero.health += 5
				print('You consume a potion and heal 5 HP')
				hero.pots['small'] = hero.pots['small'] - 1
				if hero.health > hero.hp:
					hero.health = hero.hp
				battle_choices(hero,enemy)
			else:
				print('You do not have any small potions!')
				battle_choices(hero,enemy)
			break

		elif consume_pot == '2':
			if hero.pots['medium'] > 0:
				hero.health += 15
				print('You consume a potion and heal 15 HP')
				hero.pots['medium'] = hero.pots['medium'] - 1
				if hero.health > hero.hp:
					hero.health = hero.hp
				battle_choices(hero,enemy)
			else:
				print('You do not have any medium potions!')
				battle_choices(hero,enemy)

		elif consume_pot == '3':
			if hero.pots['large'] > 0:
				hero.health += 30
				print('You consume a potion and heal 30 HP')
				hero.pots['large'] = hero.pots['large'] - 1
				if hero.health > hero.hp:
					hero.health = hero.hp
				battle_choices(hero,enemy)
			else:
				print('You do not have any large potions!')
				battle_choices(hero,enemy)
			break		
		
		else:
			print('Please select a valid input...')
			battle_choices(hero,enemy)

	else:
		print('You do not have any potions...')
		battle_choices(hero,enemy)

def flee(hero,enemy):
	t6 = 'Trying to escape the room...'
	for character in t6:
		sys.stdout.write(character)
		sys.stdout.flush()
		sleep(0.02)
	flee_roll = 50 + hero.agility
	if random.randint(1,101) < flee_roll: 
		print('You successfully escape from the ' + enemy.name)
		junction()
	else:
		print('You can\'t find a way out!')
		enemy_hit = random.randint(1,101)
		if enemy_hit < (enemy.hit_chance - hero.defense): #factors if the hit is successful based on hit chance and hero defense
			crit_enemy = crit_monster_check(enemy) #should have been a common function in parent class
			enemy_damage = int(random.randint(int(0.8 * enemy.damage), int((enemy.damage) * crit_enemy)))
			print('The ' + enemy.name + ' attack you for ' + str(enemy_damage) + ' damage')
			hero.health -= enemy_damage
			status()
			battle_choices(hero,enemy)
			if hero.health <= 0:
				death()
		else:
			print('You dodge an incoming attack' + '\n')
			battle_choices(hero,enemy)


class Monster:
	def __init__(self, monster_data):
		self.name = monster_data['Name']
		self.level = monster_data['Level']
		self.hp = monster_data['HP']
		self.damage = monster_data['Damage']
		self.hit_chance = monster_data['Hit Chance']
		self.crit_chance = monster_data['Crit Chance']
		self.crit_multi = monster_data['Crit Multi']
		self.defense = monster_data['Defense']
		self.health = self.hp



###Gameplay begins

hero, char_class = herosetup()
junction()
#wealth_drop()


