#GroceryStoreSim.py
#Name:
#Date:
#Assignment:
import simpy
import random
eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.choice ([5, 20, 15, 10, 10, 10, 15, 15])
    shoppingTime = items // 2
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)

            customer = waitingShoppers.pop(0)
            items = customer[1]
            checkoutTime = items // 10 + 2
            yield env.timeout(checkoutTime)

            eventLog.append((customer[0], customer[2], customer[3], env.now))

def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        newShopper = random.randint(1,4)
        yield env.timeout(2)

def processResults():
    totalWait = 0
    totalShoppers = 0

    for e in eventLog:
        waitTime = e[4] - e[3]
        totalWait += waitTime
        totalShoppers += 1

    avgWait = totalWait / totalShoppers

    print("The average wait time was %.2f minutes" % avgWait)
    print("The total idle time was %d minutes" % idleTime)

def main():
    numberCheckers = 2


    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180 )
    print(len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()

