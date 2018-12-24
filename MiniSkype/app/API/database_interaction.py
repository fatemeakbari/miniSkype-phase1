import datetime, random
from bson.objectid import ObjectId
from Models import *


def getUserByUsername(username):
    try:
        user = Users.objects(Username=username).first_or_404()
        return user
    except:
        return None


def getUserByUsernameAndPassword(username, password):
    try:
        user = Users.objects(Username=username, Password=password).first_or_404()
        return user
    except:
        return None


def getUserByEmailAndPassword(email, password):
    try:
        user = Users.objects(Email=email, Password=password).first_or_404()
        return user
    except:
        return None


def getUserBySessionID(session_id):
    try:
        user = Users.objects(SessionId=session_id).first_or_404()
        return user
    except:
        return None


def getUserById(id):
    try:
        user = Users.objects(_id=id).first_or_404()
        return user
    except:
        return None


def getMessageById(id):
    try:
        message = Messages.objects(_id=id).first_or_404()
        return message
    except:
        return None


def getDefaultRosters():
    rosters = []
    for i in range(900, 911):
        player = SoccerPlayers.objects(id=i).get_or_404()
        roster = Roster(Player=player)
        rosters.append(roster)

    return rosters


def getDefaultActiveRosters():
    active_rosters = []

    player = SoccerPlayers.objects(id=900).get_or_404().id
    active_rosters.append(player)
    player = SoccerPlayers.objects(id=902).get_or_404().id
    active_rosters.append(player)
    player = SoccerPlayers.objects(id=904).get_or_404().id
    active_rosters.append(player)
    player = SoccerPlayers.objects(id=905).get_or_404().id
    active_rosters.append(player)
    player = SoccerPlayers.objects(id=906).get_or_404().id
    active_rosters.append(player)

    return active_rosters


def insertUser(username, password, email):
    try:
        # load default settings
        stats = Stats()
        rosters = getDefaultRosters()
        active_rosters = getDefaultActiveRosters()
        banner = Banners.objects(id=0).get_or_404()
        formation = Formations.objects(id=0).get_or_404()

        user = Users(Username=username, Password=password, Email=email, Nickname=username, Stats=stats,
                     Owned_Formations=[formation.id], Active_Formation=formation, Owned_Banners=[banner.id],
                     Active_Banner=banner, Roster=rosters, Active=active_rosters, Gem=getConfigs().Initial_Gem,
                     Gold=getConfigs().Initial_Gold, Energy=getConfigs().Initial_Energy)
        user.save()
        return user
    except:
        return None


def insertSession():
    try:
        expire = datetime.datetime.now() + datetime.timedelta(minutes=10)
        session = GuestSessions(Expires=expire)
        session.save()
        return session
    except:
        return False


def getSessionByID(id):
    try:
        return GuestSessions.objects(_id=id).first_or_404()
    except:
        return False


def removeSessionByID(id):
    try:
        GuestSessions.objects(_id=id).first_or_404().delete()
        return True
    except:
        return False


def updateWinStatByUsername(username):
    try:
        user = getUserByUsername(username)
        user.update(inc__Stats__won=1)
        return True
    except:
        return False


def updateLostStatByUsername(username):
    try:
        user = getUserByUsername(username)
        user.update(inc__Stats__lost=1)
        return True
    except:
        return False


def updateActiveBannerByUserObject(user, active_banner):
    try:
        banner = Banners.objects(id=active_banner).first_or_404()
        user.update(set__Active_Banner=banner)
        return True
    except:
        return False


def updateSessionTime(user, extra_time):
    try:
        sesId = ObjectId()
        session_expiration = datetime.datetime.now() + extra_time
        user.update(set__Session_Expiration=session_expiration)
        user.update(set__SessionId=sesId)
        return sesId
    except:
        return False


def getConfigs():
    try:
        return Configurations.objects(_id=0).first_or_404()
    except:
        return False


def findFormationById(id):
    try:
        return Formations.objects(id=id).first_or_404()
    except:
        return None


def findBannnerById(id):
    try:
        return Banners.objects(id=id).first_or_404()
    except:
        return None


def findPowerupById(id):
    try:
        return PowerUps.objects(id=id).first_or_404()
    except:
        return None


def findGiftById(id):
    try:
        return Gift.objects(id=id).first_or_404()
    except:
        return None


def pullUserFromGift(user, gift):
    try:
        gift.update(pull__users=user.Username)
        return True
    except:
        return False


def addUserToGift(user, gift):
    try:
        gift.update(push__users=user.Username)
        return True
    except:
        return False


def reduceGiftRemainingPerson(gift):
    try:
        gift.update(inc__remainingPersons=-1)
        return True
    except:
        return False


def updateNickname(user, new_nickname):
    try:
        user.update(set__Nickname=new_nickname)
        return True
    except:
        return False


def incrementGold(user, amount):
    try:
        user.update(inc__Gold=amount)
        return True
    except:
        return False


def incrementGem(user, amount):
    try:
        user.update(inc__Gem=amount)
        return True
    except:
        return False


def incrementEnergy(user, amount):
    try:
        user.update(inc__Energy=amount)
        return True
    except:
        return False


def incrementRewardMultiplier(user, amount):
    try:
        user.update(inc__Reward_Multiplier=amount)
        return True
    except:
        return False


def addFormationToUser(user, formation_id):
    try:
        user.update(push__Owned_Formations=formation_id)
        return True
    except:
        return False


def addBannerToUser(user, banner_id):
    try:
        user.update(push__Owned_Banners=banner_id)
        return True
    except:
        return False


def findSoccerPlayerById(id):
    try:
        return SoccerPlayers.objects(id=id).first_or_404()
    except:
        return None


def activeRosterFormation(user, players, formation):
    try:
        formation_ref = findFormationById(formation)
        user.update(set__Active=players, set__Active_Formation=formation_ref)
        return True
    except:
        return False


def buyActivePlayer(user, old_roster_index, new_player, index):
    try:
        new_roster = Roster(Player=new_player)
        user.Roster[old_roster_index] = new_roster
        user.Active[index] = new_player.id
        user.save()
        return True
    except:
        return False


def buyNonActivePlayer(user, old_roster_index, new_player):
    try:
        new_roster = Roster(Player=new_player)
        user.Roster[old_roster_index] = new_roster
        user.save()
        return True
    except:
        return False


def buyInjuredHealth(user, player_index, injured_player, price):
    try:
        user.update(pull__Injury_Times=injured_player)
        user.Roster[player_index].Health = 100
        user.Gold -= price
        user.save()
        return True
    except:
        return False


def buyNonInjuredHealth(user, player_index, price):
    try:
        user.Roster[player_index].Health = 100
        user.Gold -= price
        user.save()
        return True
    except:
        return False


def getNews():
    result = []
    try:
        for news in News.objects:
            result.append({'Title': news.Title.encode('utf-8'),
                           'Date': news.Date,
                           'Text': news.Text.encode('utf-8')})
        return result
    except:
        return None


def getFreeGemAmount():
    try:
        return getConfigs().Free_Energy_Amount
    except:
        return 0


def resetFreeEnergyTime(user):
    try:
        user.update(set__FreeEnergy=datetime.datetime.now())
        return True
    except:
        return False


def updateHealthData(user, players_to_update, old_injured_players):
    try:
        healing_time = datetime.datetime.now() + datetime.timedelta(days=7)
        for element in players_to_update:
            if element[1] <= 0:
                # injured player
                user.Roster[element[0]].Health = 0

                if user.Roster[element[0]].Player.id not in old_injured_players:
                    injured_player = InjuryTimes(Player=user.Roster[element[0]].Player, Time=healing_time)
                    user.Injury_Times.append(injured_player)

            else:
                user.Roster[element[0]].Health = int(element[1])
        user.save()
        return True
    except:
        return False


def addFriendRequest(friend, user, message):
    try:
        friend_request = Friend(FriendUsername=user.Username, Message=message)
        friend.update(push__Pending=friend_request, inc__Pending_Count=1)
        return True
    except:
        return False


def acceptFriendRequest(user, friend):
    for f in user.Pending:
        if f.FriendUsername == friend.Username:
            pulling_item = f
    friend.update(push__Friends=user.Username, inc__Friends_Count=1)
    user.update(push__Friends=friend.Username, inc__Friends_Count=1, inc__Pending_Count=-1,
                pull__Pending=pulling_item)


def rejectFriendRequest(user, friend):
    for f in user.Pending:
        if f.FriendUsername == friend.Username:
            pulling_item = f
    user.update(inc__Pending_Count=-1, pull__Pending=pulling_item)


def removeFriend(user, friend):
    try:
        user.update(pull__Friends=friend.Username, inc__Friends_Count=-1)
        friend.update(pull__Friends=user.Username, inc__Friends_Count=-1)
        return True
    except:
        return False


def findMessageByUsernames(user1, user2):
    try:
        message = Messages.objects(one_side=user1, other_side=user2).first_or_404()
        if message is None:
            message = Messages.objects(one_side=user2, other_side=user1).first_or_404()
        return message
    except:
        try:
            message = Messages.objects(one_side=user2, other_side=user1).first_or_404()
            return message
        except:
            return None


def pushToMessages(message, sender, other_side, text):
    m = Message(sender=sender, message=text, read=True)
    message.update(push__message=m)
    other_side_message = Message(sender=sender, message=text)
    other_side.update(push__message=other_side_message)
    return True


def createAndPushToMessages(one_side, other_side, sender, text):
    m = Message(sender=sender, message=text, read=True)
    message = Messages(one_side=one_side, other_side=other_side)
    message.message.append(m)
    message.save()

    m = Message(sender=sender, message=text)
    message = Messages(one_side=other_side, other_side=one_side)
    message.message.append(m)
    message.save()
    return True


def setLastFreeReward(user):
    try:
        user.update(set__Last_Free_Reward=datetime.datetime.now())
        return True
    except:
        return False


def restartRewardMultiplier(user):
    try:
        user.update(set__Reward_Multiplier=0)
        return True
    except:
        return False


def activePowerup(user, player_index, powerup):
    try:
        user.Roster[player_index].activePowerUps = powerup
        user.save()
        return True
    except:
        return False


def purchasePowerup(user, player_index, powerup):
    try:
        roster_powerup = RosterPowerups(id=powerup.id,
                                        expireTime=datetime.datetime.now() + datetime.timedelta(days=powerup.Duration))
        user.Roster[player_index].Powerups.append(roster_powerup)
        user.Roster[player_index].activePowerUps = powerup.id
        user.save()
        return True
    except:
        return False


def removePowerup(user, player_index, powerup):
    try:
        user.Roster[player_index].Powerups.remove(powerup)
        if powerup.id == user.Roster[player_index].activePowerUps:
            user.Roster[player_index].activePowerUps = -1
        user.save()
        return True
    except:
        return False


def upgradeGuestUser(user, nickname, password, email):
    try:
        user.update(set__Nickname=nickname, set__Password=password, set__Email=email)
        return True
    except:
        return False


def setUserImage(user):
    try:
        user.update(set__Image=True)
        return True
    except:
        return False


def createGame(firstPlayer, secondPlayer, time, league):
    gameObj = Games(firstPlayer=firstPlayer, secondPlayer=secondPlayer, time=time, league=league)
    gameObj.save()
    return gameObj.id


def findGameById(gameId):
    game = Games.objects(id=gameId).first_or_404()
    return game


def updateGameResultByGameObject(game, player1goals, player2goals):
    game.update(set__firstPlayerGoals=player1goals,
                set__secondPlayerGoals=player2goals,
                set__gameFinished=True)


def updateLastTenResult(winner, loser):
    if winner != "AI":
        user = getUserByUsername(winner)
        lastTen = user.LasTenGameStatus
        lastTen = lastTen[-1:] + lastTen[:-1]
        lastTen[0] = 1
        user.LasTenGameStatus = lastTen
        user.save()

    if loser != "AI":
        user = getUserByUsername(loser)
        lastTen = user.LasTenGameStatus
        lastTen = lastTen[-1:] + lastTen[:-1]
        lastTen[0] = 0
        user.LasTenGameStatus = lastTen
        user.save()


def getTotalMessages(userName):
    try:
        return Messages.objects(one_side=userName)
    except:
        return None


def getFriendMessages(userName, friend):
    try:
        return Messages.objects(one_side=userName, other_side=friend).first_or_404()
    except:
        return None


def getVideoPrize():
    return getConfigs().Video_Prize


def checkVideoToken(user, token):
    try:
        tokenObj = VideoTokens.objects(TokenId=token).first()
        if tokenObj:
            return False
        else:
            tokenObj = VideoTokens(User=user, TokenId=str(token))
            tokenObj.save()
            return True
    except:
        return False


def resetVideoAwardTime(user):
    try:
        user.update(set__Last_Video_Award=datetime.datetime.now())
        return True
    except:
        return False


def getLeaguePrice(league_id):
    leagues = getConfigs().Leagues
    return leagues[league_id].Price


def getLeagueById(league_id):
    leagues = getConfigs().Leagues
    return leagues[league_id]


def getGemPackById(package_id):
    try:
        gem_packs = getConfigs().Gem_Packs
        for pack in gem_packs:
            if pack.Package_ID == package_id:
                return pack
        return False
    except:
        return False


def checkTransactionExistance(token_id):
    tokenObj = Transactions.objects(TokenId=token_id).first()
    if tokenObj:
        return True
    else:
        return False


def setTransaction(user, purchase_token, package_id, gem_pack):
    transaction_obj = Transactions(
        User=user,
        TokenId=purchase_token,
        PackageId=package_id,
        TransactionPrice=str(gem_pack.Discount_Price)
    )
    transaction_obj.save()


def getRequiredXpForLevel(level):
    xp = Experience.objects(Level=level).first()
    return xp.XP


def incrementXp(user, amount):
    try:
        user.update(inc__Exp=amount)
        return True
    except:
        return False


def incrementLevel(user):
    try:
        user.update(inc__Level=1)
        return True
    except:
        return False


def getRandomPlayerById(level):
    users = Users.objects(Level=level)
    if len(users) == 0:
        for i in range(1, 6):
            users = Users.objects(Level=level + i)
            if len(users) != 0:
                index = random.randint(0, len(users) - 1)
                return users[index].Username
            users = Users.objects(Level=level - i)
            if len(users) != 0:
                index = random.randint(0, len(users) - 1)
                return users[index].Username
        return "Not Found"

    else:
        index = random.randint(0, len(users) - 1)
        return users[index].Username


def getAIUserNames():
    return ['ai1', 'ai2', 'ai3', 'ai4', 'ai5']


if __name__ == '__main__':
    pass
