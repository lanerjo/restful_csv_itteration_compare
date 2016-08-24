#imports
import os
import sys
from bottle import route, run, request, post
import csv
from geopy.distance import great_circle


#output results
def return_results(usr_loc):
    usr_loc = usr_loc
    closest_pharm = get_pharma_nearest(usr_loc)
    pharma_name = closest_pharm['pharmacy']
    pharma_dist = closest_pharm['dist']
    pharma_addr = closest_pharm['address','city','state','zip']
    return "Pharmacy name %s, Pharmacy address %s, Distance to Pharmacy %s" % (pharma_name, pharma_addr, pharma_dist)
    return closest_pharm
#process pharmacy csv file
def get_pharma_nearest(usr_loc):
    #pharmacy_options = ()
    currentpath = os.getcwd()
    filename = currentpath + '/pharmacies.csv'
    with open(filename,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        #create a multi-dimensional dictionary with the pharmacy name as keyword
        new_dict = {}
        try:
            for row in reader:
                new_dict[row['name']] ={}
                new_dict[row['name']]['name'] = row['name']
                new_dict[row['name']]['dist'] = {}
                new_dict[row['name']]['address'] = row['address']
                new_dict[row['name']]['city'] = row['city']
                new_dict[row['name']]['state'] = row['state']
                new_dict[row['name']]['zip'] = row['zip']
                
                latt = str(row['latitude']) 
                longi = str(row['longitude'])
                #concantenate latt and longi for use in grate_circle distance calculation
                pharm_loc = latt + ','+ longi
                #add distance from usr_loc for each pharm to dict for each pharm
                new_dict[row['name']]['dist'] = str(calc_dist(usr_loc, pharm_loc))

        except csv.Error as e:
            sys.exit('file %s, line %d, %s' %(filename, reader.line_num, e))
        
        near_pharm = {}
        print new_dict
        near_pharm = get_closest_pharm(new_dict)
        print near_pharm
        #return_dict ={}
        #return_dict = min(new_dict['name'['dist']], key=lambda k: new_dict[k])
        #print return_dict
    return near_pharm
    
#calculate distance in miles from location to nearest pharmacy
def calc_dist(usr_loc, pharm_loc):
    
    return great_circle(usr_loc, pharm_loc).miles

def get_closest_pharm(dicti): #find only the closest pharm and return entry for that pharm
    nearest = min(float(d['dist']) for d in dicti.values())

    print(nearest)

    print([k for k in dicti
        if (dicti[k]['dist']) == nearest])
    return nearest
#this is just a test
'''@route('/hello')
def hello():
    return  get_pharma_nearest()
'''

#get user Location
@route('/start')
def start():
    return'''
        <form method="post">
            Current Latitude: <input name="usr_latt" type="float" />
            Current Longitude: <input name="usr_long" type="float" />
            <input value="Submit" type="submit" />
        </form>
    '''
@post('/start')
def submit():
    #grab data from form
    usr_latt = request.forms.get('usr_latt')
    usr_long = request.forms.get('usr_long')
    usr_loc = usr_latt + ',' + usr_long
    return return_results(usr_loc)
    
run(host='localhost', port=8080, debug=True)