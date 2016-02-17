

'''
Generic class for a cell phone provider.

This class holds all of the relevant details for all of the classes. Each
individual class uses whatever variables it needs from this global class.


Todo: Refactor to have more classes? Types of minutes :( I don't think anyone cares
  * Store the math for each phone in a hover-over on a data point. I apparently don't trust my code!
  * US Mobile is 1/2 the price?!
  *
'''
from browser import document
import math

#Cost = Enum('Cost','Access Monthly Initial')
#Network = Enum('Network','Verizon Sprint ATT TMobile')

# Might not need a full class, but going ahead for now
class Device(object):
    def __init__(self, megabytes=10, minutes=100, texts=100, network=[]):
        self.megabytes = megabytes
        self.minutes = minutes
        self.texts = texts
        self.network = network
            
class TalkTextPhone(Device):
    pass

class SmartPhone(Device):
    pass
'''
# This distinction really only matters for one carrier (Republic Wireless)
# who only has android phones with custom ROM's. Best to not confuse the UI
# and make a caveat clear on the website
class iPhonePhone(SmartPhone):
    pass
class AndroidPhone(SmartPhone):
    pass
'''

class Tablet_Hotspot(Device):
    pass
class iPadTablet(Tablet_Hotspot):
    pass
class AndroidTablet(Tablet_Hotspot):
    pass

class CellProvider():
    
    def Compute(self, devices, minutesPercentNightsWeekends=0, minutesPercentInNetwork=0,
                minutesPercentInternational=0,):
        return 0
 
'''
See PDF in the folder
'''
def VerizonPlan(devices):
    dictOut = {}
    
    dictOut['Network'] = 'Verizon'
    dictOut['calc'] = ''
    
    # Device access price
    dictOut['CostMonthly'] = 0
    for device in devices:
        # Same price for smart or non-smart device
        if type(device) is SmartPhone:
            dictOut['CostMonthly'] += 20
        elif type(device) is TalkTextPhone:
            dictOut['CostMonthly'] += 20
        elif type(device) is Tablet_Hotspot:
            dictOut['CostMonthly'] += 10
        else:
            dictOut['CostMonthly'] += 5
            
     
    # It'll be cheapest to lump everyone on the same plan with verizon
    # I think...
    dictOut['megabytesTotal'] = 0
    dictOut['minutesTotal'] = 0
    dictOut['textsTotal'] = 0
    for device in devices:
        dictOut['megabytesTotal'] += device.megabytes
        dictOut['minutesTotal'] += device.minutes
        dictOut['textsTotal'] += device.texts

    # Unlimited texting on all plans
    return dictOut
    
def Verizon700Minutes(devices):
    dictOut = VerizonPlan(devices)
    dictOut['name'] = 'Verizon 700 Minutes'
    
    # Can't have smartphones on this plan :(
    for device in devices:
        assert type(device) is not SmartPhone, "No smartphones allowed on this plan"
    
    # $1.99/MB data
    dictOut['CostMonthly'] += float(dictOut['megabytesTotal'])*1.99
    
    # Minutes
    # $5/month access to 700 + promo minutes
    dictOut['CostMonthly'] += 5
    # In-network and nights&weekends free.
    percentPromo = 0
    for promo in ['minutesPercentNightsWeekends','minutesPercentInNetwork']:
        if promo in dictOut:
            percentPromo += dictOut['minutesPercentNightsWeekends']
        
    dictOut['minutesTotal'] -= dictOut['minutesTotal'] * percentPromo
    
    #$.45 / minute overage
    if dictOut['minutesTotal'] > 700:
        dictOut['CostMonthly'] += (dictOut['minutesTotal'] - 700)*.45
                             
    # Messages
    # Unlimited!!
    dictOut['calc'] += 'Verizon 700 Minutes Shared Plan: $%.02f\n' % (dictOut['CostMonthly'])
    
    return dictOut
        
def VerizonPlanDataShare(devices):
    '''
    Maybe generate all possible plans and store somewhere. Helpful to know
    costs of overage and not just "cheapest plan"
    '''
    dictOut = VerizonPlan(devices)
    dictOut['name'] = 'Verizon Plan Data Share'
    # Pick the cheapest plan of the 6 possible
    megabytes   = [1000,3000,6000,12000,18000]
    bases       = [  30,  45,  60,   80,  100]
    costs  = []
    for i in range(len(megabytes)):
        costs.append(bases[i] + dictOut['CostMonthly'])
        # Base + overage, rounded up to nearest GB
        if dictOut['megabytesTotal'] > megabytes[i]:
            costs[i] += math.ceil((dictOut['megabytesTotal'] - megabytes[i])/1000.0) * 15

        dictOut['calc'] += 'Verizon Share %dGB Plan: $%.02f\n' % (megabytes[i]/1000,
                                                        costs[i])
        
    return dictOut



'''
def VerizonMoreEverything(**kwargs):
    access = 40*kwargs['smartPhones'] + 30*kwargs['dumbPhones']
            #+ 20*kwargs['devices'] + 10*kwargs['tablets']
'''

def USMobile(devices):
    dictOut = {}
    dictOut['Network'] = 'TMobile'
    dictOut['name'] = 'US Mobile'
    dictOut['calc'] = ''
    dictOut['CostMonthly'] = 2 #monthly maintenance fee
    minutesBins = [(100,3),(250,5),(500,9),(1500,10),(5000,15)]
    textsBins = [(100,2),(250,3),(500,4),(1000,5),(5000000000,7)]
    megabytesBins = [(100,2),(250,5),(500,9),(1000,14),(2500,25),(5000,35)]
    
    # It appears you just run out of stuff in your account and then
    # top up if you are over. Probably better to just buy a larger bin?
    
    # No group rates. One device at a time
    # Shorten the code by processing all the bins the same way
    for device in devices:
        for (bins, amount, name) in [(minutesBins,device.minutes,'minutes'),    \
                             (textsBins,device.texts,'texts'),          \
                             (megabytesBins,device.megabytes,'megabytes')]:
            if amount == 0:
                # No cost
                continue
            
            # Pick the "rounded up" one, as it looks cheapest/ least confusing
            cost = 0
            for i in range(len(minutesBins)-1):
                if amount >= bins[i][0] and \
                   amount < bins[i+1][0]:
                    cost = bins[i+1][1]
            if cost == 0:
                # Big user that needs more than the max. Hm...
                # I seem to remember this being a dynamic programming problem
                # Todo: Make this work. Maybe use mod
                
                # raise Exception('Over max plan %s, compute cost yourself for now'%(name))
                cost = 9999999
            
            dictOut['CostMonthly'] += cost
    dictOut['calc'] += 'US Mobile Monthly Plan (Round Up Each Line Usage): $%.02f\n' \
        % (dictOut['CostMonthly'])
                
             
    return dictOut

def PagePlus(devices):

    # No group discounts. Do device by device

    dictOut = {}
    # No device connection costs
    dictOut['CostMonthly'] = 0
    dictOut['Network'] = 'Verizon'
    return dictOut

def PagePlusMonthly(devices):
    dictOut = PagePlus(devices)
    dictOut['name'] = "Page Plus Monthly"
    dictOut['calc'] = ''
    inf = float('inf')
    bases = [12, 29.95, 39.95, 55.00, 69.95]
    minutes = [250, 1500, inf, inf, inf]
    texts = [250, inf, inf, inf, inf]

    # For last 3 plans, 2G data is unlimited
    # Todo: Express this correctly

    megabytes = [10, 1000, 1500, 5000, 7000]

    costs = []
    # Figure out the costs for each plan
    for i in range(len(bases)):
        costs.append(dictOut['CostMonthly'])
        for device in devices:
            costs[i] += bases[i]

            # Now compute overage charges
            # $.05 for minutes and texts, $.10 for megabytes
            if device.minutes > minutes[i]:
                costs[i] += (device.minutes - minutes[i]) * .05
            if device.texts > texts[i]:
                costs[i] += (device.texts - texts[i]) * .05
            if device.megabytes > megabytes[i]:
                costs[i] += (device.megabytes - megabytes[i]) * .10

        dictOut['calc'] += 'Page Plus Monthly %.02f Plan: $%.02f\n' % (bases[i],
                costs[i])

    return dictOut


def PagePlusPayAsYouGo(devices):
    dictOut = PagePlus(devices)
    dictOut['name'] = "Page Plus Pay As You Go"
    dictOut['calc'] = ''
    bases = [10.0, 25.0, 50.0, 80.0]
    expirationMonths = [4, 4, 4, 12]
    costPerMinute = [.10, .06, .05, .04]
    costPerText = .05
    costPerMegabyte = .10

    costs = []
    for i in range(len(bases)):
        costs.append(dictOut['CostMonthly'])
        for device in devices:

            # Expand minutes to yearly amount, then pick the monthly cost if
            # you purchased a new card when you needed it. Try to include
            # the utility of the card after the period ends.
            # Not that great of a model, but works for now.

            # How many months will the card last?

            moneyUsedPerMonth = costPerMinute[i] * device.minutes \
                + costPerText * device.texts + costPerMegabyte \
                * device.megabytes
            monthsCardLasts = bases[i] / moneyUsedPerMonth

            # If you're a light user, you have to pay a minimum cost
            
            if monthsCardLasts > expirationMonths[i]:
                monthsCardLasts = expirationMonths[i]

            # Calculate cost per month
            costs[i] = bases[i] / monthsCardLasts

        dictOut['calc'] += 'Page Plus Pay As You Go $%d Cards every %.02f months: $%.02f\n' % \
        (bases[i], monthsCardLasts, costs[i])
    

    return dictOut


            
def GoogleProjectFi(devices):
    dictOut = {}
    dictOut['calc'] = ''
    dictOut['name'] = 'Google Project Fi'
    dictOut['CostMonthly'] = 0
    for device in devices:
        # $20 connection *with a custom ROM Android* basically brand new, that's it
        # Uses wifi and lots of other networks for when you travel internationally
        dictOut['CostMonthly'] += 20
    
    dictOut['calc'] += 'Google Project Fi: $%.02f\n'%(dictOut['CostMonthly'])
   
    return dictOut



#def RepublicWireless(**kwargs):
    
    # Have to buy one of their custom ROM **android-only** phones. However,
    # you can buy used ones off of Craigslist/ebay
    # Try the new phone out for 30 days free
    # Network is Sprint and wifi, and maybe switches to *voice* network 
    # (not 3g voip)
    
    # Hybrid calling is supposedly quite seamless
    
    # $15 / GB data

    # You buy data in .5GB, 1GB, 2GB, 3GB buckets. They expire in a month, but
    # but then get credited as MB used / 1024 MB * $15 in next month. Sweet!
    # Source: https://community.republicwireless.com/docs/DOC-1654#jive_content_id_FAQ

"""
   
class PagePlus():
    def Compute(self, minutes, texts, megabytes, dumbPhones=0, smartPhones=1,
                minutesPercentNightsWeekends=0, minutesPercentInNetwork=0,
                minutesPercentInternational=0,):
        pass
        
        
    '''
    Things to add:
    
    -wikipedia page
    -plans website
    -Cell Network it uses
    --Coverage map (coverage in local area), use OpenSignal
    -Time period we're using the plan for (some might have introductory
    rates, esp cable tv providers...)
    
    
    
    Man there's a lot of gimmicks that cell providers put into place to get
    you to stay with their plans. Nights & weekends free, free to in-network
    people...
    
    
    We're assuming no international calls for now
    '''
"""

            
def ProcessDevices(devices):
   finalString = ''
   for plan in [VerizonPlanDataShare,Verizon700Minutes,USMobile,PagePlusMonthly,PagePlusPayAsYouGo,GoogleProjectFi]:
        try:
            dictOut = plan(devices)
        except AssertionError as e:
            finalString += '%s: NA, %s\n\n'%(plan.__name__,e)
            continue
        finalString += '%s\n'%(dictOut['calc'])
   return finalString



   

    

