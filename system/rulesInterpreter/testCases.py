from MTGFunctions import *
from system.cardhandling.card import Card

forEachTarget = Card()
card = Card()
activeAbility(forEach(target(num=card.getPower(),repeat=True),damage(forEachTarget, value=1), end=isIllegal(forEachTarget)), cost='RR')

beforeCast(condition(card.getOwner().getMana, len(card.targets), comparison='GreaterEqual', onFalse=counterspell(card)))
onCast(forEach(card.targets, action=condition(forEachTarget.getType(), 'Demon', comparison='Contains', onFalse=damage(forEachTarget, divide(card.manaSpent.getX(),len(card.targets), round="Down")),onTrue=damage(forEachTarget, multiply(divide(card.manaSpent.getX(),len(card.targets),round="Down"),2)))))

activeAbility(forEach(card.targets,tapCard(forEachTarget)),forEach(removeAbilities(forEachTarget, until=forEachTarget.getController().upkeep)), cost='1', tap=True)

keyWords('Deathtouch', 'Menace')
activeAbility(forEach(target(filter='type:Mage OR type:Wizard'),putCounter('Empathy')),cost='2U')
passiveAbility(forEach(target(filter='counter:Empathy'),card.addAbilities(target.getAbilities())))

onCast(pay(discardHand=True,onPay=(player.addCardToHand(library.search('type:Cleric',maxResults=1),reveal=True),player.addCardToHand(library.search('type:Hero', maxResults=1),reveal=True),player.addCardToHand(library.search('type:Mage', maxResults=1),reveal=True),player.addCardToHand(library.search('type:Warrior',maxResults=1),reveal=True),library.shuffle())))
passiveAbility(canBeCommander(True))